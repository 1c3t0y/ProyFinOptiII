### Metodo de aproximacion de Voguel ###

import numpy as np
import Transporte.sol_problemas_opti as spo
from classes.problemas_optimizacion import ProblemaTransporte


def metodo_MAV(matriz_costos, oferta, demanda, nombres_origen, nombres_destino):
	prob_transporte = ProblemaTransporte(matriz_costos, oferta, demanda, nombres_origen, nombres_destino)
	mat_variables_basicas = np.tile(False, (prob_transporte.n, prob_transporte.m))

	oferta_aux = prob_transporte.oferta.copy()
	demanda_aux = prob_transporte.demanda.copy()


	penalizacion_ren = np.tile(0., prob_transporte.n)
	penalizacion_col = np.tile(0., prob_transporte.m)
	penalizacion_mayor = (0.,False, -1) ###(Valor penalizacion, False = renglon / True = columna, indice)

	taches_ren = np.tile(False, prob_transporte.n)
	taches_col = np.tile(False, prob_transporte.m)
	num_taches_ren = 0
	num_taches_col = 0

	contador = 0

	while not (
	 	  (num_taches_ren == 1 and num_taches_col == 0 and oferta_aux.sum() == 0)
	  	  or (num_taches_ren == 0 and num_taches_col == 1 and demanda_aux.sum() == 0)
	):

		
		### paso 1
		for i, renglon in enumerate(prob_transporte.matriz_costos): ### se Recorre la matriz de costos
			costo_menor = np.amax(renglon)  ### SE inicializan variables auxiliares para guardar costos menor
			seg_costo_menor = np.amax(renglon) ###  y segundo costo menor con el costo más alto del renglon
			for j, elemento in enumerate(renglon):
				if not taches_ren[i] and not taches_col[j] and elemento <= costo_menor:#Si el costo que se está recoriiendo es menor que el auxiliar y no está tachado ni su renglón ni su matriz
					seg_costo_menor = costo_menor ### el que se creía costo menor se pasa a ser el segundo costo menor
					costo_menor = elemento ### el costo que se esta recorriendo se convierte en el nuevo costo menor
				elif not taches_ren[i] and not taches_col[j] and elemento <= seg_costo_menor: ### en caso de que el costo actual no sea menor que costo menor, pero si que segundo costo menor
					seg_costo_menor = elemento ## se le asigna ese valor al segundo costo menor
			penalizacion_ren[i] = seg_costo_menor - costo_menor ### por cada iteracion se almacena la penalizacion


		### se hace exactamente lo mismo, pero con las columnas
		for j, columna in enumerate(prob_transporte.matriz_costos.transpose()):
			costo_menor = np.amax(columna)
			seg_costo_menor = np.amax(columna)
			for i, elemento in enumerate(columna):
				if not taches_ren[i] and not taches_col[j] and elemento <= costo_menor:
					seg_costo_menor = costo_menor
					costo_menor = elemento
				elif not taches_ren[i] and not taches_col[j] and elemento <= seg_costo_menor:
					seg_costo_menor = elemento
			penalizacion_col[j] = seg_costo_menor - costo_menor


		### paso 2
		penalizacion_mayor = (penalizacion_ren[0], False, 0)
		for i, elemento in enumerate(penalizacion_ren):
			if elemento > penalizacion_mayor[0]:
				penalizacion_mayor = (elemento, False, i) ## Aqui se decide cual es la penalizacion menor y en qué renglon esta
		
		for j, elemento in enumerate(penalizacion_col):
			if elemento > penalizacion_mayor[0]:## Si en las columnas hay una penalizacion menor a la que hay en los renglones
				penalizacion_mayor = (elemento, True, j) ## se decide cual es la penalizacion menor y en qué columna esta
		

		costo_menor = (np.amax(prob_transporte.matriz_costos), -1, -1)
		
		### Paso 3
		if not penalizacion_mayor[1]:
			for j, elemento in enumerate(prob_transporte.matriz_costos[penalizacion_mayor[2]]):
				if not taches_col[j] and elemento <= costo_menor[0]:
					costo_menor = (elemento, penalizacion_mayor[2], j)
		else:
			for i, elemento in enumerate(prob_transporte.matriz_costos.transpose()[penalizacion_mayor[2]]):
				if not taches_ren[i] and elemento <= costo_menor[0]:
					costo_menor = (elemento, i, penalizacion_mayor[2])


		menor = min(oferta_aux[costo_menor[1]], demanda_aux[costo_menor[2]])
		prob_transporte.matriz_variables_decision[costo_menor[1]][costo_menor[2]] = menor
		oferta_aux[costo_menor[1]] = oferta_aux[costo_menor[1]] - menor
		demanda_aux[costo_menor[2]] = demanda_aux[costo_menor[2]] - menor
		mat_variables_basicas[costo_menor[1]][costo_menor[2]] = True


		if demanda_aux[costo_menor[2]] == 0:
			taches_col[costo_menor[2]] = True
		elif oferta_aux[costo_menor[1]] == 0:
			taches_ren[costo_menor[1]] = True

		num_taches_ren = (taches_ren == False).sum()
		num_taches_col = (taches_col == False).sum()


		### Condicion (b)
		if num_taches_ren == 1 and num_taches_col == 1 and np.sum(oferta_aux) > 0:
			for i, elemento in enumerate(taches_ren):
				if not elemento:
					ren_faltante = i

			costo_menor = (np.amax(prob_transporte.matriz_costos[ren_faltante]), -1, -1)
			for j, elemento in enumerate(prob_transporte.matriz_costos[ren_faltante]):
				if not taches_col[j] and elemento <= costo_menor[0]:
					costo_menor = (elemento, ren_faltante, j)


			prob_transporte.matriz_variables_decision[costo_menor[1]][costo_menor[2]] = oferta_aux[costo_menor[1]]
			mat_variables_basicas[costo_menor[1]][costo_menor[2]] = True
			demanda_aux[costo_menor[2]] = demanda_aux[costo_menor[2]] - oferta_aux[costo_menor[1]] 			
			oferta_aux[costo_menor[1]] = 0
			taches_ren[costo_menor[1]] = True
			num_taches_ren = (taches_ren == False).sum()
			num_taches_col = (taches_col == False).sum()

		elif num_taches_col == 1 and num_taches_ren == 1 and np.sum(demanda_aux) > 0:
			for i, elemento in enumerate(taches_col):
				if not elemento:
					col_faltante = i

			costo_menor = (np.amax(prob_transporte.matriz_costos.transpose()[col_faltante]), -1, -1)
			for i, elemento in enumerate(prob_transporte.matriz_costos.transpose()[col_faltante]):
				if not taches_ren[i] and elemento <= costo_menor[0]:
					costo_menor = (elemento, i, col_faltante)

			prob_transporte.matriz_variables_decision[costo_menor[1]][costo_menor[2]] = oferta_aux[costo_menor[1]]
			mat_variables_basicas[costo_menor[1]][costo_menor[2]] = True
			oferta_aux[costo_menor[1]] = oferta_aux[costo_menor[1]] - demanda_aux[costo_menor[2]]  
			demanda_aux[costo_menor[2]] = 0
			taches_col[costo_menor[2]] = True
			num_taches_ren = (taches_ren == False).sum()
			num_taches_col = (taches_col == False).sum()

		
		### Condicion (c)
		while np.sum(oferta_aux) == 0 and np.sum(demanda_aux) == 0 and num_taches_ren > 0  and num_taches_col > 0:
			if num_taches_ren > 0 and num_taches_col > 0:
				for i, renglon in enumerate(prob_transporte.matriz_costos):
					costo_menor = (np.amax(renglon),-1 ,-1)
					for j, elemento in enumerate(renglon):
						if not taches_ren[i] and not taches_col[j] and elemento <= costo_menor[0]:
							costo_menor = (elemento, i ,j)
					prob_transporte.matriz_costos[costo_menor[1]][costo_menor[2]] = 0
					oferta_aux[i] = True
				num_taches_ren = (taches_ren == False).sum()
			
			if num_taches_col > 1 and num_taches_ren == 0:
				for j, columna in enumerate(prob_transporte.matriz_costos.transpose()):
					costo_menor = (np.amax(columna),-1 ,-1)
					for j, elemento in enumerate(renglon):
						if not taches_ren[i] and not taches_col[j] and elemento <= costo_menor:
							costo_menor = (elemento, i ,j)
					if (taches_col == False).sum() > 1:
						prob_transporte.matriz_costos[costo_menor[1]][costo_menor[2]] = 0
						oferta_aux[i] = True
				num_taches_col = (taches_col == False).sum()

	prob_transporte.matriz_variables_basicas = mat_variables_basicas.flatten()
		
	return spo.solucion_problema_transporte(prob_transporte)




#costos = np.array([[10, 2, 20, 11], [12, 7, 9, 20], [4, 14, 16, 18]])
#oferta = np.array([15, 25, 10])
#demanda = np.array([5, 15, 15, 15])
#probTransporte = po.ProblemaTransporte(3, 4, costos, oferta, demanda)

#print(metodo_MAV(probTransporte).matriz_variables_decision)