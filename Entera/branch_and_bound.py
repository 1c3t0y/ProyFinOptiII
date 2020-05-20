from classes.PPL import PPL
from typing import List, Dict, Tuple
from utils.Functions import check_int, compare_floor, round_num, clear_screen
from classes.problema_entera import ProblemaEntera
import numpy as np


class BranchAndBound(ProblemaEntera):
    def __init__(self, z: List, tipo_ppl: str, restricciones: List[List],
                 lado_derecho: List[Dict], binario: bool = False):
        super().__init__(z, tipo_ppl, lado_derecho, binario)
        self.restricciones = restricciones
        self.solucion = PPL(z, tipo_ppl, restricciones, lado_derecho, binario).solve()
        self.lower_bound = self.get_lower_bound()
        self.solucion_entera = None

    # Algorithm Methods
    @classmethod
    def redondear_solucion(cls, z: List, solucion) -> None:
        rounded_vars = []
        for x in solucion.x:
            x_rounded = round_num(x)
            rounded_vars.append(x_rounded)
        solucion.x = rounded_vars
        solucion.fun = np.dot(solucion.x, z)

    def get_lower_bound(self) -> Dict or None:
        if self.solucion.success:
            z = self.z if self.tipo_ppl == 'min' else -1 * self.z
            self.redondear_solucion(z, self.solucion)
            result = {'variables': [], 'val': None}
            for x in self.solucion.x:
                result['variables'].append(np.floor(x))
            if not self.get_infactibles(z=result['variables']):
                result['val'] = np.dot(result['variables'], z)
                return result
        return None

    def get_max_non_int(self, lista: List = None) -> Tuple:
        if lista is None:
            lista = self.solucion.x
        max_x = max([x for x in lista if not compare_floor(x)])
        if type(lista) == np.ndarray:
            index = [i for i, x in enumerate(lista) if x == max_x][0]
        else:
            index = lista.index(max_x)
        return max_x, index

    def better_than_lower(self, sol):
        if self.lower_bound is None:
            self.lower_bound = {'val': sol.fun, 'variables': sol.x}
            return True
        if self.tipo_ppl == 'max':
            return sol.fun < self.lower_bound['val']
        else:
            return sol.fun > self.lower_bound['val']

    def try_new_restriction(self, var: int, val_lado_derecho: int, operador: str, restricciones: List[List],
                            lado_derecho: List[Dict]) -> bool:
        nuevas_restricciones = [item for item in restricciones]
        nuevas_restricciones.append([0 if i is not var else 1 for i in range(0, len(self.z))])
        nuevo_lado_derecho = [item for item in lado_derecho]
        nuevo_lado_derecho.append({'operador': operador, 'valor': val_lado_derecho})
        sol = PPL(self.z, self.tipo_ppl, nuevas_restricciones, nuevo_lado_derecho, self.binario).solve()
        if not (sol.success or self.better_than_lower(sol)):
            return False
        if all([compare_floor(x) for x in sol.x]):
            if not self.solucion_entera or sol.fun > self.solucion_entera.fun:
                self.solucion_entera = sol
                z = self.z if self.tipo_ppl == 'min' else -1 * self.z
                self.redondear_solucion(z, self.solucion_entera)
            return True
        else:
            val, var = self.get_max_non_int(sol.x)
            up_branch = self.try_new_restriction(var, np.ceil(val), '>', nuevas_restricciones, nuevo_lado_derecho)
            down_branch = self.try_new_restriction(var, np.floor(val), '<', nuevas_restricciones, nuevo_lado_derecho)
        return up_branch or down_branch

    def start_branch_bound(self) -> bool:
        if all([compare_floor(x) for x in self.solucion.x]):
            self.solucion_entera = self.solucion
            return True
        val, var = self.get_max_non_int()
        up_branch = self.try_new_restriction(var, np.ceil(val), '>', self.restricciones, self.lado_derecho)
        down_branch = self.try_new_restriction(var, np.floor(val), '<', self.restricciones, self.lado_derecho)
        return up_branch or down_branch

    # Menu Methods
    @classmethod
    def get_opc(cls) -> int:
        while True:
            print('\nOpciones:')
            print('\t1) Ver solución relajada')
            print('\t2) Ver solución entera')
            print('\t3) Salir del método')
            opc = check_int(input('¿Qué desea hacer a continuación?: '))
            if opc is not None and opc <= 3:
                break
            else:
                print('Por favor ingrese un número entero válido...')
        return opc

    def print_solucion(self, solucion=None):
        if solucion is None:
            z = self.lower_bound['val']
            variables = self.lower_bound['variables']
        else:
            z = solucion.fun
            variables = solucion.x
        print(f'z = {z}')
        for i, x in enumerate(variables):
            print(f'El valor de x{i + 1} = {x}')

    def switcher(self, opc):
        if opc is 1:
            iguales = " la solución entera también" if self.solucion_entera == self.solucion else ""
            print(f'La solución relajada es{iguales}:')
            self.print_solucion(self.solucion)
        elif opc is 2:
            if self.solucion_entera is not None:
                print('Se encontró una solución entera al problema, ésta es: ')
                self.print_solucion(self.solucion_entera)
            else:
                print('No se pudo encontrar una solución entera al problema mejor a la cota inferior inicial...')
                self.print_solucion()

    def menu(self):
        if not self.solucion.success:
            print('No se pudo encontrar una solución factible al problema relajado...')
            input('Volviendo al menu anterior, presione enter para continuar...')
            return None
        self.start_branch_bound()
        while True:
            clear_screen()
            opc = self.get_opc()
            if opc == 3:
                print('Saliendo del método...')
                break
            self.switcher(opc)
            input('\nPulse enter para continuar...')
