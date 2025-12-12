import numpy as np
from itertools import product
from pyrr import Matrix44
import math

from .obj_reader import OBJReader
from .helper import Color, vector3d, Renderer, Script, Message

class GameObject:
    def __init__(self, name):
        self.name = name
        self.scripts = []
        self.script_paths = []
        self.messages = []
        self.received_message = False

    def update(self, dt):
        for script in self.scripts:
            script.update(dt)

        self.received_message = False

    def draw(self, renderer: Renderer):
        pass

    def attach(self, file_path, context):
        if isinstance(file_path, str):
            self.script_paths.append(file_path)
        else:
            self.script_paths.append(str(file_path))
        script = Script(self, file_path, context)
        script.init_instance()
        self.scripts.append(script)

    def attach_scripts(self, scripts, context):
        for path in scripts:
            self.attach(path, context)

    def init_scripts(self):
        for script in self.scripts:
            script.init_instance()

    def message(self, message, sender):
        self.messages.append(Message(message=message, sender=sender))
        self.received_message = True

class Cuboid(GameObject):
    def __init__(self, pos: vector3d = vector3d.zero,
                 size: vector3d = vector3d(5),
                 color: Color = Color.green,
                 name: str = "Cuboid",
                 rotation: vector3d = vector3d.zero,
                 visible: bool = True):
        super().__init__(name)
        self.name = name
        self.pos = pos
        self.size = size
        self.color = color
        self.rotation = rotation
        self.visible = visible
        self.rigid_body = None

        self.faces = [
            [0, 1, 3, 2],
            [4, 6, 7, 5],
            [0, 4, 5, 1],
            [2, 3, 7, 6],
            [0, 2, 6, 4],
            [1, 5, 7, 3],
        ]

    def get_rotation_matrix(self):
        return Matrix44.from_eulers((
            math.radians(self.rotation.x),
            math.radians(self.rotation.y),
            math.radians(self.rotation.z)
        )).transpose()[:3, :3]  # extract 3x3 rotation

    def get_corners(self):
        corners = []
        half_size = self.size / 2
        rot = self.get_rotation_matrix()

        for dx, dy, dz in product([-1, 1], repeat=3):
            local = np.array([dx * half_size.x, dy * half_size.y, dz * half_size.z])
            rotated = rot @ local
            world = self.pos + vector3d(*rotated)
            corners.append(world)

        return corners

    def is_point_in(self, point: vector3d) -> bool:
        p = np.array([point.x, point.y, point.z])
        center = np.array([self.pos.x, self.pos.y, self.pos.z])
        half = np.array([self.size.x / 2, self.size.y / 2, self.size.z / 2])

        rot = self.get_rotation_matrix()
        inv_rot = rot.T  # inverse of rotation matrix is its transpose

        local_point = inv_rot @ (p - center)

        return np.all(np.abs(local_point) <= half + 1e-6)

    def draw(self, renderer: Renderer):
        if not self.visible:
            return
        corners = self.get_corners()
        for face_idx in self.faces:
            renderer.render_quad(
                corners[face_idx[0]],
                corners[face_idx[1]],
                corners[face_idx[2]],
                corners[face_idx[3]],
                color=self.color
            )

    def serialize(self):
        return {
            "type": "cuboid",
            "pos": self.pos.totuple(),
            "size": self.size.totuple(),
            "color": self.color.to_rgb(),
            "name": self.name,
            "rotation": self.rotation.totuple(),
            "scripts": self.script_paths,
            "visible": self.visible
        }

    @staticmethod
    def deserialize(data, context):
        pos = data["pos"]
        size = data["size"]
        color = data["color"]
        name = data["name"]
        rotation = data["rotation"]
        scripts = data["scripts"]
        visible = data["visible"]

        obj = Cuboid(pos=vector3d.fromtuple(pos), color=Color.RGB(*color), size=vector3d.fromtuple(size), name=name, rotation=vector3d.fromtuple(rotation), visible=visible)
        obj.attach_scripts(scripts, context)

        return obj

class Sphere(GameObject):
    def __init__(self, pos: vector3d = vector3d.zero,
                 radius: float = 5,
                 color: Color = Color.green,
                 segments: int = 32,
                 rings: int = 16,
                 name: str = "Sphere", visible=True):
        super().__init__(name)
        self.name = name
        self.pos = pos
        self.radius = radius
        self.color = color
        self.segments = segments
        self.rings = rings
        self.visible = visible

    def is_point_in(self, point: vector3d) -> bool:
        dx = point.x - self.pos.x
        dy = point.y - self.pos.y
        dz = point.z - self.pos.z
        distance_squared = dx*dx + dy*dy + dz*dz
        return distance_squared <= self.radius * self.radius

    def draw(self, renderer: Renderer):
        if not self.visible:
            return
        renderer.render_sphere(self.pos, self.radius, self.color, self.segments, self.rings)

    def serialize(self):
        return {
            "type": "sphere",
            "pos": self.pos.totuple(),
            "color": self.color.to_rgb(),
            "radius": self.radius,
            "segments": self.segments,
            "rings": self.rings,
            "name": self.name,
            "scripts": self.script_paths,
            "visible": self.visible
        }

    @staticmethod
    def deserialize(data, context):
        pos = data["pos"]
        color = data["color"]
        radius = data["radius"]
        segments = data["segments"]
        rings = data["rings"]
        name = data["name"]
        scripts = data["scripts"]
        visible = data["visible"]

        obj = Sphere(pos=vector3d.fromtuple(pos), color=Color.RGB(*color), radius=radius, segments=segments, rings=rings, name=name, visible=visible)
        obj.attach_scripts(scripts, context)

        return obj

class Cylinder(GameObject):
    def __init__(self, pos: vector3d = vector3d.zero,
                 length: float = 2,
                 radius: float = 0.5,
                 color: Color = Color.light_yellow,
                 segments: int = 32,
                 rotation: vector3d = vector3d.zero,
                 name: str = "Cylinder", visible: bool = True):
        super().__init__(name)
        self.name = name
        self.pos = pos
        self.length = length
        self.radius = radius
        self.color = color
        self.segments = segments
        self.rotation = rotation  # Euler angles in degrees
        self.visible = visible

    def get_rotation_matrix(self):
        rx, ry, rz = math.radians(self.rotation.x), math.radians(self.rotation.y), math.radians(self.rotation.z)
        cx, sx = math.cos(rx), math.sin(rx)
        cy, sy = math.cos(ry), math.sin(ry)
        cz, sz = math.cos(rz), math.sin(rz)
        # Rotation matrices
        Rx = np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])
        Ry = np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])
        Rz = np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
        return Rz @ Ry @ Rx  # apply in XYZ order

    def is_point_in(self, point: vector3d, eps=1e-9) -> bool:
        p = np.array([point.x, point.y, point.z])
        center = np.array([self.pos.x, self.pos.y, self.pos.z])

        # Transform point into cylinder local space
        R = self.get_rotation_matrix()
        invR = R.T  # inverse rotation
        local = invR @ (p - center)

        # Check axial bounds (Y axis)
        half_length = self.length / 2
        if not (-half_length - eps <= local[1] <= half_length + eps):
            return False

        # Check radial distance in XZ plane
        radial_dist_sq = local[0]**2 + local[2]**2
        return radial_dist_sq <= (self.radius + eps)**2

    def draw(self, renderer: Renderer):
        if not self.visible:
            return
        renderer.render_cylinder(center=self.pos, height=self.length, radius=self.radius,
                                 color=self.color, segments=self.segments, rotation=self.rotation)

    def serialize(self):
        return {
            "type": "cylinder",
            "pos": self.pos.totuple(),
            "length": self.length,
            "radius": self.radius,
            "color": self.color.to_rgb(),
            "segments": self.segments,
            "rotation": self.rotation.totuple(),
            "name": self.name,
            "scripts": self.script_paths,
            "visible": self.visible,
        }

    @staticmethod
    def deserialize(data, context):
        pos = data["pos"]
        length = data["length"]
        radius = data["radius"]
        color = data["color"]
        segments = data["segments"]
        rotation = data["rotation"]
        name = data["name"]
        scripts = data["scripts"]
        visible = data["visible"]

        obj = Cylinder(pos=vector3d.fromtuple(pos), length=length, radius=radius, color=Color.RGB(*color), segments=segments, rotation=vector3d.fromtuple(rotation), name=name, visible=visible)
        obj.attach_scripts(scripts, context)

        return obj

class ObjModel(GameObject):
    def __init__(self, pos: vector3d = vector3d.zero,
                 color: Color = Color.white,
                 name: str = "ObjModel",
                 scale: vector3d = vector3d(1.0),
                 file_path: str = "", visible: bool = True):
        super().__init__(name)
        self.name = name
        self.pos = pos
        self.color = color
        self.file_path = file_path
        self.visible = visible
        self.scale = scale

        self.vertices = []
        self.faces = []

        self.load_from_file()

    def load_from_file(self):
        reader = OBJReader(self.file_path)
        self.vertices, self.faces = reader.read()

    def draw(self, renderer: Renderer):
        if not self.visible:
            return

        for face in self.faces:
            renderer.render_plane(p1=self.vertices[face[0]]*self.scale+self.pos, p2=self.vertices[face[1]]*self.scale+self.pos, p3=self.vertices[face[2]]*self.scale+self.pos,
                                  color=self.color)

    def serialize(self):
        return {
            "type": "obj-model",
            "pos": self.pos.totuple(),
            "color": self.color.to_rgb(),
            "name": self.name,
            "scripts": self.script_paths,
            "scale": self.scale.totuple(),
            "file_path": self.file_path,
            "visible": self.visible,
        }

    @staticmethod
    def deserialize(data, context):
        pos = data["pos"]
        color = data["color"]
        name = data["name"]
        scripts = data["scripts"]
        scale = data["scale"]
        visible = data["visible"]
        file_path = data["file_path"]

        obj = ObjModel(pos=vector3d.fromtuple(pos), name=name, color=Color.RGB(*color), scale=vector3d.fromtuple(scale), visible=visible, file_path=file_path)
        obj.attach_scripts(scripts, context)

        return obj
