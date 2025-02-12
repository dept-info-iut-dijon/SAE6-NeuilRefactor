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


const vec3 TEST_S = vec3(1, 1, -1);
const mat3 SYM = mat3(
    0, -1, 0,
    -1, 0, 0,
    1, 1, 1
);

const vec3 TEST_R = vec3(1, 0.5, -0.5);
const vec3 TEST_RP = vec3(-1, 1, 0);
const vec3 TEST_RN = vec3(1, 2, -1);
const mat3 ROT_P = mat3(
    -1, 1, 0,
    -1, 0, 0,
    1, 0, 1
);
const mat3 ROT_N = mat3(
    0, -1, 0,
    1, -1, 0,
    0, 1, 1
);

const mat3 TEX = mat3(
    -1, 1, 0,
    -2, -1, 0,
    1, 0, 1
);

vec2 domainCoords(vec3 p) {
    if (dot(p, TEST_S) > 0.) {
        p = SYM * p;
    }
    if (dot(TEST_R, p) < 0. && dot(TEST_RP, p) > 0.) {
        p = ROT_P * p;
    }
    if (dot(TEST_R, p) > 0. && dot(TEST_RN, p) > 0.) {
        p = ROT_N * p;
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