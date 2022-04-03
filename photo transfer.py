import VKUser
import YandexDisk
from pprint import pprint


if __name__ == '__main__':
    with open('VKtoken.txt', 'r') as file_object:
        VKtoken = file_object.read().strip()
    vk_client = VKUser.VkUser(VKtoken, '5.131')
    with open('YaToken.txt', 'r') as file_object:
        YaToken = file_object.read().strip()
    uploader = YandexDisk.YaUploader(YaToken)

    # pprint(vk_client.get_all_photos(vk_client.user_id()))
    photos = vk_client.get_all_photos()
    # pprint(photos)
    uploader.import_photos_to_disk(photos)
