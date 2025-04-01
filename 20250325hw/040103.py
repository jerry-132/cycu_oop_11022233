from playwright.sync_api import sync_playwright

def save_rendered_html(url, output_file):
    """
    使用 Playwright 渲染網頁並儲存為 HTML 檔案
    :param url: 要渲染的網頁 URL
    :param output_file: 儲存的 HTML 檔案名稱
    """
    with sync_playwright() as p:
        # 啟動瀏覽器
        browser = p.chromium.launch(headless=True)  # headless=True 表示無頭模式
        page = browser.new_page()

        # 開啟目標 URL
        page.goto(url)

        # 等待網頁完全加載（可根據需要調整等待條件）
        page.wait_for_load_state("networkidle")

        # 獲取渲染後的 HTML
        content = page.content()

        # 將 HTML 儲存到檔案
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"已成功將渲染後的網頁儲存為 {output_file}")

        # 關閉瀏覽器
        browser.close()

# 主程式
if __name__ == "__main__":
    # 測試用的 URL（請替換為實際的目標網址）
    url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

    # 輸出的 HTML 檔案名稱
    output_file = "rendered_page.html"

    # 呼叫函數
    save_rendered_html(url, output_file)