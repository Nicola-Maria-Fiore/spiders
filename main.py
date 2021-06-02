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
    if len(sys.argv)>2 and sys.argv[1]=="-monitor":
        monitor_taks = lambda : Monitor.start(int(sys.argv[2]))
        schedule.every(5).seconds.do(monitor_taks)
        schedule.every().day.at("00:00").do(monitor_taks)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("invalid argv") 
    print("done")