from src.engine.relative_paths import get_path


class ShaderProgram:
    def __init__(self, context):
        self.context =  context
        self.programs = {
            "default" : self.get_program("default"),
            "skybox" : self.get_program("skybox"),
            "shadow_map" : self.get_program("shadow_map"),
            "saturated" : self.get_program("saturated")
        }

    def get_program(self, shader_program_name):
        with open(get_path(f"shaders/{shader_program_name}.vert")) as file:
            vertex_shader = file.read()

        with open(get_path(f"shaders/{shader_program_name}.frag")) as file:
            fragment_shader = file.read()

        return self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        
    def destroy(self):
        [program.release() for program in self.programs.values()]
