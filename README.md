# DatatonAnticorrupcion-IntegriDAT

## Miembros
Britany Castillo Sarmienta
Oscar García
Julian Preciado Verduzco
Marina Olvera Martínez

## Guia de ejecuccion

Descargar los archivos del s1, s3 y el s6 en root y extraerlos.
Ejecutar los archivos en el siguiente orden, programas con el mismo numero pueden ser corridos en paralelo:

1\. procesar_s1.ipynb  
1\. procesar_s6_pandas.ipynb  
2\. generar-periodos-invalidacion.ipynb  
2\. procesar_fechas_s6.ipynb  
2\. procesar_declaraciones.ipynb  
3\. cruzar_s1_s3.ipynb -> posesion_durante_inhabilitacion_IntegriDAT.xlsx  
3\. cruzar_s6_s3.ipynb -> contrato_durante_inhabilitacion_IntegriDAT.xlsx  

Despues de correr los archivos la estructura del directorio quedara parecido a esto, notece que las carpetas del S6, S1 y S3 tienen que ser extraidas previamente:

├───bulk-s6  
│  
├───s1  
│   
├───s3p  
│  
├───s3s    
contrato_durante_inhabilitacion_IntegriDAT.xlsx  
cruzar_s1_s3.ipynb  
cruzar_s6_s3.ipynb   
generar-periodos-invalidacion.ipynb  
inhabilitaciones.pkl  
posesion_durante_inhabilitacion_IntegriDAT.xlsx  
procesar_declaraciones.ipynb  
procesar_fechas_s6.ipynb  
procesar_s1.ipynb  
procesar_s6.ipynb  
procesar_s6_pandas.ipynb  
requirements.txt  
s1_declaracion.pkl  
s1_df_raw.pkl  
s1_fecha_toma_posesion.h5  
s6_hdf.h5  
s6_hdf_dates.h5  
s6_parquet.h5