import os
# Suppress repeated pygame welcome messages
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from config import operating_mode, gentec_planet_index
from src.app.app import AppJeuxPhotoniques, AppGentec


if __name__ == "__main__":
    if operating_mode == "Jeux Photoniques":
        app = AppJeuxPhotoniques()
    elif operating_mode == "Gentec":
        app = AppGentec(gentec_planet_index)
    else:
        raise ValueError('Invalid operating_mode in config.py, valid values are "Jeux Photoniques" and "Gentec"')

    app.mainloop()
