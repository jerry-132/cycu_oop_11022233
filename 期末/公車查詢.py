import csv
from playwright.sync_api import sync_playwright

def fetch_bus_stops(route_id):
    route_url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(route_url, timeout=60000)
        page.wait_for_selector("ul.auto-list-pool.stationlist-list-pool", timeout=60000)

        result = []

        # 先抓去程
        stop_elements = page.query_selector_all("ul.auto-list-pool.stationlist-list-pool li")
        for stop in stop_elements:
            try:
                arrival_time = stop.query_selector(".auto-list-stationlist-position-time, .auto-list-stationlist-position-now, .auto-list-stationlist-position-none").inner_text().strip()
                stop_number = stop.query_selector(".auto-list-stationlist-number").inner_text().strip()
                stop_name = stop.query_selector(".auto-list-stationlist-place").inner_text().strip()
                stop_id = stop.query_selector("input#item_UniStopId").get_attribute("value")
                latitude = stop.query_selector("input#item_Latitude").get_attribute("value")
                longitude = stop.query_selector("input#item_Longitude").get_attribute("value")
                result.append([
                    "去程",  # 新增方向
                    arrival_time, stop_number, stop_name, stop_id, latitude, longitude
                ])
            except Exception as e:
                print(f"去程處理站點時發生錯誤：{e}")

        # 點擊返程按鈕
        try:
            come_btn = page.query_selector("a.stationlist-come")
            if come_btn:
                come_btn.click()
                page.wait_for_timeout(1000)
                stop_elements = page.query_selector_all("ul.auto-list-pool.stationlist-list-pool li")
                for stop in stop_elements:
                    try:
                        arrival_time = stop.query_selector(".auto-list-stationlist-position-time, .auto-list-stationlist-position-now, .auto-list-stationlist-position-none").inner_text().strip()
                        stop_number = stop.query_selector(".auto-list-stationlist-number").inner_text().strip()
                        stop_name = stop.query_selector(".auto-list-stationlist-place").inner_text().strip()
                        stop_id = stop.query_selector("input#item_UniStopId").get_attribute("value")
                        latitude = stop.query_selector("input#item_Latitude").get_attribute("value")
                        longitude = stop.query_selector("input#item_Longitude").get_attribute("value")
                        result.append([
                            "返程",  # 新增方向
                            arrival_time, stop_number, stop_name, stop_id, latitude, longitude
                        ])
                    except Exception as e:
                        print(f"返程處理站點時發生錯誤：{e}")
        except Exception as e:
            print(f"找不到返程按鈕或切換失敗：{e}")

        browser.close()
    return result

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["方向", "到達時間", "車站序號", "車站名稱", "車站編號", "緯度", "經度"])
        writer.writerows(data)

if __name__ == "__main__":
    route_id = input("請輸入公車代碼 (例如 '0100000A00')：")
    try:
        bus_stops = fetch_bus_stops(route_id)
        if not bus_stops:
            print("未能取得任何資料，請檢查公車代碼是否正確。")
        else:
            filename = f"{route_id}.csv"
            save_to_csv(bus_stops, filename)
            print(f"資料已成功儲存為 {filename}")
    except Exception as e:
        print(f"發生錯誤：{e}")