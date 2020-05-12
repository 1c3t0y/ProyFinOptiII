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
