import utils.ingresar_datos as datos
from utils.Functions import check_int, confirmacion, clear_screen

import utils.mostrar_asignacion as ma
import utils.mostrar_transporte as mt
import utils.mostrar_simplex as ms

from Transporte.metodo_mav import metodo_MAV
from Transporte.metodo_esquina_ne import metodo_esquina_NE
from Transporte.metodo_costo_minimo import metodo_costo_minimo
from Transporte.metodo_hungaro import metodo_hungaro

from Redes.solucion_inicial_simplex import m_grande
from Redes.solucion_inicial_simplex import solucion_inicial_manual

from utils.switcher_métodos import switcher_metodos_redes, switcher_metodos_entera
from Redes.arbolExpMin import inputMatrix, expansionMinima
from Redes.flujoMax import flujoMaximo


def menu_principal():
	clear_screen()
	print("Menu de opciones:")
	print("1) Resolver un problema de transporte")
	print("2) Resolver un problema de redes")
	print("3) Resolver un problema de programación entera")
	print("q) Salir")


def menu_ingresar_matriz_costos(msg: str = "TRANSPORTE", ppl: bool = False):
	while True:
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
		if matriz is not None:
			return matriz

def menu_ingresar_transporte(asignacion: bool = False):
	if asignacion:
		problema = "ASIGNACION"
	else:
		problema = "TRANSPORTE"
	print(f'PROBLEMA DE {problema}')
	print("Opciones para ingresar datos:")
	print(f"1) Ingresar problema manualmente")
	print(f"2) Ingresar problema desde archivos csv")
	print("q) regresar al menú anterior.")

	while True:
		opcion = input('¿Qué desea hacer?: ')
		if opcion == 'q' or (check_int(opcion) is not None and 0 < check_int(opcion) <= 2):
			break
		else:
			print('Ingrese una opción válida...')
	if opcion == '1' and not asignacion:
		matriz_costos, oferta, demanda, nombres_origen, nombres_destino = datos.ingresar_transporte_manualmente()
	elif opcion == '1' and asignacion:
		matriz_costos, nombres_origen, nombres_destino = datos.ingresar_asignacion_manualmente()
	elif opcion == '2'and not asignacion:
		matriz_costos, oferta, demanda, nombres_origen, nombres_destino = datos.ingresar_transporte_csv()
	elif opcion == '2'and asignacion:
		matriz_costos, nombres_origen, nombres_destino = datos.ingresar_asignacion_csv()
	elif opcion == 'q':
		return 0,0,0,0,0

	if asignacion:
		return matriz_costos, nombres_origen, nombres_destino
	else: 
		return matriz_costos, oferta, demanda, nombres_origen, nombres_destino

def menu_ingresar_red():
	print(f'PROBLEMA DE REDES POR SIMPLEX')
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
		matriz_adyacencia, matriz_costos, capacidades, nombres = datos.ingresar_red_manualmente()
	elif opcion == '2':
		matriz_adyacencia, matriz_costos, capacidades, nombres = datos.ingresar_red_csv()
	elif opcion == 'q':
		return 0,0,0

	return matriz_adyacencia, matriz_costos, capacidades, nombres


def menu_sol_bas_fact_inicial_red():
	adyacencia, costos, capacidades, nombres = menu_ingresar_red()
	if adyacencia is 0:
		return
	while True:
		clear_screen()
		print(f'SOLUCIONAR RED POR SIMPLEX')
		print("Opciones para SOLUCIÓN BÁSICA FACTIBLE INICIAL:")
		print(f"1) Método de la M grande")
		print(f"2) Dar una solución básica factible")
		print(f"o) Dar otro MCFP")
		print("q) regresar al menú anterior.")
		opcion = input('¿Qué desea hacer?: ')
		if opcion == 'q':
			break
		elif opcion == '1':
			prob_redes = m_grande(adyacencia, costos, capacidades, nombres)
			ms.mostrar_problema(prob_redes)
			continue
		elif opcion == '2':
			prob_redes = solucion_inicial_manual(adyacencia, costos, capacidades, nombres)
			if prob_redes is None:
				continue
			else:
				ms.mostrar_problema(prob_redes)
		elif opcion == 'o':
			adyacencia_aux, costos_aux, capacidades_aux = menu_ingresar_red()
			if not (adyacencia_aux is 0):
				matriz_adyacencia = adyacencia_aux
				matriz_costos = costos_aux
				capacidades = capacidades_aux
			continue
		elif opcion == 'q':
			break
		else:
			print('Ingrese una opción válida...')
			input('Presione enter para continuar...')
	return


def menu_transporte():
	clear_screen()
	opcion = input("¿Desea ingresar un problema de asignacion?(S/n): ")
	if opcion == 'S' or opcion == 'S':
		matriz_costos, nombres_origen, nombres_destino = menu_ingresar_transporte(True)
		asignacion = True
	else:
		matriz_costos, oferta, demanda, nombres_origen, nombres_destino = menu_ingresar_transporte()
		asignacion = False
	
	if matriz_costos is 0:
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
		elif opc == '1' and not asignacion:
			prob_transporte = metodo_esquina_NE(matriz_costos, oferta, demanda, nombres_origen, nombres_destino)
			mt.mostrar_problema(prob_transporte)
		elif opc == '2' and not asignacion:
			prob_transporte = metodo_costo_minimo(matriz_costos, oferta, demanda, nombres_origen, nombres_destino)
			mt.mostrar_problema(prob_transporte)
		elif opc == '3' and not asignacion:
			prob_transporte = metodo_MAV(matriz_costos, oferta, demanda, nombres_origen, nombres_destino)
			mt.mostrar_problema(prob_transporte)
		elif opc == '4' and asignacion:
			problema_asignacion = metodo_hungaro(matriz_costos, nombres_origen, nombres_destino)
			ma.mostrar_problema(problema_asignacion)
		elif opc == 'm':
			opcion = input("¿Desea ingresar un problema de asignacion?(S/n): ")
			if opcion == 'S' or opcion == 'S':
				costos_aux, nombres_origen_aux, nombres_destino_aux = menu_ingresar_transporte(True)
				asignacion = True
			else:
				costos_aux, oferta_aux, demanda_aux, nombres_origen_aux, nombres_destino_aux = menu_ingresar_transporte()
				asignacion = False
			if not (costos_aux is 0) and not asignacion:
				matriz_costos = costos_aux
				oferta = oferta_aux
				demanda = demanda_aux
				nombres_origen = nombres_origen_aux
				nombres_destino = nombres_destino_aux
			else:
				matriz_costos = costos_aux
				nombres_origen = nombres_origen_aux
				nombres_destino = nombres_destino_aux
			continue
		elif opcion in ['1','2','3'] and asignacion:
			print("El problema que ingresó es de asignación, por lo que no es válido para éste método")
			input('Presione enter para continuar...')
		elif opcion == '4' and not asignacion:
			print("El problema que ingresó es de transporte, por lo que no es válido para éste método")
			input('Presione enter para continuar...')
		else:
			print('Ingrese una opción válida...')
			input('Presione enter para continuar...')
			continue
	return 

def menu_redes():
	while True:
		clear_screen()

		print("METODOS PARA PROBLEMAS DE REDES")
		print("¿Qué método desea utilizar?:")
		print("1) Camino más corto, Dijkstra")
		print("2) Floyd-Warshal")
		print("3) Árbol de Expansión Mínima")
		print("4) Flujo Máximo ")
		print("5) Método simplex para redes")
		print("q) Regresar al menu anterior")

		opc = input('¿Qué desea hacer?: ')

		if opc == 'q':
			break
		elif opc == '1' or opc == '2':
			matriz = menu_ingresar_matriz_costos('REDES')
			if matriz is not None and matriz is not 0:
				switcher_metodos_redes[opc](matriz).menu()
			continue
		elif opc == '5':
			menu_sol_bas_fact_inicial_red()
			continue
		elif opc == '3':
			data = inputMatrix()
			expansionMinima(data)
			wait = input('\n Presiona cualquier tecla para continuar.')
			continue
		elif opc == '4':
			data = inputMatrix()
			objectMFS = flujoMaximo(data)
			objectMFS.solverFlujoMaximo()
			print('\nFlujo Máximo de la red, F =', objectMFS.FM)
			print('\nLista de Rutas: ', objectMFS.resultados)
			wait = input('\n Presiona cualquier tecla para continuar.')
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
