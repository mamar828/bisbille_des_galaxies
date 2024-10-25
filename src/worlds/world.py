import numpy as np
from glm import vec3

from src.engine.elements import *
from src.engine.models import *
from src.worlds.ais import *



class World:
    def __init__(self, health_bar_rate: float=20):
        self.health_bar = Object(
            texture="red",
            model=Cube,
            instance=HealthBar(rate=health_bar_rate),
            saturated=True
        )

    def update(self, app):
        for obj in self.__dict__.values():
            if obj.instance:
                obj.instance.update(app)


class Coruscant(World):
    def __init__(self):
        super().__init__()
        self.star_destroyer = Object(
            model=StarDestroyer,
            instance=StarDestroyerAI()
        )


class Yavin4(World):
    def __init__(self):
        super().__init__()
        self.tie_fighter = Object(
            model=TieFighter,
            instance=TieFighterAI()
        )
        # self.cat = Object(
        #     "cat",
        #     position=vec3(0, 0, 0),
        #     model=Cat,
        # )


# class Yavin4(World):
#     def __init__(self):
#         # self.tie_fighter = Object(
#         #     model=TieFighter,
#         #     instance=TieFighterAI()
#         # )
#         super().__init__(1e-8)
#         self.tie_fighter = Object(
#             model=TieFighter,
#             position=glm.vec3(0, 10, 0),
#         )
#         self.cube = Object(
#             model=Cube,
#             position=glm.vec3(2, 10, 0),
#         )
#         self.cube_2 = Object(
#             model=Cube,
#             position=glm.vec3(0, 10, 2),
#         )

worlds = [
    # Coruscant,
    Yavin4
]