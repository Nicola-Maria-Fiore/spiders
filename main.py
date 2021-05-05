from multiprocessing import Pool
import multiprocessing
import pandas as pd
import schedule
import time


def findWorks(df):
    print("Checking...")
    available_cpus = multiprocessing.cpu_count() - 1

    n = int(len(df.index)/available_cpus)  #chunk row size
    list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]
    print(list_df)



if __name__ == "__main__":
    input_csv = "resources/input.csv"
    df = pd.read_csv(input_csv)

    checker = lambda : findWorks(df)
    schedule.every(10).seconds.do(checker)
    schedule.every().day.at("00:00").do(checker)


    while True:
        schedule.run_pending()
        time.sleep(1)