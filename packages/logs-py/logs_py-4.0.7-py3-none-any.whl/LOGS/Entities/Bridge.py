from enum import Enum
from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import LOGSMultilineException
from LOGS.Entities.AutoloadFileInfo import AutoloadFileInfo
from LOGS.Entities.BridgeClientInfo import BridgeClientInfo
from LOGS.Entities.BridgeType import BridgeType
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity


class SFTPAuthenticationMethodOption(Enum):
    PrivateKey = "PrivateKey"
    Password = "Password"


@Endpoint("bridges")
class Bridge(
    IEntityWithIntId,
    IUniqueEntity,
    INamedEntity,
    IEntryRecord,
    IModificationRecord,
    IGenericPermissionEntity,
):
    _type: Optional[BridgeType] = None
    _hostname: Optional[str] = None
    _ipAddress: Optional[str] = None
    _description: Optional[str] = None
    _username: Optional[str] = None
    _port: Optional[int] = None
    _connectedClients: Optional[List[BridgeClientInfo]] = None
    _isConnected: Optional[bool] = None
    _areMultipleClientsConnected: Optional[bool] = None
    _sftpAuthenticationMethod: Optional[SFTPAuthenticationMethodOption] = None

    _password: Optional[str] = None
    _privateKey: Optional[str] = None

    def readDirectory(self):
        connection, endpoint, id = self._getConnectionData()

        data, responseError = connection.postEndpoint(endpoint + [id, "read_directory"])
        if responseError:
            raise LOGSMultilineException(responseError=responseError)

        return self.checkListAndConvertNullable(
            data, AutoloadFileInfo, "directory content"
        )

    @property
    def url(self):
        return "{type}://{user}@{host}{port}".format(
            type=str(self.type.name if self.type else "").lower(),
            user=self.username,
            host=self.hostname,
            port=":%d" % self.port if self.port else ":22",
        )

    @property
    def type(self) -> Optional[BridgeType]:
        return self._type

    @type.setter
    def type(self, value):
        self._type = self.checkAndConvertNullable(value, BridgeType, "type")

    @property
    def hostname(self) -> Optional[str]:
        return self._hostname

    @hostname.setter
    def hostname(self, value):
        self._hostname = self.checkAndConvertNullable(value, str, "hostname")

    @property
    def ipAddress(self) -> Optional[str]:
        return self._ipAddress

    @ipAddress.setter
    def ipAddress(self, value):
        self._ipAddress = self.checkAndConvertNullable(value, str, "ipAddress")

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, value):
        self._description = self.checkAndConvertNullable(value, str, "description")

    @property
    def username(self) -> Optional[str]:
        return self._username

    @username.setter
    def username(self, value):
        self._username = self.checkAndConvertNullable(value, str, "username")

    @property
    def port(self) -> Optional[int]:
        return self._port

    @port.setter
    def port(self, value):
        self._port = self.checkAndConvertNullable(value, int, "port")

    @property
    def connectedClients(self) -> Optional[List[BridgeClientInfo]]:
        return self._connectedClients

    @connectedClients.setter
    def connectedClients(self, value):
        self._connectedClients = self.checkListAndConvertNullable(
            value, BridgeClientInfo, "connectedClients"
        )

    @property
    def isConnected(self) -> Optional[bool]:
        return self._isConnected

    @isConnected.setter
    def isConnected(self, value):
        self._isConnected = self.checkAndConvertNullable(value, bool, "isConnected")

    @property
    def areMultipleClientsConnected(self) -> Optional[bool]:
        return self._areMultipleClientsConnected

    @areMultipleClientsConnected.setter
    def areMultipleClientsConnected(self, value):
        self._areMultipleClientsConnected = self.checkAndConvertNullable(
            value, bool, "areMultipleClientsConnected"
        )

    @property
    def sftpAuthenticationMethod(self) -> Optional[SFTPAuthenticationMethodOption]:
        return self._sftpAuthenticationMethod

    @sftpAuthenticationMethod.setter
    def sftpAuthenticationMethod(self, value):
        self._sftpAuthenticationMethod = self.checkAndConvertNullable(
            value, SFTPAuthenticationMethodOption, "sftpAuthenticationMethod"
        )

    @property
    def password(self) -> Optional[str]:
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.checkAndConvertNullable(value, str, "password")

    @property
    def privateKey(self) -> Optional[str]:
        return self._privateKey

    @privateKey.setter
    def privateKey(self, value):
        self._privateKey = self.checkAndConvertNullable(value, str, "privateKey")
