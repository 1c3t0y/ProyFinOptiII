import numpy as np

### Algoritmo de Optimizacion para problemas de transporte ###

def solucion_problema_transporte(prob_transporte):
    u = []
    v = []
    var_entrada = (0, -1, -1)
    var_salida = (0, -1, -1)

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
                if prob_transporte.matriz_variables_basicas[i][j] and u[i] != "*" and v[j] == "*":
                    v[j] = prob_transporte.matriz_costos[i][j] - u[i]

        for j in range(prob_transporte.m):
            for i in range(prob_transporte.n):
                if prob_transporte.matriz_variables_basicas[i][j] and v[j] != "*" and u[i] == "*":
                    u[i] = prob_transporte.matriz_costos[i][j] - v[j]

        if u_aux == u and v_aux == v:
            for i, elemento in enumerate(u):
                if elemento == "*":
                    u[i] = 0
                    break

    ### Calculo de variables no básicas
    for i, renglon in enumerate(prob_transporte.matriz_variables_decision):
        for j, elemento in enumerate(renglon):
            if not prob_transporte.matriz_variables_basicas[i][j]:
                prob_transporte.matriz_variables_decision[i][j] = (
                    u[i] + v[j] - prob_transporte.matriz_costos[i][j]
                )
    
    ### Condicion de salida ###
    if verificar_minimo_encontrado(prob_transporte.matriz_variables_basicas, prob_transporte.matriz_variables_decision):
        return prob_transporte

    ### Identificando variable de entrada
    for i, renglon in enumerate(prob_transporte.matriz_variables_decision):
        for j, elemento in enumerate(renglon):
            if elemento >= var_entrada[0] and (not prob_transporte.matriz_variables_basicas[i][j]):
                var_entrada = (elemento, i, j)

    mat_ciclo_min = ciclo_minimo(prob_transporte.matriz_variables_basicas, var_entrada)
    prob_transporte.matriz_variables_basicas[var_entrada[1], var_entrada[2]] = True ## Se mete la variable a la base
    mat_flujos = asignar_flujos(mat_ciclo_min, var_entrada)
    var_salida = (np.amax(prob_transporte.matriz_variables_decision), -1, -1)

    for i, renglon in enumerate(prob_transporte.matriz_variables_decision):
        for j, elemento in enumerate(renglon):
            if mat_ciclo_min[i][j] and var_salida[0] >= elemento and mat_flujos[i][j] == '-':
                var_salida = (elemento, i, j) 

    for i, renglon in enumerate(prob_transporte.matriz_variables_decision):
        for j, elemento in enumerate(renglon):
            if mat_ciclo_min[i][j]:
                if mat_flujos[i][j] == '+':
                    prob_transporte.matriz_variables_decision[i][j] += var_salida[0]
                else:
                    prob_transporte.matriz_variables_decision[i][j] -= var_salida[0]

    prob_transporte.matriz_variables_decision[var_entrada[1], var_entrada[2]] = var_salida[0]
    prob_transporte.matriz_variables_basicas[var_salida[1], var_salida[2]] = False ## Se saca la variable de la base

    return solucion_problema_transporte(prob_transporte)



def asignar_flujos(mat_ciclo_min, var_entrada):
    mat_flujos = np.tile('.', mat_ciclo_min.shape)
    lista_elementos_ciclo = []
    lista_elementos_ciclo.append([var_entrada[1], var_entrada[2], "+"])
   
    for i, renglon in enumerate(mat_ciclo_min):
        for j, elemento in enumerate(renglon):
            if((i,j) != (var_entrada[1], var_entrada[2]) and elemento):
                lista_elementos_ciclo.append([i,j,"."])

    #Se asignan flujos a los elementos de la 
    for actual in lista_elementos_ciclo:
        for j, elemento in enumerate(lista_elementos_ciclo):
            if actual != elemento and elemento[2] == "."  and ( actual[0] == elemento[0] or actual[1] == elemento[1] ):
                if actual[2] == '+':
                    lista_elementos_ciclo[j][2] = "-"
                elif actual[2] == '-':
                    lista_elementos_ciclo[j][2] = "+"

    for i in lista_elementos_ciclo:
        mat_flujos[i[0]][i[1]] = i[2]

    return mat_flujos



def ciclo_minimo(mat_variables_basicas, var_entrada):
    mat_ciclo_min = mat_variables_basicas.copy()
    mat_ciclo_min[var_entrada[1],var_entrada[2]] = True
    ciclo_minimo_encontrado = False

    while not ciclo_minimo_encontrado:

        mat_ciclo_min_aux = mat_ciclo_min.copy()

        ## Eliminando renglones con sólo un elemento
        for i, renglon in enumerate(mat_ciclo_min):
            if(renglon == True).sum() == 1:
                for j, elemento in enumerate(renglon):
                    mat_ciclo_min[i][j] = False

        ## Eliminando columnas con sólo un elemento
        mat_ciclo_min = mat_ciclo_min.transpose()

        for j, columna in enumerate(mat_ciclo_min):
            if(columna == True).sum() == 1:
                for i, elemento in enumerate(columna):
                    mat_ciclo_min[j][i] = False

        mat_ciclo_min = mat_ciclo_min.transpose()

        ## Verificando si no hubo cambios en la matriz, 
        ## entonces se encontro la matriz con los elementos del ciclo minimo
        if np.array_equal(mat_ciclo_min, mat_ciclo_min_aux):
            ciclo_minimo_encontrado = True

    return mat_ciclo_min

def verificar_minimo_encontrado(mat_variables_basicas, matriz_variables_decision):
    for i, renglon in enumerate(matriz_variables_decision):
        for j, elemento in enumerate(renglon):
            if elemento > 0 and mat_variables_basicas[i][j] == False:
                return False
    return True