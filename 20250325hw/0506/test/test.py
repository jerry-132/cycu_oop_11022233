import cycu11022233

if __name__ == "__main__":
    # 定義檔案路徑
    csv_file = r"C:\Users\User\Documents\GitHub\cycu_oop_11022233\0161000900.csv"
    geojson_file = r"C:\Users\User\Documents\GitHub\cycu_oop_11022233\bus_stop2.geojson"
    icon_paths = {
        "red": r"C:\Users\User\Documents\GitHub\cycu_oop_11022233\pink_circle_transparent.png",
        "bus": r"C:\Users\User\Documents\GitHub\cycu_oop_11022233\ChatGPT Image 2025年4月29日 下午07_23_27.png",
        "person": r"C:\Users\User\Documents\GitHub\cycu_oop_11022233\ChatGPT Image 2025年4月29日 下午06_39_19.png"
    }

    # 呼叫函數處理資料
    cycu11022233.process_bus_route(csv_file, geojson_file, icon_paths)