from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests, warnings
from tqdm import tqdm

def get_web_driver_options():
    return webdriver.ChromeOptions()

def set_driver_as_head_less(options):
    options.add_argument('--headless')

def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')

def set_browser_as_incognito(options):
    options.add_argument('--incognito')   

def hide_browser_massages(options):
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  

def disable_python_warnings():
    warnings.filterwarnings("ignore")     

def download(url, fname):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def quality(argument):
    switcher={
        1:'240',
        2:'360',
        3:'480',
        4:'720',
        5:'1080',
    }
    return switcher.get(argument, "invalid quality")    

def open_browser(options):
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    return driver

