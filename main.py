from config import operating_mode, gentec_planet_index
from src.app.app import AppJeuxPhotoniques, AppGentec


if __name__ == "__main__":
    if operating_mode == "Jeux Photoniques":
        app = AppJeuxPhotoniques()
    elif operating_mode == "Gentec":
        app = AppGentec(gentec_planet_index)

    app.mainloop()
