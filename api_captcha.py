from selenium import webdriver
from selenium.webdriver.common.by import By
import time,os
from selenium.webdriver.support.ui import  WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import openpyxl,re
import time
from datetime import datetime
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from python_anticaptcha import AnticaptchaClient, ImageToTextTask

from paddleocr import PaddleOCR
import base64
import requests,json

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode('utf-8')
    except Exception as e:
        print(f"Error: {e}")
        return None

# # Example usage:
# image_path = "path/to/your/image.jpg"
# base64_image = image_to_base64(image_path)
# if base64_image:
#     print("Base64 representation of the image:")
#     print(base64_image)


def get_captcha(driver,path):

    ele = driver.find_element(By.XPATH, value='//*[@id="content"]/div[1]/div/div[1]/div/div/form/div[8]/div/div[1]/p/img')  

    ele.screenshot(path)

    captcha_fp = open(path, 'rb')

    client = AnticaptchaClient("b2b510888e9324fdf42975d81168b15a")

    task = ImageToTextTask(captcha_fp)

    job = client.createTask(task)

    job.join()

    c1 = job.get_captcha_text()

    captcha_fp.close()

    os.remove(path)

    return c1

"""
This Python function captures an image of a captcha on a webpage, converts it to base64, sends it to
a specified API endpoint for processing, and returns the captcha text.

:param driver: The `driver` parameter in the `get_captcha1` function is typically an instance of a
web driver, such as Selenium WebDriver, that allows you to interact with a web browser in an
automated way. You can use this driver to find elements on a web page, interact with them, and
:param path: The `path` parameter in the `get_captcha1` function is the file path where the
screenshot of the captcha image will be saved before sending it for processing. It is used as an
input to the `screenshot` method to save the image of the captcha displayed on the webpage
:return: The function `get_captcha1` returns the value of the 'Captcha' key from the JSON response
data.
"""
def get_captcha1(driver,ss_path):

    ele = driver.find_element(By.XPATH, value='//*[@id="content"]/div[1]/div/div[1]/div/div/form/div[8]/div/div[1]/p/img')  
    ele.screenshot(ss_path)

    url = "https://sequelpythonapps.azurewebsites.net/api/captcha/d?code=mu3llrtj1HD2J4GjFvW3f5Tcgnv-cNEXVOKsDOOp0AzXAzFuvXOuYQ=="

    base64str = image_to_base64(ss_path)
    
    sample = {
    "file": f"data:image/png;base64,{base64str}"}
    
    json_data = json.dumps(sample)

    response = requests.post(url, data=json_data, headers={"Content-type":"application/json"})
    print(response)
    data = response.json()
    print(data)
    # json_str = json.dumps(data, indent=4)
    # print(json_str)
    # time.sleep(20)


    # os.remove(ss_path)
    # time.sleep(3)

    # return data['Captcha']
    return data




def get_captcha2(driver, path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
    ele = driver.find_element(By.XPATH, value='//*[@id="content"]/div[1]/div/div[1]/div/div/form/div[8]/div/div[1]/p/img')
    ele.screenshot(path)
    try:
        result = ocr.ocr(path, det=False, cls=False)
        result = result[0][0][0]
    except:
        result = ''
        
    # os.remove(path)
    # result = 444444
    return result