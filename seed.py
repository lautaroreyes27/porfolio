import getpass
from database import Database
from models import crear_usuario

db = Database()

username = input("Username para el login: ").strip()
password = getpass.getpass("Password (no se ve al escribir): ")

usuario = crear_usuario(username, password)
id_usuario = db.ejecutar(
    "INSERT INTO usuario (username, password_hash) VALUES (%s, %s)",
    (usuario.obtener_username(), usuario.obtener_password_hash()),
)

id_persona = db.ejecutar(
    """INSERT INTO persona (id_usuario, nombre, apellido, titulo, resumen, objetivo,
                            email, telefono, ciudad, foto, cv_pdf)
       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
    (id_usuario, "Lautaro", "Reyes",
     "Estudiante de Programación",
     "Estudiante de sexto año del Instituto Técnico Renault, orientación en "
     "Programación, con sólida formación técnica y fuerte interés en tecnología "
     "e inteligencia artificial. Combino habilidades técnicas con capacidad de "
     "trabajo bajo presión y comunicación efectiva.",
     "Estudiar Ingeniería en Sistemas y Telecomunicaciones.",
     "lautirey2007@gmail.com", "351-558-2185", "Córdoba, Argentina",
     "img/foto.jpg", "docs/CV_Lautaro_Reyes.pdf"),
)

for inst, titulo, nivel, ini, fin in [
    ("Centro Educativo Santo Domingo", None, "primario", 2020, 2022),
    ("Instituto Técnico Renault", "Técnico en Programación", "secundario", 2023, None),
]:
    db.ejecutar(
        "INSERT INTO educacion (id_persona, institucion, titulo, nivel, fecha_inicio, fecha_fin) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (id_persona, inst, titulo, nivel, ini, fin),
    )

for puesto, empresa, ini, fin, desc in [
    ("Edición de videos e imágenes", "Brandup", "2026-03-01", "2026-07-31",
     "Edité entre 7 y 8 videos mensuales con Kdenlive para clientes de distintos "
     "rubros y edité imágenes con apoyo de IA. Logré la aprobación del material "
     "en un máximo de dos rondas de corrección."),
    ("Empleado de comercio", "Kiosco familiar", "2026-01-01", "2026-06-30",
     "Gestioné de forma autónoma la atención al público y el orden del local, "
     "con atención personalizada y resolución de reclamos."),
]:
    db.ejecutar(
        "INSERT INTO experiencia (id_persona, puesto, empresa, fecha_inicio, fecha_fin, descripcion) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (id_persona, puesto, empresa, ini, fin, desc),
    )

for h in ["Excelente comunicación y honestidad",
          "Trato amable y extrovertido",
          "Puntualidad y respeto",
          "Capacidad de trabajo en equipo y con el público"]:
    db.ejecutar("INSERT INTO habilidad_blanda (id_persona, descripcion) VALUES (%s, %s)",
                (id_persona, h))

print("Listo. Datos cargados.")
