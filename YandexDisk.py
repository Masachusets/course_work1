import json, time, requests
from tqdm import tqdm


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        """Метод получает заголовки"""
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def get_file_list(self):
        """Метод получает список файлов на диске"""
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def get_upload_link(self, disk_file_path):
        """Метод получает ссылку для загрузки файла"""
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': disk_file_path, 'owerwrite': 'true'}
        headers = self.get_headers()
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, file_path: str):
        """Метод загружает файлы на яндекс диск"""
        href_json = self.get_upload_link(disk_file_path=file_path)
        href = href_json['href']
        response = requests.put(href, data=open(file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')

    def upload_url(self, file_path: str, url: str):
        """Метод загружает файл по ссылке на яндекс диск"""
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'url': url, 'path': file_path}
        headers = self.get_headers()
        res = requests.post(upload_url, params=params, headers=headers)
        res.raise_for_status()
        # if response.status_code in [200, 201, 202]:
        #      print('Success')
        return res.json()

    def import_photos_to_disk(self, photos: dict):
        """Метод загружает файлы по ссылкам из словаря на яндекс диск"""
        direct = time.strftime('%y_%m_%d', time.gmtime(time.time()))
        headers = self.get_headers()
        if 'error' not in requests.get('https://cloud-api.yandex.net/v1/disk/resources',
                                       params={'path': direct}, headers=headers).json():
            direct += '_one_more'
        requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                     params={'path': direct}, headers=headers)
        end_list = []
        for name, photo in tqdm(photos.items()):
            self.upload_url(file_path=f'/{dir}/{name}', url=photo['url'])
            end_list.append({'file_name': f'/{dir}/{name}', 'size': photo['type']})
        with open('result.json', 'w') as outfile:
            json.dump(end_list, outfile)


# if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    # path_to_file =
    # token =
    # uploader = YaUploader(token)
    # result = uploader.upload(path_to_file)
