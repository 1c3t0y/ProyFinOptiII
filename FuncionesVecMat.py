### Funciones de vectores y Matrices ###
import numpy as np

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

def contarValorEnVector(vector,valor):
	total=0
	for elemento in vector:
		if(elemento == valor):
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

	while(hayNumeroEnMatriz(matrizCostosAux,0)):
		mayorCantidadCeros = (0,0,0) ### (# de 0s, indice, renglón(0) o columna(1))
		cantidadCeros = 0

		for index,renglon in enumerate(matrizCostosAux):
			cantidadCeros = contarValorEnVector(renglon,0)
			if(mayorCantidadCeros[0] < cantidadCeros):
				mayorCantidadCeros = (cantidadCeros,index,0)

		for index,columna in enumerate(matrizCostosAux.transpose()):
			cantidadCeros = contarValorEnVector(columna,0)
			if(mayorCantidadCeros[0] < cantidadCeros):
				mayorCantidadCeros = (cantidadCeros,index,1)

		if(mayorCantidadCeros[2] == 0):
			matrizCostosAux[mayorCantidadCeros[1]] = np.tile(1000,matrizCos.shape[0])
		else:
			matrizCostosAux[:,mayorCantidadCeros[1]] = np.tile(1000,matrizCos.shape[1])

		matrizLineas = tacharMatriz(matrizLineas, mayorCantidadCeros[1], mayorCantidadCeros[2])
		numLineas += 1

		menor = menorElementoMatriz(matrizCostosAux)

	return matrizLineas, numLineas, menor