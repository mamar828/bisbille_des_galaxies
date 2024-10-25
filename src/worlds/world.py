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
        self.ship = Object(
            model=StarDestroyer,
            instance=StarDestroyerAI()
        )


class Dathomir(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=Malevolence,
            instance=TieFighterAI()
        )


class Hoth(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=MilleniumFalcon,
            instance=TieFighterAI()
        )


class Kamino(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=TieFighter,
            instance=TieFighterAI()
        )


class Kashyyyk(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=TieFighter,
            instance=TieFighterAI()
        )


class Naboo(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=TieFighter,
            instance=TieFighterAI()
        )


class Umbara(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=TieFighter,
            instance=TieFighterAI()
        )


class Yavin4(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=TieFighter,
            instance=TieFighterAI()
        )


class Test(World):
    def __init__(self):
        super().__init__(1e-8)
        self.ship = Object(
            model=Slave,
            position=glm.vec3(0, 10, 0),
        )
        self.cube = Object(
            model=Cube,
            position=glm.vec3(2, 10, 0),
        )
        self.cube_2 = Object(
            model=Cube,
            position=glm.vec3(0, 10, 2),
        )

available_worlds = [
    Coruscant,
    Yavin4,
    Hoth,
    Dathomir,
    # Test,
]
