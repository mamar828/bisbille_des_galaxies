import numpy as np
from pywavefront import Wavefront

from src.engine.relative_paths import get_path


class MaterialLoader:
    def __init__(self):
        self.object_materials = {}
        for obj, filename in [
            ("corvette", "Star Wars CORVETTE centered.obj"),
            # ("millenium_falcon", "Star Wars FALCON centered.obj"),
            # ("x_wing", "t-65.obj")
        ]:
            path = get_path(f"objects/{obj}")
            materials = []
            for material in Wavefront(f"{path}/{filename}", collect_faces=True).materials.values():
                materials.append((material.name, material.vertices))
            self.object_materials[obj] = materials

    @staticmethod
    def recenter_obj_file(input_path, output_path):
        vertices = []
        with open(input_path, "r") as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith("v "):
                parts = line.split()
                vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                vertices.append(vertex)

        vertices = np.array(vertices)
        center = np.mean(vertices, axis=0)

        with open(output_path, "w") as file:
            for line in lines:
                if line.startswith("v "):
                    parts = line.split()
                    vertex = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
                    centered_vertex = vertex - center
                    file.write(f"v {centered_vertex[0]} {centered_vertex[1]} {centered_vertex[2]}\n")
                else:
                    file.write(line)
