import sys
from src.Selenium import Selenium


def main():
    selenium = Selenium('https://www.usf.edu.br/apps/portal2/login')

    logged = selenium.login('202205328', 'Gabriel1')

    if not logged:
        print('Ra ou Senha inválido!!!')
        sys.exit(1)

    if logged:
        selenium.enter_in_materials()

if __name__ == '__main__':
    sys.exit(main())
