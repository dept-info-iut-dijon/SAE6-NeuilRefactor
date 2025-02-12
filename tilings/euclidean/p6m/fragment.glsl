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


const float a = sqrt(3.) / 3;
const mat3 MORPH_INV = mat3(
    1, 0, 0,
    -a, 2 * a, 0,
    0, 0, 1
);

const vec3 TEST_C = vec3(1, 1, -1);
const mat3 ROT_C = mat3(
    -1, 0, 0,
    0, -1, 0,
    1, 1, 1
);

const vec3 TEST_S1 = vec3(1, 0.5, -0.5);
const mat3 SYM_1 = mat3(
    -1, 0, 0,
    -1, 1, 0,
    1, 0, 1
);

const vec3 TEST_S2 = vec3(-1, 1, 0);
const mat3 SYM_2 = mat3(
    0, 1, 0,
    1, 0, 0,
    0, 0, 1
);


const mat3 TEX = mat3(
    0, -2, 0,
    3, -1, 0,
    0, 1, 1
);


vec2 domainCoords(vec3 p) {
    if (dot(p, TEST_C) > 0.) {
        p = ROT_C * p;
    }
    if (dot(p, TEST_S1) > 0.) {
        p = SYM_1 * p;
    }
    if (dot(p, TEST_S2) > 0.) {
        p = SYM_2 * p;
    }
    if (dot(p, TEST_S1) > 0.) {
        p = SYM_1 * p;
    }
    p = TEX * p;
    return p.xy;
}

vec2 tileCoords(vec2 p) {
    return tileCorner0 + p.x * (tileCorner1 - tileCorner0) + p.y * (tileCorner2 - tileCorner0);
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