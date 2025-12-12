from joblib import load as jload
import numpy as np

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

# Specify the files location
_ASPECT_FOLDER = Path(__file__).parent
_MODEL_FOLDER = _ASPECT_FOLDER/'models'

# Configuration file
_CONF_FILE = _ASPECT_FOLDER/'aspect.toml'

class Aspect_Error(Exception):
    """Aspect exception function"""

# Read lime configuration file
with open(_CONF_FILE, mode="rb") as fp:
    cfg = tomllib.load(fp)

# Default feature detection model
DEFAULT_MODEL_ADDRESS = Path(_MODEL_FOLDER/'aspect_min-max-log_12_pixels_v10_model.joblib')

def read_trained_model(file_address):

    # Read trained model
    model = jload(file_address)

    # Read lime configuration file
    cfg_address = Path(file_address).parent/f'{file_address.stem}.toml'
    with open(cfg_address, mode="rb") as cm:
        cfg_model = tomllib.load(cm)

    return model, cfg_model


def check_lisa(model1D, model2D, setup_cfg):

    if model1D is None:
        coeffs1D = np.array(setup_cfg['linear']['model1D_coeffs']), np.array(setup_cfg['linear']['model1D_intercept'])
    else:
        model1D_job = jload(model1D)
        coeffs1D = np.squeeze(model1D_job.coef_), np.squeeze(model1D_job.intercept_)

    if model2D is None:
        coeffs2D = np.array(setup_cfg['linear']['model2D_coeffs']), np.array(setup_cfg['linear']['model2D_intercept'])
    else:
        model2D_job = jload(model2D)
        coeffs2D = np.squeeze(model2D_job.coef_), np.squeeze(model2D_job.intercept_)

    return coeffs1D, coeffs2D


# Function to load configuration file
def load_cfg(file_address, fit_cfg_suffix='_line_fitting'):

    """

    This function reads a configuration file with the `toml format <https://toml.io/en/>`_.

    :param file_address: Input configuration file address.
    :type file_address: str, pathlib.Path

    :param fit_cfg_suffix: Suffix for LiMe configuration sections. The default value is "_line_fitting".
    :type fit_cfg_suffix:  str

    :return: Parsed configuration data
    :type: dict

    """

    file_path = Path(file_address)

    # Open the file
    if file_path.is_file():

        # Toml file
        with open(file_path, mode="rb") as fp:
            cfg = tomllib.load(fp)

    else:
        raise Aspect_Error(f'The configuration file was not found at: {file_address}')

    return cfg

def load_model(file_address):

    ml_function = jload(file_address)

    return ml_function