# import requests
# import time

# url = "https://media.gedidigital.it/repubblicatv/file/2024/12/03/1038518/1038518-video-rrtv-1200-processo_turetta_gino_cecchettin.mp4"
# url = "https://media.gedidigital.it/repubblicatv/file/2024/12/03/1038480/1038480-video-rrtv-1200-241203_idlib_ospedale.mp4"
# #url = "https://media.gedidigital.it/repubblicatv/file/2024/12/04/1039380/1039380-video-rrtv-1200-241204_georgia.mp4"
# #url = "https://media.gedidigital.it/repubblicatv/file/2024/12/04/1039203/1039203-video-rrtv-1200-videolasopranaorizzontale.mp4"

# start = time.time()
# response = requests.get(url, stream=True)
# end = time.time()

# print("Status code:", response.status_code)
# print("Time to first byte:", end - start, "seconds")

import requests
import time
import pandas as pd


df_dec = pd.read_csv("url_dicembre.csv")
video_urls = df_dec["url_tvmanager"].dropna().tolist()[:100]

# Rimuove eventuali spazi iniziali
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

