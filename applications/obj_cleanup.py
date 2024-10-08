import os

def triangulate_face(vertices):
    """
    Convert a polygon face into triangles.
    Assumes input is a list of vertices (e.g., [v1, v2, v3, v4]).
    Returns a list of face lines, each containing 3 vertices.
    """
    triangles = []
    # Create triangles by connecting the first vertex with each subsequent pair of vertices
    for i in range(1, len(vertices) - 1):
        triangles.append([vertices[0], vertices[i], vertices[i + 1]])
    return triangles

def preprocess_obj_file(path, filename):
    obj_path = os.path.join(path, filename)
    new_obj_path = os.path.join(path, "processed_" + filename)

    with open(obj_path, 'r') as infile, open(new_obj_path, 'w') as outfile:
        for line in infile:
            if line.startswith("f "):
                vertices = line.split()[1:]
                new_vertices = []
                for vertex in vertices:
                    # Split vertex attributes (v/vt/vn format)
                    parts = vertex.split("/")
                    # Ensure all vertices have the same number of components
                    if len(parts) == 3:
                        # All components are present (v, vt, vn)
                        new_vertices.append(vertex)
                    elif len(parts) == 2:
                        # Missing normals, add dummy normal index
                        new_vertices.append(f"{parts[0]}/{parts[1]}/0")
                    elif len(parts) == 1:
                        # Missing texture and normals, add dummy indices
                        new_vertices.append(f"{parts[0]}/0/0")
                    else:
                        # Handle malformed lines (if any)
                        new_vertices.append(f"{parts[0]}/0/0")
                
                # If the face has more than 3 vertices, triangulate it
                if len(new_vertices) > 3:
                    triangles = triangulate_face(new_vertices)
                    for triangle in triangles:
                        outfile.write(f"f {' '.join(triangle)}\n")
                else:
                    # Write the face as is (triangle or quad)
                    outfile.write(f"f {' '.join(new_vertices)}\n")
            else:
                # Write other lines unchanged
                outfile.write(line)

    return new_obj_path

# Example usage:
path = "src/engine/objects/tie_fighter"
filename = "tie.obj"
new_filename = preprocess_obj_file(path, filename)
print(f"Processed OBJ file saved as: {new_filename}")
