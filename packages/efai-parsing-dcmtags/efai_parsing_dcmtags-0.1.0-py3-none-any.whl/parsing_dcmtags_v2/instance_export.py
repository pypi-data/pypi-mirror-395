import pandas as pd
from pathlib import Path
from .hierarchy_stats import compute_hierarchy_stats

def export_final_excel(all_batches, df_file_list, FOLDER_NAME, DATE_STR, output_dir="./output", max_rows_per_file=1000000):
    # 整理欄位順序並匯出 EXCEL，檔名包含層級統計
    df_file_list['Dcm_Path'] = df_file_list['Dcm_Path'].astype(str)
    all_batches['Dcm_Path'] = all_batches['Dcm_Path'].astype(str)
    
    # 內部 merge
    all_batches = pd.merge(all_batches, df_file_list, on='Dcm_Path', how='inner')

    # 欄位排序
    columns_to_front = ["PatientID", "AccessionNumber", "StudyInstanceUID",
                        "SeriesInstanceUID", "SOPInstanceUID", "Batch",
                        "Dcm_Path_Series", "Dcm_Path"]
    all_batches = all_batches[columns_to_front + [col for col in all_batches.columns if col not in columns_to_front]]
    
    all_batches_soplist = all_batches[["PatientID", "AccessionNumber", "StudyInstanceUID", "SeriesInstanceUID", "SOPInstanceUID", "Batch", "Dcm_Path"]]

    # 計算層級統計
    stats = compute_hierarchy_stats(all_batches)

    # 組合檔名
    out_name = f"{FOLDER_NAME}_DcmTags_InstanceLevel_{stats[0]}pid_" \
               f"{stats[2]}st_{stats[3]}se_{stats[5]}ins-{DATE_STR}.xlsx"
    out_path = Path(output_dir) / out_name

    # 匯出 EXCEL
    all_batches.to_excel(out_path, index=False)
    print(f"[完成] 已匯出 Excel：{out_path}")
    return out_path

def export_final_excel_split(
    all_batches,
    df_file_list,
    FOLDER_NAME,
    DATE_STR,
    output_dir="./output",
    chunk_size=500     # 每 500 個 PatientID 一份
):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # 確保 Dcm_Path 可 merge
    df_file_list['Dcm_Path'] = df_file_list['Dcm_Path'].astype(str)
    all_batches['Dcm_Path'] = all_batches['Dcm_Path'].astype(str)

    # merge instance df
    all_batches = pd.merge(all_batches, df_file_list, on='Dcm_Path', how='inner')

    # 欄位排序
    columns_to_front = [
        "PatientID", "AccessionNumber", "StudyInstanceUID",
        "SeriesInstanceUID", "SOPInstanceUID", "Batch",
        "Dcm_Path_Series", "Dcm_Path"
    ]
    all_batches = all_batches[
        columns_to_front + [col for col in all_batches.columns if col not in columns_to_front]
    ]

    # 統計層級數量 (只統一計算一次即可)
    stats = compute_hierarchy_stats(all_batches)

    # 取得所有 unique PatientID
    unique_pids = sorted(all_batches["PatientID"].astype(str).unique())

    output_paths = []

    # ---- 分段輸出 ----
    part = 1
    for i in range(0, len(unique_pids), chunk_size):
        pid_chunk = unique_pids[i:i + chunk_size]

        df_chunk = all_batches[
            all_batches["PatientID"].astype(str).isin(pid_chunk)
        ]
        
        # 加入你指定的 patient index 範圍
        start_id = i
        end_id = min(i + chunk_size, len(unique_pids))

        out_name = (
            f"{FOLDER_NAME}_DcmTags_InstanceLevel_{start_id}to{end_id}pid-{DATE_STR}.xlsx"
        )
        out_path = Path(output_dir) / out_name

        df_chunk.to_excel(out_path, index=False, engine="openpyxl")

        print(f"[完成] 已輸出: {out_name}, 共 {len(df_chunk)} 筆資料")

        output_paths.append(out_path)
        part += 1

    return output_paths