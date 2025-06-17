from selenium import webdriver
from time import sleep
import os
import csv
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib

browser = webdriver.Chrome()
browser.get('https://www.enoteca.co.jp/item/detail/130040021?td_seg=tds990077tds773385')

from selenium.webdriver.common.by import By
elem = browser.find_element(By.CSS_SELECTOR,"#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > div.mb-7.flex.justify-between.md\:mb-8 > h1 > span.mb-2\.5.block")
print(elem.text)

elem = browser.find_element(By.CSS_SELECTOR,"#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > p.mb-7.border-b.pb-7.text-lg.md\:mb-10.md\:pb-10.md\:text-2xl")
print(elem.text)

browser.get('https://www.enoteca.co.jp/item/detail/111500190?td_seg=tds990077tds773385')
while True:
    try:
        elem = browser.find_element(By.CSS_SELECTOR,"#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > div.mb-7.flex.justify-between.md\:mb-8 > h1 > span.mb-2\.5.block")
        print(elem.text)

        elem = browser.find_element(By.CSS_SELECTOR,"#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > p.mb-7.border-b.pb-7.text-lg.md\:mb-10.md\:pb-10.md\:text-2xl")
        print(elem.text)
        break
    except:
        continue

# CSVファイルの準備
os.makedirs("output", exist_ok=True)
csv_file_path = "wine_data.csv"

# ヘッダー行を書き込む
with open(csv_file_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "name", "description", "page_url", "image_url"])


#赤ワイン
wine_urls = []
browser.get('https://www.enoteca.co.jp/item/list?_color=1&_qty=1&td_seg=tds990077tds773385')
sleep(5)
for i in range(1, 20):
        wine = browser.find_element(
            By.CSS_SELECTOR,
            f"#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div:nth-child(1) > div > div:nth-child(2) > div.md\:mx-12.md\:flex.md\:justify-center > div > ul > li:nth-child({i}) > div > div.grow.md\:flex > div.mb-2.space-y-3\.5.md\:mb-0.md\:mr-8.md\:grow > h3 > a",
        )
        try:
            wine_urls.append(wine.get_attribute("href"))
        except:
        # 要素がなければスキップ
            continue

for index, wine_url in enumerate(wine_urls, 1):
        
    print(f"\n【ワイン {index}】")
    print(f"URL: {wine_url}")
        
    # ワインの詳細ページにアクセス
    browser.get(wine_url)
        
    # ページが完全に読み込まれるまで少し待機
    sleep(2)
        
    # ワイン名を取得
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    wait = WebDriverWait(browser, 10)
    
    try:
        wine_name_elem = wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > div.mb-7.flex.justify-between.md\:mb-8 > h1 > span.mb-2\.5.block"
                ))
            )
        wine_name = wine_name_elem.text
        print(f"ワイン名: {wine_name}")

        # ワインの説明を取得
        
        wine_description_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > p.mb-7.border-b.pb-7.text-lg.md\:mb-10.md\:pb-10.md\:text-2xl"
        )
        wine_description = wine_description_elem.text
        print(f"説明: {wine_description}")

        # 画像URLの取得
        img_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-440px.relative.mx-auto.md\:ml-0.md\:mr-12.md\:w-2\/5.md\:flex-shrink-0.xl\:mr-16 > section:nth-child(1) > div.relative.mt-1.overflow-x-hidden > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > img"
        )
        img_url = img_elem.get_attribute("src")
        print(f"画像URL: {img_url}")

        # urllibライブラリを使って画像URLからバイナリ読み込む
        with urllib.request.urlopen(img_url)as rf:
            img_data = rf.read()

        # with open()構文を使ってバイナリデータをpng形式で書き出す
        with open(f"images/redwine{index}.png", mode="wb")as wf:
            wf.write(img_data)

        # CSVに書き込み
        with open(csv_file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([index, wine_name, wine_description, wine_url, img_url])

        

    except Exception as e:
        print(f"{index}番目のワインでエラー: {e}")
        continue

#白ワイン
wine_urls = []
browser.get('https://www.enoteca.co.jp/item/list?_color=2&_qty=1&td_seg=tds990077tds773385')
sleep(5)
for i in range(1, 20):
        wine = browser.find_element(
            By.CSS_SELECTOR,
            f"#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div:nth-child(1) > div > div:nth-child(2) > div.md\:mx-12.md\:flex.md\:justify-center > div > ul > li:nth-child({i}) > div > div.grow.md\:flex > div.mb-2.space-y-3\.5.md\:mb-0.md\:mr-8.md\:grow > h3 > a",
        )
        try:
            wine_urls.append(wine.get_attribute("href"))
        except:
        # 要素がなければスキップ
            continue

for index, wine_url in enumerate(wine_urls, 1):
        
    print(f"\n【ワイン {index}】")
    print(f"URL: {wine_url}")
        
    # ワインの詳細ページにアクセス
    browser.get(wine_url)
        
    # ページが完全に読み込まれるまで少し待機
    sleep(2)
        
    # ワイン名を取得
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    wait = WebDriverWait(browser, 10)
    
    try:
        wine_name_elem = wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > div.mb-7.flex.justify-between.md\:mb-8 > h1 > span.mb-2\.5.block"
                ))
            )
        wine_name = wine_name_elem.text
        print(f"ワイン名: {wine_name}")

        # ワインの説明を取得
        
        wine_description_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > p.mb-7.border-b.pb-7.text-lg.md\:mb-10.md\:pb-10.md\:text-2xl"
        )
        wine_description = wine_description_elem.text
        print(f"説明: {wine_description}")

        # 画像URLの取得
        img_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-440px.relative.mx-auto.md\:ml-0.md\:mr-12.md\:w-2\/5.md\:flex-shrink-0.xl\:mr-16 > section:nth-child(1) > div.relative.mt-1.overflow-x-hidden > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > img"
        )
        img_url = img_elem.get_attribute("src")
        print(f"画像URL: {img_url}")

        # urllibライブラリを使って画像URLからバイナリ読み込む
        with urllib.request.urlopen(img_url)as rf:
            img_data = rf.read()

        # with open()構文を使ってバイナリデータをpng形式で書き出す
        with open(f"images/whitewine{index}.png", mode="wb")as wf:
            wf.write(img_data)

        # CSVに書き込み
        with open(csv_file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([index, wine_name, wine_description, wine_url, img_url])

        

    except Exception as e:
        print(f"{index}番目のワインでエラー: {e}")
        continue

#ロゼワイン
wine_urls = []
browser.get('https://www.enoteca.co.jp/item/list?_color=3&_qty=1&td_seg=tds990077tds773385')
sleep(5)
for i in range(1, 20):
        wine = browser.find_element(
            By.CSS_SELECTOR,
            f"#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div:nth-child(1) > div > div:nth-child(2) > div.md\:mx-12.md\:flex.md\:justify-center > div > ul > li:nth-child({i}) > div > div.grow.md\:flex > div.mb-2.space-y-3\.5.md\:mb-0.md\:mr-8.md\:grow > h3 > a",
        )
        try:
            wine_urls.append(wine.get_attribute("href"))
        except:
        # 要素がなければスキップ
            continue

for index, wine_url in enumerate(wine_urls, 1):
        
    print(f"\n【ワイン {index}】")
    print(f"URL: {wine_url}")
        
    # ワインの詳細ページにアクセス
    browser.get(wine_url)
        
    # ページが完全に読み込まれるまで少し待機
    sleep(2)
        
    # ワイン名を取得
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    wait = WebDriverWait(browser, 10)
    
    try:
        wine_name_elem = wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > div.mb-7.flex.justify-between.md\:mb-8 > h1 > span.mb-2\.5.block"
                ))
            )
        wine_name = wine_name_elem.text
        print(f"ワイン名: {wine_name}")

        # ワインの説明を取得
        
        wine_description_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > p.mb-7.border-b.pb-7.text-lg.md\:mb-10.md\:pb-10.md\:text-2xl"
        )
        wine_description = wine_description_elem.text
        print(f"説明: {wine_description}")

        # 画像URLの取得
        img_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-440px.relative.mx-auto.md\:ml-0.md\:mr-12.md\:w-2\/5.md\:flex-shrink-0.xl\:mr-16 > section:nth-child(1) > div.relative.mt-1.overflow-x-hidden > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > img"
        )
        img_url = img_elem.get_attribute("src")
        print(f"画像URL: {img_url}")

        # urllibライブラリを使って画像URLからバイナリ読み込む
        with urllib.request.urlopen(img_url)as rf:
            img_data = rf.read()

        # with open()構文を使ってバイナリデータをpng形式で書き出す
        with open(f"images/rosewine{index}.png", mode="wb")as wf:
            wf.write(img_data)

        # CSVに書き込み
        with open(csv_file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([index, wine_name, wine_description, wine_url, img_url])

        

    except Exception as e:
        print(f"{index}番目のワインでエラー: {e}")
        continue

#スパークリングワイン
wine_urls = []
browser.get('https://www.enoteca.co.jp/item/list?_color=5&_color=6&_color=7&_qty=1&td_seg=tds990077tds773385')
sleep(5)
for i in range(1, 20):
        wine = browser.find_element(
            By.CSS_SELECTOR,
            f"#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div:nth-child(1) > div > div:nth-child(2) > div.md\:mx-12.md\:flex.md\:justify-center > div > ul > li:nth-child({i}) > div > div.grow.md\:flex > div.mb-2.space-y-3\.5.md\:mb-0.md\:mr-8.md\:grow > h3 > a",
        )
        try:
            wine_urls.append(wine.get_attribute("href"))
        except:
        # 要素がなければスキップ
            continue

for index, wine_url in enumerate(wine_urls, 1):
        
    print(f"\n【ワイン {index}】")
    print(f"URL: {wine_url}")
        
    # ワインの詳細ページにアクセス
    browser.get(wine_url)
        
    # ページが完全に読み込まれるまで少し待機
    sleep(2)
        
    # ワイン名を取得
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    wait = WebDriverWait(browser, 10)
    
    try:
        wine_name_elem = wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > div.mb-7.flex.justify-between.md\:mb-8 > h1 > span.mb-2\.5.block"
                ))
            )
        wine_name = wine_name_elem.text
        print(f"ワイン名: {wine_name}")

        # ワインの説明を取得
        
        wine_description_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > p.mb-7.border-b.pb-7.text-lg.md\:mb-10.md\:pb-10.md\:text-2xl"
        )
        wine_description = wine_description_elem.text
        print(f"説明: {wine_description}")

        # 画像URLの取得
        img_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-440px.relative.mx-auto.md\:ml-0.md\:mr-12.md\:w-2\/5.md\:flex-shrink-0.xl\:mr-16 > section:nth-child(1) > div.relative.mt-1.overflow-x-hidden > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > img"
        )
        img_url = img_elem.get_attribute("src")
        print(f"画像URL: {img_url}")

        # urllibライブラリを使って画像URLからバイナリ読み込む
        with urllib.request.urlopen(img_url)as rf:
            img_data = rf.read()

        # with open()構文を使ってバイナリデータをpng形式で書き出す
        with open(f"images/sparklwine{index}.png", mode="wb")as wf:
            wf.write(img_data)

        # CSVに書き込み
        with open(csv_file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([index, wine_name, wine_description, wine_url, img_url])

        

    except Exception as e:
        print(f"{index}番目のワインでエラー: {e}")
        continue

#オレンジワイン
wine_urls = []
browser.get('https://www.enoteca.co.jp/item/list?_color=14&_qty=1&td_seg=tds990077tds773385')
sleep(5)
for i in range(1, 20):
        wine = browser.find_element(
            By.CSS_SELECTOR,
            f"#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div:nth-child(1) > div > div:nth-child(2) > div.md\:mx-12.md\:flex.md\:justify-center > div > ul > li:nth-child({i}) > div > div.grow.md\:flex > div.mb-2.space-y-3\.5.md\:mb-0.md\:mr-8.md\:grow > h3 > a",
        )
        try:
            wine_urls.append(wine.get_attribute("href"))
        except:
        # 要素がなければスキップ
            continue

for index, wine_url in enumerate(wine_urls, 1):
        
    print(f"\n【ワイン {index}】")
    print(f"URL: {wine_url}")
        
    # ワインの詳細ページにアクセス
    browser.get(wine_url)
        
    # ページが完全に読み込まれるまで少し待機
    sleep(2)
        
    # ワイン名を取得
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    wait = WebDriverWait(browser, 10)
    
    try:
        wine_name_elem = wait.until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > div.mb-7.flex.justify-between.md\:mb-8 > h1 > span.mb-2\.5.block"
                ))
            )
        wine_name = wine_name_elem.text
        print(f"ワイン名: {wine_name}")

        # ワインの説明を取得
        
        wine_description_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-screen-sm.md\:relative.md\:flex-grow > section.mb-8.mt-5.md\:mb-10.md\:mt-0 > p.mb-7.border-b.pb-7.text-lg.md\:mb-10.md\:pb-10.md\:text-2xl"
        )
        wine_description = wine_description_elem.text
        print(f"説明: {wine_description}")

        # 画像URLの取得
        img_elem = browser.find_element(
            By.CSS_SELECTOR,
            "#__layout > div > div.flex.min-h-screen.flex-col > div.flex.flex-grow.flex-col.justify-start > div.pb-60px.md\:pb-20 > div > div > div.relative.mx-auto.mb-10.md\:mb-20.md\:flex.md\:justify-center > div.max-w-440px.relative.mx-auto.md\:ml-0.md\:mr-12.md\:w-2\/5.md\:flex-shrink-0.xl\:mr-16 > section:nth-child(1) > div.relative.mt-1.overflow-x-hidden > div.swiper-container.swiper-container-initialized.swiper-container-horizontal.swiper-container-pointer-events > div.swiper-wrapper > div.swiper-slide.swiper-slide-active > img"
        )
        img_url = img_elem.get_attribute("src")
        print(f"画像URL: {img_url}")

        # urllibライブラリを使って画像URLからバイナリ読み込む
        with urllib.request.urlopen(img_url)as rf:
            img_data = rf.read()

        # with open()構文を使ってバイナリデータをpng形式で書き出す
        with open(f"images/orangewine{index}.png", mode="wb")as wf:
            wf.write(img_data)

        # CSVに書き込み
        with open(csv_file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([index, wine_name, wine_description, wine_url, img_url])

        

    except Exception as e:
        print(f"{index}番目のワインでエラー: {e}")
        continue