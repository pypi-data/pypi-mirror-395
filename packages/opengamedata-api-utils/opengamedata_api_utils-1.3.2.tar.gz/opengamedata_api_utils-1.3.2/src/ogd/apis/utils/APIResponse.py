"""
APIResponse

Contains class for representing a response from an OGD API,
as well as utility enums used by the APIResponse class.
"""

# import standard libraries
import json
from enum import IntEnum
from typing import Any, Dict, Optional, Set

# import 3rd-party libraries
from flask import Response

# import OGD libraries
from ogd.common.utils.typing import Map
import ogd.core.requests.RequestResult as RequestResult

# Import local files

class RESTType(IntEnum):
    """Simple enumerated type to track type of a REST request.
    """
    GET  = 1
    POST = 2
    PUT  = 3

    def __str__(self):
        """Stringify function for RESTTypes.

        :return: Simple string version of the name of a RESTType
        :rtype: _type_
        """
        match self.value:
            case RESTType.GET:
                return "GET"
            case RESTType.POST:
                return "POST"
            case RESTType.PUT:
                return "PUT"
            case _:
                return "INVALID REST TYPE"

class ResponseStatus(IntEnum):
    """Simple enumerated type to track the status of an API request result.
    """
    NONE    =   1
    SUCCESS = 200
    ERR_REQ = 400
    ERR_NOTFOUND = 404
    ERR_SRV = 500

    @staticmethod
    def ServerErrors() -> Set["ResponseStatus"]:
        return {ResponseStatus.ERR_SRV}

    @staticmethod
    def ClientErrors() -> Set["ResponseStatus"]:
        return {ResponseStatus.ERR_REQ, ResponseStatus.ERR_NOTFOUND}

    def __str__(self):
        """Stringify function for ResponseStatus objects.

        :return: Simple string version of the name of a ResponseStatus
        :rtype: _type_
        """
        match self.value:
            case ResponseStatus.NONE:
                return "NONE"
            case ResponseStatus.SUCCESS:
                return "SUCCESS"
            case ResponseStatus.ERR_SRV:
                return "SERVER ERROR"
            case ResponseStatus.ERR_REQ:
                return "REQUEST ERROR"
            case _:
                return "INVALID STATUS TYPE"

class APIResponse:
    def __init__(self, req_type:Optional[RESTType], val:Optional[Map], msg:str, status:ResponseStatus):
        self._type   : Optional[RESTType] = req_type
        self._val    : Optional[Map]      = val
        self._msg    : str                = msg
        self._status : ResponseStatus     = status

    def __str__(self):
        return f"{str(self.Type)} request: {self.Status}\n{self.Message}\nValues: {self.Value}"

    @staticmethod
    def Default(req_type:RESTType):
        return APIResponse(
            req_type=req_type,
            val=None,
            msg="",
            status=ResponseStatus.NONE
        )

    @staticmethod
    def FromRequestResult(result:RequestResult.RequestResult, req_type:RESTType) -> "APIResponse":
        """Generate an `APIResponse` from an OGD `RequestResult`.

        The `RequestResult` indicates the result of a data export request.
        Thus, this builder for an `APIResponse` is included as a convenient way to set up a response for the Data API.

        :param result: The result object from an OGD export request
        :type result: RequestResult.RequestResult
        :param req_type: The REST request type that triggered the export request
        :type req_type: RESTType
        :return: An `APIResponse` corresponding to the result of the export request
        :rtype: APIResponse
        """
        _status : ResponseStatus
        match result.Status:
            case RequestResult.ResultStatus.SUCCESS:
                _status = ResponseStatus.SUCCESS 
            case RequestResult.ResultStatus.FAILURE:
                _status = ResponseStatus.ERR_REQ
            case _:
                _status = ResponseStatus.ERR_SRV
        ret_val = APIResponse(req_type=req_type, val={"session_count":result.SessionCount, "duration":str(result.Duration)}, msg=result.Message, status=_status)
        return ret_val
    
    @staticmethod
    def FromDict(all_elements:Dict[str, Any], status:Optional[ResponseStatus]=None) -> Optional["APIResponse"]:
        ret_val : Optional["APIResponse"] = None

        _type_raw   = all_elements.get("type", "NOT FOUND")
        _val_raw    = all_elements.get("val")
        _msg        = all_elements.get("msg", "NOT FOUND")
        _status_raw = all_elements.get("status")
        try:
            _type   = RESTType[str(_type_raw).upper()] if _type_raw else None
            _val    = _val_raw if isinstance(_val_raw, dict) else json.loads(str(_val_raw)) if _val_raw is not None else None
            _status = ResponseStatus[str(_status_raw).upper()] if _status_raw else (status or ResponseStatus.NONE)
        except KeyError:
            pass
        else:
            ret_val = APIResponse(req_type=_type, val=_val, msg=_msg, status=_status)
        return ret_val

    @property
    def Type(self) -> Optional[RESTType]:
        """Property for the type of REST request

        :return: A RESTType representing the type of REST request
        :rtype: _type_
        """
        return self._type

    @property
    def Value(self) -> Optional[Map]:
        """Property for the value of the request result.

        :return: Some value, of any type, returned from the request.
        :rtype: Any
        """
        return self._val
    @Value.setter
    def Value(self, new_val:Optional[Map]):
        self._val = new_val


    @property
    def Message(self) -> str:
        """Property for the message associated with a request result.

        :return: A string message giving details on the result of the request.
        :rtype: str
        """
        return self._msg
    @Message.setter
    def Message(self, new_msg:str):
        self._msg = new_msg

    @property
    def Status(self) -> ResponseStatus:
        """Property for the status of the request.

        :return: A ResponseStatus indicating whether request is/was successful, incomplete, failed, etc.
        :rtype: ResponseStatus
        """
        return self._status

    @property
    def AsDict(self):
        return {
            "type"   : str(self._type),
            "val"    : self._val,
            "msg"    : self._msg,
        }

    @property
    def AsJSON(self):
        return json.dumps(self.AsDict)

    @property
    def AsFlaskResponse(self) -> Response:
        return Response(response=self.AsJSON, status=self.Status.value, mimetype='application/json')

    def RequestErrored(self, msg:str, status:Optional[ResponseStatus]=None):
        self._status = status if status is not None and status in ResponseStatus.ClientErrors() else ResponseStatus.ERR_REQ
        self.Message = f"ERROR: {msg}"

    def ServerErrored(self, msg:str, status:Optional[ResponseStatus]=None):
        self._status = status if status is not None and status in ResponseStatus.ServerErrors() else ResponseStatus.ERR_SRV
        self.Message = f"SERVER ERROR: {msg}"

    def RequestSucceeded(self, msg:str, val:Optional[Map]):
        self._status = ResponseStatus.SUCCESS
        self.Message = f"SUCCESS: {msg}"
        self.Value   = val
