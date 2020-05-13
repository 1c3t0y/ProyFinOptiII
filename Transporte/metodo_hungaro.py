###### metodoHungaro ######

import numpy as np
import utils.fun_vec_mat as fvm
from Transporte.sol_problemas_opti import solucion_problema_asignacion


def metodo_hungaro(prob_asignacion):

    """
    #####################################################################
    #           Método húngaro para problemas de asignación             #
    #                                                                   #
    #   Taha, H(2017)Investigación de operaciones.(10ma. ed.) México:   #
    #   Pearson Educación de México.                                    #
    #                                                                   #
    #   *Paso 1. Determine p_i, el elemento de costo mínimo de la fila  #
    #   i de la matriz de costos original, y réstelo de todos los ele-  #
    #   mentos de la fila i, i=1,2,3                                    #
    #                                                                   #   
    #   *Paso 2. Para la matriz creada en el paso 1, determine q_j, el  #
    #   elemento de un costo mínimo de la columna j, y réstelo de todos #
    #   los elementos de la columna j,j=1,2,3                           #
    #                                                                   #
    #   *Paso 3. A partir de la matriz del paso 2, intente determinar   #
    #   una asignación factible entre todas las entradas cero resultan- #
    #   tes.                                                            #
    #                                                                   #
    #   Paso 3                                                          #   
    #####################################################################
    """
    prob_asignacion.matriz_asignacion = prob_asignacion.matriz_costos.copy()
    ### Paso 1
    for renglon in prob_asignacion.matriz_asignacion:
        menor = np.amin(renglon)
        for index, elemento in enumerate(renglon):
            renglon[index] = elemento - menor

    ### Paso 2
    matriz_trans_aux = prob_asignacion.matriz_asignacion.transpose()

    for renglon in matriz_trans_aux:
        if not np.any(renglon == 0):
            menor = np.amin(renglon)
            for index, elemento in enumerate(renglon):
                renglon[index] = elemento - menor

    prob_asignacion.matriz_asignacion = matriz_trans_aux.transpose()

    ### Paso 3
    matriz_lineas, num_lineas, menor = fvm.numero_taches_matriz(
        prob_asignacion.matriz_asignacion
    )

    while num_lineas < prob_asignacion.matriz_asignacion.shape[0]:
        for i, renglon in enumerate(matriz_lineas):
            for j, elemento in enumerate(renglon):
                if elemento == 2:
                    prob_asignacion.matriz_asignacion[i][j] = (
                        prob_asignacion.matriz_asignacion[i][j] + menor
                    )
                elif elemento == 0:
                    prob_asignacion.matriz_asignacion[i][j] = (
                        prob_asignacion.matriz_asignacion[i][j] - menor
                    )
        matriz_lineas, num_lineas, menor = fvm.numero_taches_matriz(
            prob_asignacion.matriz_asignacion
        )

    return solucion_problema_asignacion(
        prob_asignacion, prob_asignacion.matriz_asignacion.copy()
    )


# costos = np.array([[1,4,6,3],[9,7,10,9],[4,5,11,7],[8,7,8,5]])
# prob_asignacion = po.ProblemaAsignacion(costos)
# prob_asignacion = metodo_hungaro(prob_asignacion)
# print(prob_asignacion.matriz_asignacion)
# print(prob_asignacion.matriz_variables_decision)
