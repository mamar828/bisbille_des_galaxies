import pygame as pg
from moderngl import NEAREST as mglNEAREST
from pywavefront import Wavefront

from src.engine.relative_paths import get_path


class Texture:
    def __init__(self, app):
        self.app = app
        self.context = app.context

        # Set cursor image
        img = pg.transform.scale_by(
            surface=pg.image.load(get_path("textures/laser.png")).convert_alpha(),
            factor=0.1
        )
        pg.mouse.set_cursor(
            pg.cursors.Cursor((img.get_width()//2, img.get_height()//2), img)
        )
        pg.mouse.set_visible(True)

        self.textures = {
            "skybox" :        self.get_texture_cube(get_path("textures/skybox")),
            "depth_texture" : self.get_depth_texture(),
            "cat" :           self.get_texture(get_path("objects/cat/20430_cat_diff_v1.jpg")),
        }

        for obj, data in self.app.loader.object_materials.items():
            if obj == "star_destroyer":
                self.textures[f"{obj}_EdgeBummp"] = self.get_texture(
                                                        get_path(f"objects/{obj}/wallSegment_DisplacementMap.png"))
                self.textures[f"{obj}_JetFire"] = self.get_texture(
                                                        get_path(f"objects/{obj}/force_fields.png"))
                self.textures[f"{obj}_None"] = self.get_texture(
                                                        get_path(f"objects/{obj}/LightGraySteel_DisplacementMap.png"))
                self.textures[f"{obj}_TopCover"] = self.get_texture(
                                                        get_path(f"objects/{obj}/LightGraySteel_DisplacementMap.png"))
            elif obj in ["tie_fighter", "corvette", "royal_starship", "imperial_shuttle", "death_star"]:
                current_material = ""
                with open(get_path(f"objects/{obj}/info.mtl")) as f:
                    for line in f.readlines():
                        if line.startswith("newmtl"):
                            current_material = line.split()[1]
                        if line.startswith("Kd"):
                            color = line.split()
                            self.textures[f"{obj}_{current_material}"] = self.get_color(
                                tuple([int(float(c) * 255) for c in color[1:]]))
            else:
                for material, vertices in data:
                    try:
                        self.textures[f"{obj}_{material}"] = self.get_texture(
                            f"{get_path(f'objects/{obj}')}/{material}.jpg"
                        )
                    except FileNotFoundError:
                        self.textures[f"{obj}_{material}"] = self.get_texture(
                            f"{get_path(f'objects/{obj}')}/{material}.png"
                        )

        for color in ["green", "red", "blue", "yellow", "orange", "cyan", "magenta", "white", "black", "purple",
                      "brown", "grey"]:
            self.textures[color] = self.get_color(color)

    def get_depth_texture(self):
        depth_texture = self.context.depth_texture(self.app.window_size)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture
    
    def get_texture_cube(self, directory_path):
        skybox_path = f"{directory_path}/skybox_{self.app.world.__class__.__name__.lower()}.png"
        texture = pg.transform.flip(pg.image.load(skybox_path).convert(),
                                    flip_x=True, flip_y=False)
        texture_cube = self.context.texture_cube(size=texture.get_size(), components=3, data=None)
        for i in range(6):
            texture_cube.write(face=i, data=pg.image.tostring(texture, "RGB"))
        return texture_cube

    def get_texture(self, path):
        # Load the texture and flip it upside down to make it upright
        texture = pg.transform.flip(pg.image.load(path).convert(), flip_x=False, flip_y=True)
        # texture.fill("green")
        texture = self.context.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, "RGB"))
        # mipmaps activation (correction for high distance objects)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        texture.filter = (mglNEAREST, mglNEAREST)
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
