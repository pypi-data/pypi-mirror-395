from .fastchat.api.api import FastApp, FastAPI
from .fastchat.config import AuthApiConfig

base_prompt: str = """
# Contexto Base de Technova:\n
La empresa "TechNova" vende productos electrónicos. Tiene un promedio de 5.000
ventas mensuales en Latinoamérica. Los productos pincipales que vende technova se divden en las siguentes categorias:
- smartphones
- notebooks
- accesorios
"""

no_sql_prompt: str = """Es muy importante que al momento de dividir una consulta en subconsultas, no generes codigo SQL como una subconsulta."""
md: str = (
    """ Utiliza el lenguage markdown para dar respuestas. Siempre que no se te pida otro comportamiento, escribe las respuestas en Markdown."""
)


auth_settings = AuthApiConfig().new_override({"log_lv": "DEBUG"})
fastapp: FastApp = FastApp(
    extra_reponse_system_prompts=[base_prompt, md],
    extra_selection_system_prompts=[base_prompt, no_sql_prompt],
)
app: FastAPI = fastapp.app
