from requests import Request, Session
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import utils
import time
import csv
import os


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class Worker:
    req_headers = headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    def __init__(self, jobs, wid, mins):
        self.min_wait = mins
        self.jobs = jobs
        self.wid = wid
        self.history = {}
        self.history_count = {}
        self.fname = "results/workers_temp/w{}.csv".format(str(wid))
        if os.path.isfile(self.fname):
            self.df = pd.read_csv(self.fname,index_col=False)
        else:
            self.df = pd.DataFrame(columns=["index",'link'])
            self.df = self.df.fillna("")
        
        self.working_rows = []
        for job in self.jobs:
            index = len(self.df.index)
            self.df.loc[index,"index"] = job[0]
            self.df.loc[index,"link"] = job[1]
            self.history_count[index] = 1
            self.working_rows.append(index)

        self.df["index"] = self.df["index"].astype(int)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--incognito")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(executable_path=os.path.join(dir_path, "chromedriver"), chrome_options=options)
        self.driver.set_page_load_timeout(6)
        self.ea = ["earnings announcment", "earnings release", "quarterly report", "earnings press release"]



    #wirks are list of pairs (index,link)
    def start(self):
        n_jobs = len(self.jobs)
        print("Worker {} started with {} jobs".format(str(self.wid),str(n_jobs)))
        
        last_day = datetime.now().day
        last_timestamp = int(time.time())
        first = True
        while True:
            curr_day = datetime.now().day
            if curr_day != last_day:
                break
            

            if first==False:
                curr_timestamp = int(time.time())
                    
                time_diff = curr_timestamp-last_timestamp 
                if time_diff>self.min_wait:
                    print("- Late! "+str(time_diff))

                while curr_timestamp-last_timestamp < self.min_wait: 
                    time.sleep(1)
                    curr_timestamp = int(time.time())
                last_timestamp = curr_timestamp
            else:
                first = False

            print("- Worker {} : new check at {}".format(str(self.wid),datetime.now().strftime("%H:%M:%S")))

            for index in self.working_rows:

                if self.df.loc[index,"link"]=="#N/A" or self.df.loc[index,"link"]=='':
                    continue

                content, content_html = self.getRequestSelenium(self.df.loc[index,"link"])
                #content, content_html = self.getRequest(self.df.loc[index,"link"])
                if content=='':
                    continue

                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                text = "[{}] {}".format(current_time, content_html.replace('\n'," "))
                self.df.loc[index,"Update_"+str(self.history_count[index])] = text
                self.history_count[index] = self.history_count[index] + 1

            self.df.to_csv(self.fname, quotechar='"', quoting=csv.QUOTE_ALL, encoding='utf-8-sig', index=False)

        self.driver.quit()



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
            #print("-- Net error --")
            pass
        
        return content, content_html



    def getRequestSelenium(self,url):
        content = ""
        content_html = ""
        try:
            self.driver.get(url)
            html = self.driver.find_element_by_tag_name('html').get_attribute('innerHTML')

            for _ in range(0,10): 
                if self.driver.execute_script('return document.readyState;') == 'complete':
                    break
                time.sleep(0.2)

            soup = BeautifulSoup(html,"html.parser")
            body = soup.findAll('body')
            if len(body)>0:
                content_html = str(body[0])
                content = body[0].text
        except Exception as e:
            #print("-- Net error --")
            pass
        
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
                
