from glm import vec3, lookAt


class Light:
    def __init__(
            self,
            position: vec3=vec3(0,0,0),
            color: vec3=vec3(1,1,1),
            ambient_intensity=0.1,
            diffuse_intensity=2,
            specular_intensity=1.0
    ):
        # Light positioning should be made for the camera to be able to see the whole scene at the light position for
        # shadows to correctly work
        self.position = position
        self.color = color
        self.direction = vec3(0,0,0)
        # Intensities of different lights
        self.Ia = ambient_intensity * self.color    # Ambient intensity
        self.Id = diffuse_intensity * self.color    # Diffuse intensity
        self.Is = specular_intensity * self.color   # Specular intensity
        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        return lookAt(self.position, self.direction, vec3(0,1,0))
