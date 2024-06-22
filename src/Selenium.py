from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


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
            element_pos_login = WebDriverWait(self, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'avatar-usf'))
            )

            if element_pos_login:
                return True

        except:
            return False

    def enter_in_materials(self):
        try:
            hover_element = self.find_element(By.CLASS_NAME, "icone-Acadêmico")

            actions = ActionChains(self)
            actions.move_to_element(hover_element).perform()

            link_selector = '.menu1 ul li a'
            links = self.find_elements(By.CSS_SELECTOR, link_selector)

            for link in links:
                href = link.get_attribute('href')
                if href == 'https://www.usf.edu.br/apps/portalaluno2/notashistorico':
                    try:
                        # Tenta clicar no link
                        link.click()
                    except Exception:
                        # Se o clique normal falhar, usa JavaScript
                        self.execute_script("arguments[0].click();", link)
                    break

            WebDriverWait(self, 10).until(
                EC.presence_of_element_located((By.ID, 'fonte_linha_cabecalho'))
            )
            print("Navegação bem-sucedida")
            return True

        except Exception as e:
            print(f"Erro ao navegar para o link de materiais: {e}")
            return False
