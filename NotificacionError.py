import requests
import json

# URL del endpoint de la API de WhatsApp
url = "https://graph.facebook.com/v20.0/372456282623148/messages"

# Lista de números de teléfono
phone_numbers = [
    "593985628860",
    "593986170673"
]

# Base payload para enviar el mensaje con la plantilla y variables
base_payload = {
    "messaging_product": "whatsapp",
    "type": "template",
    "template": {
        "name": "comprobantes_error",  # Nombre de la plantilla
        "language": {
            "code": "es"  # Código del idioma (por ejemplo, "es" para español)
        },
        "components": [
            {
                "type": "header",
                "parameters": [
                    {
                        "type": "image",
                        "image": {
                            "link": "https://bbf.com.ec/wp-content/uploads/2024/08/Error.jpg"  # URL de la nueva imagen
                        }
                    }
                ]
            },
            {
                "type": "body",
                "parameters": [
                    {
                        "type": "text",
                        "text": "Error de conexión al servidor del SRI"  # Mensaje que reemplazará {{1}} en la plantilla
                    }
                ]
            }
        ]
    }
}

# Encabezados para la solicitud
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer EAAOhHDgcmAEBO8ltpzig0r97dn1k7cZCvfMKvC4hq9o3vbsaPXb3cNurVQZB2PrKp23bhn2IDxBhTXZAjlYtBTobM2zeyrYk3Iwr1rUgdIZBeY5sbB8eGmnvtjP7WZBgZCKCOgue5QaSKLMSEBVvzg3Odcn5JXBdWZCLrelx0ExvKlYnXWDZBuDIIoBLDayp31syQgZDZD'
}

# Enviar mensaje a cada número
for number in phone_numbers:
    # Clona el payload base para cada número
    payload = base_payload.copy()
    payload["to"] = number

    # Realiza la solicitud POST
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Imprime la respuesta
    print(f"Response for {number}: {response.text}")
