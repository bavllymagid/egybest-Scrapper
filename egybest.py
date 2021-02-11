from selenium import webdriver
import time
from os import sys
import os 
import driverConfig
from bs4 import BeautifulSoup
import requests 


# input from user 
input_search = input("movie: ")
URL = "https://cola.egybest.guru/explore/?q="+input_search+""

print("\n=========Searching for movie===========")

#checking the internet connection
if driverConfig.check_internet(URL) == False :
    print("\n======= please check your internet connection ======\n")
    time.sleep(7)
    sys.exit()
    

#running the browser in the back ground 
options = driverConfig.get_web_driver_options()
driverConfig.set_driver_as_head_less(options)
driverConfig.set_ignore_certificate_error(options)
driverConfig.set_browser_as_incognito(options)
#disabling browser and python warnings
driverConfig.hide_browser_massages(options)
driverConfig.disable_python_warnings()

#identifying the driver 
driver = driverConfig.open_browser(options)
driver.get(URL)
 

#saving the current page 
parent_h = driver.current_window_handle

movieFound = 0
movies = driver.find_elements_by_xpath('//*[@id="movies"]/a/span')
#searching algorithm 
for movie in movies :
    if input_search.lower() in movie.text.lower():
        movie.click()
        movieFound = 1
        title = movie.text
        break

if movieFound == 0 :
    print("\n\n\nthe movie you want is not found ... \n")
    time.sleep(1)
    driver.close()
    os.startfile(sys.argv[0])
    sys.exit()
    
time.sleep(1)


#switching to the popup url 
for handle in driver.window_handles: 
    if handle != parent_h: 
        login_page = handle 
          
        
driver.switch_to.window(login_page) 

driver.close()
#switching to the parent page again 
driver.switch_to.window(parent_h) 


time.sleep(3)
print("\n=========Done===========")
#getting the length of number of qualities 
length = len(driver.find_elements_by_xpath('//*[@id="watch_dl"]/table/tbody/tr'))

if length != 0: 
    #getting the download qualities  
    linkFound = 0 
    print("\n\n===========Available qualities============\n")
    print("choose quality:: press :")
    for s in range(1,length):
        qualities = driver.find_element_by_xpath('//*[@id="watch_dl"]/table/tbody/tr['+str(s)+']/td[2]').text
        print(" "+str(s) + " for " + qualities)

    Quality = int(input())
else:
    print("==========this is not a movie==========")    
    driver.quit()
    sys.exit()

#to check the validty of the quality entered 
if(Quality == "invalid quality"):
    print("\n\n\nplease enter valid choice for quality... \n")
    time.sleep(1)
    os.startfile(sys.argv[0])
    os.exit()

driver.find_element_by_xpath('//*[@id="watch_dl"]/table/tbody/tr['+str(Quality)+']/td[4]/a/i').click()
print("\n==========Preparing for downloading===========\n")
time.sleep(3)

#switching to the popup url 
for handle in driver.window_handles: 
    if handle != parent_h: 
        login_page = handle 

down_parent = login_page 

driver.switch_to.window(down_parent) 

#click download two times 

time.sleep(3)
driver.find_element_by_xpath('/html/body/div[1]/div/p/a[1]/i').click() 

#switching to the popup url 
for handle in driver.window_handles: 
    if handle != parent_h: 
        login_page = handle 
time.sleep(3)
driver.switch_to_window(login_page) 
driver.close()
driver.switch_to_window(down_parent) 
time.sleep(3)
print("\n==========Done===========\n")
#getting download link
movieUrl = driver.find_element_by_xpath('/html/body/div[1]/div/p/a[1]').get_attribute('href')
driver.quit()
driverConfig.download(movieUrl, title + '.mp4')