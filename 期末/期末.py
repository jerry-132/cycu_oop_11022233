import json
from playwright.sync_api import sync_playwright

def fetch_all_bus_routes():
    """
    使用 Playwright 抓取臺北市所有公車路線的資訊
    :return: 公車路線的詳細資訊列表
    """
    url = "https://ebus.gov.taipei/ebus"
    all_routes = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 啟動無頭瀏覽器
        page = browser.new_page()

        print(f"正在訪問 URL：{url}")
        page.goto(url, timeout=60000)  # 設置超時時間為 60 秒
        page.wait_for_selector("ul#list", timeout=60000)  # 等待頁面載入完成
        print("網頁載入完成")

        # 抓取所有公車路線資訊
        route_elements = page.query_selector_all("ul#list li a")
        print(f"找到的公車路線數量：{len(route_elements)}")

        for route in route_elements:
            try:
                route_name = route.inner_text().strip()  # 公車名稱
                route_id = route.get_attribute("href").split("'")[1]  # 公車代碼

                all_routes.append({
                    "路線名稱": route_name,
                    "路線代碼": route_id
                })
            except Exception as e:
                print(f"處理路線時發生錯誤：{e}")

        browser.close()
    return all_routes

def save_to_json(data, filename):
    """
    將資料儲存為 JSON 格式
    :param data: 公車路線資料列表
    :param filename: 輸出的 JSON 檔案名稱
    """
    with open(filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # 使用 UTF-8 編碼並格式化輸出
    print(f"資料已成功儲存為 {filename}")

# 主程式
if __name__ == "__main__":
    try:
        bus_routes = fetch_all_bus_routes()
        if not bus_routes:
            print("未能取得任何資料，請檢查網站是否正常。")
        else:
            # 儲存為 JSON
            filename = "taipei_bus_routes.json"
            save_to_json(bus_routes, filename)
    except Exception as e:
        print(f"發生錯誤：{e}")