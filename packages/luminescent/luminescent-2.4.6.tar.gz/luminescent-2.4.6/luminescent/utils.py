import math
import cv2
from IPython.display import Image
from PIL import Image as PILImage
import os
from matplotlib import pylab
import meshio
import shapely
import json
from statistics import median
from .constants import *
import gdsfactory as gf
from gdsfactory.cross_section import Section
from .constants import *
from .materials import *
import pyvista as pv

try:
    from IPython.display import display
except ImportError:
    pass
# import pyvista as pv

# from .picToGDS import main

from math import ceil, cos, pi, sin, tan
import matplotlib.pyplot as plt
import numpy as np
from gdsfactory.generic_tech import LAYER_STACK, LAYER
import copy
import shutil
import trimesh

SEP = "#"


def isnum(x):
    return isinstance(
        x,
        (
            float,
            int,
            np.floating,
            np.integer,
            np.complexfloating,
            np.float64,
            np.complex64,
            complex,
        ),
    )


def _writejsonnp(pre, d):
    # print(f"keeping {pre} as is {type(d)}")
    # if type(d) is list:
    #     print(type(d[0]))
    if isinstance(d, dict):
        return {k: _writejsonnp(f"{pre}{SEP}{k}", v) for k, v in d.items()}
    if isinstance(d, np.ndarray):  # or (
        #     type(d) is list and (isnum(d[0]) or (type(d[0]) is list and isnum(d[0][0])))
        # ):
        name = f"{pre}.npy"
        np.save(name, d)
        return os.path.basename(name)

    if type(d) is list or type(d) is tuple:
        return [_writejsonnp(f"{pre}{SEP}{i+1}", x) for i, x in enumerate(d)]
    # if isinstance(d, np.complex64):
    #     raise ValueError("complex numbers should be in dict {'re':..., 'im':...}")
    if isnum(d) or isinstance(d, str) or d is None:
        return d
    print(d)
    raise ValueError(f"cannot serialize {pre} of type {type(d)}")


def writejsonnp(path, d):
    DATA = os.path.join(os.path.dirname(path), f".{os.path.basename(path)}")
    os.makedirs(DATA, exist_ok=True)
    with open(path, "w") as io:
        r = {k: _writejsonnp(str(os.path.join(DATA, str(k))), v) for k, v in d.items()}
        json.dump(
            r,
            io,
            indent=4,
        )


def _readjsonnp(pre, x):
    if type(x) is dict:
        return {k: _readjsonnp(f"{pre}{SEP}{k}", v) for k, v in x.items()}
    if type(x) is list:
        return [_readjsonnp(f"{pre}{SEP}{i+1}", x) for i, x in enumerate(x)]
    if str(x).endswith(".npy"):
        return np.load(f"{pre}.npy")
    return x


def readjsonnp(path):
    return {
        k: _readjsonnp(
            str(os.path.join(os.path.dirname(path), f".{os.path.basename(path)}", k)), v
        )
        for k, v in json.load(open(path, "r")).items()
    }


# from gdsfactory import LAYER_VIEWS

tol = 0.001


def get(c, i):
    try:
        return c[i]
    except:
        try:
            return getattr(c, i)
        except:
            return None


def arange(a, b, d):
    ret = np.linspace(a, b, round((b - a) / (d)) + 1).tolist()
    return ret


def trim(x, dx):
    return round(x / dx) * dx


def extend(endpoints, wm):
    v = endpoints[1] - endpoints[0]
    v = v / np.linalg.norm(v)
    return [(endpoints[0] - wm * v).tolist(), (endpoints[1] + wm * v).tolist()]


def portsides(c):
    ports = c.ports
    bbox = c.bbox_np()
    res = [[], [], [], []]
    xmin0, ymin0 = bbox[0]
    xmax0, ymax0 = bbox[1]
    for p in ports:
        x, y = np.array(p.center) / 1e0

        if abs(x - xmin0) < tol:
            res[2].append(p.name)
        if abs(x - xmax0) < tol:
            res[0].append(p.name)
        if abs(y - ymin0) < tol:
            res[3].append(p.name)
        if abs(y - ymax0) < tol:
            res[1].append(p.name)
    return res


def add_bbox(c, layer, nonport_margin=0):  # , dx=None):
    bbox = c.bbox_np()
    xmin0, ymin0 = bbox[0]
    xmax0, ymax0 = bbox[1]
    l = xmax0 - xmin0
    w = ymax0 - ymin0

    # l = dx*np.ceil((xmax0-xmin0)/dx)
    # w = dx*np.ceil((ymax0-ymin0)/dx)

    # if dx is not None:
    #     if nonport_margin is None:
    #         nonport_margin = dx
    # if nonport_margin is None:
    #     nonport_margin = 0
    margin = nonport_margin
    xmin, ymin, xmax, ymax = (
        xmin0 - margin,
        ymin0 - margin,
        xmin0 + l + margin,
        ymin0 + w + margin,
    )

    for p in c.ports:
        # p = c.ports[k]
        x, y = np.array(p.center) / 1e0
        if abs(x - xmin0) < tol:
            xmin = x
        if abs(x - xmax0) < tol:
            xmax = x
        if abs(y - ymin0) < tol:
            ymin = y
        if abs(y - ymax0) < tol:
            ymax = y
    p = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
    _c = gf.Component()
    _c << c

    if type(layer[0]) is int:
        layer = [layer]
    for layer in layer:
        layer = tuple(layer)
        _c.add_polygon(p, layer=layer)
    for port in c.ports:
        _c.add_port(name=port.name, port=port)
    return _c

    # def pic2gds(fileName, sizeOfTheCell, layerNum=1, isDither=False, scale=1):
    main(fileName, sizeOfTheCell, layerNum, isDither, scale)
    return "image.bmp", "image.gds"


def finish(c, name):
    c.add_label(name, position=c.bbox_np()[1])


def normal_from_orientation(orientation):
    return [cos(orientation / 180 * pi), sin(orientation / 180 * pi)]


def generate_background_mesh(bounds, resolution=20, eps=1e-6):
    x_min, x_max, y_min, y_max, z_min, z_max = bounds
    grid_x, grid_y, grid_z = np.meshgrid(
        np.linspace(x_min - eps, x_max + eps, resolution),
        np.linspace(y_min - eps, y_max + eps, resolution),
        np.linspace(z_min - eps, z_max + eps, resolution),
        indexing="ij",
    )
    return pv.StructuredGrid(grid_x, grid_y, grid_z).triangulate()


def sizing_function(
    points, focus_point=np.array([0, 0, 0]), max_size=1.0, min_size=0.1
):
    distances = np.linalg.norm(points - focus_point, axis=1)
    return np.clip(max_size - distances, min_size, max_size)


def rectify(v):
    for i, x in enumerate(v):
        if abs(x) < 1e-4:
            v[i] = 0
    v /= np.linalg.norm(v)
    return v


def section_mesh(mesheps, origin, frame, start, stop, bg):
    N = len(origin)
    origin = np.array(origin) - np.array(frame[:, 2][:N]) / 1e6
    bbox = [start[0], start[1], stop[0], stop[1]]
    bbox = shapely.geometry.box(*bbox)
    polyeps = []
    for mesh, eps, layer_name in mesheps:
        slice_2D = mesh.section(plane_origin=origin, plane_normal=frame[:, 2])
        if slice_2D is not None:
            slice_2D.apply_transform(
                trimesh.transformations.translation_matrix(-np.array(origin))
            )
            A = np.linalg.inv(frame)
            to_2D = np.zeros((4, 4))
            to_2D[:3, :3] = A
            to_2D[3, 3] = 1
            slice_2D, _ = slice_2D.to_planar(to_2D=to_2D)
            # slice_2D.show()

            # 4. Get the polygons from the slice
            polygons_full = slice_2D.polygons_full

            # Perform 2D intersections with a line
            # Assuming 'line' is a shapely LineString
            for polygon in polygons_full:
                # shapely.set_precision(polygon, 1e-4)
                intersection = polygon.intersection(bbox)
                if intersection and intersection.area > 1e-3:
                    polyeps.append((intersection, eps, layer_name))
    polyeps.append((bbox, bg, ""))
    # print(polyeps)
    return polyeps


def material_voxelate(c, zmin, zmax, layers, layer_stack, material_library, path):
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)
    stacks = sum(
        [
            [
                [v.mesh_order, v.material, tuple(layer), k, v.info, v.zmin, v.thickness]
                for k, v in get_layers(layer_stack, layer, withkey=True)
            ]
            for layer in layers
        ],
        [],
    )
    stacks = sorted(stacks, key=lambda x: x[0])
    layer_stack_info = dict()
    # raise NotImplementedError("This is a stub")
    lb, ub = c.bbox_np()
    # bbox = [[**lb, zmin], [**ub, zmax]]
    bbox = [[lb[0], lb[1], zmin], [ub[0], ub[1], zmax]]
    layers = [x[2] for x in stacks]

    i = 1
    polygons_by_layer = c.get_polygons_points(by="tuple", merge=False)
    for stack in stacks:
        order = stack[0]
        m = stack[1]
        l1, l2 = layer = stack[2]
        k = stack[3]
        zmin = stack[5]
        thickness = stack[6]

        d = copy.deepcopy(get(layer_stack, "layers")[k])
        if d.zmin <= zmax and d.bounds[1] >= zmin:
            polys = polygons_by_layer[layer]
            for poly in polys:
                mesh = trimesh.creation.extrude_polygon(
                    shapely.geometry.Polygon(poly),
                    height=thickness,
                    transform=[
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, zmin],
                        [0, 0, 0, 1],
                    ],
                )
                OBJ = os.path.join(path, f"{i}{SEP}{m}{SEP}{k}{SEP}unnamed{i}1.obj")
                i += 1
                # print(mesh.bounds)
                mesh = mesh.slice_plane([0, 0, zmin], [0, 0, 1])
                mesh = mesh.slice_plane([0, 0, zmax], [0, 0, -1])
                # print(mesh.bounds)
                trimesh.exchange.export.export_mesh(mesh, OBJ, "obj")

            layer_stack_info[k] = {
                "layer": (l1, l2),
                "zmin": d.zmin,
                "thickness": d.thickness,
                # "material": matname(m),
                "mesh_order": stack[0],
                # "origin": origin,
            }
    return layer_stack_info


from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import box
from shapely.ops import clip_by_rect
from skfem.io.meshio import from_meshio
from tqdm import tqdm

from femwell.maxwell.waveguide import compute_modes
from femwell.mesh import mesh_from_OrderedDict
from skfem import Basis, ElementTriP0, ElementVector, ElementDG, ElementTriP1
import rasterio.features
import EMpy


def atcentroid(a):
    # for i in a.ndim:
    a = (a[0:-1, :] + a[1:, :]) / 2
    a = (a[:, 0:-1] + a[:, 1:]) / 2
    return a


def epsilon_from_polyeps(polyeps, background_eps, start, stop, dx, dy):
    L = stop[0] - start[0]
    W = stop[1] - start[1]
    m = int(L / dx)
    n = int(W / dy)

    epsilon = np.zeros((m, n)) + background_eps
    polyeps.reverse()
    for poly, eps, _ in polyeps:
        if not isPEC(eps):
            poly = shapely.affinity.translate(poly, xoff=-start[0], yoff=-start[1])
            poly = shapely.affinity.scale(
                poly, xfact=1 / dx, yfact=1 / dy, origin=(0, 0)
            )
            poly = clip_by_rect(poly, 0, 0, m, n)
            mask = rasterio.features.rasterize([poly], out_shape=epsilon.T.shape)
            mask = mask.T
            epsilon *= 1 - mask
            epsilon += mask * eps
    polyeps.reverse()
    return epsilon


def solvemodes(
    polyeps, background_eps, start, stop, wavelength, num_modes, dx, dy, name, show=True
):
    L = stop[0] - start[0]
    W = stop[1] - start[1]
    m = int(L / dx)
    n = int(W / dy)

    epsilon = np.zeros((m - 1, n - 1)) + background_eps
    polyeps.reverse()
    for poly, eps, _ in polyeps:
        poly = shapely.affinity.translate(poly, xoff=-start[0], yoff=-start[1])
        poly = shapely.affinity.scale(poly, xfact=1 / dx, yfact=1 / dy, origin=(0, 0))
        poly = clip_by_rect(poly, 0.5, 0.5, m - 0.5, n - 0.5)
        mask = rasterio.features.rasterize([poly], out_shape=epsilon.T.shape)
        mask = mask.T
        epsilon *= 1 - mask
        epsilon += mask * eps
    polyeps.reverse()

    # x = np.linspace(0, L, m)
    # y = np.linspace(0, W, n)
    x = np.linspace(dx / 2, L - dx / 2, m)
    y = np.linspace(dy / 2, W - dy / 2, n)
    # plt.matshow(epsilon)
    # plt.colorbar()  # Add a colorbar to show the mapping
    # plt.show()

    # print(start, stop)

    def ϵfunc(x_, y_):
        return epsilon

    tol = 1e-6
    solver = EMpy.modesolvers.FD.VFDModeSolver(wavelength, x, y, ϵfunc, "0000").solve(
        num_modes, tol
    )
    modes = solver.modes
    # modes = sorted(solver.modes, key=lambda x: -np.abs(x.neff))

    if show:
        for i, mode in enumerate(modes):
            fig = pylab.figure()

            fig.add_subplot(2, 3, 1)
            Ex = np.transpose(mode.get_field("Ex", x, y))
            pylab.contourf(x, y, abs(Ex), 25)
            pylab.title("Ex")

            fig.add_subplot(2, 3, 2)
            Ey = np.transpose(mode.get_field("Ey", x, y))
            pylab.contourf(x, y, abs(Ey), 25)
            pylab.title("Ey")

            fig.add_subplot(2, 3, 3)
            Ez = np.transpose(mode.get_field("Ez", x, y))
            pylab.contourf(x, y, abs(Ez), 25)
            pylab.title("Ez")

            fig.add_subplot(2, 3, 4)
            Hx = np.transpose(mode.get_field("Hx", x, y))
            pylab.contourf(x, y, abs(Hx), 25)
            pylab.title("Hx")

            fig.add_subplot(2, 3, 5)
            Hy = np.transpose(mode.get_field("Hy", x, y))
            pylab.contourf(x, y, abs(Hy), 25)
            pylab.title("Hy")

            fig.add_subplot(2, 3, 6)
            Hz = np.transpose(mode.get_field("Hz", x, y))
            pylab.contourf(x, y, abs(Hz), 25)
            pylab.title("Hz")

            pylab.savefig(f"{name}_{i}.png")

    neffs = [np.real(m.neff) for m in modes]
    modes = [
        # {k: m.get_field(k, x, y).T for k in ["Ex", "Ey", "Ez", "Hx", "Hy", "Hz"]}
        {
            k: m.get_field(k, x, y)
            for k in [
                "Ex",
                "Ey",
                "Hx",
                "Hy",
            ]
        }
        for m in modes
    ]
    # for i, mode in enumerate(modes):
    #     np.savez(os.path.join(path, f"{name}_mode_{i}.npz"), **modes[i])

    return modes


def solvemodes_femwell(
    polyeps,
    start,
    stop,
    wavelength,
    num_modes,
    dx,
    dy,
    metallic_boundaries,
    nmetals=3452,
    show=True,
):
    print("Solving port modes with FEM...")
    xmin, ymin = start
    xmax, ymax = stop
    L = xmax - xmin
    W = ymax - ymin

    polygons = OrderedDict()
    epsilons = OrderedDict()
    _metallic_boundaries = []
    i = 0
    for x in metallic_boundaries:
        found = True
        # if x[0]
        if x == "x+":
            p = shapely.LineString([(xmax, ymin), (xmax, ymax)])
        elif x == "x-":
            p = shapely.LineString([(xmin, ymin), (xmin, ymax)])
        elif x == "y+":
            p = shapely.LineString([(xmin, ymax), (xmax, ymax)])
        elif x == "y-":
            p = shapely.LineString([(xmin, ymin), (xmax, ymin)])
        else:
            found = False
        if found:
            k = f"b{i}"
            i += 1
            _metallic_boundaries.append(k)
            polygons[k] = p

    i = 0
    j = 0
    for poly, eps, layer_name in polyeps:
        if layer_name in metallic_boundaries:
            # if j < nmetals:
            #     j += 1
            i += 1
            k = f"p{i}"

            _metallic_boundaries.append(k)
            # if type(poly) is shapely.LineString:
            #     # polygons[k] = poly
            #     0
            # else:
            l = list(poly.exterior.coords)
            polygons[k] = shapely.simplify(
                shapely.LineString(l), tolerance=0.25 * math.sqrt(dx * dx + dy * dy)
            )
            #     # v = shapely.LinearRing(l)
        if isPEC(eps):
            0
        else:
            i += 1
            k = f"p{i}"
            polygons[k] = poly
            epsilons[k] = eps

    resolutions = {
        k: {
            "resolution": dx,
            "distance": wavelength,
        }
        for k in epsilons
    }

    for key in polygons.keys():
        polygons[key] = shapely.set_precision(polygons[key], 1e-4)

    mesh = from_meshio(
        mesh_from_OrderedDict(polygons, resolutions, default_resolution_max=wavelength)
    )

    basis0 = Basis(mesh, ElementTriP0())
    epsilon = basis0.zeros()
    try:
        epsilon = epsilon.astype(np.float32)
    except Exception:
        # if it's not a numpy array, keep as-is
        pass

    for subdomain in reversed(epsilons.keys()):
        # ensure epsilons are float32
        val = np.float32(epsilons[subdomain])
        epsilon[basis0.get_dofs(elements=subdomain)] = val

    modes = compute_modes(
        basis0,
        epsilon,
        wavelength=wavelength,
        num_modes=num_modes,
        metallic_boundaries=_metallic_boundaries,
    )

    if show:
        for i, mode in enumerate(modes):
            mode.show("E", part="real", colorbar=True, title=f"Mode {i}")
            # mode.show("E", part="imag", colorbar=True, title=f"Mode {i}")
            mode.show("H", part="real", colorbar=True, title=f"Mode {i}")
            # mode.show("H", part="imag", colorbar=True, title=f"Mode {i}")

    basis = modes[0].basis
    basis_fix = basis.with_element(ElementVector(ElementDG(ElementTriP1())))

    grid_x, grid_y = np.meshgrid(
        np.linspace(
            xmin + dx / 2, xmax - dx / 2, round((xmax - xmin) / dx), dtype=np.float32
        ),
        np.linspace(
            ymin + dy / 2, ymax - dy / 2, round((ymax - ymin) / dy), dtype=np.float32
        ),
    )
    coordinates = np.array(
        [grid_x.flatten(), grid_y.flatten()], dtype=np.float32
    )  # ensure float32 coordinates
    shape = grid_x.shape

    r = []
    for mode in modes:
        (et, et_basis), (ez, ez_basis) = basis.split(mode.E)
        (et_x, et_x_basis), (et_y, et_y_basis) = basis_fix.split(
            basis_fix.project(et_basis.interpolate(et))
        )
        E = np.array(
            (
                et_x_basis.interpolator(et_x)(coordinates),
                et_y_basis.interpolator(et_y)(coordinates),
                ez_basis.interpolator(ez)(coordinates),
            ),
            dtype=np.float32,
        ).T

        (ht, ht_basis), (hz, hz_basis) = basis.split(mode.H)
        (ht_x, ht_x_basis), (ht_y, ht_y_basis) = basis_fix.split(
            basis_fix.project(ht_basis.interpolate(ht))
        )
        H = np.array(
            (
                ht_x_basis.interpolator(ht_x)(coordinates),
                ht_y_basis.interpolator(ht_y)(coordinates),
                hz_basis.interpolator(hz)(coordinates),
            ),
            dtype=np.float32,
        ).T

        d = {
            "Ex": E[:, 0],
            "Ey": E[:, 1],
            "Ez": E[:, 2],
            "Hx": H[:, 0] * np.float32(377.0),
            "Hy": H[:, 1] * np.float32(377.0),
            "Hz": H[:, 2] * np.float32(377.0),
        }
        d = {k: v.reshape(shape).T.astype(np.float32) for k, v in d.items()}
        r.append(d)

    return r


def get_layers(layer_stack, layer, withkey=False):
    r = []
    d = get(layer_stack, "layers").items()

    for k, x in d:
        l = get(x, "layer")
        if l is not None:
            t = get(l, "layer")
            if t is not None and tuple(t) == tuple(layer):
                if withkey:
                    x = k, x
                r.append(x)
    if r:
        return r

    for k, x in d:
        l = get(x, "derived_layer")
        if l is not None:
            t = get(l, "layer")
            if t is not None and tuple(t) == tuple(layer):
                if withkey:
                    x = k, x
                r.append(x)
    return r


def wavelength_range(origin, bandwidth, length=3):
    f1 = 1 / (origin + bandwidth / 2)
    f2 = 1 / (origin - bandwidth / 2)
    hw = (f2 - f1) / 2
    f1 = 1 / origin - hw
    f2 = 1 / origin + hw
    return sorted([1 / x for x in np.linspace(f1, f2, length).tolist()])


def wrap(wavelengths):
    if isinstance(wavelengths, float) or isinstance(wavelengths, int):
        wavelengths = [[wavelengths]]
    elif isinstance(wavelengths[0], float) or isinstance(wavelengths[0], int):
        wavelengths = [wavelengths]
    return wavelengths


def save_problem(prob, path):
    path = os.path.abspath(path)

    path = prob["path"]
    if not os.path.exists(path):
        os.makedirs(path)
        #   compiling julia code...
        #   """)
    prob_path = os.path.join(path, "problem.json")
    writejsonnp(prob_path, prob)
    path = os.path.abspath(path)
    print("using simulation folder", path)


def load_prob(path):
    path = os.path.abspath(path)
    print(f"loading problem from {path}")
    return json.loads(open(os.path.join(path, "problem.json"), "rb").read())


def create_gif(image_path, output_path, duration):
    """
    Creates a GIF from a list of image paths.

    Args:
        image_paths: A list of file paths to the images.
        output_path: The output path for the generated GIF.
        duration: The duration of each frame in milliseconds (default: 200).
    """
    image_paths = os.listdir(image_path)
    image_paths = sorted(image_paths, key=lambda x: float(x[0:-4]))
    frames = [PILImage.open(os.path.join(image_path, f)) for f in image_paths]

    # Ensure all frames have the same palette if necessary
    for i in range(len(frames)):
        if frames[i].mode != "RGB":
            frames[i] = frames[i].convert("RGB")

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,  # 0 means infinite loop
    )


from subprocess import Popen, PIPE
import subprocess


def run(cmd):
    print("=" * 40)
    print()
    proc = Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # proc.wait()
    with proc:
        for line in proc.stdout:
            print(str(line.decode().strip()), flush=True)
        err_message = proc.stderr.read().decode()
        print(err_message)
    return proc.returncode


from IPython.display import Image


def peek(path, views=None):
    if views:
        writejsonnp(
            os.path.join(path, "visualization.json"),
            {"views": views},
        )
    try:
        run(
            [
                "luminescent",
                path,
                "peek",
            ]
        )
    except Exception as e:
        print("failed plotting new frames")

    folder = os.path.join(path, "frames_special")
    for fn in os.listdir(folder):
        display(Image(filename=os.path.join(folder, fn)))


def movie(path, views=None, fps=2):
    if views:
        writejsonnp(
            os.path.join(path, "visualization.json"),
            {"views": views},
        )
    nthreads = os.cpu_count()

    try:
        run(
            [
                "luminescent",
                path,
                "movie",
                f" --julia-args -t{nthreads}",
            ]
        )
    except Exception as e:
        print("failed plotting new frames")

    frames_folder = os.path.join(path, "frames")
    video_name = os.path.abspath(os.path.join(path, "simulation.mp4"))

    images = [
        img
        for img in os.listdir(frames_folder)
        if img.endswith((".jpg", ".jpeg", ".png"))
    ]
    try:
        images = sorted(images, key=lambda x: float(x[0:-4]))
    except:
        images = sorted(images)

    for i, img in enumerate(images):
        src = os.path.join(frames_folder, img)
        dst = os.path.join(frames_folder, f"{i:04d}.png")
        if src != dst:
            os.rename(src, dst)
            images[i] = f"{i:04d}.png"
    # # Set frame from the first image
    # frame = cv2.imread(os.path.join(frames_folder, images[0]))
    # height, width, layers = frame.shape

    # # Video writer to create .avi file
    # video = cv2.VideoWriter(
    #     video_name, cv2.VideoWriter_fourcc(*"DIVX"), fps, (width, height)
    # )

    # # Appending images to video
    # for image in images:
    #     video.write(cv2.imread(os.path.join(frames_folder, image)))

    # # Release the video file
    # video.release()
    # cv2.destroyAllWindows()

    GIF = os.path.abspath(os.path.join(path, "simulation.gif"))
    create_gif(frames_folder, GIF, 1000 / fps)
    print(f"Video generated successfully at {GIF}!")
    display(Image(filename=os.path.join(path, "simulation.gif")))


# return display(Image.open(GIF))


def make_top_movie(path, **kwargs):
    FRAMES = os.path.join(path, "temp", "frames")
    os.makedirs(FRAMES, exist_ok=True)
    for d in os.listdir(os.path.join(path, "checkpoints")):
        shutil.copy(
            os.path.join(path, "checkpoints", d, "halfway.png"),
            os.path.join(FRAMES, f"{d}_halfway.png"),
        )
    plot(path, frames_folder=FRAMES, video_name=os.path.join(path, "opt.mp4"), **kwargs)


def make_design_gds(path, prob=None):
    if prob is None:
        prob = load_prob(path)
    for fn in os.listdir(path):
        if fn.endswith(".npy") and fn.startswith("design"):
            a = np.load(os.path.join(path, fn))
            c = gf.read.from_np(a, prob["pixel_size"] * 1e3, threshold=0.5)
            c.write_gds(os.path.join(path, f"{fn[:-4]}.gds"))

            a = np.uint8(a) * 255  # Convert to uint8
            image = PILImage.fromarray(a)  # Convert to uint8 if needed
            image.save(os.path.join(path, f"{fn[:-4]}.png"))
    # CKPT = os.path.join(path, "checkpoints")
    # if os.path.exists(CKPT):
    #     for d in os.listdir(CKPT):
    #         make_design_gds(os.path.join(CKPT, d), prob)


def port_name(port):
    s = str(port).split("@")[0]
    if s[0] in ("o", "e"):
        return s
    return f"o{s}"


def port_number(port):
    s = str(port).split("@")[0]
    if s[0] in ("o", "e"):
        s = s[1:]
    return int(s)


def mode_number(port):
    l = str(port).split("@")
    return 0 if len(l) == 1 else int(l[1])


def unpack_sparam_key(k):
    o, i = k.split(",")
    po, pi = port_name(o), port_name(i)
    mo, mi = mode_number(o), mode_number(i)
    return po, mo, pi, mi


def long_sparam_key(k):
    po, mo, pi, mi = unpack_sparam_key(k)
    return f"{po}@{mo},{pi}@{mi}"


def query(sol, q):
    t = q[0]
    q = q[1:]
    q2, q1 = q.split(",")
    er = 'For S params you need to specify modes like "So1@0,o2@0". Alternatively you can query T params of total flux like "T2,1"'
    if q1[0] in "0123456789":
        q1 = f"o{q1}"
    if "@" in q1:
        y1 = sol["waves"][f"{q1}-"]
    else:
        y1 = sol["flux"][f"{q1}-"]

    if q2[0] in "0123456789":
        q2 = f"o{q2}"
    if "@" in q2:
        y2 = sol["waves"][f"{q2}+"]
    else:
        y2 = sol["flux"][f"{q2}+"]

    if t == "S":
        if "@" not in q1 or "@" not in q2:
            raise ValueError(er)
        return y2 / y1
    elif t == "T":
        if "@" in q1:
            y1 = np.vectorize(lambda x: abs(x) ** 2)(y1)
        if "@" in q2:
            y2 = np.vectorize(lambda x: abs(x) ** 2)(y2)
        return y2 / y1


def convert_frequency_wavelength(f, w1f, bw=None):
    if bw:
        w2 = w1f / (f - bw / 2)
        w1 = w1f / (f + bw / 2)
        bw = w2 - w1
        w = (w1 + w2) / 2
        return w, bw
    w = w1f / f
    return w, None


def straight(length=10, width: float = 1, layer=(1, 0)):
    c = gf.Component()
    c.add_polygon(
        [(0, -width / 2), (length, -width / 2), (length, width / 2), (0, width / 2)],
        layer=layer,
    )  # This draws the main rectangular body of the waveguide.
    c.add_port(  # This adds two connection points, or ports, which are essential for connecting this component to others.
        name="o1",
        center=(0, 0),
        width=width,
        orientation=180,
        layer=layer,  # "o1" is the input port and is facing left due to rotation (orientation=180)
    )
    c.add_port(
        name="o2",
        center=(length, 0),
        width=width,
        orientation=0,
        layer=layer,  # "o2" is the output port and is facing right.
    )
    return c


# import gmsh

# # gmsh.initialize()
# # gmsh.option.setNumber(
# #     "General.Terminal", 1
# # )  # Optional: display Gmsh messages in terminal

# import pymeshfix

# import meshio


# def parse_obj(filepath):
#     vertices = []
#     faces = []
#     with open(filepath, "r") as f:
#         for line in f:
#             parts = line.strip().split()
#             if not parts:
#                 continue
#             if parts[0] == "v":
#                 vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
#             elif parts[0] == "f":
#                 # Assuming triangular faces for simplicity
#                 faces.append(
#                     [int(p.split("/")[0]) - 1 for p in parts[1:]]
#                 )  # -1 for 0-indexed lists
#     return vertices, faces


# def remesh_msh_file(input_file, output_file, mesh_size=None, algorithm=6):
#     """
#     Remesh an existing MSH file using Gmsh.

#     Parameters:
#     -----------
#     input_file : str
#         Path to input .msh file
#     output_file : str
#         Path to output .msh file
#     mesh_size : float, optional
#         Target mesh element size. If None, uses automatic sizing
#     algorithm : int
#         Meshing algorithm:
#         1 = MeshAdapt, 2 = Automatic, 5 = Delaunay,
#         6 = Frontal-Delaunay (default), 7 = BAMG, 8 = Frontal-Delaunay for Quads,
#         9 = Packing of Parallelograms
#     """

#     # Initialize Gmsh
#     gmsh.initialize()
#     gmsh.option.setNumber("General.Terminal", 1)

#     try:
#         # Load the existing mesh
#         print(f"Loading mesh from: {input_file}")
#         gmsh.open(input_file)

#         # Set meshing options
#         if mesh_size is not None:
#             # Set characteristic length globally
#             gmsh.option.setNumber("Mesh.CharacteristicLengthMin", mesh_size * 0.5)
#             gmsh.option.setNumber("Mesh.CharacteristicLengthMax", mesh_size * 2.0)
#             gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 1.0)

#         # Set meshing algorithm
#         gmsh.option.setNumber("Mesh.Algorithm", algorithm)

#         # Additional quality settings
#         gmsh.option.setNumber("Mesh.Optimize", 1)  # Optimize mesh
#         gmsh.option.setNumber("Mesh.OptimizeNetgen", 1)  # Use Netgen optimizer

#         # Clear existing mesh
#         print("Clearing existing mesh...")
#         gmsh.model.mesh.clear()

#         # Regenerate the mesh
#         print("Generating new mesh...")
#         gmsh.model.mesh.generate(2)  # 2D mesh
#         # For 3D mesh, use: gmsh.model.mesh.generate(3)

#         # Optionally refine the mesh
#         # gmsh.model.mesh.refine()

#         # Save the remeshed file
#         print(f"Saving remeshed file to: {output_file}")
#         gmsh.write(output_file)

#         # Get mesh statistics
#         nodes = gmsh.model.mesh.getNodes()
#         elements = gmsh.model.mesh.getElements()
#         print(f"\nMesh statistics:")
#         print(f"  Number of nodes: {len(nodes[0])}")
#         print(f"  Number of elements: {sum(len(e) for e in elements[1])}")

#     except Exception as e:
#         print(f"Error during remeshing: {e}")
#         sys.exit(1)

#     finally:
#         # Finalize Gmsh
#         gmsh.finalize()


# import struct
# import sys


# def read_gmsh_msh(filename):
#     """Read GMSH .msh file (ASCII format version 2.2)"""
#     vertices = []
#     faces = []

#     with open(filename, "r") as f:
#         lines = f.readlines()

#     i = 0
#     while i < len(lines):
#         line = lines[i].strip()

#         # Read nodes/vertices
#         if line == "$Nodes":
#             i += 1
#             num_nodes = int(lines[i].strip())
#             i += 1
#             for _ in range(num_nodes):
#                 parts = lines[i].strip().split()
#                 # parts[0] is node number, parts[1:4] are x, y, z
#                 vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
#                 i += 1
#             continue

#         # Read elements/faces
#         elif line == "$Elements":
#             i += 1
#             num_elements = int(lines[i].strip())
#             i += 1
#             for _ in range(num_elements):
#                 parts = lines[i].strip().split()
#                 element_type = int(parts[1])

#                 # Element type 2 is a 3-node triangle
#                 if element_type == 2:
#                     num_tags = int(parts[2])
#                     # Node indices start after: element_num, type, num_tags, and tags
#                     node_start = 3 + num_tags
#                     face = [
#                         int(parts[node_start]) - 1,  # Convert to 0-based indexing
#                         int(parts[node_start + 1]) - 1,
#                         int(parts[node_start + 2]) - 1,
#                     ]
#                     faces.append(face)
#                 i += 1
#             continue

#         i += 1

#     return vertices, faces


# def write_obj(filename, vertices, faces):
#     """Write .obj file"""
#     with open(filename, "w") as f:
#         f.write("# OBJ file generated from .msh\n")
#         f.write(f"# Vertices: {len(vertices)}\n")
#         f.write(f"# Faces: {len(faces)}\n\n")

#         # Write vertices
#         for v in vertices:
#             f.write(f"v {v[0]} {v[1]} {v[2]}\n")

#         f.write("\n")

#         # Write faces (OBJ uses 1-based indexing)
#         for face in faces:
#             f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")


# def convert_msh_to_obj(msh_file, obj_file=None):
#     """Convert .msh file to .obj file"""
#     if obj_file is None:
#         obj_file = msh_file.rsplit(".", 1)[0] + ".obj"

#     print(f"Reading {msh_file}...")
#     vertices, faces = read_gmsh_msh(msh_file)

#     print(f"Found {len(vertices)} vertices and {len(faces)} faces")

#     print(f"Writing {obj_file}...")
#     write_obj(obj_file, vertices, faces)

#     print("Conversion complete!")


# def remesh(path, materials, dx0):
#     folder = os.path.join(path, "geometry")
#     for f in os.listdir(folder):
#         _, m, _, _ = f.split(SEP)
#         OBJ = os.path.abspath(os.path.join(folder, f))
#         # pymeshfix.clean_from_file(OBJ, OBJ)
#         MSH = OBJ.replace(".obj", ".msh")
#         STL = OBJ.replace(".obj", ".stl")

#         # meshio.read(OBJ).write(MSH)

#         # gmsh.merge(MSH)  # Replace with the path to your OBJ file
#         # Global characteristic length
#         # gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
#         # gmsh.initialize()

#         # # Or define a size field for more control
#         # # For example, to refine near a specific point
#         # # field_tag = gmsh.model.mesh.field.add("Distance")
#         # # gmsh.model.mesh.field.setNumber(field_tag, "PointsList", [x, y, z])
#         # # gmsh.model.mesh.field.setNumber(field_tag, "LcMin", 0.01)
#         # # gmsh.model.mesh.field.setNumber(field_tag, "LcMax", 0.5)
#         # # gmsh.model.mesh.field.setNumber(field_tag, "DistMax", 0.1)
#         # # gmsh.model.mesh.field.setAsBackgroundMesh(field_tag)

#         # # Initialize Gmsh
#         # gmsh.model.add("obj_model")

#         # # Parse the OBJ file
#         # vertices, faces = parse_obj(OBJ)

#         # # Create Gmsh points from OBJ vertices
#         # gmsh_points = []
#         # for i, v in enumerate(vertices):
#         #     gmsh_points.append(gmsh.model.geo.addPoint(v[0], v[1], v[2], tag=i + 1))

#         # # Create Gmsh surfaces from OBJ faces (assuming triangular faces)
#         # for face in faces:
#         #     # Create lines for each edge of the face
#         #     lines = []
#         #     for i in range(len(face)):
#         #         p1_tag = gmsh_points[face[i]]
#         #         p2_tag = gmsh_points[face[(i + 1) % len(face)]]
#         #         lines.append(gmsh.model.geo.addLine(p1_tag, p2_tag))

#         #     # Create a curve loop and then a plane surface
#         #     curve_loop = gmsh.model.geo.addCurveLoop(lines)
#         #     gmsh.model.geo.addPlaneSurface([curve_loop])
#         # gmsh.write(MSH)
#         # gmsh.finalize()
#         # raise NotImplementedError("This is a stub")

#         # gmsh.initialize()
#         # gmsh.model.add("remesh_model")
#         # gmsh.merge(MSH)  # Replace with the path to your OBJ file
#         # gmsh.model.mesh.createTopology()
#         # gmsh.model.mesh.createGeometry()  # This creates the underlying geometry for remeshing
#         # gmsh.option.setNumber(
#         #     "Mesh.CharacteristicLengthMax", 0.5 * dx0 / materials[m]["mesh_density"]
#         # )
#         # # gmsh.model.mesh.generate(2) # Generate 2D mesh on the surfaces
#         # gmsh.model.mesh.generate(2)  # Generate a 3D mesh (or 2 for 2D surfaces)
#         # gmsh.write(MSH)
#         # gmsh.finalize()
#         # remesh_msh_file(
#         #     MSH,
#         #     MSH,
#         #     mesh_size=0.5 * dx0 / materials[m]["mesh_density"],
#         #     algorithm=6,
#         # )

#         # trimesh.load(MSH).export(OBJ)
#         convert_msh_to_obj(MSH, OBJ)
#         os.remove(MSH)
#         # You can also export to other formats if needed, e.g.,
#         # gmsh.write("remeshed_output.vtk")
import numpy as np
from collections import defaultdict


def load_obj(filename):
    """Load vertices and faces from OBJ file."""
    vertices = []
    faces = []

    with open(filename, "r") as f:
        for line in f:
            if line.startswith("v "):
                vertices.append([float(x) for x in line.split()[1:4]])
            elif line.startswith("f "):
                face = [int(x.split("/")[0]) - 1 for x in line.split()[1:]]
                faces.append(face)

    return np.array(vertices), faces


def save_obj(filename, vertices, faces):
    """Save vertices and faces to OBJ file."""
    with open(filename, "w") as f:
        for v in vertices:
            f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
        for face in faces:
            f.write(f'f {" ".join(str(i+1) for i in face)}\n')


def get_edge_map(faces):
    """Build edge connectivity map."""
    edges = defaultdict(list)
    for fi, face in enumerate(faces):
        n = len(face)
        for i in range(n):
            v1, v2 = face[i], face[(i + 1) % n]
            edge = tuple(sorted([v1, v2]))
            edges[edge].append(fi)
    return edges


def split_edge(vertices, faces, v1, v2, target_length):
    """Split edge if longer than target length."""
    p1, p2 = vertices[v1], vertices[v2]
    length = np.linalg.norm(p2 - p1)

    if length <= target_length * 1.5:
        return vertices, faces, False

    # Add midpoint
    mid = (p1 + p2) / 2
    new_idx = len(vertices)
    vertices = np.vstack([vertices, mid])

    # Update faces containing this edge
    new_faces = []
    for face in faces:
        new_face = list(face)
        modified = False
        for i in range(len(face)):
            if (face[i] == v1 and face[(i + 1) % len(face)] == v2) or (
                face[i] == v2 and face[(i + 1) % len(face)] == v1
            ):
                # Insert new vertex
                new_face = face[: i + 1] + [new_idx] + face[i + 1 :]
                modified = True
                break
        new_faces.append(new_face if modified else face)

    return vertices, new_faces, True


def collapse_edge(vertices, faces, v1, v2, target_length):
    """Collapse edge if shorter than target length."""
    p1, p2 = vertices[v1], vertices[v2]
    length = np.linalg.norm(p2 - p1)

    if length >= target_length * 0.5:
        return vertices, faces, False

    # Collapse to midpoint
    mid = (p1 + p2) / 2
    vertices[v1] = mid

    # Replace v2 with v1 in all faces
    new_faces = []
    for face in faces:
        new_face = [v1 if v == v2 else v for v in face]
        # Remove degenerate faces
        if len(set(new_face)) >= 3:
            new_faces.append(new_face)

    return vertices, new_faces, True


def smooth_vertices(vertices, faces, iterations=1):
    """Laplacian smoothing."""
    for _ in range(iterations):
        neighbors = defaultdict(list)
        for face in faces:
            n = len(face)
            for i in range(n):
                v1, v2 = face[i], face[(i + 1) % n]
                neighbors[v1].append(v2)
                neighbors[v2].append(v1)

        new_vertices = vertices.copy()
        for v in range(len(vertices)):
            if v in neighbors and len(neighbors[v]) > 0:
                avg = np.mean(vertices[list(set(neighbors[v]))], axis=0)
                new_vertices[v] = 0.5 * vertices[v] + 0.5 * avg
        vertices = new_vertices

    return vertices


def _remesh(vertices, faces, target_length, iterations=5):
    """Remesh with target edge length."""
    for it in range(iterations):
        print(f"Iteration {it+1}/{iterations}")

        # Split long edges
        edge_map = get_edge_map(faces)
        modified = False
        for v1, v2 in list(edge_map.keys()):
            vertices, faces, split = split_edge(vertices, faces, v1, v2, target_length)
            modified |= split

        # Collapse short edges
        edge_map = get_edge_map(faces)
        for v1, v2 in list(edge_map.keys()):
            vertices, faces, collapsed = collapse_edge(
                vertices, faces, v1, v2, target_length
            )
            modified |= collapsed

        # Smooth
        vertices = smooth_vertices(vertices, faces, iterations=2)

        print(f"  Vertices: {len(vertices)}, Faces: {len(faces)}")

        if not modified:
            print("  Converged")
            break

    return vertices, faces


import gmsh

import trimesh


def remesh_trimesh(input_file, output_file, max_edge_length):
    # Load the STL file
    mesh = trimesh.load(input_file)

    # Subdivide the mesh until all edges are shorter than the specified length
    # Note: this returns a 'triangle soup', not a structured mesh
    new_vertices, new_faces = trimesh.remesh.subdivide_to_size(
        mesh.vertices, mesh.faces, max_edge=max_edge_length
    )

    # Create a new Trimesh object from the results
    remeshed_mesh = trimesh.Trimesh(vertices=new_vertices, faces=new_faces)

    # Save the remeshed mesh to a new STL file
    remeshed_mesh.export(output_file)
    print(
        f"Remeshed mesh saved to {output_file} with max edge length {max_edge_length}"
    )


# Example usage:
# remesh_stl_trimesh("input.stl", "output_remeshed.stl", 0.5)

import pymeshlab


def remesh_pymeshlab(input_file, output_file, target_edge_length):
    # Create a MeshSet object
    ms = pymeshlab.MeshSet()

    # Load the STL file
    ms.load_new_mesh(input_file)

    # Apply a filter to remesh the surface
    # The 'targetlen' parameter can use a absolute value (PureValue) or a percentage
    ms.apply_filter(
        "meshing_isotropic_explicit_remeshing",
        targetlen=pymeshlab.PureValue(target_edge_length),
    )  # target_edge_length as percentage of bounding box diagonal

    # Save the remeshed mesh
    ms.save_current_mesh(output_file)


def _min(l):
    if type(l) in (list, tuple):
        return min(l)
    return l


def remesh(path, materials, dx0):
    folder = os.path.join(path, "geometry")
    for f in os.listdir(folder):
        _, m, _, _ = f.split(SEP)

        OBJ = os.path.abspath(os.path.join(folder, f))

        dx = dx0 / _min(materials[m]["mesh_density"])
        print(dx)

        remesh_pymeshlab(OBJ, OBJ, target_edge_length=1.0 * dx)
        # meshio.read(OBJ).write(MSH, file_format="gmsh")
        # # trimesh.load(OBJ).export(MSH)

        # gmsh.initialize()
        # # point_entities = gmsh.model.getEntities(0)
        # # num_points = len(point_entities)
        # # print(f"Number of points in the model: {num_points}")
        # gmsh.open(MSH)
        # # vertices, faces = load_obj(OBJ)
        # # vertices, faces = _remesh(vertices, faces, dx, iterations=5)
        # # save_obj(OBJ, vertices, faces)
        # # Set a global characteristic length
        # # gmsh.option.setNumber("Mesh.CharacteristicLengthMin", 0.1)
        # gmsh.model.mesh.reclassifyNodes()
        # gmsh.model.mesh.createGeometry()
        # gmsh.option.setNumber("Mesh.CharacteristicLengthMin", dx / 100)
        # gmsh.option.setNumber("Mesh.CharacteristicLengthMax", dx / 2)

        # # Or define local characteristic lengths at specific points/entities
        # # (Requires having geometric entities defined)
        # # gmsh.model.mesh.setSize(gmsh.model.getEntities(0)[0], 0.05) # Example for a point
        # gmsh.model.mesh.generate(2)  # Generate 2D mesh on the surfaces
        # gmsh.write(MSH)

        # point_entities = gmsh.model.getEntities(0)
        # num_points = len(point_entities)
        # print(f"Number of points in the model: {num_points}")
        # gmsh.finalize()

        # trimesh.load(MSH).export(OBJ)
        # os.remove(OBJ)
        # meshio.read(MSH).write(OBJ, file_format="obj")
        # os.remove(MSH)


def View(
    field,
    prop="epsilon",
    x="halfway",
    y="halfway",
    z="halfway",
    field_color_intensity=1.0,
    material_color_intensity=1.0,
    material_color_map=None,
    material_library=None,
):
    """
    3-slice view of 3d field overlayed ontop of material property

    Args:

    - field: eg 'Ey'
    - prop: eg 'epsilon'
    - x: num, 'halfway' or None
    - y:
    - z:
    - field_color_intensity: color field_color_intensity
    """
    if material_color_map:
        # tmp = {}
        # for k, d in material_color_map.items():
        kvs = [(material_library[k][prop], v) for k, v in material_color_map.items()]
        kvs.sort(key=lambda x: x[0])
        ks, vs = zip(*kvs)
        material_color_map = [vs, ks]
        # material_color_map = tmp
    return {
        "field": field,
        "prop": prop,
        "slices": [x, y, z],
        "field_color_intensity": field_color_intensity,
        "material_color_intensity": material_color_intensity,
        "material_color_map": material_color_map,
    }


def chebyshev_nodes(a, b, n=5):
    """
    Generate n Chebyshev nodes in the interval [a, b].

    Chebyshev nodes are the roots of the Chebyshev polynomial of the first kind
    and are optimal for polynomial interpolation to minimize Runge's phenomenon.

    Args:
        n: Number of nodes to generate

    Returns:
        Array of n Chebyshev nodes in [-1, 1]
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if n == 1:
        return np.array([0.0])

    # Chebyshev nodes are: x_k = cos((2k - 1) * pi / (2n)) for k = 1, 2, ..., n
    k = np.arange(n - 1, -1, -1)
    nodes = a + (b - a) / 2 * (1 + np.cos((2 * k + 1) * np.pi / (2 * n)))
    return nodes
