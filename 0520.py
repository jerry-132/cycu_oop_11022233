import pandas as pd

# 定義不及格的分數
FAIL_SCORE = 60

# 讀取 CSV 檔案
df = pd.read_csv('midterm_scores.csv')

# 過濾出只有科目成績的部分（排除 Name 和 StudentID）
scores_df = df.iloc[:, 2:]

# 計算每位學生不及格科目的數量
fail_counts = (scores_df < FAIL_SCORE).sum(axis=1)

# 找出不及格科目超過一半的學生
students_with_many_fails = df[fail_counts > (scores_df.shape[1] / 2)]

# 顯示結果
print("有一半以上科目不及格的學生及其成績：")
print(students_with_many_fails)

# 將結果儲存為 CSV 檔案
output_file = 'students_with_many_fails.csv'
students_with_many_fails.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"結果已儲存至 {output_file}")