import pika
import json
import os
import re

# Configuración de los parámetros de conexión
url = 'amqps://kgyarjjq:raTNcH6iGe5_3I6zV5TBBsMtd97TWpyF@sparrow-01.rmq.cloudamqp.com/kgyarjjq'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declarar la cola (por si acaso)
channel.queue_declare(queue='ruc.queues', durable=True)

# Ruta del archivo JSON donde se almacenarán los RUCs y su estado
output_file = r'C:\BBF_SRI_BOT\BBF_SRI_BOT\orchestator\cola_rucs.json'


# Función para extraer el RUC del mensaje
def extraer_ruc(mensaje):
    # Ajustar la expresión regular para capturar el valor de "id" después de "i:"
    match = re.search(r'\\Ruc\\";s:\d+:\\\"id\\";i:(\d+)', mensaje)
    if match:
        return match.group(1)
    return None


# Función para guardar el RUC en un archivo JSON con su estado
def guardar_ruc_con_estado(ruc, estado="pendiente"):
    # Si el archivo existe, cargamos su contenido, sino, iniciamos un diccionario vacío
    if os.path.exists(output_file):
        with open(output_file, 'r') as file:
            try:
                datos = json.load(file)
                # Si los datos no son un diccionario, conviértelos a un diccionario vacío
                if not isinstance(datos, dict):
                    print("Advertencia: el archivo JSON no contiene un diccionario. Se sobrescribirá con uno nuevo.")
                    datos = {}
            except json.JSONDecodeError:
                print("Error al decodificar el archivo JSON. Se sobrescribirá con un diccionario vacío.")
                datos = {}
    else:
        datos = {}

    # Guardar o actualizar el RUC con su estado
    datos[ruc] = {"estado": estado}

    # Guardar el diccionario actualizado en el archivo
    with open(output_file, 'w') as file:
        json.dump(datos, file, indent=4)

    print(f"RUC {ruc} con estado '{estado}' añadido/actualizado en el archivo JSON.")


# Función callback para procesar los mensajes recibidos
def callback(ch, method, properties, body):
    print(f"Mensaje recibido: {body.decode()}")
    mensaje = body.decode()

    # Extraer el RUC del mensaje
    ruc = extraer_ruc(mensaje)
    if ruc:
        print(f"RUC extraído: {ruc}")
        # Guardar el RUC con su estado en el archivo JSON
        guardar_ruc_con_estado(ruc)
    else:
        print("No se pudo extraer el RUC del mensaje.")


# Configurar el consumidor para que escuche la cola indefinidamente
channel.basic_consume(queue='ruc.queues', on_message_callback=callback, auto_ack=True)

print('Esperando mensajes en la cola "ruc.queues". Presiona CTRL+C para salir.')

try:
    # Iniciar el consumo de mensajes
    channel.start_consuming()
except KeyboardInterrupt:
    print("Proceso interrumpido. Cerrando conexión...")
    channel.stop_consuming()
finally:
    connection.close()
