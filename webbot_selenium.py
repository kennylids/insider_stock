import settings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time
import os
from datetime import datetime

import shutil


def scrapedaily(dir):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": dir + "\\input"})
    # options/bin
    PATH = dir + "\\chromedriver.exe"
    driver = webdriver.Chrome(PATH, chrome_options=options)

    driver.get("http://www.j3sg.com/index.php")
    driver.find_element("name", "userid").send_keys("liwingtai120@gmail.com")
    driver.find_element("name", "password").send_keys("kl9712")
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(1)

    driver.get("http://www.j3sg.com/predefined/dailyFilings-download.php")
    url = 'retrieveDownload.php?in=2'
    url2 = 'retrieveDownload.php?in=3'
    # time.sleep(1)
    if driver.find_elements(By.XPATH, "//span[@class='ns-o0dvb-e-18']"):
        driver.find_element(By.XPATH, "//span[@class='ns-o0dvb-e-18']").click()
        time.sleep(1)

    driver.find_element(By.XPATH, '//a[@href="' + url + '"]').click()

    # driver.get("http://www.j3sg.com/predefined/dailyFilings-download.php")
    # time.sleep(10)
    # driver.get("http://www.j3sg.com/predefined/dailyFilings-download.php")
    # driver.find_element_by_xpath('//a[@href="'+url2+'"]').click()
    time.sleep(10)

    driver.quit()

    today = datetime.today().strftime('%Y%m%d')
    # directory = r'C:\Users\liwin\OneDrive\Desktop\stock\input'
    # directory = os.path.join(dir, 'input')
    # os.chdir(settings.directory)
    os.chdir(dir + "\\input")

    # print(os.getcwd())
    name1 = 'insider_buy_' + str(today) + '.xls'
    # name2= 'insider_sell_' + str(today) + '.xls'
    os.rename('results.xls', name1)
    # os.rename('results (1).xls', name2)

    # newPath = shutil.move(name1, 'input')
    # newPath2 = shutil.move(name2, 'input')

    # new_name = os.path.join(directory, 'insider_buy_' + str(today) + '.xls')
    # new_name2 = os.path.join(directory, 'insider_sell_' + str(today) + '.xls')

    # try:

    # except:
    #     print("An exception occurred")


def scrapeweekly(dir):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"download.default_directory": dir + "\\input"})
    # options/bin
    PATH = dir + "\\chromedriver.exe"
    driver = webdriver.Chrome(PATH, chrome_options=options)

    driver.get("http://www.j3sg.com/index.php")
    driver.find_element("name", "userid").send_keys("liwingtai120@gmail.com")
    driver.find_element("name", "password").send_keys("kl9712")
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(1)

    urlList= {
        "insider_buy_weekly_":"retrieveDownload.php?in=2",
        "insider_sell_weekly_": "retrieveDownload.php?in=3"
    }
    # ['retrieveDownload.php?in=2','retrieveDownload.php?in=3']

    today = datetime.today().strftime('%Y%m%d')
    os.chdir(dir + "\\input")

    for name, downloadUrl in urlList.items():

        driver.get("http://www.j3sg.com/predefined/dailyFilings-download.php")
    # url = 'retrieveDownload.php?in=2'
    # url2 = 'retrieveDownload.php?in=3'

        if driver.find_elements(By.XPATH, "//span[@class='ns-o0dvb-e-18']"):
            driver.find_element(By.XPATH, "//span[@class='ns-o0dvb-e-18']").click()
            time.sleep(1)
        driver.find_element(By.XPATH, '//a[@href="' + downloadUrl + '"]').click()

        time.sleep(10)
        new_name = name + str(today) + '.xls'
        os.rename('results.xls', new_name)

    driver.quit()




    #
    # new_name = 'insider_buy_weekly_' + str(today) + '.xls'
    # os.rename('results.xls', new_name)
