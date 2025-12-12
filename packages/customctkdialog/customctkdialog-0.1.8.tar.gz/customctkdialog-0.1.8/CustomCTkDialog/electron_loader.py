import os
import sys
import zipfile
import io
import requests
from pathlib import Path

ELECTRON_ZIP_URL = "https://github.com/AceBurgundy/CustomCTkDialog/releases/download/v1.0.0/folder-picker-1.0.0.zip"
PACKAGE_DIR = Path(__file__).parent
EXE_NAME = "folder-picker.exe"
EXE_PATH = PACKAGE_DIR / EXE_NAME

def _supports_input() -> bool:
    """Return True if the process is running in a terminal."""
    return sys.stdin is not None and sys.stdin.isatty()

def _prompt_user() -> bool:
    """
    Ask user whether to download required runtime files.
    If running non-interactively, auto-accept.
    """
    if not _supports_input():
        print("[CustomCTkDialog] Non-interactive environment — auto-downloading files.")
        return True

    print("Some necessary files are required for CustomCTkDialog.folder_picker to work.")
    response: str = input("Download these files now? (Y/n): ").strip().lower()

    if response in ("n", "no"):
        return False

    return True

def _download_with_progress(url: str) -> bytes:
    """Download a file with progress bar and return raw bytes."""
    response: requests.Response = requests.get(url, stream=True)
    response.raise_for_status()

    total: int = int(response.headers.get("content-length", 0))
    downloaded: int = 0
    chunks = []

    print(f"Downloading Electron package ({total/1_000_000:.1f} MB)...")

    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            chunks.append(chunk)
            downloaded += len(chunk)

            if total > 0:
                percent: float = (downloaded / total) * 100
                bar_len: int = 40
                filled_len: int = int(bar_len * percent / 100)
                bar: str = "#" * filled_len + "-" * (bar_len - filled_len)
                print(f"\r[{bar}] {percent:5.1f}%", end="")

    print("\nDownload complete.\n")
    return b"".join(chunks)

def ensure_electron() -> None:
    """
    Ensure the Electron runtime exists.
    If missing:
      - Prompt the user (or auto-accept in non-interactive mode)
      - Download
      - Extract
    """

    # Already present → nothing to do
    if EXE_PATH.exists():
        return

    # User confirmation
    if not _prompt_user():
        print("Download cancelled. folder_picker() will not work without required files.")
        return

    try:
        # Download ZIP bytes
        zip_bytes: bytes = _download_with_progress(ELECTRON_ZIP_URL)

        print("Extracting files...")

        with zipfile.ZipFile(io.BytesIO(zip_bytes) ) as zip:
            zip.extractall(PACKAGE_DIR)

        print("Extraction complete.")

    except Exception as error:
        print("Failed to download required files:", error)
        raise RuntimeError("CustomCTkDialog could not obtain required runtime files.") from error
