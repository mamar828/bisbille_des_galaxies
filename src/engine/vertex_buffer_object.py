import numpy as np
from pywavefront import Wavefront
from gzip import open as gzip_open
from os.path import exists
from pickle import dump, load
from pygame import transform, image
import json
import pygame as pg
from moderngl import NEAREST as mglNEAREST
from pywavefront import Wavefront

from src.engine.relative_paths import get_path


class VertexBufferObject:
    def __init__(self, app):
        self.app = app
        self.context = app.context
        self.vertex_buffer_objects = {
            "cube" : CubeVBO(self.context),
            "sphere" : SphereVBO(self.context),
            "skybox" : SkyboxVBO(self.context),
            "cat" : CatVBO(self.context),
        }

        for obj, data in self.app.loader.object_materials.items():
            for material, vertices in data:
                self.vertex_buffer_objects[f"{obj}_{material}"] = MaterialVBO(self.context, vertices)

    def destroy(self):
        [vbo.destroy() for vbo in self.vertex_buffer_objects.values()]


class BaseVertexBufferObject:
    def __init__(self, context):
        self.context = context
        self.vertex_buffer_object = self.get_vertex_buffer_object()
        self.format: str=None
        self.attrib: list=None

    def get_vertex_buffer_object(self):
        return self.context.buffer(self.get_vertex_data())
    
    def destroy(self):
        self.vertex_buffer_object.release()
    
    @staticmethod
    def get_data(vertices, indices):
        return np.array([vertices[i] for triangle in indices for i in triangle], dtype="f4")


class SkyboxVBO(BaseVertexBufferObject):
    def __init__(self, context):
        super().__init__(context)
        self.format = "3f"
        self.attribs = ["in_position"]
        
    def get_vertex_data(self):
        vertices = [
            (-1,-1, 1), ( 1,-1, 1), ( 1, 1, 1), (-1, 1, 1), # front
            (-1, 1,-1), (-1,-1,-1), ( 1,-1,-1), ( 1, 1,-1)  # back
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]

        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.flip(vertex_data, 1).copy(order="C")

        return vertex_data


class CubeVBO(BaseVertexBufferObject):
    def __init__(self, context):
        super().__init__(context)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]
    
    def get_vertex_data(self):
        vertices = [
            (-1,-1, 1), ( 1,-1, 1), ( 1, 1, 1), (-1, 1, 1), # front
            (-1, 1,-1), (-1,-1,-1), ( 1,-1,-1), ( 1, 1,-1)  # back
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]

        vertex_data = self.get_data(vertices, indices)

        # Texture related data
        tex_coord_vertices = [(0,0), (1,0), (1,1), (0,1)]
        tex_coord_indices = [
            (0,2,3), (0,1,2),
            (0,2,3), (0,1,2),
            (0,1,2), (2,3,0),
            (2,3,0), (2,0,1),
            (0,2,3), (0,1,2),
            (3,1,2), (3,0,1)
        ]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        # Lighting on all the different faces
        normals = np.array(
            [( 0, 0, 1) * 6,
             ( 1, 0, 0) * 6,
             ( 0, 0,-1) * 6,
             (-1, 0, 0) * 6,
             ( 0, 1, 0) * 6,
             ( 0,-1, 0) * 6],
             dtype="f4"
        ).reshape(36,3)

        return np.hstack([tex_coord_data, normals, vertex_data])


class External_VBO(BaseVertexBufferObject):
    def __init__(self, context):
        super().__init__(context)
        self.format = "2f 3f 3f"
        self.attribs = ["in_texcoord_0", "in_normal", "in_position"]

    def get_vertex_data(self, object_path):
        object_ = Wavefront(object_path, cache=True, parse=True, create_materials=True)
        obj = object_.materials.popitem()[1]
        return np.array(obj.vertices, dtype="f4")


class SphereVBO(External_VBO):
    def get_vertex_data(self):
        return super().get_vertex_data(get_path("objects/sphere/sphere.obj"))


class CatVBO(External_VBO):
    def get_vertex_data(self):
        return super().get_vertex_data(get_path("objects/cat/20430_Cat_v1_NEW.obj"))


class MaterialVBO(External_VBO):
    def __init__(self, context, vertices):
        self.vertices = vertices
        super().__init__(context)
        
    def get_vertex_data(self):
        return np.array(self.vertices, dtype="f4")


class CorvetteVBO(External_VBO):
    def get_vertex_data(self):
        object_ = Wavefront(
            get_path("objects/corvette/Star wars CORVETTE.obj"),
            strict=True,
            encoding="iso-8859-1",
            parse=True
        )
        vertex_data = {}
        for material in object_.materials.values():
            vertex_data[material.name] = np.array(material.vertices, dtype="f4")
        return vertex_data
            # if material.texture.image_name == "olderchrome0.jpg":
            #     return np.array(material.vertices, dtype="f4")
            #     vertices += material.vertices
            # else:
            #     continue
            # print(type(material.texture))
            # raise
            # print(material.__dict__.keys())
            # raise
            # tex_coords += material.texcoords
        # return np.hstack([np.array(tex_coords, dtype="f4"), np.array(vertices, dtype="f4")])
        # return np.array(np.vertices, dtype="f4")

    # def get_vertex_data2(self):
    #     return super().get_vertex_data(get_path("objects/corvette/TantiveIV.obj"))
    #     return super().get_vertex_data(get_path("objects/corvette/Star wars CORVETTE.obj"))



# class CorvetteVBO(External_VBO):
#     def __init__(self, context):
#         super().__init__(context)
#         with open(get_path("src/engine/objects/corvette/Star wars CORVETTE.obj.json")) as f:
#             textures = json.load(f)
#         for vertex_buffer in textures["vertex_buffers"]:
#             material = vertex_buffer["material"]
#             self.textures[material] = self.get_texture(get_path(f"src/engine/objects/corvette/{material}.jpg"))

#         self.vbos = self.create_vbos()

#     def load_textures(self, texture_paths):
#         textures = {}
#         for material, path in texture_paths.items():
#             textures[material] = self.context.texture(size=self.load_texture(path).get_size(), 
#                                                       components=3, 
#                                                       data=pg.image.tostring(self.load_texture(path), "RGB"))
#         return textures

#     def load_texture(self, path):
#         return pg.transform.flip(pg.image.load(path).convert(), flip_x=False, flip_y=True)
    
#     def create_vbos(self):
#         vbos = {}
#         json_data = self.load_json()
#         for material_data in json_data['vertex_buffers']:
#             material = material_data['material']
#             byte_offset = material_data['byte_offset']
#             byte_length = material_data['byte_length']
#             vertex_format = material_data['vertex_format']

#             vertex_data = self.load_vertex_data(byte_offset, byte_length)
#             vbos[material] = self.context.buffer(vertex_data)
#         return vbos
    
#     def load_vertex_data(self, byte_offset, byte_length):
#         # Load the vertex data from the file based on byte offset and length
#         with open('path_to_vertex_data_file', 'rb') as f:
#             f.seek(byte_offset)
#             return f.read(byte_length)

#     def load_json(self):
#         with open('path_to_corvette.json', "r") as f:
#             return json.load(f)

#     def render(self, material):
#         texture = self.textures[material]
#         texture.use(location=0)
#         vbo = self.vbos[material]
#         vao = self.context.vertex_array(self.program, [(vbo, self.format, *self.attribs)])
#         vao.render()
