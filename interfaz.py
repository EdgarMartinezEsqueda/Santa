import sys
from tkinter import font
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import santa

app = QApplication(sys.argv) #aplicacion - objeto

#----------------VENTANA----------------
ventana = QWidget()
ventana.setWindowTitle("Santa Claus")
ventana.setFixedWidth(600) 
ventana.show()

#----------------CUADRICULA (GRID)----------------
grid = QGridLayout()

#----------------IMÁGENES----------------
ctnCentral = QLabel()
ctnCentral.setStyleSheet("background: #f2f2f2")
# imgcaliz = QPixmap("imagenes/santaRegalo.jpg")
# imgcaliz = imgcaliz.scaledToHeight(360) #redimensionar la imagen
# ctnCentral.setPixmap(imgcaliz)

#----------------GIFS----------------
gif = QMovie("imagenes/repartiendo.gif")
ctnCentral.setMovie(gif)
gif.start()

#renos
ctnRenos = QLabel()
ctnRenos.setAlignment(Qt.AlignCenter)
imgRenos = QPixmap("imagenes/renos.png")
imgRenos = imgRenos.scaledToHeight(80) #redimensionar la imagen
ctnRenos.setPixmap(imgRenos)

#duendes
ctnDuentes = QLabel()
ctnDuentes.setAlignment(Qt.AlignCenter)
imgDuentes = QPixmap("imagenes/duende.png")
imgDuentes = imgDuentes.scaledToHeight(80) #redimensionar la imagen
ctnDuentes.setPixmap(imgDuentes)

#santa
ctnSanta = QLabel()
ctnSanta.setAlignment(Qt.AlignCenter)
imgSanta = QPixmap("imagenes/santa.png")
imgSanta = imgSanta.scaledToHeight(80) #redimensionar la imagen
ctnSanta.setPixmap(imgSanta)

#Agregamos los elementos al grid
grid.addWidget(ctnDuentes,0,0)
grid.addWidget(ctnRenos,0,2)
grid.addWidget(ctnSanta,0,4)
grid.addWidget(ctnCentral,1,1,1,4)

#----------------ETIQUETAS----------------
tituloSanta = QLabel('Santa\nDormido')
tituloSanta.setStyleSheet("font-size:20px; font-family:'sans-serif'; text-align: center;")
tituloSanta.setAlignment(Qt.AlignCenter)

tituloDuendes = QLabel('Duentes\n0')
tituloDuendes.setStyleSheet("font-size:20px; font-family:'sans-serif'; text-align: center;")
tituloDuendes.setAlignment(Qt.AlignCenter)

tituloRenos = QLabel('Renos\n0')
tituloRenos.setStyleSheet("font-size:20px; font-family:'sans-serif'; text-align: center;")
tituloRenos.setAlignment(Qt.AlignCenter)

tituloAccion = QLabel('')
tituloAccion.setStyleSheet("font-size:15px; font-family:'sans-serif'; text-align: center;")
tituloAccion.setAlignment(Qt.AlignCenter)

#Agregamos los elementos al grid
grid.addWidget(tituloSanta,0,5)
grid.addWidget(tituloDuendes,0,1)
grid.addWidget(tituloRenos,0,3)
grid.addWidget(tituloAccion,2,1,1,4)

grid.setRowStretch(0, 1)
grid.setRowStretch(1, 5)
grid.setRowStretch(2, 1)

#----------------BOTONES----------------
# botonSalir = QPushButton("Salir")
# botonSalir.setStyleSheet("width: 20px;")
botonIniciar = QPushButton("Iniciar")
botonIniciar.clicked.connect(lambda: santa.inicio(tituloSanta, tituloDuendes, tituloRenos, tituloAccion, ctnCentral))
botonIniciar.setStyleSheet("width: 20px;")

#Agregamos los elementos al grid
# grid.addWidget(botonSalir,3,2)
grid.addWidget(botonIniciar,3,2,1,2)

#----------------EJECUCIÓN----------------
ventana.setLayout(grid)
sys.exit(app.exec())
