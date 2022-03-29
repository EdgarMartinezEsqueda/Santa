#Librerías básicas
from threading import Thread, Semaphore
import time
import random
from PyQt5.QtGui import QPixmap

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
def santa(label, accion, cntCentral):
    global nRenos
    global duendesEsperando
    while nRenos < 9:
        semSanta.acquire() # Decrementa el samaforo, pero como el contador interno no puede ser menor a 0, esperará hasta que se libere
        label.setText("Santa\nDespierto")
        accion.setText("Santa se ha despertado")
        if duendesEsperando == 3:   #Si lo están esperando 3 duendes...
            duendesEsperando = 0    #Se resetea el contador
            imgAyuda = QPixmap("imagenes/ayudando_duendes.png")
            imgAyuda = imgAyuda.scaledToHeight(360) #redimensionar la imagen
            cntCentral.setPixmap(imgAyuda)
            for i in range(3):  #Liberamos
                accion.setText("Santa ayuda al duende {} de 3".format(i + 1))
                time.sleep(3)   
                semAyudaDuendes.release() # desbloqueas para la llegada de 3 duendes mas
            accion.setText("Santa termina de ayudar a los duendes")
            label.setText("Santa:\nDormido")
    navidad(accion, cntCentral)

# Hilo de los renos
def reno(label, accion, cntCentral):
    global nRenos
    while nRenos < 9:
        time.sleep(random.randint(5,7))    
        nRenos += 1
        label.setText("Renos:\n{}".format(nRenos))
        accion.setText("Reno {} listo y enganchado en el trineo, es el {}". format(nombreRenos[nRenos-1], nRenos))
        imgReno = QPixmap("imagenes/renos.png")
        imgReno = imgReno.scaledToHeight(240) #redimensionar la imagen
        cntCentral.setPixmap(imgReno)
    accion.setText("LOS 9 RENOS ESTÁN LISTOS ESPERANDO A SANTA")
    semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta


# Hilo de los duendes
def duende(label, accion, cntCentral):
    global duendesEsperando
    global regalosEntregados
    while not regalosEntregados or nRenos < 9:
        time.sleep(random.randint (1,4))
        semAyudaDuendes.acquire() # decrementa el contador de que los duendes ocupan a Santa... ¿Por qué? Porque si no lo tuviera, llegarían más y más duendes sin parar
        duendesEsperando += 1
        label.setText("Duendes:\n{}".format(duendesEsperando))
        imgDuentes = QPixmap("imagenes/llegaDuende.jpg")
        imgDuentes = imgDuentes.scaledToHeight(480) #redimensionar la imagen
        cntCentral.setPixmap(imgDuentes)
        if duendesEsperando < 3:  #Si aún no llegan a ser 3 duendes... se agrega a la espera
            accion.setText("Duende esperando, es el {} en la fila".format(duendesEsperando))
        elif duendesEsperando == 3:   #Cuando sean los 3, liberan el semáforo de Santa
            accion.setText("Llega el 3er duende, entre los tres llaman a Santa!")
            semSanta.release() # Libera el semaforo, aumenta el contador -> santa se despierta
            label.setText("Duendes:\n0")

# Santa prepara el trineo y se va a dormir
def navidad(accion, cntCentral):
    global regalosEntregados
    regalosEntregados = True
    accion.setText("SANTA SE VA EN SU TRINEO")
    time.sleep(1)
    accion.setText("FELIZ NAVIDAD")
    imgNavidad = QPixmap("imagenes/santaRegalo.jpg")
    imgNavidad = imgNavidad.scaledToHeight(360) #redimensionar la imagen
    cntCentral.setPixmap(imgNavidad)

#Arrancar todo
def inicio(lbSanta, lbDuendes, lbRenos, lblAccion, cntCentral):
    # Array de hilos
    threads = []
    # Santa
    threads.append(Thread(target=santa, args = (lbSanta, lblAccion, cntCentral) ))
    # Duendes
    threads.append(Thread(target=duende, args = (lbDuendes, lblAccion, cntCentral) ))
    # Reno
    threads.append(Thread(target=reno, args = (lbRenos, lblAccion, cntCentral) ))
    # Iniciamos todos los hilos
    for t in threads:
        t.start()
