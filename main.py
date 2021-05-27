from JoinCSV import joinCSV
import multiprocessing
import pandas as pd
import Monitor
import schedule
import time
import sys


if __name__ == "__main__":
    if multiprocessing.cpu_count()==1:
        print("Error: at least 3 cores are required!")
        sys.exit()

    if len(sys.argv)<2:
        print("Error: invalid arguments!")
        sys.exit()

    print("Start!")

    if sys.argv[1]=="-monitor":
        schedule.every(5).seconds.do(Monitor.start)
        schedule.every().day.at("00:00").do(Monitor.start)

        while True:
            schedule.run_pending()
            time.sleep(1)
    elif sys.argv[1]=="-join":
        joinCSV()
    else:
        print("Error: invalid arguments!") 

    print("Done!")