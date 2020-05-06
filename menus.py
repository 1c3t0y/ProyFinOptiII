### menus ###
import os
import sys
import ingresar_datos as datos
import sol_problema_transporte as spt


def menu_principal():
    print("Menu de opciones:")
    print("1) Resolver un problema de transporte")
    print("q) Salir")


def menu_ingresar_matriz_costos():
    matriz = 0

    opcion = "z"
    print("PROBLEMAS DE TRANSPORTE")
    print("Opciones para ingresar datos:")
    print("1) Ingresar una matriz manualmente")
    print("2) Ingresar una matriz desde un archivo csv")
    print("q) regresar al menú principal.")

    opcion = input("¿Qué desea hacer?: ")

    if opcion == "1":
        matriz = datos.ingresar_matriz_manualmente()
    elif opcion == "2":
        matriz = datos.ingresar_matriz_csv()
    elif opcion == "q":
        matriz = 0

    return matriz


def menu_metodos_transporte(matriz_costos):
    opcion = "z"

    print("METODOS PARA PROBLEMAS DE TRANSPORTE")
    print("¿Qué método desea utilizar?:")
    print("1) Esquina Noroeste")
    print("2) Costo minimo")
    print("3) Aproximacion de Voguel")
    print("4) Método húngaro (Asignacion)")
    print("q) Regresar al menu anterior")

    opcion = input("¿Qué método desea utilizar?: ")

    spt.sol_problema_transporte(matriz_costos, opcion)
