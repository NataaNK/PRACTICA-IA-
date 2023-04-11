"""
Autores: Natalia Rodríguez Navarro y Ángela Serrano Casas


"""

import csv

# Cargamos las tablas de probabilidades como una matriz
with open("./PROB_ON.csv", 'r') as file:
  csvreader = csv.reader(file)
  primero = True
  matriz = []
  for row in csvreader:
    if primero:
        primero = False
    elif not primero:
        linea = []
        for data in row:
            linea.append(float(data))
        matriz.append(linea)

print(matriz)


