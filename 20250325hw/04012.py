import os
from bs4 import BeautifulSoup
import pandas as pd
import requests

# 儲存 HTML 檔案的資料夾路徑
html_folder = "./"  # 假設 HTML 檔案與程式在同一目錄下

# 初始化資料列表
all_data = []

# 網頁的基礎 URL
base_url = "https://pda5284.gov.taipei/MQS/"

# 模擬的 DataFrame，包含站點名稱和相對連結
data = {
    "站點名稱": [
        "蘆洲總站", "王爺廟口", "空中大學(中正路)", "中原公寓", "蘆洲國小"
    ],
    "連結": [
        "stop.jsp?sid=36021",
        "stop.jsp?sid=36022",
        "stop.jsp?sid=36023",
        "stop.jsp?sid=36024",
        "stop.jsp?sid=36025"
    ]
}

# 將資料轉換為 DataFrame
df = pd.DataFrame(data)

# 遍歷 DataFrame 中的每個站點
for index, row in df.iterrows():
    station_name = row["站點名稱"]
    relative_link = row["連結"]
    full_url = base_url + relative_link  # 完整的 URL

    # 發送 GET 請求
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(full_url, headers=headers)

    # 確保請求成功
    if response.status_code == 200:
        # 儲存 HTML 檔案
        filename = f"{station_name}.html"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"已成功儲存 {station_name} 的 HTML 檔案為 {filename}")
    else:
        print(f"無法下載 {station_name} 的網頁，HTTP 狀態碼: {response.status_code}")

# 遍歷資料夾中的所有 HTML 檔案
for filename in os.listdir(html_folder):
    if filename.endswith(".html"):  # 確保只處理 HTML 檔案
        filepath = os.path.join(html_folder, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(content, "html.parser")

        # 找到目標表格
        table = soup.find("table", class_="formattable1")
        if table:
            # 遍歷表格中的每一行
            for row in table.find_all("tr", class_=["ttego1", "ttego2"]):
                cols = row.find_all("td")
                if len(cols) >= 4:
                    route = cols[0].text.strip()  # 路線
                    stop = cols[1].text.strip()  # 站牌
                    direction = cols[2].text.strip()  # 去返程
                    estimate = cols[3].text.strip()  # 預估到站
                    all_data.append({
                        "HTML檔案": filename,
                        "路線": route,
                        "站牌": stop,
                        "去返程": direction,
                        "預估到站": estimate
                    })

# 將資料轉換為 DataFrame
df = pd.DataFrame(all_data)

# 輸出結果
print(df)

# 將結果儲存為 CSV 檔案
df.to_csv("所有站點公車動態.csv", index=False, encoding="utf-8-sig")
print("已成功將所有資料儲存為所有站點公車動態.csv")