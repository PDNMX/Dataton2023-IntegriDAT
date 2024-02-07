import os
import json
from dateutil.parser import parse, ParserError

# Carpeta base
carpeta_base = "../s1/"
carpeta_salida = "../paso_1_s1_salida/"
# Abrir el archivo de salida en modo de agregar
with open(carpeta_salida + "s1_fecha_toma_posesion.json", 'a') as f_out:
    # Agregar el corchete de apertura al inicio del archivo
    f_out.write("[\n")

    # Recorrer carpetas y archivos dentro de la carpeta base
    for directorio_actual, subdirectorios, archivos in os.walk(carpeta_base):
        for archivo_json in archivos:
            # Combinar la ruta del directorio actual con el nombre del archivo
            ruta_completa = os.path.join(directorio_actual, archivo_json)

            print(f"Procesando archivo: {ruta_completa}")

            with open(ruta_completa, 'r') as f:
                try:
                    # Cargar el archivo JSON como un diccionario
                    datos_json = json.load(f)

                    # Obtener el objeto "declaracion"
                    declaraciones = datos_json

                    # Procesar cada declaración
                    for declaracion in declaraciones:
                        nombre = declaracion.get("declaracion", {}).get("situacionPatrimonial", {}).get("datosGenerales", {}).get("nombre", "")
                        primer_apellido = declaracion.get("declaracion", {}).get("situacionPatrimonial", {}).get("datosGenerales", {}).get("primerApellido", "")
                        segundo_apellido = declaracion.get("declaracion", {}).get("situacionPatrimonial", {}).get("datosGenerales", {}).get("segundoApellido", "")

                        nivelOrdenGobierno = declaracion.get("declaracion", {}).get("situacionPatrimonial", {}).get("datosEmpleoCargoComision", {}).get("nivelOrdenGobierno", "")
                        nombreEntePublico = declaracion.get("declaracion", {}).get("situacionPatrimonial", {}).get("datosEmpleoCargoComision", {}).get("nombreEntePublico", "")
                        empleoCargoComision = declaracion.get("declaracion", {}).get("situacionPatrimonial", {}).get("datosEmpleoCargoComision", {}).get("empleoCargoComision", "")
                        claveEntidadFederativa = declaracion.get("declaracion", {}).get("situacionPatrimonial", {}).get("datosEmpleoCargoComision", {}).get("domicilioMexico", {}).get("entidadFederativa", {}).get("clave", "")
                        # Concatenar nombres y apellidos
                        nombre_declaracion = f"{nombre} {primer_apellido} {segundo_apellido}".lower().strip()
                        nombre_declaracion = nombre_declaracion.encode('ascii', 'ignore').decode('utf-8')

                        # Parsear fecha de toma de posesión
                        fecha_toma_posesion_str = declaracion.get("declaracion", {}).get("situacionPatrimonial", {}).get("datosEmpleoCargoComision", {}).get("fechaTomaPosesion", "")
                        try:
                            fecha_toma_posesion = parse(fecha_toma_posesion_str).strftime('%Y-%m-%d') if fecha_toma_posesion_str else None
                        except ParserError as e:
                            print(f"Error al parsear fecha en archivo {ruta_completa}: {e}")
                            fecha_toma_posesion = None
                        # Almacenar resultados
                        resultado = {
                            "nombre_declaracion": nombre_declaracion,
                            "fechaTomaPosesion": fecha_toma_posesion,
                            "nivelOrdenGobierno": nivelOrdenGobierno,
                            "nombreEntePublico": nombreEntePublico,
                            "empleoCargoComision": empleoCargoComision,
                            "claveEntidadFederativa": claveEntidadFederativa
                        }

                        # Escribir el resultado al archivo de salida
                        json.dump(resultado, f_out, default=str)
                        f_out.write(',\n')  # Agregar una coma y un salto de línea para separar los resultados

                except json.JSONDecodeError as e:
                    print(f"Error al decodificar JSON en archivo {ruta_completa}: {e}")

    # Retroceder para sobrescribir la última coma y agregar el corchete de cierre al final del archivo
    f_out.seek(f_out.tell() - 2, os.SEEK_SET)
    f_out.truncate()
    f_out.write("\n]\n")
print("Terminado paso 1 del s1")
print("Guardando archivo de salida")