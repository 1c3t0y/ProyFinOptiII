def inputMatrix():
    from csv import reader
    
    data = []
    chc = input('Ingresar la matriz inicial: \n\n 1) Desde un csv \n 2) Desde terminal \n')
    
    if chc == '1':
        nombre = input('nombre del archivo csv: ')
        # read csv file as a list of lists
        with open(nombre + '.csv', 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Pass reader object to list() to get a list of lists
            data = list(csv_reader)
        
        for i in range(0, len(data[0])):
            for j in range(0, len(data[0])):
                if data[i][j] != 'x':
                    data[i][j] = int(data[i][j])
            
    elif chc == '2':
        nod = int(input('\n Número de nodos en la red: '))
            
        for i in range(0, nod):
            data.append([])
            for j in range(0, nod):
                if i == j:
                    data[i].append('x')
                else:
                    print('Costo para ir del nodo ', i+1, ' al nodo ', j+1,'. Si no hay conexión esciba: x .')
                    cst = input()
                    if cst == 'x':
                        data[i].append('x')
                    else:
                        data[i].append(int(cst))
                        
    return data
                   
    
def isInArray(arr, x):
    resp = False
    for z in arr:
        if( type(z) == str ):
            continue
        if( z == x ):
            resp = True
        
    return(resp)

def expansionMinima(data):
    # Valores iniciales del proceso
    inicio = 0
    n = len(data)
    ruta = [inicio]
    nodos = []
    k = []
    costo = 0

    for i in range(0, n):
        if i != inicio:
            nodos.append(i)


    # Inicia el proceso

    while len(nodos) > 0:
        aux = []
        for i in ruta:
            for j in range(0,n):
                if type(data[i][j]) != str :
                    if isInArray(ruta, j) == False:
                        aux.append((i, j, data[i][j]))

        small = aux[0]

        for elem in aux:
            if elem[2] <= small[2]:
                small = elem

        costo += small[2]
        k.append(small)
        ruta.append(small[1])
        nodos.remove(small[1])

    # print(ruta, k, nodos, costo)
    print('Costo del árbol: ', costo)
    print('\nConexiones: ')
    for elem in k:
        print('Nodo ', elem[0]+1, ' con el nodo ', elem[1]+1, ' por el costo de ', elem[2])