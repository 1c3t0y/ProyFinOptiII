from typing import List, Tuple
import numpy as np
import math


def print_m(matriz: List[List]):
    for row in matriz:
        print(f'\t{row}')


def check_int(num: str) -> int or None:
    try:
        result = int(num)
    except ValueError:
        return None
    return result


def get_param(param: str, lower_bound: int = 0, upper_bound: int = np.inf) -> int:
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


def get_z_ppl(num_var: int) -> Tuple:
    print('Para la función objetivo Z...')
    z = get_coeficientes_ppl(num_var)
    while True:
        opc = input('¿Desea maximizar o minimizar z? (max/min): ')
        if opc.lower() == 'max' or opc == 'min':
            break
        else:
            print('Ingrese una opción válida... max para maximizar y min para minimizar')
    signo = -1 if opc == 'max' else 1
    return np.multiply(np.array(z), signo), opc


def get_restricciones_ppl(n: int, num_vars: int) -> Tuple:
    restricciones = []
    lado_derecho = []
    for i in range(1, n + 1):
        while True:
            print(f'Para la restricción {i}...')
            row = get_coeficientes_ppl(num_vars)
            operador = get_operador_restriccion()
            valor_lado_derecho = get_param('el lado derecho de la restricción', -np.inf)
            x = ' + '.join([f"{f'{x}*' if x is not 1 else ''}x{idx + 1}" for idx, x in enumerate(row) if x is not 0])
            print(f'La restricción {i} es: \n\t{x} {operador} {valor_lado_derecho}')
            if confirmacion():
                break
        restricciones.append(row)
        lado_derecho.append({'operador': operador, 'valor': valor_lado_derecho})

    return restricciones, lado_derecho


def get_operador_restriccion() -> str:
    while True:
        print('¿De qué tipo de restricción se trata?')
        print('\tMayor o igual que: >')
        print('\tMenor o igual que: <')
        print('\tIgual que: =')
        operador = input('Ingrese el operador correspondiente: ')
        if operador == '>' or operador == '<' or operador == '=':
            return operador
        else:
            print('Ingrese una opción válida...')


def get_coeficientes_ppl(length: int) -> List:
    result = []
    for i in range(1, length + 1):
        var = get_param(f'x{i}', -np.inf)
        result.append(var)
    return result


def compare_floor(num: float) -> bool:
    num = round_num(num)
    if num == math.floor(num):
        return True
    else:
        return False


def round_num(num: float):
    num_ceil = np.ceil(num)
    num_floor = np.floor(num)
    if num_ceil - num < .00001:
        return num_ceil
    elif num - num_floor < .00001:
        return num_floor
    else:
        return num
