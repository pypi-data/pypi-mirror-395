import platform
import subprocess
from .constants import *
from .layers import *
from .utils import *
from .materials import *
import json
import gdsfactory as gf
from copy import deepcopy

# from time import time
import datetime
from math import cos, pi, sin
import os
import numpy as np

from sortedcontainers import SortedDict, SortedSet
from gdsfactory.generic_tech import LAYER_STACK, LAYER


def SpherePort(
    name,
    origin,
    radius,
    frame=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    angres=np.deg2rad(10),
    θmin=1e-3,
    θmax=np.pi,
    φmin=0,
    φmax=2 * np.pi,
):
    frame = np.array(frame).T
    return {
        "name": name,
        "type": "sphere",
        "origin": origin,
        "radius": radius,
        "frame": frame,
        "angres": angres,
        "θmin": θmin,
        "θmax": θmax,
        "φmin": φmin,
        "φmax": φmax,
    }


def PlanePort(
    name,
    origin=None,
    x=None,
    y=None,
    z=None,
    frame=None,
    normal=None,
    tangent=None,
    start=None,
    stop=None,
    direction="+",
    layer=None,
):
    if frame is None:
        if z is not None:
            if direction.startswith("+"):
                frame = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            else:
                frame = [[-1, 0, 0], [0, 1, 0], [0, 0, -1]]
        elif x is not None:
            if direction.startswith("+"):
                frame = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
            else:
                frame = [[0, -1, 0], [0, 0, 1], [-1, 0, 0]]
        elif y is not None:
            if direction.startswith("+"):
                frame = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
            else:
                frame = [[0, 0, -1], [1, 0, 0], [0, -1, 0]]
    frame = np.array(frame).T

    if normal is None:
        normal = frame[:, 2]
    if tangent is None:
        tangent = frame[:, 0]
    r = {
        "name": name,
        "type": "plane",
        "origin": origin,
        "x": x,
        "y": y,
        "z": z,
        "frame": frame,
        "normal": normal,
        "tangent": tangent,
        "direction": direction,
        "start": start,
        "stop": stop,
        "layer": layer,
    }
    return r


def Mode(
    fields=None,
    enum=0,
    ports=None,
    frequencies=None,
    wavelengths=None,
    nmodes=None,
    dr=None,
    lx=None,
    ly=None,
    start=None,
    stop=None,
    metallic_boundaries=None,
    voltage_line=None,
    current_loop=None,
    # **kwargs,
):
    """
       Mode solutions for a port geometry at given frequencies or wavelengths. Sources and monitors automatically use (or interpolate) mode solutions with closest wavelengths

       Args:

       - fields: If None, modes will be solved for automatically. Otherwise, dict or (if using higher order modes) list of dicts with precomputed mode fields eg [{'Ex': np_array, 'Ey': ..., 'Hx': ..., 'Hy': ...} ..., ]
       - frequency or wavelength: specify one (not both)
       - ports: ports that this mode applies to eg ["o1","o2"]. If None, applies to all ports.
       - nmodes: number of modes to solve for if fields is None. More modes mean more accurate  forward and reflected total power coefficients. None means automatic (1 for metal transmission lines, 2 for dielectric waveguide)
    - dr: either dx or [dx, dy] mesh resolution for mode solver. Otherwise will be set automatically. Do not set if `fields` is set.
    """
    # - dr: either dx or [dx, dy] mesh resolution. Required for supplied mode fields. Optional otherwise (will be set automatically for for mode solver)
    # if fields is not None:
    if type(wavelengths) is float or type(wavelengths) is int:
        wavelengths = [wavelengths]
    if type(fields) is dict:
        modes = [[fields]]
        assert dr is None
    elif type(fields) is list:
        if type(fields[0]) is dict:
            modes = [[f] for f in fields]
        else:
            modes = fields
        assert dr is None
    elif fields is None:
        modes = None
    else:
        raise ValueError(f"fields should be dict or list or None. Got {type(fields)}")

    return {
        "modes": modes,
        "enum": enum,
        "ports": ports,
        "frequencies": frequencies,
        "wavelengths": wavelengths,
        "nmodes": nmodes,
        "start": start,
        "stop": stop,
        "lx": lx,
        "ly": ly,
        "dr": dr,
        "metallic_boundaries": metallic_boundaries,
        "voltage_line": voltage_line,
        "current_loop": current_loop,
    }


def Source(
    name,
    source_port_margin,
    wavelength=None,
    frequency=None,
    bandwidth=None,
    duration=None,
    modenums=[0],
):
    """
    Modulated Gaussian pulse source with gradual spectral roll off  at bandwidth limits. Becomes continuous wave if `bandwidth=0`.

    Args:

    - name: should match a port name eg "o1"
    - source_port_margin: distance from port along outward normal to source
    - wavelength or frequency: Specify either (not both)
    - bandwidth: in same units as above
    - modenums: list of mode numbers to excite
    """
    # if not bandwidth:
    #     if frequency:
    #         bandwidth = frequency
    #     elif wavelength:
    #         bandwidth = wavelength

    return {
        "name": name,
        "wavelength": wavelength,
        "bandwidth": bandwidth,
        "duration": duration,
        "frequency": frequency,
        "modenums": modenums,
        "source_port_margin": source_port_margin,
        "type": "plane",
    }


def setup(
    path,
    study,
    wavelength,
    wavelengths,
    layer_stack,
    material_library,
    wl1f=None,
    name="",
    bbox=None,
    boundaries=["PML", "PML", "PML"],
    nres=4,
    dx=None,
    dy=None,
    dz=None,
    component=None,
    z=None,
    # zmargin=None,
    zmin=None,
    zmax=None,
    inset=0,
    sources=[],
    monitors=[],
    exclude_layers=[],
    gpu="CUDA",
    dtype=np.float32,
    saveat=1000,
    gradient_checkpoint=None,
    magic="",
    modes=None,
    ports=None,
    approx_2D_mode=False,
    show_grid=True,
    Tsim=None,
    field_decay_threshold=None,
    path_length_multiple=None,
    relative_pml_depths=1,
    relative_courant=0.9,
    hasPEC=None,
    keys=None,
    ordering="frequency",
    designs=[],
    targets=[],
    load_saved_designs=False,
    optimizer=None,
    verbose=False,
    pixel_size=0.01,
    secret=None,
    time_extrapolation=False,
    info=None,
    subpixel_smoothing=True,
    subpixel_smoothing_sampling_distance=None,
    views=None,
):
    if views:
        writejsonnp(
            os.path.join(path, "visualization.json"),
            {"views": views},
        )
    # if force:
    #     shutil.rmtree(path, ignore_errors=True)
    # elif os.path.exists(path):
    #     raise FileExistsError(
    #         f"Path {path} already exists. Use force=True to overwrite."
    #     )

    os.makedirs(path, exist_ok=True)
    if info is None:
        info = {}
    json.dump(info, open(os.path.join(path, "info.json"), "w"), indent=4)
    if approx_2D_mode:
        N = 2
    else:
        N = 3
        approx_2D_mode = None

    if inset is None:
        inset = [0] * N

    prob = {
        "nres": nres,
        "wavelength": wavelength,
        "wavelengths": wavelengths,
        "name": name,
        "path": path,
        "keys": keys,
        "dx": dx,
        "dy": dy,
        "dz": dz,
        "z": z,
        "Tsim": Tsim,
        "field_decay_threshold": field_decay_threshold,
        "path_length_multiple": path_length_multiple,
        "saveat": saveat,
        "gradient_checkpoint": gradient_checkpoint,
        "verbose": verbose,
        "boundaries": boundaries[0:N],
        "show_grid": show_grid,
        "approx_2D_mode": approx_2D_mode,
        "relative_pml_depths": relative_pml_depths,
        "relative_courant": relative_courant,
        "hasPEC": hasPEC,
        "ordering": ordering,
        "pixel_size": pixel_size,
        "secret": secret,
        "study": study,
        "subpixel_smoothing": subpixel_smoothing,
        "subpixel_smoothing_sampling_distance": subpixel_smoothing_sampling_distance,
        "material_library": material_library,
        "designs": designs,
        "optimizer": optimizer,
        "N": N,
        "load_saved_designs": load_saved_designs,
        "targets": targets,
        "time_extrapolation": time_extrapolation,
    }

    prob["class"] = "pic"
    prob["dtype"] = str(dtype)
    prob["timestamp"] = (
        datetime.datetime.now().isoformat(timespec="seconds").replace(":", "-")
    )
    prob["magic"] = magic

    gpu_backend = gpu
    # if gpu_backend:s
    prob["gpu_backend"] = gpu_backend

    if component is None:
        0
    else:
        c = component
        if ports is None:
            ports = []

        if c.get_ports_list():
            for p in c.get_ports_list(prefix="o"):
                d = get_layers(layer_stack, p.layer)[0]
                hcore = d.thickness
                zcore = d.zmin

                zcenter = zcore
                origin = (np.array(p.center) / 1e0).tolist()
                normal = [
                    cos(p.orientation / 180 * pi),
                    sin(p.orientation / 180 * pi),
                ]
                tangent = [
                    -sin(p.orientation / 180 * pi),
                    cos(p.orientation / 180 * pi),
                ]
                if N == 3:
                    origin.append(zcenter)
                    normal.append(0)
                    tangent.append(0)

                z, n = [0, 0, 1], [*normal, 0][:3]
                t = np.cross(z, n).tolist()
                frame = np.array([t, z, n])
                v = PlanePort(
                    origin=origin,
                    name=p.name,
                    normal=normal,
                    tangent=tangent,
                    frame=frame,
                    layer=tuple(p.layer),
                )
                ports.append(v)

        bbox2 = c.bbox_np()
        if bbox is None:
            bbox = bbox2.tolist()
            bbox[0].append(zmin)
            bbox[1].append(zmax)

        layers = set(c.layers) - set(exclude_layers)

    for mode in modes:
        if mode["frequencies"] is not None:
            mode["wavelengths"] = [wl1f / f for f in mode["frequencies"]]
    for target in targets:
        if target["frequency"]:
            target["wavelength"] = wl1f / target["frequency"]

    MODES = os.path.join(path, "modes")
    os.makedirs(MODES, exist_ok=True)
    GEOMETRY = os.path.join(path, "geometry")
    os.makedirs(GEOMETRY, exist_ok=True)

    if c:
        layer_stack_info = material_voxelate(
            c, zmin, zmax, layers, layer_stack, material_library, GEOMETRY
        )

        dir = os.path.dirname(os.path.realpath(__file__))

        prob["layer_stack"] = layer_stack_info

    for v in ports:
        if v["type"] == "sphere":
            0
        else:
            if v["origin"] is None:
                if v["z"] is not None:
                    v["origin"] = [
                        (bbox[0][0] + bbox[1][0]) / 2,
                        (bbox[0][1] + bbox[1][1]) / 2,
                    ] + [v["z"]]
                    v["lx"] = bbox[1][0] - bbox[0][0]
                    v["ly"] = bbox[1][1] - bbox[0][1]
                elif v["x"] is not None:
                    v["origin"] = [
                        v["x"],
                        (bbox[0][1] + bbox[1][1]) / 2,
                        (bbox[0][2] + bbox[1][2]) / 2,
                    ]
                    v["lx"] = bbox[1][1] - bbox[0][1]
                    v["ly"] = bbox[1][2] - bbox[0][2]
                elif v["y"] is not None:
                    v["origin"] = [
                        (bbox[0][0] + bbox[1][1]) / 2,
                        v["y"],
                        (bbox[0][2] + bbox[1][2]) / 2,
                    ]
                    v["ly"] = bbox[1][2] - bbox[0][2]
                    v["lx"] = bbox[1][0] - bbox[0][0]
                v["start"] = [-v["lx"] / 2, -v["ly"] / 2]
                v["stop"] = [+v["lx"] / 2, +v["ly"] / 2]
    for s in sources:
        p = next((p for p in ports if p["name"] == s["name"]), None)
        s.update(p)
        ct = np.array(p["origin"])
        n = np.array(p["normal"])
        if s["wavelength"] is None:
            s["wavelength"] = wl1f / s["frequency"]
        s["origin"] = (ct + n * s["source_port_margin"]).tolist()
    monitors = ports
    bg = material_library["background"]["epsilon"]
    ime = []
    hasPEC = False
    for f in os.listdir(GEOMETRY):
        i, mat, layer_name, _ = f[:-4].split(SEP)
        if mat in material_library:
            eps = material_library[mat].get("epsilon", None)
            if eps is not None:
                hasPEC = isPEC(eps) or hasPEC
                ime.append(
                    (int(i), trimesh.load(os.path.join(GEOMETRY, f)), eps, layer_name)
                )
    mesheps = [x[1:] for x in sorted(ime, key=lambda x: x[0])]
    l = []
    for i, mode in enumerate(modes):
        name = os.path.join(path, "modes", str(i + 1))
        os.makedirs(name, exist_ok=True)
        print(f"saving mode plots to {name}")
        if mode["wavelengths"] is None:
            mode["wavelengths"] = [wavelength]
        if not mode["ports"]:
            mode["ports"] = [m["name"] for m in monitors]

        v = next((v for v in monitors if v["name"] == mode["ports"][0]), None)
        if v["type"] == "plane":
            if mode["start"] is None:
                if v["start"] is None:
                    d = get_layers(layer_stack, v["layer"])[0]
                    hcore = d.thickness
                    zcore = d.zmin
                    xmargin = (mode["lx"] - hcore) / 2
                    ymargin = (mode["ly"] - hcore) / 2
                    mode["start"] = [-(mode["lx"]) / 2, -(mode["ly"] - hcore) / 2]
                    mode["stop"] = [(mode["lx"]) / 2, (mode["ly"] + hcore) / 2]
                else:
                    mode["start"] = v["start"]
                    mode["stop"] = v["stop"]
            start = mode["start"]
            stop = mode["stop"]
            origin = v["origin"]
            L = stop[0] - start[0]
            W = stop[1] - start[1]
            # start = np.array(origin) + frame[:, 0] * start[0] + frame[:, 1] * start[1]
            # stop = np.array(origin) + frame[:, 0] * stop[0] + frame[:, 1] * stop[1]

            dr = mode["dr"]
            if dr is None:
                if hasPEC:
                    dr = L / 40
                else:
                    dr = L / 40

            if type(dr) is float or type(dr) is int:
                dr = [dr, dr]

            dx, dy = dr
            dx = L / round(L / dx)
            dy = W / round(W / dy)

            mode["dr"] = [dx, dy]

            if mode["modes"]:
                l.append(mode)
            else:
                origin = v["origin"]
                # if len(origin) == 2:
                #     origin = [*origin, zcenter]
                # print(f"origin: {origin}, frame: {v['frame']}, start: {start}, stop: {stop}, bg: {bg}")
                polyeps = section_mesh(
                    mesheps,
                    origin,
                    v["frame"],
                    start,
                    stop,
                    bg,
                )
                # print(f"polyeps: {polyeps}")
                metallic_boundaries = mode["metallic_boundaries"]
                hasPEC = metallic_boundaries is not None or hasPEC
                if not mode["nmodes"]:
                    mode["nmodes"] = 1 if hasPEC else 2
                nmodes = mode["nmodes"]

                eps = epsilon_from_polyeps(polyeps, bg, start, stop, dx, dy).tolist()
                _l = []
                virgin = True
                for i, wavelength in enumerate(mode["wavelengths"]):
                    if virgin:
                        print("showing modes for first wavelength ")
                        show = True
                        virgin = False
                    else:
                        show = False

                    _name = os.path.join(name, f"{wavelength}")
                    if hasPEC:
                        print(f"solving modes with PEC boundaries")
                        # print(f"wavelength: {wavelength}, nmodes: {nmodes}, dx: {dx}, dy: {dy}, metallic_boundaries: {metallic_boundaries}")
                        _modes = solvemodes_femwell(
                            polyeps,
                            start,
                            stop,
                            wavelength,
                            nmodes,
                            dx,
                            dy,
                            metallic_boundaries,
                            show=show,
                        )
                    else:
                        _modes = solvemodes(
                            polyeps,
                            bg,
                            start,
                            stop,
                            wavelength,
                            nmodes,
                            dx,
                            dy,
                            _name,
                            show=show,
                        )
                    _l.append(_modes)

                l.append(
                    {
                        **mode,
                        "modes": _l,
                        "dr": [dx, dy],
                        "epsilon": eps,
                    }
                )
        else:
            l.append(mode)

        for p in mode["ports"]:
            for sm in [monitors, sources]:
                v = next((v for v in sm if v["name"] == p), None)
                if v:
                    if v["start"]:
                        assert v["start"] == mode["start"]
                    if v["stop"]:
                        assert v["stop"] == mode["stop"]
                    v["start"] = mode["start"]
                    v["stop"] = mode["stop"]

    prob["modes"] = l
    prob["bbox"] = bbox
    prob.update({"monitors": monitors, "sources": sources})
    if not os.path.exists(path):
        os.makedirs(path)
    return prob
