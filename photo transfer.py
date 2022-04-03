import VKUser, YandexDisk, requests
from pprint import pprint


def sorted_photo(all_photos: list):
    max_photos = {}
    for photo in all_photos:
        max_photos[f"{photo['likes']['count']}_{photo['likes']['user_likes']}"] = photo['sizes'][-1]['url']
    pprint(max_photos)



if __name__ == '__main__':
    with open('VKtoken.txt', 'r') as file_object:
        VKtoken = file_object.read().strip()
    vk_client = VKUser.VkUser(VKtoken, '5.131')
    with open('YaToken.txt', 'r') as file_object:
        YaToken = file_object.read().strip()
    uploader = YandexDisk.YaUploader(YaToken)
    #pprint(vk_client.get_all_photos())
    sorted_photo(vk_client.get_all_photos())
