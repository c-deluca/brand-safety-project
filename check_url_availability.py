import requests
import time
import pandas as pd


df_dec = pd.read_csv("data/url_dicembre.csv")
video_urls = df_dec["url_tvmanager"].dropna().tolist()[:100]


video_urls = [url.strip() for url in video_urls]

for i, url in enumerate(video_urls, start=1):
    try:
        print(f"\nTesting video {i}: {url}")
        start = time.time()
        response = requests.get(url, stream=True, timeout=10)
        end = time.time()

        print(f"Status code: {response.status_code}")
        print(f"Time to first byte: {round(end - start, 2)} seconds")
        
        if response.status_code != 200:
            print("⚠️ Errore nella risposta. L'URL potrebbe non essere accessibile.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Errore durante l'accesso a {url}: {e}")

