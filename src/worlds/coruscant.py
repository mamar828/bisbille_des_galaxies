import numpy as np
from glm import vec3

from src.engine.elements import *
from src.engine.models import *
from src.worlds.world import World


class Coruscant(World):
    def __init__(self):
        self.star_destroyer = Object(
            model=StarDestroyer,
            instance=StarDestroyerAI()
        )

        self.health_bar = Object(
            texture="red",
            model=Cube,
            instance=HealthBar(),
            saturated=True
        )


class StarDestroyerAI:
    def __init__(self):
        self.position = glm.vec3(0, 1500, 0)
        self.scale = vec3(5,5,5)
        self.rotation = vec3(0, 0, 0)
        self.forward = vec3(0, -1, 0)
        self.flag = False
    
    def update(self, app):
        t = app.time - 4
        dt = 1/app.framerate # app.delta_time
        self.forward = self.calculate_forward_vector()
        if 0 < (t%110) < 0.2:
            self.position += self.forward * (11400 * dt)
        elif (t%110) < 5:
            self.position += self.forward * (70 * dt)
        elif (t%110) < 8:
            if not self.flag:       # make sure the start position is coherent
                self.position = vec3(0, 200, 0)
                self.flag = True
            self.position += self.forward * (40 * dt)
            self.rotation += vec3(0, 1, 0) * dt
        elif (t%110) < 21:
            self.flag = False
            self.position += self.forward * (20 * dt)
            self.rotation += vec3(-0.6, 0, 0) * dt
        elif (t%110) < 24:
            self.position += self.forward * (30 * dt)
            self.rotation += vec3(0, 1, 0) * dt
        elif (t%110) < 27:
            self.position += self.forward * (30 * dt)
        elif (t%110) < 32:
            self.position += self.forward * (30 * dt)
            self.rotation += vec3(0.4, 0, 0) * dt
        elif (t%110) < 36:
            self.position += self.forward * (30 * dt)
            self.rotation += vec3(0, 0.5, -0.2) * dt
        elif (t%110) < 43:
            self.position += self.forward * (40 * dt)
            self.rotation += vec3(0.5, 0.0, 0.0) * dt
        elif (t%110) < 47:
            self.position += self.forward * (40 * dt)
            self.rotation += vec3(1, 0, 0) * dt
        elif (t%110) < 50:
            self.position += self.forward * (40 * dt)
            self.rotation += vec3(1, 0, 1) * dt
        elif (t%110) < 52:
            self.position += self.forward * (40 * dt)
            self.rotation += vec3(0, -0.5, 0) * dt
        elif (t%110) < 55:
            self.position += self.forward * (40 * dt)
            self.rotation += vec3(-0.5, 0, 0) * dt
        elif (t%110) < 60:
            self.position += self.forward * (40 * dt)
            self.rotation += vec3(0, 0.5, 0) * dt
        elif (t%110) < 68:
            self.position += self.forward * (40 * dt)
            self.rotation += vec3(-0.5, 0, -0.3) * dt
        elif (t%110) < 72:
            self.position += self.forward * (20 * dt)
            self.rotation += vec3(-0.2, 0.5, 0.0) * dt
        elif (t%110) < 75:
            self.position += self.forward * (20 * dt)
            self.rotation += vec3(0, -0.5, 0.0) * dt
        elif (t%110) < 80:
            self.position += self.forward * (30 * dt)
            self.rotation += vec3(0.1, 0.1, 0.1) * dt
        elif (t%110) < 83:
            self.position += self.forward * (30 * dt)
            self.rotation += vec3(0, 0, 0.4) * dt
        elif (t%110) < 90:
            self.position += self.forward * (30 * dt)
            self.rotation += vec3(0, 0.7, 0.5) * dt
        elif (t%110) < 95:
            self.position += self.forward * (30 * dt)
            self.rotation += vec3(0.2, -0.5, 0) * dt
        elif (t%110) < 105:
            self.position += self.forward * (40 * dt)
        elif (t%110) < 107:
            self.position += self.forward * (10000 * dt)
        else:
            self.position = glm.vec3(0, 1500, 0)
            self.rotation = vec3(0, 0, 0)
    
    def calculate_forward_vector(self):
        rotation_matrix = glm.mat4(1.0)  # Identity matrix

        rotation_matrix = glm.rotate(rotation_matrix, self.rotation.y, glm.vec3(0, -1, 0))
        rotation_matrix = glm.rotate(rotation_matrix, self.rotation.x, glm.vec3(1, 0, 0))
        rotation_matrix = glm.rotate(rotation_matrix, self.rotation.z, glm.vec3(0, 0, 1))
        
        # Initial forward vector is (0, -1, 0) pointing downwards
        initial_forward = glm.vec4(0, -1, 0, 0)
        
        # Rotate the forward vector
        rotated_forward = rotation_matrix * initial_forward
        
        # Return the rotated forward vector as vec3
        return glm.vec3(rotated_forward)
