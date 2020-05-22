#### mostrar informacion asignacion ###
from tabulate import tabulate
from utils.Functions import clear_screen

def imprimir_solucion(prob_asignacion):
    clear_screen()
    print("La asignación que minimiza el costo es: ")
    print("Nombre -> Actividad")
    for i,renglon in enumerate(prob_asignacion.matriz_variables_decision):
        for j, elemento in enumerate(renglon):
            if elemento:
                print(prob_asignacion.nombres_oferta[i] + " -> " + prob_asignacion.nombres_demanda[j])
    print("Con un costo de: {0}".format(prob_asignacion.z))
    input("\n\nPresione Enter para continuar...")

def imprimir_costos(prob_asignacion):
    clear_screen()
    cabecera = prob_asignacion.nombres_demanda.copy()
    cabecera.insert(0, " ")
    tabla =[]
    print("Mostrando la matriz de costos")
    for i, renglon in enumerate(prob_asignacion.matriz_costos):
        renglon_tab = []
        renglon_tab.append(prob_asignacion.nombres_oferta[i])
        for elemento in renglon:
            if elemento < 999:
                renglon_tab.append(elemento)
            else:
                renglon_tab.append("-")
        tabla.append(renglon_tab)
    print(tabulate(tabla, cabecera, tablefmt = "fancy_grid"))
    input("\n\nPresione Enter para continuar...")
    return

    
def mostrar_problema(prob_asignacion):
    while True:
        clear_screen()
        print("Información del problema de asignacion:")
        print("1) Costos del problema")
        print("2) Solucion")
        print("q) Regresar")
        opcion = input("¿Qué desea ver?: ")

        if opcion == '1':
            imprimir_costos(prob_asignacion)
        elif opcion == '2':
            imprimir_solucion(prob_asignacion)
        elif opcion == 'q':
        	break
        else: 
            print("Opcion inválida...")
            input("\n\nPresione Enter para continuar...")
    return
