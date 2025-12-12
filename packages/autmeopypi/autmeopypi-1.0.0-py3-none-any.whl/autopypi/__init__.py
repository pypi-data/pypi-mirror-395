__version__ = "1.0.0"
__author__ = "mero"
__email__ = "mero@ps.dev"
__telegram__ = "@QP4RM"
__github__ = "https://github.com/6x-u"

from autopypi.bld import bld
from autopypi.upl import upl
from autopypi.chk import chk
from autopypi.cfg import Config
from autopypi.log import Logger
from autopypi.git import git
from autopypi.srv import srv
from autopypi.ver import ver
from autopypi.bat import bat
from autopypi.ci import ci
from autopypi.col import c
from autopypi.utl import Utils

__all__ = [
    "bld",
    "upl",
    "chk",
    "Config",
    "Logger",
    "git",
    "srv",
    "ver",
    "bat",
    "ci",
    "c",
    "Utils",
    "__version__",
    "__author__",
    "__email__",
    "__telegram__",
    "__github__"
]
