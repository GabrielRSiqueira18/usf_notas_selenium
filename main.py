import sys
from src.Selenium import Selenium


def main():
    selenium = Selenium('https://www.usf.edu.br/apps/portal2/login')

    logged = selenium.login('202205327', 'Gabriel1')

    if not logged:
        print('Ra ou Senha inválido!!!')
        sys.exit(1)

    if logged:
        x = selenium.get_avatar()
        print(x)

if __name__ == '__main__':
    sys.exit(main())
