from gamengine3d import vector3d, Context, Cuboid
import math


class PlayerMovement:  # Class name must match file name in PascalCase
    def __init__(self, obj: Cuboid, context: Context):
        self.obj = obj
        self.context = context

        self.speed = 1                  # units per second
        self.rotate_speed = 100         # degrees per second
        self.gravity = vector3d(0, -4.8, 0)
        self.velocity = vector3d.zero

        # Movement bindings
        self.context.on_key_held("w", callback=self.handle_controls, dt=True, args=["forward"])
        self.context.on_key_held("s", callback=self.handle_controls, dt=True, args=["backward"])
        self.context.on_key_held("a", callback=self.handle_controls, dt=True, args=["left"])
        self.context.on_key_held("d", callback=self.handle_controls, dt=True, args=["right"])
        self.context.on_key_held("space", callback=self.handle_controls, dt=True, args=["up"])

        self.obj.rotation = vector3d(0)  # start facing forward


    def update(self, dt):
        # Gravity runs every frame
        self.handle_gravity(dt)


    def handle_controls(self, dt, direction):
        forward = get_forward(self.obj.rotation)  # forward relative to facing direction

        if direction == "forward":
            delta_pos = forward * self.speed * dt
            self.obj.pos += delta_pos

            # undo if hitting walls
            if any([
                self.context.functions.is_colliding(self.obj.name, "Left"),
                self.context.functions.is_colliding(self.obj.name, "Right"),
                self.context.functions.is_colliding(self.obj.name, "Back"),
            ]):
                self.obj.pos -= delta_pos

        elif direction == "backward":
            delta_pos = forward * self.speed * dt
            self.obj.pos -= delta_pos

            # undo if hitting walls
            if any([
                self.context.functions.is_colliding(self.obj.name, "Left"),
                self.context.functions.is_colliding(self.obj.name, "Right"),
                self.context.functions.is_colliding(self.obj.name, "Back"),
            ]):
                self.obj.pos += delta_pos

        elif direction == "left":
            self.obj.rotation.z -= self.rotate_speed * dt  # turn left

        elif direction == "right":
            self.obj.rotation.z += self.rotate_speed * dt  # turn right

        elif direction == "up":
            # jump only if grounded
            if self.context.functions.is_colliding(self.obj.name, "Floor"):
                self.velocity.y = 3
                self.obj.pos.y += 0.1  # small lift to ensure gravity applies next frame


    def handle_gravity(self, dt):
        grounded = self.context.functions.is_colliding(self.obj.name, "Floor")

        if not grounded:
            self.velocity += self.gravity * dt  # accelerate downward
        else:
            floor = self.context.functions.get_game_object("Floor")
            self.obj.pos.y = floor.pos.y + floor.size.y/2 + self.obj.size.y/2  # snap to surface
            self.velocity = vector3d.zero

        # check predicted collision next frame
        if self.context.functions.is_colliding_pos("Floor", self.obj.pos + self.velocity * dt):
            floor = self.context.functions.get_game_object("Floor")
            self.obj.pos.y = floor.pos.y + floor.size.y/2 + self.obj.size.y/2
        else:
            self.obj.pos += self.velocity * dt  # apply gravity motion


def get_forward(rotation):
    yaw = math.radians(rotation.z)
    fx = -math.sin(yaw)
    fy = 0
    fz = math.cos(yaw)
    return vector3d(fx, fy, fz)
