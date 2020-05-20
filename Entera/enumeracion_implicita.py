from typing import List, Dict
from utils.Functions import check_int, clear_screen
from classes.problema_entera import ProblemaEntera
import numpy as np


class EnumeracionImplicita(ProblemaEntera):
    def __init__(self, z: List, tipo_ppl: str, restricciones: List[List],
                 lado_derecho: List[Dict], binario: bool = False):
        super().__init__(z, tipo_ppl, lado_derecho, binario)
        self.conveniente_z = self.conveniente_para(z)
        self.restricciones = [
            {
                'restriccion': restriccion,
                'conveniente': self.conveniente_para(restriccion, i)
            }
            for i, restriccion in enumerate(restricciones)
        ]
        self.solucion = None
        self.lower_bound = None

    def conveniente_para(self, restriccion: List, i: int = None) -> List:
        if i is None:
            signo = 1
        else:
            signo = 1 if self.lado_derecho[i]['operador'] == '<' else -1
        result = []
        for var in restriccion:
            coef = 1 if signo * var < 0 else 0
            result.append(coef)
        return result

    def start_metodo(self) -> bool:
        valor_z = np.dot(self.conveniente_z, self.z)
        infactibles_z = self.get_infactibles(z=self.conveniente_z)
        if infactibles_z:
            return self.enumeracion_implicita()
        else:
            self.lower_bound = valor_z
            self.solucion = self.conveniente_z
            return True

    def enumeracion_implicita(self, vars_forzadas: List[Dict] = None) -> bool:
        if vars_forzadas is None:
            vars_forzadas = []
        num_var = self.get_mejor(vars_forzadas)
        vars_forzadas.append({'variable': num_var, 'valor': 1})
        infactibles = self.get_infactibles(vars_forzadas)
        if len(infactibles):
            return False
        else:
            sol = [0] * len(self.z)
            for variable in vars_forzadas:
                sol[variable['variable']] = variable['valor']
            valor_z = float(np.dot(sol, self.z))
            infactibles_z = self.get_infactibles(vars_forzadas, sol)
            if len(infactibles_z):
                vars_rama1 = [v for v in vars_forzadas]
                rama1 = self.enumeracion_implicita(vars_rama1)
                vars_rama2 = [v if not v['variable'] == num_var else
                              {'variable': num_var, 'valor': 0} for v in vars_forzadas]
                rama2 = self.enumeracion_implicita(vars_rama2)
                return rama1 or rama2
            elif self.lower_bound is None or valor_z < self.lower_bound:
                self.lower_bound = valor_z
                self.solucion = sol
                return True

    def get_mejor(self, vars_forzadas: List) -> int:
        mejor = {'en_z': None, 'en_restricciones': None}
        mejor_var = None
        no_disponibles = [var['variable'] for var in vars_forzadas]
        for i in range(0, len(self.z)):
            if i not in no_disponibles:
                evaluacion_var = self.valorar_variable(i)
                if ((mejor['en_z'] is None or mejor['en_restricciones'] < evaluacion_var['en_restricciones'])
                        or (mejor['en_restricciones'] == evaluacion_var['en_restricciones']
                            and mejor['en_z'] > evaluacion_var['en_z'])):
                    mejor = evaluacion_var
                    mejor_var = i
        return mejor_var

    def valorar_variable(self, variable: int):
        evaluacion = {'en_z': self.z[variable], 'en_restricciones': 0}
        for restriccion in self.restricciones:
            if restriccion['conveniente'][variable]:
                evaluacion['en_restricciones'] += 1
        return evaluacion

    def print_condiciones_iniciales(self):
        print('\nCondiciones iniciales: ')
        coeficientes = [f'x{i + 1} = {coef}' for i, coef in enumerate(self.conveniente_z)]
        print(f'\t-> A Z le conviene que: {", ".join(coeficientes)}\n')
        for r, restriccion in enumerate(self.restricciones):
            coeficientes = [f'x{i + 1} = {coef}' for i, coef in enumerate(restriccion['conveniente'])]
            print(f'\t-> A la restriccion {r} le conviene que: {", ".join(coeficientes)}')

    def print_solucion(self):
        if self.solucion is not None:
            print('\nLa solución encontrada es: ')
            for i, x in enumerate(self.solucion):
                print(f'\tx{i + 1} = {x}')
            print(f'\n\tZ = {self.lower_bound if self.tipo_ppl == "min" else -self.lower_bound}')
        else:
            print('\nNo se pudo encontrar solución al problema :c')

    @classmethod
    def get_opc(cls) -> int:
        while True:
            print('\nOpciones:')
            print('\t1) Ver condiciones iniciales')
            print('\t2) Ver solución final')
            print('\t3) Salir del método')
            opc = check_int(input('¿Qué desea hacer a continuación?: '))
            if opc is not None and opc < 4:
                break
            else:
                print('Por favor ingrese un número entero válido...')
        return opc

    def switcher(self, opc):
        if opc is 1:
            self.print_condiciones_iniciales()
        elif opc is 2:
            self.print_solucion()

    def menu(self):
        clear_screen()
        if not self.start_metodo():
            print('\nNo se pudo encontrar solución al problema')
        while True:
            opc = self.get_opc()
            if opc == 3:
                print('Saliendo del método...')
                break
            self.switcher(opc)
            input('\nPulse enter para continuar...')
            clear_screen()
