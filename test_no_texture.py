import moderngl
import moderngl_window as mglw
import pywavefront
import numpy as np


class ObjViewer(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "OBJ Viewer Without Textures"
    window_size = (800, 600)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load the .obj model using pywavefront
        self.scene = pywavefront.Wavefront('src/engine/objects/corvette/Star Wars CORVETTE.obj', collect_faces=True)

        # Collect all vertices
        vertices = []
        for name, material in self.scene.materials.items():
            vertices.extend(material.vertices)

        # Convert the list of vertices to a numpy array
        self.vertices = np.array(vertices, dtype='f4')

        # Create a buffer to hold the vertex data
        self.vbo = self.ctx.buffer(self.vertices)

        # Simple vertex and fragment shaders (with basic transformation and no textures)
        self.program = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec3 in_vert;
            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 proj;
            void main() {
                gl_Position = proj * view * model * vec4(in_vert, 1.0);
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

        # Setup basic transformation matrices
        self.projection = self.create_perspective_matrix(45.0, self.window_size[0] / self.window_size[1], 0.1, 100.0)
        self.view = self.create_look_at_matrix(np.array([5, 2, 5]), np.array([0.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]))
        self.model = np.eye(4, dtype='f4') * 0.5  # Scale down the model

    def create_perspective_matrix(self, fov, aspect, z_near, z_far):
        f = 1.0 / np.tan(np.radians(fov) / 2.0)
        return np.array([
            [f / aspect, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (z_far + z_near) / (z_near - z_far), (2 * z_far * z_near) / (z_near - z_far)],
            [0, 0, -1, 0]
        ], dtype='f4')

    def create_look_at_matrix(self, eye, center, up):
        f = (center - eye)
        f = f / np.linalg.norm(f)
        u = up / np.linalg.norm(up)
        s = np.cross(f, u)
        u = np.cross(s, f)
        m = np.eye(4, dtype='f4')
        m[0, :3] = s
        m[1, :3] = u
        m[2, :3] = -f
        m[3, 0] = -np.dot(s, eye)
        m[3, 1] = -np.dot(u, eye)
        m[3, 2] = np.dot(f, eye)
        return m

    def render(self, time, frame_time):
        self.ctx.clear(0.2, 0.2, 0.2)
        self.ctx.enable(moderngl.DEPTH_TEST)

        # Bind and use the transformation matrices
        self.program['model'].write(self.model)
        self.program['view'].write(self.view)
        self.program['proj'].write(self.projection)

        # Render the model
        self.vao.render(moderngl.TRIANGLES)

    def resize(self, width, height):
        self.projection = self.create_perspective_matrix(45.0, width / height, 0.1, 100.0)
        self.ctx.viewport = (0, 0, width, height)


if __name__ == '__main__':
    mglw.run_window_config(ObjViewer)