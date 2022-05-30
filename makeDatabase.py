import random

f = open('database.txt', 'r')
base = eval(f.read())
f.close()

database = []

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
unitCodes = []

for i in range(50):
    newCode =''
    unique = True
    for l in range(3):
        newCode = newCode + random.choice(letters)
    for l in range(4):
        newCode = newCode + str(random.randint(0,9))
    for l in unitCodes:
        if newCode == l:
            unique = False
    if unique:
        unitCodes.append(newCode)
    else:
        i -= 1
            
print("codes generated" )

RorM = input("1. Random\n2. Manual\n")
rand = False
if RorM == '1':
    rand = True

for i in range(20):
    #name = input("Full name: ")
    name = base[i]['f_name']
    #ID = input("Student ID: ")
    ID = base[i]['id']
    #password = input("Password: ")
    password = base[i]['password']
    newData = {"f_name":name, 'id':ID, 'password':password}
    for j in range(random.randint(12, 30)):
        while True:
            code = random.choice(unitCodes)
            if code in newData:
                continue
            print(code)
            scores = [None, None, None]
            newScore = 0
            count = 1
            if rand:
                while newScore < 50:
                    print("attempt", count)
                    if i == 0: #CA-01
                        newScore = round(random.uniform(70,100),2)
                    elif i == 1:#CA-02
                        if j < 8: # top 8 > 80
                            newScore = round(random.uniform(80,85),2)
                        else:
                            newScore = round(random.uniform(65,70),2)
                    elif i == 2:#CA-03
                        newScore = round(random.uniform(65,70),2)
                    elif i == 3:#CA-04
                        if j < 8: # top 8 > 80
                            newScore = round(random.uniform(80,85),2)
                        else:
                            newScore = round(random.uniform(60,65),2)
                    elif i == 4:#CA-05
                        newScore = round(random.uniform(60,65),2)
                    elif i == 5:#CA-06
                        newScore = round(random.uniform(50,60),2)
                    elif i == 6:#CA-07
                        if j < 3:#>6 fails
                            newScore = round(random.uniform(0,50),2)
                        else:
                            newscore = round(random.uniform(40,100),2)
                    else:
                        newScore = round(random.uniform(40,100),2)
                    if count == 3 and newScore < 50:
                        newScore = newScore + 50
                    scores[count-1] = newScore
                    count += 1
            else:
                while int(newScore) < 50:
                    print("attempt", count)
                    newScore = input("grade: ")
                    if count == 3 and float(newScore) < 50:
                        newScore = str(float(newScore) + 50)
                    scores[count-1] = newScore
                    count += 1
            newData[code] = scores
            break
    database.append(newData)

print(database)
f = open("database.txt", "w")
f.write(str(database))
f.close()
