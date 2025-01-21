from numpy import frombuffer, uint8, array_equal, array
from pygame import mouse


class CollisionDetector:
    def __init__(self, app):
        self.app = app
        self.off_screen_frame_buffer_object = self.app.context.framebuffer(
            color_attachments=[self.app.context.texture(self.app.window_size, 4)],
            depth_attachment=self.app.context.depth_renderbuffer(self.app.window_size)
        )
        self.collision = False
        self.background_color = array([33,64,92])   # random background color
        self.collision_radius = 10

    def clear(self):
        self.off_screen_frame_buffer_object.use()
        self.off_screen_frame_buffer_object.clear(*(self.background_color/255), 1.0)

    def update(self):
        if self.app.dev_mode:
            cursor_x, cursor_y = mouse.get_pos()
        else:
            beamage_pos = self.app.input.beamage.get_position()
            if beamage_pos is not None:
                cursor_x, cursor_y = beamage_pos
                cursor_y = self.app.window_size[1] - cursor_y
                mouse.set_pos(cursor_x, cursor_y)

        if cursor_x is not None and cursor_y is not None:
            cursor_y = self.app.window_size[1] - cursor_y
            # Define the viewport to read a block of pixels around the cursor
            radius = self.collision_radius
            min_x = max(0, cursor_x - radius)
            min_y = max(0, cursor_y - radius)
            width = min(self.app.window_size[0], cursor_x + radius + 1) - min_x
            height = min(self.app.window_size[1], cursor_y + radius + 1) - min_y

            # Read the block of pixels
            pixel_data = frombuffer(self.off_screen_frame_buffer_object.read(
                viewport=(min_x, min_y, width, height)), dtype=uint8
            ).reshape((height, width, 3))
            
            # Check each pixel in the block
            self.collision = any(
                not array_equal(pixel_data[dy, dx, :3], self.background_color)
                for dx in range(width) for dy in range(height)
            )
        else:
            self.collision = False
