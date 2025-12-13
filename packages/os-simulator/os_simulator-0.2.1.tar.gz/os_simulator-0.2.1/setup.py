from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "os_simulator.os_algorithms",
        [
            "src/cpp/src/pybind_module.cpp",
            "src/cpp/src/scheduler.cpp",
        ],
        include_dirs=[
            pybind11.get_include(),
            "src/cpp/include",
        ],
        define_macros=[('VERSION_INFO', '"dev"')],
        language="c++",
        extra_compile_args=["-std=c++17"],
    )
]

setup(
    ext_modules=ext_modules,
)