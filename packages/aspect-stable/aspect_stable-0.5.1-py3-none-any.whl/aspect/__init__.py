import logging
from pathlib import Path
from aspect.io import cfg, load_cfg, load_model
from aspect.workflow import ComponentsDetector, model_mgr, CHOICE_DM, TIME_DM
from aspect.plots import decision_matrix_plot
from aspect.trainer import components_trainer

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# Creating the lime logger
_logger = logging.getLogger("aspect")
_logger.setLevel(logging.INFO)

# Read lime configuration .toml
_inst_dir = Path(__file__).parent
_conf_path = _inst_dir/'aspect.toml'
with open(_conf_path, mode="rb") as fp:
    _setup_cfg = tomllib.load(fp)

__version__ = _setup_cfg['metadata']['version']

# Invert the dictionary of categories number
cfg['number_shape'] =  {v: k for k, v in cfg['shape_number'].items()}