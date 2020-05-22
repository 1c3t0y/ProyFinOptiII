### main ###
import menus
from utils.Functions import confirmacion


def main():
	opcion = 'z'
	print("*************************************************************************")
	print("*			Proyecto final optimizacion II		 	*")
	print("*************************************************************************")
	print("Integrantes: ")
	print("\n")
	print("\tCabrejos Reyes Eliseo Aldair")
	print("\tFlores Zenteno Alfonso")
	print("\tMejía Maldonado José Fernando")
	print("\tTenorio Lugo Brandon Alexis")
	print("\n\n\n")

	input("Presione Enter para continuar...")

	while True:

		menus.menu_principal()
		opcion = input("¿Que desea hacer?: ")

		if opcion == '1':
			menus.menu_transporte()
		if opcion == '2':
			menus.menu_redes()
		if opcion == '3':
			menus.menu_programacion_entera()

		elif opcion == 'q':
			if not confirmacion('Está saliendo del programa. ¿Está seguro?'):
				continue
			exit()


if __name__ == "__main__":
	main()
