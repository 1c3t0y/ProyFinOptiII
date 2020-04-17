###### metodoHungaro ######

import numpy as np

import problemas_optimizacion as po
import fun_vec_mat as fvm


def metodo_hungaro(prob_asignacion):

    """
	#####################################################################
	#			Método húngaro para problemas de asignación				#
	#																	#
	#	Taha, H(2017)Investigación de operaciones.(10ma. ed.) México:	#
	#	Pearson Educación de México.									#
	#																	#
	#	*Paso 1. Determine p_i, el elemento de costo mínimo de la fila 	#
	#	i de la matriz de costos original, y réstelo de todos los ele-	#
	#	mentos de la fila i, i=1,2,3									#
	#																	#	
	#	*Paso 2. Para la matriz creada en el paso 1, determine q_j, el 	#
	#	elemento de un costo mínimo de la columna j, y réstelo de todos #
	#	los elementos de la columna j,j=1,2,3							#
	#																	#
	#	*Paso 3. A partir de la matriz del paso 2, intente determinar 	#
	#	una asignación factible entre todas las entradas cero resultan-	#
	#	tes.															#
	#																	#
	#	Paso 3															#	
	#####################################################################
	"""
    matriz_costos_opti = prob_asignacion.matriz_costos
    ### Paso 1
    for renglon in matriz_costos_opti:
        menor = np.amin(renglon)
        for index, elemento in enumerate(renglon):
            renglon[index] = elemento - menor

    ### Paso 2
    matriz_trans_aux = matriz_costos_opti.transpose()

    for renglon in matriz_trans_aux:
        if not np.any(renglon == 0):
            menor = np.amin(renglon)
            for index, elemento in enumerate(renglon):
                renglon[index] = elemento - menor

    matriz_costos_opti = matriz_trans_aux.transpose()

    ### Paso 3
    matriz_lineas, num_lineas, menor = fvm.numero_taches_matriz(matriz_costos_opti)

    while num_lineas < matriz_costos_opti.shape[0]:
        for i, renglon in enumerate(matriz_lineas):
            for j, elemento in enumerate(renglon):
                if elemento == 2:
                    matriz_costos_opti[i][j] = matriz_costos_opti[i][j] + menor
                elif elemento == 0:
                    matriz_costos_opti[i][j] = matriz_costos_opti[i][j] - menor
        print(matriz_costos_opti)
        matriz_lineas, num_lineas, menor = fvm.numero_taches_matriz(matriz_costos_opti)
