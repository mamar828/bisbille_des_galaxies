from numpy import array as nparray
from random import choice
import glm
from pywavefront import Wavefront
import moderngl as mgl

from src.engine.relative_paths import get_path


class BaseModel:
    def __init__(
            self, 
            app,
            vertex_array_object_name,
            texture_id,
            position: glm.vec3,
            rotation: glm.vec3,
            scale: glm.vec3,
            instance=None,
            saturated=False
    ):
        if saturated and not vertex_array_object_name.startswith("surface"):
            vertex_array_object_name = f"saturated_{vertex_array_object_name}"

        self.app = app
        self.position = position
        self.rotation = glm.vec3([glm.radians(angle) for angle in rotation])  # Convert angles from degrees to radians
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.texture_id = texture_id
        self.vertex_array_object = app.mesh.vertex_array_object.vertex_array_objects[vertex_array_object_name]
        self.vertex_array_object_name = vertex_array_object_name
        self.program = self.vertex_array_object.program
        self.instance = instance
        self.saturated = saturated
        self.on_init()

    def update(self):
        self.m_model = self.get_model_matrix()
        self.texture.use(location=0)
        if not self.saturated: self.program["camPos"].write(self.app.camera.position)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def update_shadow(self):
        self.shadow_program["m_model"].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vertex_array_object.render()
    
    def on_init(self):
        self.shadow_program = None
        if not self.saturated:
            # Initialize shadow and light concerned parameters
            self.program["m_view_light"].write(self.app.light.m_view_light)
            self.program["shadow_map"] = 1
            # resolution
            # self.program["u_resolution"].write(glm.vec2(self.app.window_size))        # Used for shadow smoothing
            # depth texture
            # shadow
            self.shadow_vertex_array_object = self.app.mesh.vertex_array_object.vertex_array_objects[
                                                                            f"shadow_{self.vertex_array_object_name}"]
            self.shadow_program = self.shadow_vertex_array_object.program
            self.shadow_program["m_proj"].write(self.app.camera.m_proj)
            self.shadow_program["m_view_light"].write(self.app.light.m_view_light)
            self.shadow_program["m_model"].write(self.m_model)
            # light
            self.program["light.position"].write(self.app.light.position)
            self.program["light.Ia"].write(self.app.light.Ia)
            self.program["light.Id"].write(self.app.light.Id)
            self.program["light.Is"].write(self.app.light.Is)

        self.depth_texture = self.app.mesh.texture.textures["depth_texture"]
        self.depth_texture.use(location=1)
        # texture
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_0"] = 0
        self.texture.use(location=0)
        # mvp matrices
        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(self.app.camera.m_view)
        self.program["m_model"].write(self.m_model)

    def get_model_matrix(self):
        # translation 
        # Account for the fact that usual coords are (x,y,z) but model ones should be (x,z,y)
        t_model = glm.translate(glm.mat4(), (self.position[0], self.position[2], -self.position[1]))
        # rotation
        r_model = glm.rotate(t_model, self.rotation.y, glm.vec3(0,0,1))
        r_model = glm.rotate(r_model, self.rotation.x, glm.vec3(1,0,0))
        r_model = glm.rotate(r_model, self.rotation.z, glm.vec3(0,1,0))
        # scale
        s_model = glm.scale(r_model, glm.vec3(self.scale.x, self.scale.z, self.scale.y))
        return s_model
    
    def render(self):
        self.update()
        self.vertex_array_object.render()

    def update_visual(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def destroy(self):
        del self
    
    @staticmethod
    def get_random_color():
        # black removed
        return choice(["green", "red", "blue", "yellow", "orange", "cyan", "magenta", "white", "purple",
                       "brown", "grey"])


class Skybox(BaseModel):
    def __init__(
            self,
            app,
            texture_id="skybox",
            position=glm.vec3(0,0,0),
            rotation=glm.vec3(0,0,0),
            scale=glm.vec3(1,1,1)
    ):
        super().__init__(app, "skybox", texture_id, position, rotation, scale)
        self.on_init()

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program["u_texture_skybox"] = 0
        self.texture.use(location=0)
        # mvp matrices
        self.program["m_proj"].write(self.app.camera.m_proj)
        self.program["m_view"].write(glm.mat4(glm.mat3(self.app.camera.m_view)))

    def update(self):
        self.m_model = self.get_model_matrix()
        self.program["m_view"].write(glm.mat4(glm.mat3(self.app.camera.m_view)))


class Cube(BaseModel):
    def __init__(
            self,
            app,
            texture_id,
            position=glm.vec3(0,0,0),
            rotation=glm.vec3(0,0,0),
            scale=glm.vec3(1,1,1),
            instance=None,
            saturated=False
    ):
        super().__init__(app, "cube", texture_id, position, rotation, scale, instance, saturated)


class Surface(BaseModel):
    def __init__(
            self,
            app,
            vertex_array_object_name,
            texture_id,
            position=glm.vec3(0,0,0),
            rotation=glm.vec3(0,0,0),
            scale=glm.vec3(1,1,1),
            instance=None
    ):
        super().__init__(app, vertex_array_object_name, texture_id, position, rotation, scale, instance, True)


class Sphere(BaseModel):
    def __init__(
            self,
            app,
            texture_id,
            position=glm.vec3(0,0,0),
            rotation=glm.vec3(0,0,0),
            scale=glm.vec3(1,1,1),
            instance=None,
            saturated=False
    ):
        super().__init__(app, "sphere", texture_id, position, rotation, self.convert_scale(scale), instance, saturated)
    
    def convert_scale(self, scale):
        # Convert the object's scale in the default dimensions
        return scale*0.009095


class Cat(BaseModel):
    def __init__(
            self,
            app,
            position=glm.vec3(0,0,0),
            rotation=glm.vec3(0,0,0),
            scale=glm.vec3(1,1,1),
            instance=None,
            saturated=False,
            texture_id="cat"
    ):
        super().__init__(app, "cat", texture_id, position, rotation, scale, instance, saturated)


class Cat(BaseModel):
    def __init__(
            self,
            app,
            position=glm.vec3(0,0,0),
            rotation=glm.vec3(0,0,0),
            scale=glm.vec3(1,1,1),
            instance=None,
            saturated=False,
            texture_id="cat"
    ):
        super().__init__(app, "cat", texture_id, position, rotation, scale, instance, saturated)


class MaterialModel:
    def __init__(
            self,
            app,
            texture_id: str,
            position=glm.vec3(0,0,0),
            rotation=glm.vec3(0,0,0),
            scale=glm.vec3(1,1,1),
            instance=None,
            saturated=False,
    ):
        self.app = app
        self.position = position
        self.rotation = glm.vec3([glm.radians(angle) for angle in rotation])  # Convert angles from degrees to radians
        self.scale = scale
        self.instance = instance
        self.saturated = saturated
        self.models = []
        for data in self.app.loader.object_materials[texture_id]:
            material_name = f"{texture_id}_{data[0]}"
            self.models.append(BaseModel(
                app,
                material_name,
                material_name,
                position,
                self.rotation,
                scale,
                instance,
                saturated,
            ))

    def update(self):
        for model in self.models:
            model.update()

    def update_shadow(self):
        for model in self.models:
            model.update_shadow()

    def render_shadow(self):
        for model in self.models:
            model.render_shadow()

    def render(self):
        for model in self.models:
            model.render()

    def update_visual(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        for model in self.models:
            model.update_visual(**kwargs)

    def destroy(self):
        del self


class Corvette(MaterialModel):
    def __init__(
            self,
            app,
            texture_id: str=None,
            position=glm.vec3(0, 0, 0),
            rotation=glm.vec3(0, 0, 0),
            scale=glm.vec3(1, 1, 1),
            instance=None,
            saturated: bool=False
    ):
        super().__init__(app, "corvette", position, rotation, scale, instance, saturated)


class MilleniumFalcon(MaterialModel):
    def __init__(
            self,
            app,
            texture_id: str=None,
            position=glm.vec3(0, 0, 0),
            rotation=glm.vec3(0, 0, 0),
            scale=glm.vec3(1, 1, 1),
            instance=None,
            saturated: bool=False
    ):
        self.instance = instance
        aligned_rotation = rotation/2 * 115 - glm.vec3(0,0,2250)
        scaling = scale / 100
        super().__init__(app, "millenium_falcon", position, aligned_rotation, scaling, instance, saturated)

    def update_visual(self, **kwargs):
        kwargs["rotation"] = kwargs["rotation"]/2 * 115 - glm.vec3(0,0,2250)
        kwargs["scale"] /= 100
        super().update_visual(**kwargs)


class ImperialShuttle(MaterialModel):
    def __init__(
            self,
            app,
            texture_id: str=None,
            position=glm.vec3(0, 0, 0),
            rotation=glm.vec3(0, 0, 0),
            scale=glm.vec3(1, 1, 1),
            instance=None,
            saturated: bool=False
    ):
        scaling = scale / 350
        super().__init__(app, "imperial_shuttle", position, rotation, scaling, instance, saturated)

    def update_visual(self, **kwargs):
        kwargs["scale"] /= 350
        super().update_visual(**kwargs)


class StarDestroyer(MaterialModel):
    def __init__(
            self,
            app,
            texture_id: str=None,
            position=glm.vec3(0, 0, 0),
            rotation=glm.vec3(0, 0, 0),
            scale=glm.vec3(1, 1, 1),
            instance=None,
            saturated: bool=False
    ):
        self.scaling_factor = 0.9
        scaling = scale * self.scaling_factor
        super().__init__(app, "star_destroyer", position, rotation, scaling, instance, saturated)

    def update_visual(self, **kwargs):
        kwargs["scale"] *= self.scaling_factor
        super().update_visual(**kwargs)


class AssaultFrigate(MaterialModel):
    def __init__(
            self,
            app,
            texture_id: str=None,
            position=glm.vec3(0, 0, 0),
            rotation=glm.vec3(0, 0, 0),
            scale=glm.vec3(1, 1, 1),
            instance=None,
            saturated: bool=False
    ):
        scaling = scale * 0.9
        super().__init__(app, "assault_frigate", position, rotation, scaling, instance, saturated)


class TieFighter(MaterialModel):
    def __init__(
            self,
            app,
            texture_id: str=None,
            position=glm.vec3(0, 0, 0),
            rotation=glm.vec3(0, 0, 0),
            scale=glm.vec3(1, 1, 1),
            instance=None,
            saturated: bool=False
    ):
        self.scaling_factor = 0.7
        scaling = scale * self.scaling_factor
        super().__init__(app, "tie_fighter", position, rotation, scaling, instance, saturated)

    def update_visual(self, **kwargs):
        kwargs["scale"] *= self.scaling_factor
        super().update_visual(**kwargs)


class XWing(MaterialModel):
    def __init__(
            self,
            app,
            texture_id: str=None,
            position=glm.vec3(0, 0, 0),
            rotation=glm.vec3(0, 0, 0),
            scale=glm.vec3(1, 1, 1),
            instance=None,
            saturated: bool=False
    ):
        super().__init__(app, "x_wing", position, rotation, scale, instance, saturated)
