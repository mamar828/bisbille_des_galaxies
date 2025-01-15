from src.app.app import AppJeuxPhotoniques, AppGentec


if __name__ == "__main__":
    # app = AppJeuxPhotoniques()
    app = AppGentec(2)      # 0 Hoth, 1 Coruscant, 2 Yavin4, 3 Dathomir, 4 Kashyyyk, 5 Naboo, 6 Kamino, 7 Umbara

    app.mainloop()
