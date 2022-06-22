
from multiprocessing import Process
from datetime import datetime
from Worker import Worker
import multiprocessing
import zipfile
import shutil
import pandas as pd
import math
import time
import os

def job(websites, wid, mins, out_dir):
    worker = Worker(websites, wid, mins, out_dir)
    worker.start()

def zipdir(dir_name):
    def zipHandler(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))

    zipf = zipfile.ZipFile('results/{}.zip'.format(dir_name), 'w', zipfile.ZIP_DEFLATED)
    zipHandler('results/{}/'.format(dir_name), zipf)
    zipf.close()
    shutil.rmtree('results/{}/'.format(dir_name))

def start(mins):
    today = None
    input_csv = "resources/input.csv"
    
    while True:
        df = pd.read_csv(input_csv)
        df = df.fillna("")
        
        today = datetime.today().date()
        works = [] 
        if os.path.isfile("resources/{}.csv".format(str(today))):
            os.replace("resources/{}.csv".format(str(today)), "resources/cache/{}.csv".format(str(today)))
            df_today = pd.read_csv("resources/cache/{}.csv".format(str(today)))
            df_today = df_today.fillna("")
            for _, row in df_today.iterrows():
                symbol = row["Symbol"]
                dt_temp = df[ df["Symbol"]==symbol ]
                if len(dt_temp.index)>0:
                    link = dt_temp.iloc[0]
                    works.append((symbol,link["website_ir"]))

        n_works = len(works)
        print("- {} works today {}".format(str(n_works),str(today)))
        if n_works>0:    
            out_dir = str(today)
            if not os.path.exists("results/"+out_dir):
                os.makedirs("results/"+out_dir)

            available_cpus = multiprocessing.cpu_count() + int(multiprocessing.cpu_count()/2)
            blocks = int(math.ceil(n_works/available_cpus))
            
            last_idx = 0
            processes = []
            for i in range(1,available_cpus+1):
                end_idx = i*blocks
                if end_idx > n_works:
                    end_idx = n_works

                sub_works = works.copy()
                sub_works = sub_works[last_idx:i*blocks]
                last_idx = i*blocks

                p = Process(target=job, args=(sub_works,i,mins,out_dir))
                processes.append(p)
                p.start()

            for pro in processes:
                pro.join()

            zip_proc = Process(target=zipdir, args=(str(out_dir), ) )
            zip_proc.start()
            print("- {} works done!".format(str(today)))
        else:
            time.sleep(60)
