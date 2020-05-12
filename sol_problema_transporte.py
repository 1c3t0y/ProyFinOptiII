### solucionar problemas transporte ###
import utils.ingresar_datos as datos
import classes.problemas_optimizacion as po
import metodo_esquina_ne as men
import metodo_costo_minimo as mcm
import metodo_mav as mav
import metodo_hungaro as mh


def sol_problema_transporte(matriz_costos, opcion):
	if opcion == '1':
		oferta, demanda = datos.ingresar_oferta_demanda(matriz_costos.shape)
		problema_transporte = po.ProblemaTransporte(matriz_costos.shape[0], matriz_costos.shape[1], matriz_costos, oferta, demanda)
		problema_transporte = men.metodo_esquina_NE(problema_transporte)
		print(problema_transporte.matriz_variables_decision)
		input("Presione Enter para continuar...")
	elif opcion == '2':
		oferta, demanda = datos.ingresar_oferta_demanda(matriz_costos.shape)
		problema_transporte = po.ProblemaTransporte(matriz_costos.shape[0], matriz_costos.shape[1], matriz_costos, oferta, demanda)
		prob_transporte = mcm.metodo_costo_minimo(problema_transporte)
		print(prob_transporte.matriz_variables_decision)
		input("Presione Enter para continuar...")
	elif opcion == '3':
		oferta, demanda = datos.ingresar_oferta_demanda(matriz_costos.shape)
		problema_transporte = po.ProblemaTransporte(matriz_costos.shape[0], matriz_costos.shape[1], matriz_costos, oferta, demanda)
		prob_transporte = mav.metodo_MAV(problema_transporte)
		print(prob_transporte.matriz_variables_decision)
		input("Presione Enter para continuar...")
	elif opcion == '4':
		problema_transporte = po.ProblemaAsignacion(matriz_costos)
		prob_transporte = mh.metodo_hungaro(problema_transporte)
		print(prob_transporte.matriz_variables_decision)
		input("Presione Enter para continuar...")
