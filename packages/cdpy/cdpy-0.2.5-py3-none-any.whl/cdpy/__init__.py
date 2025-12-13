import importlib.metadata
import os

from platformdirs import AppDirs

__chromium_revision__ = "1516839"
__cdpy_home__ = os.environ.get("CDPY_HOME", AppDirs("cdpy").user_data_dir)

from cdpy.launcher import connect, defaultArgs, executablePath, launch

DEBUG = False

version = importlib.metadata.version("cdpy")
version_info = tuple(int(i) for i in str(version).split("."))

__all__ = [
    "connect",
    "launch",
    "executablePath",
    "defaultArgs",
    "version",
    "version_info",
]
