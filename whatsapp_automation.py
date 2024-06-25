from selenium import webdriver # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
import time
import pickle
import os

# Path to your ChromeDriver executable
chrome_driver_path = r"C:\Users\jaina\Desktop\Project\JARVIS\chromedriver.exe"

def init_whatsapp():
    service = Service(chrome_driver_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com/")

    cookies_file = "whatsapp_cookies.pkl"
    if os.path.exists(cookies_file):
        with open(cookies_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(5)
    else:
        input("Scan the QR code and press Enter to continue...")
        with open(cookies_file, "wb") as f:
            pickle.dump(driver.get_cookies(), f)

    return driver

def send_message(driver, contact_name, message):
    try:
        search_box = driver.find_element("xpath", '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(contact_name)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)
        message_box = driver.find_element("xpath", '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Failed to send message: {e}")



if __name__ == "__main__":
    driver = init_whatsapp()
    send_message(driver, "Contact Name", "Hello, this is a test message!")
    
