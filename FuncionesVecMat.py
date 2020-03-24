### Funciones de vectores y Matrices ###
import numpy as np

### Funciones de renglones ###


### Funciones de matrices ###

def genMatRestriccionesTransporte(n, m):
	matrizRestricciones = np.zeros((n+m,n*m))

	for i in range(n) :
		for j in range(m):
			matrizRestricciones[i,(i*m)+j] = 1
	
	for j in range(m):
		for i in range(n):
			matrizRestricciones[j+n,(i*m)+(j)] = 1

	return matrizRestricciones
	

def tacharMatriz(matriz, indice, ren_o_col):
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

	while(np.any(matrizCostosAux == 0)):
		mayorCantidadCeros = (0,0,0) ### (# de 0s, indice, renglón(0) o columna(1))
		cantidadCeros = 0

		for index,renglon in enumerate(matrizCostosAux):
			cantidadCeros = (renglon == 0).sum()
			if(mayorCantidadCeros[0] < cantidadCeros):
				mayorCantidadCeros = (cantidadCeros,index,0)

		for index,columna in enumerate(matrizCostosAux.transpose()):
			cantidadCeros = (columna == 0).sum()
			if(mayorCantidadCeros[0] < cantidadCeros):
				mayorCantidadCeros = (cantidadCeros,index,1)

		if(mayorCantidadCeros[2] == 0):
			matrizCostosAux[mayorCantidadCeros[1]] = np.tile(1000,matrizCos.shape[0])
		else:
			matrizCostosAux[:,mayorCantidadCeros[1]] = np.tile(1000,matrizCos.shape[1])

		matrizLineas = tacharMatriz(matrizLineas, mayorCantidadCeros[1], mayorCantidadCeros[2])
		numLineas += 1

		menor = np.amin(matrizCostosAux)

	return matrizLineas, numLineas, menor