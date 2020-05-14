from typing import List, Tuple
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


def get_z_ppl(num_var: int) -> np.ndarray:
    print('Para la función objetivo Z...')
    z = get_coeficientes_ppl(num_var)
    while True:
        opc = input('¿Desea maximizar o minimizar z? (max/min): ')
        if opc.lower() == 'max' or opc == 'min':
            break
        else:
            print('Ingrese una opción válida... max para maximizar y min para minimizar')
    signo = -1 if opc == 'max' else 1
    return np.multiply(np.array(z), signo)


def get_restricciones_ppl(n: int, num_vars: int) -> Tuple:
    restricciones = []
    lado_derecho = []
    for i in range(1, n + 1):
        print(f'Para la restricción {i}...')
        row = get_coeficientes_ppl(num_vars)
        operador = get_operador_restriccion()
        valor_lado_derecho = get_param('el lado derecho de la restricción', -np.inf)
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
    for i in range(0, length):
        var = get_param(f'x{i}', -np.inf)
        result.append(var)
    return result
