import datetime as dt
import re
import csv
import pandas as pd
from openpyxl.styles import Alignment
import xlsxwriter

dic_principal = {}

# Función para calcular el promedio de los montos de las notas en un período
def calcular_promedio_montos():
    print("\nCÁLCULO DEL PROMEDIO DE MONTOS DE NOTAS EN UN PERÍODO")
    while True:
        try:
            fecha_inicial = input("Fecha inicial del período (DD/MM/AAAA): ")
            fecha_inicial = dt.datetime.strptime(fecha_inicial, "%d/%m/%Y")
        except ValueError:
            print("Formato de fecha incorrecto. Ingrese la fecha en el formato DD/MM/AAAA.")
            continue

        while True:
            try:
                fecha_final = input("Fecha final del período (DD/MM/AAAA): ")
                fecha_final = dt.datetime.strptime(fecha_final, "%d/%m/%Y")
            except ValueError:
                print("Formato de fecha incorrecto. Ingrese la fecha en el formato DD/MM/AAAA.")
                continue

            if fecha_final < fecha_inicial:
                print("La fecha final debe ser mayor o igual a la fecha inicial.")
                continue

            break

        monto_total = 0.0
        num_notas = 0

        for folio, nota in dic_principal.items():
            fecha_nota = dt.datetime.strptime(nota[0], "%d/%m/%Y")
            if fecha_inicial <= fecha_nota <= fecha_final:
                monto_total += nota[5]
                num_notas += 1

        if num_notas > 0:
            promedio = monto_total / num_notas
            print(f"\nEl promedio de los montos de las notas en el período seleccionado es: {promedio:.2f}")
        else:
            print("No se encontraron notas en el período seleccionado.")

# Función para consultas y reportes
def consultas_reportes():
    while True:
        print('COMO DESEAS CONSULTAR EN LA BASE DE DATOS:')
        print('[1] POR PERIODO')
        print('[2] POR FOLIO')
        print('[3] POR CLIENTE')
        print('[4] CÁLCULO DE PROMEDIO DE MONTOS EN UN PERÍODO')
        try:
            opcion = input('SELECCIONA: ')
            if (opcion.strip() == ""):
                print('No se debe omitir el dato')
                continue
            if not(bool(re.match("^[1-4]{1}$", opcion))):
                print('No cumple con el patrón')
                continue
            opcion = int(opcion)
            if opcion == 1:
                consultar_periodo()
            elif opcion == 2:
                consultar_folio()
            elif opcion == 3:
                consultar_cliente()
            elif opcion == 4:
                calcular_promedio_montos()
        except ValueError:
            print('Debes ingresar un dato entero')
        break