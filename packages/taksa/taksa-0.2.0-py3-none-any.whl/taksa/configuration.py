from enum import Enum

class Configuration:
    THIRDPARTY_DIR_NAME = "thirdparty"
    BUILD_DIR_NAME = "build"
    INSTALL_DIR_NAME = "install"
    NPROC = 5
    pass

class BuildType(Enum):
    Debug = 1
    Release = 2
    def to_path(self):
        _to_path_dict = {
            BuildType.Debug : "_debug",
            BuildType.Release : "_release",
        }
        return _to_path_dict[self]
    
    def to_str(self):
        _to_str_dict = {
            BuildType.Debug : "Debug",
            BuildType.Release : "Release",
        }
        return _to_str_dict[self]