import requests

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