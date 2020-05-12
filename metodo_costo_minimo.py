### Método del costo minimo ###
import numpy as np
import sol_problemas_opti as spo


def metodo_costo_minimo(prob_transporte):
	oferta_aux = prob_transporte.oferta
	demanda_aux = prob_transporte.demanda
	mat_variables_basicas = np.tile(False, (prob_transporte.n, prob_transporte.m))
	taches_ren = np.tile(False, prob_transporte.n)
	taches_col = np.tile(False, prob_transporte.m)
	num_taches_ren = 0
	num_taches_col = 0


	while not (
	    (num_taches_ren == 1 and num_taches_col == 0)
	    or (num_taches_ren == 0 and num_taches_col == 1)
	):
		costo_menor = (np.amax(prob_transporte.matriz_costos), -1, -1)
		### Paso 1
		for i, renglon in enumerate(prob_transporte.matriz_costos):
			for j, elemento in enumerate(renglon):
				if not taches_col[j] and not taches_ren[i] and elemento <= costo_menor[0] :
					costo_menor = (elemento, i, j)


		menor = min(oferta_aux[costo_menor[1]], demanda_aux[costo_menor[2]])
		prob_transporte.matriz_variables_decision[costo_menor[1]][costo_menor[2]] = menor
		oferta_aux[costo_menor[1]] = oferta_aux[costo_menor[1]] - menor
		demanda_aux[costo_menor[2]] = demanda_aux[costo_menor[2]] - menor
		mat_variables_basicas[costo_menor[1]][costo_menor[2]] = True

		### Paso 2

		if oferta_aux[costo_menor[1]] == 0:
			taches_ren[costo_menor[1]] = True

		elif demanda_aux[costo_menor[2]] == 0:
			taches_col[costo_menor[2]] = True
		
		

		### Paso 3
		num_taches_ren = (taches_ren == False).sum()
		num_taches_col = (taches_col == False).sum()

	return spo.solucion_problema_transporte(prob_transporte, mat_variables_basicas)


#costos = np.array([[10, 2, 20, 11], [12, 7, 9, 20], [4, 14, 16, 18]])
#oferta = np.array([15, 25, 10])
#demanda = np.array([5, 15, 15, 15])
#probTransporte = po.ProblemaTransporte(3, 4, costos, oferta, demanda)
#print(metodo_costo_minimo(probTransporte).matriz_variables_decision)