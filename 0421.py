from playwright.sync_api import sync_playwright
import csv

def fetch_bus_stops(route_id):
    """
    使用 Playwright 渲染網頁並抓取公車站名與進站時間
    :param route_id: 公車代碼
    :return: 公車站點的詳細資訊列表，包括到達時間、車站序號、車站名稱、車站編號、經緯度
    """
    route_url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    print(f"正在訪問 URL：{route_url}")
    
    try:
        with sync_playwright() as p:
            # 啟動瀏覽器
            browser = p.chromium.launch(headless=True)  # 無頭模式
            page = browser.new_page()
            
            # 打開目標網址
            page.goto(route_url, timeout=60000)
            
            # 等待網頁加載完成
            page.wait_for_load_state("networkidle")
            
            # 提取 JSON 資料
            raw_data = page.evaluate("document.querySelector('pre').innerText")
            data = json.loads(raw_data)
            
            # 提取站點資訊
            stops = data.get("Stops", [])
            result = []
            for stop in stops:
                # 提取資料
                estimate_time = stop.get("EstimateTime")
                stop_sequence = stop.get("StopSequence")
                stop_name = stop.get("StopName", {}).get("Zh_tw", "未知")
                stop_id = stop.get("StopID")
                latitude = stop.get("StopPosition", {}).get("PositionLat")
                longitude = stop.get("StopPosition", {}).get("PositionLon")
                
                # 將秒數轉換為分鐘，若無資料則顯示「進站中」
                if estimate_time is not None:
                    estimate_time = f"{estimate_time // 60}分鐘"
                else:
                    estimate_time = "進站中"
                
                # 加入結果列表
                result.append((estimate_time, stop_sequence, stop_name, stop_id, latitude, longitude))
            
            print(f"成功提取 {len(result)} 筆資料")
            return result
    except Exception as e:
        print(f"發生錯誤：{e}")
        return []

def save_to_csv(data, filename):
    """
    將資料儲存為 CSV 格式
    :param data: 公車站點資料列表
    :param filename: 輸出的 CSV 檔案名稱
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 寫入標題
        writer.writerow(["到達時間", "車站序號", "車站名稱", "車站編號", "緯度", "經度"])
        # 寫入資料
        writer.writerows(data)

# 主程式
if __name__ == "__main__":
    route_id = input("請輸入公車代碼 (例如 '0100000100')：")
    try:
        bus_stops = fetch_bus_stops(route_id)
        if not bus_stops:
            print("未能取得任何資料，請檢查公車代碼是否正確。")
        else:
            # 儲存為 CSV
            filename = f"{route_id}.csv"
            save_to_csv(bus_stops, filename)
            print(f"資料已成功儲存為 {filename}")
    except Exception as e:
        print(f"發生錯誤：{e}")