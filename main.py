import multiprocessing
import sys
import schedule
import Monitor
import time


if __name__ == "__main__":
    if multiprocessing.cpu_count()==1:
        print("error - at least 3 cores are required")
        sys.exit()
    print("start")
    if sys.argv[1]=="-monitor":
        schedule.every(5).seconds.do(Monitor.start)
        schedule.every().day.at("00:00").do(Monitor.start)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("invalid argv") 
    print("done")