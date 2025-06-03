def fetch_bus_stop_details(route_id):
    """
    使用 Playwright 抓取指定公車路線的所有站點名稱及經緯度
    :param route_id: 公車代碼
    :return: 車站詳細資訊列表 (包含公車名稱、站點名稱、經緯度)
    """
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    stop_details = []
    bus_name = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 啟動無頭瀏覽器
        page = browser.new_page()

        print(f"正在訪問 URL：{url}")
        page.goto(url, timeout=60000)  # 設置超時時間為 60 秒

        # 等待頁面載入完成
        try:
            page.wait_for_selector("div.stationlist-text-c", timeout=90000)  # 增加等待時間
        except Exception as e:
            print(f"等待目標元素超時，路線代碼: {route_id}, 錯誤: {e}")
            browser.close()
            return stop_details

        print(f"抓取路線 {route_id} 的站點詳細資訊")

        # 抓取公車名稱
        try:
            bus_name_element = page.query_selector("span.stationlist-title")
            if bus_name_element:
                bus_name = bus_name_element.inner_text().strip()
            else:
                print(f"無法找到公車名稱元素，路線代碼: {route_id}")
        except Exception as e:
            print(f"無法抓取公車名稱，路線代碼: {route_id}, 錯誤: {e}")

        # 抓取所有站點資訊
        stop_elements = page.query_selector_all("ul.auto-list-pool.stationlist-list-pool li")
        for stop in stop_elements:
            try:
                # 提取站點名稱
                stop_name = stop.query_selector("span.auto-list-stationlist-place").inner_text().strip()
                # 提取經緯度
                latitude = stop.query_selector("input#item_Latitude").get_attribute("value")
                longitude = stop.query_selector("input#item_Longitude").get_attribute("value")
                # 將資料加入列表
                stop_details.append((bus_name, stop_name, latitude, longitude))
            except Exception as e:
                print(f"處理站點時發生錯誤：{e}")

        browser.close()
    return stop_details