import datetime as dt
import re

fecha_actual = dt.datetime.now()
fecha_maxima = fecha_actual.strftime("%d/%m/%Y")

dic_principal = {}
papelera={}

def generar_folio():
    ultimo_folio = max(dic_principal.keys()) if dic_principal else 0
    nuevo_folio = ultimo_folio + 1
    return nuevo_folio

def registrar_nota():
    print("REGISTRO DE NOTA")
    folio = generar_folio()
    fecha_inicio = fecha_actual
    while True:
        cliente = input("Cliente:\n")
        if (cliente.strip() == ""):
            print("No se debe omitir el dato")
            continue
        break
    while True:
        try:
            print(f"Fecha actual: {fecha_maxima}")
            fecha_entrega = input("Fecha de entrega (DD/MM/AAAA): ")
            fecha_entrega = dt.datetime.strptime(fecha_entrega, "%d/%m/%Y")
            if fecha_entrega > fecha_actual:
                print("La fecha de entrega debe ser mayor a la fecha actual. Inténtalo de nuevo.")
                continue
            break
        except ValueError:
            print("Formato de fecha incorrecto. Inténtalo de nuevo (DD/MM/AAAA).")
    while True:
        servicio_elegido=input("Elige el servicio que requieres:\n")
        if (servicio_elegido == ""):
            print("No se debe omitir el dato")
            continue
        if not(bool(re.match("^[A-Za-z]$",servicio_elegido))):
            print('Solo se debe ingresar caracteres')
            continue
        break
    while True:
        try:
            monto_total=float(input("Ingresa el monto a cobrar:\n"))
        except Exception:
            print('se debe ingresar digitos')
        else:
            break


    nueva_nota = [cliente, fecha_inicio.strftime("%d/%m/%Y"), fecha_entrega.strftime("%d/%m/%Y") ,servicio_elegido, monto_total]
    dic_principal[folio] = nueva_nota

    print(f"Nota registrada con éxito. Folio: {folio}")
    print("Detalles de la nota:")
    print(f"Folio: {folio}")
    print(f"Fecha de Pedido: {fecha_inicio.strftime('%d/%m/%Y')}")
    print(f"Fecha de Entrega: {fecha_entrega.strftime('%d/%m/%Y')}")
    print(f"Cliente: {cliente}")
    print(f"Servicio: {servicio_elegido}")
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
            fecha_inicio=input("Ingrese la fecha inicial: (DD/MM/AAAA)")
            fecha_inicio=dt.datetime.strptime(fecha_inicio, "%d/%m/%Y")
        except ValueError:
            print("Formato de fecha incorrecto, ingrese la fecha en el formato (DD/MM/AAAA)")
        else:
            break
    
    while True:
        try:
            fecha_final=input("Ingrese la fecha inicial: (DD/MM/AAAA)")
            fecha_final=dt.datetime.strptime(fecha_final, "%d/%m/%Y")
        except ValueError:
            print("Formato de fecha incorrecto, ingrese la fecha en el formato (DD/MM/AAAA)")
        else:
            break
    
    for folio, recuperador in dic_principal.items():
        fecha_inicio_diccionario = dt.datetime.strptime(recuperador[1], '%d/%m/%Y')
        fecha_final_diccionario = dt.datetime.strptime(recuperador[2], '%d/%m/%Y')
    
        if (fecha_inicio <= fecha_inicio_diccionario <= fecha_final) or (fecha_inicio <= fecha_final_diccionario <= fecha_final):
            print('\nFOLIO\tCLIENTE\t\tFECHA DE PEDIDO\t\tFECHA DE ENTREGA\t\tSERVICIO\t\tMONTO')
            print(f'{folio}:\t{recuperador[0]}\t\t{recuperador[1]}\t\t{recuperador[2]}\t\t{recuperador[3]}\t\t{recuperador[4]}')

def consultas_reportes():
    while True:
        print('COMO DESEAS CONSULTAR EN LA BASE DE DATOS:\n')
        print('[1] POR PERIODO\n[2] POR FOLIO\n[0] para regresar al menu principal')
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
            elif opcion == 0:
                return
        except ValueError:
            print('Debes ingresar un dato entero')

def recuperador_notas():
    print("RECUPERACIÓN DE NOTAS")
    print(f'FOLIO\tNOTAS CANCELADAS')
    for folio, notas in papelera.items():
        print(f'{folio}\t{notas[3]}')

    print('')
    while True:
        try:
            opcion = input('SELECCIONA EL FOLIO A RECUPERAR (0 para volver al menú principal): ')
            if (opcion.strip() == ""):
                print('No se debe omitir el dato')
                continue
            if not(bool(re.match("^[0-9]{1,9}$", opcion))):
                print('no cumple con el patron')
                continue
            opcion=int(opcion)
            if opcion == 0:
                return
        except ValueError:
            print('se debe ingresar un entero no un decimal')
        else:
            if opcion not in papelera:
                print(f'EL FOLIO {opcion} NO EXISTE, INTENTA DE NUEVO')
                continue
            if opcion in papelera:
                recuperador = papelera[opcion]
                print('\nFOLIO\tCLIENTE\t\tFECHA DE PEDIDO\t\tFECHA DE ENTREGA\t\tSERVICIO\t\tMONTO')
                print(f'{opcion}:\t{recuperador[0]}\t\t{recuperador[1]}\t\t{recuperador[2]}\t\t{recuperador[3]}\t\t{recuperador[4]}')
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

def eliminador_notas():
    print("ELIMINACIÓN DE NOTAS")
    while True:
        try:
            opcion = input('SELECCIONA EL FOLIO A ELIMINAR (0 para volver al menú principal): ')
            if (opcion.strip() == ""):
                print('No se debe omitir el dato')
                continue
            if not(bool(re.match("^[0-9]{1,9}$", opcion))):
                print('no cumple con el patron')
                continue
            opcion=int(opcion)
            if opcion == 0:
                return
        except Exception:
            print("Solo se aceptan datos enteros no decimales")
        else:
            if opcion not in dic_principal:
                print(f'EL FOLIO {opcion} NO EXISTE, INTENTA DE NUEVO')
                continue
            if opcion in dic_principal:
                recuperador = dic_principal[opcion]
                print('\nFOLIO\tCLIENTE\t\tFECHA DE PEDIDO\t\tFECHA DE ENTREGA\tSERVICIO\tMONTO')
                print(f'{opcion}:\t\t{recuperador[0]}\t\t{recuperador[1]}\t\t{recuperador[2]}\t\t{recuperador[3]}\t\t{recuperador[4]}')
                while True:
                    try:
                        print('[1] ELIMINAR\n[2] CANCELAR')
                        opcion_2 = input('SELECCIONA: ')
                        if (opcion_2.strip() == ""):
                            print('No se debe omitir el dato')
                            continue
                        if not(bool(re.match("^[1-2]{1}$",opcion_2))):
                            print('No cumple con el patron')
                            continue
                        opcion_2=int(opcion_2)
                        if opcion_2 == 1:
                            eliminado = dic_principal.pop(opcion)
                            papelera[opcion] = eliminado
                            print('NOTA ELIMINADA CON ÉXITO')
                        elif opcion_2 == 2:
                            print('NO SE HA PODIDO CANCELAR LA NOTA')
                        else:
                            print('HAS SELECCIONADO UN COMANDO INEXISTENTE \n INTENTA DE NUEVO')
                            continue
                        break
                    except ValueError:
                        print('Debes ingresar un dato entero')

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
                eliminador_notas()
            elif (opcion == 4):
                recuperador_notas()
            elif (opcion == 5):
                return
            elif (opcion > 5):
                print('No existe el Comando intenta de nuevo')
                continue

menu_principal()