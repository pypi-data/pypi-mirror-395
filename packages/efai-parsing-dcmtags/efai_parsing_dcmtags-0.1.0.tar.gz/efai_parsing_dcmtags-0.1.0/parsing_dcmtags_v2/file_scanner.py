import pandas as pd
from pathlib import Path
from tqdm import tqdm
import os

def scan_files(paths_and_patterns, ROOT_MARKER=None, file_format="dcm"):
    list_column_name = file_format[0].upper() + file_format[1:]
    file_records = []
    ext = "." + file_format.lower()

    for base_path, pattern, batch_name in paths_and_patterns:
        for root, dirs, files in tqdm(os.walk(base_path), desc=f"Scanning {base_path.name}"):
            for f in files:
                if f.lower().endswith(ext):
                    full_path = Path(root) / f
                    file_records.append({'Path': str(full_path), 'Batch': batch_name})

    df_file_list = pd.DataFrame(file_records)
    if "Path" not in df_file_list.columns:
        raise ValueError("掃描結果沒有Path欄位")
    df_file_list.rename(columns={'Path': f'{list_column_name}_Path'}, inplace=True)
    return df_file_list
