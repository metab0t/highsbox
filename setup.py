from setuptools import setup
import os, platform, subprocess
import shutil

from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class genericpy_bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        python, abi = "py3", "none"
        if os.environ.get("CIBUILDWHEEL", "0") == "1":
            # pypi does not allow linux_x86_64 wheels to be uploaded
            if plat == "linux_x86_64":
                plat = "manylinux2014_x86_64"
            elif plat == "linux_aarch64":
                plat = "manylinux2014_aarch64"
        return python, abi, plat


cmdclass = {"bdist_wheel": genericpy_bdist_wheel}


# cd to `HiGHS` directory and build highs
# run:
#   mkdir build
#   cmake -S. -Bbuild -DFAST_BUILD=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=highs_dist
#   cmake --build build --config Release --parallel 6
#   cmake --install build
# then package highs_dist directory
def build_highs():
    this_directory = os.path.abspath(os.path.dirname(__file__))
    highs_dir = os.path.join(this_directory, "HiGHS")

    # if highs dir does not exist, clone it
    if not os.path.exists(highs_dir):
        subprocess.run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                "v1.12.0",
                "https://github.com/ERGO-Code/HiGHS.git",
            ],
            cwd=this_directory,
            check=True,
        )

    # build highs
    build_dir = os.path.join(highs_dir, "build")
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    subprocess.run(
        [
            "cmake",
            "-S.",
            "-Bbuild",
            "-DFAST_BUILD=ON",
            "-DBUILD_SHARED_LIBS=ON",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_INSTALL_PREFIX=highs_dist",
        ],
        cwd=highs_dir,
        check=True,
    )
    subprocess.run(
        ["cmake", "--build", "build", "--config", "Release", "--parallel", "6"],
        cwd=highs_dir,
        check=True,
    )
    subprocess.run(
        ["cmake", "--install", "build"],
        cwd=highs_dir,
        check=True,
    )


build_highs()


this_directory = os.path.abspath(os.path.dirname(__file__))

long_description = """
highsbox is a python package that packs binary of [HiGHS](https://github.com/ERGO-Code/HiGHS)
"""

from tempfile import TemporaryDirectory


def patch_rpath(executable_path: str):
    if platform.system() == "Darwin":
        subprocess.run(
            [
                "install_name_tool",
                "-add_rpath",
                "@loader_path/../lib",
                executable_path,
            ],
            check=True,
        )
        # show the altered rpath
        p = subprocess.run(
            ["otool", "-l", executable_path],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Output of otool:\n{p.stdout}")
    elif platform.system() == "Linux":
        subprocess.run(
            [
                "patchelf",
                "--set-rpath",
                "$ORIGIN/../lib",
                executable_path,
            ],
            check=True,
        )
        # show the altered rpath
        p = subprocess.run(
            ["patchelf", "--print-rpath", executable_path],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"Output of patchelf:\n{p.stdout}")


with TemporaryDirectory() as temp_dir:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    highs_dir = os.path.join(this_directory, "HiGHS")

    dist_name = "highs_dist"
    shutil.copytree(
        os.path.join(highs_dir, dist_name),
        os.path.join(temp_dir, dist_name),
        dirs_exist_ok=True,
    )

    # In manylinux container, the lib directory will be set as lib64, we need to change it to lib
    lib64dir = os.path.join(temp_dir, dist_name, "lib64")
    if os.path.exists(lib64dir):
        shutil.move(lib64dir, os.path.join(temp_dir, dist_name, "lib"))

    # patch rpath
    # if os.name != "nt":
    #    executable_path = os.path.join(temp_dir, dist_name, "bin", "highs")
    #    patch_rpath(executable_path)

    for fname in ["__init__.py", "__main__.py"]:
        shutil.copy2(
            os.path.join(base_dir, "src", fname), os.path.join(temp_dir, fname)
        )

    setup(
        name="highsbox",
        version="1.12.0",
        cmdclass=cmdclass,
        author="Yue Yang",
        author_email="metab0t@outlook.com",
        url="https://github.com/metab0t/highsbox",
        description="highsbox: binary distribution of HiGHS optimizer",
        long_description=long_description,
        long_description_content_type="text/markdown",
        license="MIT",
        packages=["highsbox"],
        zip_safe=False,
        package_dir={"highsbox": temp_dir},
        package_data={
            "highsbox": [
                "highs_dist/**",
            ]
        },
    )
