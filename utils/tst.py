import requests

url = "https://edith.xiaohongshu.com/api/sns/v10/search/notes?allow_rewrite=1&api_extra=&geo=eyJsYXRpdHVkZSI6NDEuNzk0MDE1MDMzNjY1LCJsb25naXR1ZGUiOjEyMy4zMDQwODc3MTgzOTg3fQ%3D%3D&keyword=%E7%89%B9%E6%96%AF%E6%8B%89&loaded_ad=&location_permission=1&page=4&page_pos=63&page_size=20&recommend_info_extra=&scene=history&search_id=2c3gfpzrh17rssl2jfiyo%402c3gfqlvruqjzjowqbgmn&session_id=2c3gfpuzj7o8d85kxahat&sort=time_descending&source=explore_feed"
headers = {
    "User-Agent": "Stream/1.0.6 (iPhone; iOS 16.6; Scale/3.00)",
    "Accept": "*/*",
    "Connection": "Keep-Alive"
}

response = requests.get(url, headers=headers)
print(response.text)
