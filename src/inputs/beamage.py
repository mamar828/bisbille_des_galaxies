from numpy import array as nparray


class Beamage:
    """
    This class defines the base class for a Beamage-4M.
    """

    def __init__(self, master_input, filename: str):
        self.master_input = master_input
        self.filename = filename

    def get_position(self):
        try:
            with open(self.filename, "r") as f:
                lines = f.readlines()
                infos = lines[-1].split("\t")
                if len(lines) > 100:
                    with open(self.filename, "w") as f:
                        f.write("NOTHING\n")
                if float(infos[11]) > 50:   # peak saturation
                    x = (float(infos[-4]) + 5500) / 11000
                    y = (float(infos[-3]) + 5500) / 11000
                    # x and y seem to range from ~-5500 to ~5500
                    return (nparray([x, y]) * nparray(self.master_input.app.window_size)).round(0).astype(int)
        
        except Exception:
            pass
