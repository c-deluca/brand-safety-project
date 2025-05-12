from google.cloud import storage
from google.cloud import bigquery
import db_dtypes
import re
from bs4 import BeautifulSoup
import requests

print("Starting extraction...")

client = bigquery.Client()


# Scrivi la tua query SQL
query = """
SELECT url -- id, article_id, tipo, testata, title, url, testo, creation_timestamp, category 
FROM gd-gcp-prd-dp-lake-2-0.gd_gcp_prd_dp_lake_2_bq_0.cms_cms_atex_tutti_contenutieditoriali_snp 
where tipo = "video"
and testata = "repubblica"
--and category in ("esteri")
and creation_timestamp between ("2025-04-01 00:00:00 UTC") and "2025-04-10 00:00:00 UTC"
order by creation_timestamp desc
limit 2
"""

# Esegui la query
# query_ = client.query(query, location = "EU")  # Usa Standard SQL di default (equivalente a --use_legacy_sql=false)
# query_.result()
# df = query_.to_dataframe()
# df.to_csv('!risultati_query.csv', index=False)




#df.head()
#----

# Ottieni i risultati come lista di righe
#results = query_job.result()

# query_=client.query(query, location = "EU")
# query_.result()

# df=query_.to_dataframe()
# df.head()

def extraction_func ():

    # Esegui la query
    query_ = client.query(query, location = "EU")  # Usa Standard SQL di default (equivalente a --use_legacy_sql=false)
    query_.result()
    print (query_)
    df = query_.to_dataframe()
    #df.to_csv('!!!risultati_query.csv', index=False)
    urls = df['url'].astype(str).tolist()
    return (urls)
    #urls.head()
    #print ("extraction done!")





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


#video_extr()             
#extraction_func()
#video_extr()



#extraction ()

#embed_urls = extraction_func()

# def extract_video_url(html_content):

#     video_urls = []

#     """ Estrae l'URL del video .mp4 dalla pagina HTML """
#     html_string = str(html_content)
#     pattern = r"https://media\.gedidigital\.it/repubblicatv[^\"\']*\.mp4"
#     match = re.search(pattern, html_string)
#     #return match.group(0) if match else None

#     for embed_url in embed_urls:
#         response = requests.get(embed_url)
#         soup = BeautifulSoup(response.content, 'html.parser')
#         video_url = extract_video_url(soup)
    
#     if video_url:
#         video_urls.append(video_url)

#     return video_urls

# extract_video_url(html_content)




####
# def extract_video_url(html_content):
#     """ Estrae l'URL del video .mp4 dalla pagina HTML """
#     html_string = str(html_content)
#     pattern = r"https://media\.gedidigital\.it/repubblicatv[^\"\']*\.mp4"
#     match = re.search(pattern, html_string)
#     return match.group(0) if match else None

# def extract_all_video_urls(embed_urls):
#     """ Estrae tutti gli URL video da una lista di embed_urls """
#     video_urls = []

#     for embed_url in embed_urls:
#         try:
#             response = requests.get(embed_url)
#             soup = BeautifulSoup(response.content, 'html.parser')
#             video_url = extract_video_url(soup)
#             if video_url:
#                 video_urls.append(video_url)
#         except Exception as e:
#             print(f"Errore con {embed_url}: {e}")

#     return video_urls


# video_urls = extract_all_video_urls(embed_urls)
# print(video_urls)