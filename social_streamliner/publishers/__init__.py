# Importa le funzioni di pubblicazione da ogni modulo
from . import instagram
from . import tiktok
from . import youtube
from . import twitter

# Lista di tutti i moduli di pubblicazione disponibili
# Questo permette allo scheduler di iterare dinamicamente su tutti i publisher
all_publishers = [
    instagram,
    tiktok,
    youtube,
    twitter,
]
