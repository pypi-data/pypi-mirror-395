from pathlib import Path

# 預設輸出資料夾
OUTPUT_DIR = Path("./output/temp")

# 每批處理數量
BATCH_SIZE = 200

# Excel 寫入設定
EXCEL_ENGINE = "xlsxwriter"
EXCEL_OPTIONS = {"strings_to_urls": False}
