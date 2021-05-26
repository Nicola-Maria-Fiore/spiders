from requests import Request, Session
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import utils
import time
import csv
import os

class Worker:
    req_headers = headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    pdf_out = "results/pdf/"

    def __init__(self, jobs, wid):
        self.jobs = jobs
        self.wid = wid
        self.history = {}
        self.history_count = {}
        self.fname = "results/workers_temp/w{}.csv".format(str(wid))
        if os.path.isfile(self.fname):
            self.df = pd.read_csv(self.fname,index_col=False)
        else:
            self.df = pd.DataFrame(columns=["index",'link','main'])
            self.df = self.df.fillna("")
        
        self.working_rows = []
        for job in self.jobs:
            index = len(self.df.index)
            self.df.loc[index,"index"] = job[0]
            self.df.loc[index,"link"] = job[1]
            self.df.loc[index,"main"] = ""
            self.working_rows.append(index)



    #wirks are list of pairs (index,link)
    def start(self):
        n_jobs = len(self.jobs)
        print("Worker {} started with {} jobs".format(str(self.wid),str(n_jobs)))
        #if(self.wid==2):
        #    return
        
        last_day = datetime.now().day
        last_timestamp = int(time.time())
        first = True
        while True:
            curr_day = datetime.now().day
            if curr_day != last_day:
                break
            
            if first==False:
                curr_timestamp = int(time.time())    
                while curr_timestamp-last_timestamp < 10: #120
                    time.sleep(1)
                    curr_timestamp = int(time.time())
                last_timestamp = curr_timestamp
            else:
                first = False

            print("- Worker {} : new check at {}".format(str(self.wid),datetime.now().strftime("%H:%M:%S")))

            update = False
            for index in self.working_rows:
                if self.df.loc[index,"link"]=="#N/A" or self.df.loc[index,"link"]=='':
                    continue

                content, content_html = self.getRequest(self.df.loc[index,"link"])
                if content=='':
                    continue

                #print(index)

                content = content.replace("\n"," ")
                if self.df.loc[index,"main"]=="":
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")

                    self.df.loc[index,"main"] = "[{}] {}".format(current_time,content)
                    self.history[index] = content
                    self.history_count[index] = 1
                    update = True
                else:
                    if content!=self.history[index]:
                        now = datetime.now()
                        current_time = now.strftime("%H:%M:%S")
                        print("- Worker {} : change found at {}".format(str(self.wid),datetime.now().strftime("%H:%M:%S")))

                        new_page = self.pageDiff(self.history[index], content)
                        self.df.loc[index,"Update_"+str(self.history_count[index])] = "[{}] {}".format(current_time,new_page)
                        self.history[index] = content
                        self.history_count[index] = self.history_count[index] + 1

                        self.findPDF(content_html, "Update_"+str(index), self.history_count[index])
                        update = True

            if update:
                self.df.to_csv(self.fname, quotechar='"', quoting=csv.QUOTE_ALL, encoding='utf-8-sig', index=False)



    def getRequest(self,url):
        content = ""
        content_html = ""
        session = Session()
        session.headers.update(self.req_headers)
        try:
            response = session.get(url, timeout=6)
            html = response.text
            soup = BeautifulSoup(html,"html.parser")
            body = soup.findAll('body')
            if len(body)>0:
                content_html = str(body[0])
                content = body[0].text
        except Exception as e:
            print("-- Net error --")
        
        return content, content_html


    def pageDiff(self,old_page, new_page):
        old_page = old_page.split()
        new_page = new_page.split()
        
        diff_start = 0
        for index, val in enumerate(new_page):
            if index < len(old_page):
                if val!=old_page[index]:
                    diff_start = index
                    break


        diff_end = len(new_page)
        for i in range(1,len(new_page)):
            if len(old_page)-i >= 0 and len(new_page)-i >= 0:
                if new_page[len(new_page)-i] != old_page[len(old_page)-i]:
                    diff_end = len(new_page)
                    break 

        return " ".join(new_page[diff_start:diff_end])


    
    def findPDF(self, html, fname, id):
        soup = BeautifulSoup(html,"html.parser")
        n = 1
        for a in soup.find_all('a', href=True):
            link = a['href']
            if link.endswith('pdf'):
                fname = self.pdf_out+"{}_{}_{}.pdf".format(str(id),fname, str(n))
                session = Session()
                session.headers.update(self.req_headers)
                try:
                    r = session.get(link)
                    if 'application/pdf' in r.headers.get('content-type'):
                        utils.saveBinFile(fname,r.content)
                        n += 1
                except Exception as e:
                    pass


                
