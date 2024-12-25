import requests

URL = "http://localhost:3367/speak"

def speak(text):
    requests.get(URL, params={
        "text": text
    })
    
