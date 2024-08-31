from pywavefront import Wavefront

from src.engine.vertex_buffer_object import VertexBufferObject
from src.engine.shader_program import ShaderProgram
from src.engine.relative_paths import get_path


class VertexArrayObject:
    def __init__(self, app):
        self.context =  app.context
        self.vertex_buffer_object = VertexBufferObject(app)
        self.program = ShaderProgram(self.context)
        self.vertex_array_objects = {
            "skybox" : self.get_vertex_array_object(
                    program=self.program.programs["skybox"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects["skybox"]),
        }
        for obj in ["cube", "sphere", "cat"]:
            self.vertex_array_objects.update({
                obj : self.get_vertex_array_object(
                    program=self.program.programs["default"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects[obj]
                ),
                f"shadow_{obj}" : self.get_vertex_array_object(
                    program=self.program.programs["shadow_map"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects[obj]
                ),
                f"saturated_{obj}" : self.get_vertex_array_object(
                    program=self.program.programs["saturated"],
                    vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects[obj]
                )
            })

        # self.vertex_array_objects_materials = {}
        # for obj in ["corvette"]:
        #     path = get_path(f"objects/{obj}")
        #     materials = []
        #     for material in Wavefront(f"{path}/Star Wars CORVETTE.obj", collect_faces=True).materials.values():
        #         materials.append((material.name, material.vertices))
        #     self.vertex_array_objects_materials[obj] = materials

        for obj, data in self.vertex_buffer_object.object_materials.items():
            for material, vertices in data:
                self.vertex_array_objects.update({
                    f"{obj}_{material}" : self.get_vertex_array_object(
                        program=self.program.programs["default"],
                        vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects[f"{obj}_{material}"]
                    ),
                    f"shadow_{obj}_{material}" : self.get_vertex_array_object(
                        program=self.program.programs["shadow_map"],
                        vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects[f"{obj}_{material}"]
                    ),
                    f"saturated_{obj}_{material}" : self.get_vertex_array_object(
                        program=self.program.programs["saturated"],
                        vertex_buffer_object=self.vertex_buffer_object.vertex_buffer_objects[f"{obj}_{material}"]
                    )
                })

    def get_vertex_array_object(self, program, vertex_buffer_object):
        vbo = vertex_buffer_object
        return self.context.vertex_array(program, [(vbo.vertex_buffer_object, vbo.format, *vbo.attribs)],
                                         skip_errors=True)    # Skip errors if the VAO is not complete

    def destroy(self):
        self.vertex_buffer_object.destroy()
        self.program.destroy()
