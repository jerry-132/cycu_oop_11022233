import json
import csv
from playwright.sync_api import sync_playwright

def fetch_bus_stop_names(route_id):
    """
    使用 Playwright 抓取指定公車路線的所有站點名稱
    :param route_id: 公車代碼
    :return: 車站名稱列表
    """
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    stop_names = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 啟動無頭瀏覽器
        page = browser.new_page()

        print(f"正在訪問 URL：{url}")
        page.goto(url, timeout=60000)  # 設置超時時間為 60 秒
        page.wait_for_selector("ul.auto-list-pool.stationlist-list-pool", timeout=60000)  # 等待頁面載入完成
        print(f"抓取路線 {route_id} 的站點名稱")

        # 抓取所有站點名稱
        stop_elements = page.query_selector_all("ul.auto-list-pool.stationlist-list-pool li")
        for stop in stop_elements:
            try:
                stop_name = stop.query_selector("span.auto-list-stationlist-place").inner_text().strip()  # 車站名稱
                stop_names.append(stop_name)
            except Exception as e:
                print(f"處理站點時發生錯誤：{e}")

        browser.close()
    return stop_names

def read_routes_from_json(filename):
    """
    從 JSON 檔案中讀取所有公車代碼
    :param filename: JSON 檔案名稱
    :return: 公車代碼列表
    """
    with open(filename, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return [route["路線代碼"] for route in data]

def save_to_csv(data, filename):
    """
    將資料儲存為 CSV 格式
    :param data: 公車站點資料字典
    :param filename: 輸出的 CSV 檔案名稱
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 寫入標題
        writer.writerow(["公車代碼", "站點名稱"])
        # 寫入資料
        for route_id, stop_names in data.items():
            for stop_name in stop_names:
                writer.writerow([route_id, stop_name])
    print(f"資料已成功儲存為 {filename}")

# 主程式
if __name__ == "__main__":
    try:
        # 讀取所有公車代碼
        route_file = "taipei_bus_routes.json"
        route_ids = read_routes_from_json(route_file)

        all_stops = {}
        for route_id in route_ids:
            stop_names = fetch_bus_stop_names(route_id)
            all_stops[route_id] = stop_names

        # 儲存為 CSV
        output_file = "taipei_bus_stop_names.csv"
        save_to_csv(all_stops, output_file)
    except Exception as e:
        print(f"發生錯誤：{e}")