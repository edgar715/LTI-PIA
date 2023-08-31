dic_principal={6: ['Reparación', '08/09/2023', '27/10/2023']}

papelera={}

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


# Cancelar una nota: Se solicitará al usuario el folio de la nota a cancelar; 
# si la nota existe se desplegarán los datos de la nota indicada y todo el detalle que la conforma y 
# se le solicitará al usuario la confirmación para proceder a cancelar la nota antes de realizar dicha operación 
# considerando que puede no confirmarla y entonces no se procederá a la cancelación y se le informará que dicha 
# nota no fue cancelada. Si el folio indicado no existe o corresponde a una nota cancelada, se debe informar que 
#no está en el sistema. Considere que cancelar una nota no la debe eliminar realmente, simplemente se debe ignorar 
# para cualquier reporte que no sea de notas canceladas.

dic={1: ['Reparación', '08/09/2023', '27/10/2023'],
    2: ['Mantenimiento', '15/10/2023', '20/11/2023'],
    3: ['Recolección de residuos', '03/09/2023', '10/09/2023'],
    4: ['Inspección de equipos', '12/11/2023', '18/11/2023'],
    5: ['Capacitación sobre reciclaje', '22/09/2023', '30/09/2023']}

def eliminador_notas():
    while True:
        try:
            opcion=int(input('SELECCIONA EL FOLIO A ELIMINAR: \n'))
        except ValueError:
            print('debes ingresar un dato int no string vuelve a intentarlo')
            continue
        else:
            if opcion in dic:
                recuperador=dic[opcion]
                print('\nFOLIO\tNOTA\t\tFECHA DE INICIO\t\tTFECHA DE ENTREGA')
                print(f'{opcion}:\t{recuperador[0]}\t{recuperador[1]}\t\t{recuperador[2]}')
                break
            else:
                print('no existe')
    print('\n')
    while True: 
        try:
            print('[1] ELIMINAR\n[2] CANCELAR')
            opcion_2=int(input('SELECCIONA: \n'))
        except Exception:
            print("Debes ingresas un dato entero")
        else:
            if (opcion_2 == 1):
                recuperado=dic.pop(opcion)
                papelera[opcion]=recuperado
            if (opcion_2 == 2):
                print('NO SE HA PODIDO RECUPEAR')
            break  

recuperador_archivos()
print(dic)
print(papelera)
