# import packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime, date
import re, os, shutil

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
check the webdriver version before running this script. 
Make sure the driver has the same name and version as the browser of the user.

Default browser and version:    Chrome; version 95
Default driver:                 chromedriver.exe (for version 95)

Check your browser version: 'help' -->  'About Google Chrome'

If the version differs from the default version used by this tool, than download the driver for the verion used by your machine here:
https://chromedriver.chromium.org/downloads

Replace the driver with the correct chromedriver.exe in the driver folder
"""

# start timing
start_time = datetime.now()

# ask for login as input and batch number
user = input("User email to login to AIP system: ")
password = input("Password to login to AIP system: ")
batch = input("Enter batch number: ")
folder = input("Input directory for batch destination: ")
driver_url = "https://aip.amsterdam.nl"

# add function to select single bru instead of full batch
# single download or total download
choose_options = input("Do you want to download the whole batch? (Y/N): ")
if choose_options.upper() == "Y":
    single_download = False
elif choose_options.upper() == "N":
    single_download = True
else:
    print("Input option was incorrect, restart program.")
    exit()

# check and create batch folder with error handeling for duplicates
dupl = 0
batch_name = "Batch " + str(batch)
for file in os.listdir(folder):
    if batch_name in file:
        dupl += 1

today = date.today()
d = today.strftime("%d-%m-%y")

batch_name = batch_name + "_v" + str(dupl) + "_" + str(d)
path = os.path.join(folder, batch_name)

# set chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1366,768')
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--start-maximized')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# add directory preference
prefs = {}
os.makedirs(path)
prefs["profile.default_content_settings.popups"]=0
prefs["download.default_directory"]=path
chrome_options.add_experimental_option("prefs", prefs)

# connect to driver with selenium
PATH = 'driver//chromedriver.exe'
driver = webdriver.Chrome(executable_path=PATH, options=chrome_options)
driver.get(driver_url)

## functions
# find an element bij id
def find_by_id(elem_id, webdriver):
    # explicit wait for browser to load
    try:
        WebDriverWait(webdriver, 15).until(
            EC.presence_of_all_elements_located((By.ID, elem_id))
        )
    except:
        print("ERROR: Either loading time is taking longer than expected or ID not found")
    
    find_id = webdriver.find_element(By.ID, elem_id)

    return find_id

def find_by_xpath(elem_xpath, webdriver):
    try:
        WebDriverWait(driver, 25).until(
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
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, elem_class_name))
        )
    except:
        print("ERROR: Either loading time is taking longer than expected or class name not found")

    # search for batch info and get object info
    find_class_name = webdriver.find_element(By.CLASS_NAME, elem_class_name)

    return find_class_name

def wait_for_class_name(elem_class_name):
    # explicit wait
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, elem_class_name))
        )
    except:
        print("ERROR: Either loading time is taking longer than expected or class name not found")


## Tie together
# login tags for ID element find
login_user_tag = "useremail"
login_pass_tag = "password"
# login
user_inp = find_by_id(login_user_tag, driver)
user_inp.send_keys(user)
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
searchbar_find.send_keys("Batch " + str(batch))
searchbar_find.send_keys(Keys.ENTER)

# go to batch
batch_info_tag = "nowrap"
batch_info_navigate = find_by_class_name(batch_info_tag, driver)
batch_info_navigate.click()

# collect bru's
bru_table_tag = 'table table-condensed table-hover'
html_regex_bru = 'tr class="bg-white" style="cursor: default;"><td class="" style="cursor: pointer;">(.*?)</td'
bru_info_find = wait_for_class_name(bru_table_tag)
html_content_page = driver.page_source
regex_tables = re.findall(html_regex_bru, str(html_content_page))
# check if bru's are found
if len(regex_tables) == 0:
    print("""
        Loading the table with the list of batch objects did not work.
        Try running this tool again on a faster machine or a faster internet connection
        """)
    exit()

# function tp loop through all bru's and collect data
def all_data(regex_tables, driver):
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
        sleep(3)

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

        #go back one
        driver.back()

        # print update on download progress
        print("(" + str(count) + "/" + str(len(regex_tables)) + "): " + "From " + str(batch_name) + " and object " + str(bru) + " there where " + str(len(regex_hyperlinks)) + " files downloaded.")
        count += 1

    #TODO: download 'Excel report'
    excel_export_tag = '//*[@id="objectlist"]/div[1]/div/a[2]'
    excel_report = find_by_xpath(excel_export_tag, driver)
    excel_report.click()

# function to get single bru from aip site
def single_data(regex_tables, driver):
    count = 1
    for bru in regex_tables:
        # remove whitespace
        bru = bru.rstrip()

        # print all bru's found for selection
        sum_all_bru = str(count) + " :   " + str(bru)
        print(sum_all_bru)
        count += 1
    
    # get input that specifies wich bru to find
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

    #go back one
    driver.back()

    # print update on download progress
    print("(" + str(specific_bru) + "/" + str(len(regex_tables)) + "): " + "From " + str(batch_name) + " and object " + str(bru) + " there where " + str(len(regex_hyperlinks)) + " files downloaded.")


# make selection for complete bru download or single bru selection
if single_download == False:
    all_data(regex_tables, driver)
elif single_download == True:
    single_data(regex_tables, driver)

# delete user login data
del user
del password
print("\nDownloading has completed, and it took this long:")
print(datetime.now() - start_time)
print("\n!__you can close this terminal now__!\n")
print("ლ ( ◕  ᗜ  ◕ ) ლ\n")

# quit and shut down driver
driver.quit()




