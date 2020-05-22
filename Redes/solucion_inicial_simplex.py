### solucion_inicial_simplex ###

from classes.problemas_optimizacion import ProblemaRedes

from utils.fun_vec_mat import convertir_graf_dir_a_noDir
from utils.fun_vec_mat import calculo_variables_duales
from utils.fun_vec_mat import ciclo_minimo
from utils.fun_vec_mat import obtener_variable_salida

from utils.Functions import clear_screen

from Redes.solucion_redes_simplex import simplex_redes
from Redes.balance_redes import balance_red
from Redes.FloydWarshal import MetodoFloyd

import numpy as np

def m_grande(matriz_adyacencia, matriz_costos, capacidades, nombres):
	if capacidades.sum() != 0:
		matriz_adyacencia, matriz_costos, capacidades, nombres = balance_red(matriz_adyacencia, matriz_costos, capacidades, nombres)

	### Agregando nodo artificial
	matriz_adyacencia = np.append(matriz_adyacencia, np.tile(False, (matriz_adyacencia.shape[0],1)), axis = 1)
	matriz_adyacencia = np.append(matriz_adyacencia, np.tile(False, (1, matriz_adyacencia.shape[1])), axis = 0)

	matriz_variables_basicas = np.tile(False, matriz_adyacencia.shape)
	matriz_variables_decision = np.zeros(matriz_adyacencia.shape)

	matriz_costos = np.append(matriz_costos, np.tile(0, (matriz_costos.shape[0],1)), axis = 1)
	matriz_costos = np.append(matriz_costos, np.tile(0, (1, matriz_costos.shape[1])), axis = 0)


	nodo_art = matriz_costos.shape[0]-1

	for i, capacidad in enumerate(capacidades):
		capacidad_0_asignada = False
		if capacidad > 0:
			matriz_adyacencia[i][nodo_art] = True
			matriz_variables_basicas[i][nodo_art] = True
			matriz_variables_decision[i][nodo_art] = capacidad
			matriz_costos[i][nodo_art] = 9999
		elif capacidad < 0:
			matriz_adyacencia[nodo_art][i] = True
			matriz_variables_basicas[nodo_art][i] = True
			matriz_variables_decision[nodo_art][i] = -1*capacidad
			matriz_costos[nodo_art][i] = 9999

		
	num_ceros = 0
	while num_ceros != (capacidades == 0).sum():
		for i, capacidad in enumerate(capacidades):
			for j, elemento in enumerate(matriz_adyacencia[i]):
				if capacidad == 0 and matriz_adyacencia[i][j] and (matriz_variables_basicas[i].sum() != 0 or matriz_variables_basicas[j].transpose().sum() != 0):
					matriz_variables_basicas[i][j] = True
					matriz_variables_decision[i][j] = 0
					num_ceros = num_ceros + 1 
					break
				elif capacidad == 0 and matriz_adyacencia[j][i] and (matriz_variables_basicas[i].sum() != 0 or matriz_variables_basicas[j].transpose().sum() != 0):
					matriz_variables_basicas[j][i] = True
					matriz_variables_decision[j][i] = 0
					num_ceros = num_ceros + 1 
					break

	
	capacidades = np.append(capacidades,0)

	red_inicial = ProblemaRedes(matriz_adyacencia, matriz_costos, capacidades, nombres)
	red_inicial.matriz_variables_basicas = matriz_variables_basicas.flatten()
	red_inicial.matriz_variables_decision = matriz_variables_decision.flatten()

	con_basicas_art_ren = red_inicial.matriz_variables_basicas[nodo_art].sum()
	con_basicas_art_col = red_inicial.matriz_variables_basicas.transpose()[nodo_art].sum()

	while not ((con_basicas_art_ren == 1 and con_basicas_art_col == 0) or 
				(con_basicas_art_ren == 0 and con_basicas_art_col == 1)):

		### m grande ###
		var_entrada = (np.NINF, -1, -1)
		var_salida = (np.inf, -1, -1)

		### Calculo variables duales ###
		variables_duales = calculo_variables_duales(red_inicial.matriz_variables_basicas, red_inicial.matriz_costos, nodo_art)

		### Calculo precios sombra ###
		for i, renglon in enumerate(red_inicial.matriz_adyacencia):
			for j, elemento in enumerate(renglon):
				if elemento and not red_inicial.matriz_variables_basicas[i][j]:
					red_inicial.matriz_variables_decision[i][j] = variables_duales[i] - variables_duales[j] - red_inicial.matriz_costos[i][j]

		### Identificando variable de entrada
		for i, renglon in enumerate(red_inicial.matriz_variables_decision):
			for j, elemento in enumerate(renglon):
				if elemento > var_entrada[0] and red_inicial.matriz_adyacencia[i][j] and not red_inicial.matriz_variables_basicas[i][j]:
					var_entrada = (elemento, i, j)

		### Ciclo de balance ###
		ciclo = ciclo_minimo(red_inicial.matriz_variables_basicas, var_entrada)


		### Calculo de variables de salida ###
		var_salida = obtener_variable_salida(red_inicial.matriz_variables_basicas, red_inicial.matriz_variables_decision, ciclo)


		### Balanceo ###
		for nodo in range(0,len(ciclo)-1,1):
			i = nodo
			j = nodo+1
			if red_inicial.matriz_variables_basicas[ciclo[i]][ciclo[j]]:
				red_inicial.matriz_variables_decision[ciclo[i]][ciclo[j]] -= var_salida[0]
			else:
				red_inicial.matriz_variables_decision[ciclo[j]][ciclo[i]] += var_salida[0]

		red_inicial.matriz_variables_basicas[var_entrada[1]][var_entrada[2]] = True		
		red_inicial.matriz_variables_decision[var_entrada[1]][var_entrada[2]] = var_salida[0]

		red_inicial.matriz_variables_basicas[var_salida[1]][var_salida[2]] = False

		con_basicas_art_ren = red_inicial.matriz_variables_basicas[nodo_art].sum()
		con_basicas_art_col = red_inicial.matriz_variables_basicas.transpose()[nodo_art].sum()


	if con_basicas_art_ren == 1:
		raiz = np.where(red_inicial.matriz_variables_basicas[nodo_art])[0]
	else:
		raiz = np.where(red_inicial.matriz_variables_basicas.transpose()[nodo_art])[0]

	### Eliminando nodo artificial ###
	matriz_adyacencia = np.delete(red_inicial.matriz_adyacencia, obj = nodo_art, axis = 0)
	matriz_adyacencia = np.delete(matriz_adyacencia, obj= nodo_art, axis = 1)

	matriz_costos = np.delete(red_inicial.matriz_costos, obj = nodo_art, axis = 0)
	matriz_costos = np.delete(matriz_costos, obj= nodo_art, axis = 1)

	matriz_variables_basicas = np.delete(red_inicial.matriz_variables_basicas, obj= nodo_art, axis = 0)
	matriz_variables_basicas = np.delete(matriz_variables_basicas, obj= nodo_art, axis = 1)

	matriz_variables_decision = np.delete(red_inicial.matriz_variables_decision, obj= nodo_art, axis = 0)
	matriz_variables_decision = np.delete(matriz_variables_decision, obj= nodo_art, axis = 1)

	capacidades = np.delete(capacidades, obj = nodo_art, axis = 0)

	prob_redes = ProblemaRedes(matriz_adyacencia, matriz_costos, capacidades, nombres)

	prob_redes.matriz_variables_basicas = matriz_variables_basicas.flatten()
	prob_redes.matriz_variables_decision = matriz_variables_decision.flatten()
	prob_redes.raiz = raiz


	return simplex_redes(prob_redes)

def solucion_inicial_manual(adyacencia, costos, capacidades, nombres):
	clear_screen()
	if np.sum(capacidades) != 0:
		print("""Dado que su problema no está balanceado, para evitar algún inconveniente \n
		No permitimos una asignación manual de variables básicas, le pedimos que \n
		utilice la opción del método de M grande""")
		return None


	matriz_variables_basicas = np.tile(False, adyacencia.shape)
	matriz_variables_decision = np.zeros(adyacencia.shape)

	capacidades_aux = capacidades.copy()

	num_nodos = adyacencia.shape[0] - 1

	for i in range(0, num_nodos, 1):
		print("Ingresando variables básicas")
		opcion = 'S'
		while opcion == 'S' or opcion == 's':
			i = int(input("Ingrese el nodo desde el que surje el flujo: ")) - 1
			j = int(input("Ingrese el nodo al que se dirige el flujo: ")) - 1
			flujo = float(input("Ingrese el flujo de  {0} a {1}: ".format(nombres[i],nombres[j])))
			opcion = input("¿Está seguro de los valores?(S/n): ")
			if (i < 0 or i > num_nodos or j < 0 or j > num_nodos or flujo < 0):
				print("Ingresó un valor inválido, inténtelo de nuevo")
				opcion = 'S'
			elif not adyacencia[i][j]:
				print("El flujo que ingresó no existe, inténtelo de nuevo")
			else:
				matriz_variables_basicas[i][j] = True
				matriz_variables_decision[i][j] = flujo
				break

	for i, renglon in enumerate(matriz_variables_basicas):
		for j, elemento in enumerate(renglon):
			if i < j and matriz_variables_basicas[i][j]:
				capacidades_aux[i] = capacidades_aux[i] - matriz_variables_decision[i][j]
				capacidades_aux[j] = capacidades_aux[j] + matriz_variables_decision[i][j]
			elif i > j and matriz_variables_basicas[i][j]:
				capacidades_aux[j] = capacidades_aux[j] - matriz_variables_decision[j][i]
				capacidades_aux[i] = capacidades_aux[i] + matriz_variables_decision[j][i]

	if (capacidades_aux == 0).sum() == num_nodos + 1:
		prob_redes = ProblemaRedes(adyacencia, costos, capacidades, nombres)
		prob_redes.matriz_variables_basicas = matriz_variables_basicas.flatten()
		prob_redes.matriz_variables_decision = matriz_variables_decision.flatten()
		return simplex_redes(prob_redes)
	else:
		print("***Error*** La solución que ingresó no es factible...")
		input("Presione Enter para continuar...")
		return None


