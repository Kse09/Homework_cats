import requests
import json

text_for_image = input("Введите текст для картинки: ").strip()
yandex_token = input("Введите яндекс-токен: ").strip()
group_name = "FPY-140"
image_url = f"https://cataas.com/cat/says/{text_for_image}"
filename = text_for_image

# папка
headers = {'Authorization': yandex_token}
params = {'path': group_name}
response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                        params=params, headers=headers)

# файл в папку
params = {
    'url': image_url,
    'path': f'{group_name}/{filename}.jpg'
}

response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                         headers=headers, params=params)

# информация о картинке
params = {
        'path': f'{group_name}/{filename}.jpg',
        'fields': 'name,path,size,created,modified,' 
    }
    
response = requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                           headers=headers, params=params)

# запись в json
json_filename = f"{filename}_info.json"
file_info = response.json()
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json.dump(file_info, json_file, ensure_ascii=False, indent=2)