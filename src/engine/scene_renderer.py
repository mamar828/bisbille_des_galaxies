class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.context = app.context
        self.mesh = app.mesh
        self.scene = app.scene
        # Shadow depth buffer
        self.depth_texture = self.mesh.texture.textures["depth_texture"]
        self.depth_frame_buffer_object = self.context.framebuffer(depth_attachment=self.depth_texture)

    def render_shadow(self):
        self.depth_frame_buffer_object.clear()
        self.depth_frame_buffer_object.use()
        for element in self.scene.elements:
            if not hasattr(element, "models") and element.shadow_program:
                element.render_shadow()

    def main_render(self):
        self.context.screen.use()
        if self.scene.elements:
            for element in self.scene.elements:
                element.render()
        self.scene.skybox.render()

    def render(self):
        # Render the elements to the collision frame buffer
        self.app.collision_detector.clear()
        if self.scene.elements:
            for element in self.scene.elements:
                if not element.instance.__class__.__name__ == "HealthBar":
                    element.render()

        # pass 1
        self.render_shadow()
        # pass 2
        self.main_render()
        self.app.collision_detector.update()

    def destroy(self):
        self.depth_frame_buffer_object.release()
