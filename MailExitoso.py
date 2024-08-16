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
subject = 'Documentos del SRI descargados con éxito'

# Descargar la imagen
image_url = 'https://bbf.com.ec/wp-content/uploads/2024/08/Descarga_Completa.jpg'
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
    <p>Hola, Soraya Valenzuela.</p>
    <p>Los documentos del SRI solicitados, han sido descargados con éxito.</p>
    <p>Revísalo en: <a href="https://bbf.com.ec/">https://bbf.com.ec/</a></p>
    <p>Por favor, no responda a este mensaje, ha sido enviado de forma automática.</p>
    <p>TYGOR BOT</p>
    <img src="data:image/jpeg;base64,{img_base64}" alt="Imagen de descarga"/>
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
    print('Correo enviado con éxito.')
except Exception as e:
    print(f'Error al enviar el correo: {e}')
