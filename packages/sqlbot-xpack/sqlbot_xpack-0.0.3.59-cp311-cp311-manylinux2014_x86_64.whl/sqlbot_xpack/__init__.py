# xpack/__init__.py

import sys
import warnings
from fastapi import FastAPI
from sqlbot_xpack.core import init_xpack_core
#from sqlbot_xpack.license.xpack_proxy import apply_proxy_patches
#apply_proxy_patches()

class DependencyEnforcer:
    _checked = False
    
    @classmethod
    def check(cls):
        if cls._checked:
            return
            
        if "sqlbot_xpack" not in sys.modules:
            raise RuntimeError(
                "This application requires 'sqlbot_xpack' package. "
                "Please add 'import sqlbot_xpack' to your main module."
            )
        
        frame = sys._getframe()
        while frame:
            if 'init_fastapi_app' in frame.f_code.co_names:
                cls._checked = True
                return
            frame = frame.f_back
        
        warnings.warn(
            "sqlbot_xpack.init_fastapi_app() not called. "
            "Application may not function properly.",
            RuntimeWarning
        )
        cls._checked = True

def _install_fastapi_hook():
    original_setup = FastAPI.setup
    
    def patched_setup(self):
        DependencyEnforcer.check()
        #init_xpack_core(original_setup)
        return original_setup(self)
    
    FastAPI.setup = patched_setup

_install_fastapi_hook()

def init_fastapi_app(app: FastAPI):
    DependencyEnforcer.check()
    init_xpack_core(app)        