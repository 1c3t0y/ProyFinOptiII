import numpy as np

class ProblemaOptimizacion(object):
	def __init__(self, n, m, costos, recursos, restricciones):
		self._n = n
		self._m = m
		self._costos = costos.copy() ###numpy array
		self._recursos = recursos.copy() ###numpy array
		self._restricciones = restricciones.copy() ###numpy matrix
		self._variablesDecision = np.zeros(self._n*self._m) ###numpy array


	### Properties ###
	@property
	def n(self):
		return self._n

	@property
	def m(self):
		return self._m

	@property
	def costos(self):
		return self._costos

	@property
	def recursos(self):
		return self._recursos

	@property
	def restricciones(self):
		return self._restricciones

	@property
	def variablesDecision(self):
		return self._variablesDecision

	
	### seters ###
	@n.setter
	def n(self, valor):
		self._n = valor

	@m.setter
	def m(self, valor):
		self._m = valor

	@costos.setter
	def costos(self, vector):
		if(len(vector) == self.n*self.m):
			self._costos = vector
		else:
			raise ValueError("Error en la asignacion del vector costos, dimensiones incorrectas")
		
	@recursos.setter
	def recursos(self, vector):
		if(len(vector) == self.n+self.m):
			self._recursos = vector
		else:
			raise ValueError("Error en la asignacion del vector recursos, dimensiones incorrectas")

	@restricciones.setter
	def restricciones(self, matriz):
		self._restricciones = matriz

	@variablesDecision.setter
	def variablesDecision(self, matriz):
		self._variablesDecision = matriz


	### Metodos ###



class ProblemaTransporte(ProblemaOptimizacion):
	"""docstring for matrizTransporte"matrizOptimizacion"""
	
	def __init__(self, origenes, destinos, costos, recursos):
		matrizRestricciones = genMatRestriccionesTransporte(origenes,destinos)
		super(ProblemaTransporte, self).__init__(origenes, destinos, costos, recursos, matrizRestricciones)
		self._oferta = recursos
		self._demanda = recursos
		self._matrizCostos = costos
		self._matrizVariablesDecision = self.variablesDecision


	### Properties ###
	@property
	def oferta(self):
		return self._oferta

	@property
	def demanda(self):
		return self._demanda

	@property
	def matrizCostos(self):
		return self._matrizCostos

	@property
	def matrizVariablesDecision(self):
		return self._matrizVariablesDecision
	

	### Setters ###
	@oferta.setter
	def oferta(self, vector):
		if(len(vector) == self.n):
			self._oferta = vector.copy()
		elif(len(vector) == self.n+self.m):
			self._oferta = self.recursos[:self.n]
		else:
			raise ValueError("Error en la asignacion del vector oferta, dimensiones incorrectas")

	@demanda.setter
	def demanda(self, vector):
		if(len(vector) == self._m):
			self._demanda = vector.copy()
		elif(len(vector) == self.n+self.m):
			self._demanda = vector[self.n:]
		else:
			raise ValueError("Error en la asignacion del vector demanda, dimensiones incorrectas")

	@matrizCostos.setter
	def matrizCostos (self, vector):
		if(len(vector) == self.n*self.m):
			self._matrizCostos = vector.reshape((self.n,self.m))
		elif((self.n,self.m) == vector.shape):
			self._matrizCostos = vector
		else:
			raise ValueError("Error en la asignacion del vector demanda, dimensiones incorrectas")

	@matrizVariablesDecision.setter
	def matrizVariablesDecision (self, vector):
		if(len(vector) == self.n*self.m):
			self._matrizVariablesDecision = vector.reshape((self.n,self.m))
		else:
			raise ValueError("Error en la asignacion del vector demanda, dimensiones incorrectas")


	### Metodos ###





class ProblemaAsignacion(ProblemaTransporte):
	"""docstring for ProblemaAsignacion"ProblemaTransporte"""
	def __init__(self, costos):
		tempRecursos = np.ones(costos.shape[0]+costos.shape[1])
		super(ProblemaAsignacion,self).__init__(costos.shape[0], costos.shape[1], costos, tempRecursos)


	### properties ###


	### Setters ### 


	### Métodos ###
	


def genMatRestriccionesTransporte(n, m):
	matrizRestricciones = np.zeros((n+m,n*m))

	for i in range(n) :
		for j in range(m):
			matrizRestricciones[i,(i*m)+j] = 1
	
	for j in range(m):
		for i in range(n):
			matrizRestricciones[j+n,(i*m)+(j)] = 1

	return matrizRestricciones
