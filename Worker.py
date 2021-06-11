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

    def __init__(self, jobs, wid, mins, out_dir):
        self.min_wait = mins
        self.jobs = jobs
        self.wid = wid
        self.history = {}
        self.history_count = {}
        self.fname = "results/workers_temp/w{}.csv".format(str(wid))
        self.out_dir = out_dir

        dir_path = os.path.dirname(os.path.realpath(__file__))
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--incognito")
        options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
        options.add_argument("--disable-dev-shm-usage");
        options.add_argument("--no-sandbox");
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

            for isin, link in self.jobs:

                if link in ["#N/A", '']:
                    continue

                content, content_html = self.getRequestSelenium(link)
                if content=='':
                    continue

                now = datetime.now()
                current_time = now.strftime("%H_%M_%S")
                fname = "results/{}/{}_{}.html".format(self.out_dir, isin,current_time)
                utils.writeFile(fname, content_html)


        self.driver.quit()



    def getRequestSelenium(self,url):
        content = ""
        content_html = ""
        try:
            self.driver.get(url)

            time.sleep(2.5)
            #for _ in range(0,10): 
            #   if self.driver.execute_script('return document.readyState;') == 'complete':
            #        break
            #    time.sleep(0.2)
            
            #html = self.driver.find_element_by_tag_name('html').get_attribute('innerHTML')
            html = self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

            soup = BeautifulSoup(html,"html.parser")
            content_html = html
            content = soup.text
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
                
