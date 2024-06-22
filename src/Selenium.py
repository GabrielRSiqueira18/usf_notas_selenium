import sys

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

    def __get_subject_element(self, subject: str):
        subject = subject.lower()
        tr_target = None

        css_selector = f'tr[valign="middle"]'

        tr_elements = self.find_elements(By.CSS_SELECTOR, css_selector)

        for tr in tr_elements:
            td_elements = tr.find_elements(By.TAG_NAME, 'td')

            for td in td_elements:
                if subject in td.text.lower():
                    tr_target = tr
                    break

            if tr_target is not None:
                break

        return tr_target

    def __get_subject_table(self, subject: str):
        try:
            element = self.__get_subject_element(subject)

            if element is None:
                print("Matéria não encontrada!!!")
                sys.exit(1)

            button_to_get_notes = element.find_element(By.CLASS_NAME, 'btn')
            button_to_get_notes.click()

            wait = WebDriverWait(self, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-body')))

            tables = self.find_elements(By.CLASS_NAME, 'modal-body')

            for table in tables:
                tbody_element = table.find_element(By.CSS_SELECTOR, 'tbody')

                for tr in tbody_element.find_elements(By.CSS_SELECTOR, 'tr'):
                    for td in tr.find_elements(By.CSS_SELECTOR, 'td'):
                        if subject.lower() in td.text.lower():
                            return table

        except Exception as e:
            print(f"Erro encontrado: {e}")
            return None

    def get_note(self, subject: str):
        rows_target = []

        table_target = self.__get_subject_table(subject)

        if table_target is None:
            print("Matéria não encontrada!!!")
            sys.exit(1)

        for tr in table_target.find_elements(By.CSS_SELECTOR, 'tr'):
            for td in tr.find_elements(By.CSS_SELECTOR, 'td'):
                if 'NOTA' in td.text or 'MÉDIA' in td.text:
                    rows_target.append(tr)

        for row in rows_target:
            tds = row.find_elements(By.CSS_SELECTOR, 'td')

            if len(tds) >= 2:
                title = tds[1].text.strip()
                note = tds[2].text.strip()

                if title and note:
                    print(f'{title}: {note}')

