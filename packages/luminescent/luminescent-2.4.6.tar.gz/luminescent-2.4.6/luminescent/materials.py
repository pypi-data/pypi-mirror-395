import math
from gdsfactory.technology import LogicalLayer, LayerLevel, LayerStack
from gdsfactory.generic_tech.layer_map import LAYER
import gdsfactory as gf
import copy


PECVAL = 1337


def Material(
    epsilon=1, mu=1, sigma=0, chi2=0, chi3=0, dispersion=None, mesh_density=None
):
    """
    Define material properties in relative units

    Args:

    - epsilon: relative permittivity
    - mu: relative permeability
    - sigma: conductivity (multiply by `377 * (characteristic wavelength in m)` to convert from metric (`S/m, 1 /(Ω m)`) to relative units)
    - chi2: Pockels second order nonlinear susceptibility
    - chi3: Kerr third order nonlinear susceptibility
    - dispersion: list of tuples [(gamma, omega, is_lorentzian)...] each defining a dispersion term. `is_lorentzian=True` for Lorentzian, `False` for Drude. We use Meep convention https://meep.readthedocs.io/en/latest/Materials/#material-dispersion and relative units.
    - mesh_density: mesh density relative to vacuum, defaults to square root of relative permittivity
    """
    # - name: material name eg 'Si'
    # - background: if True, set as background material
    if mesh_density is None:
        mesh_density = math.sqrt(abs(epsilon * mu))
    return {
        # "name": name,
        "epsilon": epsilon,
        "mu": mu,
        "sigma": sigma,
        "chi2": chi2,
        "chi3": chi3,
        "dispersion": dispersion,
        "mesh_density": mesh_density,
    }


def PECMaterial(mesh_density):
    """
    Perfect electric conductor material for modeling metals
    """
    return Material(
        epsilon=PECVAL,
        mesh_density=mesh_density,
    )


def PlaceholderMaterial(mesh_density):
    """
    placeholder material contributes to meshing but not to physical properties, eg used for design region
    """
    return Material(
        epsilon=None,
        mesh_density=mesh_density,
    )


MATERIAL_LIBRARY = {
    "vacuum": Material(),
    "air": Material(),
    "cSi": Material(epsilon=3.476**2),
    "SiO2": Material(epsilon=1.444**2),
    "SiN": Material(epsilon=2.0**2),
    "Ge": Material(epsilon=4.0**2),
    "Si": Material(epsilon=3.476**2),
    # "ZeSe": {"epsilon": 5.7},
    "FR4": Material(epsilon=4.3),
    # "Al2O3": {"epsilon": 9.9},
    # "PEC": {"epsilon": 1337, "sigma": 50},
    "background": Material(),
}


def isPEC(x):
    return x >= PECVAL


ks = copy.deepcopy(list(MATERIAL_LIBRARY.keys()))
for k in ks:
    MATERIAL_LIBRARY[k.lower()] = MATERIAL_LIBRARY[k]

# BBOX = (0, 0)
# WG = (1, 0)
# CLAD = (2, 0)
# DESIGN = (1000, 0)
# OVERRIDE = (2000, 0)

# thickness_wg = 0.22
# layers = {
#     "core": LayerLevel(
#         layer=LogicalLayer(layer=WG),
#         thickness=thickness_wg,
#         zmin=0.0,
#         material="Si",
#         mesh_order=1,
#     ),
#     "design": LayerLevel(
#         layer=LogicalLayer(layer=DESIGN),
#         thickness=thickness_wg,
#         zmin=0.0,
#         material="design",
#         mesh_order=0,
#     ),
# }


# SOI220 = LayerStack(layers=layers)

# th_sub = 1.6
# layers = {
#     "top": LayerLevel(
#         layer=LogicalLayer(layer=LAYER.WG),
#         thickness=0.1,
#         zmin=th_sub,
#         material="PEC",
#         mesh_order=1,
#     ),
#     "core": LayerLevel(
#         layer=LogicalLayer(layer=(2, 0)),
#         thickness=th_sub,
#         zmin=0.0,
#         material="FR4",
#         mesh_order=2,
#     ),
#     "bot": LayerLevel(
#         layer=LogicalLayer(layer=(2, 0)),
#         thickness=5,
#         zmin=-5,
#         material="PEC",
#         mesh_order=3,
#     ),
# }


# MS = LayerStack(layers=layers)
# MS.layers["background"] = {"material": "air"}


MATKEYS = {
    "si": "cSi",
    "Si": "cSi",
    "sio2": "SiO2",
    "sin": "SiN",
    "ge": "Ge",
}


def matname(k):
    if k in MATKEYS:
        return MATKEYS[k]
    return k.capitalize()
