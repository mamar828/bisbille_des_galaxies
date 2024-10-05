from glm import vec3

from src.engine.engine import Engine
from src.worlds.yavin import Yavin


engine = Engine(
    world=Yavin(),
    # window_size=(1920, 1080),
    window_size=(1440, 900),
    # window_size=(700, 700),
    framerate=60,
    # framerate=5,
    fullscreen=True,
    # fullscreen=False,
    light_position=vec3(0,0,100),
    light_color=vec3(1,1,1),
    light_ambient_intensity=0.1,
    light_diffuse_intensity=1.5,
    light_specular_intensity=1.0,
    camera_origin=(0,0,0),
    camera_speed=0.025,
    camera_sensitivity=0.1,
    camera_fov=50,
    camera_near_render_distance=0.05,
    camera_far_render_distance=1e20,
    camera_yaw=-90,
    camera_pitch=0,
    model_saturation=False,
)
engine.run()
