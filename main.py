#Pa' lo grafico 
import tkinter as tk  #https://realpython.com/python-gui-tkinter/
#window = tk.Tk()

#https://github.com/mussaiin/Santa-Claus-Problem
import random
from threading import Semaphore
from threading import Thread #pa los hilos
import time

#Variables: Elfos, renos, semaforoSanta, semaforoElfo
#semaforoRenos, renos
elves_c = 0
reindeer_c = 0
santaSem = Semaphore()
reindeerSem = Semaphore()
elfTex = Semaphore()
mutex = Semaphore(1)

#Funcion prepararTrineo
def prepareSleigh():
    global reindeer_c
    print("Santa Claus: preparando trineo")


#Funcion para ayudar a los renos
def helpElves():
    print("Santa Claus: ayudando elfos")


#Funcion para amarrar un reno
def getHitched():
    print("Este es un reno ", reindeer_c)

#Funcion que les dice a los elfos que ayuden
def getHelp():
    print("Este es un elfo", elves_c)

#Definimos a santa
def santa():
    global elves_c, reindeer_c
    print("Santa Claus: Yaye gue, ?qal esel ped2¿?")
    while True:
        santaSem.acquire()
        mutex.acquire()
      #Si los renos son 9, preparamos el trineo
        if reindeer_c >= 9:
            prepareSleigh()
          #Liberamos al los renos
            for i in range(9):
                reindeerSem.release()
            print("Santa Claus: Yevenle periko a loz mocoxoz delmun do")
            reindeer_c -= 9
            time.sleep(4)
        elif elves_c == 3:
            helpElves()
        mutex.release()

#Definimos a los renos
def reindeer():
    global reindeer_c
    while True:
      #Cambiamos el estado del semaforo para que lleguen los 
      #renos
        mutex.acquire()
        reindeer_c += 1
        if reindeer_c == 9:
            santaSem.release()
        mutex.release
      #Amarramos al reno
        getHitched()
        print("El reno numero ", reindeer_c, " ha sido amarrado")
        reindeerSem.acquire()
        time.sleep(random.randint(2, 3))

#Definimos a los elfos
def elves():
    global elves_c
    while True:
      #Preparamos los semaforos para el funcionamiento
        elfTex.acquire()
        mutex.acquire()
      #Agregamos elfos para que se pueda continuar con el problema
        elves_c += 1
        if elves_c == 3:
          #Despertamos a santa
            santaSem.release()
        else:
          #Aumentamos el semaforo
            elfTex.release()
        mutex.release()
        getHelp()
        time.sleep(random.randint(2, 5))
        mutex.acquire()
        elves_c -= 1
        if elves_c == 0:
            elfTex.release()
        mutex.release()
        print("Duende ", elves_c, "at work")


elfThread = []  # threads for elves
reindThread = []  # threads from reindeers


def main():
    thread = Thread(target=santa)  # main thread for SantaClaus
    thread.start()  # starting the thread
    for i in range(9):
        reindThread.append(Thread(target=reindeer))
    for j in range(9):
        elfThread.append(Thread(target=elves))
    for t in elfThread:
        t.start()
    for t in reindThread:
        t.start()
    for t in elfThread:
        t.join()
    for t in reindThread:
        t.join()
    thread.join()


main()