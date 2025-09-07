import smtplib
import datetime
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Configuración ---
usuarios = {
    "Jaume": "jaumemir5000@hotmail.com",
    "Javi": "javierherranz00@gmail.com ",
    "Mario": "mario.egro.vila@gmail.com"
}

tareas = ["Limpiar baño", "Limpiar cocina", "Limpiar salón"]

# Credenciales desde variables de entorno (GitHub Actions)
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def reparto_tareas():
    """Asigna tareas en rotación según la semana del año."""
    semana = datetime.date.today().isocalendar()[1]
    compañeros = list(usuarios.keys())
    asignacion = {}

    for i, nombre in enumerate(compañeros):
        tarea = tareas[(i + semana) % len(tareas)]
        asignacion[nombre] = tarea

    return asignacion


def enviar_mail(asignacion):
    """Envía un único correo a todos con el reparto semanal."""
    destinatarios = list(usuarios.values())

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = "Tareas semanales del piso 🧹"

    # Crear cuerpo del mensaje
    cuerpo = "¡Hola trío calavera!\n\nAquí están las tareas de esta próxima semana:\n\n"
    for nombre, tarea in asignacion.items():
        cuerpo += f"- {nombre}: {tarea}\n"
    cuerpo += "\n¡Ánimo con la limpieza!\n"

    msg.attach(MIMEText(cuerpo, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


if __name__ == "__main__":
    asignacion = reparto_tareas()
    enviar_mail(asignacion)
