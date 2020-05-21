from typing import List, Dict, Tuple
from utils.Functions import check_int
import numpy as np


class ProblemaEntera:
    def __init__(self, z: List, tipo_ppl: str, lado_derecho: List[Dict], binario: bool = False):
        self.z = z
        self.tipo_ppl = tipo_ppl
        self.lado_derecho = lado_derecho
        self.binario = binario
        self.restricciones = None

    def factible_para(self, restriccion: Dict or List, lado_derecho: Dict, vars_forzadas: List = None, z: List = None) -> bool:
        if z is None:
            convenientes = [val for val in restriccion['conveniente']]
            for var in vars_forzadas:
                convenientes[var['variable']] = var['valor']
        else:
            convenientes = z
        if type(restriccion) is list:
            coeficientes_restriccion = restriccion
        else:
            coeficientes_restriccion = restriccion['restriccion']
        rest_evaluada = np.dot(convenientes, coeficientes_restriccion)
        return self.checar_factibilidad(rest_evaluada, lado_derecho['operador'], lado_derecho['valor'])

    @classmethod
    def checar_factibilidad(cls, restriccion: float or np.ndarray, operador: str, lado_derecho: float) -> bool:
        if operador == '<':
            return restriccion <= lado_derecho
        elif operador == '>':
            return restriccion >= lado_derecho
        else:
            return restriccion == lado_derecho

    def get_infactibles(self, vars_forzadas: List = None, z: List = None):
        infactibles = []
        for i, restriccion in enumerate(self.restricciones):
            if not self.factible_para(restriccion, self.lado_derecho[i], vars_forzadas, z):
                infactibles.append(i)
        return infactibles
