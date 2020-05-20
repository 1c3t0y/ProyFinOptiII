import numpy as np
import utils.fun_vec_mat as fvm


class ProblemaOptimizacion(object):
    def __init__(self, n, m, costos, recursos, restricciones):
        self.n = n
        self.m = m
        self.costos = costos.copy()  ###numpy array
        self.restricciones = restricciones.copy()  ###numpy matrix
        self.recursos = recursos.copy()  ###numpy array
        self.variables_decision = np.zeros(self._n * self._m)  ###numpy array
        self.variables_basicas = np.tile(False, self._n * self._m)
        self.z  ## funcion objetivo ##

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
    def variables_decision(self):
        return self._variables_decision

    @property
    def variables_basicas(self):
        return self._variables_basicas

    @property
    def z(self):
        self._z = 0
        for i in enumerate(self.variables_basicas):
            if self.variables_basicas[i]:
                self._z += self.costos[i] * self.variables_decision[i]
        return self._z

    ### seters ###
    @n.setter
    def n(self, valor):
        self._n = valor

    @m.setter
    def m(self, valor):
        self._m = valor

    @costos.setter
    def costos(self, vector):
        if len(vector) == self.n * self.m:
            self._costos = vector
        else:
            raise ValueError(
                "Error en la asignacion del vector costos, dimensiones incorrectas"
            )

    @recursos.setter
    def recursos(self, vector):
        if len(vector) == self.restricciones.shape[0]:
            self._recursos = vector
        else:
            raise ValueError(
                "Error en la asignacion del vector recursos, dimensiones incorrectas"
            )

    @restricciones.setter
    def restricciones(self, matriz):
        self._restricciones = matriz

    @variables_decision.setter
    def variables_decision(self, matriz):
        self._variables_decision = matriz

    @variables_basicas.setter
    def variables_basicas(self, matriz):
        self._variables_basicas = matriz

    ### Metodos ###


class ProblemaTransporte(ProblemaOptimizacion):
    """docstring for matrizTransporte"matrizOptimizacion"""

    def __init__(self, origenes, destinos, costos, oferta, demanda):
        matriz_restricciones = fvm.gen_mat_restricciones_transporte(origenes, destinos)
        super(ProblemaTransporte, self).__init__(
            origenes,
            destinos,
            costos.flatten(),
            np.concatenate((oferta, demanda), axis=None),
            matriz_restricciones,
        )
        self.oferta = oferta
        self.demanda = demanda
        self.matriz_costos = costos
        self.matriz_variables_decision = self.variables_decision
        self.matriz_variables_basicas = self.variables_basicas

    ### Properties ###
    @property
    def oferta(self):
        return self._oferta

    @property
    def demanda(self):
        return self._demanda

    @property
    def matriz_costos(self):
        return self._matriz_costos

    @property
    def matriz_variables_decision(self):
        return self._matriz_variables_decision

    @property
    def matriz_variables_basicas(self):
        return self._matriz_variables_basicas

    ### Setters ###
    @oferta.setter
    def oferta(self, vector):
        if len(vector) == self.n:
            self._oferta = vector.copy()
        elif len(vector) == self.n + self.m:
            self._oferta = self.recursos[: self.n]
        else:
            raise ValueError(
                "Error en la asignacion del vector oferta, dimensiones incorrectas"
            )

    @demanda.setter
    def demanda(self, vector):
        if len(vector) == self._m:
            self._demanda = vector.copy()
        elif len(vector) == self.n + self.m:
            self._demanda = vector[self.n :]
        else:
            raise ValueError(
                "Error en la asignacion del vector demanda, dimensiones incorrectas"
            )

    @matriz_costos.setter
    def matriz_costos(self, vector):
        if len(vector) == self.n * self.m:
            self._matriz_costos = vector.reshape((self.n, self.m))
        elif (self.n, self.m) == vector.shape:
            self._matriz_costos = vector
        else:
            raise ValueError(
                "Error en la asignacion de la matriz costos, dimensiones incorrectas"
            )

    @matriz_variables_decision.setter
    def matriz_variables_decision(self, vector):
        if len(vector) == self.n * self.m:
            self._matriz_variables_decision = vector.reshape((self.n, self.m))
        else:
            raise ValueError(
                "Error en la asignacion de la matriz variables_decision, dimensiones incorrectas"
            )

    @matriz_variables_basicas.setter
    def matriz_variables_basicas(self, vector):
        if len(vector) == self.n * self.m:
            self._matriz_variables_basicas = vector.reshape((self.n, self.m))
        else:
            raise ValueError(
                "Error en la asignacion de la matriz variables_basicas, dimensiones incorrectas"
            )

    ### Metodos ###


class ProblemaAsignacion(ProblemaTransporte):
    """docstring for ProblemaAsignacion"ProblemaTransporte"""

    def __init__(self, costos):
        oferta = np.ones(costos.shape[0])
        demanda = np.ones(costos.shape[1])
        super(ProblemaAsignacion, self).__init__(
            costos.shape[0], costos.shape[1], costos, oferta, demanda
        )
        self.matriz_asignacion = np.zeros(costos.shape)

    ### properties ###
    @property
    def matriz_asignacion(self):
        return self._matriz_asignacion

    ### Setters ###
    @matriz_asignacion.setter
    def matriz_asignacion(self, matriz):
        self._matriz_asignacion = matriz

    ### Métodos ###


class ProblemaRedes(ProblemaOptimizacion):
    def __init__(self, matriz_adyacencia, costos, capacidades):
        matriz_restricciones = fvm.gen_mat_restricciones_redes(matriz_adyacencia)
        super(ProblemaRedes, self).__init__(
            matriz_adyacencia.shape[0],
            matriz_adyacencia.shape[1],
            costos.flatten(),
            capacidades,
            matriz_restricciones,
        )

        self.matriz_adyacencia = matriz_adyacencia
        self.matriz_costos = costos
        self.matriz_variables_decision = self.variables_decision
        self.matriz_variables_basicas = self.variables_basicas
        self.raiz = -1


    ### Properties ###
    @property
    def matriz_adyacencia(self):
        return self._matriz_adyacencia

    @property
    def matriz_costos(self):
        return self._matriz_costos

    @property
    def matriz_variables_decision(self):
        return self._matriz_variables_decision

    @property
    def matriz_variables_basicas(self):
        return self._matriz_variables_basicas

    @property
    def raiz(self):
        return self._raiz

    ### Setters ###
    @matriz_adyacencia.setter
    def matriz_adyacencia(self, matriz):
        self._matriz_adyacencia = matriz

    @matriz_costos.setter
    def matriz_costos(self, vector):
        if len(vector) == self.n * self.m:
            self._matriz_costos = vector.reshape((self.n, self.m))
        elif (self.n, self.m) == vector.shape:
            self._matriz_costos = vector
        else:
            raise ValueError(
                "Error en la asignacion de la matriz costos, dimensiones incorrectas"
            )

    @matriz_variables_decision.setter
    def matriz_variables_decision(self, vector):
        if len(vector) == self.n * self.m:
            self._variables_decision = vector
            self._matriz_variables_decision = self.variables_decision.reshape((self.n, self.m))
        else:
            raise ValueError(
                "Error en la asignacion de la matriz variables_decision, dimensiones incorrectas"
            )

    @matriz_variables_basicas.setter
    def matriz_variables_basicas(self, vector):
        if len(vector) == self.n * self.m:
            self._variables_basicas = vector
            self._matriz_variables_basicas = self._variables_basicas.reshape((self.n, self.m))
        else:
            raise ValueError(
                "Error en la asignacion de la matriz variables_basicas, dimensiones incorrectas"
            )
    
    @raiz.setter
    def raiz(self, valor):
        self._raiz = valor

    ### Métodos ###