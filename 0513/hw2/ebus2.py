from playwright.sync_api import sync_playwright

class BusInfoFetcher:
    def __init__(self, route_id):
        """
        初始化 BusInfoFetcher 類別
        :param route_id: 公車代碼
        """
        self.route_id = route_id
        self.stops = []  # 用於存儲站點資訊

    def fetch_bus_stops(self):
        """
        使用 Playwright 抓取公車站名與進站時間
        """
        route_url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={self.route_id}"
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # 啟動無頭瀏覽器
            page = browser.new_page()
            
            print(f"正在訪問 URL：{route_url}")
            page.goto(route_url, timeout=60000)  # 設置超時時間為 60 秒
            page.wait_for_selector("li .auto-list-stationlist", timeout=60000)
            page.wait_for_timeout(5000)  # 額外等待 5 秒，確保資料完全載入
            print("網頁載入完成")
            
            # 選取所有站點的 HTML 節點
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
                    if not all([stop_number_element, stop_name_element, stop_id_element, latitude_element, longitude_element]):
                        print(f"無法找到完整的站點資訊，HTML: {stop.inner_html()}")
                        continue
                    
                    # 提取資料
                    arrival_time = arrival_time_element.inner_text().strip() if arrival_time_element else "未知"
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
            
            browser.close()
        self.stops = result

    def get_stop_info(self, stop_id):
        """
        根據站牌 ID 獲取站牌資訊
        :param stop_id: 車站 ID
        :return: 包含站牌資訊的字典
        """
        for stop in self.stops:
            if stop["車站編號"] == stop_id:
                return stop
        return None


if __name__ == "__main__":
    # 提示使用者輸入公車代碼
    route_id = input("請輸入公車代碼 (例如 '0100000A00')：")
    bus_info_fetcher = BusInfoFetcher(route_id)
    
    # 抓取站點資訊
    bus_info_fetcher.fetch_bus_stops()
    
    # 顯示所有站點資訊
    print("\n公車站點資訊：")
    for stop in bus_info_fetcher.stops:
        print(f"到達時間: {stop['到達時間']}, 車站序號: {stop['車站序號']}, 車站名稱: {stop['車站名稱']}, 車站編號: {stop['車站編號']}, 緯度: {stop['緯度']}, 經度: {stop['經度']}")

    # 提示使用者輸入站牌 ID
    stop_id = input("\n請輸入要查詢的站牌 ID：")
    stop_info = bus_info_fetcher.get_stop_info(stop_id)
    
    # 顯示查詢結果
    if stop_info:
        print("\n查詢結果：")
        for key, value in stop_info.items():
            print(f"{key}: {value}")
    else:
        print("未找到對應的站牌資訊。")