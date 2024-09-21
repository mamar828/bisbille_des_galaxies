from numpy import frombuffer, uint8, array_equal
from pygame import mouse


class CollisionDetector:
    def __init__(self, app):
        self.app = app
        self.off_screen_frame_buffer_object = self.app.context.framebuffer(
            color_attachments=[self.app.context.texture(self.app.window_size, 4)],
            depth_attachment=self.app.context.depth_renderbuffer(self.app.window_size)
        )
        self.collision = False

    def clear(self):
        self.off_screen_frame_buffer_object.use()
        self.off_screen_frame_buffer_object.clear(0.0,0.0,0.0,1.0)

    def update(self):
        mouse_x, mouse_y = mouse.get_pos()
        mouse_y = self.app.window_size[1] - mouse_y  # Invert Y to match OpenGL's coordinate system
        pixel_data = frombuffer(self.off_screen_frame_buffer_object.read(
            viewport=(mouse_x, mouse_y, 1, 1)), dtype=uint8
        )
        if sum(pixel_data[:3]) > 0:  # Example color check (red)
            self.collision = True
        else:
            self.collision = True
