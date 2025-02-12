#version 410 core

const vec3 ORIGIN = vec3(0, 0, 1);

in vec2 v_text;
out vec4 f_color;

uniform vec2 resolution;

uniform mat3 morphInv;
uniform mat3 similarity;


uniform sampler2D tileTexture;
uniform vec2 tileCorner0;
uniform vec2 tileCorner1;
uniform vec2 tileCorner2;

const vec3 TEST_S = vec3(1, 1, -1);
const mat3 SYM = mat3(
    0, -1, 0,
    -1, 0, 0,
    1, 1, 1
);

vec2 domainCoords(vec3 p) {
    if (dot(p, TEST_S) > 0.) {
        p = SYM * p;
    }
    return p.xy;
}

vec2 tileCoords(vec2 p) {
    return tileCorner0 + p.x * (tileCorner1 - tileCorner0) + p.y * (tileCorner2 - tileCorner0);
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