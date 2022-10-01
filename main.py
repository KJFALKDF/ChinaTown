# This is a sample Python script.
import os
import random
import json

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
state = ['空', '地', '房', '学', '医', '警', '消', '花', '草']
costs = [0, 0, 20, 40, 40, 50, 50, 5, 2]


def hash(n: str):
    res = 1

    for c in n:
        cn = ord(c)
        digits = 8
        if cn >= 256:
            digits += 8
        if cn >= 65536:
            digits += 8
        res = (res << digits) + cn

    res = pow(res, 65537, 2147483647)
    return res


def register():
    # Name enter and check
    username = ''
    while True:
        print('Please enter your name: ')
        username = input()
        if not username in citizens:
            break
        print('Name occupied. ')
        print('1. Retry')
        print('Other. Exit')
        choice = input()
        if choice != '1':
            return

    # Password enter, confirm and check
    pwd = ''
    while True:
        print('Please enter your password: ')
        pwd = input()
        print('Please confirm your password: ')
        pwd2 = input()
        if pwd == pwd2:
            break
        print('Passwords are different. ')
        print('1. Retry')
        print('Other. Exit')
        choice = input()
        if choice != '1':
            return

    # Do register process
    citizens[username] = {
        'pwd': hash(pwd),
        'offsetX': 0,
        'offsetY': 0,
        'lengthX': 3,
        'lengthY': 3,
        'field': [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        'deposit': 0
    }
    moveIn(username)
    print('Register success! ')
    return menu(username)


def login():
    # name enter and check
    username = ''
    while True:
        print('Please enter your name: ')
        username = input()
        if username in citizens:
            break
        print('Unknown name! ')
        print('1. Retry')
        print('Other. Exit')
        choice = input()
        if choice != '1':
            index()

    # password enter and check
    print(f'Welcome back, {username}.')
    pwd = ''
    pHash = citizens[username]['pwd']
    while True:
        print('Please enter your password: ')
        pwd = input()
        if hash(pwd) == pHash:
            break
        print('Password incorrect! ')
        print('1. Retry')
        print('Other. Exit')
        choice = input()
        if choice != '1':
            return None

    # Login
    print(f'Logged in as {username}. ')
    return menu(username)


def index():
    print("Welcome to Cyber Town")
    print("1. Login Your Role")
    print("2. Creat Your Role")
    choice = input()
    if choice == "1":
        login()
    elif choice == "2":
        register()
    else:
        print("Input Error")

def menu(username):
    save()
    print("welcome to your estate")
    print("1. Check your Property")
    print("2. Decorate your Property")
    print("3. Enter the Town")
    print("Other. Log out")
    menu_choice = input()
    if menu_choice == "1":
        check(username)
        print("Press Enter to go back...")
        input()
        return menu(username)
    elif menu_choice == "2":
        decorate(username)
    elif menu_choice == "3":
        view(username)
    else:
        index()


def check(username):
    print(f'''Deposit: {citizens[username]['deposit']}
Land: ''')
    landstr = ''
    for i in range(citizens[username]['lengthX']):
        for j in range(citizens[username]['lengthY']):
            landstr += state[citizens[username]['field'][i][j]] + ' '
        landstr += '\n'
    print(landstr)


def decorate(username):
    rows, columns = citizens[username]['lengthX'], citizens[username]['lengthY']
    ttlCost = 0
    matrix = []
    flag = True
    while flag:
        ttlCost = 0
        flag = False
        matrix = []
        print("Enter the %s x %s matrix:" % (rows, columns))
        print(f'''1: Land  Cost: {costs[1]}
2: House  Cost: {costs[2]}
3: School  Cost: {costs[3]}
4: Hospital  Cost: {costs[4]}
5: Police Station  Cost: {costs[5]}
6: Fire Station  Cost: {costs[6]}
7: Flower  Cost: {costs[7]}
8: Grass  Cost: {costs[8]}''')
        for i in range(rows):
            matrix.append(list(map(int, input().rstrip().split(" "))))
        for i in range(rows):
            for j in range(min(columns, len(matrix[i]))):
                if not flag:
                    if 0 < matrix[i][j] < 9:
                        if matrix[i][j] != citizens[username]['field'][i][j]:
                            ttlCost += costs[matrix[i][j]]
                    else:
                        print("Error Input, Please Try again")
                        flag = True

    print(ttlCost)
    if ttlCost <= citizens[username]['deposit']:
        citizens[username]['deposit'] -= ttlCost
        print("Congratulation, New Decoration Saved")
        for i in range(rows):
            for j in range(columns):
                citizens[username]['field'][i][j] = matrix[i][j]
                town[citizens[username]['offsetX'] + i][citizens[username]['offsetY'] + j]['field'] = matrix[i][j]
        view(username)
    else:
        print("Sorry, you are too poor to afford this, please try again")
        decorate(username)

def moveIn(username):
    flag = True
    x, y = 0, 0
    while flag:
        flag = False
        x = int(input("Enter number of rows in the matrix:"))
        y = int(input("Enter number of columns in the matrix:"))

        for i in range(3):
            for j in range(3):
                if town[x + i][y + j]['field'] != 0:
                    if not flag:
                        print("Invalid field! ")
                        flag = True

    citizens[username]['offsetX'] = x
    citizens[username]['offsetY'] = y
    deposit = 0
    for i in range(3):
        for j in range(3):
            town[x + i][y + j]['field'] = 1
            deposit += town[x + i][y + j]['value']

    citizens[username]['deposit'] += deposit
    return


def view(username):
    res = ''
    for i in range(len(town)):
        for j in range(len(town[i])):
            res += state[town[i][j]['field']] + ' '
        res += '\n'
    print(res)

    choice = input("Press Enter to continue")
    return menu(username)


def save():
    obj = {'citizens': citizens, 'town': town}
    json_obj = json.JSONEncoder().encode(obj)
    with open('savedata.town', 'w') as f:
        f.write(json_obj)


def load():
    cs = {}
    ts = []
    if not os.path.exists('savedata.town'):
        for i in range(15):
            ts.append([])
            for j in range(15):
                ts[i].append({'field': 0, 'value': random.randint(1, 10)})
        with open('savedata.town', 'w') as f:
            pass
        return cs, ts

    with open('savedata.town', 'r') as f:
        json_obj = f.read()
        obj = json.JSONDecoder().decode(json_obj)
        cs = obj['citizens']
        ts = obj['town']

    return cs, ts


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    citizens, town = load()
    save()
    index()
