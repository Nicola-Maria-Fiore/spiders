import os
import csv
import pandas as pd
from openpyxl import load_workbook
import shutil

def xlsToCsv():
    #TO_CSV
    to_csv=dict(sep=',', na_rep='.', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding="utf-8-sig", compression='infer', quoting=csv.QUOTE_ALL, quotechar='"', line_terminator='\r\n', chunksize=10000, date_format=None, doublequote=True, escapechar='\\', decimal='.', errors='strict', storage_options=None)
    #READ_CSV
    read_csv=dict(sep=',', delimiter=None, header='infer', names=None, index_col=None, usecols=None, squeeze=False, prefix=None, mangle_dupe_cols=True, dtype=str, engine=None, converters=None, true_values=None, false_values=None, skipinitialspace=False, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False, skip_blank_lines=True, parse_dates=False, infer_datetime_format=False, keep_date_col=False, date_parser=None, dayfirst=False, cache_dates=True, iterator=False, chunksize=None, compression='infer', thousands=None, decimal='.', lineterminator=None, quotechar='"', quoting=csv.QUOTE_ALL, doublequote=True, escapechar='\\', comment=None, encoding=None, dialect=None, error_bad_lines=True, warn_bad_lines=True, delim_whitespace=False, low_memory=True, memory_map=False, float_precision=None, storage_options=None)
    #READ_EXCEL
    read_excel=dict(sheet_name=0, header=0, names=None, index_col=None, usecols=None, squeeze=False, dtype=None, engine=None, converters=None, true_values=None, false_values=None, skiprows=None, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False, parse_dates=False, date_parser=None, thousands=None, comment=None, skipfooter=0, convert_float=True, mangle_dupe_cols=True, storage_options=None)

    path_resources = "resources/"
    path_results = "resources/"

    dirs=os.listdir(path_resources)
    for i, file in enumerate(dirs):
        if file.endswith(".xlsx") == False:
            continue
        #LOAD WORKBOOK
        wb=load_workbook(path_resources+file)
        ws=wb['Company Overview']
        ws.delete_rows(1, 4)
        ws.delete_rows(2, 1)
        #DATAFRAME
        from itertools import islice
        data = ws.values
        cols = next(data)[1:]   
        data = list(data)
        idx = [r[0] for r in data]
        data = (islice(r, 1, None) for r in data)
        df = pd.DataFrame(data, index=idx, columns=cols)
        df=df.rename_axis("Symbol")
        df=df.reset_index()
        df=df.rename_axis("index")
        df.columns = [*df.columns[:-1], 'date']
        #FILE_NAME
        s=file.replace(".xlsx", ".csv")
        s_list=list(s)
        s_list.insert(4, "-")
        s_list.insert(6+1, "-")
        file_name=''.join(s_list)
        #TO_CSV
        file_path=path_results+file_name
        df.to_csv(file_path, **to_csv)
        os.remove(path_resources+file)
