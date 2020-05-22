### balance red ###
import numpy as np

def balance_red(matriz_adyacencia, matriz_costos, capacidades, nombres):
	nombres = np.append(nombres, "Artificial").tolist()
	capacidad_artificial = -1*capacidades.sum()
	matriz_adyacencia = np.append(matriz_adyacencia, np.tile(False, (matriz_adyacencia.shape[0],1)), axis = 1)
	matriz_adyacencia = np.append(matriz_adyacencia, np.tile(False, (1, matriz_adyacencia.shape[1])), axis = 0)

	matriz_costos = np.append(matriz_costos, np.tile(99999, (matriz_costos.shape[0],1)), axis = 1)
	matriz_costos = np.append(matriz_costos, np.tile(99999, (1, matriz_costos.shape[1])), axis = 0)

	artificial = matriz_costos.shape[0]-1

	for i, capacidad in enumerate(capacidades):
		if capacidad_artificial < 0 and capacidad > 0:
			matriz_adyacencia[i][artificial] = True
			matriz_costos[i][artificial] = 0
		elif capacidad_artificial > 0 and capacidad < 0:
			matriz_adyacencia[artificial][i] = True
			matriz_costos[artificial][i] = 0

	capacidades = np.append(capacidades, capacidad_artificial)

	return matriz_adyacencia, matriz_costos, capacidades, nombres