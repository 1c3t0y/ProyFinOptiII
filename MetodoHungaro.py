	###### metodoHungaro ######
import numpy as np
import ProblemasOptimizacion as po

### Funciones de renglones ###

def menorElementoRenglon(renglon):
	menor = renglon[0]
	for elemento in renglon:
		if(elemento < menor):
			menor = elemento
	return menor


def hayNumeroEnRenglon(renglon,numero):
	for elemento in renglon:
		if(elemento == numero):
			return True
	return False

def contarNumeroEnRenglon(renglon,numero):
	total=0
	for elemento in renglon:
		if(elemento == numero):
			total += 1
	return total


### Funciones Matrices ###

def hayNumeroEnMatriz(matriz,numero):
	for renglon in matriz:
		for elemento in renglon:
			if(elemento==numero):
				return True
	return False

def menorElementoMatriz(matriz):
	menor = matriz[0][0]
	for renglon in matriz:
		for elemento in renglon:
			if(elemento < menor):
				menor = elemento
	return menor

def tacharMatrizLineas(matriz, indice, ren_o_col):
	if(ren_o_col == 0):
		for i,elemento in enumerate(matriz[indice,:]):
			matriz[indice][i] = elemento+1
	elif(ren_o_col == 1):
		for i,elemento in enumerate(matriz[:,indice]):
			matriz[i][indice] = elemento+1
	return matriz


def numeroTachesMatriz(matrizCos):
	numLineas = 0
	matrizCostosAux = matrizCos.copy()
	matrizLineas = np.zeros(matrizCos.shape)

	while(hayNumeroEnMatriz(matrizCostosAux,0)):
		mayorCantidadCeros = (0,0,0) ### (# de 0s, indice, renglón(0) o columna(1))
		cantidadCeros = 0

		for index,renglon in enumerate(matrizCostosAux):
			cantidadCeros = contarNumeroEnRenglon(renglon,0)
			if(mayorCantidadCeros[0] < cantidadCeros):
				mayorCantidadCeros = (cantidadCeros,index,0)

		for index,columna in enumerate(matrizCostosAux.transpose()):
			cantidadCeros = contarNumeroEnRenglon(columna,0)
			if(mayorCantidadCeros[0] < cantidadCeros):
				mayorCantidadCeros = (cantidadCeros,index,1)

		if(mayorCantidadCeros[2] == 0):
			matrizCostosAux[mayorCantidadCeros[1]] = np.tile(1000,matrizCos.shape[0])
		else:
			matrizCostosAux[:,mayorCantidadCeros[1]] = np.tile(1000,matrizCos.shape[1])

		matrizLineas = tacharMatrizLineas(matrizLineas, mayorCantidadCeros[1], mayorCantidadCeros[2])
		numLineas += 1

		menor = menorElementoMatriz(matrizCostosAux)

	return matrizLineas, numLineas, menor


def metodoHungaro(probAsignacion):

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
	matrizCostosOpti = probAsignacion.matrizCostos
	### Paso 1
	for renglon in matrizCostosOpti:
		menor = menorElementoRenglon(renglon)
		for index,elemento in enumerate(renglon):
			renglon[index] = elemento - menor

	### Paso 2 
	matrizTransAux = matrizCostosOpti.transpose()

	for renglon in matrizTransAux:
		if(not hayNumeroEnRenglon(renglon,0)):
			menor = menorElementoRenglon(renglon)
			for index,elemento in enumerate(renglon):
				renglon[index] = elemento - menor

	matrizCostosOpti = matrizTransAux.transpose()

	### Paso 3
	matrizLineas, numLineas, menor = numeroTachesMatriz(matrizCostosOpti)

	while(numLineas < matrizCostosOpti.shape[0]):
		for i,renglon in enumerate(matrizLineas):
			for j,elemento in enumerate(renglon):
				if(elemento == 2):
					matrizCostosOpti[i][j]=matrizCostosOpti[i][j]+menor
				elif(elemento == 0):
					matrizCostosOpti[i][j]=matrizCostosOpti[i][j]-menor
		print(matrizCostosOpti)
		matrizLineas, numLineas, menor = numeroTachesMatriz(matrizCostosOpti)



matCostos = np.array([[20,25,22,28],[15,18,23,17],[19,17,21,24],[25,23,24,24]])
matrizHungaro = po.ProblemaAsignacion(matCostos)

metodoHungaro(matrizHungaro)
