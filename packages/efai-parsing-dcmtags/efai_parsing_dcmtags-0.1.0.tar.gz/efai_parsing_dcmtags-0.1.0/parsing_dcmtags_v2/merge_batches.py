import pandas as pd
from pathlib import Path
import glob
from datetime import datetime
from tqdm import tqdm  # 加入進度條

def merge_temp_batches(
    FOLDER_NAME=None, 
    DATE_STR=None, 
    temp_dir="./output/temp"):
    # 設定預設值
    FOLDER_NAME = FOLDER_NAME or "DefaultFolder"
    DATE_STR = DATE_STR or datetime.now().strftime("%Y%m%d")
    # 所有temp batches讀入並合併
    dfs = []
    # pattern 只包含當日的 DATE_STR
    pattern = f"{temp_dir}/{FOLDER_NAME}_DcmTags_InstanceLevel_*-{DATE_STR}.xlsx"
    file_paths = sorted(glob.glob(pattern))
    
    print(f"找到 {len(file_paths)} 個檔案：")
    for p in file_paths:
        print(" -", p)
    # 逐一讀取
    for file_path in tqdm(file_paths, desc="讀取 temp batch Excel"):
        dfs.append(pd.read_excel(file_path))
    
    # 合併成一個大 dataframe
    if dfs:
        all_batches = pd.concat(dfs, ignore_index=True)
        print("合併後資料筆數：", len(all_batches))
        return all_batches
    else:
        print("[提醒] 沒有找到任何資料。")
        return pd.DataFrame()
