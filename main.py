### main ###
import menus
import os
import sys


def main():
    opcion = "z"
    matriz_costos = []
    print("******************************************************")
    print("*			Proyecto final optimizacion II		 	*")
    print("******************************************************")
    print("Integrantes: ")
    print("\n")
    print("\tCabrejos Reyes Eliseo Aldair")
    print("\tFlores Zenteno Alfonso")
    print("\tMejía Maldonado José Fernando")
    print("\tTenorio Lugo Brandon Alexis")
    print("\n\n\n")

    input("Presione Enter para continuar...")

    while opcion != "q":

        if sys.platform[:3] == "win":
            os.system("cls")
        if sys.platform[:5] == "linux" or sys.platform[:6] == "darwin":
            os.system("clear")

        menus.menu_principal()
        opcion = input("¿Que desea hacer?: ")

        if opcion == "1":
            matriz_costos = menus.menu_ingresar_matriz_costos()
            menus.menu_metodos_transporte(matriz_costos)

        elif opcion == "q":
            exit()


if __name__ == "__main__":
    main()
