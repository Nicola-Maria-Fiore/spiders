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
while True:
    while int(time.time())-start_time<120 and start_time!=init_time:
        pass

    print("- Session start at {}".format(str(start_time)))
    start_time = int(time.time())
    req_ok = 0
    for index, row in df.iterrows():
        row["req_count"] += 1
        try:
            r = requests.get(row["website_ir"], headers=HEADERS)
            if r.status_code == 200:
                df["req_ok"] += 1
                req_ok += 1
        except:
            pass

    df_time.loc[len(df_time.index),"time"] = start_time-init_time
    df_time.loc[len(df_time.index),"req_ok"] = req_ok
    df["%ok"] = (100/row["req_count"])*df["req_ok"]

    df.to_csv("res.csv")
    df_time.to_csv("dist.csv")