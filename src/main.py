from utils import generate_for_videos, clean_json_output, json_to_dataframe
import extraction
import json
from extraction import extraction_func, video_extr
from conf import prompt, generation_config, system_instruction, safety_settings

def main():

    # video_urls = [#" https://media.gedidigital.it/repubblicatv/file/2025/04/09/1096403/1096403-video-rrtv-650-usa_come_non_impugnare_un_fucile.mp4",
    #           "https://media.gedidigital.it/repubblicatv/file/2025/04/09/1096339/1096339-video-rrtv-650-talk2.mp4"]
    
    video_urls = video_extr()
    
    output = generate_for_videos(video_urls, system_instruction, prompt, generation_config, safety_settings)
    cleaned_output = clean_json_output(output)
    df = json_to_dataframe(cleaned_output)


    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_output, f, ensure_ascii=False, indent=4)


    df.to_csv('output.csv', index=False)

    return df
    

if __name__ == "__main__":
    main()

