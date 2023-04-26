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
            linea = []
            for data in row:
                if primero:
                    primero = False
                    linea.append(data)
                else:
                    linea.append(float(data))
            matriz.append(linea)
    return matriz


def ec_Bellman(lista_convergencia: list, matriz_ON: list, matriz_OFF: list, 
               coste_on: float, coste_off: float, n_ciclos: int) -> list:
    """
    Cálculo de la ecuación de Bellman
    """
    # Limitamos el número de cilos a 994 para no exceder la recursión
    if type(n_ciclos) != int:
        raise TypeError ("El número de ciclos debe ser un natural")
    
    if n_ciclos > 994:
        raise ValueError ("El número de ciclos debe ser menor o igual a 994")
    
    lista_convergencia_temp = ["VALORES ESTADOS: "]
    lista_mejor_accion = ["PATH: "]

    for estado in range(len(matriz_ON)):
        if estado != 0:
            v_on = 0
            v_off = 0
            lista_probs_ON = matriz_ON[estado]
            lista_probs_OFF = matriz_OFF[estado]
            for prob in range(len(lista_probs_ON)):
                # Distinguimos entre las probabilidades y
                if lista_probs_ON[prob] != 0 and prob != 0:
                    v_on += lista_convergencia[prob] * lista_probs_ON[prob] 
            
            v_on += coste_on

            for prob in range(len(lista_probs_OFF)):
                # Distinguimos entre las probabilidades y
                if lista_probs_OFF[prob] != 0 and prob != 0:
                    v_off += lista_convergencia[prob] * lista_probs_OFF[prob] 
            
            v_off += coste_off

            # Estado 13 = 22 grados -> estado final (vale 0)
            if estado != 13:
                if v_on <= v_off:
                    lista_convergencia_temp.append(v_on)
                    lista_mejor_accion.append("ON")
                else:
                    lista_convergencia_temp.append(v_off)
                    lista_mejor_accion.append("OFF")
            else:
                lista_convergencia_temp.append(0)
                # Desde el estado final puedes transitar a otros estados
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

    if converge or n_ciclos == 1:
        # Acabamos al llegar al ciclo indicado
        print(lista_convergencia_temp)
        return lista_mejor_accion
    else:
        print(lista_convergencia_temp)
        lista_convergencia = copy.deepcopy(lista_convergencia_temp)
    
    # Volvemos a calcular hasta que llegar al ciclo indicado
    n_ciclos -= 1
    return ec_Bellman(lista_convergencia, matriz_ON, matriz_OFF, coste_on, coste_off, n_ciclos)
    

coste_on = 2000
coste_off = 10
matriz_ON = obtener_matrices_probs("./PROB_ON.csv")
matriz_OFF = obtener_matrices_probs("./PROB_OFF.csv")
estados = len(matriz_ON)+1
lista_convergencia  = [0] * estados
n_ciclos = 994
lista_politica_optima = ec_Bellman(lista_convergencia, matriz_ON, matriz_OFF, 
                                   coste_on, coste_off, n_ciclos)

print(lista_politica_optima)


