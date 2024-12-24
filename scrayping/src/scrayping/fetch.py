import json
import os
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from jinja2 import Template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from .transform import transform_banzuke_to_rikishi


class WWWSUMO:
    protocol = "https"
    domain = "www.sumo.or.jp"
    banzuke_path = "/ResultBanzuke/table/"
    profile_path_template = Template("/ResultRikishiData/profile/{{ rikishi_id }}/")


class Dirs:
    base = Path(__file__).resolve().parents[2]
    img = base / "img"
    data = base / "data"


def create_dirs():
    os.makedirs(Dirs.base / Dirs.img, exist_ok=True)
    os.makedirs(Dirs.base / Dirs.data, exist_ok=True)


def fetch_banzuke_content():
    url = f"{WWWSUMO.protocol}://{WWWSUMO.domain}{WWWSUMO.banzuke_path}"
    # Seleniumでブラウザを起動してページを取得
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ヘッドレスモードで実行
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    url = "https://www.sumo.or.jp/ResultBanzuke/table/"
    driver.get(url)

    time.sleep(3)

    # ページのHTMLを取得
    html_content = driver.page_source
    driver.quit()
    return html_content


def extract_banzuke_table():
    html_content = fetch_banzuke_content()
    # BeautifulSoupで解析
    soup = BeautifulSoup(html_content, "html.parser")

    # 場所情報を取得
    basho = soup.select_one("p.mdDate").get_text(strip=True)

    # テーブル行を取得
    rows = soup.select("tr.bTnone")

    rikishi_list = []
    for row in rows:
        # 東側力士の情報を取得
        east_player = row.select_one("td.east .player")
        east_name = (
            east_player.select_one("dt span").get_text(strip=True) if east_player.select_one("dt span") else None
        )
        east_profile_url = east_player.select_one("dt a")["href"] if east_player.select_one("dt a") else None
        east_country = (
            east_player.select_one("dd a:first-child span").get_text(strip=True)
            if east_player.select_one("dd a:first-child span")
            else None
        )
        east_country_url = (
            east_player.select_one("dd a:first-child")["href"] if east_player.select_one("dd a:first-child") else None
        )
        east_heya = (
            east_player.select_one("dd a:last-child span").get_text(strip=True)
            if east_player.select_one("dd a:last-child span")
            else None
        )
        east_heya_url = (
            east_player.select_one("dd a:last-child")["href"] if east_player.select_one("dd a:last-child") else None
        )

        # 西側力士の情報を取得
        west_player = row.select_one("td.west .player")
        west_name = (
            west_player.select_one("dt span").get_text(strip=True) if west_player.select_one("dt span") else None
        )
        west_profile_url = west_player.select_one("dt a")["href"] if west_player.select_one("dt a") else None
        west_country = (
            west_player.select_one("dd a:first-child span").get_text(strip=True)
            if west_player.select_one("dd a:first-child span")
            else None
        )
        west_country_url = (
            west_player.select_one("dd a:first-child")["href"] if west_player.select_one("dd a:first-child") else None
        )
        west_heya = (
            west_player.select_one("dd a:last-child span").get_text(strip=True)
            if west_player.select_one("dd a:last-child span")
            else None
        )
        west_heya_url = (
            west_player.select_one("dd a:last-child")["href"] if west_player.select_one("dd a:last-child") else None
        )

        # 役職情報
        rank = row.select_one("td.rank p").get_text(strip=True) if row.select_one("td.rank p") else None

        rikishi_list.append(
            {
                "rank": rank,
                "east": {
                    "basho": basho,
                    "name": east_name,
                    "profile_url": f"https://www.sumo.or.jp{east_profile_url}" if east_profile_url else None,
                    "country": east_country,
                    "country_url": f"https://www.sumo.or.jp{east_country_url}" if east_country_url else None,
                    "heya": east_heya,
                    "heya_url": f"https://www.sumo.or.jp{east_heya_url}" if east_heya_url else None,
                },
                "west": {
                    "basho": basho,
                    "name": west_name,
                    "profile_url": f"https://www.sumo.or.jp{west_profile_url}" if west_profile_url else None,
                    "country": west_country,
                    "country_url": f"https://www.sumo.or.jp{west_country_url}" if west_country_url else None,
                    "heya": west_heya,
                    "heya_url": f"https://www.sumo.or.jp{west_heya_url}" if west_heya_url else None,
                },
            }
        )

    return rikishi_list


def extract_profile(url, name):
    # Seleniumの設定
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ヘッドレスモードで実行
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(2)  # ページが読み込まれるまで少し待機

    # BeautifulSoupで解析
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # 画像URLを取得
    image_div = soup.select_one("div.mdColSet1 img")

    # 名前と役職を取得
    _name_rank = soup.select_one("span.fntXL").get_text(strip=True)
    full_name, rank_detail = [part.strip() for part in _name_rank.split("\u2003") if part.strip()]

    # 読み仮名を取得
    table = soup.select_one("table.mdTable2")
    first_row = table.find("tr").find("td")
    text = first_row.get_text(strip=True)

    # 読み仮名を抽出（括弧内のテキスト）
    reading_match = re.search(r"\((.*?)\)", text)

    if reading_match:
        full_name_hiragana = reading_match.group(1)  # "てるのふじ はるお"
    else:
        full_name_hiragana = None

    if image_div:
        image_url = image_div["src"]
        if not image_url.startswith("http"):
            image_url = f"https://www.sumo.or.jp{image_url}"  # 相対パスをフルパスに変換

        # 画像をダウンロードして保存
        response = requests.get(image_url)
        if response.status_code == 200:
            # 保存するファイル名を決定
            file_name = f"{name}_{os.path.basename(image_url)}"
            save_path = os.path.join(Dirs.img, file_name)

            with open(save_path, "wb") as f:
                f.write(response.content)

            # 記録を保存
            profile_img = {"url": url, "image_url": image_url, "local_path": save_path}
            detail = {"full_name": full_name,
                      "full_name_hiragana": full_name_hiragana,
                      "rank_detail": rank_detail}
        else:
            profile_img = {"url": None, "image_url": None, "local_path": None}
            detail = {"full_name": None,
                      "full_name_hiragana": None,
                      "rank_detail": None}

    # ドライバを終了
    driver.quit()

    return profile_img, detail


def extract_profiles():
    rikishi_list = extract_banzuke_table()
    create_dirs()
    for rikishi in tqdm(rikishi_list, total=len(rikishi_list)):
        if rikishi["east"]["name"]:
            name = rikishi["east"]["name"]
            img_info, detial = extract_profile(rikishi["east"]["profile_url"], name=name)
            rikishi["east"]["profile_img"] = img_info
            rikishi["east"]["detail"] = detial
        if rikishi["west"]["name"]:
            name = rikishi["west"]["name"]
            img_info, detial = extract_profile(rikishi["west"]["profile_url"], name=name)
            rikishi["west"]["profile_img"] = img_info
            rikishi["west"]["detail"] = detial

    return rikishi_list


def save_data():
    banzuke_json = extract_profiles()
    rikishi_json = transform_banzuke_to_rikishi(banzuke_json)
    with open(Dirs.data / "banzuke.json", "w") as f:
        json.dump(banzuke_json, f, ensure_ascii=False, indent=4)

    with open(Dirs.data / "rikishi.json", "w") as f:
        json.dump(rikishi_json, f, ensure_ascii=False, indent=4)
