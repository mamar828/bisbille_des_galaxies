import pygame as pg
from moderngl import NEAREST as mglNEAREST
from pywavefront import Wavefront

from src.engine.relative_paths import get_path


class Texture:
    def __init__(self, app):
        self.app = app
        self.context = app.context

        self.textures = {
            "skybox" :        self.get_texture_cube(get_path("textures/skybox")),
            "depth_texture" : self.get_depth_texture(),
            "cat" :           self.get_texture(get_path("objects/cat/20430_cat_diff_v1.jpg")),
        }

        for obj, data in self.app.loader.object_materials.items():
            if obj == "imperial_shuttle":
                self.textures[f"{obj}_wire_088199225"] = self.get_texture(get_path(f"objects/{obj}/wing texture.png"))
                self.textures[f"{obj}_wire_057008136"] = self.get_texture(get_path(f"objects/{obj}/wing texture.png"))
                self.textures[f"{obj}_wire_115115115"] = self.get_texture(get_path(f"objects/{obj}/wing texture.png"))
                self.textures[f"{obj}_wire_086086086"] = self.get_texture(get_path(f"objects/{obj}/wing texture.png"))
                self.textures[f"{obj}_wire_154185229"] = self.get_texture(get_path(f"objects/{obj}/wing texture.png"))
                self.textures[f"{obj}_wire_008110134"] = self.get_texture(get_path(f"objects/{obj}/wing texture.png"))
                self.textures[f"{obj}_wire_006135006"] = self.get_texture(get_path(f"objects/{obj}/wing texture.png"))
                self.textures[f"{obj}_wire_140088225"] = self.get_texture(get_path(f"objects/{obj}/wing texture.png"))
                self.textures[f"{obj}_wire_087225198"] = self.get_texture(get_path(f"objects/{obj}/wing texture.png"))
            elif obj == "star_destroyer":
                self.textures[f"{obj}_EdgeBummp"] = self.get_texture(
                                                        get_path(f"objects/{obj}/wallSegment_DisplacementMap.png"))
                self.textures[f"{obj}_JetFire"] = self.get_texture(
                                                        get_path(f"objects/{obj}/force_fields.png"))
                self.textures[f"{obj}_None"] = self.get_texture(
                                                        get_path(f"objects/{obj}/LightGraySteel_DisplacementMap.png"))
                self.textures[f"{obj}_TopCover"] = self.get_texture(
                                                        get_path(f"objects/{obj}/LightGraySteel_DisplacementMap.png"))
            else:
                for material, vertices in data:
                    self.textures[f"{obj}_{material}"] = self.get_texture(f"{get_path(f"objects/{obj}")}/{material}.jpg")

        for color in ["green", "red", "blue", "yellow", "orange", "cyan", "magenta", "white", "black", "purple",
                      "brown", "grey"]:
            self.textures[color] = self.get_color(color)

    def get_depth_texture(self):
        depth_texture = self.context.depth_texture(self.app.window_size)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture
    
    def get_texture_cube(self, directory_path, extension="png"):
        faces = ["right", "left", "top", "bottom", "back", "front"]
        textures = []

        for face in faces:
            current_texture = pg.image.load(f"{directory_path}/{face}.{extension}").convert()
            if face in ["right", "left", "front", "back"]:
                texture = pg.transform.flip(current_texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(current_texture, flip_x=False, flip_y=True)
            textures.append(texture)

        texture_cube = self.context.texture_cube(size=textures[0].get_size(), components=3, data=None)
        for i, texture in enumerate(textures):
            texture_cube.write(face=i, data=pg.image.tostring(texture, "RGB"))
        
        return texture_cube

    def get_texture(self, path):
        # Load the texture and flip it upside down to make it upright
        texture = pg.transform.flip(pg.image.load(path).convert(), flip_x=False, flip_y=True)
        # texture.fill("green")
        texture = self.context.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, "RGB"))
        # mipmaps activation (correction for high distance objects)
        texture.filter = (mglNEAREST, mglNEAREST)
        # texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)       # alternative mipmap
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        return texture

    def get_color(self, color):
        color_texture = pg.Surface((1,1)).convert_alpha()
        color_texture.fill(color)
        color_texture = self.context.texture(size=color_texture.get_size(), components=3,
                                             data=pg.image.tostring(color_texture, "RGB"))
        color_texture.filter = (mglNEAREST, mglNEAREST)
        color_texture.build_mipmaps()
        color_texture.anisotropy = 32.0
        return color_texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
