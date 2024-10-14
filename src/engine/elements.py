from glm import vec3

from src.engine.models import *


class Object:
    def __init__(
            self,
            texture: str | int = "white",
            position: vec3=vec3(0,0,0),
            rotation: vec3=vec3(0,0,0),
            scale: vec3=vec3(1,1,1),
            instance=None,
            model: BaseModel=Sphere,
            saturated: bool=False,
        ):
        """
        Initialize an Object3D object. All coordinates are given in tuples of x, y, z.

        Parameters
        ----------
        texture : str or int, optional
            Texture id of the object. Available texture ids can be found in textures.py. Defaults to "white".
        position : vec3, optional
            Position of the object's origin if no instance is provided. Otherwise, the instance.get_position method is
            called to determine the object's center coordinates. Defaults to (0,0,0).
        rotation : vec3, optional
            Rotation to apply to the object. Defaults to (0,0,0).
        scale : vec3, optional
            Scale to apply to the object. Defaults to (1,1,1).
        instance : object with a .update method
            Function that determines the object's movement in the scene. Defaults to None.
        model : str, optional
            Specify the object's 3D model that should be used.
        """
        self.texture = texture
        self.rotation = instance.rotation if instance and hasattr(instance, "rotation") else rotation
        self.scale = instance.scale if instance and hasattr(instance, "scale") else scale
        self.position = instance.position if instance and hasattr(instance, "position") else position
        self.instance = instance
        self.model = model
        self.saturated = saturated


class HealthBar:
    def __init__(self, health: float=100, rate: float=10):
        self.health = health
        self.update_visual_health_parameters()
        self.rotation = vec3(0,0,0)
        self.count = 0
        self.rate = rate
        self.empty = False

    def update_visual_health_parameters(self):
        if self.health > 0:
            self.position = vec3(0,0.1,0.04) - (100 - self.health)/100 * vec3(0.07,0,0)
            self.scale = vec3(0.07,0.0001,0.001) - (100 - self.health)/100 * vec3(0.07,0,0)
        else:
            self.scale = vec3(0,0,0)
            self.empty = True

    def update(self, app):
        if self.empty:          # update first to allow the health bar to completely deplete (visually)
            app.running = False
        if app.collision_detector.collision:
            self.health -= self.rate*app.delta_time
            self.update_visual_health_parameters()
