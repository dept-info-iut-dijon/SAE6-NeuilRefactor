#version 410 core

const vec3 ORIGIN = vec3(0, 0, 1);

in vec2 v_text;
out vec4 f_color;
//
//uniform float depthSphere;
//uniform float radiusSphere;

uniform vec2 sphereData;

uniform vec2 resolution;
uniform mat3 isometry;

uniform sampler2D tileTexture;
uniform vec2 tileCorner0;
uniform vec2 tileCorner1;
uniform vec2 tileCorner2;

uniform mat3 shiftXP;
uniform mat3 shiftXN;
uniform mat3 shiftYP;
uniform mat3 shiftYN;
uniform mat3 shiftZP;
uniform mat3 shiftZN;


vec3 reduceError(vec3 p) {
    return normalize(p);
}

vec3 applyIsometry(mat3 isom, vec3 p) {
    vec3 res = isom * p;
    return reduceError(res);
}

vec2 tileCoords(vec3 p) {
    float sum = dot(p, vec3(1.0));
    vec3 aux = p / sum;
    return aux.x * tileCorner0 + aux.y * tileCorner1 + aux.z * tileCorner2;
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

    if (p.x >= 0 && p.y >= 0 && p.z >= 0) {
        face_id = 0;
    }
    if (p.x <= 0 && p.y >= 0 && p.z >= 0) {
        face_id = 1;
    }
    if (p.x >= 0 && p.y <= 0 && p.z >= 0) {
        face_id = 2;
    }
    if (p.x <= 0 && p.y <= 0 && p.z >= 0) {
        face_id = 3;
    }
    if (p.x >= 0 && p.y >= 0 && p.z <= 0) {
        face_id = 4;
    }
    if (p.x <= 0 && p.y >= 0 && p.z <= 0) {
        face_id = 5;
    }
    if (p.x >= 0 && p.y <= 0 && p.z <= 0) {
        face_id = 6;
    }
    if (p.x <= 0 && p.y <= 0 && p.z <= 0) {
        face_id = 7;
    }

    switch (face_id) {
        case 0: // +++
            break;
        case 1: // -++
            p = applyIsometry(shiftZN, p);
            break;
        case 2: // +-+
            p = applyIsometry(shiftZP, p);
            break;
        case 3: // -++
            p = applyIsometry(shiftZP, p);
            p = applyIsometry(shiftZP, p);
            break;
        case 4: // ++-
            p = applyIsometry(shiftYP, p);
            p = applyIsometry(shiftYP, p);
            p = applyIsometry(shiftZN, p);
            break;
        case 5: // -+-
            p = applyIsometry(shiftYP, p);
            p = applyIsometry(shiftYP, p);
            break;
        case 6: // +--
            p = applyIsometry(shiftYP, p);
            p = applyIsometry(shiftYP, p);
            p = applyIsometry(shiftZN, p);
            p = applyIsometry(shiftZN, p);
            break;
        case 7: // ---
            p = applyIsometry(shiftYP, p);
            p = applyIsometry(shiftYP, p);
            p = applyIsometry(shiftZP, p);
            break;
    }

    vec2 coords = tileCoords(p);
    vec3 color = texture(tileTexture, coords).rgb;
    f_color = vec4(color, 1);
}