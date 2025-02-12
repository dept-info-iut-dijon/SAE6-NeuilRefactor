#version 410 core

const vec3 ORIGIN = vec3(0, 0, 1);
const float sqrt2 = sqrt(2.);

in vec2 v_text;
out vec4 f_color;

uniform vec2 resolution;
uniform int iterations;
uniform mat3 isometry;

//uniform vec2 tileSize;
uniform vec2 tileData;
uniform sampler2D tileTexture;
uniform vec2 tileCorner0;
uniform vec2 tileCorner1;
uniform vec2 tileCorner2;
uniform vec2 tileCorner3;

uniform mat3 shiftXP;
uniform mat3 shiftXN;
uniform mat3 shiftYP;
uniform mat3 shiftYN;

/*
 * Hyperboloid model H of the hyperbolic plane H2.
 * - points of H are 3d vectors (x,y,z) such that x^2 + y^2 - z^2 = -1 with z > 0
 * - the group SO(2,1) acts by isometry on H
 */


float hypDot(vec3 p, vec3 q) {
    return p.x * q.x + p.y * q.y - p.z * q.z;
}

float hypLenghtSq(vec3 p) {
    return -hypDot(p, p);
}

float hypLength(vec3 p) {
    return sqrt(hypLenghtSq(p));
}

vec3 reduceError(vec3 p) {
    return p / hypLength(p);
}

vec3 applyIsometry(mat3 isom, vec3 p) {
    vec3 res = isom * p;
    return reduceError(res);
}

/*
 * Conversion from the disc model to the hyperboloid model
 */
vec3 disc2hyp(vec2 p) {
    float aux = dot(p, p);
    return vec3(2. * p, 1. + aux) / (1. - aux);
}

float arctanh(float x) {
    return 0.5 * log((1. + x) / (1. - x));
}


float auxDistKlein(float x) {
    float th_rho = tileData.y / tileData.x;
    float a = sqrt(1. - 0.5 * th_rho * th_rho);
    return 0.5 * log((a + x) / (a - x));
}



vec2 tileCoordsAxesIsom(vec3 p) {
    // coordinates of p in the projective model
    float sizeKlein = arctanh(0.5 * sqrt2 * tileData.y / tileData.x);
    vec2 klein_coords = p.xy / p.z;
    float sX = arctanh(klein_coords.x) / sizeKlein;
    float sY = arctanh(klein_coords.y) / sizeKlein;
    vec2 s = vec2(sX, sY);
    return clamp(0.5 * s + vec2(0.5), vec2(0, 0), vec2(1, 1));
}

vec2 tileCoordsSidesIsom(vec3 p) {
    // coordinates of p in the projective model
    float sizeKlein = auxDistKlein(0.5 * sqrt2 * tileData.y / tileData.x);
    vec2 klein_coords = p.xy / p.z;
    float sX = auxDistKlein(klein_coords.x) / sizeKlein;
    float sY = auxDistKlein(klein_coords.y) / sizeKlein;
    vec2 s = vec2(sX, sY);

    vec2 aux = clamp(0.5 * s + vec2(0.5), vec2(0, 0), vec2(1, 1));
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


vec2 tileCoordsNaive(vec3 p) {
    // coordinates of p in the projective model
    vec2 klein_coords = p.xy / p.z;
    return clamp(klein_coords / (sqrt2 * tileData.y / tileData.x) + vec2(0.5), vec2(0, 0), vec2(1, 1));
}



void main() {
    vec2 q = 1.2 * v_text * (resolution / resolution.y);
    if (length(q) > 1.) {
        f_color = vec4(1, 1, 1, 1);
        return;
    }


    vec3 p, r;
    float preDistP, preDistR;
    p = disc2hyp(q);
    // moving the point p by the given isometry
    p = isometry * p;
    preDistP = hypDot(ORIGIN, p);

    for (int i = 0; i < iterations; i++) {
        r = applyIsometry(shiftXP, p);
        preDistR = hypDot(ORIGIN, r);
        // no need to compare the exact distances,
        // we only compute -cosh(dist(p1,p2)) = hypDot(p1,p2)
        if (preDistR > preDistP) {
            p = r;
            preDistP = preDistR;
            continue;
        }
        r = applyIsometry(shiftXN, p);
        preDistR = hypDot(ORIGIN, r);
        if (preDistR > preDistP) {
            p = r;
            preDistP = preDistR;
            continue;
        }
        r = applyIsometry(shiftYP, p);
        preDistR = hypDot(ORIGIN, r);
        if (preDistR > preDistP) {
            p = r;
            preDistP = preDistR;
            continue;
        }
        r = applyIsometry(shiftYN, p);
        preDistR = hypDot(ORIGIN, r);
        if (preDistR > preDistP) {
            p = r;
            preDistP = preDistR;
            continue;
        }
        break;
    }

    vec2 coords = tileCoordsSidesIsom(p);
    vec3 color = texture(tileTexture, coords).rgb;
    f_color = vec4(color, 1);
}
