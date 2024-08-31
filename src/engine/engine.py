import pygame as pg
import moderngl as mgl
from glm import vec3
from eztcolors import Colors as C

from src.engine.camera import Camera
from src.engine.light import Light
from src.engine.mesh import Mesh
from src.engine.scene import Scene
from src.engine.scene_renderer import SceneRenderer
from src.inputs.master_input import MasterInput
from src.inputs.keyboard import Keyboard
from src.inputs.controller import Controller
from src.engine.display import Display



class Engine:
    """
    This class defines the 3D engine.
    """

    def __init__(
            self,
            world=None,
            window_size: tuple[int,int]=(1440,900),
            framerate: int=60,
            fullscreen: bool=True,
            light_position: vec3=vec3(0,0,0),
            light_color: vec3=vec3(1,1,1),
            light_ambient_intensity: float=0,
            light_diffuse_intensity: float=1.5,
            light_specular_intensity: float=1.0,
            camera_origin: tuple[int,int,int]=(0,0,0),
            camera_speed: float=0.025,
            camera_sensitivity: float=0.1,
            camera_fov: float=50.,
            camera_near_render_distance: float=0.05,
            camera_far_render_distance: float=1e20,
            camera_yaw: float=-90.,
            camera_pitch: float=0.,
            # objects: list[Object3D]=None,
            # functions: list[Function3D]=None,
            model_saturation: bool=True,
            camera_cinematic_settings: dict={
                "positive_acceleration" : 0.05,
                "negative_acceleration" : 0.05,
                "positive_rotation" : 0.05,
                "negative_rotation" : 0.94
            },
            dev_mode: bool=False,
    ):
        """
        Initialize an Engine object.

        Arguments
        ---------
        simulation : Simulation, optional
            Simulation instance. None if not provided.
        window_size : tuple[int,int], optional
            Window size in pixels. Default is (1440,900).
        framerate : int, optional
            Desired framerate. Default is 60.
        fullscreen : bool, optional
            Whether to start in fullscreen mode. Default is True.
        light_position : tuple[int,int,int], optional
            Light position in 3D space. Default is (0,0,0) or the simulation.system.origin if applicable.
        light_color : tuple[int,int,int], optional
            Light color. Default is (1,1,1).
        light_ambient_intensity : float, optional
            Ambient light intensity. Default is 0.
        light_diffuse_intensity : float, optional
            Diffuse light intensity. Default is 1.5.
        light_specular_intensity : float, optional
            Specular light intensity. Default is 1.0.
        camera_origin : tuple[int,int,int], optional
            Camera origin in 3D space. Default is (0,0,0) or the simulation.system.origin if applicable.
        camera_speed : float, optional
            Camera base movement speed. Default is 0.025.
        camera_sensitivity : float, optional
            Camera sensitivity. Default is 0.1.
        camera_fov : float, optional
            Camera field of view. Default is 50.
        camera_near_render_distance : float, optional
            Camera near render distance. Default is 0.05.
        camera_far_render_distance : float, optional
            Camera far render distance. Default is 1e20.
        camera_yaw : float, optional
            Camera starting yaw value. Default is -90.
        camera_pitch : float, optional
            Camera starting pitch value. Default is 0.
        objects : list[Object3D], optional
            List of 3D objects to be rendered. Default is None.
        functions : list[Function3D], optional
            List of 3D functions to be rendered. Default is None.
        simulation_presets_allowed : bool, optional
            Whether to allow using simulation presets if one is provided. Default is True.
        model_size_type : str, optional
            Type of model size. Default is "exaggerated", but can be "realistic".
        model_saturation : bool, optional
            Whether to apply color saturation to the models. Default is True.
        camera_cinematic_settings : dict, optional
            Camera cinematic settings. Default is a dictionary with specific values.
        """
        self.window_size = window_size
        self.framerate = framerate
        self.fullscreen = fullscreen
        self.running = True

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        
        self.pressed_inputs = set()       # Keep track of pressed keys
        
        self.input = MasterInput()
        self.display = Display(self)

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(self.window_size, flags=pg.OPENGL | pg.DOUBLEBUF)
        if fullscreen: pg.display.toggle_fullscreen()

        # Mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        self.context = mgl.create_context()
        self.context.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)       # Allows for depth testing (z-buffering)
        self.camera_delta_time = 0                                   # Used for constant camera speed regardless of fps
        self.saturated = model_saturation

        self.light = Light(
            position=light_position, 
            color=light_color,
            ambient_intensity=light_ambient_intensity,
            diffuse_intensity=light_diffuse_intensity,
            specular_intensity=light_specular_intensity
        )
        self.camera = Camera(
            app=self,
            position=camera_origin,
            speed=camera_speed,
            sensitivity=camera_sensitivity,
            fov=camera_fov,
            near_render_distance=camera_near_render_distance,
            far_render_distance=camera_far_render_distance,
            yaw=camera_yaw,
            pitch=camera_pitch,
            # cinematic_settings=camera_cinematic_settings
        )

        self.world = world

        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)

    def quit(self):
        self.scene.destroy()
        self.display.destroy()
        pg.quit()
        self.running = False

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.quit()
            # else:
            #     self.filter_event(event)

    # def check_keyboard_event(self, event):
        # elif self.key_mode == "camera":
        #     for i in range(1,10):
        #         if event.key == getattr(pg, f"K_{i}"):
        #             if i <= 5:
        #                 self.camera.current_speed_modifier = 1 / 5**3 * i**3
        #             else:
        #                 self.camera.current_speed_modifier = 1 / 5**6 * i**6
        #             self.camera.current_speed_modifier_i = i
        #             break

    # def check_controller_event(self, event):
    #     if self.key_mode == "presets":
    #         if event.button == 11:
    #             self.current_preset_i += 1
    #         elif event.button == 12:
    #             self.current_preset_i -= 1
    #         self.current_preset_i = max(self.current_preset_i, 0)
    #         self.physics_speed = round((10**(2.4)*self.current_preset_i)**2 + 1)

    #     elif self.key_mode == "camera":
    #         if event.button == 11:
    #             self.camera.current_speed_modifier_i += 1
    #         elif event.button == 12:
    #             self.camera.current_speed_modifier_i -= 1
    #         self.camera.current_speed_modifier_i = max(self.camera.current_speed_modifier_i, 0)
    #         if self.camera.current_speed_modifier_i <= 5:
    #             self.camera.current_speed_modifier = 1 / 5**3 * self.camera.current_speed_modifier_i**3
    #         else:
    #             self.camera.current_speed_modifier = 1 / 5**6 * self.camera.current_speed_modifier_i**6

    #     if event.button == 0 and "camera" in self.key_modes:
    #         self.camera.cycle_tracked_bodies()

    #     if event.button == 1 and "camera" in self.key_modes:
    #         self.camera.cycle_movement_modes()

    #     if event.button == 3 and "camera" in self.key_modes and self.scene.hidden_surfaces:
    #         self.scene.hidden_surfaces.append(self.scene.surfaces[0])
    #         self.scene.surfaces.remove(self.scene.surfaces[0])
    #         self.scene.surfaces.append(self.scene.hidden_surfaces[0])
    #         self.scene.hidden_surfaces.remove(self.scene.hidden_surfaces[0])


    #     if event.button == 14:
    #         current_mode_1 = self.key_modes.index(self.key_mode)
    #         self.key_mode = self.key_modes[(current_mode_1 + 1) % len(self.key_modes)]
    #         if self.key_mode == "manual":
    #             current_mode_1 = self.key_modes.index(self.key_mode)
    #             self.key_mode = self.key_modes[(current_mode_1 + 1) % len(self.key_modes)]
    #         self.key_string = ""

    #     if event.button == 13:
    #         current_mode_1 = self.key_modes.index(self.key_mode)
    #         self.key_mode = self.key_modes[(current_mode_1 - 1 + len(self.key_modes)) % len(self.key_modes)]
    #         if self.key_mode == "manual":
    #             current_mode_1 = self.key_modes.index(self.key_mode)
    #             self.key_mode = self.key_modes[(current_mode_1 - 1 + len(self.key_modes)) % len(self.key_modes)]
    #         self.key_string = ""

    #     if event.button == 6:
    #         self.quit()
            
    # def filter_event(self, event):
    #     if event.type == pg.KEYDOWN:
    #         if event.key not in self.pressed_inputs:
    #             self.check_keyboard_event(event)
    #             self.pressed_inputs.add(event.key)

    #     elif event.type == pg.KEYUP and event.key in self.pressed_inputs:
    #         self.pressed_inputs.remove(event.key)

    #     elif event.type == pg.JOYBUTTONDOWN:
    #         if event.button not in self.pressed_inputs:
    #             self.check_controller_event(event)
    #             self.pressed_inputs.add(event.button)
        
    #     elif event.type == pg.JOYBUTTONUP and event.button in self.pressed_inputs:
    #         self.pressed_inputs.remove(event.button)

    # @staticmethod
    # def is_int(value):
    #     try:
    #         int(value)
    #         return True
    #     except ValueError:
    #         return False

    def check_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def render(self):
        # Update scene and camera before to prevent flickering
        self.scene.update()
        self.camera.update()
        self.context.clear()
        self.scene_renderer.render()
        pg.display.flip()

    # def get_current_state(self):
    #     state = {
    #         "lEngine type" : self.__class__.__name__,
    #         "Simulation time (s)" : f"{self.simulation_time:.2e}",
    #         "lWindow size" : self.window_size,
    #         "Physics speed" : f"{self.physics_speed:.2e}",
    #         "lFramerate" : f"{0 if self.delta_time ==0 else self.physics_speed / self.delta_time:.1f}",
    #         "Camera pos (x,y,z)" : \
    #             f"{self.camera.position.x:.3f}, {-self.camera.position.z:.3f}, {self.camera.position.y:.3f}",
    #         "lNumber of inputs" : len(self.input.inputs),
    #         "Camera speed" : self.camera.current_speed_modifier_i,
    #         "lKey mode" : self.key_mode,
    #         "Tracked body index" : self.camera.current_tracked_body_index,
    #         "lModel size type" : self.model_size_type,
    #         "Camera movement mode" : self.camera.movement_mode,
    #         "lManual str" : self.key_string,
    #         "empty" : "   "
    #     }
    #     return state

    def run(self):
        while self.running:
            self.check_time()
            self.check_events()
            if self.running:
                self.render()
                self.delta_time = self.clock.tick(self.framerate) / 1000
                self.camera_delta_time = self.clock.tick(self.framerate)
                self.world.update(self.delta_time)
