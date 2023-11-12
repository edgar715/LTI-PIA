import re
import sys
import sqlite3
import pandas as pd
from sqlite3 import Error

#TABLAS Y BASE DE DATOS
try:
    with sqlite3.connect("TALLER_PIA.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS clientes \
        (clave_cliente INTEGER PRIMARY KEY, nombre TEXT NOT NULL, rfc TEXT NOT NULL, correo TEXT NOT NULL);")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS notas \
                        folio INTEGER PRIMARY KEY, \
                        fecha TIMESTAMP, \
                        clave_cliente INTEGER, \
                        monto_pagar REAL, \
                        FOREIGN KEY (clientes) REFERENCES clientes(clave_cliente) ")
        
except Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")


#CREAR NOTAS (PARTE DE CHOCO)
#CONSULTAS Y REPORTES DE LAS NOTAS (DIEGO)
#SUSPENDER UNA NOTA (JONA)
#RECUPERAR UNA NOTA(EDGAR)

#SERVICIOS(JONA Y DIEGO)

#CLIENTES(EDGAR)
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

    try:
        with sqlite3.connect("TALLER_PIA.db") as conn:
            mi_cursor = conn.cursor()
            datos_cliente = {"nombre":nombre_cliente, "rfc":rfc_cliente, "correo": correo_cliente}
            mi_cursor.execute("INSERT INTO clientes VALUES(:nombre,:rfc,:correo)", datos_cliente)
    except Error as e:
        print (e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()
        
#*************************************************************************************************************#

def BUSCAR_POR_CLAVE():
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
    
    while True:
        try:
            with sqlite3.connect("TALLER_PIA.db") as conn:
                consulta = "SELECT * FROM clientes"
                clientes_df = pd.read_sql(consulta, conn)
                cliente_especifico = clientes_df.loc[clientes_df["clave_cliente"] == opcion]
            if not any(clientes_df["clave_cliente"] == opcion):
                print("EL CLIENTE NO SE HA PODIDO ENCONTRAR")
                print()
                break
            else:
                print(cliente_especifico)
                print()
                break
        except Error as e:
            print(e)
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
        
def ORDENAR_CLIENTES_CLAVE():
    print()
    while True:
        try:
            with sqlite3.connect("TALLER_PIA.db") as conn:
                consulta = "SELECT * FROM clientes \
                    ORDER BY clave_cliente ASC"
                clientes_df = pd.read_sql(consulta, conn)
                break
        except Error as e:
            print(e)
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
    
    while True:
        try:
            opcion = input('[1] EXPORTAR ARCHIVO A CSV\n[2] EXPORTAR ARCHIVO A EXCEL\n[3] REGRESAR AL MENU DE CLIENTES\n')
            if (opcion.strip() == ""):
                print("NO SE DEBE OMITIR EL DATO")
                continue
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
        
    opcion = int(opcion)
    if (opcion == 1):
        return clientes_df.to_csv(f"{nombre_csv}", header = True , index = True)
    elif (opcion == 2):
        return clientes_df.to_excel(nombre_excel, index=False)
    elif (opcion == 3):
        return
    
#*************************************************************************************************************#

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

    while True:
        try:
            with sqlite3.connect("TALLER_PIA.db") as conn:
                consulta = "SELECT * FROM clientes"
                clientes_df = pd.read_sql(consulta, conn)
                cliente_nombre = clientes_df.loc[clientes_df["nombre"] == opcion]                
                if cliente_nombre.empty:
                    print("EL CLIENTE NO EXISTE O NO SE ENCONTRO")
                    print()
                    break
                else:
                    print(cliente_nombre)
                    print()
                    break
        except Error as e:
            print(e)
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue

    

def ORDENAR_CLIENTES_NOMBRE():
    print()
    while True:
        try:
            with sqlite3.connect("TALLER_PIA.db") as conn:
                consulta = "SELECT * FROM clientes \
                    ORDER BY nombre ASC"
                clientes_df = pd.read_sql(consulta, conn)
                break
        except Error as e:
            print(e)
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
        
    while True:
        try:
            opcion = input('EXPORTAR ARCHIVO A CSV [1]\nEXPORTAR ARCHIVO A EXCEL [2]\nREGRESAR A MENU DE CLIENTES [3]\n')
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
        print('REGRESANDO....')
        return

def LISTADO_SERVICIOS():
    print()
    while True:
        try:
            opcion = input('LISTADO DE CLIENTES\nORDENADOS POR LA CLAVE [1]\nORDENADOS POR EL NOMBRE [2]\nVOLVER AL MENU DE CONSULTAS Y REPORTES [3]\n')
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
            opcion = int(opcion)
            if (opcion == 1):
                ORDENAR_CLIENTES_CLAVE()
            elif (opcion == 2):
                ORDENAR_CLIENTES_NOMBRE()
            elif (opcion == 3):
                print('REGRESANDO....')
                return

#*************************************************************************************************************#

def CONSULTAS_REPORTES():
    print()
    while True:
        try:
            opcion = input('LISTADO DE CLIENTES\nBUCAR POR LA CLAVE [1]\nBUSCAR POR EL NOMBRE [2]\nLISTADO DE SERVICIOS[3]\nVOLVER AL MENU DE CONSULTAS Y REPORTES [4]\n')
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
            opcion = int(opcion)
            if (opcion == 1):
                BUSCAR_POR_CLAVE()
            elif (opcion == 2):
                BUSCAR_POR_NOMBRE()
            elif (opcion == 3):
                LISTADO_SERVICIOS()
            elif (opcion == 4):
                return

def MENU_CLIENTES_PRINCIPAL():
    while True:
        try:
            opcion = input('MENU DE CLIENTES\nREGISTRAR UN NUEVO CLIENTE [1]\nCONSULTAS Y REPORTES [2]\nVOLVER AL MENU PRINCIPAL [3]\n')
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
    
#ESTADISTICOS(TODOS)