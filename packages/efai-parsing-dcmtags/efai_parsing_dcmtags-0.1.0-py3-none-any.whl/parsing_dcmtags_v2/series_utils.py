import pandas as pd
import numpy as np
import pydicom

def convert_multivalue_and_sequence_to_string(value):
    if isinstance(value, (pydicom.multival.MultiValue, pydicom.sequence.Sequence)):
        return str(value)
    return value

def clean_multivalue_columns(df: pd.DataFrame) -> pd.DataFrame:
    # 將所有 MultiValue/Sequence 轉為字串
    for col in df.columns:
        df[col] = df[col].apply(convert_multivalue_and_sequence_to_string)
    return df

def extract_first_if_array(x):
    if isinstance(x, np.ndarray):
        return x[0] if x.size > 0 else None
    elif pd.isna(x):
        return None
    else:
        return x

def clean_specific_columns(df: pd.DataFrame, columns_to_clean: list) -> pd.DataFrame:
    # 針對特定欄位做 ndarray/NaN 清理
    for col in columns_to_clean:
        df[col] = df[col].apply(extract_first_if_array)
    return df

def move_columns_to_front(df: pd.DataFrame, columns_to_front: list) -> pd.DataFrame:
    # 把特定欄位移到最前面
    return df[columns_to_front + [col for col in df.columns if col not in columns_to_front]]
