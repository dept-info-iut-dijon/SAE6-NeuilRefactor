#version 410 core

const vec3 ORIGIN = vec3(0, 0, 1);

in vec2 v_text;
out vec4 f_color;

uniform vec2 resolution;

uniform mat3 morphInv;
uniform mat3 similarity;

uniform int glide;

uniform sampler2D tileTexture;
uniform vec2 tileCorner0;
uniform vec2 tileCorner1;
uniform vec2 tileCorner2;
uniform vec2 tileCorner3;


mat3 PRE = mat3(
    0, 1, 0,
    1, 0, 0,
    0, 0, 1
);

vec3 TEST = vec3(2, 0, -1);
mat3 GT = mat3(
    1, 0, 0,
    0, -1, 0,
    -0.5, 1, 1
);

mat3 TEX = mat3(
    2, 0, 0,
    0, 1, 0,
    0, 0, 1
);

vec2 domainCoords(vec3 p) {
    if (glide == 1) {
        p = PRE * p;
    }
    if (dot(p, TEST) > 0.) {
        p = GT * p;
    }
    p = TEX * p;
    if (glide == 1) {
        p = PRE * p;
    }
    return p.xy;
}

vec2 tileCoords(vec2 p) {
    float x = p.x;
    float y = p.y;

    vec2 a0 = (1. - x) * (tileCorner3 - tileCorner0) + x * (tileCorner2 - tileCorner1);
    vec2 a1 = (1. - y) * (tileCorner1 - tileCorner0) + y * (tileCorner2 - tileCorner3);
    vec2 b = ((1. - y) * tileCorner0 + y * tileCorner3) - ((1. - x) * tileCorner0 + x * tileCorner1);
    mat2 a = mat2(a0, -a1);

    vec2 sol = inverse(a) * b;
    float theta = sol.x;
    return (1. - theta) * ((1. - x) * tileCorner0 + x * tileCorner1) + theta * ((1 - x) * tileCorner3 + x * tileCorner2);
}


void main() {
    vec3 q = vec3(v_text * (resolution / resolution.y), 1);
    q = similarity * q;
    vec3 p = vec3(mod(morphInv * q, 1.0).xy, 1.);
    vec2 dom = domainCoords(p);
    vec2 coords = tileCoords(dom);
    vec3 color = texture(tileTexture, coords).rgb;
    f_color = vec4(color, 1);
}