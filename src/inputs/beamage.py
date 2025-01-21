from numpy import array as nparray


class Beamage:
    """
    This class defines the base class for a Beamage-4M.
    """

    def __init__(self, master_input, filename: str):
        self.master_input = master_input
        self.filename = filename
        self.position = [0,0]
        self.peak_saturation_threshold = 90

    def get_position(self):
        try:
            with open(self.filename, "r") as f:
                lines = f.readlines()
                infos = lines[-1].split("\t")
                if len(lines) > 100:
                    with open(self.filename, "w") as f:
                        f.write("NOTHING\n")

                if float(infos[11]) > self.peak_saturation_threshold:   # peak saturation limit
                    x = (float(infos[7]) + 5500) / 11000
                    y = (float(infos[8]) + 5500) / 11000
                    # x and y seem to range from ~-5500 to ~5500
                    self.position = (nparray([x, y]) * nparray(self.master_input.app.window_size)).round(0).astype(int)
        
        except Exception:
            pass
        return self.position
