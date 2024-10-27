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
        cursor_x, cursor_y = None, None
        if self.app.dev_mode:
            cursor_x, cursor_y = mouse.get_pos()
        if not self.app.dev_mode:
            beamage_pos = self.app.input.beamage.get_position()
            if beamage_pos is not None:
                cursor_x, cursor_y = beamage_pos
                # cursor_y = self.app.window_size[1] - cursor_y
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


        # if cursor_x is not None and cursor_y is not None:
        #     cursor_y = self.app.window_size[1] - cursor_y  # Invert Y to match OpenGL's coordinate system
        #     pixel_data = frombuffer(self.off_screen_frame_buffer_object.read(
        #         viewport=(cursor_x, cursor_y, 1, 1)), dtype=uint8
        #     )
        #     if not array_equal(pixel_data[:3], self.background_color) and cursor_y != self.app.window_size[1]:
        #         self.collision = True
        #     else:
        #         self.collision = False
        # else:
        #     self.collision = False


        # if cursor_x is not None and cursor_y is not None:
        #     cursor_y = self.app.window_size[1] - cursor_y  # Invert Y to match OpenGL's coordinate system
        #     radius = self.collision_radius

        #     # Define a grid of points around the cursor
        #     collision_detected = False
        #     for dx in range(-radius, radius + 1):
        #         for dy in range(-radius, radius + 1):
        #             sample_x, sample_y = cursor_x + dx, cursor_y + dy
                    
        #             # Skip positions outside the window bounds
        #             if (0 <= sample_x < self.app.window_size[0] and
        #                     0 <= sample_y < self.app.window_size[1]):
                        
        #                 # Read pixel data at the sample position
        #                 pixel_data = frombuffer(self.off_screen_frame_buffer_object.read(
        #                     viewport=(sample_x, sample_y, 1, 1)), dtype=uint8
        #                 )
                        
        #                 # Check if pixel color matches anything other than background color
        #                 if not array_equal(pixel_data[:3], self.background_color):
        #                     collision_detected = True
        #                     break
        #         if collision_detected:
        #             break
            
        #     self.collision = collision_detected
        # else:
        #     self.collision = False
