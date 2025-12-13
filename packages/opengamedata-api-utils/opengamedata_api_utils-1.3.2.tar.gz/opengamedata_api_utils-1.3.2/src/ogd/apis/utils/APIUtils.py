"""
APIUtils

Contains general utility functions for common  tasks when setting up our flask/flask-restful API functions.
In particular, has functions to assist in parsing certain kinds of data, and for generating OGD-core objects.
"""

# import standard libraries
import json
import os
from json.decoder import JSONDecodeError
from logging import Logger
from typing import Any, List, Optional

# import OGD libraries
from ogd.common.storage.interfaces.Interface import Interface
from ogd.common.storage.interfaces.MySQLInterface import MySQLInterface
from ogd.common.storage.interfaces.BigQueryInterface import BigQueryInterface
from ogd.common.configs.DataTableConfig import DataTableConfig
# from ogd.core.schemas.configs.ConfigSchema import ConfigSchema

# import local files

def parse_list(list_str:str, logger:Optional[Logger]=None) -> Optional[List[Any]]:
    """Simple utility to parse a string containing a bracketed list into a Python list.
    Returns None if the list was empty

    :param list_str: _description_
    :type list_str: str
    :return: A list parsed from the input string, or None if the string list was invalid or empty.
    :rtype: Union[List[Any], None]
    """
    ret_val : Optional[List[Any]] = None
    try:
        ret_val = json.loads(list_str)
    except JSONDecodeError as e:
        if logger:
            logger.warning(f"Could not parse '{list_str}' as a list, format was not valid!\nGot Error {e}")
    else:
        if ret_val is not None and len(ret_val) == 0:
            # If we had empty list, just treat as null.
            ret_val = None
    return ret_val

# def gen_interface(game_id, core_config:ConfigSchema, logger:Optional[Logger]=None) -> Optional[Interface]:
#     """Utility to set up an Interface object for use by the API, given a game_id.

#     :param game_id: _description_
#     :type game_id: _type_
#     :return: _description_
#     :rtype: _type_
#     """
#     ret_val = None
    
#     _game_source : DataTableConfig = core_config.GameSourceMap.get(game_id, DataTableConfig.Default())

#     if _game_source.Source is not None:
#         # set up interface and request
#         match _game_source.Source.Type.upper():
#             case "MYSQL":
#                 ret_val = MySQLInterface(game_id, config=_game_source, fail_fast=False)
#                 if logger:
#                     logger.info(f"Using MySQLInterface for {game_id}")
#             case "BIGQUERY":
#                 if logger:
#                     logger.info(f"Generating BigQueryInterface for {game_id}, from directory {os.getcwd()}...")
#                 ret_val = BigQueryInterface(game_id=game_id, config=_game_source, fail_fast=False)
#                 if logger:
#                     logger.info("Done")
#             case _:
#                 ret_val = MySQLInterface(game_id, config=_game_source, fail_fast=False)
#                 if logger:
#                     logger.warning(f"Could not find a valid interface for {game_id}, defaulting to MySQL!")
#     return ret_val

# def gen_coding_interface(game_id) -> Optional[CodingInterface]:
#     """Utility to set up an Interface object for use by the API, given a game_id.

#     :param game_id: _description_
#     :type game_id: _type_
#     :return: _description_
#     :rtype: _type_
#     """
#     ret_val = None

#     _core_config = ConfigSchema(name="Core Config", all_elements=core_settings)
#     _game_source : GameSourceSchema = _core_config.GameSourceMap.get(game_id, GameSourceSchema.EmptySchema())

#     if _game_source.Source is not None:
#         # set up interface and request
#         if _game_source.Source.Type == "BigQuery":
#             ret_val = BigQueryCodingInterface(game_id=game_id, config=_core_config)
#             current_app.logger.info(f"Using BigQueryCodingInterface for {game_id}")
#         else:
#             ret_val = BigQueryCodingInterface(game_id=game_id, config=_core_config)
#             current_app.logger.warning(f"Could not find a valid interface for {game_id}, defaulting to BigQuery!")
#     return ret_val
