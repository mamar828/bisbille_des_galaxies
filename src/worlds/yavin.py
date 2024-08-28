from glm import vec3

from src.engine.relative_paths import get_path
from src.engine.elements import Object
from src.engine.models import *
from src.worlds.world import World


class Yavin(World):
    def __init__(self):
        self.master_catty_boi = Object(
            texture="cat",
            position=vec3(0,0,0),
            rotation=vec3(-90,0,0),
            scale=vec3(1,1,1),
            model=Cat,
        )
        self.sphere = Object(
            texture="white",
            position=vec3(5,0,5),
            rotation=vec3(0,0,0),
            scale=vec3(1,1,1),
            model=Sphere,
        )
        self.cube = Object(
            texture="red",
            position=vec3(7,0,5),
            rotation=vec3(0,0,0),
            scale=vec3(1,1,1),
            model=Cube,
        )

        self.corvette = Object(
            texture="yellow",
            position=vec3(0,0,-10),
            rotation=vec3(0,0,0),
            scale=vec3(1,1,1),
            model=Corvette,
        )
