from typing import List, Tuple, Dict
import os
import sys
import numpy as np
import math
import json


def print_m(matriz: List[List]):
    for row in matriz:
        print(f'\t{row}')


def check_int(num: str) -> int or None:
    try:
        result = int(num)
    except ValueError:
        return None
    return result


def check_float(flt: str or float) -> float or None:
    if type(flt) == str and '/' in flt:
        helper = []
        nums = flt.split('/')
        if len(nums) is not 2:
            return None
        for val in nums:
            helper.append(check_int(val))
        if all(helper):
            number = int(helper[0]) / int(helper[1])
        else:
            return None
    else:
        try:
            number = float(flt)
        except ValueError:
            return None
    return number


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
    while True:
        print('Para la función objetivo Z...')
        z = get_coeficientes_ppl(num_var)
        while True:
            opc = input('¿Desea maximizar o minimizar z? (max/min): ')
            if opc.lower() == 'max' or opc == 'min':
                break
            else:
                print('Ingrese una opción válida... max para maximizar y min para minimizar')
        signo = -1 if opc == 'max' else 1
        binario = confirmacion('¿Se trata de un problema binario?')
        objetivo = ' + '.join([f"{f'{x}*' if x is not 1 else ''}x{idx + 1}" for idx, x in enumerate(z) if x is not 0])
        print(f'La función objetivo queda: \n\t{opc} Z = {objetivo}')
        if confirmacion():
            break
    return np.multiply(np.array(z), signo), opc, binario


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


def clear_screen():
    if sys.platform[:3] == 'win':
        os.system('cls')
    if sys.platform[:5] == 'linux' or sys.platform[:6] == 'darwin':
        os.system('clear')


def read_from_JSON(ruta: str) -> Dict or None:
    try:
        file = open(ruta, 'r')
        contenidos = json.load(file)
        file.close()
        return contenidos
    except FileNotFoundError:
        print('No se pudo encontrar el archivo')
        return None
    except json.JSONDecodeError:
        print('No se pudo interpretar el archivo, asegúrese de que tenga terminación .json o .txt y '
              'que tenga la estructura correcta...')
        return None


def check_ppl_JSON(ppl: Dict) -> bool:
    keys = ['z', 'tipo_ppl', 'restricciones', 'lado_derecho', 'binario']
    if not check_keys_of(ppl, keys):
        print('\t***Error: Hace falta algún elemento.***')
        return False
    dim = len(ppl['z'])

    if not (ppl['tipo_ppl'] == 'max' or ppl['tipo_ppl'] == 'min'):
        print('\t***Error: El tipo no es ni "max" ni "min".***')
        return False
    if type(ppl['binario']) is not bool:
        print('\t***Error: binario debe ser de tipo bool, es decir, True o False.***')
        return False
    if [val for val in ppl['z'] if check_float(val) is None]:
        print('\t***Error: Se encontró algún elemento en Z que no es un número.***')
        return False
    if len(ppl['restricciones']) is not len(ppl['lado_derecho']):
        print('\t***Error: Hace falta algún elemento.***')
        return False

    for restriccion in ppl['restricciones']:
        if len(restriccion) is not dim or [val for val in restriccion if check_float(val) is None]:
            print('\t***Error: Estructura de las restricciones. La dimensión debe ser la misma que la de z. '
                  'Todos los elementos deben ser números***')
            return False
    for ld in ppl['lado_derecho']:
        if not (check_keys_of(ld, ['operador', 'valor']) and
                (ld['operador'] == '>' or ld['operador'] == '<' or ld['operador'] == '=') and
                check_float(ld['valor'] is not None)):
            print('\t***Error: Estructura de "lado_derecho". Debe contener dos elementos, "operador" y "valor".'
                  'El operador debe ser "<", ">" o "=". El valor debe ser un número***')
            return False
    return True


def check_keys_of(obj: Dict, keys: List) -> bool:
    for key in keys:
        try:
            obj[key]
        except KeyError:
            return False
    return True


def check_csv(matriz: np.ndarray, only_numbers: bool) -> bool:
    if [val for val in matriz if type(val) is float]:
        print('\t***Error: Ocurrió un error en la lectura de los datos***')
        print('\tRegresando al menú anterior...')
        input('\tPresione enter para continuar')
        return False
    if only_numbers:
        for row in matriz:
            if [val for val in row if check_float(val) is None]:
                print('\t***Error: Estructura de las restricciones. '
                      'Todos los elementos deben ser números***')
                print('\tRegresando al menú anterior...')
                input('\tPresione enter para continuar')
                return False
    return True
