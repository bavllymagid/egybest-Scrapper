from selenium import webdriver
import time
from os import sys
import os 
import driverConfig
from bs4 import BeautifulSoup
import requests 


# input from user 
input_search = input("movie: ")
nQuality = int(input("choose quality:: press 1 for 240 / 2 for 360/ 3 for 480 / 4 for 720p / 5 for 1080p : "))


finalQuality = driverConfig.quality(nQuality)

#to check the validty of the quality entered 
if(finalQuality == "invalid quality"):
    print("\n\n\nplease enter valid choice for quality... \n")
    time.sleep(1)
    os.startfile(sys.argv[0])
    os.exit()

#running the browser in the back ground 
options = driverConfig.get_web_driver_options()
driverConfig.set_driver_as_head_less(options)
driverConfig.set_ignore_certificate_error(options)
driverConfig.set_browser_as_incognito(options)


#identifying the driver 
driver = driverConfig.open_browser(options)

driver.get("https://cola.egybest.guru/explore/?q="+input_search+"")
 

#saving the current page 
parent_h = driver.current_window_handle

movieFound = 0
movies = driver.find_elements_by_xpath('//*[@id="movies"]/a/span')
#searching algorithm 
for movie in movies :
    if input_search.lower() in movie.text.lower():
        movie.click()
        movieFound = 1 
        break

if movieFound == 0 :
    print("\n\n\nthe movie you want is not found ... \n")
    time.sleep(1)
    driver.close()
    os.startfile(sys.argv[0])
    sys.exit()
    



#switching to the popup url 
for handle in driver.window_handles: 
    if handle != parent_h: 
        login_page = handle 
          
        
driver.switch_to.window(login_page) 

driver.close()
#switching to the parent page again 
driver.switch_to.window(parent_h) 


time.sleep(3)
#getting the length of number of qualities 
length = len(driver.find_elements_by_xpath('//*[@id="watch_dl"]/table/tbody/tr'))

#getting the id of download button  
linkFound = 0 
for s in range(1,length):
    if finalQuality in driver.find_element_by_xpath('//*[@id="watch_dl"]/table/tbody/tr['+str(s)+']/td[2]').text:
        driver.find_element_by_xpath('//*[@id="watch_dl"]/table/tbody/tr['+str(s)+']/td[4]/a/i').click()
        linkFound = 1 
        break
#if the download button not found       
if (linkFound == 0):
    print("\n\n\nthe quality required is not found... \n")
    time.sleep(1)
    driver.close()
    sys.exit()

time.sleep(3)

#switching to the popup url 
for handle in driver.window_handles: 
    if handle != parent_h: 
        login_page = handle 

down_parent = login_page 

driver.switch_to.window(down_parent) 

#click download two times 

time.sleep(1)
driver.find_element_by_xpath('/html/body/div[1]/div/p/a[1]/i').click() 
#switching to the popup url 
for handle in driver.window_handles: 
    if handle != parent_h: 
        login_page = handle 
driver.switch_to_window(login_page) 
driver.close()
driver.switch_to_window(down_parent) 
time.sleep(1)

#getting download link 
a= driver.find_element_by_xpath('/html/body/div[1]/div/p/a[1]').get_attribute('href')
print(a)
