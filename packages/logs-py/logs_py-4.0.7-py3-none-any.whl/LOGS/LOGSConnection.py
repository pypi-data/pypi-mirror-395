import json
import random
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast

import requests
from requests import Response

from LOGS.Auxiliary import LOGSException, Tools
from LOGS.Auxiliary.LOGSErrorResponse import LOGSErrorResponse
from LOGS.Entities.FileEntry import FileEntry
from LOGS.LOGSOptions import LOGSOptions
from LOGS.ServerMetaData import ServerMetaData


class ResponseTypes(Enum):
    RAW = "raw"
    JSON = "json"


RESPONSE_TYPES = Union[bytes, Dict[Any, Any], Response, str]


@dataclass
class MultipartEntry:
    name: str
    fileName: Optional[str]
    content: Union[str, dict, FileEntry]


class LOGSConnection:
    """Python class to access the LOGS web API"""

    _noErrorStates = set([200, 201, 204])
    _compatibleAPIVersions = set(["4.0"])
    # _compatibleAPIVersions = set(["1.1"])
    __urlRe = re.compile(r"(?:(https*)\:\/\/)*([^\/:]+)(?:\:(\d+))*(?:\/(.*))*")
    __urlApiRe = re.compile(r"api\/(\d+\.\d+)")
    _port: Optional[int]
    _connected: bool
    _metadata: ServerMetaData

    def __init__(
        self,
        url: str,
        apiKey: str,
        use_internal: bool = False,
        options: Optional[LOGSOptions] = None,
        verify: bool = True,
    ):
        """Checks the connection to the server on creation

        :param url: URL to specific LOGS group (e.g. https://mylogs/mygroup or https://mylogs:80/mygroup/api/0.1)
        :param api_key: The API key that grants access to LOGS (you need to generate on in LOGS and copy it)
        :param verbose: If set you see some information about the server connection. Defaults to False.

        :raises Exception: URL does not defined or is invalid.
        :raises Exception: The URL does not define a group.
        :raises Exception: Server cannot be reached.
        """
        self._options = Tools.checkAndConvert(
            options, LOGSOptions, "options", initOnNone=True
        )
        self.promptPrefix = "LOGSAPI>"

        self.url = url

        if self._options.showServerInfo:
            self.printServerStatus()

        self._apiKey = apiKey
        self._useInternal = use_internal
        self._verify = verify
        self._connected = False
        self._metadata = ServerMetaData()

        self.checkServer()

    def printServerStatus(self):
        print(self.promptPrefix, "Server properties:")
        print(self.promptPrefix, "   protocol:", self._protocol)
        print(self.promptPrefix, "   server:", self._server)
        print(self.promptPrefix, "   port:", self._port)
        print(self.promptPrefix, "   group:", self._group)

    def setUrl(self, url):
        match = self.__urlRe.search(url)
        protocol = "http"
        version = "0.1"
        if not match:
            raise Exception("Invalid URL '%s'." % url)
        else:
            (protocol, server, portStr, endpoints) = match.groups()
            if endpoints:
                group = endpoints.split("/")[0]
            else:
                group = None
            if server == None or server == "":
                raise Exception("URL must define a server.")
            if group == None or group == "":
                raise Exception("URL must contain a group.")

            if portStr == None or portStr == "":
                port = None
            else:
                port = int(portStr)

            match = self.__urlApiRe.search(endpoints)
            if match:
                version = match.group(1)

        # print("match", (protocol, server, port, group, version))

        self._version = version
        self._protocol = protocol
        self._server = server
        self._port = port
        self._group = group
        # self._url = url

    def checkServer(self):
        """Check if server can be reached

        :raises Exception: Server cannot be reached.
        """
        testEndpoint = ["version", "detail"]

        result, error = self.getEndpoint(testEndpoint)
        url = result["url"] if isinstance(result, dict) else self.url
        if error:
            raise LOGSException(
                "Could not connect to '%s': %s" % (url, error.errorString())
            )
        if self._options.showServerInfo:
            print(
                self.promptPrefix,
                "Connection to server '%s://%s%s' successful."
                % (
                    self.protocol,
                    self.server,
                    ":" + str(self.port) if self.port else "",
                ),
            )
        self._connected = True

        if isinstance(result, dict):
            self._metadata = ServerMetaData(ref=result)
            if (
                not self._metadata.apiVersion
                or self._metadata.apiVersion not in self._compatibleAPIVersions
            ):
                raise LOGSException(
                    "This library is not compatible with the LOGS API version '%s'. (Expected %s %s)"
                    % (
                        (
                            self._metadata.apiVersion
                            if self._metadata.apiVersion
                            else "unknown"
                        ),
                        (
                            "one of versions"
                            if len(self._compatibleAPIVersions) > 1
                            else "version"
                        ),
                        Tools.eclipsesJoin(", ", list(self._compatibleAPIVersions)),
                    )
                )
        else:
            raise LOGSException(
                "Server '%s' could be reached but behaved unexpectedly." % (url, error)
            )

    def getUIUrl(self) -> str:
        """Generate full API URL

        Returns:
            str: The url of the connected LOGS API (e.g. https://logs.com/api/2.1)
        """
        return "%s://%s%s/%s" % (
            self.protocol,
            self.server,
            ":" + str(self.port) if self.port else "",
            self.group,
        )

    def getAPIUrl(self) -> str:
        """Generate full API URL

        :return: The url of the connected LOGS API (e.g. https://logs.com/api/2.1)
        """
        return "%s://%s%s/%s/api/%s" % (
            self.protocol,
            self.server,
            ":" + str(self.port) if self.port else "",
            self.group,
            self.version,
        )

    def getUIEndpointUrl(
        self, endpoint: Union[Union[str, int], Sequence[Union[str, int]]]
    ) -> str:
        """Generate full API URL for a given endpoint

        Returns:
            str: The url of the connected LOGS API (for dataset endpoint e.g. https://logs.com/api/2.1/dataset)
        """

        if isinstance(endpoint, list):
            endpoint = "/".join([str(e) for e in endpoint])

        return self.getUIUrl() + "/" + str(endpoint)

    def getEndpointUrl(
        self, endpoint: Union[Union[str, int], Sequence[Union[str, int]]]
    ) -> str:
        """Generate full API URL for a given endpoint

        :return: The url of the connected LOGS API (for dataset endpoint e.g. https://logs.com/api/2.1/dataset)
        """

        if isinstance(endpoint, list):
            endpoint = "/".join([str(e) for e in endpoint])

        return self.getAPIUrl() + "/" + str(endpoint)

    def getUrl(
        self,
        url: str,
        parameters: Optional[dict] = None,
        responseType: ResponseTypes = ResponseTypes.JSON,
        includeUrl: bool = True,
    ):
        """Generate full API URL with GET parameters

        :param url: Specify an API url otherwise object internal is used. Defaults to None.
        :param parameters: Parameters to pass to an GET request. Defaults to None.
        :param responseType: The return value is converted to the specified format. Defaults to "json".
        :param includeUrl:

        :return: The response of the server and the error code.
        """
        if self._options.showRequestUrl:
            paramString = ""
            if parameters:
                paramString = " ".join(
                    ("%s:%s" % (k, v))
                    for k, v in parameters.items()
                    if v != None and v != ""
                )
            print(
                self.promptPrefix,
                "GET: %s %s" % (url, "{" + paramString + "}" if paramString else ""),
            )
        if self._options.showRequestHeader:
            print(self.promptPrefix, "HEADER: %s" % self.getHeader())

        # print("params", params)
        response = requests.get(
            url, headers=self.getHeader(), params=parameters, verify=self._verify
        )
        # print("URL:", response.url)

        # if response == None:
        #     response =
        # print("url", url)
        return self.__convertResponse(response, responseType, includeUrl)

    def getHeader(self) -> Dict[str, str]:
        header = {"X-Api-Key": self.apiKey}

        if self._useInternal:
            header["X-LOGS-internal"] = "true"

        if self._options.proxyTargetUrl:
            header["X-Target-Backend"] = self._options.proxyTargetUrl

        return header

    def deleteUrl(
        self,
        url: str,
        parameters: dict = {},
        responseType: ResponseTypes = ResponseTypes.JSON,
        includeUrl: bool = True,
    ):
        """Generate full API URL with PUT body

        :param url: Specify an API url otherwise object internal is used. Defaults to None.
        :param params: Parameters to pass to an PUT request as json body. Defaults to None.
        :param mode: The return value is converted to the specified format. Defaults to "json".

        :return: The response of the server and the error code.
        """

        if self._options.showRequestUrl:
            print(self.promptPrefix, "DELETE: %s" % url)
        if self._options.showRequestHeader:
            print(self.promptPrefix, "HEADER: %s" % self.getHeader())

        response = requests.delete(
            url, headers=self.getHeader(), params=parameters, verify=self._verify
        )
        return self.__convertResponse(response, responseType, includeUrl=includeUrl)

    def putUrl(
        self,
        url: str,
        data: Union[dict, list] = {},
        responseType: ResponseTypes = ResponseTypes.JSON,
    ):
        """Generate full API URL with PUT body

        :param url: Specify an API url otherwise object internal is used. Defaults to None.
        :param params: Parameters to pass to an PUT request as json body. Defaults to None.
        :param mode: The return value is converted to the specified format. Defaults to "json".

        :return: The response of the server and the error code.
        """

        if self._options.showRequestUrl:
            print(self.promptPrefix, "PUT: %s" % url)
        if self._options.showRequestHeader:
            print(self.promptPrefix, "HEADER: %s" % self.getHeader())

        if self._options.showRequestBody:
            print(self.promptPrefix, "BODY: %s" % self.__convertBody(data))

        response = requests.put(
            url, headers=self.getHeader(), json=data, verify=self._verify
        )
        return self.__convertResponse(response, responseType)

    def putEndpoint(
        self,
        endpoint: Union[Union[str, int], Sequence[Union[str, int]]],
        data: Union[dict, list] = {},
        responseType: ResponseTypes = ResponseTypes.JSON,
    ) -> Tuple[Optional[RESPONSE_TYPES], Optional[LOGSErrorResponse]]:
        """Connects to the API with PUT access to given endpoint

        :param endpoint: Name of the endpoint (e.g. dataset/2/tracks)
        :param params: Parameters to pass to the endpoint as json body. Defaults to None.

        :return: The response of the server and the error code.
        """
        url = self.getEndpointUrl(endpoint)

        return self.putUrl(url, data, responseType)

    def postMultipartUrl(
        self,
        url: str,
        data: List[MultipartEntry] = [],
        responseType: ResponseTypes = ResponseTypes.JSON,
    ):
        if self._options.showRequestUrl:
            print(self.promptPrefix, "POST: %s" % url)
        if self._options.showRequestHeader:
            print(self.promptPrefix, "HEADER: %s" % self.getHeader())

        if self._options.showRequestBody:
            separator = "-" * 29 + "".join(
                [str(random.randint(0, 9)) for _ in range(29)]
            )

        files = []
        for entry in data:
            content: Any = ""
            if isinstance(entry.content, FileEntry):
                # content = entry.content.toJson(compact=True)
                with open(entry.content.path, "rb") as read:
                    content = read.read()
            else:
                content = json.dumps(entry.content)

            if self._options.showRequestBody:
                print(self.promptPrefix, "BODY: %s" % separator)
                print(
                    self.promptPrefix,
                    "BODY: %s"
                    % "Content-Disposition: form-data; name='entry.fileName'",
                )

                c = (
                    str(content[:100]) + "..."
                    if isinstance(content, bytes) and len(content) > 100
                    else content
                )
                print(self.promptPrefix, "BODY: %s" % c)

            files.append((entry.name, (entry.fileName, content)))

        #### For checking the request
        # request = requests.Request(
        #     "POST", "http://localhost:900/sandbox/api/0.1/datasets/create", files=files
        # ).prepare()
        # print(cast(Any, request.body).decode("ascii", "ignore"))

        response = requests.post(
            url, headers=self.getHeader(), files=files, verify=self._verify
        )

        return self.__convertResponse(response, responseType)

    def postUrl(
        self,
        url: str,
        data: Union[dict, list] = {},
        parameters: Optional[dict] = None,
        responseType: ResponseTypes = ResponseTypes.JSON,
        includeUrl: bool = True,
    ):
        """Generate full API URL with PUT body

        :param url: Specify an API url otherwise object internal is used. Defaults to None.
        :param params: Parameters to pass to an PUT request as json body. Defaults to None.
        :param mode: The return value is converted to the specified format. Defaults to "json".

        :return: The response of the server and the error code.
        """
        if self._options.showRequestUrl:
            paramString = ""
            if parameters:
                paramString = " ".join(
                    ("%s:%s" % (k, v))
                    for k, v in parameters.items()
                    if v != None and v != ""
                )
            print(
                self.promptPrefix,
                "POST: %s %s" % (url, "{" + paramString + "}" if paramString else ""),
            )
        if self._options.showRequestHeader:
            print(self.promptPrefix, "HEADER: %s" % self.getHeader())

        if self._options.showRequestBody:
            print(self.promptPrefix, "BODY: %s" % self.__convertBody(data))

        response = requests.post(
            url,
            headers=self.getHeader(),
            params=parameters,
            json=data,
            verify=self._verify,
        )
        return self.__convertResponse(response, responseType, includeUrl)

    def postMultipartEndpoint(
        self,
        endpoint: Union[Union[str, int], Sequence[Union[str, int]]],
        data: List[MultipartEntry] = [],
        responseType: ResponseTypes = ResponseTypes.JSON,
    ):
        url = self.getEndpointUrl(endpoint)

        return self.postMultipartUrl(url, data, responseType)

    def postEndpoint(
        self,
        endpoint: Union[Union[str, int], Sequence[Union[str, int]]],
        parameters: Optional[dict] = None,
        data: Union[dict, list] = {},
        responseType: ResponseTypes = ResponseTypes.JSON,
    ):
        """Connects to the API with PUT access to given endpoint

        :param endpoint: Name of the endpoint (e.g. dataset/2/tracks)
        :param params: Parameters to pass to the endpoint as json body. Defaults to None.

        :return: The response of the server and the error code.
        """
        url = self.getEndpointUrl(endpoint)

        return self.postUrl(
            url=url, data=data, parameters=parameters, responseType=responseType
        )

    def deleteEndpoint(
        self,
        endpoint: Union[Union[str, int], Sequence[Union[str, int]]],
        parameters: dict = {},
        responseType: ResponseTypes = ResponseTypes.JSON,
        includeUrl: bool = True,
    ):
        """Connects to the API with DELETE access to given endpoint

        :param endpoint: Name of the endpoint (e.g. dataset/2/tracks)
        :param params: Parameters to pass to the endpoint. Defaults to None.
        :param mode: Convert result to this format. Defaults to None.

        :return: The response of the server and the error code.
        """
        # print("Headers:", headers)
        # print("Params:", params)
        url = self.getEndpointUrl(endpoint)

        return self.deleteUrl(
            url, parameters=parameters, responseType=responseType, includeUrl=includeUrl
        )

    def getEndpoint(
        self,
        endpoint: Union[Union[str, int], Sequence[Union[str, int]]],
        parameters: Optional[dict] = None,
        responseType: ResponseTypes = ResponseTypes.JSON,
        includeUrl: bool = True,
    ) -> Tuple[Optional[RESPONSE_TYPES], Optional[LOGSErrorResponse]]:
        """Connects to the API with GET access to given endpoint

        :param endpoint: Name of the endpoint (e.g. dataset/2/tracks)
        :param params: Parameters to pass to the endpoint. Defaults to None.
        :param mode: Convert result to this format. Defaults to None.

        :return: The response of the server and the error code.
        """
        # print("Headers:", headers)
        # print("Params:", params)
        url = self.getEndpointUrl(endpoint)
        # print("URL:", url)
        # print("Params:", params)

        return self.getUrl(
            url, parameters=parameters, responseType=responseType, includeUrl=includeUrl
        )

        # header = {"X-Api-Key": api_key}

        # # try:
        # response = requests.get(url, headers=header, params=params, verify=False, verify=self._verify)
        # # except ValueError as error:
        # #     print(error)
        # return self.convertResponse(response, mode)

    # def convertCustomFieldParams(self, params: dict):
    #     # print(">", params)
    #     return {"customFields[%s]" % k: v for k, v in params.items()}

    @classmethod
    def __convertBody(cls, body) -> str:
        if body == None:
            return "None"
        if isinstance(body, dict) or isinstance(body, list):
            return json.dumps(body)
        return body

    def __convertResponse(
        self,
        response: Response,
        responseType: ResponseTypes = ResponseTypes.JSON,
        includeUrl: bool = True,
    ) -> Tuple[Optional[RESPONSE_TYPES], Optional[LOGSErrorResponse]]:
        if response.status_code >= 200 and response.status_code < 300:
            if responseType == ResponseTypes.RAW:
                return response.content, None
            else:
                try:
                    result = response.json() if len(response.content) > 0 else ""
                    if isinstance(result, dict) and includeUrl:
                        result["url"] = response.url
                    return cast(Union[dict, str], result), None
                except:
                    errors = []
                    try:
                        errors = response.text.split("\n")
                    except:
                        pass
                    errorResponse = LOGSErrorResponse()
                    errors.insert(0, "%d %s" % (response.status_code, response.reason))
                    errorResponse.errors = errors
        else:

            if response.status_code in self._noErrorStates:
                errorResponse = LOGSErrorResponse()
                errorResponse.status = response.status_code
            else:
                try:
                    r = response.json()
                    errorResponse = LOGSErrorResponse(r)
                except:
                    errors = []
                    try:
                        errors = response.text.split("\n")
                    except:
                        pass
                    errorResponse = LOGSErrorResponse()
                    errors.insert(0, "%d %s" % (response.status_code, response.reason))
                    errorResponse.errors = errors

        return (
            response,
            (
                errorResponse
                if errorResponse and errorResponse.errorStringList
                else None
            ),
        )

    @property
    def version(self) -> str:
        return self._version

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def server(self) -> str:
        return self._server

    @property
    def port(self) -> Optional[int]:
        return self._port

    @property
    def group(self) -> str:
        return self._group

    @property
    def apiUrl(self) -> str:
        return "%s/api/%s" % (self.url, self.version)

    @property
    def url(self) -> str:
        return "%s://%s%s/%s" % (
            self.protocol,
            self.server,
            ":" + str(self.port) if self.port else "",
            self.group,
        )

    @url.setter
    def url(self, value):
        self.setUrl(value)

    @property
    def apiKey(self) -> str:
        return self._apiKey

    @apiKey.setter
    def apiKey(self, value):
        self._apiKey = value

    @property
    def metadata(self) -> ServerMetaData:
        return self._metadata
