import re
import gc
import pandas as pd
import pydicom
from multiprocessing import Pool, cpu_count
from pathlib import Path
from tqdm import tqdm
import math

def _safe_to_str(v):
    try:
        return str(v)
    except Exception:
        return None

def extract_tags_single(dcm_path: str):
    try:
        dcm = pydicom.read_file(dcm_path, stop_before_pixels=True, force=True)

        p = Path(dcm_path)
        tags = {
            "Dcm_Path": str(p),
            "Dcm_Path_Series": str(p.parent),
        }

        modality = str(dcm.get("Modality", ""))

        if modality == "RTSTRUCT":
            # 非序列欄位
            for elem in dcm:
                try:
                    if getattr(elem, "VR", None) == "SQ":
                        continue
                    key = elem.keyword if elem.keyword else str(elem.tag)
                    tags[key] = _safe_to_str(elem.value)
                except Exception:
                    pass

            # 先掃 ROIContourSequence：彙整 ref ROINumber 是否有任何 ContourSequence>0
            refnum_has_contour = {}
            roi_contour_seq = getattr(dcm, "ROIContourSequence", None)  # (3006,0039)
            if roi_contour_seq is not None:
                for contour_item in roi_contour_seq:
                    try:
                        ref_num = getattr(contour_item, "ReferencedROINumber", None)  # (3006,0084)
                        if ref_num is None:
                            continue
                        contour_seq = getattr(contour_item, "ContourSequence", None)   # (3006,0040)
                        has_contour = 1 if (contour_seq is not None and len(contour_seq) > 0) else 0
                        # 只要任一相同 ROINumber 有 1，就記 1
                        if has_contour == 1:
                            refnum_has_contour[ref_num] = 1
                        else:
                            refnum_has_contour.setdefault(ref_num, 0)
                    except Exception:
                        continue

            # 根據 StructureSetROISequence 產生 ROI_Dict：key=ROIName, value=1/0（同名取最大值）
            roi_dict = {}
            struct_seq = getattr(dcm, "StructureSetROISequence", None)  # (3006,0020)
            if struct_seq is not None:
                for roi_item in struct_seq:
                    try:
                        roi_number = getattr(roi_item, "ROINumber", None)  # (3006,0022)
                        roi_name = getattr(roi_item, "ROIName", None)
                        roi_name = str(roi_name).strip() if roi_name is not None else ""
                        if roi_name == "":
                            roi_name = f"ROI_{roi_number}"

                        value = int(refnum_has_contour.get(roi_number, 0))
                        # 同名 ROIName：任一為 1 則填 1
                        roi_dict[roi_name] = max(roi_dict.get(roi_name, 0), value)
                    except Exception:
                        continue

            tags["ROI_Dict"] = roi_dict

        else:
            # 非 RS：全按原本方式讀
            tags_dir = dcm.dir()
            for tag_name in tags_dir:
                try:
                    tags[tag_name] = _safe_to_str(dcm.get(tag_name, None))
                except Exception:
                    pass

        return tags

    except Exception as e:
        return {"__error__": str(e), "Dcm_Path": dcm_path}

def extract_tags_parallel(paths, num_workers=None):
    # 平行處理多個 DICOM 檔案
    num_workers = num_workers or cpu_count()
    rows = []
    with Pool(processes=num_workers) as pool:
        for result in tqdm(pool.imap_unordered(extract_tags_single, paths), total=len(paths)):
            rows.append(result)
    return pd.DataFrame(rows)

def extract_dcmtags(
    df_file_list,
    ROOT_MARKER=None,
    BATCH_SIZE=None,
    NUM_WORKERS=None,
    OUTPUT_DIR="./output/temp",
    DATE_STR=None,
    FOLDER_NAME=None,
    EXCEL_MAX_ROWS=1_000_000
):
    
    OUTPUT_DIR = Path(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 正規化路徑
    df_files = df_file_list.copy()
    s = (df_files["Dcm_Path"]
            .astype(str)
            .str.strip()
            .str.replace('\\', '/', regex=False))
    # 更健壯的 regex：允許前後是 / 或 \，夾出 ROOT_MARKER 下一層目錄名
    pattern = re.compile(rf"[\\/]{re.escape(ROOT_MARKER)}[\\/]+([^\\/]+)[\\/]")
    
    # 直接抽成一個 Series
    bucket_x = s.str.extract(pattern, expand=False) # 取出 x；加 expand=False 直接拿到 Series（不是一欄名為 0 的 DF）
    df_files["bucket_x"] = bucket_x # 存回去

    missing = df_files["bucket_x"].isna().sum()
    if missing > 0:
        print(f"[警告] 有 {missing} 筆路徑未能解析出 x，將被排除。")
        df_files = df_files[df_files["bucket_x"].notna()].copy()

    unique_x = sorted(df_files["bucket_x"].unique())
    batches = [unique_x[i:i+BATCH_SIZE] for i in range(0, len(unique_x), BATCH_SIZE)]
    print(f"共 {len(unique_x)} 個 x，將分成 {len(batches)} 批（每批 {BATCH_SIZE} 個）")

    # 分批處理
    for bi, x_list in enumerate(batches, start=1):
        out_path = OUTPUT_DIR / f"{FOLDER_NAME}_DcmTags_InstanceLevel_{bi}-{DATE_STR}.xlsx"

        if out_path.exists():
            print(f"[略過] 第 {bi} 批輸出已存在：{out_path}")
            continue

        df_paths_batch = df_files.loc[df_files["bucket_x"].isin(x_list), "Dcm_Path"].tolist()
        print(f"\n=== 處理第 {bi} 批：{len(x_list)} 個 x，{len(df_paths_batch):,} 個 DICOM 檔 ===")

        # 讀取本批所有 DICOM tags
        df_dcm_batch = extract_tags_parallel(df_paths_batch, num_workers=NUM_WORKERS)
        
        # 存成 Excel（若超過單表上限，切成多工作表 part1/part2/...）
        if len(df_dcm_batch) == 0:
            print(f"[提醒] 第 {bi} 批沒有資料，略過存檔。")
        else:
            n_parts = math.ceil(len(df_dcm_batch) / EXCEL_MAX_ROWS)
            with pd.ExcelWriter(out_path, engine="xlsxwriter") as writer:
                for pi in range(n_parts):
                    start = pi * EXCEL_MAX_ROWS
                    end = min((pi + 1) * EXCEL_MAX_ROWS, len(df_dcm_batch))
                    sheet_name = f"part{pi+1}" if n_parts > 1 else "data"
                    df_dcm_batch.iloc[start:end].to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"[完成] 已儲存：{out_path}（{len(df_dcm_batch):,} 列，工作表數：{n_parts}）")
        
        # 釋放記憶體
        del df_dcm_batch
        gc.collect()

    print("\n全部批次處理完成。輸出目錄：", OUTPUT_DIR)
