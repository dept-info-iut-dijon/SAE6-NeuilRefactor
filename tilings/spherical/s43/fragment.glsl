#version 410 core

const vec3 ORIGIN = vec3(0, 0, 1);

in vec2 v_text;
out vec4 f_color;

uniform vec2 sphereData;
uniform vec2 resolution;
uniform mat3 isometry;

uniform sampler2D tileTexture;
uniform vec2 tileCorner0;
uniform vec2 tileCorner1;
uniform vec2 tileCorner2;
uniform vec2 tileCorner3;

uniform mat3 shiftXP;
uniform mat3 shiftXN;
uniform mat3 shiftYP;
uniform mat3 shiftYN;


vec3 reduceError(vec3 p) {
    return normalize(p);
}

vec3 applyIsometry(mat3 isom, vec3 p) {
    vec3 res = isom * p;
    return reduceError(res);
}

vec2 tileCoords(vec3 p) {
    vec2 proj_coords = p.xy / p.z;
    vec2 aux = clamp(0.5 * proj_coords + vec2(0.5), vec2(0, 0), vec2(1, 1));

    float x = aux.x;
    float y = aux.y;

    vec2 a0 = (1. - x) * (tileCorner3 - tileCorner0) + x * (tileCorner2 - tileCorner1);
    vec2 a1 = (1. - y) * (tileCorner1 - tileCorner0) + y * (tileCorner2 - tileCorner3);
    vec2 b = ((1. - y) * tileCorner0 + y * tileCorner3) - ((1. - x) * tileCorner0 + x * tileCorner1);
    mat2 a = mat2(a0, -a1);

    vec2 sol = inverse(a) * b;
    float theta = sol.x;
    return (1. - theta) * ((1. - x) * tileCorner0 + x * tileCorner1) + theta * ((1 - x) * tileCorner3 + x * tileCorner2);
}

vec3 proj_inverse_sphere(vec2 m) {
    float depthSphere = sphereData.x;
    float radiusSphere = sphereData.y;
    float aux0 = depthSphere * depthSphere - radiusSphere * radiusSphere;
    vec3 f = vec3(0, 0, sqrt(aux0) / radiusSphere);
    vec3 fc = vec3(0, 0, -depthSphere);
    vec3 fm = vec3(m, 0) - f;
    float aux1 = dot(fc, fm);
    float aux2 = dot(fm, fm);
    float lambda = (aux1 - sqrt(aux1 * aux1 - aux2 * aux0)) / aux2;
    return normalize(-fc + lambda * fm);
}


void main() {
    vec2 m = 1.2 * v_text * (resolution / resolution.y);

    if (length(m) > 1.) {
        f_color = vec4(1, 1, 1, 1);
        return;
    }

    vec3 q = proj_inverse_sphere(m);

    int face_id;
    vec3 p = applyIsometry(isometry, q);

    float ax = abs(p.x);
    float ay = abs(p.y);
    float az = abs(p.z);

    if (az >= ax && az >= ay) {
        if (p.z > 0.) face_id = 0;
        else face_id = 1;
    }
    if (ax >= ay && ax >= az) {
        if (p.x > 0.) face_id = 2;
        else face_id = 3;
    }
    if (ay >= az && ay >= ax) {
        if (p.y > 0.) face_id = 4;
        else face_id = 5;
    }

    switch (face_id) {
        case 0:
            break;
        case 1:
            p = applyIsometry(shiftXN, p);
            p = applyIsometry(shiftXN, p);
            break;
        case 2:
            p = applyIsometry(shiftYP, p);
            break;
        case 3:
            p = applyIsometry(shiftYN, p);
            break;
        case 4:
            p = applyIsometry(shiftXP, p);
            break;
        case 5:
            p = applyIsometry(shiftXN, p);
            break;
    }

    vec2 coords = tileCoords(p);
    vec3 color = texture(tileTexture, coords).rgb;
    f_color = vec4(color, 1);
}