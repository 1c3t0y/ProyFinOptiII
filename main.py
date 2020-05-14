### main ###
import menus 
import os
import sys


def main():
	opcion = 'z'
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

	while opcion != 'q':
	
		if sys.platform[:3] == 'win':
			os.system('cls')
		if sys.platform[:5] == 'linux' or sys.platform[:6] == 'darwin':
			os.system('clear')

		menus.menu_principal()
		opcion = input("¿Que desea hacer?: ")

		if opcion == '1':
			menus.menu_metodos_transporte()
		if opcion == '2':
			menus.menu_redes()
		if opcion == '3':
			menus.menu_programacion_entera()

		elif opcion == 'q':
			exit()


if __name__ == "__main__":
	main()
