import json
import csv
from playwright.sync_api import sync_playwright

def fetch_bus_stop_details(route_id):
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    stop_details = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        try:
            page.wait_for_selector("div.stationlist-text-c", timeout=90000)
        except Exception as e:
            print(f"等待目標元素超時，路線代碼: {route_id}, 錯誤: {e}")
            browser.close()
            return stop_details

        # 抓取公車名稱
        try:
            bus_name_element = page.query_selector("span.stationlist-title")
            bus_name = bus_name_element.inner_text().strip() if bus_name_element else ""
        except Exception as e:
            print(f"無法抓取公車名稱，路線代碼: {route_id}, 錯誤: {e}")
            bus_name = ""

        # 去程
        stop_elements = page.query_selector_all("ul.auto-list-pool.stationlist-list-pool li")
        for stop in stop_elements:
            try:
                stop_name = stop.query_selector("span.auto-list-stationlist-place").inner_text().strip()
                latitude = stop.query_selector("input#item_Latitude").get_attribute("value")
                longitude = stop.query_selector("input#item_Longitude").get_attribute("value")
                stop_details.append(("去程", route_id, bus_name, stop_name, latitude, longitude))
            except Exception as e:
                print(f"去程處理站點時發生錯誤：{e}")

        # 返程
        try:
            come_btn = page.query_selector("a.stationlist-come")
            if come_btn:
                come_btn.click()
                page.wait_for_timeout(1000)
                stop_elements = page.query_selector_all("ul.auto-list-pool.stationlist-list-pool li")
                for stop in stop_elements:
                    try:
                        stop_name = stop.query_selector("span.auto-list-stationlist-place").inner_text().strip()
                        latitude = stop.query_selector("input#item_Latitude").get_attribute("value")
                        longitude = stop.query_selector("input#item_Longitude").get_attribute("value")
                        stop_details.append(("返程", route_id, bus_name, stop_name, latitude, longitude))
                    except Exception as e:
                        print(f"返程處理站點時發生錯誤：{e}")
        except Exception as e:
            print(f"找不到返程按鈕或切換失敗：{e}")

        browser.close()
    return stop_details

def read_routes_from_json(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return [route["路線代碼"] for route in data]

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["方向", "公車代碼", "公車名稱", "站點名稱", "緯度", "經度"])
        writer.writerows(data)
    print(f"資料已成功儲存為 {filename}")

# 主程式
if __name__ == "__main__":
    try:
        route_file = "taipei_bus_routes.json"
        route_ids = read_routes_from_json(route_file)
        all_stops = []
        for route_id in route_ids:
            print(f"正在抓取路線 {route_id} ...")
            all_stops.extend(fetch_bus_stop_details(route_id))
        output_file = "taipei_bus_stop_details_with_direction.csv"
        save_to_csv(all_stops, output_file)
    except Exception as e:
        print(f"發生錯誤：{e}")