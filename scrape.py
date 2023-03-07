import requests
from bs4 import BeautifulSoup
import pandas as pd
import pwinput
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def getSheet(regno, password):

    # regno = input("Enter Registration Number: ")
    # password = pwinput.pwinput(prompt='Enter Password: ')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)
    driver.get("https://eduserve.karunya.edu/Login.aspx")
    
    driver.implicitly_wait(15)

    uname = driver.find_element("id", "mainContent_Login1_UserName") 
    uname.send_keys(regno)
    pwd = driver.find_element("id", "mainContent_Login1_Password") 
    pwd.send_keys(password)
    driver.find_element("id", "mainContent_Login1_LoginButton").click()

    try:
        url = "https://eduserve.karunya.edu/Student/AttSummary.aspx"
        driver.get(url)

        select = Select(driver.find_element('id','mainContent_DDLACADEMICTERM'))
        select.select_by_visible_text('2022-23 Even Semester')
        
        df = scrape(driver)

    except Exception:
        for i in range(9):
            try:
                s = "ctl00_mainContent_grdHFB_ctl00_ctl0" + str(i) + "_rdoClassHandle"
                driver.find_element('id',s).click()
            except:
                pass
        
        driver.find_element("id", "mainContent_btnSave").click()
        
        url = "https://eduserve.karunya.edu/Student/AttSummary.aspx"
        driver.get(url)

        select = Select(driver.find_element('id','mainContent_DDLACADEMICTERM'))
        select.select_by_visible_text('2022-23 Even Semester')
        
        df = scrape(driver)
        
    driver.quit()

    return df

def scrape(page):
    
    soup = BeautifulSoup(page.page_source, 'html.parser')
    tables = soup.find_all('table')

    df = pd.read_html(str(tables[2]), flavor='html5lib')
    df = pd.DataFrame(df[0])

    return df
