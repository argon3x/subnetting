#!/usr/bin/python3
# codign: utf-8
from os import system
from time import sleep
import signal

# colores
verde = "\033[01;32m"; rojo = "\033[01;31m"
azul = "\033[01;34m"; purpura = "\033[01;35m"
amarillo = "\033[01;33m"; fin = "\033[00m"

# Señal para cancelar el proceso del script
def handler(signum, frame):
    print(f"\n\n {azul}>>> {rojo}Proceso Terminado {azul}<<<{fin}\n")
    exit(1)

signal.signal(signal.SIGINT, handler)


# Funcion Principal
def main(subredes, direccion_red, mascara_red):
    # Calcula Los Saltos De Red
    def calcularSaltos(nueva_subred):
        # formula -> 2**m - 2 = hosts disponibles
        # formula -> 2**m = saltos
        zeros = 8 - int(nueva_subred[0])

        saltos_red = 2**zeros
        hosts_disponibles = (2**zeros) - 2

        return saltos_red, hosts_disponibles

    
    # Calcula La Nueva Submascara de Red de Binario a Decimal y Decimal a Binario
    def calcularSubMascara(mascara_red, nueva_subred):
        octetos_binarios = []
        separar_octetos = mascara_red.split('.')

        for i in separar_octetos:
            enteros = int(i)
            binario = bin(enteros)[2:].zfill(8)
            octetos_binarios.append(binario)
        
        c = 1
        nuevos_octetos_binarios = []
        octetos_modificados = []
        for i in octetos_binarios:
            if i.count('0') >= 1:
                while c <= 8:
                    if c <= nueva_subred:
                        octetos_modificados.append('1')
                    else:
                        octetos_modificados.append('0')
                    c+=1
                union = ''.join(octetos_modificados)
                nuevos_octetos_binarios.append(union)
            else:
                nuevos_octetos_binarios.append(i)

        mascara_decimales = []
        for i in nuevos_octetos_binarios:
            decimal = int(i, 2)
            mascara_decimales.append(str(decimal))


        nueva_mascara_decimal = '.'.join(mascara_decimales)
        nueva_mascara_binaria = '.'.join(nuevos_octetos_binarios)
        numero_mascara = nueva_mascara_binaria.count('1')

        return nueva_mascara_decimal, numero_mascara


    # Calucla La Nueva Subred
    def calcularSubRedes(subredes):
        # formula -> 2**n - 2 >= subredes
        n = 1
        
        while n < 254: 
            total = (2**n) - 2
            if total >= subredes:
                #print(total)
                break

            n+=1

        return n, total
    
    # Valores De La Funciones Anidadas
    nueva_subred = calcularSubRedes(subredes)
    nueva_submascara = calcularSubMascara(mascara_red, nueva_subred[0])
    saltos_de_red = calcularSaltos(nueva_subred)

    # Muestra Todos Los Valores 
    print(f'{azul}*{fin}' * 50)
    print(f"{rojo} > {amarillo}Cantidad De Subredes {purpura}=> {verde}{subredes}{fin}")
    print(f"{rojo} > {amarillo}Hosts Por Subred {purpura}=> {verde}{saltos_de_red[1]}{fin}")
    print(f"{rojo} > {amarillo}Nueva Mascara De Red {purpura}=> {verde}{nueva_submascara[0]}/{nueva_submascara[1]}{fin}")
    print(f'{azul}*{fin}' * 77)
    
    # Genera La Tabla De Saltos
    direccion_de_red = direccion_red.split('.')
    sr = int(saltos_de_red[0])
    c, s = 1, 0
    
    print(f"{amarillo}   N°\tSubred\t\tInicio\t\tFinal\t\tBroadcast{fin}")
    print(f'{azul}*{fin}' * 77)
    while c <= subredes:
        red = '.'.join(direccion_de_red[0:3])
        host = int(direccion_de_red[-1]) + s
        print(f"{azul}   {c}\t{purpura}{red}.{host}\t{azul}{red}.{host + 1}\t{purpura}{red}.{(sr * c) - 2}\t{azul}{red}.{(sr * c) - 1}{fin}")
        print(f'{azul}*{fin}' * 77)

        s+=sr
        c+=1


# Obtencion de Datos
if __name__ == '__main__':
    subredes = int(input(f"{purpura}:> {amarillo}Subredes{fin}: "))
    direccion_red = input(f"{purpura}:> {amarillo}Direccion De Red{fin}: ")
    mascara_red = input(f"{purpura}:> {amarillo}Mascara De Red{fin}: ")
    
    sleep(0.5)
    system('clear')
    main(subredes, direccion_red, mascara_red)

