from myFuncs import *
while 1:
    os.system('clear')
    print("Авторизация")
    print("Выберете вашу роль:")
    print("1. Читатель")
    print("2. Библиотекарь")
    if int(input())==1:
        menuReader()
    else:
        menuLibrarian()