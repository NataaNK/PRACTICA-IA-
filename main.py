"""
Autores: Natalia Rodríguez Navarro y Ángela Serrano Casas


"""
import csv
import copy
import random

def obtener_matrices_probs(csv_path: str) -> list:
    """
    Carga las probabilidades de una tabla en csv en una matriz
    """
    with open(csv_path, 'r') as file:
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
    return matriz


def ec_Bellman(lista_convergencia: list, matriz_ON: list, matriz_OFF: list, 
               coste_on: float, coste_off: float) -> list:
    """
    Cálculo de la ecuación de Bellman
    """
    lista_convergencia_temp = ["VALORES ESTADOS: "]
    lista_mejor_accion = ["PATH: "]

    for estado in range(len(matriz_ON)):
        v_on = 0
        v_off = 0
        lista_probs_ON = matriz_ON[estado]
        lista_probs_OFF = matriz_OFF[estado]
        for prob in range(len(lista_probs_ON)):
            # Distinguimos entre las probabilidades y
            if lista_probs_ON[prob] != 0 and prob != 0:
                v_on += lista_convergencia[prob] * lista_probs_ON[prob] 
        
        v_on += coste_on
        # Para converger antes y no exceder la recursión
        v_on = round(v_on, 1)

        for prob in range(len(lista_probs_OFF)):
            # Distinguimos entre las probabilidades y
            if lista_probs_OFF[prob] != 0 and prob != 0:
                v_off += lista_convergencia[prob] * lista_probs_OFF[prob] 
        
        v_off += coste_off
        # Para converger antes y no exceder la recursión
        v_off = round(v_off, 1)

        # Estado 12 = 22 grados -> estado final (vale 0)
        if estado != 12:
            if v_on <= v_off:
                lista_convergencia_temp.append(v_on)
                lista_mejor_accion.append("ON")
            else:
                lista_convergencia_temp.append(v_off)
                lista_mejor_accion.append("OFF")
        else:
            lista_convergencia_temp.append(0)
            if v_on <= v_off:
                lista_mejor_accion.append("ON")
            else:
                lista_mejor_accion.append("OFF")
        
    # Comprobamos si convergen los valores
    i = 0
    converge = True
    while i < len(lista_convergencia_temp) and converge:
        if lista_convergencia[i] != lista_convergencia_temp[i]:
            converge = False
        i+=1

    if converge:
        print(lista_convergencia_temp)
        return lista_mejor_accion
    else:
        print(lista_convergencia_temp)
        lista_convergencia = copy.deepcopy(lista_convergencia_temp)
    
    # Volvemos a calcular hasta que converja
    return ec_Bellman(lista_convergencia, matriz_ON, matriz_OFF, coste_on, coste_off)
    

coste_on = 20
coste_off = 3
matriz_ON = obtener_matrices_probs("./PROB_ON.csv")
matriz_OFF = obtener_matrices_probs("./PROB_OFF.csv")
estados = len(matriz_ON)+1
lista_convergencia  = [0] * estados
lista_politica_optima = ec_Bellman(lista_convergencia, matriz_ON, matriz_OFF, coste_on, coste_off)

print(lista_politica_optima)


