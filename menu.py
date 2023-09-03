diccionario = {
    1: ["Reparaciond de motor"],
    2: ["Cambio de llantas"],
    3: ["Refaccion de asientos"]
}
      
while True:
    try:
        consultar = int(input("Escribe el id de la nota que buscas")) 
        for folio, notas in diccionario.items():
            if consultar == folio:
                print(f'Folio\tNotas')
                print(f'{folio}\t{notas[0]}')
        if consultar not in diccionario:
            print("No existe registros\nEstos son los folios que tenemos en nuestra base de datos")
            print(list(diccionario.keys()))

    except ValueError:
        print("Ingreso un valor no valido")
