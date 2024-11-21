from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from paddleocr import PaddleOCR
import base64

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