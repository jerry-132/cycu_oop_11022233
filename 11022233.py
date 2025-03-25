import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import rcParams
# 讀取 CSV 檔案，指定編碼格式
file_path = r'c:\Users\User\Documents\GitHub\cycu_oop_11022233\ExchangeRate@202503251851.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# 檢查欄位名稱
print(df.columns)

# 手動選擇正確的欄位名稱
df.columns = ['資料日期', '幣別', '匯率', '現金', '即期', '遠期10天', '遠期30天', '遠期60天', '遠期90天', '遠期120天', '遠期150天', '遠期180天', '匯率.1', '現金.1', '即期.1', '遠期10天.1', '遠期30天.1', '遠期60天.1', '遠期90天.1', '遠期120天.1', '遠期150天.1', '遠期180天.1']

# 選擇需要的欄位
df = df[['資料日期', '現金', '現金.1']]

# 將資料日期轉換為日期格式
df['資料日期'] = pd.to_datetime(df['資料日期'], format='%Y%m%d')

# 繪製線圖
plt.figure(figsize=(10, 6))
plt.plot(df['資料日期'], df['現金'], label='本行買入')
plt.plot(df['資料日期'], df['現金.1'], label='本行賣出')

# 設定圖表標題和標籤
plt.title('買入賣出匯率')
plt.xlabel('日期')
plt.ylabel('匯率')
plt.legend()

# 顯示圖表
plt.show()