#version 410 core

in vec2 v_text;
out vec4 f_color;

uniform vec2 resolution;
const int iterations = 100;
uniform mat3 similarity;

uniform sampler2D tileTexture;
uniform vec2 tileCorner0;
uniform vec2 tileCorner1;
uniform vec2 tileCorner2;
uniform vec2 tileCorner3;

const vec3 TEST0 = vec3(1, 1, -1);

const vec3 TEST1P = vec3(-2, 1, 0);
const vec3 TEST1N = vec3(-1, 2, -1);
const vec3 TEST2P = vec3(2, -1, -1);
const vec3 TEST2N = vec3(1, -2, 0);

const float a = sqrt(3.) / 3.;
const mat3 MORPH_INV = mat3(
    1, 1, 0,
    -a, a, 0,
    0, 0, 1
);


const mat3 R1P = mat3(
    0, 1, 0,
    -1, -1, 0,
    1, 1, 1
);

const mat3 R1N = mat3(
    -1, -1, 0,
    1, 0, 0,
    0, 1, 1
);

const mat3 R2P = mat3(
    0, 1, 0,
    -1, -1, 0,
    1, 0, 1
);

const mat3 R2N = mat3(
    -1, -1, 0,
    1, 0, 0,
    1, 1, 1
);

const mat3 TEX = mat3(
    2, -1, 0,
    -1, 2, 0,
    0, 0, 1
);



vec2 domainCoords(vec3 p) {
    if (dot(p, TEST0) < 0. && dot(p, TEST1P) > 0.) {
        p = R1P * p;
    }
    if (dot(p, TEST0) > 0. && dot(p, TEST1N) > 0.) {
        p = R1N * p;
    }
    if (dot(p, TEST0) > 0. && dot(p, TEST2P) > 0.) {
        p = R2P * p;
    }
    if (dot(p, TEST0) < 0. && dot(p, TEST2N) > 0.) {
        p = R2N * p;
    }

    p = TEX * p;
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

    vec3 p = vec3(mod(MORPH_INV * q, 1.0).xy, 1.);
    vec2 dom = domainCoords(p);
    vec2 coords = tileCoords(dom);
    vec3 color = texture(tileTexture, coords).rgb;
    f_color = vec4(color, 1);
}