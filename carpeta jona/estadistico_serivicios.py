cantidad_servicios = int(input("Ingrese la cantidad de servicios más prestados a identificar (mínimo 1): "))
while cantidad_servicios < 1:
    cantidad_servicios = int(input("Por favor, ingrese un valor igual o mayor a 1: "))

fecha_inicial = input("Ingrese la fecha inicial del período a reportar (mm_dd_aaaa): ")
fecha_final = input("Ingrese la fecha final del período a reportar (mm_dd_aaaa): ")

query = '''
    SELECT Servicio, COUNT(*) as cantidad
    FROM services
    WHERE fecha_atencion BETWEEN ? AND ?
    GROUP BY nombre
    ORDER BY cantidad DESC
    LIMIT ?
'''

cursor.execute(query, (fecha_inicial, fecha_final, cantidad_servicios))
resultados = cursor.fetchall()

print("\nServicios más solicitados en el período:")
print("Nombre del Servicio\tCantidad")

for servicio, cantidad in resultados:
    print(f"{servicio}\t\t\t{cantidad}")

exportar_opcion = input("\n¿Desea exportar el informe a CSV? (Sí/No): ")

if exportar_opcion.lower() == "sí":
    nombre_archivo = f"ReporteServiciosMasPrestados_{fecha_inicial}_{fecha_final}.csv"
    with open(nombre_archivo, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Nombre del Servicio", "Cantidad"])
        csv_writer.writerows(resultados)

    print(f"El informe ha sido exportado como '{nombre_archivo}'.")

conn.close()