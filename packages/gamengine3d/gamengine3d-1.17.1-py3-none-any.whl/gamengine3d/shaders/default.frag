
#version 330

struct Light {
    vec3 position;
    vec3 color;
    float intensity;
};

#define MAX_LIGHTS 8
uniform int num_lights;
uniform Light lights[MAX_LIGHTS];
uniform float ambient;
uniform sampler2DShadow shadow_map;

in vec3 frag_pos;
in vec3 frag_normal;
in vec3 frag_color;
in vec4 frag_pos_light_space;

out vec4 f_color;

void main() {
    vec3 normal = normalize(frag_normal);
    vec3 color = frag_color / 255.0;
    vec3 result = ambient * color;

    for (int i = 0; i < num_lights; i++) {
        vec3 light_dir = normalize(lights[i].position - frag_pos);

        // ----- Physically-correct attenuation -----
        float dist = length(lights[i].position - frag_pos);
        float attenuation = 1.0 / (dist * dist + 0.001);

        // ----- Diffuse (Lambert) -----
        float diff = max(dot(normal, light_dir), 0.0);

        // ----- Specular (Blinn-Phong) -----
        vec3 view_dir = normalize(-frag_pos); // camera at origin for now
        vec3 half_dir = normalize(light_dir + view_dir);

        float shininess = 32.0;
        float spec = pow(max(dot(normal, half_dir), 0.0), shininess);

        // ----- Shadow (your PCF, unchanged) -----
        vec3 proj_coords = frag_pos_light_space.xyz / frag_pos_light_space.w;
        proj_coords = proj_coords * 0.5 + 0.5;

        float shadow = 1.0;
        if (proj_coords.x >= 0.0 && proj_coords.x <= 1.0 &&
        proj_coords.y >= 0.0 && proj_coords.y <= 1.0) {

            float ndotl = dot(normal, light_dir);
            float bias = clamp(mix(0.002, 0.01, 1.0 - clamp(ndotl, 0.0, 1.0)),
            0.002, 0.01);

            ivec2 texSize = textureSize(shadow_map, 0);
            float texelSizeX = 1.0 / float(texSize.x);
            float texelSizeY = 1.0 / float(texSize.y);

            shadow = 0.0;
            for (int x = -1; x <= 1; ++x) {
                for (int y = -1; y <= 1; ++y) {
                    vec2 offset = vec2(float(x) * texelSizeX,
                    float(y) * texelSizeY);
                    shadow += texture(shadow_map,
                    vec3(proj_coords.xy + offset,
                    proj_coords.z - bias));
                }
            }
            shadow /= 9.0;
        }

        // ----- Final Lighting -----
        vec3 lightColor = lights[i].color * lights[i].intensity;

        vec3 diffuse = diff * lightColor * attenuation;
        vec3 specular = spec * lightColor * attenuation;

        result += shadow * (diffuse + specular) * color;
    }

    f_color = vec4(result, 1.0);
}
