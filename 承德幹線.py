import pandas as pd
import matplotlib.pyplot as plt

# Main program
if __name__ == "__main__":
    # CSV 檔案名稱
    csv_file = "0161000900.csv"  # 確保檔案名稱正確，且位於相同目錄

    try:
        # 讀取 CSV 檔案
        df = pd.read_csv(csv_file, header=None, names=["到達時間", "車站序號", "車站名稱", "車站編號", "緯度", "經度"])

        # 檢查是否成功讀取資料
        if df.empty:
            print("CSV 檔案為空或無法讀取。")
        else:
            print(f"成功讀取 {len(df)} 筆公車站點資料。")

            # 繪製地圖
            fig, ax = plt.subplots(figsize=(10, 10))
            scatter = ax.scatter(df["經度"], df["緯度"], c='blue', alpha=0.7, label='Bus Stops')

            # 設定地圖標題與標籤
            ax.set_title("Bus Stops Map", fontsize=16)
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.grid(True)
            plt.legend()

            # 顯示地圖
            plt.show()

    except FileNotFoundError:
        print(f"錯誤：找不到檔案 '{csv_file}'，請確認檔案是否存在於程式目錄中。")
    except Exception as e:
        print(f"發生錯誤：{e}")