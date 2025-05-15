from google.cloud import storage
from google.cloud import bigquery
import db_dtypes
import re
from bs4 import BeautifulSoup
import requests
from query import query
import pandas as pd
#from query import query

#with open("input/query.txt", "r", encoding="utf-8") as f:
 #   query = f.read()

print("Starting extraction...")

client = bigquery.Client()

def extraction_func ():
    query_ = client.query(query, location = "EU")  # Usa Standard SQL di default (equivalente a --use_legacy_sql=false)
    query_.result()
    print (query_)
    df = query_.to_dataframe()
    urls = df['url'].astype(str).tolist()
    #print(urls)
    return (urls)


def extract_video_url(htlm_content):
    html_string = str(htlm_content)
    pattern = r"https://media\.gedidigital\.it/repubblicatv[^\"\']*\.mp4"
    match = re.search(pattern, html_string)
    return match.group(0) if match else None


def video_extr ():
    data = []
    video_urls = []
    embed_urls = extraction_func()

    for embed_url in embed_urls:
         response = requests.get(embed_url)
         soup = BeautifulSoup(response.content, 'html.parser')
         video_url = extract_video_url(soup)

         data.append({
            'website_url': embed_url,
            'tvmanager_url': video_url
        })
         
         if video_url:
             video_urls.append(video_url)
    #print (embed_urls, video_urls) 

    df = pd.DataFrame(data)
    df.to_csv('url_video_tvmanager.csv', index=False)        

    return video_urls


#video_extr_url()