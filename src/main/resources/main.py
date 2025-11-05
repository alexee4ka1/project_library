from myFuncs import *
while 1:
    os.system('clear')
    print("Авторизация")
    print("Выберете вашу роль:")
    print("0. Читатель")
    print("1. Библиотекарь")
    if int(input())==1:
        print("Введите пароль")
        if str(input())==(open('src/main/resources/tochno_ne_parol.txt').readline()): menuLibrarian()
        else: print("Пароль неправильный")
    else:
        menuReader()