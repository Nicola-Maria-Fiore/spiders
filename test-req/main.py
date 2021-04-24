import sys
import time
import requests
import pandas as pd

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

df = pd.read_csv(sys.argv[1])
df["req_count"] = 0
df["req_ok"] = 0
df_time = pd.DataFrame(columns=["time","req_ok"])

start_time = int(time.time())
init_time = start_time
first = True
while True:
    if first==False:
        while int(time.time())-start_time<120:
            time.sleep(1)
    first = False
    start_time = int(time.time())
    print("- Session start at {}".format(str(start_time-init_time)))
    req_ok = 0
    for index, row in df.iterrows():
        df.loc[index,"req_count"] += 1
        try:
            r = requests.get(row["website_ir"], headers=HEADERS)
            if r.status_code == 200:
                df.loc[index,"req_ok"] += 1
                req_ok += 1
        except:
            pass

    idx = len(df_time.index)
    df_time.loc[idx,"time"] = start_time-init_time
    df_time.loc[idx,"req_ok"] = req_ok
    df["ok_prc"] = (100/df["req_count"])*df["req_ok"]

    df.to_csv("res.csv")
    df_time.to_csv("dist.csv")