import sys
import os

# 動態添加模組路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, "../../src/cycu"))
sys.path.append(parent_dir)

from cycu.ebus_map import fetch_bus_stops  # 匯入 fetch_bus_stops 函數

def test_city1_bus_stops():
    """
    測試 fetch_bus_stops 函數，並輸出結果
    """
    route_id = input("請輸入公車代碼 (例如 '0100000A00')：")
    try:
        bus_stops = fetch_bus_stops(route_id)
        if not bus_stops:
            print("未能取得任何資料，請檢查公車代碼是否正確。")
        else:
            print("公車站點資訊：")
            for stop in bus_stops:
                print(f"到達時間: {stop[0]}, 車站序號: {stop[1]}, 車站名稱: {stop[2]}, 車站編號: {stop[3]}, 緯度: {stop[4]}, 經度: {stop[5]}")
    except Exception as e:
        print(f"發生錯誤：{e}")

if __name__ == "__main__":
    test_city1_bus_stops()