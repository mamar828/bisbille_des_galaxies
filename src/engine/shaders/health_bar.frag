// #version 330
// in vec2 fragTexCoord;
// out vec4 fragColor;

// uniform float health_percentage;  // Value between 0.0 and 1.0

// void main() {
//     // Check if the fragment is within the current health range
//     if (fragTexCoord.x <= health_percentage) {
//         fragColor = vec4(0.0, 1.0, 0.0, 1.0);  // Green for health
//     } else {
//         fragColor = vec4(0.8, 0.0, 0.0, 1.0);  // Red for missing health
//     }
// }



// #version 330 core
// in vec2 fragTexCoord;  // Texture coordinates from vertex shader

// uniform float health_percentage; // Health percentage to display
// uniform sampler2D u_texture;     // The texture for the health bar

// out vec4 fragColor;

// void main() {
//     vec4 color = texture(u_texture, fragTexCoord);
//     if (fragTexCoord.x > health_percentage) {
//         // Cut off the health bar past the health percentage
//         discard;
//     }
//     fragColor = color;
// }


#version 330

out vec4 FragColor;

void main() {
    // Output solid red color
    FragColor = vec4(1.0, 0.0, 0.0, 1.0);  // Red color with full opacity
}