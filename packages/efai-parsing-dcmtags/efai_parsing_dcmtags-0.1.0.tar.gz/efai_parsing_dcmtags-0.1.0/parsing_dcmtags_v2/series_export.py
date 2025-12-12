import pandas as pd
from pathlib import Path
from .hierarchy_stats import compute_hierarchy_stats
from datetime import datetime
import ast
import os

def export_series_excel(
    df_dcm_slt_Series_merge_SC,
    FOLDER_NAME,
    DATE_STR,
    instance_df=None,
    output_dir="./output"
):
   # 如果提供了 instance-level 的 df，就計算 ImagePositionPatient_z_diff
    if instance_df is not None:
        if 'ImagePositionPatient' in instance_df.columns:
            # 安全解析：將字串轉為 list，防止格式錯誤導致程式中止
            def safe_parse(x):
                if isinstance(x, str):
                    try:
                        val = ast.literal_eval(x)
                        if isinstance(val, (list, tuple)) and len(val) >= 3:
                            return val
                        else:
                            return None
                    except Exception:
                        return None
                elif isinstance(x, (list, tuple)) and len(x) >= 3:
                    return x
                else:
                    return None

            instance_df['ImagePositionPatient'] = instance_df['ImagePositionPatient'].apply(safe_parse)

            # 計算每個 SeriesInstanceUID 的 z 差 unique
            z_diff_unique = (
                instance_df
                .sort_values(['SeriesInstanceUID', 'InstanceNumber'])
                .groupby('SeriesInstanceUID')['ImagePositionPatient']
                .apply(lambda x: list(
                    set(
                        [
                            x.iloc[i+1][2] - x.iloc[i][2]
                            for i in range(len(x) - 1)
                            if isinstance(x.iloc[i], (list, tuple))
                            and isinstance(x.iloc[i+1], (list, tuple))
                            and len(x.iloc[i]) >= 3
                            and len(x.iloc[i+1]) >= 3
                        ]
                    )
                ))
            )

            # 把 z_diff_unique 根據 SeriesInstanceUID 對應回每一列
            df_dcm_slt_Series_merge_SC['ImagePositionPatient_z_diff'] = (
                df_dcm_slt_Series_merge_SC['SeriesInstanceUID'].map(z_diff_unique)
            )

            # 顯示略過的筆數（非 list 或格式錯誤）
            skipped = instance_df['ImagePositionPatient'].isna().sum()
            print(f"[Info] 跳過 {skipped} 筆無效的 ImagePositionPatient 資料。")

        else:
            # 沒有這個欄位，跳過計算並給空值
            print("Warning: 'ImagePositionPatient' not found in instance_df — skipping z-diff calculation.")
            df_dcm_slt_Series_merge_SC['ImagePositionPatient_z_diff'] = None
    
    # 計算各層級數量
    n_pid, n_an, n_st, n_se, n_srs, n_ins = compute_hierarchy_stats(df_dcm_slt_Series_merge_SC)

    # 組合檔名
    out_series_name = f"{FOLDER_NAME}_DcmTags_SeriesLevel_AllInOne_{n_pid}pid_{n_st}st_{n_se}se-{DATE_STR}.xlsx"
    out_series_path = Path(output_dir) / out_series_name

    # 匯出 Excel
    df_dcm_slt_Series_merge_SC.to_excel(out_series_path, index=False)

    print(f"[完成] 已匯出 Series-Level Excel：{out_series_path}")
    return out_series_path

def export_split_series_excel(
    df_dcm_slt_Series_merge_SC,
    FOLDER_NAME,
    DATE_STR,
    instance_df=None,
    output_dir="./output",
    chunk_size=500  # 每500個PatientID一組
):

    os.makedirs(output_dir, exist_ok=True)

    # 如果提供 instance-level df，就計算 ImagePositionPatient_z_diff
    if instance_df is not None:
        if 'ImagePositionPatient' in instance_df.columns:
            # 安全解析
            def safe_parse(x):
                if isinstance(x, str):
                    try:
                        val = ast.literal_eval(x)
                        if isinstance(val, (list, tuple)) and len(val) >= 3:
                            return val
                        else:
                            return None
                    except Exception:
                        return None
                elif isinstance(x, (list, tuple)) and len(x) >= 3:
                    return x
                else:
                    return None

            instance_df['ImagePositionPatient'] = instance_df['ImagePositionPatient'].apply(safe_parse)

            # 計算每個 SeriesInstanceUID 的 z 差 unique（加上安全檢查）
            z_diff_unique = (
                instance_df
                .sort_values(['SeriesInstanceUID', 'InstanceNumber'])
                .groupby('SeriesInstanceUID')['ImagePositionPatient']
                .apply(lambda x: list(
                    set(
                        [
                            x.iloc[i+1][2] - x.iloc[i][2]
                            for i in range(len(x) - 1)
                            if isinstance(x.iloc[i], (list, tuple))
                            and isinstance(x.iloc[i+1], (list, tuple))
                            and len(x.iloc[i]) >= 3
                            and len(x.iloc[i+1]) >= 3
                        ]
                    )
                ))
            )

            df_dcm_slt_Series_merge_SC['ImagePositionPatient_z_diff'] = (
                df_dcm_slt_Series_merge_SC['SeriesInstanceUID'].map(z_diff_unique)
            )

            skipped = instance_df['ImagePositionPatient'].isna().sum()
            print(f"[Info] 跳過 {skipped} 筆無效的 ImagePositionPatient 資料。")

        else:
            print("Warning: 'ImagePositionPatient' not found in instance_df — skipping z-diff calculation.")
            df_dcm_slt_Series_merge_SC['ImagePositionPatient_z_diff'] = None

    # 取得唯一 PatientID 並排序
    unique_pids = sorted(df_dcm_slt_Series_merge_SC["PatientID"].astype(str).unique())

    output_paths = []

    # 分批處理
    for i in range(0, len(unique_pids), chunk_size):
        pid_chunk = unique_pids[i:i + chunk_size]
        df_chunk = df_dcm_slt_Series_merge_SC[
            df_dcm_slt_Series_merge_SC["PatientID"].astype(str).isin(pid_chunk)
        ]

        start_id = i
        end_id = min(i + chunk_size, len(unique_pids))

        # 組合檔名
        out_name = f"{FOLDER_NAME}_DcmTags_SeriesLevel_{start_id}to{end_id}pid-{DATE_STR}.xlsx"
        out_path = Path(output_dir) / out_name

        # 匯出 Excel
        df_chunk.to_excel(out_path, index=False, engine="openpyxl")
        print(f"[完成] 已輸出: {out_name}, 共 {len(df_chunk)} 筆資料")

        output_paths.append(out_path)

    return output_paths