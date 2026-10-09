import subprocess

from setuptools import setup

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext

__version__ = "1.1.1"


# liboxenmq's headers need more than the default include path: oxenmq.h includes zmq.hpp, which
# includes <zmq.h>, and a liboxenmq built with a bundled libzmq installs that header beside zmq.hpp
# and adds its directory to the pkg-config Cflags.
def pkgconfig(*args):
    return subprocess.check_output(["pkg-config", *args, "liboxenmq"], text=True).split()


# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [Pybind11Extension(
        "oxenmq",
        ["src/oxenmq.cpp"],
        cxx_std=20,
        include_dirs=[f[2:] for f in pkgconfig("--cflags-only-I")],
        library_dirs=[f[2:] for f in pkgconfig("--libs-only-L")],
        libraries=[f[2:] for f in pkgconfig("--libs-only-l")],
        ),
]

setup(
    name="oxenmq",
    version=__version__,
    author="Jason Rhinelander",
    author_email="jason@oxen.io",
    url="https://github.com/oxen-io/oxen-mq",
    description="Python wrapper for oxen-mq message passing library",
    long_description="",
    ext_modules=ext_modules,
    zip_safe=False,
)
