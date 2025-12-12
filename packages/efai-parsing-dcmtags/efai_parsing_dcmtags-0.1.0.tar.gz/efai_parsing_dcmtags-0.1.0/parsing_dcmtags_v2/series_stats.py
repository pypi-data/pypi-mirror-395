import pandas as pd
import numpy as np
import pydicom

def convert_multivalue_and_sequence_to_string(value):
    # 將 pydicom 的 MultiValue 或 Sequence 轉成字串
    if isinstance(value, (pydicom.multival.MultiValue, pydicom.sequence.Sequence)):
        return str(value)
    return value

def extract_first_if_array(x):
    # 取 numpy array 或 list 的第一個值，其他安全處理
    if isinstance(x, np.ndarray):
        return x[0] if x.size > 0 else None
    elif pd.isna(x):
        return None
    else:
        return x

def aggregate_series_level(df_dcm, df_file_list=None):
    # 將 Instance-Level DataFrame 聚合成 Series-Level。 若 df_file_list 提供，確保 Batch 欄位存在。
    # 確保 Batch 欄位存在
    if 'Batch' not in df_dcm.columns and df_file_list is not None and 'Batch' in df_file_list.columns:
        df_dcm = pd.merge(df_dcm, df_file_list[['Dcm_Path', 'Batch']], on='Dcm_Path', how='left')

    # 記錄 Series -> Batch 映射
    batch_map = None
    if "Batch" in df_dcm.columns:
        batch_map = df_dcm.groupby("SeriesInstanceUID")["Batch"].first().reset_index()

    # 計算 SliceCount
    df_slicecount = df_dcm.groupby('SeriesInstanceUID')['SeriesInstanceUID']\
                          .count().reset_index(name='SliceCount')

    # 複製資料避免改原本 df
    df_slt = df_dcm.copy()

    # 將 multivalue/sequence 轉成字串
    for col in df_slt.columns:
        df_slt[col] = df_slt[col].apply(convert_multivalue_and_sequence_to_string)

    # 聚合 unique tags (排除 Batch) 這裡要調整
    unique_cols = [c for c in df_slt.columns if c not in ['SeriesInstanceUID', 'Batch']]
    df_slt_series = df_slt.groupby('SeriesInstanceUID')[unique_cols].agg(['unique']).reset_index()

    # 取消多層欄位
    df_slt_series.columns = df_slt_series.columns.get_level_values(0)

    # 合併 SliceCount
    df_slt_series = pd.merge(df_slt_series, df_slicecount, how='left', on='SeriesInstanceUID')

    # 合併 Batch
    if batch_map is not None:
        df_slt_series = pd.merge(df_slt_series, batch_map, on='SeriesInstanceUID', how='left')

    # 取第一個值
    columns_to_clean = ["PatientID", "AccessionNumber", "StudyInstanceUID",
                        "SeriesInstanceUID", "Batch", "Dcm_Path_Series"]
    for col in columns_to_clean:
        if col in df_slt_series.columns:
            df_slt_series[col] = df_slt_series[col].apply(extract_first_if_array)

    # 欄位排序
    columns_to_front = ["PatientID", "AccessionNumber", "StudyInstanceUID",
                        "SeriesInstanceUID", "Batch", "Dcm_Path_Series", "SliceCount", "SOPInstanceUID", "Dcm_Path"]
    df_slt_series = df_slt_series[[c for c in columns_to_front if c in df_slt_series.columns] +
                                  [c for c in df_slt_series.columns if c not in columns_to_front]]

    return df_slt_series
