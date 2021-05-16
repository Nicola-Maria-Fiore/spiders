import pandas as pd
import os

def joinCSV():
    main_csv = "resources/input.csv"
    res_csvs_folder = "results/workers_temp/"
    main_df = pd.read_csv(main_csv)

    for filename in os.listdir(res_csvs_folder):
        if filename.endswith(".csv"): 
            print(filename)