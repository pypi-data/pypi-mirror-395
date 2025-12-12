from environs import Env

env = Env()
env.read_env()

# Charger toutes les variables d'environnement nécessaires
GENUI_API_URL = env.url("GENUI_API_URL").geturl()
