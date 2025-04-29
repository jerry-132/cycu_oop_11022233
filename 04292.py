import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib import rcParams
from rapidfuzz import process, fuzz  # 用於相似度匹配
import os

# 設定 Matplotlib 使用支援中文的字體
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體
rcParams['axes.unicode_minus'] = False  # 解決負號顯示問題

# Main program
if __name__ == "__main__":
    # CSV 檔案名稱
    csv_file = r"C:\Users\User\Documents\cycu_oop_11022233\0161000900.csv"  # CSV 檔案路徑
    geojson_file = "bus_stop2.geojson"  # GeoJSON 檔案名稱
    icon_path_red = r"C:\Users\User\Documents\cycu_oop_11022233\pink_circle_transparent.png"  # 紅色圖示
    icon_path_bus = r"C:\Users\User\Documents\cycu_oop_11022233\ChatGPT Image 2025年4月29日 下午07_23_27.png"  # 公車圖示
    icon_path_person = r"C:\Users\User\Documents\cycu_oop_11022233\ChatGPT Image 2025年4月29日 下午06_39_19.png"  # 小人圖示

    # 檢查圖示檔案是否存在
    for path in [icon_path_red, icon_path_bus, icon_path_person]:
        if not os.path.exists(path):
            print(f"錯誤：找不到圖示檔案 - {path}")
            exit()

    try:
        # 讀取 CSV 檔案
        df_csv = pd.read_csv(csv_file, header=None, names=["到達時間", "車站序號", "車站名稱", "車站編號", "緯度", "經度"])

        # 檢查是否成功讀取 CSV 資料
        if df_csv.empty:
            print("CSV 檔案為空或無法讀取。")
        else:
            print(f"成功讀取 {len(df_csv)} 筆公車站點資料。")

            # 讀取 GeoJSON 檔案
            gdf_geojson = gpd.read_file(geojson_file)

            # 檢查是否成功讀取 GeoJSON 資料
            if gdf_geojson.empty:
                print("GeoJSON 檔案為空或無法讀取。")
            else:
                print(f"成功讀取 {len(gdf_geojson)} 筆地理資料。")

                # 使用相似度匹配站名
                matched_names = []
                for csv_name in df_csv["車站名稱"]:
                    match = process.extractOne(
                        csv_name, gdf_geojson["BSM_CHINES"], scorer=fuzz.ratio
                    )
                    if match and match[1] >= 80:  # 相似度達到 80%
                        matched_names.append((csv_name, match[0]))

                # 建立匹配的 DataFrame
                matched_df = pd.DataFrame(matched_names, columns=["CSV站名", "GeoJSON站名"])
                print("相似度匹配結果：")
                print(matched_df)

                # 將匹配結果應用到原始資料
                df_csv["匹配站名"] = df_csv["車站名稱"].map(
                    dict(matched_names)
                )

                # 匹配 CSV 與 GeoJSON 資料
                merged_data = pd.merge(
                    df_csv,
                    gdf_geojson,
                    left_on="匹配站名",  # 使用匹配後的站名
                    right_on="BSM_CHINES",  # GeoJSON 中的車站名稱
                    how="inner"  # 僅保留匹配的資料
                )

                # 檢查是否有匹配的資料
                if merged_data.empty:
                    print("無法匹配任何資料，請檢查 CSV 與 GeoJSON 的車站名稱是否一致。")
                else:
                    print(f"成功匹配 {len(merged_data)} 筆資料。")

                    # 將匹配的資料轉換為 GeoDataFrame
                    gdf_merged = gpd.GeoDataFrame(merged_data, geometry=merged_data["geometry"])

                    # 列出所有匹配的站名
                    print("匹配的站名如下：")
                    print(gdf_merged["車站名稱"].unique())

                    # 讓使用者輸入站名
                    station_name = input("請輸入要顯示的站名：").strip()

                    # 繪製地圖
                    fig, ax = plt.subplots(figsize=(10, 10))
                    gdf_geojson.plot(ax=ax, color='lightgrey', alpha=0.5, label='All Bus Stops')  # 繪製所有站點

                    # 加載圖示並繪製每個站點
                    for _, row in gdf_merged.iterrows():
                        station_coords = row.geometry.coords[0]
                        arrival_status = row["到達時間"].strip()  # 去除空格
                        station_name_cleaned = row["車站名稱"].strip()  # 去除空格並清理站名

                        # 判斷圖示順序
                        if station_name_cleaned == station_name:  # 使用者輸入的站點
                            icon_path = icon_path_person  # 使用小人圖示
                        elif arrival_status == "進站中":  # 到達時間為進站中的站點
                            icon_path = icon_path_bus  # 使用公車圖示
                        else:  # 其他站點
                            icon_path = icon_path_red  # 使用紅色圖示

                        # 加載圖示
                        icon = plt.imread(icon_path)
                        image_box = OffsetImage(icon, zoom=0.02)  # 調整圖示大小
                        ab = AnnotationBbox(image_box, station_coords, frameon=False)
                        ax.add_artist(ab)

                    # 設定地圖標題與標籤
                    ax.set_title(f"{station_name} 的位置", fontsize=16)
                    plt.xlabel("經度")
                    plt.ylabel("緯度")
                    plt.grid(True)
                    plt.legend()

                    # 顯示地圖
                    plt.show()

    except FileNotFoundError as e:
        print(f"錯誤：找不到檔案 - {e}")
    except Exception as e:
        print(f"發生錯誤：{e}")