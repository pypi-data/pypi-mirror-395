# Authenta Python SDK

Python client for the Authenta API to detect deepfakes and manipulated media using image and video models.

## Installation

Follow the steps below to install the `authenta` package.

### Install from PyPI
```
pip install authenta
```

### (Optional) Local development
```
git clone https://github.com/phospheneai/authenta-python-sdk.git
cd authenta-python-sdk
pip install -e .
```

## Basic functionalities and workflows

The package provides basic functionalities for:

- Uploading images and videos to Authenta
- Running deepfake / AI-generated content detection
- Polling for results and retrieving detection outputs
- Listing and deleting media records via the `/media` endpoints

### 1. Quick detection workflow
```
from authenta import AuthentaClient

client = AuthentaClient(
    base_url="https://platform.authenta.ai/api",  # platform base : https://platform.authenta.ai 
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)

# Upload a file and wait for processing to finish
media = client.process("samples/nano_img.png", model_type="AC-1")
print("Status:", media["status"])
print("Fake:", media.get("fake"))
print("Result URL:", media.get("resultURL"))
print("Heatmap URL:", media.get("heatmapURL"))
```

### 2. Two-step upload and polling
```
from authenta import AuthentaClient

client = AuthentaClient(
    base_url="https://platform.authenta.ai/api",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)

# 1) Upload only
upload_meta = client.upload_file("samples/nano_img.png", model_type="AC-1")
mid = upload_meta["mid"]

# 2) Poll later using the media id
final_media = client.wait_for_media(mid)
print(final_media["status"], final_media.get("fake"))
```

## Model types and usage

Authenta exposes different detection models that you select via the `model_type` parameter.

| Model type | Modality | Description                                           |
|-------------|-----------|-------------------------------------------------------|
| `AC-1`      | Image     | Detects AI-generated or manipulated images.           |
| `DF-1`      | Video     | Detects deepfake or manipulated faces in video content. |

### Detect AI-generated images (`AC-1`)
```
from authenta import AuthentaClient

client = AuthentaClient(
    base_url="https://platform.authenta.ai/api",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)

media = client.upload_file("samples/nano_img.png", model_type="AC-1")
print(media["mid"], media["status"])
```

### Detect deepfake videos (`DF-1`)
```
from authenta import AuthentaClient

client = AuthentaClient(
    base_url="https://platform.authenta.ai/api",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)

media = client.upload_file("samples/video.mp4", model_type="DF-1")
print(media["mid"], media["status"])
```

## Method reference

### `AuthentaClient`

The main entrypoint for interacting with the Authenta API.

#### Initialization
```
from authenta import AuthentaClient

client = AuthentaClient(
    base_url="https://platform.authenta.ai/api",
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
)
```

- `base_url: str` – Authenta API base URL (e.g. `https://platform.authenta.ai/api`).
- `client_id: str` – Your Authenta client ID.
- `client_secret: str` – Your Authenta client secret.

#### `upload_file(path: str, model_type: str) -> Dict[str, Any]`
- Creates a media record via `POST /media` and uploads the file to the returned presigned URL.  
- Returns media JSON including fields such as `mid`, `status`, `modelType`, and timestamps.

#### `wait_for_media(mid: str, interval: float = 5.0, timeout: float = 600.0) -> Dict[str, Any]`
- Polls `GET /media/{mid}` until the status is `PROCESSED`, `FAILED`, or `ERROR`.  
- Sleeps `interval` seconds between polls and raises `TimeoutError` if `timeout` is exceeded.

#### `process(path: str, model_type: str, interval: float = 5.0, timeout: float = 600.0) -> Dict[str, Any]`
- High-level helper that runs `upload_file` followed by `wait_for_media`.  
- Returns the final processed media JSON, including detection outputs like `fake`, `resultURL`, `heatmapURL`, and scores (when available).

#### `get_media(mid: str) -> Dict[str, Any]`
- Fetches the current state of a media record via `GET /media/{mid}`.  
- Returns the parsed JSON media object.

#### `list_media(**params) -> Dict[str, Any]`
- Lists media records for the client using `GET /media`.  
- Supports optional query parameters such as `page`, `pageSize`, or `status` (depending on API support).

#### `delete_media(mid: str) -> None`
- Deletes a media record via `DELETE /media/{mid}`.  
- Raises an HTTP error if the request fails.


[View source on GitHub](https://github.com/phospheneai/authenta-python-sdk/blob/main/src/authenta/authenta_client.py)


