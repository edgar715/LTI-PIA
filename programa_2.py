import datetime as dt

servicios = {
    'Reparación': 100,
    'Mantenimiento': 150,
    'Recolección de residuos': 50,
    'Inspección de equipos': 120,
    'Capacitación sobre reciclaje': 80
}

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
    cliente = input("Cliente: ")

    print("Servicios disponibles:")
    for i, (servicio, precio) in enumerate(servicios.items(), start=1):
        print(f"{i}. {servicio} - ${precio}")

    servicios_elegidos = []
    while True:
        try:
            opcion_servicio = int(input("Selecciona un servicio (0 para finalizar): "))
            if opcion_servicio == 0:
                break
            elif opcion_servicio < 1 or opcion_servicio > len(servicios):
                print("Opción inválida. Inténtalo de nuevo.")
                continue
            else:
                servicio_elegido = list(servicios.keys())[opcion_servicio - 1]
                servicios_elegidos.append(servicio_elegido)
        except ValueError:
            print("Opción inválida. Inténtalo de nuevo.")

    monto_total = sum(servicios.get(servicio, 0) for servicio in servicios_elegidos)

    while True:
        try:
            print(f"Fecha actual: {fecha_maxima}")
            fecha_entrega = input("Fecha de entrega (DD/MM/AAAA): ")
            fecha_entrega = dt.datetime.strptime(fecha_entrega, "%d/%m/%Y")
            if fecha_entrega <= fecha_actual:
                print("La fecha de entrega debe ser mayor a la fecha actual. Inténtalo de nuevo.")
                continue
            break
        except ValueError:
            print("Formato de fecha incorrecto. Inténtalo de nuevo (DD/MM/AAAA).")

    nueva_nota = [cliente, fecha_inicio.strftime("%d/%m/%Y"), fecha_entrega.strftime("%d/%m/%Y") ,servicios_elegidos, monto_total]
    dic_principal[folio] = nueva_nota

    print(f"Nota registrada con éxito. Folio: {folio}")
    print("Detalles de la nota:")
    print(f"Folio: {folio}")
    print(f"Fecha de Pedido: {fecha_inicio.strftime('%d/%m/%Y')}")
    print(f"Fecha de Entrega: {fecha_entrega.strftime('%d/%m/%Y')}")
    print(f"Cliente: {cliente}")
    print("Servicios seleccionados:")
    for servicio in servicios_elegidos:
        print(f"- {servicio}")
    print(f"Monto Total: ${monto_total}")

def recuperador_notas():
    print(dic_principal, '\n',papelera)
    print("RECUPERACIÓN DE NOTAS")
    print(f'FOLIO\tNOTAS CANCELADAS')
    for folio, notas in papelera.items():
        print(f'{folio}\t{notas[3]}')

    print('')
    while True:
        try:
            opcion = input('SELECCIONA EL FOLIO A RECUPERAR (0 para volver al menú principal): ')
            if opcion.strip() == "":
                print('No se debe omitir el dato')
                continue
            opcion = int(opcion)
            if opcion == 0:
                return
            
            
        except ValueError:
            if "." in opcion:
                print('Debes ingresar un dato entero no decimal, vuelve a intentarlo')
            else:
                print('Debes ingresar un dato entero no cadena de texto, vuelve a intentarlo')
                continue
        else:
            if opcion not in papelera:
                print(f'EL FOLIO {opcion} NO EXISTE, INTENTA DE NUEVO')
                continue
            if opcion in papelera:
                recuperador = papelera[opcion]
                print('\nFOLIO\tNOTA CANCELADA')
                print(f'{opcion}:\t\t{recuperador[2]}')
                while True:
                    try:
                        print('[1] RECUPERAR\n[2] CANCELAR')
                        opcion_2 = int(input('SELECCIONA: '))
                        if opcion_2 == 1:
                            recuperado = papelera.pop(opcion)
                            dic_principal[opcion] = recuperado
                            print('NOTA RECUPERADA CON ÉXITO')
                            print(dic_principal, '\n',papelera)
                        elif opcion_2 == 2:
                            print('NO SE HA PODIDO RECUPERAR LA NOTA')
                        else:
                            print('HAS SELECCIONADO UN COMANDO INEXISTENTE \n INTENTA DE NUEVO')
                            continue
                        break
                    except ValueError:
                        print('Debes ingresar un dato entero')  

          
    
def eliminador_notas():
    print("ELIMINACIÓN DE NOTAS")
    while True:
        try:
            opcion = int(input('SELECCIONA EL FOLIO A ELIMINAR (0 para volver al menú principal): '))
            if opcion == 0:
                return
        except Exception:
            print("Dato no valido, Intenta de Nuevo")
        else:
            if opcion not in dic_principal:
                print(f'EL FOLIO {opcion} NO EXISTE, INTENTA DE NUEVO')
                continue
            if opcion in dic_principal:
                recuperador = dic_principal[opcion]
                print('\nFOLIO\tCLIENTE\t\tFECHA DE PEDIDO\t\tFECHA DE ENTREGA\t\tSERVICIO\t\tMONTO')
                print(f'{opcion}:\t{recuperador[0]}\t\t{recuperador[1]}\t\t{recuperador[2]}\t\t{recuperador[3]}\t\t{recuperador[4]}')
                while True:
                    try:
                        print('[1] ELIMINAR\n[2] CANCELAR')
                        opcion_2 = int(input('SELECCIONA: '))
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
            if not (opcion.isdigit()):
                print('El dato debe ser un digito no un str')
                continue
            else:
                opcion = int(opcion)
        except ValueError:
            print("El dato debe ser entero no decimal")
        else:
            if (opcion == 1):
                registrar_nota()
            elif (opcion == 2):
                print('eso tilin')
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
        


