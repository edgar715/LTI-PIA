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
