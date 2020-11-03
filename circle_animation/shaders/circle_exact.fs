#version 330 core

in vec2 pos;
in vec4 circleColor;
out vec4 FragColor;

void main() {
    float rsq = dot(pos, pos);
    if (rsq > 1)
        discard;
    FragColor = circleColor;
}
