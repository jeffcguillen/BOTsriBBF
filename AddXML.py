import boto3
from botocore.client import Config

# Configurar la conexión a DigitalOcean Spaces
client = boto3.client('s3',
                      region_name='nyc3',
                      endpoint_url='https://nyc3.digitaloceanspaces.com',
                      aws_access_key_id='DO0074HHRXH6QF24YYJG',  # Reemplaza con tu clave de acceso
                      aws_secret_access_key='BRFKm5UxevpbSoKDv2foxVCOKXuT5zll1wVCjM4s4QY')  # Reemplaza con tu clave secreta

# Ruta local del archivo que deseas subir
local_file_path = r"C:\BBF_SRI_BOT\BBF_SRI_BOT\docs\1790683486001\1790683486001_1_20240815.txt"

# Nombre del espacio y ruta de destino en el espacio
space_name = 'tygor-bots'
destination_path = 'BBF_SRI_BOT/BBF_SRI_BOT/docs/1790683486001/1790683486001_1_20240815.txt'

# Subir el archivo al espacio
client.upload_file(local_file_path, space_name, destination_path)

print(f"Archivo subido exitosamente a: {destination_path}")
