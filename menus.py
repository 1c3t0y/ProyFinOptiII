import utils.ingresar_datos as datos
from Transporte.sol_problema_transporte import sol_problema_transporte
from utils.Functions import check_int
from utils.switcher_métodos import switcher_metodos_redes


def menu_principal():
	print("Menu de opciones:")
	print("1) Resolver un problema de transporte")
	print("2) Resolver un problema de redes")
	print("q) Salir")


def menu_ingresar_matriz_costos(msg: str = "TRANSPORTE"):
	matriz = None
	print(f'PROBLEMAS DE {msg}')
	print("Opciones para ingresar datos:")
	print("1) Ingresar una matriz manualmente")
	print("2) Ingresar una matriz desde un archivo csv")
	print("q) regresar al menú principal.")

	while True:
		opcion = input('¿Qué desea hacer?: ')
		if opcion == 'q' or (check_int(opcion) is not None and 0 < check_int(opcion) <= 2):
			break
		else:
			print('Ingrese una opción válida...')
	if opcion == '1':
		matriz = datos.ingresar_matriz_manualmente()
	elif opcion == '2':
		matriz = datos.ingresar_matriz_csv()
	elif opcion == 'q':
		matriz = 0

	return matriz


def menu_metodos_transporte():
	matriz = menu_ingresar_matriz_costos('TRANSPORTE')
	if matriz is 0:
		return
	while True:
		print("METODOS PARA PROBLEMAS DE TRANSPORTE")
		print("1) Esquina Noroeste")
		print("2) Costo minimo")
		print("3) Aproximacion de Voguel")
		print("4) Método húngaro (Asignacion)")
		print("m) Ingresar otra matriz")
		print("q) Regresar al menu anterior")

		opc = input('¿Qué desea hacer?: ')
		if opc == 'q':
			break
		elif opc == 'm':
			matriz = menu_ingresar_matriz_costos('REDES')
			continue

		sol_problema_transporte(matriz, opc)


def menu_redes():
	matriz = menu_ingresar_matriz_costos('REDES')
	if matriz is 0:
		return
	while True:
		print("METODOS PARA PROBLEMAS DE REDES")
		print("¿Qué método desea utilizar?:")
		print("1) Floyd-Warshal")
		print("m) Utilizar otra matriz")
		print("q) Regresar al menu anterior")

		opc = input('¿Qué desea hacer?: ')
		if opc == 'q':
			break
		elif opc == 'm':
			matriz = menu_ingresar_matriz_costos('REDES')
			continue
		num = check_int(opc)
		if num is not None and num < 2:
			switcher_metodos_redes[opc](matriz).menu()