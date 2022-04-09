import VKUser
import YandexDisk
from GoogleDrive import GoogleObject
from pprint import pprint


if __name__ == '__main__':
    with open('VKtoken.txt', 'r') as file_object:
        VKtoken = file_object.read().strip()
    vk_client = VKUser.VkUser(VKtoken, '5.131')
    with open('YaToken.txt', 'r') as file_object:
        YaToken = file_object.read().strip()
    YaUploader = YandexDisk.YaUploader(YaToken)
    GoogleUploader = GoogleObject()

    # pprint(vk_client.get_all_photos(vk_client.user_id()))
    photos = vk_client.get_all_photos()
    # pprint(photos)
    GoogleUploader.import_photos_to_disk(photos)
    # YaUploader.import_photos_to_disk(photos)
