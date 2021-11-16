import math
import os
import os.path
import json

from cv2 import putText

def esCuadrada(izquierda, derecha, Cua):
    count = 0
    for idx,lista in enumerate(Cua[0]):
        if idx <7:          
            print(izquierda[idx])  
            if (lista[0] <= izquierda[idx]) and (izquierda[idx] <= lista[1]):
                count += 1
        else:
            print(derecha[idx-7])  

            if (lista[0] <= derecha[idx-7]) and (derecha[idx-7] <= lista[1]):
                count += 1
    if count >= 10:
        print('es cuadrada')
        return 'es cuadrada'
    else:
        return 'no es cuadrada'

def esOvalado(izquierda, derecha, Ov):
    count = 0
    
    for idx,lista in enumerate(Ov[0]):
        if idx <7:
            if (lista[0] <= izquierda[idx]) and (izquierda[idx] <= lista[1]):
                count += 1
        else:
            if (lista[0] <= derecha[idx-7]) and (derecha[idx-7] <= lista[1]):
                count += 1
    if count >= 8:
        print('es ovalada')
        return 'es ovalada'
    else:
        return 'no es ovalada'
        
        

    
    

def function(largo,ancho,mandibulacua,mandibulaova):
    #define el tipo de rostro
    if (ancho + (ancho/3))<largo:
        if mandibulacua == 'es cuadrada':
            print("tu cara es rectangular")
            return "rectangular"
        else:
            print("tu cara es alargada")
            return "alargada"
    else:
        print(largo)
        print(ancho)
        if largo<=ancho+(0.01) and largo>=ancho-(0.01):
            if mandibulacua == 'es cuadrada':
                print("tu cara es cuadrada")
                return "cuadrada"
            else:
                print("tu cara es redonda")
                return "redonda"
        else:
            #codigo gerson 
            if mandibulacua == 'es cuadrada':
                print("tu cara es triangular")
                return "triangular"
            elif mandibulaova == 'es ovalada':
               print("tu cara es ovalada")
               return "ovalada"
                
            else:
                print('tu cara tiene forma de corazon')
                return "corazon"
                



def principal(largo, ancho, izquierda ,derecha):
    tf = open("cuadrado.json", "r")
    tf2= open("ovalado.json", "r")
    new_dict = json.load(tf)
    new_dict2 = json.load(tf2)
    cuadrado = list(new_dict.values())
    ovalado = list(new_dict2.values())
    EC = esCuadrada(izquierda, derecha, cuadrado)
    EO = esOvalado(izquierda, derecha, ovalado)
    print(EC)
    print(EO)

    tt = function(largo,ancho,EC,EO)
    return tt
#principal("asd","asd","asd","asd")