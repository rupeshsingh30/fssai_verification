from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import config
from api_captcha import get_captcha2
from db import dbConnection, insertQuery
from datetime import datetime


def open_url(chrome_driver, url):
    """Initialize the Chrome driver and open the given URL."""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    return driver


def fill_license_number(driver, license_number_value):

    try:
        license_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="content"]/div[1]/div/div[1]/div/div/form/div[4]/div/div[1]/input')
            )
        )
        license_input.send_keys(license_number_value)
        time.sleep(2)
    except Exception as e:
        print('fill license number :-',str(e))

        # return None

    # return True

def solve_and_input_captcha(driver, captcha_image_path):
    captcha_value = get_captcha2(driver, captcha_image_path)
    print("CAPTCHA Value: ", captcha_value)

    
    captcha_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/div[1]/div/div[1]/div/div/form/div[8]/div/div[2]/div/input')
        )
    )
    captcha_input.send_keys(int(captcha_value))
    time.sleep(2)


def click_search_button(driver):
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="content"]/div[1]/div/div[1]/div/div/form/button[1]')
        )
    )
    search_button.click()
    time.sleep(2)


def extract_table_data(driver):

    try:
        table = driver.find_element(By.ID, "data-table-simple")
        rows = table.find_elements(By.XPATH, ".//tbody/tr")
        # data_rows = []
        for row in rows:
            columns = row.find_elements(By.XPATH, ".//td")
            data = [col.text for col in columns]
            data.append(datetime.now())
            # data_rows.append(data)
            datetime.now()
    except Exception as e:
        print('exception handing :-',str(e))
        return None
    
    return data


def main():
    conn, cursor = dbConnection()
    chrome_driver = config.chrome_driver_path
    url = config.url
    input_excel = config.input_excel
    captcha_image_path = config.captcha_img


    # df = pd.read_excel(r'D:\Fssai\codes\details.xlsx')
    # list_license_number = df['fssai number'].tolist()
    df = pd.read_excel(input_excel)
    list_license_number = df['FSSAI License Number'].tolist()
    # list_license_number = [23322005000024]
    print(list_license_number,">>>>>>")

    try:
        driver = open_url(chrome_driver, url)
    except Exception as e:
        print("driver issue :-",str(e))
        return None

    for license_number in list_license_number:
        print(str(license_number),">>>>>>>")

        license_number = str(license_number)

        # Fill license number
        fill_license_number(driver, license_number)
        print('filled license number unsuccessfully')
         
        #input CAPTCHA
        solve_and_input_captcha(driver, captcha_image_path)

        # Click search button
        click_search_button(driver)

        # Extract and store table data
        data_rows = extract_table_data(driver)
        print(data_rows,">>>>")



        if data_rows == None: 
            not_found_data = ['','','',license_number,'','not found',datetime.now()]
            insertQuery(conn, cursor, not_found_data)
            driver.refresh()
            continue

        
        insertQuery(conn, cursor, data_rows)

        time.sleep(2)

        driver.refresh()
        time.sleep(2)

    driver.quit()

if __name__ == "__main__":
    main()



