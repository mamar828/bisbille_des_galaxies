from pywavefront import Wavefront

from src.engine.relative_paths import get_path


class MaterialLoader:
    def __init__(self):
        self.object_materials = {}
        for obj, filename in [("corvette", "Star Wars CORVETTE.obj")]:
            path = get_path(f"objects/{obj}")
            materials = []
            for material in Wavefront(f"{path}/{filename}", collect_faces=True).materials.values():
                materials.append((material.name, material.vertices))
            self.object_materials[obj] = materials
