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
