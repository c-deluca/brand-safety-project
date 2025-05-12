from utils import generate_for_videos, clean_json_output, json_to_dataframe
import extraction
from extraction import extraction_func, video_extr
from conf import prompt, generation_config, system_instruction, safety_settings

def main():

    # video_urls = [#" https://media.gedidigital.it/repubblicatv/file/2025/04/09/1096403/1096403-video-rrtv-650-usa_come_non_impugnare_un_fucile.mp4",
    #           "https://media.gedidigital.it/repubblicatv/file/2025/04/09/1096339/1096339-video-rrtv-650-talk2.mp4"]
    
    video_urls = video_extr()
    
    output = generate_for_videos(video_urls, system_instruction, prompt, generation_config, safety_settings)
    print(output)
    cleaned_output = clean_json_output(output)
    print(cleaned_output)
    df = json_to_dataframe(cleaned_output)
    print("df:", df)

    df.to_csv('!output.csv', index=False)

    return df
    

if __name__ == "__main__":
    main()

