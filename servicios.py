import pandas as pd

"""
2.3. Menú Servicios

2.3.1. Agregar un servicio: En esta opción se podrán dar de alta nuevos servicios a ofrecer en el taller y contarán con el siguiente detalle:
Una clave única para cada servicio que debe ser generada automáticamente, 
el nombre que describe al servicio (No puede quedar vacío) y el costo (Debe ser superior a 0.00) que dicho servicio tiene; 
si algún dato proporcionado no cumple con las condciones indicadas no se le debe permitir al usuario al siguiente paso.

"""
serv_list = []
serv_dic = {}

def NUEVO_SERVICIO():
    nombre_servicio = input('INGRESA EL SERVICIO:\n')
    costo_servicio = int(input('INGRESA EL COSTO DEL SERIVICIO:\n'))
    serv_list.append((nombre_servicio, costo_servicio))
    for clave, servicio in enumerate(serv_list, start=1):
        serv_dic[clave] = servicio

def CREADOR_DF(diccionario):
    diccionario_pds = [(key, value[0]) for key, value in diccionario.items()]
    serv_pd = pd.DataFrame(diccionario_pds, columns=["CLAVE", "SERVICIO"])
    serv_pd.index = ['']
"""
2.3.2. Consultas y reportes de servicios
"""

"""
2.3.2.1. Búsqueda por clave de servicio: Se le presentará al usuario un listado tabular en pantalla formado los datos de clave y nombre de 
servicio de donde el usuario elegirá una de las claves presentadas y como consecuencia se le informará el detalle del servicio asociado con 
esa clave.
"""
def CONSULTA_CLAVES(dataframe):
    print(dataframe)



"""
2.3.2.2. Búsqueda por nombre de servicio: Se le solicitará al usuario el nombre del servicio a buscar y se le responderá con un reporte que 
muestre el detalle del servicio que cuyo nombre coincida con el dato proporcionado por el usuario, 
se debe ignorar la diferencia entre mayúsculas y minúsculas para efectos de la búsqueda correspondiente.

2.3.2.3. Listado de servicios
2.3.2.3.1. Ordenado por clave: Se le presentará al usuario un reporte tabular de todos los servicios registrados que contenga todos los 
detalles de estos ordenado por la clave de servicio. Después de desplegar el reporte en pantalla se le debe ofrecer la opción al usuario de 
exportar este resultado a CSV, Excel o regresar al menú de reportes. 
Si el usuario indica que desea exportar el reporte a cualquiera de los formatos ofrecidos este se debe guardar con un nombre de archivo 
conformado por el siguiente patrón ReporteServiciosPorClave_FechaDelReporte donde: 
*FechaDelReporte = La fecha en que se está emitiendo el reporte, en formato mm_dd_aaaa

2.3.2.3.2. Ordenado por nombre de servicio: Se le presentará al usuario un reporte tabular de todos los servicios registrados que contenga
todos los detalles de estos ordenado por el nombre del servicio. Después de desplegar el reporte en pantalla se le debe ofrecer la opción al
usuario de exportar este resultado a CSV, Excel o regresar al menú de reportes. Si el usuario indica que desea exportar el reporte a 
cualquiera de los formatos ofrecidos este se debe guardar con un nombre de archivo conformado por el siguiente patrón 
ReporteServiciosPorNombre_FechaDelReporte donde: *FechaDelReporte = La fecha en que se está emitiendo el reporte, en formato mm_dd_aaaa

2.3.2.3.3. Volver al menú anterior
2.3.2.4. Volver al menú de clientes
2.3.3. Volver al menú principal

2.4. Salir: Se le debe pedir al usuario la confirmación para salir de la solución; si la confirma se procede a salir, 
de lo contrario se le presentará el menú principal.
"""