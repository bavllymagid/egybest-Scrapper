from selenium import webdriver
import time
from os import sys
import os 
import driverConfig
from bs4 import BeautifulSoup
import requests 


# input from user 
input_search = input("movie: ")


URL = "https://race.egybest.world/explore/?q="+input_search+""

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

movies =driver.find_elements_by_xpath('//*[@id="movies"]/a')
number_of_movies = len(driver.find_elements_by_xpath('//*[@id="movies"]/a')) 

if number_of_movies == 0 :
    driver.close()
    print("can't found the movie you want\n")
    sys.exit()

#searching algorithm 
found = 0
for num in range(1,number_of_movies) :
    movies = driver.find_element_by_xpath('//*[@id="movies"]/a['+str(num)+']/span[2]')
    if input_search.lower() in movies.text.lower():
        if num == 1:
            print("\n\n===========Available movies============\n")
        found = 1 
        print(" "+str(num)+" : "+movies.text)


if found == 0 :
    print("\n===========can't find the movie you want============\n")
    driver.close()
    sys.exit()

#getting movie page 
movie_code = input("Enter movie code : ")
selected_move = driver.find_element_by_xpath('//*[@id="movies"]/a['+movie_code+']/span[2]').click()
title = driver.find_element_by_xpath('//*[@id="movies"]/a['+movie_code+']/span[2]').text

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