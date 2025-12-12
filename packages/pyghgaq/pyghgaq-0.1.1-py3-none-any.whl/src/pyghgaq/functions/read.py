from importlib import resources

import yaml  # requires pyyaml installed


def read_constant(filename: str = "constant.yml") -> dict:
    """Read constant file.

    Parameters
    ----------
    filename : Path to constant file.

    Return
    -----
    conf_file :
        Constant data.
    """
    with resources.files("pyghgaq.data").joinpath(filename).open("r") as f:
        constant = yaml.safe_load(f)
    return constant
