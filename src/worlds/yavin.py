import numpy as np
from glm import vec3

from src.engine.elements import Object
from src.engine.models import *
from src.worlds.world import World


class Yavin(World):
    def __init__(self):
        # self.corvette = Object(
        #     position=vec3(0,0,0),
        #     rotation=vec3(0,0,0),#-2900
        #     scale=vec3(1,1,1),
        #     model=Corvette,
        #     instance=None#CorvetteAI(vec3(0,0,-10))
        # )

        self.millenium_falcon = Object(
            model=MilleniumFalcon,
            instance=MilleniumFalconAI()
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
        self.health_bar = Object(
            texture="red",
            model=Cube,
            instance=HealthBar(),#self.health),
            saturated=True
        )


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


# class MilleniumFalconAI:
#     def __init__(self):
#         self.position = vec3(0,100,0)
#         self.rotation = vec3(0,0,0)
#         self.scale = vec3(1,1,1)

#     def update(self, app):
#         pass



# class MilleniumFalconAI:
#     def __init__(self):
#         self.position = vec3(0, 20, 0)
#         self.rotation = vec3(0, 0, 0)  # Euler angles or use quaternions
#         self.scale = vec3(1, 1, 1)
#         self.max_speed = 1
#         self.turn_speed = 0.05  # Adjust for smoothness
#         self.velocity = vec3(0, 0, 0)


class MilleniumFalconAI:
    def __init__(self):
        self.position = glm.vec3(0, 100, 0)
        self.min_distance = 50  # Minimum allowed distance from the camera
        self.max_distance = 200  # Maximum allowed distance from the camera
        self.speed = 2.0  # Movement speed
        self.scale = vec3(10,10,10)
        self.rotation = vec3(0, 0, 0)
    
    def update(self, app):
        pass
    #     direction = glm.normalize(app.camera.position - self.position)
    #     distance = glm.length(app.camera.position - self.position)

    #     # Ensure the object stays within the FOV bounds
    #     if distance < app.camera.FOV:
    #         self.position -= direction * self.speed
    #     elif distance > app.camera.FOV:
    #         self.position += direction * self.speed

    #     # Update rotation to face the camera
    #     self.rotation.y = glm.degrees(glm.atan(direction.z, direction.x))

    # def get_transform(self):
    #     return glm.translate(glm.mat4(1.0), self.position) * glm.rotate(
    #         glm.mat4(1.0), glm.radians(self.rotation.y), glm.vec3(0, 1, 0)) * glm.scale(glm.mat4(1.0), self.scale)

    # def update(self, app):
    #     camera = app.camera
    #     camera_pos = camera.position
    #     camera_forward = camera.forward
    #     fov = camera.FOV
        
    #     # 1. Check if within FOV
    #     if not self.is_within_fov(camera_pos, camera_forward, fov):
    #         # Reorient and steer towards center of FOV
    #         self.steer_towards_center(camera_pos, camera_forward)
        
    #     # 2. Update position based on current velocity
    #     self.position += self.velocity * app.delta_time
        
    #     # 3. Update rotation smoothly
    #     self.smooth_turn(camera_pos, camera_forward)
    
    # def is_within_fov(self, camera_pos, camera_forward, fov):
    #     # Vector from camera to starship
    #     to_starship = self.position - camera_pos
    #     to_starship_normalized = glm.normalize(to_starship)
    #     camera_forward_normalized = glm.normalize(camera_forward)
        
    #     # Calculate angle between camera forward and to_starship
    #     dot_product = glm.dot(to_starship_normalized, camera_forward_normalized)
    #     angle = np.arccos(dot_product)
        
    #     # Check if within FOV
    #     return angle < np.radians(fov / 2)
    
    # def steer_towards_center(self, camera_pos, camera_forward):
    #     # Calculate desired direction towards the center of the FOV
    #     to_starship = self.position - camera_pos
    #     target_direction = camera_forward
        
    #     # Calculate the desired velocity in that direction
    #     desired_velocity = glm.normalize(target_direction - to_starship) * self.max_speed
        
    #     # Adjust current velocity towards the desired velocity (steering behavior)
    #     steering_force = desired_velocity - self.velocity
    #     self.velocity += steering_force  # You can scale it for smoother steering
    
    # def smooth_turn(self, camera_pos, camera_forward):
    #     # Vector from the starship to the camera
    #     to_starship = camera_pos - self.position
        
    #     # Current orientation of the starship (you could store this as a quaternion)
    #     current_rotation = R.from_euler('xyz', self.rotation)  # Current Euler angles to rotation

    #     # Target direction the ship needs to face (toward the camera or center of FOV)
    #     target_direction = glm.normalize(camera_forward)
        
    #     # Convert target direction to a quaternion rotation
    #     # Assuming the target direction is along the z-axis for simplicity
    #     target_rotation = R.from_rotvec(np.array([0, 0, np.arctan2(target_direction.y, target_direction.x)]))  # Simplify if facing along the Z-axis

    #     # Create SLERP object for smooth interpolation between current and target rotation
    #     slerp = Slerp([0, 1], R.from_euler('xyz', [self.rotation, target_rotation.as_euler('xyz')]))

    #     # Apply slerp to interpolate between current and target over time
    #     smooth_rotation = slerp(self.turn_speed).as_euler('xyz')

    #     # Update the starship's rotation to the smoothed rotation
    #     self.rotation = glm.vec3(smooth_rotation)
