
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def enviar_correo_contacto(nombre, correo, mensaje):
    email = EmailMessage()
    email["Subject"] = f"📨 Nuevo mensaje de contacto — Los Santos Customs Taller"
    email["From"]    = os.getenv("MAIL_USER")
    email["To"]      = os.getenv("MAIL_TO", os.getenv("MAIL_USER"))

    email.set_content(f"""\
Nuevo mensaje recibido desde el sistema Los Santos Customs.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DATOS DEL CLIENTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nombre:  {nombre}
Correo:  {correo}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  MENSAJE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{mensaje}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Este mensaje fue enviado automáticamente desde el sistema de gestión
de Los Santos Customs Taller Mecánico. Por favor no responda a este correo directamente.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    with smtplib.SMTP(os.getenv("MAIL_SERVER"), int(os.getenv("MAIL_PORT", 587))) as smtp:
        smtp.starttls()
        smtp.login(os.getenv("MAIL_USER"), os.getenv("MAIL_PASSWORD"))
        smtp.send_message(email)


def enviar_correo_confirmacion_cita(nombre_cliente, correo_cliente, fecha, hora, servicio, notas=""):
    email = EmailMessage()
    email["Subject"] = f"✅ Confirmación de cita — Los Santos Customs Taller"
    email["From"]    = os.getenv("MAIL_USER")
    email["To"]      = correo_cliente

    email.set_content(f"""\
Hola, {nombre_cliente}.

Tu cita en Los Santos Customs Taller Mecánico ha sido confirmada exitosamente.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DETALLES DE TU CITA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Servicio:  {servicio}
Fecha:     {fecha}
Hora:      {hora}
Notas:     {notas if notas else 'Sin notas adicionales'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Si necesitas cancelar o reprogramar tu cita, contáctanos
respondiendo a este correo o llamando al taller.

Gracias por confiar en Los Santos Customs.
— El equipo de Los Santos Customs Taller Mecánico
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    with smtplib.SMTP(os.getenv("MAIL_SERVER"), int(os.getenv("MAIL_PORT", 587))) as smtp:
        smtp.starttls()
        smtp.login(os.getenv("MAIL_USER"), os.getenv("MAIL_PASSWORD"))
        smtp.send_message(email)


def enviar_aviso_admin(asunto, cuerpo):
    email = EmailMessage()
    email["Subject"] = f"⚙️ Los Santos Customs Admin — {asunto}"
    email["From"]    = os.getenv("MAIL_USER")
    email["To"]      = os.getenv("MAIL_TO", os.getenv("MAIL_USER"))

    email.set_content(f"""\
Aviso automático del sistema Los Santos Customs.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{cuerpo}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Este es un mensaje automático del sistema de gestión de Los Santos Customs.
""")

    with smtplib.SMTP(os.getenv("MAIL_SERVER"), int(os.getenv("MAIL_PORT", 587))) as smtp:
        smtp.starttls()
        smtp.login(os.getenv("MAIL_USER"), os.getenv("MAIL_PASSWORD"))
        smtp.send_message(email)