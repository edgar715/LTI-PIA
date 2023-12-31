import datetime as dt
import re
import csv
import os


clave = 0
fecha_actual = dt.datetime.now()
fecha_maxima = fecha_actual.strftime("%d/%m/%Y")
fecha_hoy = dt.datetime.strptime(fecha_maxima, "%d/%m/%Y")
rfc_dict = {}
dic_principal = {}
papelera={}

def no_cumple_condicion(valor):
    regex = r'^[a-zA-Z]{4}[0-9]{4}[a-zA-Z]{2}[0-9]{1}$'
    return not bool(re.match(regex, valor))   

def validar_email(email):
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return not bool (re.match(email_pattern, email))

def generar_folio():
    ultimo_folio = max(dic_principal.keys()) if dic_principal else 0
    nuevo_folio = ultimo_folio + 1
    return nuevo_folio

def registrar_nota():
    global clave
    print("REGISTRO DE NOTA")
    folio = generar_folio()
    fecha_inicio = fecha_actual

    while True:
        print(f"Fecha actual: {fecha_maxima}")
        fecha_nota = input("FECHA DE LA NOTA\nDEBERA CUMPLIR EL SIGUIENTE FORMATO: DD/MM/AAAA\n")
        if (fecha_nota.strip() == ""):
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
        cliente = input("ESCRIBE EL NOMBRE DEL CLIENTE:\n")
        if (cliente.strip() == ""):
            print("NO SE DEBE OMITIR EL DATO\n")
            continue
        break
    
    clave += 1      

    while True:    
        rfc = input("\nINGRESE EL RFC DE LA PERSONA:\n")
        rfc = rfc.upper()
        rfc_dict[clave] = rfc
        if no_cumple_condicion(rfc):
            print('\nEL RFC DEBE CONTENER LO SIGUIENTE')
            print('1: DEBE CONTENER 4 LETRAS')
            print('2: DESPUES DEBE CONTENER 4 NUMEROS')
            print('3: DESPUES DEBE CONTENER 2 LETRAS')
            print('4: FINALMENTE DEBE CONTENER 1 NUMERO')
            continue
        else:
            break 
    
    while True:
        correo_nota = input('\nINGRESA EL CORREO DEL CLIENTE:\n')
        if correo_nota.strip() == "":
            print('\nNO SE DEBE OMITIR EL DATO\n')
            continue
        if validar_email(correo_nota):
            print('\nFORMATO INCORRECTO INTENTE DE NUEVO\n')
            continue
        else:
            break
    
    servicios={}
    monto_total=[]

    while True:
        try:
            servicio_elegido=input("\nPARA DEJAR DE INGRESAR SERVICIOS INGRESE 0\nELIGE EL SERVICIO A REALIZAR:\n")
            if (servicio_elegido == ""):
                print("No se debe omitir el dato")
                continue
            if (servicio_elegido == "0"):
                break
        except Exception:
            print('ERROR INTENTE DE NUEVO')
            continue
        
        while True:
            try:
                monto=input("\nINGRESA EL MONTO DEL SERVICIO:\n")
                if (monto == ""):
                    print('NO SE DEBE OMITIR EL DATO\n')
                    continue
                if not (bool(re.match(r"^[0-9]+(\.[0-9]{1,2})?$", monto))):
                    print('NO CUMPLE CON EL FORMATO\nDEBE INCLUIR ENTEROS Y 2 DECIMALES')
                    continue
                monto=float(monto)
            except ValueError:
                print('SE DEBE INGRESAR SOLO DIGITOS')
                continue
            else:
                if (monto <= 0):
                    print('EL MONTO DEBE SER MAYOR A CERO\n')
                    continue
                servicios[servicio_elegido] = monto
                monto_total.append(monto)
            break
        
    
    monto_total=sum(monto_total)
    nueva_nota = [fecha_nota.strftime("%d/%m/%Y"), cliente, rfc, correo_nota,servicios, monto_total]
    dic_principal[folio] = nueva_nota

    print(f"Nota registrada con éxito. Folio: {folio}")
    print("Detalles de la nota:")
    print(f"Folio: {folio}")
    print(f"FECHA ACTUAL: {fecha_inicio.strftime('%d/%m/%Y')}")
    print(f"FECHA DE LA NOTA: {fecha_nota.strftime('%d/%m/%Y')}")
    print(f"CLIENTE: {cliente}")
    print(f'RFC del Cliente: {rfc}')
    print(f'CORREO DEL CLIENTE: {correo_nota}')
    for servicio, monto in servicios.items():
        print(f'{servicio} CON UN COSTO DE: {monto}')
    print(f'Monto Total: {monto_total}')

def consultar_folio():  
    while True:
        try:
            consultar = input("Escribe el id de la nota que buscas\n[0] SALIDA")
            if (consultar == ""):
                print('no se debe omitir el dato')
                continue
            if not(bool(re.match("^[0-9]{1,9}$",consultar))):
                print("No se ingreso un digito")
                continue
            consultar=int(consultar)
            if (consultar == 0):
                return
        except ValueError:
            print("Ingreso un valor no valido")
        else:
            if consultar in dic_principal:
                recuperador = dic_principal[consultar]
                print('\nFOLIO\tCLIENTE\t\tFECHA DE PEDIDO\t\tFECHA DE ENTREGA\t\tSERVICIO\t\tMONTO')
                print(f'{consultar}:\t{recuperador[0]}\t\t{recuperador[1]}\t\t{recuperador[2]}\t\t{recuperador[3]}\t\t{recuperador[4]}')
            if consultar not in dic_principal:
                print("No existe registros\nEstos son los folios que tenemos en nuestra base de datos")
                print(list(dic_principal.keys())) 
   
def consultar_periodo():
    while True:
        try:
            fecha_inicio=input("\nINGRESE LA FECHA INICIAL: DD/MM/AAAA\n")
            if fecha_inicio.strip() == "":
                fecha_inicio = "01/01/2000" 
            fecha_inicio=dt.datetime.strptime(fecha_inicio, "%d/%m/%Y")
        except ValueError:
            print("\nFormato de fecha incorrecto, ingrese la fecha en el formato DD/MM/AAAA\n")
    
        while True:
            try:
                fecha_final=input("INGRESE LA FECHA FINAL: DD/MM/AAAA\n")
                if fecha_final.strip() == "":
                    fecha_final = fecha_hoy
                else:
                    fecha_final=dt.datetime.strptime(fecha_final, "%d/%m/%Y")
            except ValueError:
                print("Formato de fecha incorrecto, ingrese la fecha en el formato (DD/MM/AAAA)")
            else:
                break
        if fecha_inicio > fecha_final:
            print('\nLA FECHA INICIO DEBE SER MENOR A LA FECHA FINAL\n')
            continue
        break
    
    for folio, recuperador in dic_principal.items():
        fecha_inicio_diccionario = dt.datetime.strptime(recuperador[0], '%d/%m/%Y')
    
        if (fecha_inicio <= fecha_inicio_diccionario <= fecha_final):
            for folio, notas in dic_principal.items():
                    print('FOLIO   FECHA DE LA NOTA    CLIENTE    RFC            CORREO         MONTO TOTAL')
                    print(f'{folio}\t{notas[0]}\t\t{notas[1]}\t{notas[2]}\t{notas[3]}\t\t{notas[5]}')
                    print(f'SERVICIOS Y PRECIOS:\n{notas[4]}\n')


def consultas_reportes():
    while True:
        print('COMO DESEAS CONSULTAR EN LA BASE DE DATOS:\n')
        print('[1] POR PERIODO\n[2] POR FOLIO')
        try:
            opcion = input('SELECCIONA: ')
            if (opcion.strip() == ""):
                print('No se debe omitir el dato')
                continue
            if not(bool(re.match("^[0-2]{1}$",opcion))):
                print('No cumple con el patron')
                continue
            opcion=int(opcion)
            if opcion == 1:
                consultar_periodo()
            elif opcion == 2:
                consultar_folio()
        except ValueError:
            print('Debes ingresar un dato entero')
        break

def recuperador_notas():
    if not papelera:
        print('\nPAPELERA VACIA REGRESANDO...\n')
        return
    print("RECUPERACIÓN DE NOTAS")
    for folio, notas in papelera.items():
        print('FOLIO   FECHA DE LA NOTA    CLIENTE    RFC            CORREO         MONTO TOTAL')
        print(f'{folio}\t{notas[0]}\t\t{notas[1]}\t{notas[2]}\t{notas[3]}\t\t{notas[5]}')

    while True:
        try:
            opcion = input('SELECCIONA EL FOLIO A RECUPERAR: ')
            if (opcion.strip() == ""):
                print('No se debe omitir el dato')
                continue
            if not(bool(re.match("^[0-9]{1,9}$", opcion))):
                print('no cumple con el patron')
                continue
            opcion=int(opcion)
        except ValueError:
            print('se debe ingresar un entero no un decimal')
        else:
            if opcion not in papelera:
                print(f'EL FOLIO {opcion} NO EXISTE, INTENTA DE NUEVO')
                continue
            if opcion in papelera:
                for folio, notas in papelera.items():
                    print('FOLIO   FECHA DE LA NOTA    CLIENTE    RFC            CORREO         MONTO TOTAL')
                    print(f'{folio}\t{notas[0]}\t\t{notas[1]}\t{notas[2]}\t{notas[3]}\t\t{notas[5]}')
                    print(f'SERVICIOS Y PRECIOS:\n{notas[4]}\n')

                while True:
                    try:
                        print('[1] RECUPERAR\n[2] CANCELAR')
                        opcion_2 = input('SELECCIONA: ')
                        if (opcion_2.strip() == ""):
                            print('No se de omitir el dato')
                            continue
                        if not(bool(re.match("^[1-2]{1}$", opcion_2))):
                            print('no cumple con el patron')
                            continue
                        opcion_2=int(opcion_2)    
                        if opcion_2 == 1:
                            recuperado = papelera.pop(opcion)
                            dic_principal[opcion] = recuperado
                            print('NOTA RECUPERADA CON ÉXITO')
                        elif opcion_2 == 2:
                            print('NO SE HA PODIDO RECUPERAR LA NOTA')
                        else:
                            print('HAS SELECCIONADO UN COMANDO INEXISTENTE \n INTENTA DE NUEVO')
                            continue
                        break
                    except ValueError:
                        print('Debes ingresar un dato entero no decimal')  

def cancelador_notas():
    if not dic_principal:
        print('\nDICCIONARIO PRINCIPAL VACIO REGRESANDO...\n')
        return
    
    print("\nCANCELADOR DE NOTAS\n")
    while True:
        try:
            opcion = input('\nSELECCIONA EL FOLIO A ELIMINAR\n: ')
            if (opcion.strip() == ""):
                print('NO SE OMITE EL DATO')
                continue
            opcion=int(opcion)
        except ValueError:
            print("\nSOLO SE ACEPTAN DIGITOS\n")
            continue
        else:
            if opcion not in dic_principal:
                print(f'\nEL FOLIO {opcion} NO ESTA EN EL DICCIONARIO PRINCIPAL, INTENTA DE NUEVO\n')
                continue
            if opcion in dic_principal:
                for folio, notas in dic_principal.items():
                    print(f"Nota registrada con éxito. Folio: {folio}")
                    print("Detalles de la nota:")
                    print(f"Folio: {folio}")
                    print(f"FECHA DE LA NOTA: {notas[0]}")
                    print(f"CLIENTE: {notas[1]}")
                    print(f'RFC del Cliente: {notas[2]}')
                    print(f'CORREO DEL CLIENTE: {notas[3]}')
                    print(f'SERVICIOS Y SUS PRECIOS\n{notas[4]}')
                    print(f'MONTO TOTAL: {notas[5]}\n')
            break

    while True:
        try:
            print('[1] CANCELAR NOTA\n[2] NO CANCELAR LA NOTA')
            opcion_2 = input('SELECCIONA: ')
            if (opcion_2.strip() == ""):
                print('NO SE OMITE EL DATO')
                continue
            if not(bool(re.match("^[1-2]{1}$",opcion_2))):
                print('NO CUMPLE CON EL PATRON')
                continue
            opcion_2=int(opcion_2)
            if opcion_2 == 1:
                eliminado = dic_principal.pop(opcion)
                papelera[opcion] = eliminado
                print('NOTA CANCELADA CON ÉXITO')
                break
            elif opcion_2 == 2:
                print('NO SE HA PODIDO CANCELAR LA NOTA')
                break
        except ValueError:
            print('DEBES INGRESAR UN DATO ENTERO')
            continue

def menu_principal():
    while True:
        try:
            print("\nMENU PRINCIPAL")
            print("[1] Registrar Nota\n[2] Consultas y reportes\n[3] Cancelar una nota\n[4] Recuperar una nota\n[5] SALIDA")
            opcion = input('Ingresa una opcion:\n')
            if (opcion.strip() == ""):
                print('No se debe omitir el dato')
                continue
            if not(bool(re.match("^[1-5]{1}$",opcion))):
                print("El comando no existe intenta de nuevo del 1 al 5")
                continue
            opcion = int(opcion)
        except ValueError:
            print("El dato debe ser entero no decimal")
        else:
            if (opcion == 1):
                registrar_nota()
            elif (opcion == 2):
                consultas_reportes()
            elif (opcion == 3):
                cancelador_notas()
            elif (opcion == 4):
                recuperador_notas()
            elif (opcion == 5):
                # Llamar a la función para guardar el diccionario en CSV
                guardar_dic_principal(dic_principal)
                return
            elif (opcion > 5):
                print('No existe el Comando intenta de nuevo')
                continue

def guardar_dic_principal(dic_principal):
    with open("mecanico.csv","w", newline="") as pia:
        mecanico = csv.writer(pia)
        mecanico.writerow(["Folio", "Fecha de Nota", "Cliente", "RFC", "Correo", "Servicios", "Monto Total"])
        for folio, datos in dic_principal.items():
            fecha, cliente, rfc, correo, servicios, monto = datos
            folio = int(folio)
            monto = float(monto)
            mecanico.writerow([folio, fecha, cliente, rfc, correo, servicios, monto])

def cargar_datos_desde_csv():
    if os.path.exists("mecanico.csv"):
        with open("mecanico.csv", "r") as archivo_csv:
            lector_csv = csv.reader(archivo_csv)
            for fila in lector_csv:
                folio, fecha, cliente, rfc, correo, servicios, monto = fila
                dic_principal[folio] = [fecha, cliente, rfc, correo, servicios, monto]
        print("Datos cargados desde el archivo CSV.")
    else:
        print("No se encontró un archivo CSV. La aplicación parte de un estado inicial vacío.")

cargar_datos_desde_csv()
menu_principal()