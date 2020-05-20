### Solucion Algortimo redes a costo mínimo ###

from utils.fun_vec_mat import verificar_prob_minimizado
from utils.fun_vec_mat import convertir_graf_dir_a_noDir
from utils.fun_vec_mat import calculo_variables_duales
from utils.fun_vec_mat import ciclo_minimo
from utils.fun_vec_mat import obtener_variable_salida

from classes.problemas_optimizacion import ProblemaRedes

import numpy as np

def simplex_redes(prob_redes):
	var_entrada = (0, -1, -1)
	var_salida = (0, -1, -1)

	print("Inició variables duales")
	variables_duales = calculo_variables_duales(prob_redes.matriz_variables_basicas, prob_redes.matriz_costos, 4)

	### Calculo precios sombra ###
	for i, renglon in enumerate(prob_redes.matriz_adyacencia):
		for j, elemento in enumerate(renglon):
			if elemento and not prob_redes.matriz_variables_basicas[i][j]:
				prob_redes.matriz_variables_decision[i][j] = variables_duales[i]-variables_duales[j] - prob_redes.matriz_costos[i][j]

	### Condicion de salida ###
	if verificar_prob_minimizado(
		prob_redes.matriz_variables_basicas,
		prob_redes.matriz_variables_decision,
		prob_redes.matriz_adyacencia
	):
		return prob_redes

	### Identificando variable de entrada
	for i, renglon in enumerate(prob_redes.matriz_variables_decision):
		for j, elemento in enumerate(renglon):
			if elemento >= var_entrada[0] and prob_redes.matriz_adyacencia[i][j] and not prob_redes.matriz_variables_basicas[i][j]:
				var_entrada = (elemento, i, j)
	
	print(var_entrada)

	ciclo = ciclo_minimo(prob_redes.matriz_variables_basicas, var_entrada)

	print(ciclo)

	var_salida = obtener_variable_salida(prob_redes.matriz_variables_basicas, prob_redes.matriz_variables_decision, ciclo)

	print(var_salida)

	for nodo in range(0,len(ciclo)-1,1):
		i = nodo
		j = nodo+1
		if prob_redes.matriz_variables_basicas[ciclo[i]][ciclo[j]]:
			prob_redes.matriz_variables_decision[ciclo[i]][ciclo[j]] -= var_salida[0]
		else:
			prob_redes.matriz_variables_decision[ciclo[j]][ciclo[i]] += var_salida[0]

	prob_redes.matriz_variables_basicas[var_entrada[1]][var_entrada[2]] = True		
	prob_redes.matriz_variables_decision[var_entrada[1]][var_entrada[2]] = var_salida[0]

	prob_redes.matriz_variables_basicas[var_salida[1]][var_salida[2]] = False

	print(prob_redes.matriz_adyacencia)
	print(prob_redes.matriz_variables_basicas)
	print(prob_redes.matriz_variables_decision)
	print(prob_redes.z)

	return simplex_redes(prob_redes)

'''
matriz_adyacencia = np.array([
                                [False,True,True,False,False],
                                [False,False,False,True,True],
                                [False,False,False,True,True],
                                [False,False,False,False,True],
                                [False,False,False,False,False]
                            ])


matriz_costos = np.array([
	[9999,8,6,9999,9999], 
	[9999,9999,9999,5,7], 
	[9999,9999,9999,6,3], 
	[9999,9999,9999,9999,4],
	[9999,9999,9999,9999,9999]
	])

capacidades = np.array([6,0,4,-5,-5])

prob_redes = ProblemaRedes(matriz_adyacencia, matriz_costos, capacidades)

prob_redes.matriz_variables_decision = np.array([0,6,0,0,0,0,0,0,6,0,0,0,0,4,0,0,0,0,0,5,0,0,0,0,0])
print(prob_redes.matriz_variables_decision )
print(prob_redes.variables_decision )
prob_redes.matriz_variables_basicas = np.array([
	False,True,False,False,False,
	False,False,False,True,False,
	False,False,False,True,False,
	False,False,False,False,True,
	False,False,False,False,False
	])

print(solucion_mcfp(prob_redes))
'''