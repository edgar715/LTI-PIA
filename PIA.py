import datetime

def talonario(periodo, folio, nota, fecha_actual, fecha_procesada_final):
    periodo.append((folio, nota, fecha_actual, fecha_procesada_final))


periodo = []
folio = 1

while True:
    fecha_final = input("Dime la fecha en donde quieras que termine el periodo DD/MM/YYYY (o Enter para salir): ")
    
    if not fecha_final:
        break
    
    fecha_procesada_final = datetime.datetime.strptime(fecha_final, "%d/%m/%Y").date()
    fecha_actual = datetime.date.today()
    print(f"La fecha actual es {fecha_actual}")

    if fecha_procesada_final < fecha_actual:
        print("Error de fecha, ingrese una fecha correspondiente")
        continue
    
    nota = input("Ingrese una nota para este periodo: ")

    periodo.append((folio, nota, fecha_actual, fecha_procesada_final))
    folio += 1

print("\nfolio\t\tnota\t\tfecha_actual\t\tfecha_final")
for folio, nota, fecha_actual, fecha_final in periodo:
    print(f"{folio: <5}\t\t{nota: <10}\t\t{fecha_actual.strftime('%d/%m/%Y'): <15}\t\t{fecha_final.strftime('%d/%m/%Y'): <15}")
