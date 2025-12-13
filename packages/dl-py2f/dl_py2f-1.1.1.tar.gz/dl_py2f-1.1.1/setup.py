import os
import subprocess
import shutil
from pathlib import Path

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py

ROOT = Path(__file__).parent.resolve()
PKG_DIR = ROOT / 'dl_py2f'
SRC_DIR = ROOT / 'dl_py2f'
BUILD_LIB_DIR = ROOT / 'build'   # arbitrary name for CMake build dir


class build_py(_build_py):
    '''
    Custom build_py that first builds libdl_py2f.so via CMake
    and copies it into dl_py2f/ so it ends up inside the wheel.
    '''

    def run(self):
        self.build_dl_py2f_lib()
        super().run()

    def build_dl_py2f_lib(self):
        # Ensure build directory exists
        BUILD_LIB_DIR.mkdir(exist_ok=True)

        # ---- 1. Configure CMake ----
        # Adapt these commands to match your existing build.
        # For example, if your current script does:
        #   cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
        #   cmake --build build --target dl_py2f
        # you can do the same here:
        cmake_config_cmd = [
            'cmake',
            '-S', str(SRC_DIR),
            '-B', str(BUILD_LIB_DIR),
            '-DCMAKE_BUILD_TYPE=Release',
        ]
        subprocess.run(cmake_config_cmd, check=True)

        # ---- 2. Build the library ----
        cmake_build_cmd = [
            'cmake',
            '--build', str(BUILD_LIB_DIR),
            '--target', 'dl_py2f',
            '--config', 'Release',
        ]
        subprocess.run(cmake_build_cmd, check=True)

        # ---- 3. Copy libdl_py2f.so into the package directory ----
        # Adjust this glob/path if your CMake puts the .so somewhere else.
        built_lib = None
        for path in BUILD_LIB_DIR.rglob('libdl_py2f.so'):
            built_lib = path
            break

        if built_lib is None:
            raise RuntimeError('Could not find libdl_py2f.so in CMake build output')

        dest = PKG_DIR / 'libdl_py2f.so'
        shutil.copy2(built_lib, dest)
        print(f'Copied {built_lib} -> {dest}')


setup(name='dl_py2f',
      version='1.1.1',
      description='DL_PY2F: A library for Python-Fortran interoperability',
      author='You Lu',
      author_email='you.lu@stfc.ac.uk',
      url='https://github.com/stfc/dl_py2f',
      license='GNU Lesser General Public License v3.0',
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3.9',
      install_requires=['numpy>=1.26'],
      cmdclass={'build_py': build_py})

