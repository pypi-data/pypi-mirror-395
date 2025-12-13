"""
ServerConfig

Contains a Config class for managing config data for server configurations.
"""

# import standard libraries
import logging
from typing import Dict, Final, Optional, Self

# import 3rd-party libraries

# import OGD libraries
from ogd.common.configs.Config import Config
from ogd.common.models.SemanticVersion import SemanticVersion
from ogd.common.utils.typing import Map
from ogd.common.utils.Logger import Logger

# import local files

class ServerConfig(Config):
    _DEFAULT_DEBUG_LEVEL : Final[int] = logging.INFO
    _DEFAULT_VERSION     : Final[str] = "UNKNOWN VERSION"

    # *** BUILT-INS & PROPERTIES ***

    def __init__(self, name:str,
                 debug_level:Optional[int], version:Optional[SemanticVersion],
                 other_elements:Optional[Map]=None):

        unparsed_elements : Map = other_elements or {}

        self._dbg_level : int
        self._version   : SemanticVersion

        self._version   = version     if version     is not None else self._parseVersion(unparsed_elements=unparsed_elements, schema_name=name)
        self._dbg_level = debug_level if debug_level is not None else self._parseDebugLevel(unparsed_elements=unparsed_elements, schema_name=name)

        super().__init__(name=name, other_elements=other_elements)


    @property
    def DebugLevel(self) -> int:
        return self._dbg_level

    @property
    def Version(self) -> SemanticVersion:
        return self._version

    # *** IMPLEMENT ABSTRACT FUNCTIONS ***

    @property
    def AsMarkdown(self) -> str:
        ret_val : str

        ret_val = f"{self.Name}"
        return ret_val

    @classmethod
    def Default(cls):
        return ServerConfig(
            name="DefaultServerConfig",
            debug_level=ServerConfig._DEFAULT_DEBUG_LEVEL,
            version=SemanticVersion.FromString("0.0.0-Testing"),
            other_elements={}
        )

    @classmethod
    def _fromDict(cls, name:str, unparsed_elements:Map,
                  key_overrides:Optional[Dict[str, str]]=None,
                  default_override:Optional[Self]=None):
        return ServerConfig(name=name, debug_level=None, version=None, other_elements=unparsed_elements)

    @staticmethod
    def _parseDebugLevel(unparsed_elements:Map, schema_name:Optional[str]=None) -> int:
        ret_val : int

        raw_level : str = ServerConfig.ParseElement(
            unparsed_elements=unparsed_elements,
            valid_keys=["DEBUG_LEVEL"],
            to_type=[int, str],
            default_value=ServerConfig._DEFAULT_DEBUG_LEVEL,
            remove_target=True,
            schema_name=schema_name
        )
        if isinstance(raw_level, int):
            if raw_level in {logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG}:
                ret_val = raw_level
            else:
                ret_val = ServerConfig._DEFAULT_DEBUG_LEVEL
                Logger.Log(f"Debug level had a value of {raw_level}, but this does not correspond to a valid logging level, defaulting to {ret_val}.", logging.WARNING)
        elif isinstance(raw_level, str):
            match raw_level.upper():
                case "ERROR":
                    ret_val = logging.ERROR
                case "WARNING" | "WARN":
                    ret_val = logging.WARN
                case "INFO":
                    ret_val = logging.INFO
                case "DEBUG":
                    ret_val = logging.DEBUG
                case _:
                    ret_val = ServerConfig._DEFAULT_DEBUG_LEVEL
                    Logger.Log(f"Config debug level had unexpected value {raw_level}, defaulting to {ret_val}.", logging.WARNING)
        else:
            ret_val = ServerConfig._DEFAULT_DEBUG_LEVEL
            Logger.Log(f"Config debug level was unexpected type {type(raw_level)}, defaulting to {ret_val}.", logging.WARNING)

        return ret_val

    @staticmethod
    def _parseVersion(unparsed_elements:Map, schema_name:Optional[str]=None) -> SemanticVersion:
        ret_val : SemanticVersion

        raw_version = ServerConfig.ParseElement(
            unparsed_elements=unparsed_elements,
            valid_keys=["API_VERSION"],
            to_type=[int, str],
            default_value=ServerConfig._DEFAULT_VERSION,
            remove_target=True,
            schema_name=schema_name
        )
        if isinstance(raw_version, int):
            ret_val = SemanticVersion(major=raw_version)
        elif isinstance(raw_version, str):
            ret_val = SemanticVersion.FromString(semver=raw_version)
        else:
            ret_val = SemanticVersion.FromString(str(raw_version))
            Logger.Log(f"Config version was unexpected type {type(raw_version)}, defaulting to SemanticVersion(str(version))={ret_val}.", logging.WARN)

        return ret_val
