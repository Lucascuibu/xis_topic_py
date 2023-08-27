from bs4 import BeautifulSoup
from datetime import date
import asyncio, csv, aiohttp
import pandas as pd
from pathlib import Path
from utils.decorator import async_timeit
import logging, sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
logging.basicConfig(level=logging.INFO)

def read_csv_to_dict(path):
    df = pd.read_csv(path, header=None)
    df.columns = ["Key", "Value"]
    return df.set_index("Key")["Value"].to_dict()

async def get_viewer_count(session, curid):
    try:
        url = f"https://www.xiaohongshu.com/page/topics/{curid}"
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            selector = "#app > div > div > div.backdrop > div > div.page-lines.page-header > div.summary > div.meta"
            element = soup.select_one(selector)
            return 0 if element is None else (element.get_text()[:-3])
    except Exception as e:
        logging.error(f"Failed to get viewer count for curid {curid}. Error: {e}")

def parse_unit(result_str):
    if result_str[-1] == "万":
        cur = float(result_str[:-1])
    elif result_str[-1] == "亿":
        cur = float(result_str[:-1]) * 10000
    else:
        cur = None
    return cur

async def adjust_rows_to_match_topic(rows, topic_num):
    if len(rows) < topic_num:
        while len(rows) < topic_num:
            rows.append(["null"] * len(rows[0]))
    elif len(rows) > topic_num:
        rows = rows[:topic_num]
    return rows

def get_headers(rows, curSunday):
    cur_header = [curSunday.strftime("%-m.%-d")] + [""] * (len(rows) - 1)
    rows = [row + [data] for row, data in zip(rows, cur_header)]
    return rows

async def fetch_results(session,topic_dict, blacklist):
    tasks = []
    for key, curid in topic_dict.items():
        if not key or key in blacklist or not curid:
            continue
        task = get_viewer_count(session, curid=curid)
        tasks.append(task)
    return await asyncio.gather(*tasks) 

def update_rows_with_results(rows, results, topic_dict):
    Emptyness = len(rows) == 0
    if Emptyness:
        for i, (result, [key, _]) in enumerate(zip(results, topic_dict.items())):
            if i == 17:
                rows[17][-1] = str(13000)
                continue
            elif i == 18:
                rows[18][-1] = str(66)
                continue
            cur = parse_unit(str(result))
            rows.append([cur])
    else:
        for i, (result, [key, _]) in enumerate(zip(results, topic_dict.items())):
            j = i + 1 if i < (len(results) - 1) else i
            if j == 17:
                rows[17][-1] = str(13000)
                continue
            elif j == 18:
                rows[18][-1] = str(66)
                continue
            cur = parse_unit(str(result))
            rows[j][-1] = cur
    return rows

async def spill_data(blacklist, result_file_path, curSunday, topic_csv_path):
    async with aiohttp.ClientSession() as session:
        with open(result_file_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
        rows = await adjust_rows_to_match_topic(rows, topic_num)
        rows = get_headers(rows, curSunday)
        topic_dict = read_csv_to_dict(topic_csv_path)
        results = await fetch_results(session, topic_dict, blacklist)
        rows = update_rows_with_results(rows, results, topic_dict)
        with open(result_file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

BASE_DIR = Path(__file__).resolve().parent.parent
db_folder = BASE_DIR / "database"
topic_path = db_folder / "topic.csv"
database_path = db_folder / "database.csv"

@async_timeit
async def main(topic_csv_path=topic_path, database_path=database_path):
    try:
        today = date.today()
        with open(topic_path, "r", newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            global topic_num
            topic_num = len(list(reader))
            print(f"trying to inject is {topic_num} lines of data ")
        print("start the injection")
        await spill_data(
            blacklist=[],
            result_file_path=database_path,
            curSunday=today,
            topic_csv_path=topic_csv_path,
        )
        print(f"Successfully injected at {today}")
    except Exception as e:
        logging.error(f"Failed in main function. Error: {e}")
