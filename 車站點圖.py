import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Main program
if __name__ == "__main__":
    # CSV 檔案名稱
    csv_file = "0161000900.csv"  # Replace with your CSV file name
    geojson_file = "bus_stop2.geojson"  # GeoJSON file name

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

                # 匹配 CSV 與 GeoJSON 資料
                merged_data = pd.merge(
                    df_csv,
                    gdf_geojson,
                    left_on="車站名稱",  # CSV 中的車站名稱
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

                    # 繪製地圖
                    fig, ax = plt.subplots(figsize=(10, 10))
                    gdf_geojson.plot(ax=ax, color='lightgrey', alpha=0.5, label='All Bus Stops')  # 繪製所有站點
                    gdf_merged.plot(ax=ax, color='blue', alpha=0.7, label='Matched Bus Stops')  # 繪製匹配的站點

                    # 設定地圖標題與標籤
                    ax.set_title("Matched Bus Stops Map", fontsize=16)
                    plt.xlabel("Longitude")
                    plt.ylabel("Latitude")
                    plt.grid(True)
                    plt.legend()

                    # 顯示地圖
                    plt.show()

    except FileNotFoundError as e:
        print(f"錯誤：找不到檔案 - {e}")
    except Exception as e:
        print(f"發生錯誤：{e}")