import re
import sys
import datamine
import sqlite3
import os
import pandas as pd
from sqlite3 import Error
from datetime import datetime

#TABLAS Y BASE DE DATOS
def create_connection(database_file):
    try:
        print("Current working directory:", os.getcwd())

        conn = sqlite3.connect(database_file)
        print("Connection to the database successful.")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

database_file = 'TALLER_PIA.db'
connection = create_connection(database_file)


def create_tables(conn):
    try:

        with conn:
            cursor = conn.cursor()
            
            cursor.execute("CREATE TABLE IF NOT EXISTS clientes \
                (clave_cliente INTEGER PRIMARY KEY, nombre TEXT NOT NULL, rfc TEXT NOT NULL, correo TEXT NOT NULL);")
            
            cursor.execute("CREATE TABLE IF NOT EXISTS notas \
                            (folio INTEGER PRIMARY KEY, \
                            fecha TIMESTAMP, \
                            clave_cliente INTEGER, \
                            monto_pagar REAL, \
                            FOREIGN KEY (clave_cliente) REFERENCES clientes(clave_cliente));")
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    ClaveUnica INTEGER PRIMARY KEY,
                    Servicio TEXT NOT NULL,
                    Costo REAL NOT NULL,
                    Activo BOOLEAN NOT NULL
                );
            ''')
    except sqlite3.Error as e:
        print(e)

def insert_service(conn, servicio, costo, activo):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO services (Servicio, Costo, Activo)
                VALUES (?, ?, ?)
            ''', (servicio, costo, activo))
    except sqlite3.Error as e:
        print(e)

def get_all_services(conn):
    try:
        return pd.read_sql_query("SELECT * FROM services", conn)
    except sqlite3.Error as e:
        print(e)
        return pd.DataFrame()

def update_service(conn, activo, clave_unica):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE services
                SET Activo = ?
                WHERE ClaveUnica = ?
            ''', (activo, clave_unica))
    except sqlite3.Error as e:
        print(e)
    

database_file = 'TALLER_PIA.db'
connection = create_connection(database_file)
if connection is not None:
    create_table(connection)

    df = get_all_services(connection)
except Error as e:
    print (e)
except Exception:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

    

#CREAR NOTAS (PARTE DE CHOCO)
database_file = 'notas.db'
connection = create_connection(database_file)

def create_detalles_notas(conn):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detalles_notas (
                    id INTEGER PRIMARY KEY,
                    folio INTEGER,
                    clave_servicio INTEGER,
                    cantidad INTEGER,
                    FOREIGN KEY (folio) REFERENCES notas(folio),
                    FOREIGN KEY (clave_servicio) REFERENCES servicios(ClaveUnica)
                );
            ''')
    except sqlite3.Error as e:
        print(e)

def insert_cliente(conn, nombre, rfc, correo):
    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clientes (nombre, rfc, correo)
            ''', (nombre, rfc, correo))
    except sqlite3.Error as e:
        print(e)

def get_clientes(conn):
    try:
        return pd.read_sql_query("SELECT * FROM clientes", conn)
    except sqlite3.Error as e:
        print(e)
        return pd.DataFrame()

def create_note(conn, clave_cliente):
    try:
        with conn:
            cursor = conn.cursor()
            fecha_actual = datetime.now()
            monto_total = 0

            cliente = cursor.execute("SELECT nombre FROM clientes WHERE clave_cliente = ?", (clave_cliente,)).fetchone()
            if cliente is not None:
                print(f"\nCreando nota para el cliente: {cliente[0]}\n")

                print("Servicios disponibles:")
                servicios_df = get_all_services(conn)
                print(servicios_df)

                detalles = []
                while True:
                    clave_servicio = input("Ingrese la clave del servicio (o 'fin' para terminar): ")
                    if clave_servicio.lower() == 'fin':
                        break

                    servicio = servicios_df[servicios_df['ClaveUnica'] == int(clave_servicio)]
                    if not servicio.empty:
                        cantidad = int(input(f"Ingrese la cantidad de '{servicio['Servicio'].values[0]}': "))
                        monto_total += servicio['Costo'].values[0] * cantidad
                        detalles.append((clave_servicio, cantidad))
                    else:
                        print("Clave de servicio no válida. Intente nuevamente.")

                cursor.execute('''
                    INSERT INTO notas (fecha, clave_cliente, monto_pagar)
                ''', (fecha_actual, clave_cliente, monto_total))
                nota_folio = cursor.lastrowid

                for clave_servicio, cantidad in detalles:
                    cursor.execute('''
                        INSERT INTO detalles_notas (folio, clave_servicio, cantidad)
                    ''', (nota_folio, clave_servicio, cantidad))

                print("\nNota creada exitosamente.")
            else:
                print(f"\nCliente con clave {clave_cliente} no encontrado.")
    except sqlite3.Error as e:
        print(e)
        
#CONSULTAS Y REPORTES DE LAS NOTAS (DIEGO)

def consultar_por_periodo(fecha_inicial=None, fecha_final=None):
    if fecha_inicial is None:
        fecha_inicial = datetime.date(2000, 1, 1)
        print("Se asumió la fecha inicial como 01/01/2000.")

    if fecha_final is None:
        fecha_final = datetime.date.today()
        print(f"Se asumió la fecha final como {fecha_final}.")

    
    notas_en_periodo = obtener_notas_en_periodo(fecha_inicial, fecha_final)

    if notas_en_periodo:
        mostrar_reporte(notas_en_periodo)
        opcion = input("¿Desea exportar el reporte? (Sí/No): ")
        if opcion.lower() == "si":
            exportar_reporte(notas_en_periodo, fecha_inicial, fecha_final)
    else:
        print("No hay notas emitidas para el período especificado.")
#SUSPENDER UNA NOTA (JONA)
#RECUPERAR UNA NOTA(EDGAR)

#SERVICIOS(JONA Y DIEGO)

    while True:
     opcion = int(input("Elige la opción que deseas (1: Agregar registro, 2: Buscar por Clave Única, 3: Buscar por Servicio, 4: Reporte de Servicios por Clave, 5: Reporte de Servicios por Nombre, 6: Suspender un servicio, 7: Salir): "))

     if opcion == 1:
        while True:
            servicio = input("Ingrese el servicio: ").lower()
            if not servicio.strip():
                print("Este campo no puede estar vacío")
            elif not servicio.isalpha():
                print("Debes ingresar el nombre del servicio NO su costo")
            else:
                costo = input("Ingrese el costo: ")

                if not costo.isdigit():
                    print("El costo debe ser un número. Intente nuevamente.")
                    continue

                costo = float(costo)

                clave_unica = insert_service(connection, servicio, costo)
                print(f"Registro agregado con clave única: {clave_unica}")

                agregar_servicio = input("¿Desea agregar otro servicio? (Sí/No): ").lower()
                if agregar_servicio == "no":
                    break
                elif agregar_servicio != "si":
                    print("Opción no válida. Selecciona 'Sí' o 'No'.")
                    continue

     elif opcion == 2:
        clave_buscar = int(input("Ingrese la Clave Única que deseas buscar: "))
        resultado = df[df['ClaveUnica'] == clave_buscar]

        if not resultado.empty:
            print("Datos encontrados:")
            print(resultado)
        else:
            print(f"No se encontraron datos para la Clave Única {clave_buscar}.")

     elif opcion == 3:
        servicio_buscar = input("Ingrese el nombre del servicio que deseas buscar: ").lower()
        resultado = df[df['Servicio'] == servicio_buscar]

        if not resultado.empty:
            print("Datos encontrados:")
            print(resultado)
        else:
            print(f"No se encontraron datos para el servicio '{servicio_buscar}'.")

     elif opcion == 4:
        forma_exportar = input("Desea exportarlo en CSV o archivo Excel: ").strip().lower()
        if forma_exportar == "excel":
            print("Reporte de Servicios por Clave:")
            print(df.sort_values(by=['ClaveUnica']))

            exportar = input("¿Desea exportar el reporte a un archivo Excel? (Si/No): ").strip().lower()
            if exportar == 'si':
                fecha_reporte = datetime.now().strftime("%m_%d_%Y")
                nombre_archivo = f"ReporteServiciosPorClave_{fecha_reporte}.xlsx"
                df.sort_values(by=['ClaveUnica']).to_excel(nombre_archivo, index=False)
                print(f"Reporte exportado como '{nombre_archivo}'")
            elif exportar == 'no':
                pass
            else:
                print("Opción no válida. No se exportará el reporte.")
        elif forma_exportar == "csv":
            print("Reporte de Servicios por Clave:")
            print(df.sort_values(by=['ClaveUnica']))

            exportar = input("¿Desea exportar el reporte a un archivo CSV? (Si/No): ").strip().lower()
            if exportar == 'si':
                fecha_reporte = datetime.now().strftime("%m_%d_%Y")
                nombre_archivo = f"ReporteServiciosPorClave_{fecha_reporte}.csv"
                df.sort_values(by=['ClaveUnica']).to_csv(nombre_archivo, index=False)
                print(f"Reporte exportado como '{nombre_archivo}'")
            elif exportar == 'no':
                pass
            else:
                print("Opción no válida. No se exportará el reporte.")

     elif opcion == 5:
        forma_exportar = input("Desea exportarlo en CSV o archivo Excel: ").strip().lower()
        if forma_exportar == "excel":
            print("Reporte de Servicios por Nombre:")
            print(df.sort_values(by=['Servicio']))

            exportar = input("¿Desea exportar el reporte a un archivo Excel? (Si/No): ").strip().lower()
            if exportar == 'si':
                fecha_reporte = datetime.now().strftime("%m_%d_%Y")
                nombre_archivo = f"ReporteServiciosPorNombre_{fecha_reporte}.xlsx"
                df.sort_values(by=['Servicio']).to_excel(nombre_archivo, index=False)
                print(f"Reporte exportado como '{nombre_archivo}'")
            elif exportar == 'no':
                pass
            else:
                print("Opción no válida. No se exportará el reporte.")
        elif forma_exportar == "csv":
            print("Reporte de Servicios por Nombre:")
            print(df.sort_values(by=['Servicio']))

            exportar = input("¿Desea exportar el reporte a un archivo CSV? (Si/No): ").strip().lower()
            if exportar == 'si':
                fecha_reporte = datetime.now().strftime("%m_%d_%Y")
                nombre_archivo = f"ReporteServiciosPorNombre_{fecha_reporte}.csv"
                df.sort_values(by=['Servicio']).to_csv(nombre_archivo, index=False)
                print(f"Reporte exportado como '{nombre_archivo}'")
            elif exportar == 'no':
                pass
            else:
                print("Opción no válida. No se exportará el reporte.")

     elif opcion == 6:
        clave_suspender = int(input("Ingrese la Clave Única del servicio que desea suspender (o 0 para volver al menú anterior): "))


        servicio_a_suspender = df[df['ClaveUnica'] == clave_suspender]

        if servicio_a_suspender.empty:
            print(f"No se encontraron datos para la Clave Única {clave_suspender}.")
            continue

        print("Datos del servicio a suspender:")
        print(servicio_a_suspender)

        confirmacion = input("¿Desea suspender este servicio? (Sí/No): ").strip().lower()

        if confirmacion == 'si':
            update_service(connection, clave_suspender, False)
            print(f"El servicio con Clave Única {clave_suspender} ha sido suspendido.")
        elif confirmacion == 'no':
            print("El servicio no ha sido suspendido.")
        else:
            print("Opción no válida. No se suspenderá el servicio.")

     elif opcion == 7:
        connection.close()
        break

    else:
        print("Opción no válida. Por favor, elige una opción válida.")

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
        else
            opcion = int(opcion)
            if (opcion == 1):
                NUEVO_CLIENTE()
            elif (opcion == 2):
                CONSULTAS_REPORTES()
            elif (opcion == 3):
                return
    
#ESTADISTICOS(TODOS)
