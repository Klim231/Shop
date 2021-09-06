from SQLiter import Keys
from random import choice

db = Keys('main.db')
mass = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i','o','p']
num = 0
while num <= 99:
    key = []
    p = 0
    while p <= 5:
        key.append(str(choice(mass)))
        p+=1
    print(''.join(key))
    if db.chek_keys(''.join(key)) == True:
        db.write_keys(''.join(key))
        num+=1



