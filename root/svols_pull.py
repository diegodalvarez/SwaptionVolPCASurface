# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 17:33:01 2023

@author: Diego
"""

import os
import pdblp
import pandas as pd
import datetime as dt

parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
data_dir = os.path.join(parent_dir, "data")
out_dir = os.path.join(parent_dir, "out")
output_file = os.path.join(data_dir, "svols.parquet")

try:
    
    print("[INFO] Reading File from Directory")
    svols_df = pd.read_parquet(
        path  = output_file,
        engine = "pyarrow")
    print("[INFO] File found in directory not requesting from Bloomberg")
    
except:

    print("[ALERT] File not found or loaded, collecting from Bloomberg")
    
    con = pdblp.BCon(debug = False, port = 8194, timeout = 5_000)
    con.start()
    
    EXPIRY_LIST = ["0A", "0C", "01", "02", "05", "10"]
    TENOR_LIST = ["1", "2", "5", "7", "10", "30"]
    flds = ["PX_LAST"]
    
    end_date = dt.date(year = 2023, month = 3, day = 31)
    start_date = dt.date(year = 2020, month = 1, day = 1)
    
    end_date_input  = end_date.strftime("%Y%m%d")
    start_date_input = start_date.strftime("%Y%m%d")
    
    security_list = []
    
    for expiry in EXPIRY_LIST:
        for tenor in TENOR_LIST:
            
            security_input = "USSN{}{} BBIR Curncy".format(expiry, tenor)
            security_list.append(security_input)
    
    (con.bdh(
        tickers = security_list,
        flds = flds,
        start_date = start_date_input,
        end_date = end_date_input).
        reset_index().
        melt(id_vars = "date").
        to_parquet(
            path = output_file,
            engine = "pyarrow"))
    
    print("[INFO] Collected from Bloomberg Terminal")