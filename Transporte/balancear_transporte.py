### balancear problema de transporte ###
import numpy as np

def balancear_transporte(matriz_costos, oferta, demanda, nombres_origen, nombres_destino):
	if np.sum(oferta) > np.sum(demanda):
		costo_artificial = np.zeros((matriz_costos.shape[0],1))
		matriz_costos = np.append(matriz_costos, costo_artificial, axis = 1)
		demanda_artificial = np.sum(oferta)- np.sum(demanda)
		demanda = np.append(demanda,demanda_artificial)
		nombres_destino = np.append(nombres_destino,"Artificial", axis = None).tolist()
	else:
		costo_artificial = np.zeros((1, matriz_costos.shape[1]))
		matriz_costos = np.append(matriz_costos, costo_artificial, axis = 0)
		oferta_artificial = np.sum(demanda) - np.sum(oferta)
		oferta = np.append(oferta,oferta_artificial)
		nomres_origen = np.append(nombres_origen,"Artificial", axis = None).tolist()

	return matriz_costos, oferta, demanda, nombres_origen, nombres_destino