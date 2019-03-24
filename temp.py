#                                                                  Bank System
#                                                         ~Developed by Chrystian Melo ~
import os
import os.path
import matplotlib.pyplot  as plt
import getpass
from datetime import date#month/year
#import time#min/sec

#Global Variables
qttparameters = 3#quantity of parameters needed to User()
adminUsers = {'14586486643': 'admin', '05487656690': 'admin2'}

#Classes
class User(object):
    def __init__(self,name, cpf, paswd):
        self.name = name#name[string]
        self.cpf = cpf#this variable will be usd to find the users[int]
        self.paswd = paswd#password[string]
        self.file = str(self.cpf)+".txt"
    def ActualValue(self):
        actual = 0
        if(os.path.exists(self.file)):
            linhas = open(self.file).readlines()
            for i in range(0,len(linhas)):
                if i % 2 == 0:#0,2,4...(just the value alteration)
                    actual = actual + int(linhas[i])
            return actual
        return 1#ERROR No cash
    def plotGraph(self):
        lines = open(self.file).readlines()
        x = [0]
        y = [0]
        for i in range(0,len(lines)):
            if i % 2 == 0:#0,2,4,6... Value
                y.append(int(lines[i]))
            else:#1,3,5... Months
                x.append(int(lines[i]))
        graphPloter(x,y,'Anual Bank Drive','Date(Months)','Value(Dolar)')
class Account(object):
    def __init__(self, user):
        self.user = user#primary user
    limCredit = 0
    def AddCash(self, value):
        bankdrive = loadBankDrive(self.user.file)#readind file(cpf.txt)
        bankdrive.append(value)#how much has been added
        #bankdrive.append(time.localtime(time.time()).tm_min)#just testing cuz month take too long
        bankdrive.append(date.today().month)#date adding money
        addBankDrive(self.user.file, bankdrive)#writig file
        
#File Functions
def addFile(accounts):
    file = open("data.txt", "w")
    for i in range(0, len(accounts)):
        name = str(accounts[i].user.name).rstrip()#removing all the \n existants SOLVING ERROR
        passwd = str(accounts[i].user.paswd).rstrip()
        file.write(name+"\n")
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
            a = Account(User(str(st[i-1]), int(st[i]), str(st[i+1])))
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
#User Comunication Functions
def login(data):#this function will foward the logic to option()
    try:
        cpf = input("Cpf.:")
        verify = "no"
        if cpf in adminUsers:#admin?
            paswd = str(getpass.getpass("Password.:"))
            if adminUsers[cpf] == paswd.rstrip():
                admin(data)
                addFile(data)
                verify = "yes" 
            else:
                print("Wrong Password")
        if verify == "no":#Normal Client
            search = searchCPF(data, int(cpf))
            if search != 0: #There is a user
                search -= 1#Undoing what i did to confirm in SearchCPF funcion
                passwd = str(getpass.getpass("Password.:"))
                if data[search].user.paswd.strip('\n') == passwd:#passw digited is equal to passwd of user x
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
def options(op, accounts, ident):#ident will be used in a specific case
    if op == 0:#No  user in this CPF
        print("We did not found a account with this CPF number. Create a new account here..:")
        acNEW= Account(User(str(input("Name..:")), int(input("CPF..::")), str(getpass.getpass("Password.:"))))
        accounts.append(acNEW)#allocing the new account in the array of all accounts
        print("Account creeated successfully!")
    if op == 1:#Actual value + movimentation in the year
        name = str(str(accounts[ident].user.cpf)+".txt")#User .txt file
        if(os.path.exists(name)):
            #show in graph all the movimentation
            accounts[ident].user.plotGraph()
            #actual value
            print("\nMr(s) ", accounts[ident].user.name, "\nThe value in your bank account is R$ ", accounts[ident].user.ActualValue())#The actual value in the account is on the penultimate  line in the file
        else:
            print("\nMr(s) ", accounts[ident].user.name, "\nYou have not added cash in this account!")
    if op == 2:
        cpf = int(input("What's the 'CPF' of the user that you want to consult?\n..:"))#variable to search
        ok = searchCPF(accounts, cpf)
        if ok !=  0:
            ok = ok - 1#Undoing what I did in searchCPF to not return 0(line 19)
            os.remove(str(accounts[ok].user.cpf)+".txt")
            accounts.remove(accounts[ok])
            print("Account deleted")
        else:
            print("There is no user with this 'CPF'!\n")
    if op ==3:
        add = int(input("How much do you want to add in your account?  ->"))
        accounts[ident].AddCash(add)
    if op == 4:
        rm = int(input("How much do you want to remove from your account?  ->"))
        if rm <= int(accounts[ident].user.ActualValue()):
            accounts[ident].AddCash(rm*-1)
        else:
            print("Oops!\nYou don't have credit neither this mount of cash")
    addFile(accounts)#saving data
#Useful Functions
def searchCPF(acc, cpf):
    i = 0
    while i < len(acc):
        if int(acc[i].user.cpf) == cpf:
            return i+1#Only return 0 when happens some error..OBS:When I receive this return I will undo this operation
        i+=1
    return 0#not found
def sort(alist):
     for position in range(len(alist)-1,0,-1):
       positionOfMax=0
       for location in range(1,position+1):
           if int(alist[location])>int(alist[positionOfMax]):
               positionOfMax = location
       temp = int(alist[position])
       alist[position] = alist[positionOfMax]
       alist[positionOfMax] = temp  
def graphPloter(x,y, title,namex,namey):
    plt.plot(x,y)#vet(x), vet(y)
    plt.title(title)
    plt.xlabel(namex)#X
    plt.ylabel(namey)#Y
    plt.show()#Show
def admin(acc):
    x = []
    y = []
    for i in range(0,len(acc)):
        y.append(int(acc[i].user.ActualValue()))
        x.append(int(acc[i].user.cpf))
    graphPloter(x,y,'BankDrive', 'Users', 'AccountValue')

#main funciotn
print("\n\t\t\t\t\tWelcome to BMC Bank!!")
answ = 2 
while answ == 2:
    login(loadAccounts()) #menu
    try:
        answ = int(input("Do you want to quit?\n1-sim 2-nao"))
    except ValueError:
        print("Oops! That's not a valid option.")
        answ=1
print("\n\t\t\t\t\tDeveloped by Chrystian Melo")