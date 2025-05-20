import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 設定支援中文的字型
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
rcParams['axes.unicode_minus'] = False  # 解決負號無法顯示的問題

# 讀取 Shapefile 檔案
shapefile_path = './COUNTY_MOI_1140318.shp'

try:
    # 嘗試讀取 Shapefile
    gdf = gpd.read_file(shapefile_path, encoding='utf-8')

    # 篩選出台北市、新北市、基隆市和桃園市
    target_cities = ['台北市', '新北市', '基隆市', '桃園市']
    filtered_gdf = gdf[gdf['COUNTYNAME'].isin(target_cities)]

    # 修復多邊形，填充內部空洞
    filtered_gdf['geometry'] = filtered_gdf['geometry'].buffer(0)

    # 繪製地理圖形
    plt.figure(figsize=(12, 10))
    filtered_gdf.plot(ax=plt.gca(), color='lightblue', edgecolor='black')

    # 設定圖表標題
    plt.title('大台北地區與基隆、桃園地圖', fontsize=16)

    # 顯示圖表
    plt.tight_layout()
    plt.show()

except Exception as e:
    # 捕捉錯誤並顯示訊息
    print(f"讀取 Shapefile 時發生錯誤：{e}")
    print("請確認檔案是否完整，並檢查路徑是否正確。")