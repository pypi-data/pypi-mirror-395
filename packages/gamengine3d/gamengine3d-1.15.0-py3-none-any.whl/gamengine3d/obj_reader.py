
from .helper import vector3d

class OBJReader:
    def __init__(self, filename):
        self.filename = filename
        self.vertices = []
        self.faces = []

    def read(self):
        with open(self.filename, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('v '):
                    parts = line.split()[1:]
                    self.vertices.append(vector3d(*[float(p) for p in parts]))
                elif line.startswith('f '):
                    parts = line.split()[1:]
                    # Convert face into vertex indices
                    face_indices = [int(p.split('/')[0]) - 1 for p in parts]

                    # Triangulate if more than 3 vertices
                    if len(face_indices) == 3:
                        self.faces.append(face_indices)
                    elif len(face_indices) > 3:
                        # Fan triangulation: v0,v1,v2 ; v0,v2,v3 ; v0,v3,v4 ...
                        v0 = face_indices[0]
                        for i in range(1, len(face_indices) - 1):
                            self.faces.append([v0, face_indices[i], face_indices[i+1]])
        return self.vertices, self.faces
