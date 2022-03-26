#Librerías básicas
from threading import Thread, Semaphore
import time
import random
import sys 

# SEMAFOROS, los números son el valor inicial del contador 
semSanta = Semaphore(0) # Semáforo de Santa
semRenos = Semaphore(9) # Semáforos de los renos
semAyudaDuendes = Semaphore(3) # Semáforo para cuando pidan ayuda los renos
semDuendes = Semaphore(0) # Semáforos duendes

#VARIABLES
nRenos = 0 # Variable para contabilizar el numero de renos que han llegado
auxRenos = 0 #Auxuliar para que imprima de mejor manera las cosas
nDuendes = 0 #   Variable para contabilizar el numero de duendes que han llegado
duendesEsperando = 0 #Variable que contabiliza el trio de duendes 

# Nombres, pues porque sí
nombreRenos = ["RUDOLPH", "BLITZEN", "DONDER", "CUPID", "COMET", "VIXEN", "PRANCER", "DANCER", "DASHER"]
nombreDuendes = ["Tomás Turbado", "Meardel Peson", "Lalo Onganiza", "Carmelo Tallas", "Elsa Porrico", "Aquiles Pico", "Marisa Caleche", "Carmela Rosas", "Pato Carlo"]

# Hilo de Santa
def santa():
    global nRenos
    global duendesEsperando
    print("---- SANTA SE HA PUESTO A DORMIR")
    for _ in range (7):
        semSanta.acquire() # Decrementa el samaforo, pero como el contador interno no puede ser menor a 0, esperará hasta que se libere
        print("---- SANTA HA DESPERTADO")
        if duendesEsperando == 3:   #Si lo están esperando 3 duendes...
            duendesEsperando = 0    #Se resetea el contador
            for i in range(3):  #Liberamos
                print("---- SANTA AYUDA AL DUENDE {} DE 3".format(i + 1))
                semAyudaDuendes.release() # desbloqueas para la llegada de 3 duendes mas
            print("------ SANTA TERMINA DE AYUDAR A LOS DUENDES")
            for i in range(3):  #Ahora se liberan 3 espacios para duendes
                semDuendes.release()
        elif nRenos == 9:
            nRenos = 0
            navidad()

# Hilo de los renos
def reno():
    global nRenos
    global auxRenos
    num = nRenos
    nRenos += 1
    print ("Reno {} ha llegado".format (nombreRenos[num]))
    time.sleep(random. randint (5, 7))     
    auxRenos += 1     
    if auxRenos == 9:   #Cuando sean 9 renos, se libera el semaforo de Santa
        print("Han llegado los 9 renos")
        semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta
    else:
        print("Reno {} listo y enganchado en el trineo, es el {}". format(nombreRenos[num], num))
    semRenos.acquire()

# Hilo de los duendes
def duende():
    global nDuendes
    global duendesEsperando
    num = nDuendes
    nDuendes += 1
    print("Duende {} llegando al taller".format (nombreDuendes[num]))
    for _ in range(2):
        time.sleep(random.randint (1,5))
        semAyudaDuendes.acquire() # decrementa el contador de que los duendes ocupan a Santa... ¿Por qué? Porque si no lo tuviera, llegarían más y más duendes sin parar
        duendesEsperando += 1
        duende = duendesEsperando 
        if duende < 3:  #Si aún no llegan a ser 3 duendes... se agrega a la espera
            print("Duende {} esperando, es el {} en la fila".format(nombreDuendes[num], duende))
        elif duende == 3:   #Cuando sean los 3, liberan el semáforo de Santa
            print("Duende {} esperando: Es el {}, entre los tres llaman a Santa!". format(nombreDuendes[num], duende))
            semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta
        semDuendes.acquire() # Decrementa el contador de duendes

# Santa prepara el trineo y se va a dormir
def navidad():
    for i in range(9):  #Libreramos los 9 renos
        semRenos.release() 
    print(" ---- SANTA SE VA EN SU TRINEO")
    print(" ... DESPUES DE ESTO, SANTA VUELVE A DORMIR")

def inicio():
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
    print("A")
