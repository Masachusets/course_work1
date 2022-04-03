import requests


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        """Метод получает заголовки"""
        return {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}


    def get_file_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()


    def get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {'path': disk_file_path, 'owerwrite': 'true'}
        headers = self.get_headers()
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()


    def upload(self, file_path: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        href_json = self.get_upload_link(disk_file_path=file_path)
        href = href_json['href']
        response = requests.put(href, data=open(file_path, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print('Success')


#if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    # path_to_file =
    # token =
    # uploader = YaUploader(token)
    # result = uploader.upload(path_to_file)
