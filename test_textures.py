import moderngl
import moderngl_window as mglw
import pywavefront
import numpy as np
from PIL import Image


class ObjViewer(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "OBJ Viewer with Textures"
    window_size = (800, 600)
    aspect_ratio = 16 / 9

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load the .obj model using pywavefront
        self.scene = pywavefront.Wavefront('src/engine/objects/corvette/Star Wars CORVETTE.obj', collect_faces=True)

        vertices = []
        textures = []
        self.materials = {}

        # Iterate over each material in the scene
        for name, material in self.scene.materials.items():
            vertices.extend(material.vertices)

            # Access texture coordinates if available, otherwise fill with zeros
            if material.vertex_format == 'V3F T2F':
                texture_coords = material.vertex_data[3:]
                textures.extend(texture_coords)
            else:
                # If the material doesn't include texture coordinates, fill with zeros
                textures.extend([0.0, 0.0] * (len(material.vertices) // 3))

            # Load the texture image if not already loaded
            if material.texture and name not in self.materials:
                print(material.__dict__.keys())
                print(material.name)
                raise
                # print(name, material.texture.image_name)
                # self.materials[name] = self.load_texture(f"src/engine/objects/corvette/{material.texture.image_name}")
                self.materials[name] = self.load_texture(f"src/engine/objects/corvette/{name}.jpg")

        # Convert the lists to numpy arrays
        self.vertices = np.array(vertices, dtype='f4')
        self.textures = np.array(textures, dtype='f4')

        # Set up the ModernGL buffers and shaders
        self.vbo = self.ctx.buffer(self.vertices)
        self.tbo = self.ctx.buffer(self.textures)

        self.program = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec3 in_vert;
            in vec2 in_text;
            out vec2 v_text;
            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 proj;
            void main() {
                gl_Position = proj * view * model * vec4(in_vert, 1.0);
                v_text = in_text;
            }
            """,
            fragment_shader="""
            #version 330
            in vec2 v_text;
            out vec4 f_color;
            uniform sampler2D Texture;
            void main() {
                f_color = texture(Texture, v_text);
            }
            """
        )

        # Create vertex array object
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '3f', 'in_vert'), (self.tbo, '2f', 'in_text')]
        )

        # Set up projection and view matrices
        self.projection = self.create_perspective_matrix(45, self.aspect_ratio, 0.1, 100.0)
        self.view = self.create_look_at_matrix(np.array([3, 3, 3]), np.array([0, 0, 0]), np.array([0, 1, 0]))
        self.model = np.eye(4, dtype='f4')

    def load_texture(self, image_path):
        img = Image.open(image_path).transpose(Image.FLIP_TOP_BOTTOM).convert('RGB')
        texture = self.ctx.texture(img.size, 3, img.tobytes())
        texture.build_mipmaps()
        texture.use()
        return texture

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

        # Bind the textures and render the object
        for name, material in self.scene.materials.items():
            if name in self.materials:
                self.materials[name].use()
            self.program['model'].write(self.model)
            self.program['view'].write(self.view)
            self.program['proj'].write(self.projection)
            self.vao.render()

    def resize(self, width, height):
        self.projection = self.create_perspective_matrix(45, width / height, 0.1, 100.0)
        self.ctx.viewport = (0, 0, width, height)


if __name__ == '__main__':
    mglw.run_window_config(ObjViewer)