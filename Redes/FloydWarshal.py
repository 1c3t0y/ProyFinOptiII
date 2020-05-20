from typing import List
from utils.Functions import print_m, check_int, get_param, confirmacion, clear_screen


class MetodoFloyd:
    def __init__(self, matriz: List[List]):
        self.matriz_pesos = matriz
        self.dim = len(matriz)
        self.matriz_rutas = self.crear_matriz_rutas_inicial()

    def crear_matriz_rutas_inicial(self) -> List[List[int]]:
        mat = []
        for i in range(self.dim):
            row = [num for num in range(1, self.dim + 1)]
            mat.append(row)
        return mat

    def resolver(self):
        for k in range(0, self.dim):
            for i in range(0, self.dim):
                for j in range(0, self.dim):
                    nueva_ruta = self.matriz_pesos[i][k] + self.matriz_pesos[k][j]
                    if self.matriz_pesos[i][j] > nueva_ruta:
                        self.matriz_pesos[i][j] = nueva_ruta
                        self.matriz_rutas[i][j] = k + 1

    @classmethod
    def get_opc(cls) -> int:
        while True:
            print('\nOpciones:')
            print('\t1) Ver matriz de costos')
            print('\t2) Ver matriz de rutas')
            print('\t3) Calcular ruta de i a j')
            print('\t4) Salir del método')
            opc = check_int(input('¿Qué desea hacer a continuación?: '))
            if opc is not None and opc < 5:
                break
            else:
                print('Por favor ingrese un número entero válido...')
        return opc

    def switcher(self, opc):
        if opc is 1:
            print('La matriz de adyacencia con los pesos calculados es:')
            print_m(self.matriz_pesos)
        elif opc is 2:
            print('La matriz de de las rutas es:')
            print_m(self.matriz_rutas)
        elif opc is 3:
            while True:
                i = get_param('i', 1, self.dim) - 1
                j = get_param('j', 1, self.dim) - 1
                print(f'La ruta más corta entre {i + 1} y {j + 1} pesa {self.matriz_pesos[i][j]} y es: ')
                print(self.calcular_ruta(i, j))
                if not confirmacion('¿Desea calcular otra ruta?'):
                    break

    def calcular_ruta(self, i: int, j: int) -> List:
        ruta = [i + 1]
        self.from_to(i, j, ruta)
        return ruta

    def from_to(self, i: int, j: int, ruta: List) -> None:
        if self.matriz_rutas[i][j] == j + 1:
            ruta.append(j + 1)
        else:
            self.from_to(i, self.matriz_rutas[i][j] - 1, ruta)
            self.from_to(self.matriz_rutas[i][j] - 1, j, ruta)

    def menu(self):
        self.resolver()
        while True:
            clear_screen()
            opc = self.get_opc()
            if opc == 4:
                print('Saliendo del método...')
                break
            self.switcher(opc)
