import yaml
import pkgutil

def read_config(config_dir="config", name_params="drift_threshold.yml"):
    """
    Return the project configuration settings.

    Args:
        config_dir (str): Name of directory containing config
        name_params (str): name of the file yaml containing configurations

    Returns:
        (dict): combined general settings with params settings
    """
    params_config_path = pkgutil.get_data(__name__, f"{config_dir}/{name_params}")
    configurations = yaml.safe_load(params_config_path)

    return configurations