
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
uniform sampler2DShadow shadow_map; // NOTE: sampler2DShadow

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
        float ndotl = dot(normal, light_dir);
        float diff = max(ndotl, 0.05);  // stable at grazing angles

        // Project to [0,1] for shadow sampling
        vec3 proj_coords = frag_pos_light_space.xyz / frag_pos_light_space.w;
        proj_coords = proj_coords * 0.5 + 0.5;

        // Hardware PCF shadow sampling
        float shadow = 0.0;
        if (proj_coords.x >= 0.0 && proj_coords.x <= 1.0 &&
        proj_coords.y >= 0.0 && proj_coords.y <= 1.0) {

            float ndotl = dot(normal, light_dir);
            float bias = mix(0.002, 0.02, 1.0 - clamp(ndotl, 0.0, 1.0));
            // Simple 3x3 PCF
            ivec2 texSize = textureSize(shadow_map, 0);
            float texelSizeX = 1.0 / float(texSize.x);
            float texelSizeY = 1.0 / float(texSize.y);

            for (int x = -1; x <= 1; ++x) {
                for (int y = -1; y <= 1; ++y) {
                    vec2 offset = vec2(float(x) * texelSizeX, float(y) * texelSizeY);
                    shadow += texture(shadow_map, vec3(proj_coords.xy + offset, proj_coords.z - bias));
                }
            }
            shadow /= 9.0;
        }


        // No inversion needed
        result += shadow * diff * lights[i].intensity * lights[i].color * color;
    }

    f_color = vec4(result, 1.0);
}
