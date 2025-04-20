import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_normal_distribution(mu, sigma, filename="normal_pdf.jpg"):
    """
    繪製常態分佈的機率密度函數，並儲存為 JPG 圖檔。

    :param mu: 常態分佈的平均值
    :param sigma: 常態分佈的標準差
    :param filename: 儲存的 JPG 檔名 (固定為 'normal_pdf.jpg')
    """
    # 確保檔案名稱固定為 normal_pdf.jpg
    filename = "normal_pdf.jpg"

    # 定義 x 軸範圍
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
    # 計算機率密度函數
    y = norm.pdf(x, mu, sigma)

    # 繪製圖形
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label=f"Mean = {mu}, Std Dev = {sigma}")
    plt.title("Normal Distribution")
    plt.xlabel("X")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid()

    # 儲存為 JPG 圖檔
    plt.savefig(filename, format="jpg")
    plt.close()

    # 提示訊息
    print(f"圖形已儲存為 {filename}")

# 主程式
if __name__ == "__main__":
    try:
        # 讓使用者輸入 mu 和 sigma
        mu = float(input("請輸入常態分佈的平均值 (mu)："))
        sigma = float(input("請輸入常態分佈的標準差 (sigma)："))

        # 呼叫函數繪製圖形，檔名固定為 normal_pdf.jpg
        plot_normal_distribution(mu, sigma)
    except ValueError:
        print("輸入的值無效，請輸入數字！")