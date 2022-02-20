# import packages
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from time import sleep
from datetime import datetime, date
import re, os, shutil, sys
# import win32com.shell.shell as shell
# ASADMIN = 'asadmin'

# if sys.argv[-1] != ASADMIN:
#     script = os.path.abspath(sys.argv[0])
#     params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
#     shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)

# DOCSTRING
"""
This script is designed to be a webscraper specifically for the AIP site of Amsterdam.
Fetch all DMS files from a batch.

    start:  run file (possible to run as admin if necassary due to company policy)
    input:  useremail (str)
            password (str)
            batch number (int)
            download directory (str)
    output: DMS files per object in a batch

NOTE:
When a error because of the webdriver version occurs make sure to check which version is on the machine.
If the version is not included to the versions mentioned bellow, add it to the drivers folder.
After your version of the chromedriver is added, change the 'if' statement in the code under
the 'VERSION' comment.

Default browser and version:    Chrome; versions 94 till 99
Default driver:                 chromedriver.exe (for versions 94 till 99)

Check your browser version: 'help' -->  'About Google Chrome'

If the version differs from the default version used by this tool, than download the driver for the verion used by your machine here:
https://chromedriver.chromium.org/downloads
"""

def input_scraper(batch, folder):

    # start timing
    start_time = datetime.now()

    # ad a zero in front of the first 9 numbers to prevent an accidental hit with it's tenfold
    if len(batch) < 2:
        batch = "0" + str(batch)

    # check and create batch folder with error handeling for duplicates
    dupl = 0
    batch_name = "Batch " + str(batch)
    for file in os.listdir(folder):
        if batch_name in file:
            dupl += 1

    today = date.today()
    d = today.strftime("%d-%m-%y")  

    # create a folder and variable with the path to the batch directory
    batch_name = batch_name + "_v" + str(dupl) + "_" + str(d)
    path = os.path.join(folder, batch_name).replace("/", "\\")
    os.makedirs(path)

    # set chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1366,768')
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--start-maximized')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # add directory preference
    prefs = {}
    prefs["profile.default_content_settings.popups"]=0
    prefs["download.default_directory"]=path
    chrome_options.add_experimental_option("prefs", prefs)
    print(path)

    return chrome_options, start_time, batch, path, batch_name

def version_find(chrome_options):
    # VERSION control
    # connect to driver with selenium and check version
    try:
        PATH = Service('drivers//chromedriver_94.exe')
        driver = webdriver.Chrome(service=PATH, options=chrome_options)
        version = True
    except:
        try:
            PATH = Service('drivers//chromedriver_95.exe')
            driver = webdriver.Chrome(service=PATH, options=chrome_options)
            version = True
        except:
            try:
                PATH = Service('drivers//chromedriver_96.exe')
                driver = webdriver.Chrome(service=PATH, options=chrome_options)
                version = True
            except:
                try:
                    PATH = Service('drivers//chromedriver_97.exe')
                    driver = webdriver.Chrome(service=PATH, options=chrome_options)
                    version = True
                except:
                    try:
                        PATH = Service('drivers//chromedriver_98.exe')
                        driver = webdriver.Chrome(service=PATH, options=chrome_options)
                        version = True
                    except:
                        try:
                            PATH = Service('drivers//chromedriver_99.exe')
                            driver = webdriver.Chrome(service=PATH, options=chrome_options)
                            version = True
                        except:
                            driver = "error"
                            version = False
                            
    return driver, version

## functions
# find an element by id
def find_by_id(elem_id, webdriver):
    # explicit wait for browser to load
    try:
        WebDriverWait(webdriver, 30).until(
            EC.presence_of_all_elements_located((By.ID, elem_id))
        )
    except:
        print("ERROR: Either loading time is taking longer than expected or ID not found")
    
    find_id = webdriver.find_element(By.ID, elem_id)

    return find_id

def find_by_xpath(elem_xpath, webdriver):
    try:
        WebDriverWait(webdriver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, elem_xpath))
        )
    except:
        print("ERROR: Either loading time is taking longer than expected or xpath is not found")

    # navigate to batch search bar
    find_xpath = webdriver.find_element(By.XPATH, elem_xpath)

    return find_xpath

def find_by_class_name(elem_class_name, webdriver):
    # explicit wait
    try:
        ignore_exceptions = (NoSuchElementException, StaleElementReferenceException, )
        WebDriverWait(webdriver, 30, ignored_exceptions=ignore_exceptions).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, elem_class_name))
        )
    except:
        print("ERROR: Either loading time is taking longer than expected or class name not found")

    # search for batch info and get object info
    find_class_name = webdriver.find_element(By.CLASS_NAME, elem_class_name)

    return find_class_name

def wait_for_class_name(elem_class_name, webdriver):
    # explicit wait
    try:
        WebDriverWait(webdriver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, elem_class_name))
        )
    except:
        print("ERROR: Either loading time is taking longer than expected or class name not found")


def login(username, password, driver, batchnum):
    ## Tie together
    # login tags for ID element find
    login_user_tag = "useremail"
    login_pass_tag = "password"
    # login
    user_inp = find_by_id(login_user_tag, driver)
    user_inp.send_keys(username)
    pass_inp = find_by_id(login_pass_tag, driver)
    pass_inp.send_keys(password)
    pass_inp.send_keys(Keys.ENTER)

    # searchbar batches xpath tag
    batches_path = "/html/body/span[1]/div[2]/div[1]/aside[1]/div[1]/ul[1]/li[5]/a[1]"
    list_path = "/html/body/span[1]/div[2]/div[1]/aside[1]/div[1]/ul[1]/li[5]/ul[1]/li[1]/a[1]"
    searchbar_tag = "searchName"
    # search bar batches
    batch_navigate = find_by_xpath(batches_path, driver)
    batch_navigate.click()
    # search bar list
    list_navigate = find_by_xpath(list_path, driver)
    list_navigate.click()

    # find searchbar and navigate to batch
    searchbar_find = find_by_id(searchbar_tag, driver)
    searchbar_find.send_keys("Batch " + str(batchnum))
    searchbar_find.send_keys(Keys.ENTER)

    # go to batch
    batch_info_tag = "nowrap"
    batch_info_navigate = find_by_class_name(batch_info_tag, driver)
    batch_info_navigate.click()

    # collect bru's
    bru_table_tag = 'table table-condensed table-hover'
    html_regex_bru = 'tr class="bg-white" style="cursor: default;"><td class="" style="cursor: pointer;">(.*?)</td'
    wait_for_class_name(bru_table_tag, driver)
    html_content_page = driver.page_source
    regex_tables = re.findall(html_regex_bru, str(html_content_page))

    return regex_tables

# function to loop through all bru's and collect data
def all_data(regex_tables, driver, path, batch_name):
    count = 1
    for bru in regex_tables:
        # remove whitespace
        bru = bru.rstrip()
        # go to specific bru info page
        bru_info_tag = "//tbody/tr[" + str(count) + "]/td[1]"
        bru_data = find_by_xpath(bru_info_tag, driver)
        bru_data.click()
        
        # assign one window
        window_one = driver.window_handles[0]

        # open DMS
        dms_tag = "/html/body/span[1]/div[2]/div[1]/section[1]/header[1]/div[2]/a[1]"
        find_dms = find_by_xpath(dms_tag, driver)
        find_dms.click()

        # assign and handle window two
        window_dms = driver.window_handles[1]
        driver.switch_to.window(window_dms)

        # show all files in table
        select_all_tag = '//select[@name="documents_length"]/option[text()="All"]'
        select_all = find_by_xpath(select_all_tag, driver)
        select_all.click()

        #TODO: remove sleep() and make a better solution
        sleep(4)

        # fetch page html content and find all hyperlinks with regex
        html_content = driver.page_source
        regex_code = 'href="/documents/download/document/(.*?)"'
        regex_hyperlinks = re.findall(regex_code, str(html_content))

        # make folder for each bru in batch directory
        path_bru = os.path.join(path, bru)
        os.mkdir(path_bru)

        # download all data
        for file in regex_hyperlinks:
            base = "https://bmidms.amsterdam.nl/documents/download/document/"
            total_link = os.path.join(base, file) 

            # get file
            driver.get(total_link)

            # wait till downloads ready
            download_check = os.listdir(path)
            while any(".crdownload" in file for file in download_check):
                sleep(1)
                download_check = os.listdir(path)
        
        # move all files to bru specific directory
        move_list = os.listdir(path)
        for files in move_list:
            fpath = os.path.join(path, files)
            if not os.path.isdir(fpath):
                if fpath.endswith(".tmp"):
                    pass
                else:
                    shutil.move(fpath, path_bru)

        #close window_dms
        driver.close()

        #assign window_one
        driver.switch_to.window(window_one)

        # go back one
        driver.back()

        # print update on download progress
        print("(" + str(count) + "/" + str(len(regex_tables)) + "): " + "From " + str(batch_name) + " and object " + str(bru) + " there where " + str(len(regex_hyperlinks)) + " files downloaded.")
        count += 1
        
    #download 'Excel report'
    sleep(2)
    # fetch page html content and find all hyperlinks with regex
    html_content_excel = driver.page_source
    regex_code_excel = '(?<=batches\/)(.*)(?=\/batchExcel)'
    regex_hyperlink = re.search(regex_code_excel, str(html_content_excel))

    base_excel = "https://aip.amsterdam.nl/api/batches/"
    end_excel = "batchExcel"
    # parse the hit on regex to only get numbered code
    parse_regex = regex_hyperlink.group().split("/")[-1]
    total_link_excel = os.path.join(base_excel, str(parse_regex) + "/", end_excel) 

    driver.get(total_link_excel)
    sleep(4)

    # wait till downloads ready
    download_check = os.listdir(path)
    
    # TODO: add check for file length
    while any(".crdownload" in file for file in download_check):
        sleep(1)
        download_check = os.listdir(path)

    end_time = datetime.now() - start_time

    return end_time


# function to get single bru from aip site
def single_data(driver, specific_bru, bru, path, start_time):
    # go to specific bru info page
    bru_info_tag = "//tbody/tr[" + str(specific_bru) + "]/td[1]"
    bru_data = find_by_xpath(bru_info_tag, driver)
    bru_data.click()
        
    # assign one window
    window_one = driver.window_handles[0]

    # open DMS
    dms_tag = "/html/body/span[1]/div[2]/div[1]/section[1]/header[1]/div[2]/a[1]"
    find_dms = find_by_xpath(dms_tag, driver)
    find_dms.click()

    # assign and handle window two
    window_dms = driver.window_handles[1]
    driver.switch_to.window(window_dms)

    # show all files in table
    select_all_tag = '//select[@name="documents_length"]/option[text()="All"]'
    select_all = find_by_xpath(select_all_tag, driver)
    select_all.click()

    #TODO: remove sleep() and make a better solution
    sleep(3)

    # fetch page html content and find all hyperlinks with regex
    html_content = driver.page_source
    regex_code = 'href="/documents/download/document/(.*?)"'
    regex_hyperlinks = re.findall(regex_code, str(html_content))

    # make folder for bru in batch directory
    path_bru = os.path.join(path, bru)
    os.mkdir(path_bru)

    # download all data
    for file in regex_hyperlinks:
        base = "https://bmidms.amsterdam.nl/documents/download/document/"
        total_link = os.path.join(base, file) 

        # get file
        driver.get(total_link)

        # TODO: check pathlength

        # wait till downloads ready
        download_check = os.listdir(path)
        while any(".crdownload" in file for file in download_check):
            sleep(1)
            download_check = os.listdir(path)
        
    # move all files to bru specific directory
    move_list = os.listdir(path)
    for files in move_list:
        fpath = os.path.join(path, files)
        if not os.path.isdir(fpath):
            if fpath.endswith(".tmp"):
                pass
            else:
                shutil.move(fpath, path_bru)

    # close window_dms
    # driver.quit()

    end_time = datetime.now() - start_time

    return end_time


if __name__ == "__main__":

    # start scraper by giving input
    url = "https://aip.amsterdam.nl"
    user = "h.p.j.h.p.m.kolen@iv-infra.nl"
    password = "7aB3E38rp!"
    batch = "19"
    folder = r"C:\programming\test_area"

    selenium_options = input_scraper(batch, folder)

    driver = version_find(selenium_options[0])

    if driver[1] == False:
        print("Your version of chrome is not found. Contact developer.")
    else:
        driver[0].get(url)

        brus_found = login(user, password, driver[0], selenium_options[2])

        if len(brus_found) == 0:
            print("Oops, loading objects failed. Try again.")
            driver[0].quit()
            exit()
        else:
            count = 1
            for bru in brus_found:
                # remove whitespace
                bru = bru.rstrip()

                # print all bru's found for selection
                sum_all_bru = str(count) + " :   " + str(bru)
                print(sum_all_bru)
                count += 1
            
            # get input that specifies which bru to find
            input_test = True
            while input_test:
                specific_bru = input("\nInput the integer number from list to select object: ")

                try:
                    specific_bru = int(specific_bru)
                except:
                    print("ERROR: Please input an integer value. An integer is a whole number without decimals.\n")

                # check input
                if isinstance(specific_bru, int):
                    input_test = False
                else:
                    print("\nInput is not recognized, specify the number from the object as listed above.")

            single_data(brus_found, driver[0], specific_bru, bru)
            
        sleep(6)

        driver[0].quit()





