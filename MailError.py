import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import requests
from io import BytesIO
import base64

# Configuración de los datos del servidor
smtp_server = 'smtp.bbf.com.ec'
smtp_port = 465
smtp_user = 'tygor@bbf.com.ec'
smtp_password = 'Tygor2024--'

# Configuración del mensaje
from_addr = 'tygor@bbf.com.ec'
to_addr = 'jeff.guillen@bbf.com.ec'  # Cambia esto por la dirección del destinatario
subject = 'Error en la descarga de comprobantes'

# Descargar la imagen de error
image_url = 'https://bbf.com.ec/wp-content/uploads/2024/08/Error.jpg'
response = requests.get(image_url)
img_data = BytesIO(response.content)
img_base64 = base64.b64encode(img_data.getvalue()).decode('utf-8')

# Crear el mensaje
msg = MIMEMultipart('related')
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = subject

# Crear el cuerpo del mensaje en HTML
html_body = f"""\
<html>
  <body>
    <p>Ha ocurrido un error en la descarga de los comprobantes.</p>
    <p>Causa Error: Portal SRI caído</p>
    <p>Se agenda el correspondiente reintento.</p>
    <img src="data:image/jpeg;base64,{img_base64}" alt="Error Image"/>
  </body>
</html>
"""

# Añadir el cuerpo del mensaje en HTML
msg.attach(MIMEText(html_body, 'html'))

# Enviar el correo
try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
    print('Correo de error enviado con éxito.')
except Exception as e:
    print(f'Error al enviar el correo de error: {e}')
