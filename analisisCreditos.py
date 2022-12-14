import pika
from sys import path
from os import environ
import django
from datetime import datetime

path.append('monitoring/settings.py')
environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring.settings')
django.setup()

from solicitud.services.services_solicitud import send_email


def main(queue='creditos'):
  rabbit_host = '10.128.0.6'
  rabbit_user = 'monitoring_user'
  rabbit_password = 'isis2503'

  connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_host,credentials=pika.PlainCredentials(rabbit_user, rabbit_password)))
  channel = connection.channel()
  channel.queue_declare(queue=queue)
  
  def callback(ch, method, properties, body):
    documentos = body.decode()
    respuesta = "No es aprobado"
    documentos = documentos.split(";")
    fecha_mes = (datetime.strptime(documentos[5], '%d/%m/%Y')).month not in range(9,11)

    if documentos[3] == "Apple":
      if int(documentos[1]) >= 2000000:
        if int(documentos[4]) >= 30:
          if fecha_mes == True:
            respuesta = "Aprobado"

    elif documentos[3] == "Facebook":
      if int(documentos[1]) >= 3000000:
        if int(documentos[4]) >= 30:
          if fecha_mes == True:
            respuesta = "Aprobado"

    elif documentos[3] == "Microsoft":
      if int(documentos[1]) >= 7000000:
        if int(documentos[4]) >= 30:
          if fecha_mes == True:
            respuesta = "Aprobado"

    print(respuesta)
    send_email(respuesta)

  channel.basic_consume(queue='creditos', on_message_callback=callback, auto_ack=True)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()
  


if __name__ == '__main__':
    main(queue='creditos')