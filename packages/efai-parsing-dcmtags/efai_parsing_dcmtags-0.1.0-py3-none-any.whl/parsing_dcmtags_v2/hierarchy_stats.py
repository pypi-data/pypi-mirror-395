def compute_hierarchy_stats(df):
    n_pid = df["PatientID"].astype(str).nunique()
    n_an  = df["AccessionNumber"].astype(str).nunique()
    n_st  = df["StudyInstanceUID"].astype(str).nunique()
    n_se  = df["SeriesInstanceUID"].astype(str).nunique()
    n_srs = df["Dcm_Path_Series"].astype(str).nunique()
    n_ins = len(df)
    return (n_pid, n_an, n_st, n_se, n_srs, n_ins)
