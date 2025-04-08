import sys
import io
from datetime import datetime

# 設定標準輸出為 UTF-8，防止亂碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 定義英文星期與中文星期的對應表
weekday_map = {
    "Monday": "星期一",
    "Tuesday": "星期二",
    "Wednesday": "星期三",
    "Thursday": "星期四",
    "Friday": "星期五",
    "Saturday": "星期六",
    "Sunday": "星期日"
}

def calculate_julian_date(input_time_str):
    """
    計算輸入時間的星期幾與經過的太陽日數
    :param input_time_str: 時間字串，格式為 'YYYY-MM-DD HH:MM'
    :return: 星期幾、經過的太陽日數、輸入時間的 Julian Date、現在的 Julian Date
    """
    # 將輸入的時間字串轉換為 datetime 物件
    input_time = datetime.strptime(input_time_str, '%Y-%m-%d %H:%M')
    
    # 計算該天是星期幾
    weekday = input_time.strftime('%A')  # 取得星期幾 (英文)
    weekday = weekday_map[weekday]  # 將英文星期轉換為中文星期
    
    # 計算輸入時間的 Julian Date
    julian_date_input = input_time.toordinal() + 1721424.5 + (input_time.hour / 24) + (input_time.minute / 1440)
    
    # 取得現在的時間
    now = datetime.now()
    
    # 計算現在的 Julian Date
    julian_date_now = now.toordinal() + 1721424.5 + (now.hour / 24) + (now.minute / 1440)
    
    # 計算經過的太陽日數
    elapsed_days = julian_date_now - julian_date_input
    
    return weekday, elapsed_days, julian_date_input, julian_date_now

# 主程式
if __name__ == "__main__":
    # 提示使用者輸入日期
    input_time = input("請輸入日期和時間 (格式為 YYYY-MM-DD HH:MM，例如 2020-04-15 20:30)：")
    try:
        weekday, elapsed_days, julian_date_input, julian_date_now = calculate_julian_date(input_time)
        print(f"輸入的時間是星期：{weekday}")
        print(f"從輸入時間至今經過的太陽日數：{elapsed_days:.6f}")
        print(f"輸入時間的 Julian Date：{julian_date_input}")
        print(f"現在的 Julian Date：{julian_date_now}")
    except ValueError:
        print("輸入的日期格式不正確，請使用 YYYY-MM-DD HH:MM 格式。")