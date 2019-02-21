#                                                                  Bank System
#                                                         ~Developed by Chrystian Melo ~

#Classes
class User(): 
    def __init__(self,name,value,cpf):
        self.name = name#name
        self.value = value#value in the account
        self.cpf = cpf#this variable will be usd to find the users
class Account():
    def __init__(self, user):
        self.user = user#primary user

#some functions that will e useable during the code
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
        print("⚠️Oops!⚠️\n That's not a valid number. Try again!")
        return 0

answ = mainMenu()

accounts = []#This vector will contain all of the BMC bank's accounts
while answ != 7: 
    #OPTION 1: allocing/reallocing the quantity of accounts
    if answ == 1:
        a=Account(User(input("Name..:"), int(input("Value..:")), int(input("CPF..:"))))
        accounts = accounts + [a]#allocing the new account in the array of all accounts
    #OPTION 2:
    if answ == 2:
        if len(accounts) != 0:
            cpf = int(input("What's the 'CPF' of the user that you want to consult?\n..:"))#variable to search 
            ok = searchCPF(accounts, cpf)
            if ok != 0:
                ok = ok - 1#Undoing what I did in searchCPF to not return 0(line 19) 
                print("✓We found the account!")
                print("Name = ", accounts[ok].user.name, "\nValue in the bank account = ", accounts[ok].user.value)
            else:
                print("⚠️There is no user with this 'CPF'!⚠️\n")
        else:
            print("⚠️There is no users in this bank yet!⚠️\n")
    answ = mainMenu()
        