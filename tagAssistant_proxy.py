
import time
import os
from tqdm import tqdm
from browsermobproxy import Server
import json
server = Server("\\browsermob-proxy-2.1.4-bin\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat")
server.start()
proxy = server.create_proxy()
from collections import defaultdict
import xlwt
from selenium import webdriver
from harparser import HAR
from selenium.webdriver.common.proxy import Proxy,ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
wb = xlwt.Workbook()

var = raw_input("Please enter the url of the site after www. ")
siteurl="https://www."+var+"sitemap.xml"
def capture_and_write(filter_string,sheet_name,harfile):

    o = harfile
    ws = wb.add_sheet(sheet_name)
    input_list=[]
    j=0
    length_key=0
    maximum_len=0

    for key in o:
        for value in o[key]["entries"]:
            if filter_string in value["request"]["url"]:
                j=j+1
                if length_key < len(value["request"]["queryString"]):
                    length_key = len(value["request"]["queryString"])
                    maximum_len =j
    j=0
    for key in o:
        for value in o[key]["entries"]:
            if filter_string in value["request"]["url"]:
                j=j+1
                if j is maximum_len:
                    for i,enum1 in enumerate(value["request"]["queryString"]):
                        ws.write(i, 0,enum1['name'])
                        input_list.append(enum1['name'])

    j=0
    for key in o:
        for value in o[key]["entries"]:
            if filter_string in value["request"]["url"]:
                j=j+1
                for i,enum1 in enumerate(value["request"]["queryString"]):
                    for k in input_list:
                            if k == enum1['name']:
                                try:
                                    ws.write(input_list.index(k), j,enum1['value'])
                                except:
                                    continue


capabilities = DesiredCapabilities.CHROME.copy()
chop = webdriver.ChromeOptions()
chop.add_argument("--proxy-server={0}".format(proxy.proxy))
capabilities['unexpectedAlertBehaviour']="accept"
driver = webdriver.Chrome(desired_capabilities=capabilities,chrome_options=chop)

driver.set_page_load_timeout(30)
list=[]

driver.get(siteurl)
links = driver.find_elements_by_tag_name('loc')
count = len(links)
count=0
for i in links:
   #try:
      count+=1
      if count <100:
          list.append(i.get_attribute('textContent'))
      else:
          continue 

proxy.new_har("omniture")
for i in tqdm(list):
    try:
        driver.get(i)
        elements = browser.find_element_by_css_selector("a[data-ct-action]")
        print elements
        for x in range(0,len(elements)):
            if like[x].is_displayed():
                like[x].click()
    except:
        continue


driver.quit()

server.stop()
capture_and_write('/b/ss',"Adobe Analytics",proxy.har)
capture_and_write('google-analytics.com/collect',"Google Analytics",proxy.har)
capture_and_write('www.facebook.com/tr/',"Facebook Pixel",proxy.har)
wb.save('Data.xls')
