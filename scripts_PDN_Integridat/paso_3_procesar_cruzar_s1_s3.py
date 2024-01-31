import pandas as pd
import json
from dateutil.parser import parse

def eliminar_duplicados(df):
    # Eliminar duplicados basados en todas las columnas
    df_sin_duplicados = df.drop_duplicates()
    return df_sin_duplicados

# Leer el archivo JSON con el nuevo formato de fecha
with open("s1_fecha_toma_posesion.json", 'r') as f:
    # Cargar el contenido del archivo JSON
    datos_json_s1 = json.load(f)

# Convertir el JSON en un DataFrame de pandas
s1_posesion = pd.DataFrame(datos_json_s1)

# Leer el archivo JSON con el nuevo formato de fecha
with open("inhabilitaciones.json", 'r') as f:
    # Cargar el contenido del archivo JSON
    datos_json_inhab = json.load(f)

# Convertir el JSON en un DataFrame de pandas
inhabilitaciones = pd.DataFrame(datos_json_inhab)

# Realizar la fusión de los dataframes
df = s1_posesion.merge(inhabilitaciones, left_on="nombre_declaracion", right_on="sancion_nombre", how="inner", suffixes=("_s1", "_inhab"))

# Convertir las columnas de fecha a tipo date
df['fechaTomaPosesion'] = pd.to_datetime(df['fechaTomaPosesion'], errors='coerce').dt.strftime('%Y-%m-%d')
df['inhabilitacion_fechaInicial'] = pd.to_datetime(df['inhabilitacion_fechaInicial'], errors='coerce').dt.strftime('%Y-%m-%d')
df['inhabilitacion_fechaFinal'] = pd.to_datetime(df['inhabilitacion_fechaFinal'], errors='coerce').dt.strftime('%Y-%m-%d')

# Crear una columna que indica si la posesión ocurrió durante la inhabilitación
df["posesion_durante_inhabilitacion"] = df['fechaTomaPosesion'].between(df['inhabilitacion_fechaInicial'], df['inhabilitacion_fechaFinal'])

# Eliminar duplicados
df_sin_duplicados = eliminar_duplicados(df)

# Filtrar los resultados con "true" en la columna "posesion_durante_inhabilitacion"
df_final = df_sin_duplicados[df_sin_duplicados['posesion_durante_inhabilitacion']]

# Seleccionar columnas relevantes
columnas_orden = ['nombre_declaracion', 'tipoFalta', 'tipo_persona', 'nivelOrdenGobierno', 'nombreEntePublico', 'empleoCargoComision', 'claveEntidadFederativa', 'expediente', 'fechaTomaPosesion', 
       'inhabilitacion_fechaInicial', 'inhabilitacion_fechaFinal', 'posesion_durante_inhabilitacion']
df_final = df_final[columnas_orden]

# Guardar el resultado en un archivo JSON
df_final.to_json("resultado_posesion_inhabilitacion.json", orient="records")
