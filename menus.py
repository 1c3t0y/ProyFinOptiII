import utils.ingresar_datos as datos
from Transporte.sol_problema_transporte import sol_problema_transporte
from utils.Functions import check_int, confirmacion, clear_screen
from utils.switcher_métodos import switcher_metodos_redes, switcher_metodos_entera

from classes.problemas_optimizacion import ProblemaRedes ### Borrar esta linea a futuro
from Redes.solucion_MCFP import solucion_mcfp ### Borrar esta linea a futuro
import numpy as np


def menu_principal():
	clear_screen()
	print("Menu de opciones:")
	print("1) Resolver un problema de transporte")
	print("2) Resolver un problema de redes")
	print("3) Resolver un problema de programación entera")
	print("q) Salir")


def menu_ingresar_matriz_costos(msg: str = "TRANSPORTE", ppl: bool = False):
	clear_screen()

	matriz = None
	objeto = 'un PPL' if ppl else 'una matriz'
	extension = 'JSON' if ppl else 'csv'
	print(f'PROBLEMAS DE {msg}')
	print("Opciones para ingresar datos:")
	print(f"1) Ingresar {objeto} manualmente")
	print(f"2) Ingresar {objeto} desde un archivo {extension}")
	print("q) Regresar al menú anterior.")

	while True:
		opcion = input('¿Qué desea hacer?: ')
		if opcion == 'q' or (check_int(opcion) is not None and 0 < check_int(opcion) <= 2):
			break
		else:
			print('Ingrese una opción válida...')
	if opcion == '1':
		matriz = datos.ingresar_ppl_manualmente() if ppl else datos.ingresar_matriz_manualmente()
	elif opcion == '2':
		matriz = datos.ingresar_ppl_json() if ppl else datos.ingresar_matriz_csv()
	elif opcion == 'q':
		matriz = 0

	return matriz

def menu_ingresar_mcfp():
	clear_screen()
	objeto = 'un problema redes'
	print(f'PROBLEMA DE FLUJO DE REDES A COSTO MÍNIMO')
	print("Opciones para ingresar datos:")
	print(f"1) Ingresar red manualmente")
	print(f"2) Ingresar red desde archivos csv")
	print("q) regresar al menú anterior.")

	while True:
		opcion = input('¿Qué desea hacer?: ')
		if opcion == 'q' or (check_int(opcion) is not None and 0 < check_int(opcion) <= 2):
			break
		else:
			print('Ingrese una opción válida...')
	if opcion == '1':
		matriz_adyacencia, matriz_costos, capacidades = datos.ingresar_mcfp_manualmente()
	elif opcion == '2':
		matriz_adyacencia, matriz_costos, capacidades = datos.ingresar_mcfp_csv()
	elif opcion == 'q':
		matriz = 0

	return matriz_adyacencia, matriz_costos, capacidades

def menu_sol_bas_fact_inicial_mcfp():
	clear_screen()
	adyacencia, costos, capacidades = menu_ingresar_mcfp()
	print(f'SOLUCIONAR MCFP')
	print("Opciones para SOLUCIÓN BÁSICA FACTIBLE INICIAL:")
	print(f"1) Método de la M grande")
	print(f"2) Dos fases")
	print(f"3) Dar una solución básica factible")
	print(f"o) Dar otro MCFP")
	print("q) regresar al menú anterior.")

	while True:
		opcion = input('¿Qué desea hacer?: ')
		if opcion == 'q':
			break
		else:
			print('Ingrese una opción válida...')
		if opcion == '1':
			### TO DO
			continue
		elif opcion == '2':
			### TO DO
			continue
		elif opcion == '3':
			###TO DO
			prob_redes = ProblemaRedes(adyacencia, costos, capacidades)
			prob_redes.matriz_variables_decision = np.array([0,6,0,0,0,0,0,0,6,0,0,0,0,4,0,0,0,0,0,5,0,0,0,0,0])
			prob_redes.matriz_variables_basicas = np.array([False,True,False,False,False,False,False,False,True,False,False,False,False,True,False,	False,False,False,False,True,False,False,False,False,False])
			print(solucion_mcfp(prob_redes.z))
			input("Presiona enter...")
		elif opcion == 'o':
			### TO DO
			continue
		elif opcion == 'q':
			matriz = 0

	return matriz


def menu_transporte():
	clear_screen()
	matriz = menu_ingresar_matriz_costos('TRANSPORTE')
	if matriz is 0:
		return
	while True:
		print("METODOS PARA PROBLEMAS DE TRANSPORTE")
		print("1) Esquina Noroeste")
		print("2) Costo minimo")
		print("3) Aproximacion de Voguel")
		print("4) Método húngaro (Asignacion)")
		print("m) Utilizar otra matriz")
		print("q) Regresar al menu anterior")

		opc = input('¿Qué desea hacer?: ')
		if opc == 'q':
			break
		elif opc == 'm':
			matriz = menu_ingresar_matriz_costos('TRANSPORTE')
			continue

		sol_problema_transporte(matriz, opc)


def menu_redes():
	while True:
		clear_screen()

		print("METODOS PARA PROBLEMAS DE REDES")
		print("¿Qué método desea utilizar?:")
		print("1) Camino más corto, Dijkstra")
		print("2) Floyd-Warshal")
		print("4) Flujo de Redes a costo mínimo(simple)")
		print("q) Regresar al menu anterior")

		opc = input('¿Qué desea hacer?: ')
		if opc == 'q':
			break
		elif opc == '1' or opc == '2':
			matriz = menu_ingresar_matriz_costos('REDES')
			switcher_metodos_redes[opc](matriz).menu()
			continue
		elif opc == '4':
			menu_sol_bas_fact_inicial_mcfp()
			continue


def menu_programacion_entera():
	while True:
		ppl_ingresado = menu_ingresar_matriz_costos('PROGRAMACIÓN ENTERA', True)
		if ppl_ingresado is None:
			continue
		if ppl_ingresado is 0:
			return
		else:
			break
	while True:
		clear_screen()
		print("METODOS PARA PROBLEMAS DE PROGRAMACIÓN ENTERA")
		print("¿Qué método desea utilizar?:")
		print("1) Resolver por Branch and Bound")
		print("2) Resolver por enumeración implícita (sólo binario)")
		print("m) Utilizar otro ppl")
		print("q) Regresar al menu anterior")

		opc = input('¿Qué desea hacer?: ')
		if opc == 'q':
			break
		elif opc == 'm':
			ppl_ingresado = menu_ingresar_matriz_costos('PROGRAMACIÓN ENTERA', True)
			continue
		num = check_int(opc)
		if num is not None and num < 3:
			z, tipo_ppl, restricciones, lado_derecho, binario = ppl_ingresado
			if num == 2 and not binario:
				print('** Escogió enumeración implícita, pero el problema no es binario... **')
				print('** Si continua se resolverá como un problema binario. **')
				print('** Si desea otro metodo, escoja no continuar. **')
				if confirmacion('¿Desea resolver como problema binario?'):
					binario = True
				else:
					continue
			switcher_metodos_entera[opc](z, tipo_ppl, restricciones, lado_derecho, binario).menu()
