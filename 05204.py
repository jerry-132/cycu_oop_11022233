import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 設定支援中文的字型
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
rcParams['axes.unicode_minus'] = False  # 解決負號無法顯示的問題

# 讀取地圖 Shapefile 檔案
county_shapefile_path = './COUNTY_MOI_1140318.shp'
taipei_shapefile_path = './G97_A_CADIST_P.shp'

# 公車站點資料檔案
csv_file = "0161000900.csv"  # 替換為你的 CSV 檔案名稱

try:
    # 讀取縣市 Shapefile
    county_gdf = gpd.read_file(county_shapefile_path, encoding='utf-8')

    # 篩選出台北市、新北市、基隆市和桃園市
    target_cities = ['台北市', '新北市', '基隆市', '桃園市']
    filtered_county_gdf = county_gdf[county_gdf['COUNTYNAME'].isin(target_cities)].copy()

    # 修復多邊形，填充內部空洞
    filtered_county_gdf.loc[:, 'geometry'] = filtered_county_gdf['geometry'].apply(lambda geom: geom.buffer(0))

    # 嘗試讀取台北區域 Shapefile
    try:
        taipei_gdf = gpd.read_file(taipei_shapefile_path, encoding='utf-8')
    except Exception as e:
        print(f"無法讀取台北區域 Shapefile：{e}")
        taipei_gdf = gpd.GeoDataFrame()  # 如果無法讀取，建立空的 GeoDataFrame

    # 合併兩個 GeoDataFrame
    combined_gdf = gpd.GeoDataFrame(pd.concat([filtered_county_gdf, taipei_gdf], ignore_index=True))

    # 讀取公車站點資料，跳過標題行
    df_csv = pd.read_csv(csv_file, header=0, names=["到達時間", "車站序號", "車站名稱", "車站編號", "緯度", "經度"])

    # 檢查是否成功讀取 CSV 資料
    if df_csv.empty:
        print("CSV 檔案為空或無法讀取。")
    else:
        print(f"成功讀取 {len(df_csv)} 筆公車站點資料。")

        # 將公車站點資料轉換為 GeoDataFrame
        stops_gdf = gpd.GeoDataFrame(
            df_csv,
            geometry=gpd.points_from_xy(df_csv["經度"].astype(float), df_csv["緯度"].astype(float)),
            crs="EPSG:4326"  # WGS84 座標系統
        )

        # 繪製地理圖形
        plt.figure(figsize=(12, 10))
        combined_gdf.plot(ax=plt.gca(), color='lightblue', edgecolor='black', alpha=0.5, label="北北基桃地區")
        stops_gdf.plot(ax=plt.gca(), color='red', markersize=10, label="公車站點")

        # 設定圖表標題和圖例
        plt.title("北北基桃地圖與承德幹線站點", fontsize=16)
        plt.legend(title='圖例', fontsize=10)

        # 顯示圖表
        plt.tight_layout()
        plt.show()

except FileNotFoundError as e:
    print(f"錯誤：找不到檔案 - {e}")
except Exception as e:
    print(f"發生錯誤：{e}")