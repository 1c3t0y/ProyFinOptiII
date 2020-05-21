class flujoMaximo:
    def __init__(self, matriz):
        self.data = matriz
        self.resultados = []
        self.FM = 0
        self.errorcatcher = 0
        self.i = [0]
        self.n = len(matriz[0]) -1
        self.k = []
    
    
    def maxRow(self, arr):
        max_num = 0
        for x in arr:
            if( type(x) == str ):
                continue
            if( x >= max_num ):
                max_num = x

        return[max_num, arr.index(max_num)]
    
    
    def minRow(self, arr):
        min_num = self.maxRow(arr)[0]
        for x in arr:
            if( type(x) == str or x == 0):
                continue
            if( x < min_num ):
                min_num = x

        return[min_num, arr.index(min_num)]


    def printMatrix(self, arr):
        n = len(arr)
        for i in range(0,n):
            print(arr[i])
          
        
    def isInArray(self, arr, x):
        resp = False
        for z in arr:
            if( type(z) == str ):
                continue
            if( z == x ):
                resp = True

        return(resp)


    def maxRowCompare2(self, arr1, arr2):
        maxc = self.maxRow(arr1)
        aux = arr1.copy()

        while self.isInArray(arr2, maxc[1]) == True:
            idc = aux.index(maxc[0])
            aux[idc] = 'x'
            gde = self.maxRow(aux)[0]
            maxc = [gde, aux.index(gde)]

        return maxc


    def step2(self, arr1, arr2):
        result = []

        for elem in range(0, len(arr1)):

            if type(arr1[elem]) != str:
                if(arr1[elem] > 0 and self.isInArray(arr2, elem)== False ):
                    result.append( (arr1[elem], elem) )

        return result


    def step3(self, arr1):
        result = arr1[0]

        for x in arr1:
            if x[0] > result[0]:
                result = x

        return result


    def step4(self):

        r = self.i[-2]
        result = []

        for k in range(0, len(self.data[r])):
            if type(self.data[r][k]) != str:
                if (self.data[r][k] > 0 and self.isInArray(self.i, k) == False ):
                    result.append( (self.data[r][k], k) ) 

        self.i.pop()

        return result


    def step5(self,k,i):
        f = []
        for x in k:
            f.append(x[0])
            
        flujoMax = self.minRow(f)[0]


        for y in range(0, len(i)-1): #proceso para reajustar valores de matriz
            if type(self.data[i[y]][i[y+1]]) != str:
                self.data[i[y]][i[y+1]] -= flujoMax
            if type(self.data[i[y+1]][i[y]]) != str:
                self.data[i[y+1]][i[y]] += flujoMax

        self.resultados.append((i,flujoMax))
        #print('\nLa ruta encontrada es: ', i, ' con flujo máximo de: ', flujoMax)
        #self.printMatrix(self.data)


    def step6(self):

        for obj in self.resultados:
            self.FM += obj[1]

        #print('\nFlujo Máximo de la red, F =', self.FM)
        #print('\n\n Lista de Rutas: ', self.resultados)
        
    
    def solverFlujoMaximo(self):

        while self.isInArray(self.i , self.n) == False:

            if(self.errorcatcher > self.n):
                self.step6()
                break

            if self.maxRow(self.data[0])[0] == 0:
                self.step6()
                break

            S_i = self.step2(self.data[self.i[-1]], self.i)

            if len(S_i) != 0 :
                self.k.append(self.step3(S_i))
                self.i.append(self.k[-1][1])
            else:
                #Posibilidad de fin de ruta
                if(self.i[-1] == 1):
                    self.step6()
                    continue

                #Se calcula de nuevo el S_i tomando un paso atrás
                S_i = self.step4()
                self.k.pop()

                if len(S_i) != 0 :
                    self.k.append(self.step3(S_i))
                    self.i.append(self.k[-1][1])

                elif len(S_i) == 0 and len(self.i) == 1:
                    print('Dead End')
                else:
                    #print('Otra iteración de step4 ?')
                    self.errorcatcher += 1
                    S_i = self.step4()
                    self.k.pop()

                    if len(S_i) != 0 :
                        self.k.append(self.step3(S_i))
                        self.i.append(self.k[-1][1])

                #print('Excepcion:', k, i, S_i)


            #print('Check: ', i, S_i, k)

            if self.k[-1][1] == self.n:
                self.step5(self.k,self.i)
                self.i = [0]
                self.k = []