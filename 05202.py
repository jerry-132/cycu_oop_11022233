import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
from matplotlib.cm import rainbow

# 設定支援中文的字型
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
rcParams['axes.unicode_minus'] = False  # 解決負號無法顯示的問題

# 讀取 CSV 檔案
df = pd.read_csv('midterm_scores.csv')

# 過濾出科目成績的部分（排除 Name 和 StudentID）
scores_df = df.iloc[:, 2:]

# 計算每個科目成績的分布（分數範圍為 0-100，間隔為 10）
bins = range(0, 101, 10)
subject_distributions = {subject: np.histogram(scores_df[subject], bins=bins)[0] for subject in scores_df.columns}

# 設定彩虹色
colors = rainbow(np.linspace(0, 1, len(scores_df.columns)))

# 繪製長條圖
x = np.arange(len(bins) - 1)  # x 軸位置
bar_width = 0.1  # 每個長條的寬度

plt.figure(figsize=(12, 6))
for i, (subject, distribution) in enumerate(subject_distributions.items()):
    plt.bar(x + i * bar_width, distribution, width=bar_width, label=subject, color=colors[i])

# 設定圖表標題與軸標籤
plt.title('成績分布長條圖', fontsize=16)
plt.xlabel('成績範圍', fontsize=12)
plt.ylabel('人數', fontsize=12)
plt.xticks(x + bar_width * (len(scores_df.columns) - 1) / 2, [f'{bins[i]}-{bins[i+1]-1}' for i in range(len(bins) - 1)])

# 顯示圖例
plt.legend(title='科目', fontsize=10)

# 顯示圖表
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()