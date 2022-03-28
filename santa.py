#Librerías básicas
from threading import Thread, Semaphore
import time
import random
from PyQt5.QtGui import QMovie

# SEMAFOROS, los números son el valor inicial del contador 
semSanta = Semaphore(0) # Semáforo de Santa
semAyudaDuendes = Semaphore(3) # Semáforo para cuando pidan ayuda los duendes

#VARIABLES
nRenos = 0 # Variable para contabilizar el numero de renos que han llegado
duendesEsperando = 0 #Variable que contabiliza el trio de duendes 
regalosEntregados = False

# Nombres, pues porque sí
nombreRenos = ["RUDOLPH", "BLITZEN", "DONDER", "CUPID", "COMET", "VIXEN", "PRANCER", "DANCER", "DASHER"]

# Hilo de Santa
def santa(label, cntCentral):
    global nRenos
    global duendesEsperando
    print("---- SANTA ESTÁ DORMIDO")
    while nRenos < 9:
        semSanta.acquire() # Decrementa el samaforo, pero como el contador interno no puede ser menor a 0, esperará hasta que se libere
        print("---- SANTA HA DESPERTADO")
        label.setText("Santa\nDESPIERTO")
        if duendesEsperando == 3:   #Si lo están esperando 3 duendes...
            duendesEsperando = 0    #Se resetea el contador
            for i in range(3):  #Liberamos
                print("---- SANTA AYUDA AL DUENDE {} DE 3".format(i + 1))
                time.sleep(random.randint (1,3))   
                semAyudaDuendes.release() # desbloqueas para la llegada de 3 duendes mas
            print("------ SANTA TERMINA DE AYUDAR A LOS DUENDES")
            label.setText("Santa\nDORMIDO")
    navidad()

# Hilo de los renos
def reno(label):
    global nRenos
    while nRenos < 9:
        time.sleep(random.randint(5,7))    
        nRenos += 1
        label.setText("Renos\n{}".format(nRenos))
        print("Reno {} listo y enganchado en el trineo, es el {}". format(nombreRenos[nRenos-1], nRenos))
    print("--- LOS 9 RENOS ESTÁN LISTOS ESPERANDO A SANTA")
    semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta


# Hilo de los duendes
def duende(label):
    global duendesEsperando
    global regalosEntregados
    while not regalosEntregados:
        time.sleep(random.randint (1,5))
        semAyudaDuendes.acquire() # decrementa el contador de que los duendes ocupan a Santa... ¿Por qué? Porque si no lo tuviera, llegarían más y más duendes sin parar
        duendesEsperando += 1
        label.setText("Duendes\n{}".format(duendesEsperando))
        if duendesEsperando < 3:  #Si aún no llegan a ser 3 duendes... se agrega a la espera
            print("Duende esperando, es el {} en la fila".format(duendesEsperando))
        elif duendesEsperando == 3:   #Cuando sean los 3, liberan el semáforo de Santa
            print("Llega el 3er duende, entre los tres llaman a Santa!")
            semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta
            label.setText("Duendes\n0")

# Santa prepara el trineo y se va a dormir
def navidad():
    global regalosEntregados
    print(" ---- SANTA SE VA EN SU TRINEO")
    print(" ... DESPUES DE ESTO, SANTA VUELVE A DORMIR")
    regalosEntregados = True

def inicio(lbSanta, lbDuendes, lbRenos, cntCentral):
    # Array de hilos
    threads = []
    # Santa
    threads.append(Thread(target=santa, args = (lbSanta, cntCentral) ))
    # Duendes
    threads.append(Thread(target=duende, args = (lbDuendes,) ))
    # Reno
    threads.append(Thread(target=reno, args = (lbRenos,) ))
    # Iniciamos todos los hilos
    for t in threads:
        t.start()