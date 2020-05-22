### mostrar transporte ###
from tabulate import tabulate
from utils.Functions import clear_screen

def imprimir_solucion(prob_transporte):
    clear_screen()
    print("Los flujos que minimizan el costo son:")
    for i,renglon in enumerate(prob_transporte.matriz_variables_basicas):
        for j, elemento in enumerate(renglon):
            if elemento and prob_transporte.matriz_variables_decision[i][j] != 0:
                print(prob_transporte.nombres_oferta[i] + " -> " + prob_transporte.nombres_demanda[j] +" flujo de " + str(prob_transporte.matriz_variables_decision[i][j]))
    print("Con un costo de: {0}".format(prob_transporte.z))
    input("\n\nPresione Enter para continuar...")


def imprimir_costos(prob_transporte):
    clear_screen()
    cabecera = prob_transporte.nombres_demanda.copy()
    cabecera.insert(0, " ")
    tabla =[]
    print("Mostrando la matriz de costos")
    for i, renglon in enumerate(prob_transporte.matriz_costos):
        renglon_tab = []
        renglon_tab.append(prob_transporte.nombres_oferta[i])
        for elemento in renglon:
            if elemento < 9999:
                renglon_tab.append(elemento)
            else:
                renglon_tab.append("-")
        tabla.append(renglon_tab)
    print(tabulate(tabla, cabecera, tablefmt = "fancy_grid"))
    input("\n\nPresione Enter para continuar...")
    return


def imprimir_oferta_demanda(prob_transporte):
    clear_screen()
    print("La oferta es: ")
    cabecera = prob_transporte.nombres_oferta.copy()
    tabla = [[]]
    for elemento in prob_transporte.oferta:
        tabla[0].append(elemento)
    print(tabulate(tabla, cabecera, tablefmt = "fancy_grid"))
    print("La demanda es: ")
    cabecera = prob_transporte.nombres_demanda
    tabla = [[]]
    for elemento in prob_transporte.demanda:
        tabla[0].append(elemento)
    print(tabulate(tabla, cabecera, tablefmt = "fancy_grid"))
    input("\n\nPresione Enter para continuar...")
    return


def mostrar_problema(prob_transporte):
    while True:
        clear_screen()
        print("Información del problema de transporte:")
        print("1) Costos del problema")
        print("2) Oferta y demanda")
        print("3) Solucion")
        print("q) Regresar")
        opcion = input("¿Qué desea ver?: ")

        if opcion == '1':
            imprimir_costos(prob_transporte)
        elif opcion == '2':
            imprimir_oferta_demanda(prob_transporte)
        elif opcion == '3':
            imprimir_solucion(prob_transporte)
        elif opcion == 'q':
            break
        else: 
            print("Opcion inválida...")
            input("\n\nPresione Enter para continuar...")
    return
