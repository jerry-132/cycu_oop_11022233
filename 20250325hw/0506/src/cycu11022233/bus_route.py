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

def process_bus_route(csv_file, geojson_file, icon_paths):
    """
    處理公車站點資料並繪製地圖。

    :param csv_file: CSV 檔案路徑
    :param geojson_file: GeoJSON 檔案路徑
    :param icon_paths: 圖示檔案路徑字典，包含 'red', 'bus', 'person'
    """
    # 檢查圖示檔案是否存在
    for path in icon_paths.values():
        if not os.path.exists(path):
            print(f"錯誤：找不到圖示檔案 - {path}")
            return

    try:
        # 讀取 CSV 檔案
        df_csv = pd.read_csv(csv_file, header=None, names=["到達時間", "車站序號", "車站名稱", "車站編號", "緯度", "經度"])

        # 檢查是否成功讀取 CSV 資料
        if df_csv.empty:
            print("CSV 檔案為空或無法讀取。")
            return

        print(f"成功讀取 {len(df_csv)} 筆公車站點資料。")

        # 讀取 GeoJSON 檔案
        gdf_geojson = gpd.read_file(geojson_file)

        # 檢查是否成功讀取 GeoJSON 資料
        if gdf_geojson.empty:
            print("GeoJSON 檔案為空或無法讀取。")
            return

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
        df_csv["匹配站名"] = df_csv["車站名稱"].map(dict(matched_names))

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
            return

        print(f"成功匹配 {len(merged_data)} 筆資料。")

        # 將匹配的資料轉換為 GeoDataFrame
        gdf_merged = gpd.GeoDataFrame(merged_data, geometry=merged_data["geometry"])

        # 列出所有匹配的站名
        print("匹配的站名如下：")
        print(gdf_merged["車站名稱"].unique())

        # 繪製地圖（簡化範例）
        fig, ax = plt.subplots(figsize=(16, 16))
        gdf_geojson.plot(ax=ax, color='lightgrey', alpha=0.5, label='All Bus Stops')
        gdf_merged.plot(ax=ax, color='red', label='Matched Bus Stops')
        plt.title("公車站點地圖")
        plt.legend()
        plt.show()

    except FileNotFoundError as e:
        print(f"錯誤：找不到檔案 - {e}")
    except Exception as e:
        print(f"發生錯誤：{e}")