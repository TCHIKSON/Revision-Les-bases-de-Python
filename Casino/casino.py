from random import randint
import pymysql.cursors
import time
import threading
from inputimeout import inputimeout


lvl ={
    1: {"cible": 10, "attemps":3 },
    2: {"cible": 20, "attemps":5 },
    3: {"cible": 30, "attemps":7 }
}

def casino_start():

    connection=connect_db()
    user = login(connection)
    name = user[0]
    solde = user[1]
    level = user[2]

    mise = 0
    print(solde)
    while(float(solde) > 0.0 ):
        print("Choisissez votre niveau maximum "+str(level)+" ou entrer 4 pour quitter")
        niveau = choose_number(4)
        if (niveau == 4 ):
            break
        elif(not (niveau>level)):
            print(niveau, level)
            result = parti(niveau, solde)
            level = result[1]
            solde = result[0]
            print("Votre solde est de : " + str(solde))
            write_db(connection,name,solde,level)
        else : 
            print("Choissisez maximum le niveau "+str(level))



def login(connection):
    name = input("Bonjour, je suis Python. Quel est votre pseudo ? \n")
    user = read_db(connection, name)
    print(user)
    solde = user['solde']
    level = user['level']
    print("""\t- Hello """+name+""", vous avez """+str(solde)+""" €, Très bien ! Installez vous SVP à la table de pari.\n\t\t\t """)
    return [name,solde,level]

def read_rules():
     print("""Je vous expliquerai le principe du jeu : \n
        \t- Je vais penser à un nombre entre 1 et 10 pour le premier. Vous devrez devinez lequel ?\n
        \t- Att : vous avez le droit à trois essais !\n
        \t- Si vous devinez mon nombre dès le premier coup, vous gagnez le double de votre mise !\n
        \t- Si vous le devinez au 2è coup, vous gagnez exactement votre mise !\n
        \t- Si vous le devinez au 3è coup, vous gagnez la moitiè votre mise !\n    
        \t- Si vous ne le devinez pas au 3è coup, vous perdez votre mise et
        \tvous avez le droit : 
        \t\t- de retenter votre chance avec l'argent qu'il vous reste pour reconquérir le level perdu.
        \t\t- de quitter le jeu.\n
        \t- Dès que vous devinez mon nombre : vous avez le droit de quitter le jeu et de partir avec vos gains OU \n\t\tde continuer le jeu en passant au level supérieur.\n""")
def select_random(lvl):
    print("Vous êtes au niveau "+ str(lvl) +"\n Je choisis donc un nombre entre 1 et "+ str(lvl) +"0")
    return randint(1, lvl*10)

def choose_number(max):
    nb = 0
    while(not(0<nb and nb<=max)):
        print("Entrer SVP un nombre entre 1 et "+ str(max) +" :  \n")
        try:
            nb = int(input("\t Entrez votre nombre \n"))
        except ValueError :
            print("\t- Je ne comprends pas ! Entrer SVP un nombre\n")

    return nb

def choose_bet(max):
    nb = 0
    while(not(0<nb and nb<=max)):
        print("Entrer SVP un nombre entre 1 et "+ str(max) +" :  \n")
        try:
            nb = int(inputimeout("\t Entrez votre nombre \n",5))
        except ValueError :
            print("\t- Je ne comprends pas ! Entrer SVP un nombre\n")
        except Exception as e :
            print("Temps dépasser",e)

    return nb




def parti(niveau, solde):
    fail = False
    result = True
    i=1
    print("Le partie commence, commencons par votre mise elle doit être comprise entre 1 et "+str(solde))
    mise = choose_number(solde)
    solde = solde - mise
    print("\t- Votre mise est : " + str(mise))
    cible = select_random(niveau)
    print("J'ai choisi " + str(cible))
    while result and i<= lvl[niveau]["attemps"] :
        print('Essaie numéro '+ str(i))
        result = manche(cible,  lvl[niveau]["cible"])
        i=i+1

    if(not(result)) :
        print("Vous avez trouvé en "+ str(i-1)+" essais")
        print( "Vous avez gagnez " + str(mise * lvl[niveau]["attemps"] / i ))
        niveau=niveau + 1
    return [solde + (mise * lvl[niveau]["attemps"] / i), niveau]




def manche(cible,max):
    
    bet= choose_bet(max)
    if bet < cible :
        print("Votre nombre est trop petit.")
        return True
    elif bet > cible:
        print("Votre nombe est trop grand")
        return True
    else :
        print("Vous avez trouvé") 
        return False
    return True




def connect_db(): 
    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='db_casino',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection
    
def write_db(connection, name, solde,level):
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `user` (`name`, `solde`,`level`) VALUES (%s, %s,%s) ON DUPLICATE KEY UPDATE `solde`=%s,`level`=%s"
        cursor.execute(sql, (name, solde,level, solde,level))

    connection.commit()
    print("Modification réussi Solde: "+str(solde))
    return read_db(connection,name)
    

def read_db(connection, name):
    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `name`, `solde`,`level` FROM `user` where `name`=%s"
        cursor.execute(sql, (name, ))
        result = cursor.fetchone()
        if(result == None):
            result = write_db(connection, name, 10,1)
        return result

   
            
casino_start()