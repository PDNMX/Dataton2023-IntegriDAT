# DatatonAnticorrupcion-IntegriDAT

## Miembros
Britany Castillo Sarmienta
Oscar García
Julian Preciado Verduzco
Marina Olvera Martínez

## Guia de ejecuccion

Descargar los archivos del s1, s3 y el s6 con el botón de "Descarga todos los datos" en root y extraerlos.
Ejecutar los archivos en el siguiente orden, programas con el mismo número pueden ser corridos en paralelo:

1\. procesar_s1.ipynb  
1\. procesar_s6_pandas.ipynb  
2\. generar-periodos-invalidacion.ipynb  
2\. procesar_fechas_s6.ipynb  
2\. procesar_declaraciones.ipynb  
3\. cruzar_s1_s3.ipynb -> posesion_durante_inhabilitacion_IntegriDAT.xlsx  
3\. cruzar_s6_s3.ipynb -> contrato_durante_inhabilitacion_IntegriDAT.xlsx  

Después de correr los archivos la estructura del directorio quedara parecido a esto, note que las carpetas del S6, S1 y S3 tienen que ser extraídas previamente:

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

## Reportes generados

Después de ejecutar los archivos de python se generan los siguientes reportes con posibles casos de corrupción indebida.
Se pueden encontrar en Drive con su diccionario de datos en una de las hojas.

### posesion_durante_inhabilitacion_IntegriDAT.xlsx

<google-sheets-html-origin style="color: rgb(0, 0, 0);"><table xmlns="http://www.w3.org/1999/xhtml" cellspacing="0" cellpadding="0" dir="ltr" border="1" data-sheets-root="1" style="table-layout: fixed; font-size: 11pt; font-family: Calibri; width: 0px; border-collapse: collapse; border: none;">
  <thead>
    <tr style="height: 20px;">
      <th>Columna</th>
      <th>Proviene</th>
      <th>Explicacion</th>
    </tr>
  </thead><colgroup><col width="203"><col width="100"><col width="931"></colgroup>
  <tbody>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;nombre_declaracion&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">nombre_declaracion</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S1/S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S1/S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;El nombre en su declaración, ya fue cruzada con el S3. Considere que durante el cruzamiento el sujeto encontrado puede ser un homónimo&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">El nombre en su declaración, ya fue cruzada con el S3. Considere que durante el cruzamiento el sujeto encontrado puede ser un homónimo</td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;id&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">id</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;id de el registro de inhabilitacion, usada para identificar exactamente el documento de inhabilitacion en S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">id de el registro de inhabilitacion, usada para identificar exactamente el documento de inhabilitacion en S3</td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;expediente&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">expediente</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;El identificador del expediente de inhabilitacion, usada para identificar exactamente el documento de inhabilitacion en S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom; background-color: rgb(255, 255, 255);">El identificador del expediente de inhabilitacion, usada para identificar exactamente el documento de inhabilitacion en S3</td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;fechaTomaPosesion&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">fechaTomaPosesion</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S1&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S1</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;La fecha de toma de posesión segun la declaración&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">La fecha de toma de posesión segun la declaración</td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;inhabilitacion_fechaInicial&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">inhabilitacion_fechaInicial</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;La fecha inicial en el que el funcionario es inhabilitado&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">La fecha inicial en el que el funcionario es inhabilitado</td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;inhabilitacion_fechaFinal&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">inhabilitacion_fechaFinal</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;La fecha final en el que el funcionario estara inhabilitado&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">La fecha final en el que el funcionario estara inhabilitado</td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;posesion_durante_inhabilitacion&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">posesion_durante_inhabilitacion</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Generado&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">Generado</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Si la fecha de toma de posesión se encuentra entre la inhabilitación, solo se presentan los casos positivos marcados con 1&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">Si la fecha de toma de posesión se encuentra entre la inhabilitación, solo se presentan los casos positivos marcados con 1</td>
    </tr>
  </tbody>
</table></google-sheets-html-origin>

### contrato_durante_inhabilitacion_IntegriDAT.xlsx 

<google-sheets-html-origin><table xmlns="http://www.w3.org/1999/xhtml" cellspacing="0" cellpadding="0" dir="ltr" border="1" data-sheets-root="1" style="table-layout: fixed; font-size: 11pt; font-family: Calibri; width: 0px; border-collapse: collapse; border: none;">
  <thead>
    <tr style="height: 20px;">
      <th>Columna</th>
      <th>Proviene</th>
      <th>Explicacion</th>
      <th>Nota</th>
    </tr>
  </thead><colgroup><col width="247"><col width="100"><col width="1014"><col width="843"></colgroup>
  <tbody>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;sancion_tipoPersona&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">sancion_tipoPersona</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Si el sujeto encontrado es una persona física o moral de acuerdo al S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">Si el sujeto encontrado es una persona física o moral de acuerdo al S3</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;sancion_objetoSocial&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">sancion_objetoSocial</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;El objeto social de el sujeto encontrado de acuerdo al S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">El objeto social de el sujeto encontrado de acuerdo al S3</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;inhabilitacion_fechaInicial&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">inhabilitacion_fechaInicial</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;La fecha inicial en el que el funcionario es inhabilitado&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">La fecha inicial en el que el funcionario es inhabilitado</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;inhabilitacion_fechaFinal&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">inhabilitacion_fechaFinal</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;La fecha final en el que el funcionario estara inhabilitado&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">La fecha final en el que el funcionario estará inhabilitado</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;earliest_contractPeriod_startDate&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">earliest_contractPeriod_startDate</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S6&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S6</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;La fecha mas antigua de todas las encontradas en el apartado de contractPeriod&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">La fecha mas antigua de todas las encontradas en el apartado de contractPeriod</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;latest_contractPeriod_endDate&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">latest_contractPeriod_endDate</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S6&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S6</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;La fecha mas reciente de todas las encontradas en el apartado de contractPeriod&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom; background-color: rgb(255, 255, 255);">La fecha mas reciente de todas las encontradas en el apartado de contractPeriod</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;parties_name&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">parties_name</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S6/S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S6/S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;El nombre de una de las partes en la declaración, puede ser persona física o moral.  Considere que durante el cruzamiento el sujeto encontrado puede ser un homónimo.&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">El nombre de una de las partes en la declaración, puede ser persona física o moral. Considere que durante el cruzamiento el sujeto encontrado puede ser un homónimo.</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Los datos presentados requieren un cruce al menos uno de parties_name o con parties_contactPoint_name con el nombre encontrado en S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">Los datos presentados requieren un cruce al menos uno de parties_name o con parties_contactPoint_name con el nombre encontrado en S3</td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;parties_contactPoint_name&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">parties_contactPoint_name</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S6/S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S6/S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;El nombre de contacto de una de las partes en la declaración.  Considere que durante el cruzamiento el sujeto encontrado puede ser un homónimo.&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">El nombre de contacto de una de las partes en la declaración. Considere que durante el cruzamiento el sujeto encontrado puede ser un homónimo.</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Considere que durante el cruzamiento el sujeto encontrado puede ser un homónimo&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom; background-color: rgb(255, 255, 255);">Considere que durante el cruzamiento el sujeto encontrado puede ser un homónimo</td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;ids3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">ids3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;id de el registro de inhabilitacion, usada para identificar exactamente el documento de inhabilitacion en S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom; background-color: rgb(255, 255, 255);">id de el registro de inhabilitacion, usada para identificar exactamente el documento de inhabilitacion en S3</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;expediente&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">expediente</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S3</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;El identificador del expediente de inhabilitacion, usada para identificar exactamente el documento de inhabilitacion en S3&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom; background-color: rgb(255, 255, 255);">El identificador del expediente de inhabilitacion, usada para identificar exactamente el documento de inhabilitacion en S3</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;_id.$oid&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">_id.$oid</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S6&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S6</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Identificador en el archivo de la contratación, usada para identificar exactamente el documento de la contratación&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">Identificador en el archivo de la contratación, usada para identificar exactamente el documento de la contratación</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;ocid&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">ocid</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S6&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S6</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Identificador en el archivo de la contratación, usada para identificar exactamente el documento de la contratación&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom; background-color: rgb(255, 255, 255);">Identificador en el archivo de la contratación, usada para identificar exactamente el documento de la contratación</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;ids6&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">ids6</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;S6&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;">S6</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Identificador en el archivo de la contratación, usada para identificar exactamente el documento de la contratación&quot;}" style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom; background-color: rgb(255, 255, 255);">Identificador en el archivo de la contratación, usada para identificar exactamente el documento de la contratación</td>
      <td style="border: 1px solid rgb(204, 204, 204); overflow: hidden; padding: 0px 3px; vertical-align: bottom;"></td>
    </tr>
    <tr style="height: 20px;">
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;contrato_durante_inhabilitacion&quot;}" style="border: 1px solid rgb(204, 204, 204); color: rgb(0, 0, 0); font-size: 14.6667px; overflow: hidden; padding: 0px 3px; vertical-align: bottom;">contrato_durante_inhabilitacion</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Generado&quot;}" style="border: 1px solid rgb(204, 204, 204); color: rgb(0, 0, 0); font-size: 14.6667px; overflow: hidden; padding: 0px 3px; vertical-align: bottom;">Generado</td>
      <td data-sheets-value="{&quot;1&quot;:2,&quot;2&quot;:&quot;Si el periodo del contrato se cruza con el periodo de inhabilitación, solo se presentan los casos positivos marcados con 1&quot;}" style="border: 1px solid rgb(204, 204, 204); color: rgb(0, 0, 0); font-size: 14.6667px; overflow: hidden; padding: 0px 3px; vertical-align: bottom; background-color: rgb(255, 255, 255);">Si el periodo del contrato se cruza con el periodo de inhabilitación, solo se presentan los casos positivos marcados con 1</td>
    </tr>
  </tbody>
</table></google-sheets-html-origin>