### Solucion Algortimo redes a costo mínimo ###

from utils.fun_vec_mat import verificar_prob_minimizado
from utils.fun_vec_mat import convertir_graf_dir_a_noDir
from classes.problemas_optimizacion import ProblemaRedes
from Redes.FloydWarshal import MetodoFloyd
import numpy as np

def solucion_mcfp(prob_redes):
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

	return solucion_mcfp(prob_redes)


	
	

def calculo_variables_duales(matriz_variables_basicas, matriz_costos, indice_nodo_art):
	valor_variables_duales = np.zeros(matriz_variables_basicas.shape[0])
	vd_asignadas = np.tile(False, matriz_variables_basicas.shape[0])

	vd_asignadas[indice_nodo_art] = True

	while vd_asignadas.sum() != len(vd_asignadas):
		for i, renglon in enumerate(matriz_variables_basicas):
			for j, elemento in enumerate(renglon):
				if elemento and vd_asignadas[j] and not vd_asignadas[i]:
					valor_variables_duales[i] = valor_variables_duales[j] + matriz_costos[i][j]
					vd_asignadas[i] = True
				elif elemento and vd_asignadas[i] and not vd_asignadas[j]:
					valor_variables_duales[j] = valor_variables_duales[i] - matriz_costos[i][j]
					vd_asignadas[j] = True
	print(vd_asignadas)
	print(valor_variables_duales)
	input("Presiona enter :v...")
	return valor_variables_duales

def ciclo_minimo(matriz_variables_basicas, var_entrada):
	print("Buscando ciclo_minimo...")
	matriz_no_dirigida = convertir_graf_dir_a_noDir(matriz_variables_basicas)
	matriz_pesos = np.tile(np.inf,matriz_variables_basicas.shape)
	for i, renglon in enumerate(matriz_no_dirigida):
		for j, elemento in enumerate(renglon):
			if elemento:
				matriz_pesos[i][j]=1
			elif i == j:
				matriz_pesos[i][j]=0
	floyd = MetodoFloyd(matriz_pesos)
	floyd.resolver()
	print(floyd.matriz_rutas)
	ruta = floyd.calcular_ruta(var_entrada[1],var_entrada[2])

	for i in range(0,len(ruta),1):
		ruta[i] -=1

	return ruta

def obtener_variable_salida(matriz_variables_basicas, matriz_variables_decision, ruta):
	minimo = (np.inf, -1, -1)
	for nodo in range(0, len(ruta)-1,1):
		i = nodo
		j= nodo+1
		if  matriz_variables_basicas[ruta[i]][ruta[j]] and matriz_variables_decision[ruta[i]][ruta[j]] < minimo[0]:
			minimo = (matriz_variables_decision[ruta[i]][ruta[j]], ruta[i], ruta[j])
	return minimo
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