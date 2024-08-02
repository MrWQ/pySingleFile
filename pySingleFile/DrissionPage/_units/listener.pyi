# -*- coding:utf-8 -*-
"""
@Author   : g1879
@Contact  : g1879@qq.com
@Copyright: (c) 2024 by g1879, Inc. All Rights Reserved.
@License  : BSD 3-Clause.
"""
from queue import Queue
from typing import Union, Dict, List, Iterable, Optional, Literal, Any

from requests.structures import CaseInsensitiveDict

from .._base.driver import Driver
from .._pages.chromium_base import ChromiumBase
from .._pages.chromium_frame import ChromiumFrame

__RES_TYPE__ = Literal['Document', 'Stylesheet', 'Image', 'Media', 'Font', 'Script', 'TextTrack', 'XHR', 'Fetch',
'Prefetch', 'EventSource', 'WebSocket', 'Manifest', 'SignedExchange', 'Ping', 'CSPViolationReport', 'Preflight', 'Other']


class Listener(object):
    def __init__(self, owner: ChromiumBase):
        self._owner: ChromiumBase = ...
        self._address: str = ...
        self._target_id: str = ...
        self._targets: Union[str, dict, None] = ...
        self._method: set = ...
        self._res_type: set = ...
        self._caught: Queue = ...
        self._is_regex: bool = ...
        self._driver: Driver = ...
        self._request_ids: dict = ...
        self._extra_info_ids: dict = ...
        self.listening: bool = ...
        self._running_requests: int = ...
        self._running_targets: int = ...

    @property
    def targets(self) -> Optional[set]: ...

    def set_targets(self,
                    targets: Union[str, list, tuple, set, bool, None] = True,
                    is_regex: Optional[bool] = False,
                    method: Union[str, list, tuple, set, bool, None] = ('GET', 'POST'),
                    res_type: Union[__RES_TYPE__, list, tuple, set, bool, None] = True) -> None: ...

    def start(self,
              targets: Union[str, list, tuple, set, bool, None] = None,
              is_regex: Optional[bool] = None,
              method: Union[str, list, tuple, set, bool, None] = None,
              res_type: Union[__RES_TYPE__, list, tuple, set, bool, None] = None) -> None: ...

    def stop(self) -> None: ...

    def pause(self, clear: bool = True) -> None: ...

    def resume(self) -> None: ...

    def wait(self,
             count: int = 1,
             timeout: float = None,
             fit_count: bool = True,
             raise_err: bool = None) -> Union[List[DataPacket], DataPacket, None]: ...

    def steps(self,
              count: int = None,
              timeout: float = None,
              gap=1) -> Iterable[Union[DataPacket, List[DataPacket]]]: ...

    @property
    def results(self) -> Union[DataPacket, Dict[str, List[DataPacket]], False]: ...

    def clear(self) -> None: ...

    def wait_silent(self,
                    timeout: float = None,
                    targets_only: bool = False,
                    limit: int = 0) -> bool: ...

    def _to_target(self, target_id: str, address: str, owner: ChromiumBase) -> None: ...

    def _requestWillBeSent(self, **kwargs) -> None: ...

    def _requestWillBeSentExtraInfo(self, **kwargs) -> None: ...

    def _response_received(self, **kwargs) -> None: ...

    def _responseReceivedExtraInfo(self, **kwargs) -> None: ...

    def _loading_finished(self, **kwargs) -> None: ...

    def _loading_failed(self, **kwargs) -> None: ...

    def _set_callback(self) -> None: ...


class FrameListener(Listener):
    def __init__(self, owner: ChromiumFrame):
        self._owner: ChromiumFrame = ...
        self._is_diff: bool = ...


class DataPacket(object):
    """返回的数据包管理类"""

    def __init__(self, tab_id: str, target: [str, bool]):
        self.tab_id: str = ...
        self.target: str = ...
        self.is_failed: bool = ...
        self._raw_request: Optional[dict] = ...
        self._raw_response: Optional[dict] = ...
        self._raw_post_data: str = ...
        self._raw_body: str = ...
        self._raw_fail_info: Optional[dict] = ...
        self._base64_body: bool = ...
        self._request: Request = ...
        self._response: Response = ...
        self._fail_info: Optional[FailInfo] = ...
        self._resource_type: str = ...
        self._requestExtraInfo: Optional[dict] = ...
        self._responseExtraInfo: Optional[dict] = ...

    @property
    def _request_extra_info(self) -> Optional[dict]: ...

    @property
    def _response_extra_info(self) -> Optional[dict]: ...

    @property
    def url(self) -> str: ...

    @property
    def method(self) -> str: ...

    @property
    def frameId(self) -> str: ...

    @property
    def resourceType(self) -> str: ...

    @property
    def request(self) -> Request: ...

    @property
    def response(self) -> Response: ...

    @property
    def fail_info(self) -> Optional[FailInfo]: ...

    def wait_extra_info(self, timeout: float = None) -> bool: ...


class Request(object):
    url: str = ...
    _headers: Union[CaseInsensitiveDict, None] = ...
    method: str = ...

    urlFragment = ...
    hasPostData = ...
    postDataEntries = ...
    mixedContentType = ...
    initialPriority = ...
    referrerPolicy = ...
    isLinkPreload = ...
    trustTokenParams = ...
    isSameSite = ...

    def __init__(self, data_packet: DataPacket, raw_request: dict, post_data: str):
        self._data_packet: DataPacket = ...
        self._request: dict = ...
        self._raw_post_data: str = ...
        self._postData: str = ...

    @property
    def headers(self) -> dict: ...

    @property
    def postData(self) -> Any: ...

    @property
    def cookies(self) -> List[dict]: ...

    @property
    def extra_info(self) -> Optional[RequestExtraInfo]: ...


class Response(object):
    url = ...
    status = ...
    statusText = ...
    headersText = ...
    mimeType = ...
    requestHeaders = ...
    requestHeadersText = ...
    connectionReused = ...
    connectionId = ...
    remoteIPAddress = ...
    remotePort = ...
    fromDiskCache = ...
    fromServiceWorker = ...
    fromPrefetchCache = ...
    encodedDataLength = ...
    timing = ...
    serviceWorkerResponseSource = ...
    responseTime = ...
    cacheStorageCacheName = ...
    protocol = ...
    alternateProtocolUsage = ...
    securityState = ...
    securityDetails = ...

    def __init__(self, data_packet: DataPacket, raw_response: dict, raw_body: str, base64_body: bool):
        self._data_packet: DataPacket = ...
        self._response: dict = ...
        self._raw_body: str = ...
        self._is_base64_body: bool = ...
        self._body: Union[str, dict, None] = ...
        self._headers: dict = ...

    @property
    def extra_info(self) -> Optional[ResponseExtraInfo]: ...

    @property
    def headers(self) -> CaseInsensitiveDict: ...

    @property
    def raw_body(self) -> str: ...

    @property
    def body(self) -> Any: ...


class ExtraInfo(object):
    def __init__(self, extra_info: dict):
        self._extra_info: dict = ...

    @property
    def all_info(self) -> dict: ...


class RequestExtraInfo(ExtraInfo):
    requestId: str = ...
    associatedCookies: List[dict] = ...
    headers: dict = ...
    connectTiming: dict = ...
    clientSecurityState: dict = ...
    siteHasCookieInOtherPartition: bool = ...


class ResponseExtraInfo(ExtraInfo):
    requestId: str = ...
    blockedCookies: List[dict] = ...
    headers: dict = ...
    resourceIPAddressSpace: str = ...
    statusCode: int = ...
    headersText: str = ...
    cookiePartitionKey: str = ...
    cookiePartitionKeyOpaque: bool = ...


class FailInfo(object):
    _data_packet: DataPacket
    _fail_info: dict
    _fail_info: float
    errorText: str
    canceled: bool
    blockedReason: Optional[str]
    corsErrorStatus: Optional[str]

    def __init__(self, data_packet: DataPacket, fail_info: dict): ...
