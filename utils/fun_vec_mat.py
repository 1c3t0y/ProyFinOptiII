### Funciones de vectores y Matrices ###
import numpy as np

### Funciones de renglones ###


### Funciones de matrices ###


def gen_mat_restricciones_transporte(n, m):
    matriz_restricciones = np.zeros((n + m, n * m))

    for i in range(n):
        for j in range(m):
            matriz_restricciones[i, (i * m) + j] = 1

    for j in range(m):
        for i in range(n):
            matriz_restricciones[j + n, (i * m) + (j)] = 1

    return matriz_restricciones


def gen_mat_restricciones_redes(matriz_adyacencia):
    n = matriz_adyacencia.shape[0]

    matriz_restricciones = np.zeros((n, n*n))

    for i, renglon in enumerate(matriz_adyacencia):
        for j, variable in enumerate(renglon):
            if variable :
                matriz_restricciones[i][i*n+j] = 1
                matriz_restricciones[j][i*n+j] = -1

    return matriz_restricciones

def verificar_prob_minimizado(mat_variables_basicas, matriz_variables_decision, matriz_adyacencia = []):
    if matriz_adyacencia == []:
        matriz_adyacencia = np.tile(True, mat_variables_basicas.shape)

    for i, renglon in enumerate(matriz_variables_decision):
        for j, elemento in enumerate(renglon):
            if elemento > 0 and not mat_variables_basicas[i][j] and matriz_adyacencia[i][j]:
                return False
    return True

def convertir_graf_dir_a_noDir(matriz_adyacencia):
    matriz_no_dirigida = np.tile(False, matriz_adyacencia.shape)
    for i,renglon in enumerate(matriz_adyacencia):
        for j, elemento in enumerate(renglon):
            if elemento:
                matriz_no_dirigida[i][j] = True
                matriz_no_dirigida[j][i] = True
    return matriz_no_dirigida


def tachar_matriz(matriz, indice, ren_o_col):
    if ren_o_col == 0:
        for i, elemento in enumerate(matriz[indice, :]):
            matriz[indice][i] = elemento + 1
    elif ren_o_col == 1:
        for i, elemento in enumerate(matriz[:, indice]):
            matriz[i][indice] = elemento + 1
    return matriz


def numero_taches_matriz(matriz_cos):
    num_lineas = 0
    matriz_costos_aux = matriz_cos.copy()
    matriz_lineas = np.zeros(matriz_cos.shape)

    while np.any(matriz_costos_aux == 0):
        mayor_cantidad_ceros = (0, 0, 0)  ### (# de 0s, indice, renglón(0) o columna(1))
        cantidad_ceros = 0

        for index, renglon in enumerate(matriz_costos_aux):
            cantidad_ceros = (renglon == 0).sum()
            if mayor_cantidad_ceros[0] < cantidad_ceros:
                mayor_cantidad_ceros = (cantidad_ceros, index, 0)

        for index, columna in enumerate(matriz_costos_aux.transpose()):
            cantidad_ceros = (columna == 0).sum()
            if mayor_cantidad_ceros[0] < cantidad_ceros:
                mayor_cantidad_ceros = (cantidad_ceros, index, 1)

        if mayor_cantidad_ceros[2] == 0:
            matriz_costos_aux[mayor_cantidad_ceros[1]] = np.tile(
                1000, matriz_cos.shape[0]
            )
        else:
            matriz_costos_aux[:, mayor_cantidad_ceros[1]] = np.tile(
                1000, matriz_cos.shape[1]
            )

        matriz_lineas = tachar_matriz(
            matriz_lineas, mayor_cantidad_ceros[1], mayor_cantidad_ceros[2]
        )
        num_lineas += 1

        menor = np.amin(matriz_costos_aux)

    return matriz_lineas, num_lineas, menor