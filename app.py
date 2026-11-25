from flask import Flask, render_template
from repository import PortfolioRepository

app = Flask(__name__)
repo = PortfolioRepository()

def index():
    persona = repo.obtener_persona()
    if persona is None:
        return "Todavía no hay datos cargados. Ejecutá seed.py primero.", 200

    return render_template(
        "index.html",
        persona=persona,
        educacion=repo.obtener_educacion(persona.id),
        experiencia=repo.obtener_experiencia(persona.id),
        tecnologias=repo.obtener_tecnologias(persona.id),
        habilidades_blandas=repo.obtener_habilidades_blandas(persona.id),
        proyectos=repo.obtener_proyectos(persona.id),
    )

app.add_url_rule("/", "index", index)

if __name__ == "__main__":
    app.run(debug=True)
