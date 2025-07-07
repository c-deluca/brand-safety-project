from utils import generate_for_videos, clean_json_output, json_to_dataframe, generate_for_videos_prova
import extraction
import json, pandas as pd
from extraction import extraction_func, video_extr
from conf import generation_config, system_instruction, safety_settings

with open("prompt.txt", "r", encoding="utf-8") as f:
     prompt = f.read()
    

def main():

    #video_urls = [" https://media.gedidigital.it/repubblicatv/file/2025/04/09/1096403/1096403-video-rrtv-650-usa_come_non_impugnare_un_fucile.mp4","https://media.gedidigital.it/repubblicatv/file/2025/04/09/1096339/1096339-video-rrtv-650-talk2.mp4"]
    
    #video_urls = video_extr() -- per ricavare link tvmanager da html

    #df_dec = pd.read_csv("data/url_dicembre.csv") # -- link dicembre '24 per analisi preliminare
    #video_urls = df_dec["url_tvmanager"].dropna().tolist()[8:10]

    video_urls = ["https://media.gedidigital.it/repubblicatv/file/2024/12/03/1038543/1038543-video-rrtv-1200-videoverticaleneveusa.mp4",
                  "https://media.gedidigital.it/repubblicatv/file/2024/12/29/1050575/1050575-video-rrtv-1200-291224onde.mp4",
                  "https://media.gedidigital.it/repubblicatv/file/2024/12/24/1049204/1049204-video-rrtv-1200-241224_bufera.mp4",
                  "https://media.gedidigital.it/repubblicatv/file/2024/12/24/1049258/1049258-video-rrtv-1200-241224_abruzzo.mp4",
                  "https://media.gedidigital.it/repubblicatv/file/2024/12/29/1050575/1050575-video-rrtv-1200-291224onde.mp4", 
                  "https://media.gedidigital.it/repubblicatv/file/2024/12/23/1048709/1048709-video-rrtv-1200-231224eliturchia.mp4",
                  "https://media.gedidigital.it/repubblicatv/file/2024/12/02/1038172/1038172-video-rrtv-1200-0212indiaok.mp4"]

    output = generate_for_videos_prova(video_urls, system_instruction, prompt, generation_config, safety_settings)
    cleaned_output = clean_json_output(output)
    df = json_to_dataframe(cleaned_output)


    with open("output/output_fix.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_output, f, ensure_ascii=False, indent=4)


    df.to_csv('output/output_fix.csv', index=False)

    return df
    
if __name__ == "__main__":
    main()

