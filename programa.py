# Recuperar una nota: Se le mostrará al usuario un listado tabular de las notas actualmente canceladas (sin su detalle), 
#y el usuario deberá indicar el folio de la nota que desea recuperar o bien indicar que no desea recuperar ninguna de las notas 
#presentadas. Si el usuario indica un folio que corresponde a una nota que se encuentra cancelada, 
#se le deberá mostrar el detalle de dicha nota y se le pedirá que confirme su intención de recuperarla considerando que 
#puede no confirmarla y entonces no se procederá a la recuperación y se le informará que dicha nota no fue recuperada.
import datetime

servicios = {
    'Reparación': 100,
    'Mantenimiento': 150,
    'Recolección de residuos': 50,
    'Inspección de equipos': 120,
    'Capacitación sobre reciclaje': 80
}

fecha_actual = datetime.datetime.now()
fecha_maxima = fecha_actual.strftime("%d/%m/%Y")

dic_principal = {}

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

    nueva_nota = [cliente, fecha_inicio.strftime("%d/%m/%Y"), servicios_elegidos, monto_total]
    dic_principal[folio] = nueva_nota

    print(f"Nota registrada con éxito. Folio: {folio}")
    print("Detalles de la nota:")
    print(f"Folio: {folio}")
    print(f"Fecha: {fecha_inicio.strftime('%d/%m/%Y')}")
    print(f"Cliente: {cliente}")
    print("Servicios seleccionados:")
    for servicio in servicios_elegidos:
        print(f"- {servicio}")
    print(f"Monto Total: ${monto_total}")

def recuperador_notas():
    print("RECUPERACIÓN DE NOTAS")
    print(f'FOLIO\tNOTAS CANCELADAS')
    for folio, notas in dic_principal.items():
        print(f'{folio}\t{notas[0]}')

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
            if opcion not in dic_principal:
                print(f'EL FOLIO {opcion} NO EXISTE, INTENTA DE NUEVO')
                continue
            recuperador = dic_principal[opcion]
            print('\nFOLIO\tNOTA\t\tFECHA DE INICIO\t\tTFECHA DE ENTREGA')
            print(f'{opcion}:\t{recuperador[0]}\t{recuperador[1]}\t\t{recuperador[2]}')
        except ValueError:
            if "." in opcion:
                print('Debes ingresar un dato entero no decimal, vuelve a intentarlo')
            else:
                print('Debes ingresar un dato entero no cadena de texto, vuelve a intentarlo')
                continue

        while True:
            try:
                print('[1] RECUPERAR\n[2] CANCELAR')
                opcion_2 = int(input('SELECCIONA: '))
                if opcion_2 == 1:
                    recuperado = dic_principal.pop(opcion)
                    servicios[opcion] = recuperado
                    print('NOTA RECUPERADA CON ÉXITO')
                elif opcion_2 == 2:
                    print('NO SE HA PODIDO RECUPERAR LA NOTA')
                else:
                    print('HAS SELECCIONADO UN COMANDO INEXISTENTE \n INTENTA DE NUEVO')
                    continue
                break
            except ValueError:
                print('Debes ingresar un dato entero')     
    
def recuperador_notas():
    print("RECUPERACIÓN DE NOTAS")
    print(f'FOLIO\tNOTAS CANCELADAS')
    for folio, notas in dic_principal.items():
        print(f'{folio}\t{notas[0]}')

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
            if opcion not in dic_principal:
                print(f'EL FOLIO {opcion} NO EXISTE, INTENTA DE NUEVO')
                continue
            recuperador = dic_principal[opcion]
            print('\nFOLIO\tNOTA\t\tFECHA DE INICIO\t\tTFECHA DE ENTREGA')
            print(f'{opcion}:\t{recuperador[0]}\t{recuperador[1]}\t\t{recuperador[2]}')
        except ValueError:
            if "." in opcion:
                print('Debes ingresar un dato entero no decimal, vuelve a intentarlo')
            else:
                print('Debes ingresar un dato entero no cadena de texto, vuelve a intentarlo')
                continue

        while True:
            try:
                print('[1] RECUPERAR\n[2] CANCELAR')
                opcion_2 = int(input('SELECCIONA: '))
                if opcion_2 == 1:
                    recuperado = dic_principal.pop(opcion)
                    servicios[opcion] = recuperado
                    print('NOTA RECUPERADA CON ÉXITO')
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
            if opcion not in dic_principal:
                print(f'EL FOLIO {opcion} NO EXISTE, INTENTA DE NUEVO')
                continue
            recuperador = dic_principal[opcion]
            print('\nFOLIO\tNOTA\t\tFECHA DE INICIO\t\tTFECHA DE ENTREGA')
            print(f'{opcion}:\t{recuperador[0]}\t{recuperador[1]}\t\t{recuperador[2]}')
        except ValueError:
            print('Debes ingresar un dato entero')

        while True:
            try:
                print('[1] ELIMINAR\n[2] CANCELAR')
                opcion_2 = int(input('SELECCIONA: '))
                if opcion_2 == 1:
                    eliminado = dic_principal.pop(opcion)
                    servicios[opcion] = eliminado
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
            print("[1] Registrar Nota\n[2] Concultas y reportes\n[3] Cancelar una nota\n[4] Recuperar una nota\n [5] SALIDA")
            opcion = input('Ingresa una opcion:\n')
            if opcion.strip() == "":
                print('No se debe omitir el dato')
                continue
            if not opcion.isdigit():
                print('El dato debe ser un digito no un str')
                continue
            opcion = int(opcion)
            if opcion > 5:
                print('No existe el Comando intenta de nuevo')
                continue
        except ValueError:
            print('El dato debe ser entero no decimal')
        else:
            if (opcion == 1):
                registrar_nota()
            elif (opcion == 2):
                
            elif (opcion == 3):
                eliminador_notas()
            elif (opcion == 4):
                recuperador_notas()
            elif (opcion == 5):
                return

menu_principal()
        
        


