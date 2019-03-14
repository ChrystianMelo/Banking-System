#                                                                  Bank System
#                                                         ~Developed by Chrystian Melo ~
import os
import os.path
import matplotlib.pyplot  as plt

#Global Variables
qttparameters = 3#quantity of parameters needed to User()

#Classes
class User():
    def __init__(self,name,value,cpf):
        self.name = name#name
        self.value = value#value in the account
        self.cpf = cpf#this variable will be usd to find the users
class Account():
    def __init__(self, user):
        self.user = user#primary user

#Some functions that will e useable during the code
def searchCPF(acc, cpf):
    i = 0
    while i < len(acc):
        if acc[i].user.cpf == cpf:
            return i+1#Only return 0 when happens some error..OBS:When I receive this return I will undo this operation
        else:
            i+=1
    return 0#not found
def mainMenu():
    print("\n\t\t\t\t\tWelcome to BMC Bank!!")
    try :
        answ = int(input("Options:\n 1) Create a new bank account\n 2) Consult my bank account\n 7) Sair\n..:"))
        return answ
    except ValueError:
        print("Oops! That's not a valid number. Try again")
    return 0
def addFile(accounts):
    i = 0
    file = open("data.txt", "w")
    while i < len(accounts):
        x = str(accounts[i].user.name).rstrip()#removing all the \n existants SOLVING ERROR
        file.write(x+"\n")
        file.write(str(accounts[i].user.value)+"\n")
        file.write(str(accounts[i].user.cpf)+"\n")
        i+=1
    file.close()
def loadFile():
    acc = []
    if(os.path.exists("data.txt")):
        i = 1
        file = open("data.txt", "r")
        st = file.readlines()
        while i < len(st):
            a = Account(User(str(st[i-1]), int(st[i]), int(st[i+1])))
            acc = acc + [a]
            i+=qttparameters
        file.close()
        os.remove("data.txt")
    return acc
def sort(alist):
    for fillslot in range(len(alist)-1,0,-1):
       positionOfMax=0
       for location in range(1,fillslot+1):
           if int(alist[location])>int(alist[positionOfMax]):
               positionOfMax = location

       temp = int(alist[fillslot])
       alist[fillslot] = alist[positionOfMax]
       alist[positionOfMax] = temp
def graphPloter(x,y):
    plt.plot(x,y)#x, y
    plt.title('UserxValue')
    plt.xlabel('Id_Users')#X
    plt.ylabel('ValueR$')#Y
    plt.show()#Show

accounts = loadFile()#This vector will contain all of the BMC bank's accounts
answ = mainMenu()#openning the menu
while answ != 7:
    #OPTION 1: allocing/reallocing the quantity of accounts
    if answ == 1:
        a=Account(User(str(input("Name..:")), int(input("Value..:")), int(input("CPF..::"))))
        accounts = accounts + [a]#allocing the new account in the array of all accounts
    #OPTION 2:
    if answ == 2:
        if len(accounts) != 0:
            cpf = int(input("What's the 'CPF' of the user that you want to consult?\n..:"))#variable to search
            ok = searchCPF(accounts, cpf)
            if ok != 0:
                ok = ok - 1#Undoing what I did in searchCPF to not return 0(line 19)
                print("We found the account!")
                print("Name => ", accounts[ok].user.name)
                print("Value in the bank account = R$ ", accounts[ok].user.value)
            else:
                print("There is no user with this 'CPF'!\n")
        else:
            print("There is no users in this bank yet!\n")
    answ = mainMenu()
valuesRS = ['0']#vector of values in the bank
valuesCPF = ['0'] #quantitiy of values
i=0
#Get all the valors in the bank and put in the vector
while i < len(accounts):
    valuesRS += str(accounts[i].user.value)#valuesR$
    valuesCPF += str(accounts[i].user.cpf)#idCPF
    i+=1
sort(valuesCPF)
graphPloter(valuesCPF,valuesRS)
addFile(accounts)
