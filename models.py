from werkzeug.security import check_password_hash, generate_password_hash

MESES = ["ene", "feb", "mar", "abr", "may", "jun",
         "jul", "ago", "sep", "oct", "nov", "dic"]


class ItemPortfolio:
    def __init__(self, id_item, descripcion=None):
        self.id = id_item
        self.descripcion = descripcion or ""

    def titulo_visible(self):
        raise NotImplementedError

    def subtitulo(self):
        raise NotImplementedError

    def periodo(self):
        return ""


class ItemConPeriodo(ItemPortfolio):

    def __init__(self, id_item, descripcion, fecha_inicio, fecha_fin):
        super().__init__(id_item, descripcion)
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin         

    def _formatear_fecha(self, fecha):
        raise NotImplementedError

    def periodo(self):
        inicio = self._formatear_fecha(self._fecha_inicio)
        fin = self._formatear_fecha(self._fecha_fin) if self._fecha_fin else "Actualidad"
        return f"{inicio} – {fin}"

class Educacion(ItemConPeriodo):
    def __init__(self, id_item, institucion, titulo, nivel,
                 fecha_inicio, fecha_fin, descripcion=None):
        super().__init__(id_item, descripcion, fecha_inicio, fecha_fin)
        self._institucion = institucion
        self._titulo = titulo
        self._nivel = nivel

    def titulo_visible(self):
        return self._institucion

    def subtitulo(self):
        return self._titulo or self._nivel.capitalize()

    def _formatear_fecha(self, fecha):
        return str(fecha)                   

class Experiencia(ItemConPeriodo):
    def __init__(self, id_item, puesto, empresa,
                 fecha_inicio, fecha_fin, descripcion=None):
        super().__init__(id_item, descripcion, fecha_inicio, fecha_fin)
        self._puesto = puesto
        self._empresa = empresa

    def titulo_visible(self):
        return self._puesto

    def subtitulo(self):
        return self._empresa

    def _formatear_fecha(self, fecha):
        return f"{MESES[fecha.month - 1].capitalize()} {fecha.year}"  

class Proyecto(ItemPortfolio):
    def __init__(self, id_item, titulo, descripcion, url_repo,
                 url_demo, imagen, tecnologias=""):
        super().__init__(id_item, descripcion)
        self._titulo = titulo
        self.url_repo = url_repo
        self.url_demo = url_demo
        self.imagen = imagen
        self._tecnologias = tecnologias

    def titulo_visible(self):
        return self._titulo

    def subtitulo(self):
        return self._tecnologias            

class Tecnologia:
    def __init__(self, nombre, icono, categoria, nivel):
        self.nombre = nombre
        self.icono = icono
        self.categoria = categoria
        self.nivel = nivel                  

class Persona:
    def __init__(self, id_persona, nombre, apellido, titulo, resumen,
                 objetivo, email, telefono, ciudad, foto, cv_pdf):
        self.id = id_persona
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_completo = f"{nombre} {apellido}"
        self.titulo = titulo
        self.resumen = resumen
        self.objetivo = objetivo
        self.email = email
        self.telefono = telefono
        self.ciudad = ciudad
        self.foto = foto
        self.cv_pdf = cv_pdf

class Usuario:

    def __init__(self, username, password_hash):
        self.__username = username
        self.__password_hash = password_hash

    def obtener_username(self):
        return self.__username

    def obtener_password_hash(self):
        return self.__password_hash

    def verificar_password(self, password):
        return check_password_hash(self.__password_hash, password)


def crear_usuario(username, password):
    return Usuario(username, generate_password_hash(password))
