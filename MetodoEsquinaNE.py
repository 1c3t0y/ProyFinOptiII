### Metodo Esquina Noroeste ###
import numpy as np
import ProblemasOptimizacion as po
import FuncionesVecMat as fvm
import SolucionesProblemasOptimizacion as spo

def metodoEsquinaNE(probTransporte):
	ofertaAux = probTransporte.oferta
	demandaAux = probTransporte.demanda
	matVariablesBasicas = np.tile(False,(probTransporte.n,probTransporte.m))
	tachesRen = np.tile(False, probTransporte.n)
	tachesCol = np.tile(False, probTransporte.m)
	numTachesRen = 0
	numTachesCol = 0
	i = 0
	j = 0


	while(not ((numTachesRen == 1 and numTachesCol == 0) or (numTachesRen == 0 and numTachesCol == 1))):
		### Paso 1
		menor = min(ofertaAux[i],demandaAux[j])
		probTransporte.matrizVariablesDecision[i][j] = menor
		matVariablesBasicas[i][j] = True
		ofertaAux[i] = ofertaAux[i] - menor
		demandaAux[j] = demandaAux[j] - menor
		
		### Paso 2
		if((ofertaAux[i] == 0 and demandaAux[j] == 0) or ofertaAux[i] == 0):
			tachesRen[i] = True
			i += 1
		else:
			tachesCol[j] = True
			j += 1

		### Paso 3
		numTachesRen = fvm.contarValorEnVector(tachesRen,False)
		numTachesCol = fvm.contarValorEnVector(tachesCol,False)

	print(probTransporte.matrizVariablesDecision)
	print(matVariablesBasicas)

	spo.solucionProblemaTransporte(probTransporte, matVariablesBasicas)


costos = np.array([[10,2,20,11],[12,7,9,20],[4,14,16,18]])
oferta = np.array([15,25,10])
demanda = np.array([5,15,15,15])
probTransporte = po.ProblemaTransporte(3,4,costos,oferta,demanda)
metodoEsquinaNE(probTransporte)