import moderngl
import moderngl_window as mglw
import numpy as np
import json
from pyrr import Matrix44


# class ModelViewer(mglw.WindowConfig):
#     gl_version = (3, 3)
#     title = "3D Model Viewer"
#     window_size = (1280, 720)
#     resource_dir = '.'
#     aspect_ratio = 16 / 9
#     resizable = True

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.prog = self.load_program(
#             vertex_shader='''
#             #version 330
#             uniform mat4 model;
#             uniform mat4 view;
#             uniform mat4 proj;
#             in vec3 in_vert;
#             in vec3 in_norm;
#             in vec2 in_text;
#             out vec3 v_norm;
#             out vec2 v_text;
#             void main() {
#                 v_norm = in_norm;
#                 v_text = in_text;
#                 gl_Position = proj * view * model * vec4(in_vert, 1.0);
#             }
#             ''',
#             fragment_shader='''
#             #version 330
#             in vec3 v_norm;
#             in vec2 v_text;
#             out vec4 fragColor;
#             void main() {
#                 fragColor = vec4(abs(v_norm), 1.0); // simple coloring based on normals
#             }
#             '''
#         )

#         self.load_model_data('src/engine/objects/corvette/Star wars CORVETTE.obj.json')
#         self.setup_matrices()

#     def load_model_data(self, json_file):
#         with open(json_file, 'r') as file:
#             model_data = json.load(file)

#         self.vertex_buffers = []
#         for v_buffer in model_data['vertex_buffers']:
#             # Simulate loading binary data (in a real case, you'd load this from a file)
#             byte_offset = v_buffer['byte_offset']
#             byte_length = v_buffer['byte_length']
#             buffer_data = np.zeros(byte_length // 4, dtype=np.float32)  # Placeholder for real data

#             # Load the data
#             vertex_data = self.load_vertex_data(buffer_data)

#             # Create ModernGL buffer
#             vbo = self.ctx.buffer(vertex_data.tobytes())

#             # Assign vertex attributes based on the format
#             vao_content = [
#                 (vbo, '2f 3f 3f', 'in_text', 'in_norm', 'in_vert')
#             ]

#             # Create VAO
#             vao = self.ctx.vertex_array(self.prog, vao_content)

#             self.vertex_buffers.append((v_buffer['material'], vao))

#     def load_vertex_data(self, buffer):
#         byte_data = np.frombuffer(buffer, dtype=np.float32)
#         return byte_data

#     def setup_matrices(self):
#         proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
#         view = Matrix44.look_at(
#             eye=(3.0, 3.0, 3.0),
#             target=(0.0, 0.0, 0.0),
#             up=(0.0, 1.0, 0.0)
#         )
#         self.prog['proj'].write(proj.astype('float32').tobytes())
#         self.prog['view'].write(view.astype('float32').tobytes())

#     def render(self, time, frame_time):
#         self.ctx.clear(0.2, 0.3, 0.3)
#         model = Matrix44.identity()
#         self.prog['model'].write(model.astype('float32').tobytes())

#         for material, vao in self.vertex_buffers:
#             vao.render(moderngl.TRIANGLES)


# if __name__ == '__main__':
#     mglw.run_window_config(ModelViewer)



# import pywavefront
# from pywavefront import visualization

# # [create a window and set up your OpenGl context]
# obj = pywavefront.Wavefront('src/engine/objects/corvette/Star wars CORVETTE.obj')

# # [inside your drawing loop]
# visualization.draw(obj)


# print(np.array([16.51+16.62+16.65])/3)


# import numpy as np
# from PIL import Image

# Image()

# # Create a new image for the gradient
# gradient_img = Image.new("RGBA", img.size)

# # Create a gradient for the white spot
# width, height = gradient_img.size
# for y in range(height):
#     for x in range(width):
#         # Calculate the distance from the center
#         dx = x - width // 2
#         dy = y - height // 2
#         distance = np.sqrt(dx**2 + dy**2)
#         max_distance = min(width, height) // 4  # Adjust the size of the fading spot

#         # Determine the alpha based on distance
#         if distance < max_distance:
#             alpha = int(255 * (1 - (distance / max_distance)))  # Fade out
#             gradient_img.putpixel((x, y), (255, 255, 255, alpha))  # White with varying alpha
#         else:
#             gradient_img.putpixel((x, y), (0, 0, 0, 0))  # Transparent

# # Combine the green image and the gradient
# final_img = Image.alpha_composite(img.convert("RGBA"), gradient_img)

# # Save the final image
# output_path_with_gradient = "/mnt/data/green_dot_with_gradient.png"
# final_img.save(output_path_with_gradient)

# # output_path_with_gradient




# import pygame
# import numpy as np

# # Initialize Pygame
# pygame.init()

# # Screen dimensions
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption("3D Object Movement")

# # Colors
# black = (0, 0, 0)
# white = (255, 255, 255)

# # Object properties
# object_pos = np.array([0.0, 0.0, 5.0])  # Initial position in 3D space
# speed = 0.05  # Movement speed
# fov = 90  # Field of view in degrees
# min_distance = 2.0  # Minimum distance from the camera
# max_distance = 10.0  # Maximum distance from the camera

# # Function to update object position
# def update_position(pos):
#     direction = np.random.randn(3)  # Random direction
#     direction /= np.linalg.norm(direction)  # Normalize to keep speed constant
#     pos += direction * speed

#     # Ensure the object stays within the FOV and distance limits
#     distance = np.linalg.norm(pos)
#     if distance < min_distance:
#         pos = pos / distance * min_distance
#     elif distance > max_distance:
#         pos = pos / distance * max_distance

#     return pos

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Update object position
#     object_pos = update_position(object_pos)

#     # Clear screen
#     screen.fill(black)

#     # Project 3D position to 2D
#     x = int(width / 2 + object_pos * width / (2 * object_pos))
#     y = int(height / 2 - object_pos * height / (2 * object_pos))

#     # Draw object
#     pygame.draw.circle(screen, white, (x, y), 5)

#     # Update display
#     pygame.display.flip()

#     # Cap the frame rate
#     pygame.time.Clock().tick(60)

# pygame.quit()



print(int("0.00"))