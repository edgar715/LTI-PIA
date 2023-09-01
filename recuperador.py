# Recuperar una nota: Se le mostrará al usuario un listado tabular de las notas actualmente canceladas (sin su detalle), 
#y el usuario deberá indicar el folio de la nota que desea recuperar o bien indicar que no desea recuperar ninguna de las notas 
#presentadas. Si el usuario indica un folio que corresponde a una nota que se encuentra cancelada, 
#se le deberá mostrar el detalle de dicha nota y se le pedirá que confirme su intención de recuperarla considerando que 
#puede no confirmarla y entonces no se procederá a la recuperación y se le informará que dicha nota no fue recuperada.
import re

papelera={1: ['Reparación', '08/09/2023', '27/10/2023'],
    2: ['Mantenimiento', '15/10/2023', '20/11/2023'],
    3: ['Recolección de residuos', '03/09/2023', '10/09/2023'],
    4: ['Inspección de equipos', '12/11/2023', '18/11/2023'],
    5: ['Capacitación sobre reciclaje', '22/09/2023', '30/09/2023']}

dic_principal={6: ['Reparación', '08/09/2023', '27/10/2023']}

def recuperador_notas():
    print(f'FOLIO\tNOTAS CANCELADAS')
    for folio , notas in papelera.items():
        print(f'{folio}\t{notas[0]}')

    print('')
    while True:
        try:
            opcion=input('SELECCIONA EL FOLIO A RECUPERAR: \n')
            if (opcion.strip() == ""):
                print('no se debe omitir el dato')
                continue
            opcion=int(opcion)
        except ValueError:
            if ("." in opcion):
                print('debes ingresar un dato entero no decimal, vuelve a intentarlo')
                continue
            else:
                print('debes ingresar un dato entero no cadena de texto, vuelve a intentarlo')
                continue
        else:
            if opcion in papelera:
                recuperador=papelera[opcion]
                print('\nFOLIO\tNOTA\t\tFECHA DE INICIO\t\tTFECHA DE ENTREGA')
                print(f'{opcion}:\t{recuperador[0]}\t{recuperador[1]}\t\t{recuperador[2]}')
                break
            else:
                print(f'EL FOLIO {opcion} NO EXISTE, INTENTE DE NUEVO')
    print('\n')
    while True:    
        try:
            print('[1] RECUPERAR\n[2] CANCELAR')
            opcion_2=input('SELECCIONA: \n')
            if (opcion_2.strip() == ""):
                print('no se debe omitir el dato')
                continue
            opcion_2=int(opcion_2)
        except ValueError:
            if ("." in opcion_2):
                print('debes ingresar un dato entero no decimal, vuelve a intentarlo')
                continue
            else:
                print('debes ingresar un dato entero no cadena de texto, vuelve a intentarlo')
                continue

        if (opcion_2 == 1):
            recuperado=papelera.pop(opcion)
            dic_principal[opcion]=recuperado
        if (opcion_2 == 2):
            print('NO SE HA PODIDO RECUPEAR LA NOTA')
        if (opcion_2 > 2):
            print('HAS SELECCIONADO UN COMANDO INEXISTENTE \n INTENTA DE NUEVO')
            continue
        break
                

def eliminador_notas():
    while True:
        try:
            opcion=int(input('SELECCIONA EL FOLIO A ELIMINAR: \n'))
        except ValueError:
            print('debes ingresar un dato entero no decimal vuelve a intentarlo')
            continue
        else:
            if opcion in dic_principal:
                recuperador=dic_principal[opcion]
                print('\nFOLIO\tNOTA\t\tFECHA DE INICIO\t\tTFECHA DE ENTREGA')
                print(f'{opcion}:\t{recuperador[0]}\t{recuperador[1]}\t\t{recuperador[2]}')
                break
            else:
                print(f'LA NOTA {opcion} SE ENCUENTRA EN LA PAPELERA,\n')
    print('\n')
    while True: 
        try:
            print('[1] ELIMINAR\n[2] CANCELAR')
            opcion_2=int(input('SELECCIONA: \n'))
        except Exception:
            print("Debes ingresas un dato entero")
        else:
            if (opcion_2 == 1):
                recuperado=dic_principal.pop(opcion)
                papelera[opcion]=recuperado
            if (opcion_2 == 2):
                print('NO SE HA PODIDO CANCELAR LA NOTA')
            break

recuperador_notas()
