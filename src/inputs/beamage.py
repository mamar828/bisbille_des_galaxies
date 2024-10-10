from numpy import array as nparray


class Beamage:
    """
    This class defines the base class for a Beamage-4M.
    """

    def __init__(self, master_input, filename: str):
        self.master_input = master_input
        self.filename = filename
        # self.position = -1
        # self.y = -1
        # self.filename = C:\Users\Proprio\Documents\Mathieu\bisbille_des_galaxies\test_measurements.txt

    def get_position(self):
        try:
            with open(self.filename, "r") as f:
                lines = f.readlines()
                infos = lines[-1].split("\t")
                if float(infos[11]) > 50:   # peak saturation
                    x = (infos[-4] + 5500) / 11000
                    y = (infos[-3] + 5500) / 11000
                    # x and y seem to range from ~-5500 to ~5500
            if len(lines) > 100:
                with open(self.filename, "w") as f:
                    f.write("NOTHING\n")
            return nparray(x, y) * self.app.window_size
        
        except PermissionError:
            return None, None
