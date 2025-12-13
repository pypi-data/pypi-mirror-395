import manifold3d as m
import meshio
import numpy as np
import tempfile
import os


def meshio_to_manifold(mesh):
    """Convert meshio.Mesh → manifold3d.Manifold"""
    points = mesh.points.astype(np.float32)
    faces = None
    for c in mesh.cells:
        if c.type in ("triangle", "tri"):
            faces = c.data
            break
    if faces is None:
        raise ValueError("No triangle cells found in mesh")
    return m.Manifold(m.Mesh(points, faces))


def manifold_to_meshio(manifold):
    """Convert manifold3d.Manifold → meshio.Mesh"""
    m = manifold.to_mesh()
    verts = m.vert_properties
    tris = m.tri_verts
    return meshio.Mesh(points=verts, cells=[("triangle", tris)])


def remove_mutual_intersections(manifold_list):
    """
    Remove mutual intersections among manifold3d.Manifold objects.
    Earlier meshes take precedence.
    """
    cleaned = []
    accumulated = None

    for i, mf in enumerate(manifold_list):
        # Carve this mesh by subtracting all earlier ones
        # if accumulated is not None:
        #     mf = mf.difference(accumulated)
        if cleaned:
            mf = mf.batch_boolean([mf, *cleaned], m.OpType.Subtract)
        cleaned.append(mf)
        # Update accumulated union
        # accumulated = mf if accumulated is None else accumulated.union(mf)
    return cleaned


def remove_intersections_meshio(mesh_list):
    """
    Same idea, but for meshio.Mesh list.
    Returns cleaned meshio.Mesh list.
    """
    manifolds = [meshio_to_manifold(msh) for msh in mesh_list]
    cleaned_manifolds = remove_mutual_intersections(manifolds)
    return [manifold_to_meshio(mf) for mf in cleaned_manifolds]
