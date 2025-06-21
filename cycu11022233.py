import csv
from playwright.sync_api import sync_playwright
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import folium
from folium.features import CustomIcon

def fetch_and_save_bus_stops(route_id, filename):
    """
    查詢指定公車代碼的去程與返程站點資訊，並存成CSV
    """
    route_url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(route_url, timeout=60000)
        page.wait_for_selector("ul.auto-list-pool.stationlist-list-pool", timeout=60000)

        result = []

        # 去程
        stop_elements = page.query_selector_all("ul.auto-list-pool.stationlist-list-pool li")
        for stop in stop_elements:
            try:
                direction = "去程"
                stop_name = stop.query_selector("span.auto-list-stationlist-place").inner_text().strip()
                latitude = stop.query_selector("input#item_Latitude").get_attribute("value")
                longitude = stop.query_selector("input#item_Longitude").get_attribute("value")
                result.append([direction, route_id, stop_name, latitude, longitude])
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
                        direction = "返程"
                        stop_name = stop.query_selector("span.auto-list-stationlist-place").inner_text().strip()
                        latitude = stop.query_selector("input#item_Latitude").get_attribute("value")
                        longitude = stop.query_selector("input#item_Longitude").get_attribute("value")
                        result.append([direction, route_id, stop_name, latitude, longitude])
                    except Exception as e:
                        print(f"返程處理站點時發生錯誤：{e}")
        except Exception as e:
            print(f"找不到返程按鈕或切換失敗：{e}")

        browser.close()

    # 存成CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["方向", "公車代碼", "站點名稱", "緯度", "經度"])
        writer.writerows(result)
    return result

def load_bus_routes(filepath):
    routes = {}
    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            route = row['公車代碼']
            direction = row['方向']
            stop = row['站點名稱']
            lat = float(row['緯度'])
            lon = float(row['經度'])
            key = (route, direction)
            if key not in routes:
                routes[key] = []
            routes[key].append((stop, lat, lon))
    return routes

def find_routes_with_direction(routes, start, end):
    result = []
    for (route, direction), stops in routes.items():
        stop_names = [s[0] for s in stops]
        if start in stop_names and end in stop_names:
            s_idx = stop_names.index(start)
            e_idx = stop_names.index(end)
            if s_idx < e_idx:
                result.append((route, direction, stops, s_idx, e_idx))
    return result

def get_wait_time_by_selenium(route_code, stop):
    url = f"https://ebus.gov.taipei/EBus/VsSimpleMap?routeid={route_code}&gb=0"
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    current_bus_stops = []

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sm.left"))
        )
        blocks = driver.find_elements(By.CSS_SELECTOR, "div.sm.left")
        wait_time = "查無狀態"
        for block in blocks:
            try:
                stop_name_element = block.find_element(By.CSS_SELECTOR, ".snz span")
                stop_name = stop_name_element.text.strip()
                try:
                    eta_span = block.find_element(By.CSS_SELECTOR, ".eta_coming, .eta_onroad")
                    eta_text = eta_span.text.strip()
                except Exception as e:
                    eta_text = "查無狀態"
                if "進站" in eta_text or "即將進站" in eta_text:
                    current_bus_stops.append(stop_name)
                if stop in stop_name:
                    if "末班車已駛離" in eta_text or "末班已過" in eta_text:
                        wait_time = "末班已過"
                    else:
                        wait_time = eta_text
            except Exception as e:
                continue
        driver.quit()
        return wait_time, current_bus_stops
    except Exception as e:
        driver.quit()
        return f"查詢失敗: {e}", []

def plot_route_map(stops, start_idx, end_idx, start, end, bus_stops):
    m = folium.Map(location=[stops[start_idx][1], stops[start_idx][2]], zoom_start=14)
    route_points = [(s[1], s[2]) for s in stops]
    folium.PolyLine(route_points, color='blue', weight=5, opacity=0.7).add_to(m)
    folium.Marker(
        location=[stops[start_idx][1], stops[start_idx][2]],
        popup=f"<b>{stops[start_idx][0]}</b>",
        icon=CustomIcon(r'C:\Users\User\OneDrive\文件\GitHub\cycu_oop_11022233\期末\小人圖片.png', icon_size=(32, 32))
    ).add_to(m)
    folium.Marker(
        location=[stops[end_idx][1], stops[end_idx][2]],
        popup=f"<b>{stops[end_idx][0]}</b>",
        icon=CustomIcon('https://cdn-icons-png.flaticon.com/512/684/684908.png', icon_size=(32, 32))
    ).add_to(m)
    for bus_stop in bus_stops:
        idxs = [i for i, s in enumerate(stops) if s[0] == bus_stop]
        for idx in idxs:
            folium.Marker(
                location=[stops[idx][1], stops[idx][2]],
                popup=f"<b>{bus_stop}</b>",
                icon=CustomIcon(r'C:\Users\User\OneDrive\文件\GitHub\cycu_oop_11022233\期末\公車圖片.png', icon_size=(32, 32))
            ).add_to(m)
    m.save('bus_route_map.html')
    print('已產生 bus_route_map.html，請用瀏覽器開啟查看路線圖')

def check_route_validity(routes, start, end):
    valid_routes = find_routes_with_direction(routes, start, end)
    if not valid_routes:
        reverse_routes = find_routes_with_direction(routes, end, start)
        if reverse_routes:
            print(f"狀態：無此路線（{start} 無法到達 {end}，但 {end} 可以到達 {start}）")
        else:
            print(f"狀態：無此路線（{start} 和 {end} 之間無任何路線）")
        return False
    return True

if __name__ == "__main__":
    print("11022233張翔禎 公車查詢系統")
    route_id = input("請輸入公車代碼 (例如 '0100000A00')：").strip()
    csv_path = f"{route_id}_站點查詢.csv"
    stops_data = fetch_and_save_bus_stops(route_id, csv_path)

    # 顯示所有站點
    print("\n【去程站點】")
    for row in stops_data:
        if row[0] == "去程":
            print(row[2])
    print("\n【返程站點】")
    for row in stops_data:
        if row[0] == "返程":
            print(row[2])

    # 讀取站點資料進行路線查詢
    routes = load_bus_routes(csv_path)
    start = input("\n請輸入起點站名（請從上方站點複製貼上）：").strip()
    end = input("請輸入終點站名（請從上方站點複製貼上）：").strip()

    if not check_route_validity(routes, start, end):
        exit()

    found_routes = find_routes_with_direction(routes, start, end)
    if not found_routes:
        print("狀態：無此選項")
    else:
        found_routes.sort(key=lambda x: abs(x[4] - x[3]))
        print("推薦路線（依起點到終點之間站數最少排序）：")
        for idx, (route, direction, stops, s_idx, e_idx) in enumerate(found_routes):
            print(f"{idx+1}. 公車代碼：{route}，方向：{direction}，站數：{abs(e_idx-s_idx)+1}（{stops[s_idx][0]} → {stops[e_idx][0]}）")
        try:
            sel = int(input("請輸入要查詢的路線代號：")) - 1
            if sel < 0 or sel >= len(found_routes):
                print("輸入錯誤，自動選擇第 1 條路線。")
                sel = 0
        except:
            print("輸入錯誤，自動選擇第 1 條路線。")
            sel = 0
        route, direction, stops, start_idx, end_idx = found_routes[sel]
        wait_time, current_bus_stops = get_wait_time_by_selenium(route, stops[start_idx][0])
        if "進站" in wait_time:
            status = "進站中"
        elif "未發車" in wait_time:
            status = "尚未發車"
        elif "查無" in wait_time or "查詢失敗" in wait_time:
            status = wait_time
        else:
            status = f"{wait_time}抵達"
        print(f'"{stops[start_idx][0]}"前往"{stops[end_idx][0]}"的公車({route}) [{direction}] 狀態：{status}')
        if current_bus_stops:
            print(f"目前公車所在站：{'、'.join(current_bus_stops)}")
        else:
            print("目前無公車進站中")
        plot_route_map(stops, start_idx, end_idx, stops[start_idx][0], stops[end_idx][0], current_bus_stops)