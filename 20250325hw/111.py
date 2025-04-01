import os
import requests
import pandas as pd
import time

# 完整的去程和返程資料
data_go = {
    "站點名稱": [
        "蘆洲總站", "王爺廟口", "空中大學(中正路)", "中原公寓", "蘆洲國小", "蘆洲監理站", "蘆洲派出所", "溪墘", "捷運徐匯中學站", "徐匯中學",
        "幸福市場", "建和新村", "捷運三和國中站", "三和國中", "格致中學(三和路)", "厚德派出所", "德林寺(三和路)", "龍門路口", "三安里", "長壽西街口",
        "長元西街口", "正義重新路口", "天台廣場", "大同路口", "中山藝術公園", "捷運菜寮站", "過圳街", "三重區公所(過圳街)", "三重稅捐分處", "菜寮(重陽路)",
        "集美國小", "三重國民運動中心", "三重中學", "重安街口", "臺北車站(忠孝)", "捷運善導寺站", "華山文創園區", "忠孝國小", "臺北科技大學(忠孝)", "正義郵局",
        "懷生國中", "頂好市場", "捷運忠孝敦化站", "阿波羅大廈", "交通部觀光署", "捷運國父紀念館站(忠孝)", "聯合報", "捷運市政府站", "市立工農", "捷運永春站(忠孝)",
        "捷運永春站(松山)", "雙永國小", "永吉松山路口", "松山車站(松山)"
    ],
    "連結": [
        "stop.jsp?sid=36021", "stop.jsp?sid=36022", "stop.jsp?sid=36023", "stop.jsp?sid=36024", "stop.jsp?sid=36025",
        "stop.jsp?sid=36026", "stop.jsp?sid=36027", "stop.jsp?sid=36028", "stop.jsp?sid=36029", "stop.jsp?sid=36030",
        "stop.jsp?sid=36031", "stop.jsp?sid=36032", "stop.jsp?sid=129828", "stop.jsp?sid=36033", "stop.jsp?sid=36034",
        "stop.jsp?sid=36036", "stop.jsp?sid=36038", "stop.jsp?sid=36039", "stop.jsp?sid=36040", "stop.jsp?sid=36041",
        "stop.jsp?sid=36042", "stop.jsp?sid=36043", "stop.jsp?sid=36044", "stop.jsp?sid=36045", "stop.jsp?sid=36046",
        "stop.jsp?sid=218023", "stop.jsp?sid=36047", "stop.jsp?sid=36048", "stop.jsp?sid=36049", "stop.jsp?sid=36050",
        "stop.jsp?sid=36051", "stop.jsp?sid=36052", "stop.jsp?sid=36053", "stop.jsp?sid=36054", "stop.jsp?sid=36055",
        "stop.jsp?sid=36056", "stop.jsp?sid=36057", "stop.jsp?sid=36058", "stop.jsp?sid=36059", "stop.jsp?sid=36060",
        "stop.jsp?sid=36061", "stop.jsp?sid=36063", "stop.jsp?sid=36064", "stop.jsp?sid=36065", "stop.jsp?sid=36066",
        "stop.jsp?sid=36067", "stop.jsp?sid=36068", "stop.jsp?sid=36069", "stop.jsp?sid=36070", "stop.jsp?sid=36071",
        "stop.jsp?sid=36072", "stop.jsp?sid=36073", "stop.jsp?sid=36074", "stop.jsp?sid=36075"
    ],
    "方向": ["去程"] * 54
}

data_back = {
    "站點名稱": [
        "虎林街口", "永吉國中", "松隆路口", "松山高中(松隆)", "聯合報", "捷運國父紀念館站(忠孝)", "交通部觀光署", "阿波羅大廈", "捷運忠孝敦化站", "頂好市場",
        "捷運忠孝復興站", "正義郵局", "臺北科技大學(忠孝)", "忠孝國小", "華山文創園區", "捷運善導寺站", "臺北車站(忠孝)", "重安街口", "三重中學", "三重國民運動中心",
        "集美國小", "菜寮(重新路)", "捷運菜寮站", "中山藝術公園", "正義重新路口", "長元西街口", "龍門路口", "德林寺(三和路)", "厚德派出所", "格致中學(三和路)",
        "三和國中", "捷運三和國中站", "建和新村", "幸福市場", "捷運徐匯中學站", "民和公寓", "溪墘", "蘆洲派出所", "蘆洲監理站(中正路)", "蘆洲國小",
        "中原公寓", "空中大學(中正路)", "王爺廟口", "蘆洲總站"
    ],
    "連結": [
        "stop.jsp?sid=36077", "stop.jsp?sid=36078", "stop.jsp?sid=36079", "stop.jsp?sid=36080", "stop.jsp?sid=36081",
        "stop.jsp?sid=36082", "stop.jsp?sid=36083", "stop.jsp?sid=36084", "stop.jsp?sid=36085", "stop.jsp?sid=36086",
        "stop.jsp?sid=36087", "stop.jsp?sid=36088", "stop.jsp?sid=36089", "stop.jsp?sid=36090", "stop.jsp?sid=36091",
        "stop.jsp?sid=36092", "stop.jsp?sid=36093", "stop.jsp?sid=36094", "stop.jsp?sid=36095", "stop.jsp?sid=36096",
        "stop.jsp?sid=36097", "stop.jsp?sid=36098", "stop.jsp?sid=36099", "stop.jsp?sid=56960", "stop.jsp?sid=36101",
        "stop.jsp?sid=36102", "stop.jsp?sid=36105", "stop.jsp?sid=36106", "stop.jsp?sid=36108", "stop.jsp?sid=36109",
        "stop.jsp?sid=36110", "stop.jsp?sid=129829", "stop.jsp?sid=36111", "stop.jsp?sid=36112", "stop.jsp?sid=36113",
        "stop.jsp?sid=36114", "stop.jsp?sid=36115", "stop.jsp?sid=36116", "stop.jsp?sid=36117", "stop.jsp?sid=36118",
        "stop.jsp?sid=36119", "stop.jsp?sid=36120", "stop.jsp?sid=36121", "stop.jsp?sid=36122"
    ],
    "方向": ["返程"] * 44
}

# 將資料轉換為 DataFrame
df_go = pd.DataFrame(data_go)
df_back = pd.DataFrame(data_back)

# 合併去程和返程資料
df_all = pd.concat([df_go, df_back], ignore_index=True)

# 基礎 URL
base_url = "https://pda5284.gov.taipei/MQS/"

# 創建資料夾以儲存 HTML 檔案
output_folder = "downloaded_html"
os.makedirs(output_folder, exist_ok=True)

# 遍歷每個站點，下載對應的 HTML 並儲存
for index, row in df_all.iterrows():
    station_name = row["站點名稱"]
    direction = row["方向"]
    relative_link = row["連結"]
    full_url = base_url + relative_link

    try:
        # 提取 sid 作為檔案名稱的一部分
        sid = relative_link.split("sid=")[-1]
        filename = os.path.join(output_folder, f"bus_stop_{sid}.html")

        # 發送 GET 請求
        response = requests.get(full_url, timeout=10)
        if response.status_code == 200:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"已成功下載並儲存 {station_name} ({direction}) 的 HTML 檔案為 {filename}")
        else:
            print(f"無法下載 {station_name} ({direction}) 的網頁，HTTP 狀態碼: {response.status_code}")
    except Exception as e:
        print(f"下載 {station_name} ({direction}) 時發生錯誤: {e}")
        time.sleep(5)  # 等待 5 秒後重試

print(f"所有超連結已成功下載並儲存到資料夾: {output_folder}")