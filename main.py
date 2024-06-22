import sys
from src.Selenium import Selenium


def main():
    selenium = Selenium('https://www.usf.edu.br/apps/portal2/login')

    logged = selenium.login('202205328', 'Gabriel1')

    if not logged:
        print('Ra ou Senha inválido!!!')
        sys.exit(1)

    entered = selenium.enter_in_materials()

    if not entered:
        print('Não foi possível entrar no resumo acadêmico! ')

    selenium.get_note("engenharia de software")

if __name__ == '__main__':
    sys.exit(main())
