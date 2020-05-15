import utils.ingresar_datos as datos
from Transporte.sol_problema_transporte import sol_problema_transporte
from utils.Functions import check_int
from utils.switcher_métodos import switcher_metodos_redes, switcher_metodos_entera


def menu_principal():
	print("Menu de opciones:")
	print("1) Resolver un problema de transporte")
	print("2) Resolver un problema de redes")
	print("3) Resolver un problema de programación entera")
	print("q) Salir")


def menu_ingresar_matriz_costos(msg: str = "TRANSPORTE", ppl: bool = False):
	matriz = None
	objeto = 'un PPL' if ppl else 'una matriz'
	print(f'PROBLEMAS DE {msg}')
	print("Opciones para ingresar datos:")
	print(f"1) Ingresar {objeto} manualmente")
	print(f"2) Ingresar {objeto} desde un archivo csv")
	print("q) regresar al menú principal.")

	while True:
		opcion = input('¿Qué desea hacer?: ')
		if opcion == 'q' or (check_int(opcion) is not None and 0 < check_int(opcion) <= 2):
			break
		else:
			print('Ingrese una opción válida...')
	if opcion == '1':
		matriz = datos.ingresar_ppl_manualmente() if ppl else datos.ingresar_matriz_manualmente()
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


def menu_programacion_entera():
	ppl_ingresado = menu_ingresar_matriz_costos('PROGRAMACIÓN ENTERA', True)
	if ppl_ingresado is 0:
		return
	while True:
		print("METODOS PARA PROBLEMAS DE PROGRAMACIÓN ENTERA")
		print("¿Qué método desea utilizar?:")
		print("1) Resolver ppl por Branch and Bound")
		print("m) Utilizar otro ppl")
		print("q) Regresar al menu anterior")

		opc = input('¿Qué desea hacer?: ')
		if opc == 'q':
			break
		elif opc == 'm':
			ppl_ingresado = menu_ingresar_matriz_costos('PROGRAMACIÓN ENTERA', True)
			continue
		num = check_int(opc)
		if num is not None and num < 2:
			z, tipo_ppl, restricciones, lado_derecho = ppl_ingresado
			switcher_metodos_entera[opc](z, tipo_ppl, restricciones, lado_derecho).menu()
