from typing import List
import numpy as np


def print_m(matriz: List[List]):
    for row in matriz:
        print(f'\t{row}')


def check_int(num: str) -> int or None:
    try:
        result = int(num)
    except ValueError:
        return None
    return result


def get_param(param, lower_bound: int = 0, upper_bound: int = np.inf) -> int:
    while True:
        val = check_int(input(f'¿Cuál es el valor de {param}?: '))
        if val is not None and lower_bound <= val <= upper_bound:
            break
        else:
            print(f'Ingrese un número entero entre {lower_bound} y {upper_bound}...')
    return val


def confirmacion(msg: str = '¿Desea continuar?') -> bool:
    while True:
        respuesta = input(f'{msg} (Si/No): ')
        if respuesta.lower() == 'si' or respuesta == '':
            return True
        elif respuesta.lower() == 'no':
            return False
        else:
            print('Ingrese una opción aceptada...')
            continue
