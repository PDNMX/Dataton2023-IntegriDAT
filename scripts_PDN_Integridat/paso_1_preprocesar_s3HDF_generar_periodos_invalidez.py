import pandas as pd
import numpy as np
import os
import glob
import json
import datetime
from dateutil.parser import parse

def parse_date_safe(x):
    """Función para parsear fechas de forma segura"""
    try:
        if pd.isna(x) or x == "" or x is None:
            return None
        if isinstance(x, str) and x.strip() == "":
            return None
        parsed_date = parse(x)
        return parsed_date.strftime('%Y-%m-%d')
    except:
        return None

def safe_json_normalize(data, default_columns=None):
    """Función para normalizar JSON de forma segura"""
    if data is None or (isinstance(data, list) and len(data) == 0):
        if default_columns:
            return pd.DataFrame(columns=default_columns)
        return pd.DataFrame()
    
    try:
        return pd.json_normalize(data)
    except Exception as e:
        print(f"Error en json_normalize: {e}")
        if default_columns:
            return pd.DataFrame(columns=default_columns)
        return pd.DataFrame()

def extract_puesto(sancionado):
    if 'puesto' in sancionado:
        return sancionado['puesto']
    elif 'nombreRazonSocial' in sancionado:
        return "No especificado para particulares"
    else:
        return ""

def process_s3p_file(file_path):
    try:
        print(f"Procesando archivo s3p: {file_path}")
        
        # Leer archivo JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print(f"Archivo vacío: {file_path}")
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        print(f"Registros leídos en s3p: {len(df)}")
        
        # Procesar particularSancionado
        if 'particularSancionado' in df.columns:
            sancionados = safe_json_normalize(df.particularSancionado, 
                                            default_columns=['nombreRazonSocial'])
            df["sancion_nombre"] = sancionados.get('nombreRazonSocial', '')
        else:
            df["sancion_nombre"] = ''
        
        # Procesar inhabilitacion - ENFOQUE SEGURO
        df["inhabilitacion_fechaInicial"] = ''
        df["inhabilitacion_fechaFinal"] = ''
        
        if 'inhabilitacion' in df.columns:
            inhabilitacion = safe_json_normalize(df.inhabilitacion, 
                                               default_columns=['fechaInicial', 'fechaFinal'])
            
            # Procesar fechaInicial de forma segura
            if 'fechaInicial' in inhabilitacion.columns:
                fechas_iniciales = []
                for fecha in inhabilitacion['fechaInicial']:
                    fecha_parseada = parse_date_safe(fecha)
                    fechas_iniciales.append(fecha_parseada if fecha_parseada else '')
                df["inhabilitacion_fechaInicial"] = fechas_iniciales
            
            # Procesar fechaFinal de forma segura
            if 'fechaFinal' in inhabilitacion.columns:
                fechas_finales = []
                for fecha in inhabilitacion['fechaFinal']:
                    fecha_parseada = parse_date_safe(fecha)
                    fechas_finales.append(fecha_parseada if fecha_parseada else '')
                df["inhabilitacion_fechaFinal"] = fechas_finales
        
        # Normalizar sancion_nombre
        if 'sancion_nombre' in df.columns:
            df["sancion_nombre"] = df["sancion_nombre"].astype(str).str.lower()
            df["sancion_nombre"] = df["sancion_nombre"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        
        # Procesar campos adicionales
        df["institucion_dependencia"] = df["institucionDependencia"].apply(lambda x: x.get("nombre", "") if isinstance(x, dict) else "")
        df["autoridad_sancionadora"] = df.get("autoridadSancionadora", "")
        df["causa_motivo_hechos"] = df.get("causaMotivoHechos", "")
        
        # Agregar una columna 'puesto' con un valor predeterminado para particulares
        df["puesto"] = "No especificado para particulares"
        
        # Procesar tipoFalta - en s3p es string directo
        if 'tipoFalta' not in df.columns:
            df['tipoFalta'] = ''
        
        # Procesar expediente
        if 'expediente' not in df.columns:
            df['expediente'] = ''
        
        # Seleccionar columnas
        columnas = ["tipoFalta", "expediente", "sancion_nombre", "inhabilitacion_fechaInicial","inhabilitacion_fechaFinal", "puesto", "institucion_dependencia", "autoridad_sancionadora", "causa_motivo_hechos"]
        
        # Asegurar que todas las columnas existen
        for col in columnas:
            if col not in df.columns:
                df[col] = ''
        
        df = df[columnas]
        df["tipo_persona"] = "particular"
        
        print(f"Registros procesados exitosamente en s3p: {len(df)}")
        return df
        
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

def process_s3s_file(file_path):
    try:
        print(f"Procesando archivo s3s: {file_path}")
        
        # Leer archivo JSON
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print(f"Archivo vacío: {file_path}")
            return pd.DataFrame()
        
        df = pd.DataFrame(data)
        print(f"Registros leídos en s3s: {len(df)}")
        
        # Procesar servidorPublicoSancionado
        if 'servidorPublicoSancionado' in df.columns:
            servidorPublicoSancionado = safe_json_normalize(df.servidorPublicoSancionado, default_columns=['nombres', 'primerApellido', 'segundoApellido', 'puesto'])
            
            # Llenar valores nulos
            for col in ['nombres', 'primerApellido', 'segundoApellido']:
                if col not in servidorPublicoSancionado.columns:
                    servidorPublicoSancionado[col] = ''
                else:
                    servidorPublicoSancionado[col] = servidorPublicoSancionado[col].fillna('')
            
            # Construir nombre completo
            servidorPublicoSancionado["nombre"] = (
                servidorPublicoSancionado['nombres'].astype(str) + " " + 
                servidorPublicoSancionado['primerApellido'].astype(str) + " " + 
                servidorPublicoSancionado['segundoApellido'].astype(str)
            )
            servidorPublicoSancionado["nombre"] = servidorPublicoSancionado["nombre"].str.lower().str.strip()
            servidorPublicoSancionado["nombre"] = servidorPublicoSancionado["nombre"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
            
            df["sancion_nombre"] = servidorPublicoSancionado["nombre"]
            
            # Procesar puesto del servidor público
            if 'puesto' in servidorPublicoSancionado.columns:
                df["puesto"] = servidorPublicoSancionado["puesto"].fillna('Puesto no especificado')
            else:
                df["puesto"] = 'Puesto no especificado'
        else:
            df["sancion_nombre"] = ''
            df["puesto"] = 'Puesto no especificado'
        
        # Procesar campos adicionales
        df["institucion_dependencia"] = df["institucionDependencia"].apply(lambda x: x.get("nombre", "") if isinstance(x, dict) else "")
        df["autoridad_sancionadora"] = df.get("autoridadSancionadora", "")
        df["causa_motivo_hechos"] = df.get("causaMotivoHechos", "")
        
        # Procesar inhabilitacion - ENFOQUE SEGURO
        df["inhabilitacion_fechaInicial"] = ''
        df["inhabilitacion_fechaFinal"] = ''
        
        if 'inhabilitacion' in df.columns:
            inhabilitacion_servidor = safe_json_normalize(df.inhabilitacion,
                                                        default_columns=['fechaInicial', 'fechaFinal'])
            
            # Procesar fechaInicial de forma segura
            if 'fechaInicial' in inhabilitacion_servidor.columns:
                fechas_iniciales = []
                for fecha in inhabilitacion_servidor['fechaInicial']:
                    fecha_parseada = parse_date_safe(fecha)
                    fechas_iniciales.append(fecha_parseada if fecha_parseada else '')
                df["inhabilitacion_fechaInicial"] = fechas_iniciales
            
            # Procesar fechaFinal de forma segura
            if 'fechaFinal' in inhabilitacion_servidor.columns:
                fechas_finales = []
                for fecha in inhabilitacion_servidor['fechaFinal']:
                    fecha_parseada = parse_date_safe(fecha)
                    fechas_finales.append(fecha_parseada if fecha_parseada else '')
                df["inhabilitacion_fechaFinal"] = fechas_finales
        
        # Procesar tipoFalta - en s3s es objeto con clave y valor
        if 'tipoFalta' in df.columns:
            tipoFalta = safe_json_normalize(df.tipoFalta, default_columns=['valor'])
            if 'valor' in tipoFalta.columns:
                df["tipoFalta"] = tipoFalta['valor']
            else:
                df["tipoFalta"] = ''
        else:
            df["tipoFalta"] = ''
        
        # Procesar expediente
        if 'expediente' not in df.columns:
            df['expediente'] = ''
        
        # Seleccionar columnas
        columnas = ["tipoFalta", "expediente", "sancion_nombre", "inhabilitacion_fechaInicial","inhabilitacion_fechaFinal", "puesto", "institucion_dependencia", "autoridad_sancionadora", "causa_motivo_hechos"]
        
        # Asegurar que todas las columnas existen
        for col in columnas:
            if col not in df.columns:
                df[col] = ''
        
        df = df[columnas]
        df["tipo_persona"] = "servidor_publico"
        
        print(f"Registros procesados exitosamente en s3s: {len(df)}")
        return df
        
    except Exception as e:
        print(f"Error al procesar {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

def main():
    # Directorios base - ACTUALIZADOS para tu estructura
    base_s3p = "/home/phoenix/sesna/desarrollo/otros/bulk_datos_sergio_09_07_2025/s3/s3p/"
    base_s3s = "/home/phoenix/sesna/desarrollo/otros/bulk_datos_sergio_09_07_2025/s3/s3s/"
    
    # Verificar que los directorios existen
    if not os.path.exists(base_s3p):
        print(f"Directorio s3p no existe: {base_s3p}")
        return
    
    if not os.path.exists(base_s3s):
        print(f"Directorio s3s no existe: {base_s3s}")
        return
    
    # Obtener archivos JSON directamente de las carpetas base
    try:
        all_files_s3p = glob.glob(os.path.join(base_s3p, "*.json"))
        all_files_s3s = glob.glob(os.path.join(base_s3s, "*.json"))
    except Exception as e:
        print(f"Error al buscar archivos JSON: {e}")
        return
    
    print(f"Archivos JSON s3p encontrados: {len(all_files_s3p)}")
    print(f"Archivos JSON s3s encontrados: {len(all_files_s3s)}")
    
    # Mostrar archivos encontrados
    if all_files_s3p:
        print("Archivos s3p:")
        for file_path in all_files_s3p:
            print(f"  - {file_path}")
    
    if all_files_s3s:
        print("Archivos s3s:")
        for file_path in all_files_s3s:
            print(f"  - {file_path}")
    
    # Inicializar listas para almacenar los DataFrames
    s3p_dfs = []
    s3s_dfs = []
    
    # Procesar archivos s3p
    print("\n=== PROCESANDO ARCHIVOS S3P ===")
    for file_path in all_files_s3p:
        print(f"Procesando archivo s3p: {file_path}")
        try:
            df = process_s3p_file(file_path)
            if not df.empty:
                s3p_dfs.append(df)
                print(f"Procesado exitosamente: {file_path} ({len(df)} registros)")
            else:
                print(f"Archivo vacío o sin datos válidos: {file_path}")
        except Exception as e:
            print(f"Error al procesar archivo s3p {file_path}: {e}")
    
    # Procesar archivos s3s
    print("\n=== PROCESANDO ARCHIVOS S3S ===")
    for file_path in all_files_s3s:
        print(f"Procesando archivo s3s: {file_path}")
        try:
            df = process_s3s_file(file_path)
            if not df.empty:
                s3s_dfs.append(df)
                print(f"Procesado exitosamente: {file_path} ({len(df)} registros)")
            else:
                print(f"Archivo vacío o sin datos válidos: {file_path}")
        except Exception as e:
            print(f"Error al procesar archivo s3s {file_path}: {e}")
    
    # Concatenar todos los DataFrames
    print("\n=== CONCATENANDO RESULTADOS ===")
    
    all_dfs = []
    
    if s3p_dfs:
        print(f"Concatenando {len(s3p_dfs)} DataFrames de s3p")
        all_dfs.extend(s3p_dfs)
        total_s3p = sum(len(df) for df in s3p_dfs)
        print(f"Total registros s3p: {total_s3p}")
    else:
        print("No se encontraron datos s3p")
    
    if s3s_dfs:
        print(f"Concatenando {len(s3s_dfs)} DataFrames de s3s")
        all_dfs.extend(s3s_dfs)
        total_s3s = sum(len(df) for df in s3s_dfs)
        print(f"Total registros s3s: {total_s3s}")
    else:
        print("No se encontraron datos s3s")
    
    # Combinar todos los DataFrames
    if all_dfs:
        combined_df = pd.concat(all_dfs, ignore_index=True)
        print(f"Total registros combinados: {len(combined_df)}")
    else:
        print("No se encontraron datos para procesar")
        return
    
    # Crear directorio de salida si no existe
    salida_paso1_preprocesar_s3_generar_periodods_invalidez = "/home/phoenix/sesna/desarrollo/otros/bulk_datos_sergio_09_07_2025/cruces_integridat/paso_1_preprocesar_s3HDF_generar_periodos_invalidez/"
    os.makedirs(salida_paso1_preprocesar_s3_generar_periodods_invalidez, exist_ok=True)
    
    # Guardar el DataFrame combinado en múltiples formatos
    try:
        # JSON
        json_file = salida_paso1_preprocesar_s3_generar_periodods_invalidez + "inhabilitaciones.json"
        combined_df.to_json(json_file, orient="records", indent=2)
        print(f"Archivo JSON guardado: {json_file}")
        
        # HDF5
        h5_file = salida_paso1_preprocesar_s3_generar_periodods_invalidez + "inhabilitaciones.h5"
        combined_df.to_hdf(h5_file, key="inhabilitaciones", mode="w")
        print(f"Archivo HDF5 guardado: {h5_file}")
        
        # CSV
        csv_file = salida_paso1_preprocesar_s3_generar_periodods_invalidez + "inhabilitaciones.csv"
        combined_df.to_csv(csv_file, index=False)
        print(f"Archivo CSV guardado: {csv_file}")
        
        print("Se ha creado un archivo a partir de combined_df")
        
    except Exception as e:
        print(f"Error al guardar archivos: {e}")
        import traceback
        traceback.print_exc()
    
    # Mostrar resumen final
    print("\n=== RESUMEN FINAL ===")
    total_s3p = len([df for df in all_dfs if not df.empty and df.iloc[0]['tipo_persona'] == 'particular']) if all_dfs else 0
    total_s3s = len([df for df in all_dfs if not df.empty and df.iloc[0]['tipo_persona'] == 'servidor_publico']) if all_dfs else 0
    
    print(f"DataFrames de particulares procesados: {len(s3p_dfs)}")
    print(f"DataFrames de servidores públicos procesados: {len(s3s_dfs)}")
    print(f"Total de registros: {len(combined_df)}")
    print(f"Columnas finales: {list(combined_df.columns)}")
    print("Fin del programa paso_1_preprocesar_s3HDF_generar_periodos_invalidez.py")

if __name__ == "__main__":
    main()