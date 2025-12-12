from __future__ import annotations
from netgen.libngpy._meshing.pybind11_detail_function_record_v1_system_libcpp_abi1 import _Redraw
from pathlib import Path
from pyngcore.pyngcore import Timer
from . import config
from . import libngpy
__all__ = ['Path', 'Redraw', 'TimeFunction', 'Timer', 'config', 'libngpy', 'load_occ_libs']
def Redraw(*args, **kwargs):
    ...
def TimeFunction(func, name = None):
    ...
def _check_python_version():
    ...
def _get_diagnostics():
    ...
def load_occ_libs():
    ...
__diagnostics_template: str = '\nNetgen diagnostics:\n    sys.platform:          {sys.platform}\n    sys.executable:        {sys.executable}\n    sys.version:           {sys.version}\n    Netgen python version: {config.PYTHON_VERSION}\n    Netgen path            {__file__}\n    Netgen config          {config.__file__}\n    Netgen version         {config.NETGEN_VERSION}\n    sys.path: {sys.path}\n'
_netgen_bin_dir: str = '/Users/gitlab-runner/builds/builds/rL7WHzyj/0/ngsolve/netgen/_skbuild/macosx-10.15-universal2-3.12/cmake-install/bin'
_netgen_lib_dir: str = '/Users/gitlab-runner/builds/builds/rL7WHzyj/0/ngsolve/netgen/_skbuild/macosx-10.15-universal2-3.12/cmake-install/netgen'
