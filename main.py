import multiprocessing
import sys
import Monitor
import time


if __name__ == "__main__":
    if multiprocessing.cpu_count()==1:
        print("error - at least 3 cores are required")
        sys.exit()
    print("start")
    if len(sys.argv)>2 and sys.argv[1]=="-monitor":
        Monitor.start(int(sys.argv[2]))
    else:
        print("invalid argv") 
    print("done")
