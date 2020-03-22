### Algoritmo de Optimizacion para problemas de transporte ###
import numpy as np


def solucionProblemaTransporte(probTransporte, matVariablesBasicas):
	u = []
	v = []
	varEntrada = (0,-1,-1)

	for i in range(probTransporte.n):
		u.append('*')
	for j in range(probTransporte.m):
		v.append('*')

	### Calculo de multiplicadores
	u[0] = 0
	while( '*' in u or '*' in v):
		uAux = u.copy()
		vAux = v.copy()

		for i in range(0,probTransporte.n,1):
			for j in range(0,probTransporte.m,1):
				if(matVariablesBasicas[i][j] and u[i] != '*' and v[j] == '*'):
					v[j] = probTransporte.matrizCostos[i][j] - u[i]

		for j in range(probTransporte.m):
			for i in range(probTransporte.n):
				if(matVariablesBasicas[i][j] and v[j] != '*' and u[i] == '*' ):
					u[i] = probTransporte.matrizCostos[i][j] - v[j]

		if(uAux == u and vAux == v):
			for i,elemento in enumerate(u):
				if(elemento == '*'):
					u[i] = 0
					break

	### Calculo de variables no básicas	
	for i,renglon in enumerate(probTransporte.matrizVariablesDecision):
		for j,elemento in enumerate(renglon):
			if(not matVariablesBasicas[i][j]):
				probTransporte.matrizVariablesDecision[i][j] = u[i]+v[j]-probTransporte.matrizCostos[i][j]


	### Identificando variable de entrada
	for i,renglon in enumerate(probTransporte.matrizVariablesDecision):
		for j,elemento in enumerate(renglon):
			if(elemento > varEntrada[0] and (not matVariablesBasicas[i][j])):
				varEntrada = (elemento, i, j)

	matVariablesBasicas[varEntrada[1]][varEntrada[2]] = True
	cicloMinimo(matVariablesBasicas,(varEntrada[1],varEntrada[2]))

	###if(varEntrada[0] > 0):
