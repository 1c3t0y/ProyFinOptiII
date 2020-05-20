from typing import List
import numpy as np
from queue import PriorityQueue
from utils.Functions import check_int, get_param, confirmacion, clear_screen


class MetodoDijkstra:
    def __init__(self, matriz: List[List]):
        self.matriz_pesos = matriz
        self.dim = len(matriz)
        self.visitados = [False] * self.dim
        self.distancias = None
        self.anterior = [None] * self.dim
        self.nodos_pendientes = PriorityQueue()
        self.M = 1000
        self.nodo_inicial = None

    # Algorithm Methods
    def reiniciar_algoritmo(self):
        self.anterior = [None] * self.dim
        self.visitados = [False] * self.dim
        self.nodos_pendientes = PriorityQueue()
        self.nodo_inicial = get_param('el nuevo nodo inicial', 1, self.dim) - 1
        self.iniciar_algoritmo()

    def iniciar_algoritmo(self):
        self.distancias = [np.inf if i is not self.nodo_inicial else 0 for i in range(0, self.dim)]
        self.visitar_nodos_desde(self.nodo_inicial)
        while not self.nodos_pendientes.empty():
            distancia, siguiente_nodo = self.nodos_pendientes.get()
            if distancia <= self.distancias[siguiente_nodo]:
                self.visitar_nodos_desde(siguiente_nodo)

    def visitar_nodos_desde(self, nodo: int):
        adyacentes = [i for i, ady in enumerate(self.matriz_pesos[nodo]) if 0 < ady < self.M and i is not nodo]
        for adyacente in adyacentes:
            self.visitar_desde(nodo, adyacente)

    def visitar_desde(self, start: int, destination: int):
        distancia = self.distancias[start] + self.matriz_pesos[start][destination]
        if not self.visitados[destination]:
            self.visitados[destination] = True
        if distancia < self.distancias[destination]:
            self.anterior[destination] = start
            self.distancias[destination] = distancia
            self.nodos_pendientes.put((distancia, destination))

    # Menu Methods
    def get_opc(self) -> int:
        while True:
            print('\nOpciones:')
            print(f'\t1) Ver costos desde nodo {self.nodo_inicial + 1}')
            print(f'\t2) Calcular ruta de nodo {self.nodo_inicial + 1} a j')
            print('\t3) Encontrar mejor ruta para otro nodo')
            print('\t4) Salir del método')
            opc = check_int(input('¿Qué desea hacer a continuación?: '))
            if opc is not None and opc < 5:
                break
            else:
                print('Por favor ingrese un número entero válido...')
        return opc

    def switcher(self, opc):
        if opc is 1:
            self.print_distancias()
        elif opc is 2:
            self.print_ruta()
        elif opc is 3:
            self.reiniciar_algoritmo()

    def print_distancias(self):
        print('Las distancias desde el nodo incial a los demás son:')
        for i, distancia in enumerate(self.distancias):
            if i is not self.nodo_inicial:
                print(f'Distancia del nodo {self.nodo_inicial + 1} al nodo {i + 1}: {distancia}')

    def print_ruta(self):
        while True:
            j = get_param('j', 1, self.dim) - 1
            print(f'La ruta más corta entre {self.nodo_inicial + 1} y {j + 1} pesa {self.distancias[j]} y es: ')
            print(self.get_ruta(j))
            if not confirmacion('¿Desea calcular otra ruta?'):
                break

    def get_ruta(self, destination: int) -> List or str:
        ruta = []
        anterior = self.anterior[destination]
        if anterior == self.nodo_inicial or self.from_to(anterior, ruta):
            ruta.append(destination + 1)
            return ruta
        else:
            return f'No se encontró una ruta desde {self.nodo_inicial + 1} hacia {destination + 1}'

    def from_to(self, destination: int or None, ruta: List) -> bool:
        if destination is None:
            return False
        if destination == self.nodo_inicial:
            ruta.append(destination + 1)
            return True
        anterior = self.anterior[destination]
        if self.from_to(anterior, ruta):
            ruta.append(destination + 1)
            return True
        return False

    def menu(self):
        self.nodo_inicial = get_param('el nodo inicial', 1, self.dim) - 1
        self.iniciar_algoritmo()
        while True:
            clear_screen()
            opc = self.get_opc()
            if opc == 4:
                print('Saliendo del método...')
                break
            self.switcher(opc)
            input('\nPulse enter para continuar...')
