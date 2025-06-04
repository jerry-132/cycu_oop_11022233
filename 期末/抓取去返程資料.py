import json
import csv
from playwright.sync_api import sync_playwright

# 公車代碼對應公車名稱字典（請依實際需求補齊）
bus_code_to_name = {
    "0100000A00": "0東",
    "0100000B00": "1",
    "0100000100": "15",
    "0100000200": "18",
    "0100000500": "21",
    "0400000800": "222",
    "0100000900": "28"
}

def fetch_bus_stop_names(route_id):
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    stops = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_selector("ul.auto-list-pool.stationlist-list-pool", timeout=60000)

        # 先抓去程
        stop_elements = page.query_selector_all("ul.auto-list-pool.stationlist-list-pool li")
        for stop in stop_elements:
            try:
                stop_name = stop.query_selector("span.auto-list-stationlist-place").inner_text().strip()
                stops.append(("去程", route_id, stop_name))
            except Exception as e:
                print(f"去程處理站點時發生錯誤：{e}")

        # 點擊返程按鈕
        try:
            come_btn = page.query_selector("a.stationlist-come")
            if come_btn:
                come_btn.click()
                page.wait_for_timeout(1000)  # 等待返程資料載入
                stop_elements = page.query_selector_all("ul.auto-list-pool.stationlist-list-pool li")
                for stop in stop_elements:
                    try:
                        stop_name = stop.query_selector("span.auto-list-stationlist-place").inner_text().strip()
                        stops.append(("返程", route_id, stop_name))
                    except Exception as e:
                        print(f"返程處理站點時發生錯誤：{e}")
        except Exception as e:
            print(f"找不到返程按鈕或切換失敗：{e}")

        browser.close()
    return stops

def read_routes_from_json(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return [route["路線代碼"] for route in data]

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["方向", "公車代碼", "公車名稱", "站點名稱"])
        for row in data:
            direction, route_id, stop_name = row
            bus_name = bus_code_to_name.get(route_id, "")
            writer.writerow([direction, route_id, bus_name, stop_name])
    print(f"資料已成功儲存為 {filename}")

# 主程式
if __name__ == "__main__":
    try:
        route_file = "taipei_bus_routes.json"
        route_ids = read_routes_from_json(route_file)
        all_stops = []
        for route_id in route_ids:
            all_stops.extend(fetch_bus_stop_names(route_id))
        output_file = "taipei_bus_stop_names_with_direction.csv"
        save_to_csv(all_stops, output_file)
    except Exception as e:
        print(f"發生錯誤：{e}")