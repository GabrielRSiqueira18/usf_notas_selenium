import sys
from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    service = Service()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=service, options=options)

    url = 'https://www.usf.edu.br/apps/portal2/login'
    driver.get(url)

    username_field = driver.find_element(By.ID, 'matricula')
    password_field = driver.find_element(By.ID, 'senha')

    username_field.send_keys('202205328')
    password_field.send_keys('Gabriel1')

    login_button = driver.find_element(By.CLASS_NAME, 'btn-enviar-itf')
    login_button.click()

    try:
        element_pos_login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'avatar-usf'))
        )
        print("Login bem-sucedido")
    except Exception as e:
        print("Falha no login")
        print(e)

    driver.quit()

if __name__ == '__main__':
    sys.exit(main())
