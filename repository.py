from database import Database
from models import Educacion, Experiencia, Persona, Proyecto, Tecnologia

class PortfolioRepository:

    def __init__(self, db=None):
        self._db = db or Database()

    def obtener_persona(self):
        filas = self._db.consultar("SELECT * FROM persona LIMIT 1")
        if not filas:
            return None
        f = filas[0]
        return Persona(f["id_persona"], f["nombre"], f["apellido"], f["titulo"],
                       f["resumen"], f["objetivo"], f["email"], f["telefono"],
                       f["ciudad"], f["foto"], f["cv_pdf"])

    def obtener_educacion(self, id_persona):
        filas = self._db.consultar(
            "SELECT * FROM educacion WHERE id_persona = %s ORDER BY fecha_inicio DESC",
            (id_persona,),
        )
        return [Educacion(f["id_educacion"], f["institucion"], f["titulo"], f["nivel"],
                          f["fecha_inicio"], f["fecha_fin"], f["descripcion"])
                for f in filas]

    def obtener_experiencia(self, id_persona):
        filas = self._db.consultar(
            "SELECT * FROM experiencia WHERE id_persona = %s ORDER BY fecha_inicio DESC",
            (id_persona,),
        )
        return [Experiencia(f["id_experiencia"], f["puesto"], f["empresa"],
                            f["fecha_inicio"], f["fecha_fin"], f["descripcion"])
                for f in filas]

    def obtener_tecnologias(self, id_persona):
        filas = self._db.consultar(
            """SELECT t.nombre, t.icono, c.nombre AS categoria, pt.nivel
               FROM persona_tecnologia pt
               JOIN tecnologia t ON t.id_tecnologia = pt.id_tecnologia
               JOIN categoria_tecnologia c ON c.id_categoria = t.id_categoria
               WHERE pt.id_persona = %s
               ORDER BY c.nombre, pt.nivel DESC""",
            (id_persona,),
        )
        agrupadas = {}
        for f in filas:
            tec = Tecnologia(f["nombre"], f["icono"], f["categoria"], f["nivel"])
            agrupadas.setdefault(f["categoria"], []).append(tec)
        return agrupadas

    def obtener_habilidades_blandas(self, id_persona):
        filas = self._db.consultar(
            "SELECT descripcion FROM habilidad_blanda WHERE id_persona = %s",
            (id_persona,),
        )
        return [f["descripcion"] for f in filas]

    def obtener_proyectos(self, id_persona):
        filas = self._db.consultar(
            """SELECT p.*, GROUP_CONCAT(t.nombre ORDER BY t.nombre SEPARATOR ', ') AS tecnologias
               FROM proyecto p
               LEFT JOIN proyecto_tecnologia pt ON pt.id_proyecto = p.id_proyecto
               LEFT JOIN tecnologia t ON t.id_tecnologia = pt.id_tecnologia
               WHERE p.id_persona = %s
               GROUP BY p.id_proyecto""",
            (id_persona,),
        )
        return [Proyecto(f["id_proyecto"], f["titulo"], f["descripcion"], f["url_repo"],
                         f["url_demo"], f["imagen"], f["tecnologias"] or "")
                for f in filas]
