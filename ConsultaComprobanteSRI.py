import requests
import pandas as pd
import xml.etree.ElementTree as ET
import os

# Ruta del archivo .txt que contiene los números de autorización
ruta_txt = r"C:\SRI_BBF_MASIVO\DOCUMENTOS\1792715075001_1_20240814.txt"

# Extraer el RUC del nombre del archivo .txt
ruc_emisor = os.path.basename(ruta_txt).split('_')[0]

# Ruta donde se guardará el archivo Excel con el nombre dinámico basado en el RUC
ruta_excel = fr"C:\SRI_BBF_MASIVO\REPORTE\{ruc_emisor}.xlsx"

# Función para leer los números de autorización desde el archivo .txt aplicando trim y omitiendo la primera fila (encabezado)
def leer_numeros_autorizacion(ruta_txt):
    try:
        with open(ruta_txt, "r") as file:
            # Leer todas las líneas omitiendo la primera fila (encabezado)
            lineas = file.readlines()[1:]

            # Extraer solo la clave de acceso desde cada línea
            claves_acceso = []
            for linea in lineas:
                elementos = linea.split()
                # Buscar el elemento que tenga 49 caracteres (longitud de la clave de acceso)
                for elemento in elementos:
                    if len(elemento) == 49 and elemento.isdigit():
                        claves_acceso.append(elemento.strip())
                        break

            return claves_acceso
    except Exception as e:
        print(f"Error al leer el archivo de números de autorización: {e}")
        return []

# Función para realizar la consulta al servicio web del SRI
def consultar_sri(clave_acceso):
    try:
        clave_acceso = clave_acceso.strip()  # Aplicar trim a la clave de acceso

        url = "https://cel.sri.gob.ec/comprobantes-electronicos-ws/AutorizacionComprobantesOffline"
        payload = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ec="http://ec.gob.sri.ws.autorizacion">
            <soapenv:Header/>
            <soapenv:Body>
                <ec:autorizacionComprobante>
                    <claveAccesoComprobante>{clave_acceso}</claveAccesoComprobante>
                </ec:autorizacionComprobante>
            </soapenv:Body>
        </soapenv:Envelope>"""

        headers = {
            'Content-Type': 'application/xml'
        }

        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud al SRI: {e}")
        return None

# Función para procesar la respuesta XML y extraer los datos relevantes
def procesar_respuesta_xml(xml_response, clave_acceso):
    try:
        if xml_response is None:
            return None

        # Eliminar las etiquetas SOAP envolventes
        start_tag = "<RespuestaAutorizacionComprobante>"
        end_tag = "</RespuestaAutorizacionComprobante>"
        if start_tag not in xml_response or end_tag not in xml_response:
            print("La estructura de la respuesta no es válida.")
            return None

        xml_data = xml_response.split(start_tag)[1].split(end_tag)[0]
        xml_data = f"{start_tag}{xml_data}{end_tag}"

        # Parsear la respuesta XML
        root = ET.fromstring(xml_data)

        # Extraer los valores de las etiquetas relevantes
        clave_acceso_consultada = root.find(".//claveAccesoConsultada").text if root.find(
            ".//claveAccesoConsultada") is not None else "N/A"
        estado = root.find(".//estado").text if root.find(".//estado") is not None else "N/A"
        mensaje = root.find(".//mensaje/mensaje").text if root.find(".//mensaje/mensaje") is not None else "N/A"
        informacion_adicional = root.find(".//mensaje/informacionAdicional").text if root.find(
            ".//mensaje/informacionAdicional") is not None else ""

        # Si hay un error en la estructura de la clave de acceso, dejar en blanco 'informacion_adicional'
        if "ERROR EN LA ESTRUCTURA DE LA CLAVE DE ACCESO" in mensaje:
            informacion_adicional = ""

        # Extraer valores adicionales como RAZON_SOCIAL_EMISOR, TIPO_COMPROBANTE, etc.
        razon_social_emisor = root.find(".//razonSocialEmisor").text if root.find(
            ".//razonSocialEmisor") is not None else "N/A"
        tipo_comprobante = root.find(".//tipoComprobante").text if root.find(
            ".//tipoComprobante") is not None else "N/A"
        serie_comprobante = root.find(".//serieComprobante").text if root.find(
            ".//serieComprobante") is not None else "N/A"
        fecha_autorizacion = root.find(".//fechaAutorizacion").text if root.find(
            ".//fechaAutorizacion") is not None else "N/A"
        fecha_emision = root.find(".//fechaEmision").text if root.find(".//fechaEmision") is not None else "N/A"
        identificacion_receptor = root.find(".//identificacionReceptor").text if root.find(
            ".//identificacionReceptor") is not None else "N/A"
        valor_sin_impuestos = root.find(".//valorSinImpuestos").text if root.find(
            ".//valorSinImpuestos") is not None else "N/A"
        iva = root.find(".//iva").text if root.find(".//iva") is not None else "N/A"
        importe_total = root.find(".//importeTotal").text if root.find(".//importeTotal") is not None else "N/A"
        numero_documento_modificado = root.find(".//numeroDocumentoModificado").text if root.find(
            ".//numeroDocumentoModificado") is not None else "N/A"

        # Estructurar los datos en columnas
        datos = {
            "RUC_EMISOR": ruc_emisor,
            "RAZON_SOCIAL_EMISOR": razon_social_emisor,
            "TIPO_COMPROBANTE": tipo_comprobante,
            "SERIE_COMPROBANTE": serie_comprobante,
            "CLAVE_ACCESO": clave_acceso_consultada,
            "FECHA_AUTORIZACION": fecha_autorizacion,
            "FECHA_EMISION": fecha_emision,
            "IDENTIFICACION_RECEPTOR": identificacion_receptor,
            "VALOR_SIN_IMPUESTOS": valor_sin_impuestos,
            "IVA": iva,
            "IMPORTE_TOTAL": importe_total,
            "NUMERO_DOCUMENTO_MODIFICADO": numero_documento_modificado,
            "ESTADO": estado,
            "MENSAJE": mensaje,
            "INFORMACION_ADICIONAL": informacion_adicional
        }
        return datos
    except ET.ParseError as e:
        print(f"Error al procesar el XML: {e}")
        return None

# Función para guardar los resultados en un archivo Excel fila por fila
def guardar_en_excel(resultados, ruta_excel):
    try:
        # Crear un DataFrame a partir de los resultados
        df = pd.DataFrame(resultados)
        # Guardar el DataFrame en un archivo Excel
        df.to_excel(ruta_excel, index=False)
    except Exception as e:
        print(f"Error al guardar los datos en Excel: {e}")

# Proceso principal
def main():
    try:
        numeros_autorizacion = leer_numeros_autorizacion(ruta_txt)
        if not numeros_autorizacion:
            print("No se encontraron números de autorización válidos.")
            return

        resultados = []
        for numero in numeros_autorizacion:
            print(f"Consultando clave de acceso: {numero}")
            respuesta_xml = consultar_sri(numero)
            datos = procesar_respuesta_xml(respuesta_xml, numero)
            if datos:
                resultados.append(datos)

        if resultados:
            guardar_en_excel(resultados, ruta_excel)
            print(f"Resultados guardados en: {ruta_excel}")
        else:
            print("No se obtuvieron resultados válidos para guardar.")

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
