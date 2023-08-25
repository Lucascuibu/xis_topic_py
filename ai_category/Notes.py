import datetime,re,requests,openai,sys,os
from pathlib import Path
from bs4 import BeautifulSoup
from utils.Headers import HEADERS

class Note:
    def __init__(
        self, _id, _type, likes, title, user_name, create_time, image_count
    ):
        self.id = _id
        self.type = _type
        self.likes = likes
        self.title = title
        self.user_name = user_name
        self.create_time = create_time / 1000
        self.Year = 0
        self.Month = 0
        self.Day = 0
        self.Hour = 0
        self.image_count = image_count
        self.content = ""
        self.category = ""

    def get_date(self):
        timestamp_sec = self.create_time  # Convert milliseconds to seconds
        dt = datetime.datetime.fromtimestamp(timestamp_sec)
        self.Year = dt.year
        self.Month = dt.month
        self.Day = dt.day
        self.Hour = dt.hour

    def re_match(self, text):
        pattern = r"“(.*?)”"
        return re.match(pattern, text)

    def get_content(self):
        link = "https://www.xiaohongshu.com/explore/" + self.id
        try:
            response = requests.get(link, headers=HEADERS)
            if response.status_code == 200:
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                content_div = soup.find("meta", attrs={"name": "description"})
                if content_div:
                    self.content = content_div.get("content", "").strip()
                else:
                    self.content = "bbbbbb"
            else:
                self.content = "cccccc"  # 在请求失败时给出默认内容
        except requests.exceptions.RequestException as e:
            print("网络请求异常:", e)
            self.content = "dddddd"  # 在请求异常时给出默认内容
        
        return self.content

    def gen_title_content(self):
        return f"标题：{self.title}\n 内容： {self.content}"

    def get_category(self, category):
        print(f"开始获取{self.title}的分类")
        tweet = self.gen_title_content()
        categories_string = ", ".join(category)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="这是一条小红书平台特斯拉话题下的推文，请通过分析标题和内容将其归纳到提供的分类中。分类内容包括:"
            + categories_string
            + ". 推文内容如下："
            + tweet
            + "回复我该条推文所属的分类的完整名称！示例: 该条推文属于“购车相关”分类。",
            max_tokens=50,
        )
        completion = response["choices"][0]["text"].strip()
        # second_category = extract_category(completion)
        self.category = completion
