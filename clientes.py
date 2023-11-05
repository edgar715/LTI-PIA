"""
2.2. Menú Clientes

2.2.1. Agregar un cliente: En esta opción se podrán dar de alta nuevos clientes con su detalle, del cual no se puede omitir ningún dato: 
La clave (Deberá ser única y generada automáticamente), 
El nombre completo del cliente (No puede quedar vacío ni conformado únicamente por espacios en blanco), 
el RFC del cliente cumpliendo con el formato válido para ese dato (puede consultarlo en el documento que se descarga mediante el siguiente 
recurso: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwj0s-Dy86yBAxXwL0QIHcw1C60QFnoECEEQAQ&url=https%3A%2F%2Fwww.sat.gob.mx%2Fcs%2FSatellite%3Fblobcol%3Durldata%26blobkey%3Did%26blobtable%3DMungoBlobs%26blobwhere%3D1461175045755%26ssbinary%3Dtrue&usg=AOvVaw2fUKrURceighjcMUGiXZYQ&opi=89978449) 
y el correo electrónico validando también su formato correspondiente)

"""
import re
import pandas as pd
import sys
import datetime as dt
import openpyxl

clave = 1
cliente_list = []
cliente_dic = {}
fecha_hoy_cliente = dt.date.today()
fecha_hoy_cliente = fecha_hoy_cliente.strftime('%m_%d_%Y')
nombre_csv = f"ReporteClientesActivosPorClave_{fecha_hoy_cliente}.csv"
nombre_excel = f"ReporteClientesActivosPorClave_{fecha_hoy_cliente}.xlsx"

RFC_TEXT = """
1: LETRA INICIAL DEL APELLIDO PATERNO
2: PRIMER VOCAL DEL APELLIDO PATERNO
3: LETRA INICIAL DEL APELLIDO MATERNO
4: PRIMER VOCAL DEL APELLIDO MATERNO
5: LOS ULTIMOS 2 DIGITOS DEL AÑO
6: LOS 2 DIGITOS DEL MES Y DIA
7: LOS 3 CARACTERES 
"""

def NUEVO_CLIENTE():
    global clave
    while True:
        nombre_cliente = input('INGRESA EL NOMBRE DEL CLIENTE:\n')
        if (nombre_cliente.strip() == ""):
            print('NO SE DEBE OMITIR EL DATO\n')
            continue
        if not(bool(nombre_cliente.isalpha())):
            print('SOLO ACEPTA LETRAS DEL ALFABETO Y NO ADMITE ESPACIOS EN BLANCO\n')
            continue
        else:  
            break

    while True:
        rfc_cliente = input(f'EL RFC DEBE CONTENER LO SIGUIENTE:\n{RFC_TEXT}\nINGRESA EL RFC DEL CLIENTE:\n')
        if (rfc_cliente.strip() == ""):
            print('NO SE DEBE OMITIR EL DATO\n')
            continue
        elif not(bool(re.match("^[A-Za-z]{4}[0-9]{6}[a-zA-Z0-9]{3}$", rfc_cliente))):
            print('SOLO ACEPTA LO SIGUIENTE:\n1: 4 LETRAS\n2:6 NUMEROS\n3: 3 CARACTERES YA SEAN NUMEROS O LETRAS\n')
            continue
        else:
            break
        
    while True:
        correo_cliente = input('INGRESA EL CORREO DEL CLIENTE:\n')
        if (correo_cliente.strip() == ""):
            print("NO SE DEBE OMITIR EL DATO\n")
            continue
        elif not(bool(re.match("^[A-Za-z0-9]+@[A-Za-z]+.[A-Za-z]+$",correo_cliente))):
            print('EL CORREO SOLO ACEPTA CARACTERES COMO NUMEROS Y LETRAS\n')
            continue
        else:
            break
        
    cliente_list = [clave, nombre_cliente, rfc_cliente, correo_cliente]
    cliente_dic[clave] = cliente_list
    print(cliente_dic)
    clave += 1

""""
2.2.2. Consultas y reportes de clientes
        try
        except Exception:
        print(f"Ocurrió un problema {sys.exc_info()[0]}")
2.2.2.1. Listado de clientes registrados: Se presentará un submenú que ofrecerá las siguientes opciones.

2.2.2.1.1. Ordenado por clave: Se presentará un reporte de todos los clientes activos ordenado por la clave asignada para cada uno. 
Después de desplegar el reporte en pantalla se le debe ofrecer la opción al usuario de exportar este resultado a CSV, Excel o 
regresar al menú de reportes. Si el usuario indica que desea exportar el reporte a cualquiera de los formatos ofrecidos este se debe guardar 
con un nombre de archivo conformado por el siguiente 
patrón ReporteClientesActivosPorClave_FechaDelReporte donde: *FechaDelReporte = La fecha en que se está emitiendo el reporte, 
en formato mm_dd_aaaa
"""
def BUSCAR_POR_CLAVE():
    print()
    print()
    while True:
        try:
            opcion = int(input('INGRESA LA CLAVE DEL CLIENTE:\n'))
            break
        except ValueError:
            print('SE DEBE INGRESAR DIGITOS ENTEROS\n')
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
    
    for clave, clientes_valores in cliente_dic.items():
        if opcion in clientes_valores:
            print(f"CLAVE: {clave}\nNOMBE: {clientes_valores[1]}\nRFC: {clientes_valores[2]}\nCORREO ELECTRONICO: {clientes_valores[3]}")
            break
        else:
            print('NO EXISTE EL CLIENTE')
            break
    
    
    
def ORDENAR_CLIENTES_CLAVE():
    print()
    indices_clientes = ['-'] * len(cliente_dic)
    serv_pd = pd.DataFrame(cliente_dic.values(), columns=["CLAVE","NOMBRE", "RFC", "CORREO"])
    serv_pd.index = [indices_clientes]
    clientes_df = serv_pd
    print(clientes_df)
    while True:
        try:
            opcion = int(input('EXPORTAR ARCHIVO A CSV [1]\nEXPORTAR ARCHIVO A EXCEL [2]\nREGRESAR A MENU [3]\n'))
            if not(bool(re.match("[1-3]{1}", opcion))):
                print('NO CUMPLE CON EL PATRON\n')
                continue
            break
        except ValueError:
            print('SE DEBE INGRESAR DIGITOS ENTEROS\n')
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
    if (opcion == 1):
        return clientes_df.to_csv(f"{nombre_csv}", header = True , index = True)
    elif (opcion == 2):
        return clientes_df.to_excel(nombre_excel, index=False)
    elif (opcion == 3):
        return
      
        
"""
2.2.2.1.2. Ordenado por nombre: Se presentará un reporte de todos los clientes activos ordenado por el nombre de estos. Después de desplegar
el reporte en pantalla se le debe ofrecer la opción al usuario de exportar este resultado a CSV, Excel o regresar al menú de reportes. 
Si el usuario indica que desea

exportar el reporte a cualquiera de los formatos ofrecidos este se debe guardar con un nombre de archivo conformado por el 
siguiente patrón ReporteClientesActivosPorNombre_FechaDelReporte donde: *FechaDelReporte = La fecha en que se está emitiendo el reporte, 
en formato mm_dd_aaaa
"""
def BUSCAR_POR_NOMBRE():
    print()
    while True:
        try:
            opcion = input('INGRESA LA CLAVE DEL CLIENTE:\n')
            if (opcion.strip() == ""):
                print('NO SE DEBE OMITIR EL DATO\n')
                continue
            if not(bool(opcion.isalpha())):
                print('SOLO ACEPTA LETRAS DEL ALFABETO\n')
                continue                         
            break
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
    
    for clave, clientes_valores in cliente_dic.items():
        if opcion in clientes_valores:
            print(f"CLAVE: {clave}\nNOMBE: {clientes_valores[1]}\nRFC: {clientes_valores[2]}\nCORREO ELECTRONICO: {clientes_valores[3]}\n")
            break
        else:
            print('NO EXISTE EL CLIENTE')
            break

def ORDENAR_CLIENTES_NOMBRE():
    indices_clientes = ['-'] * len(cliente_dic)
    serv_pd = pd.DataFrame(cliente_dic.values(), columns=["CLAVE","NOMBRE", "RFC", "CORREO"])
    serv_pd.index = [indices_clientes]
    clientes_df = serv_pd
    clientes_df = clientes_df.sort_values(by="NOMBRE")
    print(clientes_df)
    print()
    while True:
        try:
            opcion = int(input('EXPORTAR ARCHIVO A CSV [1]\nEXPORTAR ARCHIVO A EXCEL [2]\nREGRESAR A MENU [3]\n'))
            if not(bool(re.match("[1-3]{1}", opcion))):
                print('NO CUMPLE CON EL PATRON\n')
                continue
            break
        except ValueError:
            print('SE DEBE INGRESAR DIGITOS ENTEROS\n')
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}")
            continue
    if (opcion == 1):
        return clientes_df.to_csv(f"{nombre_csv}", header = True , index = True)
    elif (opcion == 2):
        return clientes_df.to_excel(nombre_excel, index=False)
    elif (opcion == 3):
        return
      

"""
2.2.2.1.3. Volver al menú anterior: Regresará al menú de consultas y reportes de los clientes

2.2.3. Volver al menú principal: Volverá al menú principal

"""
def CONSULTAS_REPORTES():
    print()
    while True:
        try:
            opcion = int(input('LISTADO DE CLIENTES\nBUCAR POR LA CLAVE [1]\nBUSCAR POR EL NOMBRE [2]\nLISTADO DE SERVICIOS[3]\nVOLVER AL MENU DE CONSULTAS Y REPORTES [4]\n'))
            if not(bool(re.match("[1-4]{1}", opcion))):
                print('NO CUMPLE CON EL PATRON\n')
                continue
        except ValueError:
            print('SE DEBE INGRESAR DIGITOS ENTEROS\n')
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
        else:
            if (opcion == 1):
                BUSCAR_POR_CLAVE()
            elif (opcion == 2):
                BUSCAR_POR_NOMBRE()
            elif (opcion == 3):
                LISTADO_SERVICIOS()
            elif (opcion == 4):
                return

def LISTADO_SERVICIOS():
    print()
    while True:
        try:
            opcion = int(input('LISTADO DE CLIENTES\nORDENADOS POR LA CLAVE [1]\nORDENADOS POR EL NOMBRE [2]\nVOLVER AL MENU DE CONSULTAS Y REPORTES [3]\n'))
            if not(bool(re.match("[1-3]{1}", opcion))):
                print('NO CUMPLE CON EL PATRON\n')
                continue        
        except ValueError:
            print('SE DEBE INGRESAR DIGITOS ENTEROS\n')
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
        else:
            if (opcion == 1):
                ORDENAR_CLIENTES_CLAVE()
            elif (opcion == 2):
                ORDENAR_CLIENTES_NOMBRE()
            elif (opcion == 3):
                return
    
def MENU_CLIENTES_PRINCIPAL():
    while True:
        try:
            opcion = int(input('MENU DE CLIENTES\nREGISTRAR UN NUEVO CLIENTE [1]\nCONSULTAS Y REPORTES [2]\nVOLVER AL MENU PRINCIPAL [3]\n'))
            if not(bool(re.match("[1-3]{1}", opcion))):
                print('NO CUMPLE CON EL PATRON\n')
                continue
        except ValueError:
            print('SE DEBE INGRESAR DIGITOS ENTEROS\n')
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
        else:
            if (opcion == 1):
                NUEVO_CLIENTE()
            elif (opcion == 2):
                CONSULTAS_REPORTES()
            elif (opcion == 3):
                return

MENU_CLIENTES_PRINCIPAL()