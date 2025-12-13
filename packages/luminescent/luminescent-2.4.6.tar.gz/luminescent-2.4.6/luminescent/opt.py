from .materials import *
from .sparams import *
from .setup import *
from .constants import *
from .layers import *
from .utils import *
import gdsfactory as gf
from copy import deepcopy
from functools import partial
from math import cos, pi, sin
import os
from gdsfactory.generic_tech import LAYER_STACK, LAYER
import json


def Design(
    name, layer, lmin, fill_material, void_material, symmetries=[], uniform_along="z"
):
    """
    Design region to be optimized

    Args:

    - name: design name eg "d1"
    - layer: placeholder layer for design region
    - lmin: minimum feature size
    - fill_material: eg 'Si'
    - void_material: eg 'SiO2'
    - symmetries: eg ["x","y","diagonal"]
    - uniform_along: eg 'z' for planar design region extruded along z
    """
    return {
        "name": name,
        "layer": layer,
        "lmin": lmin,
        "fill_material": fill_material,
        "void_material": void_material,
        "symmetries": symmetries,
        "uniform_along": uniform_along,
    }


def Optimizer(
    iters,
    stoploss,
    lowloss=None,
    momentum=0.8,
    contrast=0.6,
    ckptat=1,
    area_change=0.05,
    gradckptat=None,
):
    """
    Args:

    - iters: maximum number of optimization iterations
    - stoploss: stop optimization if loss goes below this value
    - lowloss:
    - momentum:
    - contrast: initial binary contrast (0 to 1). slightly <1 enables topology change (new holes or islands). =1 freezes topology eg shape optimization. contrast automatically increases to 1 as loss decreases to `lowloss`
    - ckptat: save optimization checkpoint every _ iterations
    - area_change: initial fractional change
    """
    if lowloss is None:
        lowloss = 1.5 * stoploss
    return {
        "iters": iters,
        "stoploss": stoploss,
        "lowloss": lowloss,
        "momentum": momentum,
        "contrast": contrast,
        "ckptat": ckptat,
        "gradckptat": gradckptat,
        "area_change": area_change,
    }


def Target(
    key,
    target,
    weight=1,
    frequency=None,
    wavelength=None,
    func="abs",
):
    """
    - key: eg `To2@0,o1@0` transmission from port o1 to o2 @ 0th mode
    - target: target value
    - weight: weight of this target in overall loss function
    - frequency or wavelength: specify one (not both)
    - func: error function `abs, identity, -, relu, relu-'
    """

    return {
        "key": str(key),
        "wavelength": wavelength,
        "frequency": frequency,
        "target": target,
        "weight": weight,
        "func": func,
    }


def apply_design(c0, sol):
    path = sol["path"]
    a = gf.Component()
    a.add_ref(c0)
    fill = sol["design_config"]["fill"]["layer"]
    dr = sol["design_config"]["DESIGN"]
    for i, d in enumerate(sol["designs"]):
        x0, y0 = d["bbox"][0]
        x1, y1 = d["bbox"][1]
        b = gf.Component()
        b.add_polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], layer=fill)
        a = gf.boolean(a, b, "not", layer=fill)
    c = gf.Component()
    c << a
    # for layer in c0.layers:
    #     if layer != dr:
    #         c.add_ref(c0.extract([layer]))
    # c.show()
    # raise ValueError()
    g = gf.import_gds(os.path.join(path, f"optimized_design_{i+1}.gds"))
    polygons = g.get_polygons(merge=True)
    g = gf.Component()
    for p in polygons[1]:
        g.add_polygon(p, layer=fill)
    g = c << g
    g.xmin = x0
    g.ymin = y0
    return c
