diccionario = {
    1: ["Reparaciond de motor"],
    2: ["Cambio de llantas"],
    3: ["Refaccion de asientos"]
}

variable = int(input("Dime el id de la clave que borraras"))
diccionario.pop(variable)
print(f'Folio\tNotas')
for folio , notas in diccionario.items():
    print(f'{folio}\t{notas[0]}')

consultar = int(input("Escribe el id de la nota que buscas"))
for folio , notas in diccionario.items():
    if consultar == folio:
        print(f'{folio}\t{notas[0]}')
