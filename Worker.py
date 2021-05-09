from requests import Request, Session
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import csv
import os

class Worker:

    def __init__(self, jobs, wid):
        self.jobs = jobs
        self.wid = wid
        self.fname = "results/workers_temp/w{}.csv".format(str(wid))
        if os.path.isfile(self.fname):
            self.df = pd.read_csv(self.fname,index_col=False)
        else:
            self.df = pd.DataFrame(columns=["index",'link','main'])
            self.df = self.df.fillna("")
        
        for job in self.jobs:
            index = len(self.df.index)
            self.df.loc[index,"index"] = job[0]
            self.df.loc[index,"link"] = job[1]
            self.df.loc[index,"main"] = ""


    #wirks are list of pairs (index,link)
    def start(self):
        n_jobs = len(self.jobs)
        print("Worker {} started with {} jobs".format(str(self.wid),str(n_jobs)))
        
        last_day = datetime.datetime.now().day
        last_timestamp = int(time.time())
        first = True
        while True:
            curr_day = datetime.datetime.now().day
            if curr_day != last_day:
                break
            
            if first==False:
                curr_timestamp = int(time.time())    
                while curr_timestamp-last_timestamp < 120:
                    time.sleep(1)
                    curr_timestamp = int(time.time())
                last_timestamp = curr_timestamp
            else:
                first = False

            for index, row in self.df.iterrows():
                content = self.getRequest(row["link"]).replace("\n"," ")
                if self.df.loc[index,"main"]=="":
                    self.df.loc[index,"main"] = content

            self.df.to_csv(self.fname, quotechar='"', quoting=csv.QUOTE_ALL, encoding='utf-8-sig')

        print("DOne")


    def getRequest(self,url):
        content = ""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url)
            html = response.text
            soup = BeautifulSoup(html,"html.parser")
            body = soup.findAll('body')
            if len(body)>0:
                content = body[0].text
        except Exception as e:
            print(e)
        
        return content