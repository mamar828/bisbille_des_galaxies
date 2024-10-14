import numpy as np
import os
from pywavefront import Wavefront

from src.engine.relative_paths import get_path


class MaterialLoader:
    def __init__(self):
        self.object_materials = {}
        for obj, filename in [
            # ("millenium_falcon", "Star Wars FALCON centered.obj"),
            # ("imperial_shuttle", "processed_imperial_shuttle_ver1_centered.obj"),
            ("star_destroyer", "StarDestroyer.obj"),
            # ("assault_frigate", "Assault_Frigate_Model.obj"),
            ("tie_fighter", "processed_tie.obj")
            # ("corvette", "Star Wars CORVETTE centered.obj"),
            # ("x_wing", "t-65.obj")
        ]:
            path = get_path(f"objects/{obj}")
            materials = []
            for material in Wavefront(f"{path}/{filename}", collect_faces=True, strict=False).materials.values():
                if material.vertices:
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

    @staticmethod
    def preprocess_obj_file(filename):
        with open(filename, 'r') as infile, open(f"{filename[:-4]}_pro.obj", 'w') as outfile:
            for line in infile:
                # Check if the line defines a vertex with texture coordinates (v/vt/vn format)
                if line.startswith("f "):
                    vertices = line.split()[1:]
                    new_vertices = []
                    for vertex in vertices:
                        # Split vertex attributes (v/vt/vn) and check consistency
                        parts = vertex.split("/")
                        if len(parts) == 3:
                            # This vertex has texture coordinates (T2F) and normal (N3F)
                            new_vertices.append(vertex)
                        elif len(parts) == 2:
                            # This vertex lacks normal or texture coordinates
                            # Add a dummy texture coordinate
                            new_vertices.append(f"{parts[0]}/{parts[1]}/0")
                        else:
                            # Handle cases with missing fields
                            new_vertices.append(f"{parts[0]}/0/0")  # Add dummy texture & normal

                    outfile.write(f"f {' '.join(new_vertices)}\n")
                else:
                    # Write other lines (v, vn, etc.) unchanged
                    outfile.write(line)
