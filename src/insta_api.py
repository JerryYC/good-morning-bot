
import logging
logging.basicConfig(level=logging.INFO)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


SENDER_MESSAGE_CLASS = ' _ac1r _ac1w'
RECEIVER_MESSAGE_CLASS = ' _ac1q _ac1r _ac1v _ac1w'
class InstaDriver:
    def __init__(self, chrome_driver_path):
        option = webdriver.ChromeOptions()
        option.add_argument('--disable-blink-features=AutomationControlled')
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service = service, options=option)
        self.session = None
        logging.info("Driver Started")

    def login(self, username, password):
        try:
            self.driver.get('https://www.instagram.com/')
            WebDriverWait(self.driver, timeout=10).until(
                EC.presence_of_element_located((By.NAME, 'password')))
            logging.info("Logging In")
        except Exception as e:
            logging.error("Error Loading Login Page", e)
            return False
        
        try:
            username_field = self.driver.find_element(by=By.NAME, value='username')
            username_field.send_keys(username)
            password_field = self.driver.find_element(by=By.NAME, value='password')
            password_field.send_keys(password)
            password_field.submit()
            logging.info("Credential Submitted")
        except Exception as e:
            logging.error("Error Submitting Credential", e)
            return False
        
        try:
            WebDriverWait(self.driver, timeout=10).until(
                lambda driver: "accounts" in driver.current_url)
            logging.info("Login Successful")
        except Exception as e:
            logging.error("Login Failed", e)
            return False
        
        return True
    
    def open_chat(self, id):
        url = 'https://www.instagram.com/direct/t/{}'.format(id)
        logging.info("Redirect to Chat id: {}".format(id))
        self.driver.get(url)
        # wait for the page to load
        WebDriverWait(self.driver, timeout=60).until(
            EC.presence_of_element_located((By.XPATH, '//textarea')))
        logging.info("Chat page loaded")
        try:
            self.driver.find_element(By.XPATH, '//button[text()="Not Now"]').click()
        except:
            pass
        self.session = id
    
    def send_message(self, message):
        if self.session == None:
            logging.error("No Connected Chat")
            return
        text_box = self.driver.find_element(By.XPATH, '//textarea')
        text_box.send_keys(message)
        text_box.send_keys(Keys.ENTER)
        logging.info("Message Sent")

    def get_messages(self):
        elements = self.driver.find_elements(By.XPATH, "//div[@class='{}'] | //div[@class='{}']".format(SENDER_MESSAGE_CLASS, RECEIVER_MESSAGE_CLASS))
        ls = []
        for ele in elements:
            if ele.text:
                sender = 1 if ele.get_attribute("class") == RECEIVER_MESSAGE_CLASS else 0
                ls.append( (sender, ele.text) )
        return ls


    def shutdown(self):
        self.driver.close()
        logging.info("Driver Closed")