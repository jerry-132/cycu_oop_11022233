import sys
import io
import requests
import html
import pandas as pd
from bs4 import BeautifulSoup

# 設定標準輸出為 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = '''https://pda5284.gov.taipei/MQS/route.jsp?rid=10417'''

# 發送 GET 請求
response = requests.get(url)

# 確保請求成功
if response.status_code == 200:
    # 將內容寫入 bus1.html
    with open("bus1.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("網頁已成功下載並儲存為 bus1.html")

    # 重新讀取並解碼 HTML
    with open("bus1.html", "r", encoding="utf-8") as file:
        content = file.read()
        decoded_content = html.unescape(content)  # 解碼 HTML 實體

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(content, "html.parser")

    # 初始化 DataFrame 列表
    go_rows = []  # 去程資料
    back_rows = []  # 返程資料

    # 找到所有去程的 tr 標籤
    for tr in soup.find_all("tr", class_=["ttego1", "ttego2"]):
        td = tr.find("td")
        if td:
            stop_name = html.unescape(td.text.strip())  # 解碼站點名稱
            stop_link = td.find("a")["href"] if td.find("a") else None
            go_rows.append({"站點名稱": stop_name, "連結": stop_link})

    # 找到所有返程的 tr 標籤
    for tr in soup.find_all("tr", class_=["tteback1", "tteback2"]):
        td = tr.find("td")
        if td:
            stop_name = html.unescape(td.text.strip())  # 解碼站點名稱
            stop_link = td.find("a")["href"] if td.find("a") else None
            back_rows.append({"站點名稱": stop_name, "連結": stop_link})

    # 將去程和返程資料分別轉換為 DataFrame
    df_go = pd.DataFrame(go_rows)
    df_back = pd.DataFrame(back_rows)

    # 添加方向標記
    df_go["方向"] = "去程"
    df_back["方向"] = "返程"

    # 輸出結果
    print("第一個 DataFrame (去程):")
    print(df_go)
    print("\n第二個 DataFrame (返程):")
    print(df_back)

    # 將去程和返程資料分別儲存為 HTML 檔案
    df_go.to_html("去程.html", index=False, escape=False)
    df_back.to_html("返程.html", index=False, escape=False)
    print("去程和返程資料已分別儲存為去程.html和返程.html")
else:
    print(f"無法下載網頁，HTTP 狀態碼: {response.status_code}")