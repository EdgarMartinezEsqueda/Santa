from threading import Thread, Semaphore
import time
import random
import sys 

# SEMAFOROS, los números son el valor inicial del contador 
semSanta = Semaphore(0) # Semáforo de Santa
semRenos = Semaphore(9) # Semáforos de los renos
semAyudaRenos = Semaphore(3) # Semáforo para cuando pidan ayuda los renos
semDuendes = Semaphore(0) # Semáforos duendes

#VARIABLES
nRenos = 0 # Variable para contabilizar el numero de renos que han llegado
auxRenos = 0 #Auxuliar para que imprima de mejor manera las cosas
nDuendes = 0 #   Variable para contabilizar el numero de duendes que han llegado
duendesEsperando = 0 #Variable que contabiliza el trio de duendes 

            
nombreRenos = ["RUDOLPH", "BLITZEN", "DONDER", "CUPID", "COMET", "VIXEN", "PRANCER", "DANCER", "DASHER"]
nombreDuendes = ["Taleasin", "Halafarin", "Ailduin", "Adamar", "Galather", "Estelar", "Lyari", "Andrathath", "Wyn"]

# Definicion del proceso Santa: Santa duerme y le despertaran cuand
# Si tres duendes piden ayuda, Santa los ayudará, liberará otros tres
# y despues liberara (semDuendes.release()) los tres duendes ayudados. Si
# el trineo y los liberara (semRenos.release()). Santa se desper
def santa():
    global nRenos
    global duendesEsperando
    print("---- SANTA SE HA PUESTO A DORMIR")
    while True:
        semSanta.acquire() # Decrementa el samaforo, pero como el contador interno no puede ser menor a 0, esperará hasta que se libere
        print("---- SANTA HA DESPERTADO")
        if duendesEsperando == 3:
            duendesEsperando = 0
            for i in range(3):
                print("---- SANTA AYUDA AL DUENDE {} DE 3".format(i + 1))
                semAyudaRenos.release() # desbloqueas para la llegada de 3 duendes mas
            print("------ SANTA TERMINA DE AYUDAR A LOS DUENDES")
            for i in range(3):
                semDuendes.release()
        elif nRenos == 9:
            nRenos = 0
            navidad()
            for i in range(9):
                semRenos.release()

# Definicion del proceso reno: los renos van llegando y se van bloqueando (semRenos.acquire(0).
# Cuando llegan los 9 renos despiertan a Santa (Santasem.release()).
# Despues Santa los prepara y los ata al trineo solo una vez, y los libera.
def reno():
    global nRenos
    global auxRenos
    num = nRenos
    nRenos += 1
    print ("Reno {} ha llegado".format (nombreRenos[num]))
    time.sleep(random. randint (5, 7))     
    auxRenos += 1     
    if auxRenos == 9:
        print("Han llegado los 9 renos")
        semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta
    else:
        print("Reno {} listo y enganchado en el trineo, es el {}". format(nombreRenos[num], num))
    semRenos.acquire()

#Definicion del proceso elfo: como se puede apreciar los duendes van llegando y pediran ayuda dos veces cada uno. (TO_HELP=2)
# Una vez hayan llegado tres duendes, los siguientes que lleguen seran bloqueados (ELfSemH.acquire()) hasta que Santa los libere.
# Solo cuando tres duendes pidan ayuda Santa se despertara (Santasem.release()).
# Los tres duendes que piden ayuda estarán bloqueados (ELfSem.acquire(0) hasta que Santa los ayude y los libere.
# Cuando cada elfo haya sido ayudado dos veces acabaran.
def duende():
    global nDuendes
    global duendesEsperando
    num = nDuendes
    nDuendes += 1
    print("Duende {} llegando al taller".format (nombreDuendes[num]))
    while True:
        time.sleep(random.randint (1,5))
        semAyudaRenos.acquire() # decrementa el contador
        duendesEsperando += 1
        duende = duendesEsperando 
        if duende < 3:
            print("Duende {} esperando, es el {} en la fila".format(nombreDuendes[num], duende))
        elif duende == 3:
            print("Duende {} esperando: Es el {}, entre los tres llaman a Santa!". format(nombreDuendes[num], duende))
            semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta
        semDuendes.acquire() # Decrementa el contador de duendes

# Santa prepara el trineo y se va a dormir
def navidad():
    print(" ---- SANTA SE VA EN SU TRINEO")
    print(" ... DESPUES DE ESTO, SANTA VUELVE A DORMIR")
    sys.exit()


# Array de hilos
threads = []
# Santa
threads.append(Thread(target=santa))
# Duendes
for i in range(9):
    threads.append(Thread(target=duende))
# Reno
for i in range(9):
    threads.append(Thread(target=reno))
# Iniciamos todos los hilos
for t in threads:
    t.start()
# Esperamos a que se completen todos los hilos
for t in threads:
    t.join()