import requests
import json
import time

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

if response.status_code == 202:
    print("✅ Картинка успешно загружается на Яндекс диск!")
    
    # Ждем 5 секунд, чтобы картинка успела загрузиться
    print("⏳ Ожидаем завершения загрузки...")
    time.sleep(5)

# информация о картинке
    params = {
        'path': f'{group_name}/{filename}.jpg',
        'fields': 'name,path,size,created,modified,' 
    }
    
    response = requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                           headers=headers, params=params)
    if response.status_code == 200:
        file_info = response.json()
        print(f"✅ Информация о файле получена!")
        print(f"📁 Имя файла: {file_info.get('name')}")
        print(f"📐 Размер файла: {file_info.get('size', 'неизвестно')} байт")

# запись в json
        json_filename = f"{filename}_info.json"
        file_info = response.json()
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(file_info, json_file, ensure_ascii=False, indent=2)
        print(f"💾 Метаинформация сохранена в файл: {json_filename}")

        params = {
            'path': f'{group_name}/{json_filename}',
            'overwrite': 'true'
        }
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                               headers=headers, params=params)
        
        if response.status_code == 200:
            upload_url = response.json()['href']
            with open(json_filename, 'rb') as f:
                upload_response = requests.put(upload_url, files={'file': f})
    
            if upload_response.status_code == 201:
                print(f"✅ JSON файл успешно загружен на Яндекс диск!")
            else:
                print(f"❌ Ошибка при загрузке JSON файла: {upload_response.status_code}")
                print(f"📄 Ответ сервера: {upload_response.text}")
        else:
            print(f"❌ Ошибка при получении ссылки для загрузки: {response.status_code}")
            print(f"📄 Ответ сервера: {response.text}")

        
    else:
        print(f"❌ Ошибка при получении метаинформации: {response.status_code}")
        print(f"📄 Ответ сервера: {response.text}")
        
else:
    print(f"❌ Ошибка при загрузке картинки: {response.status_code}")
    print(f"📄 Ответ сервера: {response.text}")