papelera={1: ['Reparación', '08/09/2023', '27/10/2023'],
    2: ['Mantenimiento', '15/10/2023', '20/11/2023'],
    3: ['Recolección de residuos', '03/09/2023', '10/09/2023'],
    4: ['Inspección de equipos', '12/11/2023', '18/11/2023'],
    5: ['Capacitación sobre reciclaje', '22/09/2023', '30/09/2023']}

dic_principal={6: ['Reparación', '08/09/2023', '27/10/2023']}

def recuperador_archivos():
    print(f'folio')
    for folio in papelera:
        print(folio)

    while True:
        try:
            opcion=int(input('SELECCIONA EL FOLIO A RECUPERAR: \n'))
        except ValueError:
            print('debes ingresar un dato int no string vuelve a intentarlo')
            continue
        else:
            if opcion in papelera:
                recuperador=papelera[opcion]
                print('\nFOLIO\tNOTA\t\tFECHA DE INICIO\t\tTFECHA DE ENTREGA')
                print(f'{opcion}:\t{recuperador[0]}\t{recuperador[1]}\t\t{recuperador[2]}')
                break
            else:
                print('no existe')
    print('\n')
    while True: 
        try:
            print('[1] RECUPERAR\n[2] CANCELAR')
            opcion_2=int(input('SELECCIONA: \n'))
        except Exception:
            print("Debes ingresas un dato entero")
        else:
            if (opcion_2 == 1):
                recuperado=papelera.pop(opcion)
                dic_principal[opcion]=recuperado
            if (opcion_2 == 2):
                print('NO SE HA PODIDO RECUPEAR')
            break



recuperador_archivos()
print(dic_principal)