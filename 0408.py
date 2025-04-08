import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

def plot_lognormal_cdf(mu, sigma, output_filename='lognormal_cdf.jpg'):
    """
    繪製對數常態累積分布函數 (CDF) 並儲存為 JPG 檔案
    :param mu: 對數常態分布的均值
    :param sigma: 對數常態分布的標準差
    :param output_filename: 輸出的 JPG 檔案名稱
    """
    # 計算對數常態分布的參數
    s = sigma
    scale = np.exp(mu)

    # 定義 x 軸範圍
    x = np.linspace(0.01, 10, 1000)

    # 計算累積分布函數 (CDF)
    cdf = lognorm.cdf(x, s, scale=scale)

    # 繪製圖形
    plt.figure(figsize=(8, 6))
    plt.plot(x, cdf, label='Lognormal CDF', color='blue')
    plt.title('Lognormal Cumulative Distribution Function')
    plt.xlabel('x')
    plt.ylabel('CDF')
    plt.legend()
    plt.grid()

    # 儲存為 JPG 檔
    plt.savefig(output_filename, format='jpg')
    plt.show()

# 主程式
if __name__ == "__main__":
    # 設定參數
    mu = 1.5
    sigma = 0.4
    plot_lognormal_cdf(mu, sigma)