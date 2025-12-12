from __future__ import annotations

from io import BytesIO
from typing import Dict, Any, List, Optional
import os

import cv2
import requests
from PIL import Image


# -------------------------
# Internal helpers
# -------------------------

def _ensure_dir(path: str) -> None:
    """Create parent directory for a file path if needed."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)


# -------------------------
# Heatmap helpers
# -------------------------

def save_heatmap_image(
    media: Dict[str, Any],
    out_path: str,
    participant_id: int = 0,
) -> str:
    """
    Download and save the heatmap as an image for one participant.

    Intended mainly for image model outputs (e.g. AC-1).
    Returns the output path.
    """
    participant = media["participants"][participant_id]
    heatmap_url = participant.get("heatmap", "")
    if not heatmap_url:
        raise RuntimeError("No heatmap URL found for this participant")

    resp = requests.get(heatmap_url, timeout=30)
    if resp.status_code == 404:
        raise RuntimeError(
            "Heatmap not available (404). The presigned URL may have expired; "
            "please re-run detection and save the heatmap soon after."
        )
    resp.raise_for_status()

    img = Image.open(BytesIO(resp.content)).convert("RGB")
    _ensure_dir(out_path)
    img.save(out_path)
    return out_path


def save_heatmap_video(
    media: Dict[str, Any],
    out_path: str,
    participant_id: int = 0,
) -> str:
    """
    Download and save the heatmap video for one participant.

    Intended for video model outputs (e.g. DF-1), where `heatmap`
    is a presigned video URL.
    Returns the output path.
    """
    participant = media["participants"][participant_id]
    heatmap_url = participant.get("heatmap", "")
    if not heatmap_url:
        raise RuntimeError("No heatmap URL found for this participant")

    resp = requests.get(heatmap_url, stream=True, timeout=60)
    if resp.status_code == 404:
        raise RuntimeError(
            "Heatmap not available (404). The presigned URL may have expired; "
            "please re-run detection and save the heatmap soon after."
        )
    resp.raise_for_status()

    _ensure_dir(out_path)
    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return out_path


def save_heatmap(
    media: Dict[str, Any],
    out_path: str,
    participant_id: int = 0,
    model_type: Optional[str] = None,
) -> str:
    """
    Convenience wrapper that chooses image or video heatmap saver
    based on model_type (if provided) or URL extension.

    Returns the output path.
    """
    participant = media["participants"][participant_id]
    heatmap_url = participant.get("heatmap", "")
    if not heatmap_url:
        raise RuntimeError("No heatmap URL found for this participant")

    # Prefer explicit model_type if caller passes it
    if model_type is not None:
        mt = model_type.upper()
        if mt.startswith("AC-"):
            return save_heatmap_image(media, out_path, participant_id=participant_id)
        if mt.startswith("DF-"):
            return save_heatmap_video(media, out_path, participant_id=participant_id)

    # Fallback: simple heuristic based on URL
    lower = heatmap_url.lower()
    if any(lower.endswith(ext) for ext in (".jpg", ".jpeg", ".png", ".bmp")):
        return save_heatmap_image(media, out_path, participant_id=participant_id)
    return save_heatmap_video(media, out_path, participant_id=participant_id)


# -------------------------
# BBox: your existing renderer
# -------------------------

def draw_bounding_boxes(
    video_path: str,
    sequence_dict: Dict[int, List[Dict[str, Any]]],
    result_video_path: str,
) -> None:
    """
    Original bounding-box renderer.

    sequence_dict:
      frame_index (int) -> list of {
        "data": [x1, y1, x2, y2],
        "class": "real" | "fake",
        "confidence": float in [0,1]
      }
    """
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = int(cap.get(5)) or 25

    fourcc = cv2.VideoWriter_fourcc(*"H264")
    _ensure_dir(result_video_path)
    output = cv2.VideoWriter(result_video_path, fourcc, fps, (width, height))

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Check if there are any bounding boxes for the current frame index
        if frame_index in sequence_dict:
            for item in sequence_dict[frame_index]:
                bbox = item["data"]
                class_label = item["class"]
                color = (0, 255, 0) if class_label == "real" else (0, 0, 255)
                confidence = round(item["confidence"] * 100, 2)

                # Unpack bounding box coordinates
                # Note: keep your original *2 scaling
                xmin, ymin, xmax, ymax = map(int, [b * 2 for b in bbox])

                # Draw the bounding box
                cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)

                # Put the class label text
                cv2.putText(
                    frame,
                    f"{class_label} {confidence}%",
                    (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    color,
                    2,
                )

        # Write the processed frame to the output video
        output.write(frame)
        frame_index += 1

    output.release()
    cap.release()


# -------------------------
# Adapter: Authenta -> sequence_dict
# -------------------------

def authenta_to_sequence_dict(
    media: Dict[str, Any],
    participant_id: int = 0,
    default_class: str = "fake",
    default_confidence: float = 1.0,
) -> Dict[int, List[Dict[str, Any]]]:
    """
    Convert Authenta boundingBoxes JSON into sequence_dict format
    expected by draw_bounding_boxes.
    """
    detail_resp = requests.get(media["resultURL"], timeout=30)
    detail_resp.raise_for_status()
    detail = detail_resp.json()

    # detail["boundingBoxes"][str(participant_id)]["boundingBox"]
    # -> frame_idx(str) -> [x1, y1, x2, y2]
    bbox_dict = detail["boundingBoxes"][str(participant_id)]["boundingBox"]

    sequence_dict: Dict[int, List[Dict[str, Any]]] = {}

    for frame_str, bbox in bbox_dict.items():
        frame_idx = int(frame_str)
        item = {
            "data": bbox,                 # [x1, y1, x2, y2] as-is
            "class": default_class,       # "fake" or "real"
            "confidence": default_confidence,
        }
        if frame_idx not in sequence_dict:
            sequence_dict[frame_idx] = []
        sequence_dict[frame_idx].append(item)

    return sequence_dict


def save_bounding_box_video(
    media: Dict[str, Any],
    src_video_path: str,
    out_video_path: str,
    participant_id: int = 0,
) -> str:
    """
    Build sequence_dict from Authenta results and call draw_bounding_boxes.

    Returns the output path.
    """
    sequence_dict = authenta_to_sequence_dict(
        media,
        participant_id=participant_id,
        default_class="fake",       # Authenta: participant.fake == True
        default_confidence=1.0,     # or map from detail JSON if available
    )
    draw_bounding_boxes(src_video_path, sequence_dict, out_video_path)
    return out_video_path
