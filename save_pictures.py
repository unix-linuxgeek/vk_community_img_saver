import os
import vk_api
import requests

token = "enter your token here"
vk_session = vk_api.VkApi(token)
vk = vk_session.get_api()
group_id = 'enter your group id here'


def save_post_photos(post, folder):
    attachments = []
    get_attachments([post], attachments)
    for attachment in attachments:
        if attachment['type'] == 'photo':
            photo = attachment['photo']
            url = photo['orig_photo']['url']
            file_ext = url.split('?')[0].split('.')[-1]
            file_name = f"{post['id']}_{photo['id']}.{file_ext}"
            img_path = os.path.join(folder, file_name)
            img_data = requests.get(url).content
            with open(img_path, 'wb') as handler:
                handler.write(img_data)
            print(f"Сохранено изображение: {img_path}")
            return img_path


def get_attachments(posts, attachments):
    for post in posts:
        if 'attachments' in post:
            attachments += post['attachments']

        if 'copy_history' in post:
            get_attachments(post['copy_history'], attachments)


def save_wall_photos(group_id, folder):
    offset = 0
    total_posts = 1
    processed_posts = 0

    while processed_posts < total_posts:
        posts = vk.wall.get(owner_id=f'-{group_id}', count=100, offset=offset)
        total_posts = posts['count']
        posts = posts['items']
        for post in posts:
            save_post_photos(post, folder)
            processed_posts += 1
            print(f'Post: {processed_posts} / {total_posts}')
        offset += 100


def name_img_folder():
    folder_name = input("Please, name the folder where you want to download images:   ")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


folder = name_img_folder()
save_wall_photos(group_id, folder)
