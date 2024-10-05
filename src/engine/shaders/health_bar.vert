// #version 330
// in vec2 in_vert;        // Vertex position
// in vec2 in_tex;         // Texture coordinates
// out vec2 fragTexCoord;  // Pass to fragment shader

// uniform mat4 proj;  // Orthographic projection matrix

// void main() {
//     fragTexCoord = in_tex;  // Pass texture coordinates to the fragment shader
//     gl_Position = proj * vec4(in_vert, 0.0, 1.0);  // Project the vertex position
// }


#version 330

in vec2 in_vert;
in vec2 in_tex;
out vec2 v_tex;

uniform mat4 proj;

void main() {
    gl_Position = proj * vec4(in_vert, 0.0, 1.0);  // Position transformed by the projection matrix
    v_tex = in_tex;  // Pass the texture coordinates to the fragment shader (though unused for now)
}