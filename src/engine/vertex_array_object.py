from src.engine.vertex_buffer_object import VertexBufferObject
from src.engine.shader_program import ShaderProgram


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
        for obj in ["cube", "sphere", "cat", "corvette"]:
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

    def get_vertex_array_object(self, program, vertex_buffer_object):
        vbo = vertex_buffer_object
        return self.context.vertex_array(program, [(vbo.vertex_buffer_object, vbo.format, *vbo.attribs)],
                                         skip_errors=True)    # Skip errors if the VAO is not complete

    def destroy(self):
        self.vertex_buffer_object.destroy()
        self.program.destroy()
