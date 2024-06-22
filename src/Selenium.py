from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Selenium(webdriver.Chrome):
    def __init__(self, url: str):
        self.__service = Service()
        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument('--headless')
        self.__options.add_argument('--disable-gpu')

        super().__init__(service=self.__service, options=self.__options)

        self.get(url)

    def login(self, ra: str, password: str):
        ra_field = self.find_element(By.ID, 'matricula')
        password_field = self.find_element(By.ID, 'senha')

        ra_field.send_keys(ra)
        password_field.send_keys(password)

        login_button = self.find_element(By.CLASS_NAME, 'btn-enviar-itf')
        login_button.click()

        try:
            element_pos_login = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'avatar-usf'))
            )

            if element_pos_login:
                return True

        except:
            return False

    def get_avatar(self):
        try:
            element_pos_login = WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'avatar-usf'))
            )

            return element_pos_login

        except Exception as e:
            print(e)
            return None
