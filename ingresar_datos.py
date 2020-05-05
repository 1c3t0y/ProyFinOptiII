### ingresar_datos ###
import numpy as np

def ingresar_matriz_manualmente():
	opcion = "N"

	while opcion[0] == 'N' or opcion[0] == 'n':
		n = int(input('Ingrese la cantidad de renglones de la matriz: '))
		m = int(input('Ingrese la cantidad de columnas de la matriz: '))
		opcion = input('¿Está seguro de las dimensiones de la matriz?(S/n): ')

	matriz_costos = np.zeros((n,m))

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

	return np.genfromtxt(ruta_archivo, delimiter=delimitador)


def ingresar_oferta_demanda(dimensiones):
	opcion = 'S'
	oferta = np.zeros(dimensiones[0])
	demanda = np.zeros(dimensiones[1])

	while opcion[0] == 's' or opcion[0] == 'S':
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



