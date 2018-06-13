from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
import bs4
import csv
import pandas as pd
import numpy as np

#driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.get('https://codeforces.com/')

driver.find_element_by_link_text('Enter').click()

handle=raw_input("Enter your handle: ")
pwd=raw_input("Enter your password: ")

driver.find_element_by_name('handleOrEmail').send_keys(handle)
driver.find_element_by_name('password').send_keys(pwd)
driver.find_element_by_xpath("//input[@value='Login']").click()

timeout=5
element_present = EC.presence_of_element_located((By.LINK_TEXT,handle))
WebDriverWait(driver, timeout).until(element_present)
driver.find_element_by_link_text(handle).click()

with open('Myfriends.csv', 'w') as f:
    f.write("Handle" + "," + "Max_Rating" + "," + "Current_Rating" + "," + "Title" + "\n")

title=str(driver.find_element_by_xpath("//div[@class='user-rank']/span").text)
curr_rat=str(driver.find_element_by_xpath("//div[@class='info']/ul/li/span").text)
max_rat=str(driver.find_element_by_xpath("//div[@class='info']/ul/li/span[@class='smaller']").text)
max_rat=max_rat[-5:-1]

with open('Myfriends.csv', 'a') as f:
    f.write(handle + "," + max_rat + "," + curr_rat+ "," + title + "\n")


driver.find_element_by_link_text('My friends').click()
url=driver.current_url


row_count = len(driver.find_elements_by_xpath("//div[@class='datatable']/div[6]/table[@class='']/tbody/tr"))
#print(row_count)


#for i in range(1,row_count):
i=1
while i < row_count:
    x=str(i)
    friend_handle=str(driver.find_element_by_xpath("//div[@class='datatable']/div[6]/table[@class='']/tbody/tr["+x+"]/td[2]").text)
    driver.find_element_by_link_text(friend_handle).click()

    timeout=5
    element_present = EC.presence_of_element_located((By.LINK_TEXT,friend_handle))
    WebDriverWait(driver, timeout).until(element_present)

    title=str(driver.find_element_by_xpath("//div[@class='user-rank']/span").text)
    curr_rat=str(driver.find_element_by_xpath("//div[@class='info']/ul/li/span").text)
    max_rat=str(driver.find_element_by_xpath("//div[@class='info']/ul/li/span[@class='smaller']").text)
    max_rat=max_rat[-5:-1]

    with open('Myfriends.csv', 'a') as f:
        f.write(friend_handle + "," + max_rat + "," + curr_rat+ "," + title + "\n")

    driver.get(url)
    i=i+1

timeout=5
element_present = EC.presence_of_element_located((By.LINK_TEXT,'HOME'))
WebDriverWait(driver, timeout).until(element_present)
driver.find_element_by_link_text('HOME').click()

timeout=5
element_present = EC.presence_of_element_located((By.LINK_TEXT,'Logout'))
WebDriverWait(driver, timeout).until(element_present)
driver.find_element_by_link_text('Logout').click()

driver.close()

df=pd.read_csv('Myfriends.csv')
df=df.sort_values('Current_Rating',ascending=[False])
df.insert(0, 'Rank', range(1,1+len(df)))
df.to_csv('Rank.csv', encoding='utf-8', index=False)

