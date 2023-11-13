import re
import sys
import datetime as dt
import sqlite3
import pandas as pd
from sqlite3 import Error

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

#TABLAS Y BASE DE DATOS
while True:
    try:
        with sqlite3.connect("TALLER_PIA.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS clientes \
                            (clave_cliente INTEGER PRIMARY KEY, \
                            nombre TEXT NOT NULL, \
                            rfc TEXT NOT NULL, \
                            correo TEXT NOT NULL, \
                            cliente_activo INTEGER NOT NULL);")
            
            cursor.execute("CREATE TABLE IF NOT EXISTS servicios \
                            (clave_servicio INTEGER PRIMARY KEY, \
                            nombre_servicio TEXT NOT NULL, \
                            costo_servicio REAL NOT NULL, \
                            servicio_activo INTEGER NOT NULL);")
            
            cursor.execute("CREATE TABLE IF NOT EXISTS notas \
                            (folio INTEGER PRIMARY KEY, \
                            fecha TIMESTAMP NOT NULL, \
                            clave_cliente INTEGER NOT NULL, \
                            FOREIGN KEY (clave_cliente) REFERENCES clientes(clave_cliente));")
       
            cursor.execute("CREATE TABLE detalles( \
                            folio_notas INTEGER, \
                            clave_servicio INTEGER, \
                            FOREIGN KEY (Folio) REFERENCES Notas(Folio), \
                            FOREIGN KEY (clave_servicio) REFERENCES Servicios(clave_servicio) \);")
        break
    except sqlite3.Error as e:
        print(e)
        continue
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        continue
    finally:
        conn.close()

#SERVICIOS
def AGREGAR_SERVICIOS():
    print()
    while True:
        servicio = input("INGRESE EL SERVICIO A REALIZAR: ").lower()
        if not servicio.strip():
            print("Este campo no puede estar vacío")
        elif not servicio.isalpha():
            print("Debes ingresar el nombre del servicio NO su costo")
        else:
            break

    while True:
        try:
            costo_servicio = input('INGRESA EL COSTO DEL SERVICIO\n')
            if (costo_servicio.strip() == ""):
                print('NO SE DEBE OMITIR EL DATO')
                print()
                continue
            if not(bool(re.match("^[0-9]+|[0-9]+.[0-9]$", costo_servicio))):
                print('SOLO SE ACEPTAN ENTEROS O NUMEROS REALES\n')
                print()
                continue
            costo_servicio = float(costo_servicio)
            if (costo_servicio < 0):
                print('EL COSTO DEBE SER MAYOR A CERO')
                print()
                continue
            break
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            print()
            continue
        
    try:
        with sqlite3.connect("TALLER_PIA.db") as conn:
            mi_cursor = conn.cursor()
            datos_servicio = {"nombre_servicio":servicio, "costo_servicio":costo_servicio, "servicio_activo": 1}
            mi_cursor.execute("INSERT INTO servicios (nombre_servicio, costo_servicio, servicio_activo) VALUES(:nombre_servicio,:costo_servicio,:servicio_activo)", datos_servicio)
    except Error as e:
        print (e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

#*************************************************************************************************************#
def BUSCAR_POR_CLAVE_SERVICIO():
    print()
    while True:
        try:
            opcion = int(input('INGRESA LA CLAVE DEL SERVICIO:\n'))
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
                consulta = "SELECT * FROM servicios"
                servicio_df = pd.read_sql(consulta, conn)
                servicio_especifico = servicio_df.loc[servicio_df["clave_servicio"] == opcion]
            if not any(servicio_df["clave_servicio"] == opcion):
                print("EL CLIENTE NO SE HA PODIDO ENCONTRAR")
                print()
                break
            else:
                print(servicio_especifico)
                print()
                break
        except Error as e:
            print(e)
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}\n")
            continue
        
def ORDENAR_SERVICIOS_CLAVE():
    print()
    while True:
        try:
            with sqlite3.connect("TALLER_PIA.db") as conn:
                consulta = "SELECT * FROM servicios \
                    ORDER BY clave_servicio ASC"
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
            opcion = input('[1] EXPORTAR ARCHIVO A CSV\n[2] EXPORTAR ARCHIVO A EXCEL\n[3] REGRESAR AL MENU DE SERVICIOS\n')
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

def BUSCAR_POR_NOMBRE_SERVICIO():
    print()
    while True:
        try:
            opcion = input('INGRESA EL NOMBRE DEL SERVICIO:\n')
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
                consulta = "SELECT * FROM servicios"
                clientes_df = pd.read_sql(consulta, conn)
                cliente_nombre = clientes_df.loc[clientes_df["nombre_servicio"] == opcion]                
                if cliente_nombre.empty:
                    print("EL SERVICIO NO EXISTE O NO SE ENCONTRO")
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

def ORDENAR_SERVICIOS_NOMBRE():
    print()
    while True:
        try:
            with sqlite3.connect("TALLER_PIA.db") as conn:
                consulta = "SELECT * FROM servicios \
                    ORDER BY nombre_servicio ASC"
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
            opcion = input('EXPORTAR ARCHIVO A CSV [1]\nEXPORTAR ARCHIVO A EXCEL [2]\nREGRESAR A MENU DE SERVICIOS [3]\n')
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
    opcion = int(opcion)
    if (opcion == 1):
        return clientes_df.to_csv(f"{nombre_csv}", header = True , index = True)
    elif (opcion == 2):
        return clientes_df.to_excel(nombre_excel, index=False)
    elif (opcion == 3):
        print('REGRESANDO....')
        return

def LISTADO_CONSULTAS_SERVICIOS():
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
                ORDENAR_SERVICIOS_CLAVE()
            elif (opcion == 2):
                ORDENAR_SERVICIOS_NOMBRE()
            elif (opcion == 3):
                print('REGRESANDO....')
                return


#*************************************************************************************************************#

def CONSULTAS_REPORTES_SERVICIOS():
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

def MENU_SERVICIOS_PRINCIPAL():
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
            opcion = int(opcion)
            if (opcion == 1):
                NUEVO_CLIENTE()
            elif (opcion == 2):
                CONSULTAS_REPORTES_SERVICIOS()
            elif (opcion == 3):
                return

#*************************************************************************************************************#

#CLIENTES(EDGAR)
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
            datos_cliente = {"nombre":nombre_cliente, "rfc":rfc_cliente, "correo": correo_cliente, "cliente_activo": 1}
            mi_cursor.execute("INSERT INTO clientes (nombre, rfc, correo, cliente_activo) VALUES(:nombre,:rfc,:correo,:cliente_activo)", datos_cliente)
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
            opcion = input('INGRESA EL NOMBRE DEL CLIENTE:\n')
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
    opcion = int(opcion)
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
            opcion = int(opcion)
            if (opcion == 1):
                NUEVO_CLIENTE()
            elif (opcion == 2):
                CONSULTAS_REPORTES()
            elif (opcion == 3):
                return

#NOTAS
fecha_actual = dt.datetime.now()
fecha_maxima = fecha_actual.strftime("%d/%m/%Y")
fecha_hoy = dt.datetime.strptime(fecha_maxima, "%d/%m/%Y")


def registrar_nota():
    print("REGISTRO DE NOTA")
    print()
    while True:
        print(f"Fecha actual: {fecha_maxima}")
        fecha_nota = input("FECHA DE LA NOTA\nDEBERA CUMPLIR EL SIGUIENTE FORMATO: DD/MM/AAAA\n")
        if fecha_nota.strip() == "":
            print('NO SE DEBE OMITIR EL DATO\n')
            continue
        try:
            fecha_nota = dt.datetime.strptime(fecha_nota, "%d/%m/%Y")
            if fecha_nota > fecha_actual:
                print("\nLA FECHA DE LA NOTA DEBE SER MENOR O IGUAL A LA FECHA DE HOY\n")
                continue
        except Exception:
            print("\nFORMATO DE FECHA INCORRECTO. INTENTA LO SIGUIENTE\nDD/MM/AAAA.\n")
            continue
        break

    while True:
        cliente_clave = input("ESCRIBE LA CLAVE DEL CLIENTE:\n")
        if cliente_clave.strip() == "":
            print("NO SE DEBE OMITIR EL DATO\n")
            continue
        if (cliente_clave.isalpha()):
            print('SOLO SE ACEPTAN NUMEROS PARA LA CLAVE\n')
            continue  
        break
    
    while True:
        servicio_clave = input("ESCRIBE LA CLAVE DEL CLIENTE:\n")
        if servicio_clave.strip() == "":
            print("NO SE DEBE OMITIR EL DATO\n")
            continue
        if not(bool((servicio_clave.isalpha()))):
            print('SOLO SE ACEPTAN NUMEROS PARA LA CLAVE\n')
            continue  
        break

def consultar_periodo():
    while True:
        try:
            fecha_inicio = input("\nINGRESE LA FECHA INICIAL: DD/MM/AAAA\n")
            if fecha_inicio.strip() == "":
                fecha_inicio = "01/01/2000"
            fecha_inicio = dt.datetime.strptime(fecha_inicio, "%d/%m/%Y")
        except ValueError:
            print("\nFormato de fecha incorrecto, ingrese la fecha en el formato DD/MM/AAAA\n")

        while True:
            try:
                fecha_final = input("INGRESE LA FECHA FINAL: DD/MM/AAAA\n")
                if fecha_final.strip() == "":
                    fecha_final = fecha_hoy
                else:
                    fecha_final = dt.datetime.strptime(fecha_final, "%d/%m/%Y")
            except ValueError:
                print("Formato de fecha incorrecto, ingrese la fecha en el formato (DD/MM/AAAA)")
            else:
                break
        if fecha_inicio > fecha_final:
            print('\nLA FECHA INICIO DEBE SER MENOR A LA FECHA FINAL\n')
            continue
        break
    pd.to_datetime(fecha_inicio)
    pd.to_datetime(fecha_final)
         
    while True:
        try:
            with sqlite3.connect("TALLER_PIA.db") as conn:     
                consulta = "SELECT folio, fecha, clientes.nombre \
                FROM notas \
                INNER JOIN clientes ON notas.clave_cliente = clientes.clave_cliente \
                WHERE fecha >= ? AND fecha <= ?"
                notas_df = pd.read_sql(consulta, conn, params=(fecha_inicio, fecha_final))
                monto_promedio = notas_df["costo_total"].mean()

            print("Reporte de notas por período")
            print("Fecha inicial:", fecha_inicio)
            print("Fecha final:", fecha_final)
            print("Monto promedio:", monto_promedio)
            print()
            print("Folio | Fecha | Cliente")
            for nota in notas_df.itertuples():
                print(nota.folio, nota.fecha, nota.nombre)
            break
        except Error as e:
            print(e)
            continue
        except Exception:
            print(f"OCURRIO UN PROBLEMA {sys.exc_info()[0]}")
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
    opcion = int(opcion)
    if (opcion == 1):
        return notas_df.to_csv(f"{nombre_csv}", header = True , index = True)
    elif (opcion == 2):
        return notas_df.to_excel(nombre_excel, index=False)
    elif (opcion == 3):
        print('REGRESANDO....')
        return

            
def consultar_folio():
    while True:
        try:
            consultar = input("Escribe el id de la nota que buscas\n[0] SALIDA")
            if (consultar == ""):
                print('no se debe omitir el dato')
                continue
            if not(bool(re.match("^[0-9]{1,9}$", consultar))):
                print("No se ingreso un digito")
                continue
            consultar = int(consultar)
            if (consultar == 0):
                return
        except ValueError:
            print("Ingreso un valor no valido")
        else:
            break

    while True:
        with sqlite3.connect("TALLER_PIA.db") as conn:
            consulta = "SELECT folio, fecha, clientes.nombre FROM notas \
            INNER JOIN clientes ON notas.clave_cliente = clientes.clave_cliente \
            ORDER BY folio"
            notas_df = pd.read_sql(query, conn)
            nota = notas_df.loc[notas_df["folio"] == consultar]

            if nota.empty:
                print("NOTA INEXISTENTE")
            else:
                print("Folio:", nota["folio"])
                print("Fecha:", nota["fecha"])
                print("Cliente:", nota["nombre"])
                
        detalles_df = notas_df.iloc[nota.index, 2:]
        print("Detalles:")
        for detalle in detalles_df.itertuples():
            print(detalle[0], detalle[1])


def consultas_reportes():
    while True:
        print('COMO DESEAS CONSULTAR EN LA BASE DE DATOS:\n')
        print('[1] POR PERIODO\n[2] POR FOLIO\n[3] POR CLIENTE')
        try:
            opcion = input('SELECCIONA: ')
            if (opcion.strip() == ""):
                print('No se debe omitir el dato')
                continue
            if not(bool(re.match("^[1-2]{1}$", opcion))):
                print('No cumple con el patrón')
                continue
            opcion = int(opcion)
            if opcion == 1:
                consultar_periodo()
            elif opcion == 2:
                consultar_folio()
        except ValueError:
            print('Debes ingresar un dato entero')
        break

def cancelar_nota():
    print("CANCELAR UNA NOTA")
    while True:
        try:
            folio_cancelar = int(input("Ingresa el folio de la nota que deseas cancelar (0 para salir): "))
            if folio_cancelar == 0:
                return
            if folio_cancelar in dic_principal:
                nota_cancelar = dic_principal.pop(folio_cancelar)
                papelera[folio_cancelar] = nota_cancelar
                print(f"Nota con folio {folio_cancelar} cancelada exitosamente.")
                break
            else:
                print("Folio no encontrado. Intente de nuevo.")
        except ValueError:
            print("Debes ingresar un número entero válido.")

def recuperar_nota_cancelada():
    print("RECUPERAR UNA NOTA CANCELADA")
    while True:
        try:
            folio_recuperar = int(input("Ingresa el folio de la nota que deseas recuperar (0 para salir): "))
            if folio_recuperar == 0:
                return
            if folio_recuperar in papelera:
                nota_recuperar = papelera.pop(folio_recuperar)
                dic_principal[folio_recuperar] = nota_recuperar
                print(f"Nota con folio {folio_recuperar} recuperada exitosamente.")
                break
            else:
                print("Folio no encontrado en la papelera. Intente de nuevo.")
        except ValueError:
            print("Debes ingresar un número entero válido.")

def menu_principal_notas():
    while True:
        print("\nMenú Principal")
        print("1. Registrar una nota")
        print("2. Consultas y Reportes")
        print("3. Cancelar una nota")
        print("4. Recuperar una nota cancelada")
        print("5. Salir\n")

        try:
            opcion = input("Ingresa el número de la opción que deseas seleccionar: ")
            if opcion.strip() == "":
                print('No se debe omitir el dato')
                continue
            opcion = int(opcion)
        except ValueError:
            print("Debes ingresar un número entero.")
        else:
            if opcion == 1:
                registrar_nota()
            elif opcion == 2:
                consultas_reportes()
            elif opcion == 3:
                cancelar_nota()
            elif opcion == 4:
                recuperar_nota_cancelada()
            elif opcion == 5:
                guardar_dic_principal(dic_principal)
                return
            else:
                print("Opción no válida. Por favor, elige una opción del 1 al 5.")
#ESTADISTICOS(TODOS)
import sqlite3

def clientes_con_mas_notas(conexion, cantidad_clientes, fecha_inicial, fecha_final):
    # Consulta SQL para obtener los clientes con más notas
    query = """
        SELECT cliente.nombre, COUNT(*) as cantidad
        FROM notas
        INNER JOIN clientes ON notas.clave_cliente = clientes.clave_cliente
        WHERE notas.fecha BETWEEN ? AND ?
        GROUP BY cliente.nombre
        ORDER BY cantidad DESC
        LIMIT ?
    """

    # Obtener los resultados de la consulta
    cursor = conexion.cursor()
    cursor.execute(query, (fecha_inicial, fecha_final, cantidad_clientes))
    resultados = cursor.fetchall()

    # Imprimir el informe
    print("\nClientes con más notas en el período:")
    print("Nombre\t\tCantidad")

    for cliente, cantidad in resultados:
        print(f"{cliente}\t\t{cantidad}")

    # Ofrecer la opción de exportar el informe
    exportar_opcion = input("\n¿Desea exportar el informe a CSV o Excel? (CSV/Excel): ")

    # Exportar el informe si el usuario lo indica
    if exportar_opcion.lower() in ("csv", "excel"):
        nombre_archivo = f"ReporteClientesConMasNotas_{fecha_inicial}_{fecha_final}.{exportar_opcion}"
        exportar_informe(resultados, nombre_archivo)

def exportar_informe(resultados, nombre_archivo):
    # Exportar el informe a CSV
    if nombre_archivo.lower() == "csv":
        with open(nombre_archivo, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Nombre", "Cantidad"])
            csv_writer.writerows(resultados)

    # Exportar el informe a Excel
    elif nombre_archivo.lower() == "excel":
        import xlsxwriter

        # Crear un libro de Excel
        libro = xlsxwriter.Workbook(nombre_archivo)
        hoja = libro.add_worksheet()

        # Agregar los encabezados a la hoja
        hoja.write("A1", "Nombre")
        hoja.write("B1", "Cantidad")

        # Agregar los datos a la hoja
        for cliente, cantidad in resultados:
            hoja.write(hoja.get_row_count(), 0, cliente)
            hoja.write(hoja.get_row_count(), 1, cantidad)

        # Guardar el libro de Excel
        libro.close()
import sqlite3

def promedio_monto_notas(conexion, fecha_inicial, fecha_final):
    # Consulta SQL para obtener el monto total de las notas
    query = """
        SELECT SUM(costo_servicio) as monto_total
        FROM detalles
        INNER JOIN notas ON detalles.folio_notas = notas.folio
        WHERE notas.fecha BETWEEN ? AND ?
    """

    # Obtener los resultados de la consulta
    cursor = conexion.cursor()
    cursor.execute(query, (fecha_inicial, fecha_final))
    monto_total = cursor.fetchone()[0]

    # Consulta SQL para obtener la cantidad de notas
    query = """
        SELECT COUNT(*) as cantidad_notas
        FROM notas
        WHERE notas.fecha BETWEEN ? AND ?
    """

    # Obtener los resultados de la consulta
    cursor.execute(query, (fecha_inicial, fecha_final))
    cantidad_notas = cursor.fetchone()[0]

    # Calcular el promedio
    promedio = monto_total / cantidad_notas

    # Imprimir el informe
    print(f"El promedio de los montos de las notas en el período {fecha_inicial} - {fecha_final} es: {promedio}")

if __name__ == "__main__":
    # Conectarse a la base de datos
    conexion = sqlite3.connect("mi_base_de_datos.db")

    # Solicitar los parámetros al usuario
    fecha_inicial = input("Ingrese la fecha inicial del período a reportar (mm_dd_aaaa): ")
    fecha_final = input("Ingrese la fecha final del período a reportar (mm_dd_aaaa): ")

    # Llamar a la función para generar el informe
    promedio_monto_notas(conexion, fecha_inicial, fecha_final)

    # Cerrar la conexión a la base de datos
    conexion.close()
def cantidad_servicios_mas_prestados(conexion, tabla_servicios, tabla_detalles, cantidad_servicios):
    fecha_inicial = input("Ingrese la fecha inicial del período a reportar (mm_dd_aaaa): ")
    fecha_final = input("Ingrese la fecha final del período a reportar (mm_dd_aaaa): ")

    query = '''
        SELECT Servicio, COUNT(*) as cantidad
        FROM `tabla_servicios`
        WHERE fecha_atencion BETWEEN ? AND ?
        GROUP BY nombre
        ORDER BY cantidad DESC
        LIMIT ?
    '''

    cursor = conexion.cursor()
    cursor.execute(query, (fecha_inicial, fecha_final, cantidad_servicios))
    resultados = cursor.fetchall()

    print("\nServicios más solicitados en el período:")
    print("Nombre del Servicio\tCantidad")

    for servicio, cantidad in resultados:
        print(f"{servicio}\t\t\t{cantidad}")

    exportar_opcion = input("\n¿Desea exportar el informe a CSV? (Sí/No): ")

    if exportar_opcion.lower() == "sí":
        nombre_archivo = f"ReporteServiciosMasPrestados_{fecha_inicial}_{fecha_final}.csv"
        with open(nombre_archivo, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Nombre del Servicio", "Cantidad"])
            csv_writer.writerows(resultados)

        print(f"El informe ha sido exportado como '{nombre_archivo}'.")

    cursor.close()

if __name__ == "__main__":
    import mysql.connector

    # Conectarse a la base de datos
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mi_base_de_datos"
    )

    # Asignar los nombres de las tablas
    tabla_servicios = "servicios"
    tabla_detalles = "detalles"

    # Llamar a la función
    cantidad_servicios_mas_prestados(conexion, tabla_servicios, tabla_detalles, 10)


def menu():
    # Conectarse a la base de datos
    conexion = sqlite3.connect("mi_base_de_datos.db")

    while True:
        print("Menú principal")
        print("1. Clientes con más notas")
        print("2. Salir")

        opcion = input("Ingrese su opción: ")

        if opcion == "1":
            # Solicitar los parámetros al usuario
            cantidad_clientes = int(input("Ingrese la cantidad de clientes con más notas a identificar: "))
            while cantidad_clientes < 1:
                cantidad_clientes = int(input("Por favor, ingrese un valor igual o mayor a 1: "))

            fecha_inicial = input("Ingrese la fecha inicial del período a reportar (mm_dd_aaaa): ")
            fecha_final = input("Ingrese la fecha final del período a reportar (mm_dd_aaaa): ")

            # Llamar a la función para generar el informe
            clientes_con_mas_notas(conexion, cantidad_clientes, fecha_inicial, fecha_final)

        elif opcion == "2":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")

    # Cerrar la conexión a la base de datos
    conexion.close()


import sqlite3

def menu_estadistica():
    # Conectarse a la base de datos
    conexion = sqlite3.connect("mi_base_de_datos.db")

    while True:
        print("Menú principal")
        print("1. Clientes con más notas")
        print("2. Servicios más solicitados")
        print("3. Promedio de los montos de las notas")
        print("4. Salir")

        opcion = input("Ingrese su opción: ")

        if opcion == "1":
            # Solicitar los parámetros al usuario
            cantidad_clientes = int(input("Ingrese la cantidad de clientes con más notas a identificar: "))
            while cantidad_clientes < 1:
                cantidad_clientes = int(input("Por favor, ingrese un valor igual o mayor a 1: "))

            fecha_inicial = input("Ingrese la fecha inicial del período a reportar (mm_dd_aaaa): ")
            fecha_final = input("Ingrese la fecha final del período a reportar (mm_dd_aaaa): ")

            # Llamar a la función para generar el informe
            clientes_con_mas_notas(conexion, cantidad_clientes, fecha_inicial, fecha_final)

        elif opcion == "2":
            # Solicitar los parámetros al usuario
            cantidad_servicios = int(input("Ingrese la cantidad de servicios más solicitados a identificar: "))
            while cantidad_servicios < 1:
                cantidad_servicios = int(input("Por favor, ingrese un valor igual o mayor a 1: "))

            fecha_inicial = input("Ingrese la fecha inicial del período a reportar (mm_dd_aaaa): ")
            fecha_final = input("Ingrese la fecha final del período a reportar (mm_dd_aaaa): ")

            # Llamar a la función para generar el informe
            cantidad_servicios_mas_prestados(conexion, cantidad_servicios, fecha_inicial, fecha_final)

        elif opcion == "3":
            # Solicitar los parámetros al usuario
            fecha_inicial = input("Ingrese la fecha inicial del período a reportar (mm_dd_aaaa): ")
            fecha_final = input("Ingrese la fecha final del período a reportar (mm_dd_aaaa): ")

            # Llamar a la función para generar el informe
            promedio_monto_notas(conexion, fecha_inicial, fecha_final)

        elif opcion == "4":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")

    # Cerrar la conexión a la base de datos
    conexion.close()
