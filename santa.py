#Librerías básicas
from threading import Thread, Semaphore
import time
import random

# SEMAFOROS, los números son el valor inicial del contador 
semSanta = Semaphore(0) # Semáforo de Santa
semRenos = Semaphore(9) # Semáforos de los renos
semAyudaDuendes = Semaphore(3) # Semáforo para cuando pidan ayuda los renos
semDuendes = Semaphore(0) # Semáforos duendes

#VARIABLES
nRenos = 0 # Variable para contabilizar el numero de renos que han llegado
duendesEsperando = 0 #Variable que contabiliza el trio de duendes 
regalosEntregados = False

# Nombres, pues porque sí
nombreRenos = ["RUDOLPH", "BLITZEN", "DONDER", "CUPID", "COMET", "VIXEN", "PRANCER", "DANCER", "DASHER"]

# Hilo de Santa
def santa():
    global nRenos
    global duendesEsperando
    print("---- SANTA ESTÁ DORMIDO")
    while nRenos < 9:
        semSanta.acquire() # Decrementa el samaforo, pero como el contador interno no puede ser menor a 0, esperará hasta que se libere
        print("---- SANTA HA DESPERTADO")
        if duendesEsperando == 3:   #Si lo están esperando 3 duendes...
            duendesEsperando = 0    #Se resetea el contador
            for i in range(3):  #Liberamos
                print("---- SANTA AYUDA AL DUENDE {} DE 3".format(i + 1))
                time.sleep(random.randint (1,3))   
                semAyudaDuendes.release() # desbloqueas para la llegada de 3 duendes mas
            print("------ SANTA TERMINA DE AYUDAR A LOS DUENDES")
            for i in range(3):  #Ahora se liberan 3 espacios para duendes
                semDuendes.release()
    navidad()

# Hilo de los renos
def reno():
    global nRenos
    while nRenos < 9:
        time.sleep(random.randint(5,7))    
        nRenos += 1
        print("Reno {} listo y enganchado en el trineo, es el {}". format(nombreRenos[nRenos-1], nRenos))
        semRenos.acquire()
    print("--- LOS 9 RENOS ESTÁN LISTOS ESPERANDO A SANTA")
    semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta


# Hilo de los duendes
def duende():
    global duendesEsperando
    global regalosEntregados
    while not regalosEntregados:
        time.sleep(random.randint (1,5))
        semAyudaDuendes.acquire() # decrementa el contador de que los duendes ocupan a Santa... ¿Por qué? Porque si no lo tuviera, llegarían más y más duendes sin parar
        duendesEsperando += 1
        if duendesEsperando < 3:  #Si aún no llegan a ser 3 duendes... se agrega a la espera
            print("Duende esperando, es el {} en la fila".format(duendesEsperando))
        elif duendesEsperando == 3:   #Cuando sean los 3, liberan el semáforo de Santa
            print("Llega el 3er duende, entre los tres llaman a Santa!")
            semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta

# Santa prepara el trineo y se va a dormir
def navidad():
    global regalosEntregados
    for _ in range(9):  #Libreramos los 9 renos
        semRenos.release() 
    print(" ---- SANTA SE VA EN SU TRINEO")
    print(" ... DESPUES DE ESTO, SANTA VUELVE A DORMIR")
    regalosEntregados = True

def inicio():
    # Array de hilos
    threads = []
    # Santa
    threads.append(Thread(target=santa))
    # Duendes
    threads.append(Thread(target=duende))
    # Reno
    threads.append(Thread(target=reno))
    # Iniciamos todos los hilos
    for t in threads:
        t.start()
    # Esperamos a que se completen todos los hilos
    for t in threads:
        t.join()
