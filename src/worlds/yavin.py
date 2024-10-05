from glm import vec3

from src.engine.relative_paths import get_path
from src.engine.elements import Object
from src.engine.models import *
from src.worlds.world import World


class Yavin(World):
    def __init__(self):
        self.master_catty_boi = Object(
            texture="cat",
            position=vec3(0,0,20),
            rotation=vec3(-90,0,0),
            scale=vec3(1,1,1),
            model=Cat,
        )
        self.sphere = Object(
            texture="white",
            position=vec3(5,0,25),
            rotation=vec3(0,0,0),
            scale=vec3(1,1,1),
            model=Sphere,
        )
        self.cube = Object(
            texture="red",
            position=vec3(7,0,25),
            rotation=vec3(0,0,0),
            scale=vec3(1,1,1),
            model=Cube,
        )

        # self.corvette = Object(
        #     position=vec3(0,0,0),
        #     rotation=vec3(0,0,0),#-2900
        #     scale=vec3(1,1,1),
        #     model=Corvette,
        #     instance=None#CorvetteAI(vec3(0,0,-10))
        # )

        self.millenium_falcon = Object(
            position=vec3(-20,0,-10),
            rotation=vec3(0,0,0),
            scale=vec3(1,1,1),
            model=MilleniumFalcon,
            instance=None
        )

        # self.shuttle = Object(
        #     position=vec3(0,0,0),
        #     rotation=vec3(0,0,0),
        #     scale=vec3(1,1,1),
        #     model=ImperialShuttle,
        #     instance=None
        # )

        # self.star_destroyer = Object(
        #     position=vec3(0,0,0),
        #     rotation=vec3(0,0,0),
        #     scale=vec3(1,1,1),
        #     model=StarDestroyer,
        #     instance=None
        # )

        # self.assault_frigate = Object(
        #     position=vec3(0,0,0),
        #     rotation=vec3(0,0,0),
        #     scale=vec3(1,1,1),
        #     model=AssaultFrigate,
        #     instance=None
        # )

        # self.x_wing = Object(
        #     position=vec3(0,0,0),
        #     rotation=vec3(0,0,0),
        #     scale=vec3(1,1,1),
        #     model=XWing,
        #     instance=None
        # )

        self.cube_1 = Object(
            texture="blue",
            position=vec3(0,0,2),
            rotation=vec3(0,0,0),
            scale=vec3(1,1,1),
            model=Cube,
        )

        self.cube_2 = Object(
            texture="blue",
            position=vec3(-2,0,0),
            rotation=vec3(0,0,0),
            scale=vec3(1,1,1),
            model=Cube,
        )

        # self.x_wing = Object(
        #     position=vec3(-20,0,-10),
        #     rotation=vec3(0,0,0),
        #     scale=vec3(1,1,1),
        #     model=XWing,
        #     instance=None
        # )


class CorvetteAI:
    def __init__(self, position):
        self.position = position

    def update(self, delta_time):
        self.position += vec3(1,0,0) * delta_time
    
    def get_position(self):
        return self.position