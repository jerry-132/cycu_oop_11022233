import pandas as pd

# 讀取原始 CSV 檔案
input_file = "taipei_bus_stop_names.csv"
output_file = "taipei_bus_stop_names_unique.csv"

# 讀取 CSV 檔案
df = pd.read_csv(input_file)

# 打印欄位名稱以確認
print("欄位名稱：", df.columns)

# 去除重複的公車代碼，只保留第一個出現的
df_unique = df.drop_duplicates(subset=["公車代碼"])

# 將結果存成新的 CSV 檔案
df_unique.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"已成功處理並儲存為新的檔案：{output_file}")