### Algoritmo de Optimizacion para problemas de transporte ###

import numpy as np


def solucion_problema_transporte(prob_transporte, mat_variables_basicas):
    u = []
    v = []
    var_entrada = (0, -1, -1)

    for i in range(prob_transporte.n):
        u.append("*")
    for j in range(prob_transporte.m):
        v.append("*")

    ### Calculo de multiplicadores
    u[0] = 0

    while "*" in u or "*" in v:
        u_aux = u.copy()
        v_aux = v.copy()

        for i in range(0, prob_transporte.n, 1):
            for j in range(0, prob_transporte.m, 1):
                if mat_variables_basicas[i][j] and u[i] != "*" and v[j] == "*":
                    v[j] = prob_transporte.matriz_costos[i][j] - u[i]

        for j in range(prob_transporte.m):
            for i in range(prob_transporte.n):
                if mat_variables_basicas[i][j] and v[j] != "*" and u[i] == "*":
                    u[i] = prob_transporte.matriz_costos[i][j] - v[j]

        if u_aux == u and v_aux == v:
            for i, elemento in enumerate(u):
                if elemento == "*":
                    u[i] = 0
                    break

    ### Calculo de variables no básicas
    for i, renglon in enumerate(prob_transporte.matriz_variables_decision):
        for j, elemento in enumerate(renglon):
            if not mat_variables_basicas[i][j]:
                prob_transporte.matriz_variables_decision[i][j] = (
                    u[i] + v[j] - prob_transporte.matriz_costos[i][j]
                )

    ### Identificando variable de entrada
    for i, renglon in enumerate(prob_transporte.matriz_variables_decision):
        for j, elemento in enumerate(renglon):
            if elemento > var_entrada[0] and (not mat_variables_basicas[i][j]):
                var_entrada = (elemento, i, j)

    mat_variables_basicas[var_entrada[1]][var_entrada[2]] = True
    ##cicloMinimo(mat_variables_basicas,(var_entrada[1],var_entrada[2]))

    ###if(varEntrada[0] > 0):
