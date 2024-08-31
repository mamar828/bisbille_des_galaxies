from glm import vec3
from eztcolors import Colors as C

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
        self.rotation = rotation
        self.scale = scale
        self.position = instance.get_position() if instance else position
        self.instance = instance
        self.model = model
