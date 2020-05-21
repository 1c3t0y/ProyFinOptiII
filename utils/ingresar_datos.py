### ingresar_datos ###
from typing import Tuple
import numpy as np
import math
from utils.Functions import check_int, check_csv, get_param, get_z_ppl, get_restricciones_ppl, \
	read_from_JSON, check_ppl_JSON


def ingresar_matriz_manualmente():
	opcion = "N"

	while opcion[0] == 'N' or opcion[0] == 'n':
		n = int(input('Ingrese la cantidad de renglones de la matriz: '))
		m = int(input('Ingrese la cantidad de columnas de la matriz: '))
		opcion = input('¿Está seguro de las dimensiones de la matriz?(S/n): ')

	matriz_costos = np.zeros((n, m))

	opcion = "S"
	while opcion[0] == 'S' or opcion[0] == 's':
		print("Ingrese los valores de la matriz:")
		for i in range(0, n, 1):
			for j in range(0, m, 1):
				matriz_costos[i][j] = input('Costos[{0}][{1}] = '.format(i,j))

		print("\n La matriz ingresada es: ")
		print(matriz_costos)

		opcion = input('¿Desea modificar la matriz?(S/n): ')

	return matriz_costos


def ingresar_matriz_csv():
	ruta_archivo = input('ingrese la ruta del archivo con extension .csv: ')
	delimitador = input('Ingrese el delimitador: ')

	try:
		result = np.genfromtxt(ruta_archivo, delimiter=delimitador)
		if not check_csv(result):
			return None
		print('--> ¡Lectura del archivo exitosa!')
		input('\tPresione enter para continuar')
		return result
	except IOError or OSError:
		print('\t***Error: No se encontró el archivo...')
		print('\tRegresando al menú anterior...')
		input('\tPresione enter para continuar')
		return None
	except ValueError:
		print('\t***Error: Todas las filas del archivo deben de tener la misma dimensión...')
		print('\tRegresando al menú anterior...')
		input('\tPresione enter para continuar')
		return None



def ingresar_oferta_demanda(dimensiones):
	opcion = 'S'
	oferta = np.zeros(dimensiones[0])
	demanda = np.zeros(dimensiones[1])

	while opcion == 's' or opcion == 'S':
		print("Ingrese los valores de la oferta:")
		for i in range(0, dimensiones[0], 1):
			oferta[i] = input('oferta[{0}] = '.format(i))

		print("Ingrese los valores de la demanda:")
		for j in range(0, dimensiones[1], 1):
			demanda[j] = input('oferta[{0}] = '.format(j))
		
		print("\n Los valores ingresados son: ")
		print("Oferta:")
		print(oferta)
		print("Demanda:")
		print(demanda)

		opcion = input('¿Desea modificar la oferta o la demanda?(S/n): ')

	return oferta, demanda


def ingresar_ppl_manualmente() -> Tuple:
	while True:
		num_var = check_int(input('Ingrese el número de variables: '))
		if num_var is not None and num_var > 0:
			break
		else:
			print('Ingrese un número entero mayor a 0...')
	z, tipo_ppl, binario = get_z_ppl(num_var)
	print('Sea n el número de restricciones...')
	n = get_param('n', 1)
	restricciones, lado_derecho = get_restricciones_ppl(n, num_var)
	return z, tipo_ppl, restricciones, lado_derecho, binario


def ingresar_ppl_json() -> Tuple or None:
	while True:
		print('\t -> Si desea regresar al menú anterior, ingrese "q" <-')
		ruta = input('Ingrese la ruta del archivo tipo json: ')
		if ruta.lower() == 'q':
			return None
		ppl_from_json = read_from_JSON(ruta)
		if ppl_from_json is None:
			continue
		if not check_ppl_JSON(ppl_from_json):
			continue
		break

	tipo_ppl = ppl_from_json['tipo_ppl']
	signo = -1 if tipo_ppl == 'max' else 1
	z = np.multiply(np.array(ppl_from_json['z']), signo)
	restricciones = ppl_from_json['restricciones']
	lado_derecho = ppl_from_json['lado_derecho']
	binario = ppl_from_json['binario']
	return z, tipo_ppl, restricciones, lado_derecho, binario


def ingresar_red_manualmente():
	opcion = 'S'
	while opcion == 'S' or opcion == 's':
		num_nodos = int(input('Ingrese la cantidad de nodos del problema: '))
		opcion = input('¿Desea cambiar la cantidad de nodos? (S/n): ')

	opcion = 'S'
	while opcion == 'S' or opcion == 's':
		matriz_adyacencia = np.tile(False, (num_nodos, num_nodos))
		for i, nodo in enumerate(matriz_adyacencia):
			adyacencia = input("Ingrese los nodos a los que el nodo {0} manda flujo (separados por comas): ".format(i+1))
			if adyacencia == "":
				continue
			for j in list(map(int,adyacencia.split(','))):
				matriz_adyacencia[i][j-1] = True
		print("La matriz de adyacencia ingresada es:")
		print(matriz_adyacencia)
		opcion = input('¿Desea cambiar la matriz de adyacencia? (S/n): ')

	opcion = 'S'
	while opcion == 'S' or opcion == 's':
		matriz_costos = np.tile(99999, (num_nodos, num_nodos))
		for i, nodo in enumerate(matriz_adyacencia):
			for j, arista in enumerate(nodo):
				if arista:
					matriz_costos[i][j] = input("Ingrese el costo de flujo del nodo {0} al nodo {1}: ".format(i+1,j+1))
		print("La matriz de costos ingresada es:")
		print(matriz_costos)
		opcion = input('¿Desea cambiar la matriz de costos? (S/n): ')

	opcion = 'S'
	while opcion == 'S' or opcion == 's':
		capacidades = np.zeros(num_nodos)
		for i in range(0,num_nodos,1):
			capacidades[i] = input('Ingrese la capacidad del nodo {0}: '.format(i+1,j+1))
		print("Las capacidades ingresados son:")
		print(capacidades)
		opcion = input('¿Desea cambiar las capacidades de los nodos? (S/n): ')

	return matriz_adyacencia, matriz_costos, capacidades


def ingresar_red_csv():
	opcion = 'S'
	while opcion == 'S' or opcion == 's':
		print("Ingresando la matriz de adyacencia: ")
		matriz_adyacencia = np.array(ingresar_matriz_csv(),dtype=bool)
		print("La matriz de adyacencia ingresada es:")
		print(matriz_adyacencia)
		opcion = input('¿Desea cambiar la matriz de adyacencia? (S/n): ')

	opcion = 'S'
	while opcion == 'S' or opcion == 's':
		print("Ingresando la matriz de costos: ")
		matriz_costos = ingresar_matriz_csv()
		print("La matriz de costos ingresada es:")
		print(matriz_costos)
		opcion = input('¿Desea cambiar la matriz de costos? (S/n): ')

	opcion = 'S'
	while opcion == 'S' or opcion == 's':
		print("Ingresando el vector de capacidades: ")
		capacidades = ingresar_matriz_csv()
		print("Las capacidades son capacidades:")
		print(capacidades)
		opcion = input('¿Desea cambiar la matriz de costos? (S/n): ')

	return matriz_adyacencia, matriz_costos, capacidades
