"""""" # start delvewheel patch
def _delvewheel_patch_1_11_2():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pygcgopt.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pygcgopt-1.0.0b0')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-pygcgopt-1.0.0b0')) as file:
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

__version__ = '1.0.0b0'

# required for Python 3.8 on Windows
import os
if hasattr(os, 'add_dll_directory'):
    if os.getenv('SCIPOPTDIR'):
        os.add_dll_directory(os.path.join(os.getenv('SCIPOPTDIR').strip('"'), 'bin'))

# Expose pyscipopt object through pygcgopt
from pyscipopt    import multidict
from pyscipopt    import Benders
from pyscipopt    import Benderscut
from pyscipopt    import Branchrule
from pyscipopt    import Nodesel
from pyscipopt    import Conshdlr
from pyscipopt    import Eventhdlr
from pyscipopt    import Heur
from pyscipopt    import Presol
from pyscipopt    import Pricer
from pyscipopt    import Prop
from pyscipopt    import Sepa
from pyscipopt    import LP
from pyscipopt    import Expr
from pyscipopt    import quicksum
from pyscipopt    import quickprod
from pyscipopt    import exp
from pyscipopt    import log
from pyscipopt    import sqrt
from pyscipopt    import SCIP_RESULT
from pyscipopt    import SCIP_PARAMSETTING
from pyscipopt    import SCIP_PARAMEMPHASIS
from pyscipopt    import SCIP_STATUS
from pyscipopt    import SCIP_STAGE
from pyscipopt    import SCIP_PROPTIMING
from pyscipopt    import SCIP_PRESOLTIMING
from pyscipopt    import SCIP_HEURTIMING
from pyscipopt    import SCIP_EVENTTYPE
from pyscipopt    import SCIP_LPSOLSTAT
from pyscipopt    import SCIP_BRANCHDIR
from pyscipopt    import SCIP_BENDERSENFOTYPE
from pyscipopt    import SCIP_ROWORIGINTYPE

# export user-relevant objects
from pygcgopt.gcg import Model
from pygcgopt.gcg import Detector
from pygcgopt.gcg import PricingSolver
from pygcgopt.gcg import ConsClassifier
from pygcgopt.gcg import VarClassifier
from pygcgopt.gcg import Score
from pygcgopt.gcg import PY_GCG_PRICINGSTATUS as GCG_PRICINGSTATUS
from pygcgopt.gcg import PY_CONS_DECOMPINFO as CONS_DECOMPINFO
from pygcgopt.gcg import PY_VAR_DECOMPINFO as VAR_DECOMPINFO
from pygcgopt.gcg import PY_USERGIVEN as USERGIVEN
