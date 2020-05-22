### mostrar simplex ###
from tabulate import tabulate
from utils.Functions import clear_screen

def imprimir_solucion(prob_redes):
    clear_screen()
    print("Los flujos que minimizan el costo son:")
    for i,renglon in enumerate(prob_redes.matriz_variables_basicas):
        for j, elemento in enumerate(renglon):
            if elemento and prob_redes.matriz_variables_decision[i][j] != 0:
                print(prob_redes.nombres[i] + " -> " + prob_redes.nombres[j] +" flujo de " + str(prob_redes.matriz_variables_decision[i][j]))
    print("Con un costo de: {0}".format(prob_redes.z))
    input("\n\nPresione Enter para continuar...")


def imprimir_costos(prob_redes):
    clear_screen()
    cabecera = prob_redes.nombres.copy()
    cabecera.insert(0," ")
    tabla =[]
    print("Mostrando la matriz de costos")
    for i, renglon in enumerate(prob_redes._matriz_costos):
    	renglon_tab = []
    	renglon_tab.append(prob_redes.nombres[i])
    	for elemento in renglon:
    		if elemento < 999:
    			renglon_tab.append(elemento)
    		else:
    			renglon_tab.append("-")
    	tabla.append(renglon_tab)
    print(tabulate(tabla, cabecera, tablefmt = "fancy_grid"))
    input("\n\nPresione Enter para continuar...")
    return


def imprimir_adyacencia(prob_redes):
    clear_screen()
    print("La adyacencia de cada nodo es: ")
    for i, nodo in enumerate(prob_redes.matriz_adyacencia):
        adyacencia = []
        for j, elemento in enumerate(nodo):
            if elemento:
                adyacencia.append(prob_redes.nombres[j])
        print("El nodo " + prob_redes.nombres[i] + " manda flujo a: " + ','.join(adyacencia))
    input("\n\nPresione Enter para continuar...")
    return

def imprimir_capacidades(prob_redes):
    clear_screen()
    print("Las capacidades de cada nodo son: ")
    cabecera = prob_redes.nombres
    tabla = []
    tabla.append(prob_redes.recursos)
    print(tabulate(tabla, cabecera, tablefmt = "fancy_grid"))
    input("\n\nPresione Enter para continuar...")
    return

def mostrar_problema(prob_redes):
    while True:
        clear_screen()
        print("Información del problema de redes:")
        print("1) Adyacencia del problema")
        print("2) Costos del problema")
        print("3) Capacidades de los nodos")
        print("4) Solucion")
        print("q) Regresar")
        opcion = input("¿Qué desea ver?: ")

        if opcion == '1':
            imprimir_adyacencia(prob_redes)
        elif opcion == '2':
            imprimir_costos(prob_redes)
        elif opcion == '3':
            imprimir_capacidades(prob_redes)
        elif opcion == '4':
            imprimir_solucion(prob_redes)
        elif opcion == 'q':
            break
        else: 
            print("Opcion inválida...")
            input("\n\nPresione Enter para continuar...")
    return