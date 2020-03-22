	###### metodoHungaro ######
import numpy as np
import ProblemasOptimizacion as po
import FuncionesVecMat as fvm


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
		menor = fvm.menorElementoRenglon(renglon)
		for index,elemento in enumerate(renglon):
			renglon[index] = elemento - menor

	### Paso 2 
	matrizTransAux = matrizCostosOpti.transpose()

	for renglon in matrizTransAux:
		if(not fvm.hayNumeroEnRenglon(renglon,0)):
			menor = fvm.menorElementoRenglon(renglon)
			for index,elemento in enumerate(renglon):
				renglon[index] = elemento - menor

	matrizCostosOpti = matrizTransAux.transpose()

	### Paso 3
	matrizLineas, numLineas, menor = fvm.numeroTachesMatriz(matrizCostosOpti)

	while(numLineas < matrizCostosOpti.shape[0]):
		for i,renglon in enumerate(matrizLineas):
			for j,elemento in enumerate(renglon):
				if(elemento == 2):
					matrizCostosOpti[i][j]=matrizCostosOpti[i][j]+menor
				elif(elemento == 0):
					matrizCostosOpti[i][j]=matrizCostosOpti[i][j]-menor
		print(matrizCostosOpti)
		matrizLineas, numLineas, menor = fvm.numeroTachesMatriz(matrizCostosOpti)
