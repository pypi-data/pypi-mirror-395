from os.path import isdir, join
from platform import system

from setuptools import Extension, find_packages, setup
from distutils.command.build import build
from wheel.bdist_wheel import bdist_wheel


class Build(build):
    def run(self):
        if isdir("queries"):
            dest = join(self.build_lib, "tree_sitter_opencl", "queries")
            self.copy_tree("queries", dest)
        super().run()


setup(
    name="tree-sitter-opencl",
    version="0.0.1",
    packages=find_packages("bindings/python"),
    package_dir={"": "bindings/python"},
    package_data={
        "tree_sitter_opencl": ["*.pyi", "py.typed"],
        "tree_sitter_opencl.queries": ["*.scm"],
    },
    ext_package="tree_sitter_opencl",
    ext_modules=[
        Extension(
            name="_binding",
            sources=[
                "bindings/python/tree_sitter_opencl/binding.c",
                "src/parser.c",
                # NOTE: if your language uses an external scanner, add it here.
            ],
            extra_compile_args=(
                ["-std=c11"] if system() != 'Windows' else []
            ),
            define_macros=[
                ("Py_LIMITED_API", "0x03070000"),
                ("PY_SSIZE_T_CLEAN", None)
            ],
            include_dirs=["src"],
            py_limited_api=True,
        )
    ],
    cmdclass={
        "build": Build
    },
    zip_safe=False
)