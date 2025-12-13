import os
import math
import gdsfactory as gf
from .sol import *


def calibration_component(length, width, bbox_layer, margin, source_port_margin=0):
    c = gf.Component()
    line = c << gf.components.straight(length, width=width)
    if source_port_margin > 0:
        ext = c << gf.components.straight(source_port_margin, width=width)
        ext.connect("o2", line.ports["o1"])
    c << gf.components.bbox(component=c, layer=bbox_layer, top=margin, bottom=margin)
    for i in (1, 2):
        c.add_port(f"o{i}", port=line.ports[f"o{i}"])
    return c


def calibrate(path, run=True, **kwargs):
    make(path, **kwargs)
    if run:
        solve(path)
    sol = load(path)
    l = sol["fields"]["2"]
    fields = l[round((len(l) - 1) / 2)]
    flux = sol["flux"]["o2"]
    return (
        flux,
        fields,
    )
