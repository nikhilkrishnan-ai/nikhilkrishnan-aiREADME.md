<<<<<<< HEAD
import requests

url = "https://static.tp-link.com/upload/firmware/2024/20240115/Archer%20NX200(IN)_V2_240110.zip"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

print("Downloading started...")
response = requests.get(url, headers=headers, stream=True)

if response.status_code == 200:
    with open("firmware.zip", "wb") as f:
        f.write(response.content)
    print("Download Complete! Check your folder for firmware.zip")
else:
    print(f"Failed! Status Code: {response.status_code}")
=======
import sys

import requests

URL = (
    "https://static.tp-link.com/upload/firmware/2024/20240115/"
    "Archer%20NX200(IN)_V2_240110.zip"
)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
}
OUT_PATH = "firmware.zip"
CHUNK_SIZE = 8192


def download_firmware() -> int:
    """Download firmware ZIP; return 0 on success, 1 on failure."""
    print("Downloading started...")
    try:
        with requests.get(
            URL,
            headers=HEADERS,
            stream=True,
            timeout=(10, 300),
        ) as response:
            response.raise_for_status()
            with open(OUT_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
    except requests.RequestException as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 1

    print(f"Download complete: {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(download_firmware())
>>>>>>> 25e03f48e402ed73cfc8b08d481c60e70b885e50
