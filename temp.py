#                                                                  Bank System
#                                                         ~Developed by Chrystian Melo ~
import os
import os.path
import matplotlib.pyplot  as plt
from datetime import date
import time

#Global Variables
qttparameters = 4#quantity of parameters needed to User()

#Classes
class User():
    def __init__(self,name,value, cpf, paswd):
        self.name = name#name[string]
        self.value = value#value in the account[int]
        self.cpf = cpf#this variable will be usd to find the users[int]
        self.paswd = paswd#password[string]
class Account():
    def __init__(self, user):
        self.user = user#primary user

#Some functions that will e useable during the code
def searchCPF(acc, cpf):
    i = 0
    while i < len(acc):
        if int(acc[i].user.cpf) == cpf:
            return i+1#Only return 0 when happens some error..OBS:When I receive this return I will undo this operation
        i+=1
    return 0#not found
def addFile(accounts):
    file = open("data.txt", "w")
    for i in range(0, len(accounts)):
        name = str(accounts[i].user.name).rstrip()#removing all the \n existants SOLVING ERROR
        passwd = str(accounts[i].user.paswd).rstrip()
        file.write(name+"\n")
        file.write(str(accounts[i].user.value)+"\n")
        file.write(str(accounts[i].user.cpf)+"\n")
        file.write(passwd+"\n")
    file.close()
def loadAccounts():
    acc = []
    if(os.path.exists("data.txt")):
        i = 1
        file = open("data.txt", "r")
        st = file.readlines()
        while i < len(st):
            a = Account(User(str(st[i-1]), int(st[i]), int(st[i+1]), str(st[i+2])))
            acc = acc + [a]
            i+=qttparameters
        file.close()
        os.remove("data.txt")
    return acc
def loadBankDrive(name):
    drive = []
    if(os.path.exists(name)):
        file = open(name, "r")
        st = file.readlines()
        for i in range(0, len(st)):
            drive.append(int(st[i]))#money
        file.close()
        os.remove(name)
    return drive
def addBankDrive(name,data):
    file = open(name, "w")
    for i in range(0, len(data)):
        file.write(str(data[i])+"\n")
    file.close()    
def login(data):#this function will foward the logic to option()
    print("\n\t\t\t\t\tWelcome to BMC Bank!!")
    try:
        cpf = int(input("Cpf.:"))
        search = searchCPF(data, cpf)
        if search != 0: #There is a user
            search -= 1#Undoing what i did to confirm in SearchCPF funcion
            paswd = str(input("Password.:"))
            print("User->",data[search].user.paswd.strip('\n') ,"Pass->", paswd)
            if data[search].user.paswd.strip('\n') == paswd:#passw digited is equal to passwd of user x
                print("\n\t\tWelcome ", data[search].user.name.strip(),"!!")
                try :
                    answ = int(input("Options:\n 1) Consult my bank account\n 2) Delete my account\n 3) Add Money\n 4) Remove Money\n.:"))
                except ValueError:
                    print("Oops! That's not a valid option. Try again")
                options(answ, data, search)
            else:
                print("Wrong Password!!")
                addFile(data)
                return 1#Killing the process
        else:#There is no user with this cpf
            print("No user!")
            options(0, data, 0)#adding a new user
    except ValueError:
        print("Oops ! \n You can only add number in this camp.")
def sort(alist):
     for position in range(len(alist)-1,0,-1):
       positionOfMax=0
       for location in range(1,position+1):
           if int(alist[location])>int(alist[positionOfMax]):
               positionOfMax = location
       temp = int(alist[position])
       alist[position] = alist[positionOfMax]
       alist[positionOfMax] = temp
def options(op, accounts, ident):#ident will be used in a specific case
    if op == 0:#No  user in this CPF
        print("We did not found a account with this CPF number. Create a new account here..:")
        acNEW= Account(User(str(input("Name..:")), 0, int(input("CPF..::")), str(input("Password..:"))))
        accounts.append(acNEW)#allocing the new account in the array of all accounts
        print("Account creeated successfully!")
    if op == 1:
        print("\nMr(s) ", accounts[ident].user.name, "\nThe value in your bank account is R$ ", accounts[ident].user.value)
        x = []
        y = []
        bankdrive = loadBankDrive(str(str(accounts[ident].user.cpf)+".txt"))
        addBankDrive(str(str(accounts[ident].user.cpf)+".txt"),bankdrive)
        for i in range(0,len(bankdrive)):
            if i % 2 == 0 or i==0:#par = mes
                y.append(int(bankdrive[i]))
            else:
                x.append(int(bankdrive[i]))
        graphPloter(x,y)
    if op == 2:
        if len(accounts) != 0:
            cpf = int(input("What's the 'CPF' of the user that you want to consult?\n..:"))#variable to search
            ok = searchCPF(accounts, cpf)
            if ok !=  0:
                ok = ok - 1#Undoing what I did in searchCPF to not return 0(line 19)
                accounts.remove(accounts[ok])
                print("Account deleted")
            else:
                print("There is no user with this 'CPF'!\n")
        else:
            print("There is no users in this bank yet!\n")
    if op ==3:
        add = int(input("How much do you want to add in your account?  ->"))
        accounts[ident].user.value+= add
        print("\nMr(s) ", accounts[ident].user.name, "\nThe value in your bank account is R$ ", accounts[ident].user.value)
        bankdrive = loadBankDrive(str(str(accounts[ident].user.cpf)+".txt"))#readind file(cpf.txt)
        bankdrive.append(add)#how much has been added
        #bankdrive.append(time.localtime(time.time()).tm_min)#just testing cuz month take too long
        bankdrive.append(date.today().month)#date adding money
        addBankDrive(str(str(accounts[ident].user.cpf)+".txt"), bankdrive)#writig file
    if op == 4:
        rm = int(input("How much do you want to remove from your account?  ->"))
        if rm <= accounts[ident].user.value:
            accounts[ident].user.value-=rm
        else:
            print("Sorry!\n You do not have money enough to remove...")
        print("\nMr(s) ", accounts[ident].user.name, "\nThe value in your bank account is R$ ", accounts[ident].user.value)
        bankdrive = loadBankDrive(str(str(accounts[ident].user.cpf)+".txt"))#cpf.txt
        bankdrive.append(rm*-1)# Add "-3" in file
        #bankdrive.append(time.localtime(time.time()).tm_min)#just testing cuz month take too long
        bankdrive.append(date.today().month)#date adding money
        addBankDrive(str(str(accounts[ident].user.cpf)+".txt"), bankdrive)
    addFile(accounts)#saving data
    return 0
def graphPloter(x,y):
    plt.plot(x,y)#vet(x), vet(y)
    plt.title('Anual Bank Drive')
    plt.xlabel('Date')#X
    plt.ylabel('ValueR$')#Y
    plt.show()#Show

#main
answ = 2 
while answ == 2:
    login(loadAccounts()) #menu
    try:
        answ = int(input("Do you want to quit?\n1-sim 2-nao"))
    except ValueError:
        print("Oops! That's not a valid option.")
        answ=1