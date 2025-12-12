# Copyright (c) 2022-2025, Yongchao Wu in Aalto University
# This file is from the mdapy project, released under the BSD 3-Clause License.


# start delvewheel patch
def _delvewheel_patch_1_11_2():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'mdapy.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-mdapy-1.0.0a2')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-mdapy-1.0.0a2')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_11_2()
del _delvewheel_patch_1_11_2
# end delvewheel patch

from mdapy.system import System
from mdapy.box import Box
from mdapy.build_lattice import build_crystal, build_hea
from mdapy.create_polycrystal import CreatePolycrystal
from mdapy.eam import EAM, EAMAverage, EAMGenerator
from mdapy.nep import NEP
from mdapy.elastic import ElasticConstant
from mdapy.mean_squared_displacement import MeanSquaredDisplacement
from mdapy.minimizer import FIRE
from mdapy.plotset import set_figure, save_figure
from mdapy.spline import Spline
from mdapy.pigz import compress_file
from mdapy.wigner_seitz_defect import WignerSeitzAnalysis
from mdapy.atomic_strain import AtomicStrain
from mdapy.trajectory import XYZTrajectory
from mdapy.lindemann_parameter import LindemannParameter
from mdapy.void_analysis import VoidAnalysis

__all__ = [
    "System",
    "Box",
    "build_crystal",
    "build_hea",
    "CreatePolycrystal",
    "EAM",
    "EAMAverage",
    "EAMGenerator",
    "NEP",
    "ElasticConstant",
    "MeanSquaredDisplacement",
    "FIRE",
    "set_figure",
    "save_figure",
    "compress_file",
    "Spline",
    "WignerSeitzAnalysis",
    "AtomicStrain",
    "XYZTrajectory",
    "LindemannParameter",
    "VoidAnalysis",
]
__version__ = "1.0.0a2"
