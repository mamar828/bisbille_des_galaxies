import moderngl
import moderngl_window as mglw
import numpy as np


class TriangleRenderer(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Simple Triangle"
    window_size = (800, 600)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Simple triangle vertices
        vertices = np.array([
            -0.6, -0.6, 0.0,  # Bottom-left
             0.6, -0.6, 0.0,  # Bottom-right
             0.0,  0.6, 0.0   # Top-center
        ], dtype='f4')

        # Create a buffer to hold the vertex data
        self.vbo = self.ctx.buffer(vertices)

        # Simple vertex and fragment shaders
        self.program = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec3 in_vert;
            void main() {
                gl_Position = vec4(in_vert, 1.0);
            }
            """,
            fragment_shader="""
            #version 330
            out vec4 f_color;
            void main() {
                f_color = vec4(0.2, 0.7, 0.2, 1.0);
            }
            """
        )

        # Create a vertex array object
        self.vao = self.ctx.vertex_array(self.program, [(self.vbo, '3f', 'in_vert')])

    def render(self, time, frame_time):
        self.ctx.clear(0.2, 0.2, 0.2)
        self.vao.render(moderngl.TRIANGLES)


if __name__ == '__main__':
    mglw.run_window_config(TriangleRenderer)