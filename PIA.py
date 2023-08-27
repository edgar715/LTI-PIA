import datetime
#Aqui se hace la funcion del programa
def talonario(periodo, folio, nota, fecha_actual, fecha_procesada_final):
    periodo.append((folio, nota, fecha_actual, fecha_procesada_final))


periodo = []
folio = 1
#Aqui se hace un ciclo hasta que el usuario termine, primero se pregunta la fecha
while True:
    fecha_final = input("Dime la fecha en donde quieras que termine el periodo DD/MM/YYYY (o Enter para salir): ")
    #SI deja la fecha vacia ya se sale del ciclo
    if not fecha_final:
        break
    #Se almacena toda la informacion
    fecha_procesada_final = datetime.datetime.strptime(fecha_final, "%d/%m/%Y").date()
    fecha_actual = datetime.date.today()
    print(f"La fecha actual es {fecha_actual}")
#Se convierte a una fecha especifica
    if fecha_procesada_final < fecha_actual:
        print("Error de fecha, ingrese una fecha correspondiente")
        continue
    #Se dice la nota que quiere
    nota = input("Ingrese una nota para este periodo: ")
#Se almacena en la lista creada
    periodo.append((folio, nota, fecha_actual, fecha_procesada_final))
    folio += 1
#Se Tabula todos los datos en esta seccion
print("\nfolio\t\tnota\t\tfecha_actual\t\tfecha_final")
for folio, nota, fecha_actual, fecha_final in periodo:
    print(f"{folio: <5}\t\t{nota: <10}\t\t{fecha_actual.strftime('%d/%m/%Y'): <15}\t\t{fecha_final.strftime('%d/%m/%Y'): <15}")
