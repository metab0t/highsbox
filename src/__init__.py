import os


def highs_dist_dir() -> str:
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), "highs_dist")


def highs_bin_path() -> str:
    base_dir = highs_dist_dir()
    if os.name == "nt":
        return os.path.join(base_dir, "bin", "highs.exe")
    else:
        return os.path.join(base_dir, "bin", "highs")


def highs_include_dir() -> str:
    base_dir = highs_dist_dir()
    return os.path.join(base_dir, "include", "highs")


def highs_lib_dir() -> str:
    base_dir = highs_dist_dir()
    return os.path.join(base_dir, "lib")
