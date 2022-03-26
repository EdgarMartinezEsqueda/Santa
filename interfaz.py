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

#----------------BOTONES----------------
botonSalir = QPushButton("Salir")
botonSalir.setStyleSheet("width: 20px;")
botonIniciar = QPushButton("Iniciar")
botonIniciar.clicked.connect(santa.inicio)
botonIniciar.setStyleSheet("width: 20px;")

#Agregamos los elementos al grid
grid.addWidget(botonSalir,2,2)
grid.addWidget(botonIniciar,2,3)

#----------------GIFS----------------
# imgSnta = QMovie("imagenes/repartiendo.gif")
# imagen = QLabel()
# imagen.setMovie(imgSnta)
# grid.addWidget(imagen, 0, 0)


#----------------IMÁGENES----------------
ctnCentral = QLabel()
ctnCentral.setStyleSheet("background: #ff05ef")
imgcaliz = QPixmap("imagenes/renos.png")
imgcaliz = imgcaliz.scaledToHeight(80) #redimensionar la imagen
ctnCentral.setPixmap(imgcaliz)

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

tituloDuentes = QLabel('Duentes\n0')
tituloDuentes.setStyleSheet("font-size:20px; font-family:'sans-serif'; text-align: center;")
tituloDuentes.setAlignment(Qt.AlignCenter)

tituloRenos = QLabel('Renos\n0')
tituloRenos.setStyleSheet("font-size:20px; font-family:'sans-serif'; text-align: center;")
tituloRenos.setAlignment(Qt.AlignCenter)

#Agregamos los elementos al grid
grid.addWidget(tituloSanta,0,5)
grid.addWidget(tituloDuentes,0,1)
grid.addWidget(tituloRenos,0,3)

grid.setRowStretch(0, 1)
grid.setRowStretch(1, 5)
grid.setRowStretch(2, 1)

#----------------EJECUCIÓN----------------
ventana.setLayout(grid)
sys.exit(app.exec())