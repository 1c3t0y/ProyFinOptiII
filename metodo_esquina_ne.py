### Metodo Esquina Noroeste ###

import numpy as np

import problemas_optimizacion as po
import fun_vec_mat as fvm
import sol_problemas_opti as spo


def metodo_esquina_NE(prob_transporte):
    oferta_aux = prob_transporte.oferta
    demanda_aux = prob_transporte.demanda
    mat_variables_basicas = np.tile(False, (prob_transporte.n, prob_transporte.m))
    taches_ren = np.tile(False, prob_transporte.n)
    taches_col = np.tile(False, prob_transporte.m)
    num_taches_ren = 0
    num_taches_col = 0
    i = 0
    j = 0

    while not (
        (num_taches_ren == 1 and num_taches_col == 0)
        or (num_taches_ren == 0 and num_taches_col == 1)
    ):
        ### Paso 1
        menor = min(oferta_aux[i], demanda_aux[j])
        prob_transporte.matriz_variables_decision[i][j] = menor
        mat_variables_basicas[i][j] = True
        oferta_aux[i] = oferta_aux[i] - menor
        demanda_aux[j] = demanda_aux[j] - menor

        ### Paso 2
        if (oferta_aux[i] == 0 and demanda_aux[j] == 0) or oferta_aux[i] == 0:
            taches_ren[i] = True
            i += 1
        else:
            taches_col[j] = True
            j += 1

        ### Paso 3
        num_taches_ren = (taches_ren == False).sum()
        num_taches_col = (taches_col == False).sum()

    return spo.solucion_problema_transporte(prob_transporte, mat_variables_basicas)


#costos = np.array([[10, 2, 20, 11], [12, 7, 9, 20], [4, 14, 16, 18]])
#oferta = np.array([15, 25, 10])
#demanda = np.array([5, 15, 15, 15])
#probTransporte = po.ProblemaTransporte(3, 4, costos, oferta, demanda)
#print(metodo_esquina_NE(probTransporte).matriz_variables_decision)