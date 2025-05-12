from google.cloud import storage
from google.cloud import bigquery
import db_dtypes
import re
from bs4 import BeautifulSoup
import requests
from query import query

print("Starting extraction...")

client = bigquery.Client()

# query = """
# SELECT url -- id, article_id, tipo, testata, title, url, testo, creation_timestamp, category 
# FROM gd-gcp-prd-dp-lake-2-0.gd_gcp_prd_dp_lake_2_bq_0.cms_cms_atex_tutti_contenutieditoriali_snp 
# where tipo = "video"
# and testata = "repubblica"
# and category in ("esteri")
# and creation_timestamp between ("2025-04-01 00:00:00 UTC") and "2025-04-05 00:00:00 UTC"
# order by creation_timestamp desc
# limit 3
# """

def extraction_func ():
    query_ = client.query(query, location = "EU")  # Usa Standard SQL di default (equivalente a --use_legacy_sql=false)
    query_.result()
    print (query_)
    df = query_.to_dataframe()
    urls = df['url'].astype(str).tolist()
    return (urls)


def extract_video_url(htlm_content):
    html_string = str(htlm_content)
    pattern = r"https://media\.gedidigital\.it/repubblicatv[^\"\']*\.mp4"
    match = re.search(pattern, html_string)
    return match.group(0) if match else None


def video_extr ():
    video_urls = []
    embed_urls = extraction_func()

    for embed_url in embed_urls:
         response = requests.get(embed_url)
         soup = BeautifulSoup(response.content, 'html.parser')
         video_url = extract_video_url(soup)
         if video_url:
             video_urls.append(video_url)
    print (video_urls)         

    return video_urls
