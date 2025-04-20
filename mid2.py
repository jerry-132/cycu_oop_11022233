from datetime import datetime

def calculate_elapsed_days_and_date_info():
    """
    讓使用者輸入時間字串，計算從該時間到現在共經歷了幾個太陽日，
    並顯示該日期是星期幾以及當年的第幾天。

    :return: 包含經過的太陽日數、星期幾和當年第幾天的資訊
    """
    try:
        # 提示使用者輸入時間字串
        time_string = input("請輸入時間 (格式為 YYYY-MM-DD HH:MM): ")
        
        # 解析輸入的時間字串
        input_time = datetime.strptime(time_string, "%Y-%m-%d %H:%M")
        
        # 計算從該時刻到現在經過的太陽日數
        now = datetime.now()
        elapsed_days = (now - input_time).total_seconds() / (24 * 3600)  # 轉換為天數
        
        # 獲取星期幾
        weekday = input_time.strftime("%A")  # 例如: Monday, Tuesday
        
        # 獲取當年第幾天
        day_of_year = input_time.timetuple().tm_yday
        
        # 顯示結果
        print(f"輸入的日期為星期: {weekday}")
        print(f"該日期為當年的第 {day_of_year} 天")
        print(f"從 {time_string} 到現在共經歷了 {elapsed_days:.2f} 太陽日")
        
        return {
            "elapsed_days": elapsed_days,
            "weekday": weekday,
            "day_of_year": day_of_year
        }
    except ValueError as e:
        print(f"時間格式錯誤: {e}")
        return None

# 呼叫函數
calculate_elapsed_days_and_date_info()