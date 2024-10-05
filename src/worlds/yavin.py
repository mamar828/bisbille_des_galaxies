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
            position=vec3(5,10,0),
            rotation=vec3(45,0,0),
            scale=vec3(1,1,1),
            model=MilleniumFalcon,
            # instance=CorvetteAI(vec3(-20,0,-10))
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

        # self.health = 100
        self.health_bar = Object(
            texture="red",
            model=Cube,
            instance=HealthBar(),#self.health),
            saturated=True
        )


        # self.laser = Object(
        #     texture="green",
        #     model=Sphere,
        #     instance=Laser(),
        #     saturated=True
        # )


class CorvetteAI:
    def __init__(self, position):
        self.position = position
        self.rotation = vec3(0,0,0)
        self.scale = vec3(3,3,3)

    def update(self, app):
        # self.position += vec3(1,0,0) * delta_time
        # self.rotation += vec3(10,0,0) * delta_time
        self.rotation = vec3(90,0,0)
        self.scale = vec3(1,1,1)

class HealthBar:
    def __init__(self, health=100):
        self.health = health
        self.update_health_parameters()
        # self.position_func = lambda health: vec3(0,0.1,0.04)
        # self.position = vec3(0,0.1,0.04)
        self.rotation = vec3(0,0,0)
        self.count = 0

    def update_health_parameters(self):
        if self.health > 0:
            self.position = vec3(0,0.1,0.04) - (100 - self.health)/100 * vec3(0.07,0,0)
            self.scale = vec3(0.07,0.0001,0.001) - (100 - self.health)/100 * vec3(0.07,0,0)
        else:
            self.scale = vec3(0,0,0)

    def update(self, app):
        if app.collision_detector.collision:
            self.health -= 10*app.delta_time
            self.update_health_parameters()


# class Laser:
#     def __init__(self):
#         self.scale = vec3(0.1,0.1,0.1)
#         self.position = vec3(0,-1,0)
#         self.rotation = vec3(0,0,0)

#     def update(self, delta_time=None):
#         mouse_x, mouse_y = get_pos()
#         print(mouse_x,mouse_y)
#         # mouse_y = self.app.window_size[1] - mouse_y  # Invert Y to match OpenGL's coordinate system
#         # self.position = vec3(mouse_x, 100, mouse_y)
