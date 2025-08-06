from src.engine.elements import *
from src.engine.models import *
from src.worlds.ais import *


class World:
    def __init__(self):
        self.health_bar = Object(
            texture="red",
            model=Cube,
            instance=HealthBar(),
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
            instance=StarDestroyerAIFilix()
        )


class Dathomir(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=Malevolence,
            instance=MalevolenceAIFilix()
        )


class Hoth(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=MilleniumFalcon,
            instance=MillenniumFalconAIFilix()
        )


class Kamino(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=ImperialShuttle,
            instance=ImperialShuttleAI()
        )


class Kashyyyk(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=Corvette,
            instance=CorvetteAI()
        )


class Naboo(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=RoyalStarship,
            instance=RoyalStarshipAI()
        )


class Umbara(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=AWing,
            instance=AWingAI()
        )


class Yavin4(World):
    def __init__(self):
        super().__init__()
        self.ship = Object(
            model=TieFighter,
            instance=TieFighterAIFilix()
        )


class Test(World):
    def __init__(self):
        super().__init__(1e-8)
        self.ship = Object(
            model=RoyalStarship,
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
    Hoth,
    Coruscant,
    Yavin4,
    Dathomir,
    Kashyyyk,
    Naboo,
    Kamino,
    Umbara,
]
