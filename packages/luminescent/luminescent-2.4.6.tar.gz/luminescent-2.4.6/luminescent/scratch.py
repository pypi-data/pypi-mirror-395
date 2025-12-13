import manifold3d as m
import trimesh
import numpy as np


def load_obj_to_manifold(filename):
    """
    Load an .obj file and return a manifold3d.Manifold.
    """
    tri = trimesh.load_mesh(filename, process=False)
    if not isinstance(tri, trimesh.Trimesh):
        raise ValueError("File did not contain a single mesh")

    vertices = np.asarray(tri.vertices, dtype=np.float32)
    faces = np.asarray(tri.faces, dtype=np.int32)
    # return m.Manifold(vertices, faces)
    return m.Manifold(m.Mesh(vertices, faces))


# Example
man = load_obj_to_manifold("1.obj")
print(man.status())  # check if it's valid/watertight
print(man.num_edge())  # check if it's valid/watertight
# print(man.is_manifold())  # should be True for solids
