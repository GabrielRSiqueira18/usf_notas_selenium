import sys
import time

from src.Selenium import Selenium


def main():
    selenium = Selenium('https://www.usf.edu.br/apps/portal2/login')

    ra = input("Digite seu RA: ")
    password = input("Digite sua senha: ")

    logged = selenium.login(ra, password)

    if not logged:
        print('Ra ou Senha inválido!!!')
        sys.exit(1)

    entered = selenium.enter_in_materials()

    if not entered:
        print('Não foi possível entrar no resumo acadêmico! ')

    subject = input('Digite o nome da matéria: ')

    selenium.get_note(subject)

    time.sleep(30)


if __name__ == '__main__':
    sys.exit(main())
