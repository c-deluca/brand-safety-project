from google.cloud import storage
from google.cloud import bigquery

import json
import re

import requests, time
from bs4 import BeautifulSoup

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from tqdm import tqdm
import pandas as pd


def extract_video_url(html_content):
    """ Estrae l'URL del video .mp4 dalla pagina HTML """
    html_string = str(html_content)
    pattern = r"https://media\.gedidigital\.it/repubblicatv[^\"\']*\.mp4"
    match = re.search(pattern, html_string)
    return match.group(0) if match else None

def generate_for_videos(video_urls, system_instruction, prompt, generation_config, safety_settings):

    vertexai.init(project="gd-gcp-env-dp-lab-hub-1", location="europe-west1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
        system_instruction=system_instruction
    )

    results = {}

    for idx, video_url in enumerate(tqdm(video_urls, desc="Processing Videos")):
        
        print(f"Processing video {idx + 1}: {video_url}")
        try:

            video = Part.from_uri(
                mime_type="video/mp4",
                uri=video_url
            )

        
            start = time.time()
            response = requests.get(video_url, stream=True, timeout=10)
            end = time.time()

            print(f"Status code: {response.status_code}")
            print(f"Time: {round(end - start, 2)} seconds")

            responses = model.generate_content(
                [video, prompt],
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=True,
            )

            generated_text = ""
            for response in responses:
                generated_text += response.text

            results[video_url] = generated_text
            print(f"Completed processing for video {idx + 1}. {generated_text[10:-5]}")

        except Exception as e:
            # Gestisci gli errori e continua con il prossimo video
            print(f"Errore durante l'elaborazione del video {idx + 1}: {e}")
            results[video_url] = f"Errore: {e}"

    return results

#video_urls = [" https://media.gedidigital.it/repubblicatv/file/2025/04/09/1096403/1096403-video-rrtv-650-usa_come_non_impugnare_un_fucile.mp4",
 #             "https://media.gedidigital.it/repubblicatv/file/2025/04/09/1096339/1096339-video-rrtv-650-talk2.mp4"]


def clean_json_output(raw_output):
    cleaned_output = {}
    
    for key, value in raw_output.items():
        try:
            match = re.search(r"\{.*\}|\[.*\]", value, re.DOTALL)
            if match:
                json_content = match.group(0)  
                parsed_json = json.loads(json_content)
                cleaned_output[key] = parsed_json
            else:
                cleaned_output[key] = "Errore: contenuto JSON non trovato"
        except json.JSONDecodeError:
            cleaned_output[key] = "Errore nella decodifica del JSON"
    
    return cleaned_output


def json_to_dataframe(cleaned_json):

    data = []

    for link, content in cleaned_json.items():

        if isinstance(content, dict):
            presenza_violenza = content.get("violenza_presente", None)
            category = content.get("categorie_violenza", [])
        elif isinstance(content, list) and len(content) > 0 and isinstance(content[0], dict):
            presenza_violenza = content[0].get("presenza_violenza", None)
            category = content[0].get("category", [])
        else:

            presenza_violenza = None
            category = []

        data.append({
            "link_video": link,
            "presenza_violenza": presenza_violenza,
            "category": category
        })

    df = pd.DataFrame(data)
    return df



def generate_for_videos_prova(video_urls, system_instruction, prompt, generation_config, safety_settings):

    vertexai.init(project="gd-gcp-env-dp-lab-hub-1", location="europe-west1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
        system_instruction=system_instruction
    )

    results = {}

    for idx, video_url in enumerate(tqdm(video_urls, desc="Processing Videos")):
        print(f"\nProcessing video {idx + 1}: {video_url}")
        video_url = video_url.strip()  # Rimuove eventuali spazi

        success = False
        max_attempts = 10
        attempt = 0

        while not success and attempt < max_attempts:
            attempt += 1
            print(f"Tentativo {attempt} per video {idx + 1}")

            try:
                # Test velocità accesso URL (opzionale)
                start = time.time()
                response = requests.get(video_url, stream=True, timeout=10)
                end = time.time()
                print(f"Status code: {response.status_code}, Time: {round(end - start, 2)} seconds")
                #print(f"Time: {round(end - start, 2)} seconds")

                # Se il link è irraggiungibile, alza eccezione
                if response.status_code != 200:
                    raise Exception(f"HTTP {response.status_code} - URL non accessibile")

                # Prepara il video
                video = Part.from_uri(
                    mime_type="video/mp4",
                    uri=video_url
                )

                # Genera contenuto
                responses = model.generate_content(
                    [video, prompt],
                    generation_config=generation_config,
                    safety_settings=safety_settings,
                    stream=True,
                )

                # Combina i risultati generati
                generated_text = ""
                for response in responses:
                    generated_text += response.text

                results[video_url] = generated_text
                print(f"✅ Completato video {idx + 1}: {generated_text[10:-5]}")
                success = True

            except Exception as e:
                print(f"❌ Errore al tentativo {attempt} per video {idx + 1}: {e}")
                if attempt == max_attempts:
                    print(f"⚠️ Falliti tutti i tentativi per video {idx + 1}")
                    results[video_url] = f"Errore: {e}"
                else:
                    time.sleep(1.5)    

    return results