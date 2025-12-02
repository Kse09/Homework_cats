import requests
import json
import time
import urllib.parse


def create_yandex_disk_folder(token, folder_name):
    headers = {'Authorization': token}
    params = {'path': folder_name}
    response = requests.put(
        'https://cloud-api.yandex.net/v1/disk/resources',
        params=params,
        headers=headers
    )
    return response

def load_image_to_disk(token, image_url, folder_name, filename):
    headers = {'Authorization': token}
    params = {
        'url': image_url,
        'path': f'{folder_name}/{filename}.jpg'
    }
    response = requests.post(
        'https://cloud-api.yandex.net/v1/disk/resources/upload',
        headers=headers,
        params=params
    )
    return response

def get_file_info(token, folder_name, filename):
    headers = {'Authorization': token}
    params = {
        'path': f'{folder_name}/{filename}.jpg',
        'fields': 'name,path,size'
    }
    response = requests.get(
        'https://cloud-api.yandex.net/v1/disk/resources',
        headers=headers,
        params=params
    )
    return response

def save_file_info_to_json(file_info, filename):
    json_filename = f"{filename}_info.json"
    with open(json_filename, 'w', encoding='utf-8') as json_file:
        json.dump(file_info, json_file, ensure_ascii=False, indent=2)
    return json_filename


def main():
    text_for_image = input("Введите текст для картинки: ").strip()
    filename = text_for_image.replace(' ', '_')
    yandex_token = input("Введите яндекс-токен: ").strip()
    group_name = "FPY-140"
    encoded_text_url = urllib.parse.quote(text_for_image)
    image_url = f"https://cataas.com/cat/says/{encoded_text_url}"
    folder_creation = create_yandex_disk_folder(yandex_token, group_name)
    load_picture = load_image_to_disk(yandex_token, image_url, group_name, filename)
    if load_picture.status_code == 202:
        print("Картинка загружается на яндекс диск")
        time.sleep(5)
        file_info_response = get_file_info(yandex_token, group_name, filename)
        if file_info_response.status_code == 200:
            file_info = file_info_response.json()
            json_filename = save_file_info_to_json(file_info, filename)
            print("Данные о картинке загружаются в json файл")
        
        
if __name__ == '__main__':
    main()
