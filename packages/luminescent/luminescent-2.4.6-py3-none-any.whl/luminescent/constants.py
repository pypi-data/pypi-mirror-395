from copy import deepcopy
from gdsfactory.generic_tech import get_generic_pdk
from gdsfactory.technology import (
    LayerLevel,
    LayerStack,
    LayerView,
    LayerViews,
    LayerMap,
)

pdk = get_generic_pdk()
pdk.activate()
LAYER_VIEWS = pdk.layer_views

eps0 = 8.854187817e-12
Z0 = 377 * (3e8) * eps0

SEP = "#"  # Separator for filenames
