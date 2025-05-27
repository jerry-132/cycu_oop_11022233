import json
from playwright.sync_api import sync_playwright

def fetch_bus_stops(route_id):
    """
    使用 Playwright 抓取公車站名與進站時間（包含去程與返程）
    :param route_id: 公車代碼
    :return: 去程與返程的公車站點詳細資訊
    """
    route_url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 啟動無頭瀏覽器
        page = browser.new_page()
        
        print(f"正在訪問 URL：{route_url}")
        page.goto(route_url, timeout=60000)  # 設置超時時間為 60 秒
        page.wait_for_selector("li .auto-list-stationlist", timeout=60000)
        page.wait_for_timeout(5000)  # 額外等待 5 秒，確保資料完全載入
        print("網頁載入完成")
        
        # 抓取去程資訊
        print("抓取去程資訊...")
        go_stops = extract_stops(page)

        # 切換到返程
        print("切換到返程...")
        return_button = page.query_selector("a.stationlist-come")
        if return_button:
            return_button.click()
            page.wait_for_selector("li .auto-list-stationlist", timeout=60000)
            page.wait_for_timeout(5000)  # 額外等待 5 秒，確保資料完全載入
            print("抓取返程資訊...")
            return_stops = extract_stops(page)
        else:
            print("未找到返程按鈕，可能該路線沒有返程資訊。")
            return_stops = []

        browser.close()
    return {"去程": go_stops, "返程": return_stops}

def extract_stops(page):
    """
    從當前頁面提取站點資訊
    :param page: Playwright 的頁面對象
    :return: 公車站點的詳細資訊列表
    """
    stop_elements = page.query_selector_all("li .auto-list-stationlist")
    print(f"找到的站點數量：{len(stop_elements)}")  # 除錯輸出
    result = []
    for stop in stop_elements:
        try:
            # 提取站名、進站時間、車站序號、車站名稱、車站編號、經緯度
            arrival_time_element = stop.query_selector(".auto-list-stationlist-position-time, .auto-list-stationlist-position-now, .auto-list-stationlist-position-none")
            stop_number_element = stop.query_selector(".auto-list-stationlist-number")
            stop_name_element = stop.query_selector(".auto-list-stationlist-place")
            stop_id_element = stop.query_selector("input#item_UniStopId")
            latitude_element = stop.query_selector("input#item_Latitude")
            longitude_element = stop.query_selector("input#item_Longitude")
            
            # 檢查元素是否存在
            if not all([arrival_time_element, stop_number_element, stop_name_element, stop_id_element, latitude_element, longitude_element]):
                print(f"無法找到完整的站點資訊，HTML: {stop.inner_html()}")
                continue
            
            # 提取資料
            arrival_time = arrival_time_element.inner_text().strip()
            stop_number = stop_number_element.inner_text().strip()
            stop_name = stop_name_element.inner_text().strip()
            stop_id = stop_id_element.get_attribute("value")
            latitude = latitude_element.get_attribute("value")
            longitude = longitude_element.get_attribute("value")
            
            # 如果到達時間為空、進站中或尚未發車，記錄為相應的狀態
            if not arrival_time or arrival_time.strip() == "":
                arrival_time = "未知"
            elif "進站中" in arrival_time:
                arrival_time = "進站中"
            elif "尚未發車" in arrival_time:
                arrival_time = "尚未發車"
            
            # 將資料加入結果列表
            result.append({
                "到達時間": arrival_time,
                "車站序號": stop_number,
                "車站名稱": stop_name,
                "車站編號": stop_id,
                "緯度": latitude,
                "經度": longitude
            })
        except Exception as e:
            print(f"處理站點時發生錯誤：{e}")
            print(f"站點 HTML: {stop.inner_html()}")
    return result

def save_to_json(data, filename):
    """
    將資料儲存為 JSON 格式
    :param data: 公車站點資料列表
    :param filename: 輸出的 JSON 檔案名稱
    """
    json_filename = f"{filename}.json"
    with open(json_filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # 使用 UTF-8 編碼並格式化輸出
    print(f"資料已成功儲存為 {json_filename}")

# 主程式
if __name__ == "__main__":
    route_id = input("請輸入公車代碼 (例如 '0100000A00')：")
    try:
        bus_stops = fetch_bus_stops(route_id)
        if not bus_stops["去程"] and not bus_stops["返程"]:
            print("未能取得任何資料，請檢查公車代碼是否正確。")
        else:
            # 儲存為 JSON
            filename = f"{route_id}"
            save_to_json(bus_stops, filename)
    except Exception as e:
        print(f"發生錯誤：{e}")