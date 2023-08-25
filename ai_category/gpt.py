import openai
from tqdm import tqdm
import csv

api_key = "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"
openai.api_key = api_key

first_categories = [
    "用车指南",
    "体验分享",
    "新闻评论",
    "广告"
    
]
# 定义二级分类
# second_categories = [
#     "OTA功能分享",
#     "充电",
#     "导航",
#     "自用好物",
#     "驾驶体验",
#     "咨询问题",
#     "提车经历",
#     "特斯拉中国官方精品",
#     "能耗",
#     "影音娱乐",
#     "购车相关",
#     "吐槽",
#     "马斯克",
#     "召回",
#     "刹车",
#     "新闻评论",
#     "卖车",
#     "广告",
# ]
sencond_categories = [
    "OTA功能分享：分享特斯拉车辆通过在线升级（OTA）获得的新功能或改进。",
    "充电：讨论特斯拉车辆的充电方式、充电速度、充电站点等相关话题。",
    "导航：关于特斯拉车载导航系统的使用体验、导航路线规划、导航数据准确性等讨论。",
    "自用好物：分享用户购买的与特斯拉车辆相关的个人用品、周边产品或改装配件等。",
    "驾驶体验：分享特斯拉车辆驾驶体验、操控感受、加速性能、舒适性等方面的内容。",
    "咨询问题：用户对特斯拉车辆或公司的疑问、问题咨询与解答。",
    "提车经历：分享用户提取新车的经历、购车流程、交付体验等内容。",
    "特斯拉中国官方精品：介绍特斯拉中国官方推出的精品商品、周边产品、限量版车型等。",
    "能耗：关于特斯拉车辆的能耗情况、电池续航里程、充电效率等讨论。",
    "影音娱乐：与特斯拉车载影音娱乐系统、音响配置、多媒体功能相关的内容。",
    "购车相关：关于购买特斯拉车辆的流程、政策、购车优惠等信息。",
    "吐槽：用户对特斯拉车辆、服务或公司的吐槽、批评与不满意之处。",
    "马斯克：关于特斯拉公司CEO埃隆·马斯克的言论、行动、公司动态等相关话题。",
    "召回：特斯拉车辆召回信息、维修保养、售后服务等内容。",
    "刹车：与特斯拉车辆刹车性能、刹车系统、刹车噪音等相关讨论。",
    "新闻评论：对特斯拉相关新闻报道的评论、观点分享等。",
    "卖车：用户出售特斯拉车辆、二手交易相关信息。",
    "广告：特斯拉相关广告、营销活动、宣传推广等内容。"
]
categories = [
    "OTA功能分享：在这个类别中，用户分享特斯拉车辆通过在线升级（OTA）获得的新功能或改进。这可能涉及到车辆功能的扩展、性能的优化以及新的驾驶辅助功能的引入等。用户可以分享他们的使用体验和对新功能的评价。",
    "充电：这个类别讨论特斯拉车辆的充电方式、充电速度、充电站点等相关话题。用户可能分享他们的充电策略、使用超级充电站的体验，或者讨论在不同情况下的充电效率和电池寿命等问题。",
    "导航：该类别关注特斯拉车载导航系统的使用体验、导航路线规划、导航数据准确性等讨论。用户可以分享他们的导航体验，是否准确地导航到目的地，以及导航系统的功能是否满足需求等。",
    "自用好物：这个类别是分享用户购买的与特斯拉车辆相关的个人用品、周边产品或改装配件等。用户可能推荐实用的车内用品、车载充电器、车身贴纸等产品，或者分享他们自己的改装经历和效果。",
    "驾驶体验：在这个类别中，用户分享特斯拉车辆驾驶体验、操控感受、加速性能、舒适性等方面的内容。他们可能描述驾驶特斯拉的乐趣，操控与其他车型的对比，以及在不同道路条件下的表现。",
    "咨询问题：这个类别涉及用户对特斯拉车辆或公司的疑问、问题咨询与解答。其他用户或专业人士可能回答问题，提供帮助和解决方案。",
    "提车经历：用户在这个类别分享提取新车的经历、购车流程、交付体验等内容。这可能包括预约交付，交付过程中的顾虑和惊喜，以及对特斯拉交付服务的评价。",
    "特斯拉中国官方精品：该类别介绍特斯拉中国官方推出的精品商品、周边产品、限量版车型等。用户可能分享新产品的外观和功能，或者讨论特斯拉与其他品牌的合作。",
    "能耗：在这个类别讨论特斯拉车辆的能耗情况、电池续航里程、充电效率等。用户可能分享不同模式下的能耗数据，充电对续航里程的影响，以及一些节能的驾驶技巧。",
    "影音娱乐：这个类别与特斯拉车载影音娱乐系统、音响配置、多媒体功能相关。用户可能讨论车载娱乐体验，音响效果的好坏，以及与手机连接的功能。",
    "购车相关：该类别涉及购买特斯拉车辆的流程、政策、购车优惠等信息。用户可能分享购车经验，购车时需要注意的事项，以及政策变化对购车的影响。",
    "吐槽：用户在这个类别发表对特斯拉车辆、服务或公司的吐槽、批评与不满意之处。这可以是对特定问题的抱怨，或者对产品或服务的改建议。",
    "马斯克：在这个类别讨论特斯拉公司CEO埃隆·马斯克的言论、行动、公司动态等相关话题。用户可能分享关于马斯克的采访、社交媒体上的言论，或者对他领导风格的看法。",
    "召回：该类别包含特斯拉车辆召回信息、维修保养、售后服务等内容。用户可能分享召回经历，售后服务质量，以及维修保养的建议。",
    "刹车：在这个类别与特斯拉车辆刹车性能、刹车系统、刹车噪音等相关讨论。用户可能分享刹车效果，刹车系统的工作原理，以及刹车维护注意事项。",
    "新闻评论：这个类别允许用户对特斯拉相关新闻报道进行评论、观点分享等。用户可以表达对新闻事件的看法，讨论新闻对特斯拉未来发展的影响等。",
    "卖车：该类别包含用户出售特斯拉车辆、二手交易相关信息。用户可以发布车辆出售信息，或者询问关于二手车交易的相关问题。",
    "广告：这个类别涉及特斯拉相关广告、营销活动、宣传推广等内容。用户可能分享他们喜欢的特斯拉广告，或者讨论公司的营销策略。"
]



def condense_tweet(tweet):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="这是一条小红书平台特斯拉话题下的推文，请提炼出这篇推文的核心，不超过50个字。推文内容如下："+tweet,
        max_tokens=50
    )
    return response["choices"][0]["text"].strip()


def classify_tweet(tweet,category):
    categories_string = ", ".join(category)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt="这是一条小红书平台特斯拉话题下的推文，请通过分析标题和内容将其归纳到提供的分类中。分类内容包括:"+categories_string +
        ". 推文内容如下：" + tweet + "回复我该条推文所属的分类的完整名称！",
        max_tokens=50,
    )

    completion = response["choices"][0]["text"].strip()
    # second_category = extract_category(completion)

    return completion


def extract_category(text):
    categories = text.splitlines()
    for category in categories:
        category = category.strip()
        if category in sencond_categories:
            return category

    return "未分类"



sample_tweets = [
    "标题:姐妹们！这个车载香薰真的好高级！！内容：之前都用石膏滴精油的！滴到皮上直接废了！我真的会谢了…… 这次我特地买了固体香片型的香薰 固体PE材质，放车里高温也不会化 比液体精油的好用很多！强推！！ 还附有三种不同香味的香薰片 个人最喜欢都柏林的春天的香味 中性香很纯粹清新的香气 ！！男女都会喜欢！",
    "标题:还剩100公里 坚持住~内容:还剩100公里 坚持住~",
    "标题：挑战全网最美汽车脚垫内容：一体式设计，三针三线，剖版工艺！专利30项、独步全网！#汽车脚垫 #揽行一体式太空舱软包脚垫 #揽行高端定制大包围脚垫 #全网挑战 #挑战 #360航空软包脚垫 #汽车全包围脚垫 #兰酷一体式365工匠软包脚垫 #重庆市兰酷汽车饰品有限公司 #特斯拉 #特斯拉modelY #特斯拉model3 #理",
]



def read_csv_to_dict(csv_file):
    tweet_dict = {}
    with open(csv_file, mode="r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip the header row
        for row in reader:
            tweet_number, title, link, publish_time, user_name, image_count, likes, content = row
            # Combine title and content into one value
            tweet_content =  f"标题：{title}\n内容：{content}"
            tweet_dict[int(tweet_number)] = tweet_content
    return tweet_dict



def classify (dict,input_category):
    for tweet_number, tweet_content in tqdm(tweet_dict.items()):
        result_category = classify_tweet(tweet_content,input_category)
        save_csv(tweet_content, result_category)


def save_csv(note, result_category):
    with open("小红书_notes5.csv", mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        result_index = len(note.content[0]) +1
        csv.writerow                            
        
        
def condense (dict):
    for tweet_number, tweet_content in tqdm(tweet_dict.items()):
        conden = condense_tweet(tweet_content)
        print(f"序号: {tweet_number}")
        print(f"推文内容：{tweet_content}")
        print(f"{conden}")
        print("---------------")
    
if __name__ == '__main__':
    csv_file = "小红书_notes2.csv"  
    tweet_dict = read_csv_to_dict(csv_file)
    classify(tweet_dict,categories)

