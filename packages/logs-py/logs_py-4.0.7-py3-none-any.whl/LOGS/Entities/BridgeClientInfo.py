from datetime import datetime
from typing import Optional
from uuid import UUID

from LOGS.Entity.SerializableContent import SerializableContent


class BridgeClientInfo(SerializableContent):
    _id: Optional[UUID] = None
    _host: Optional[str] = None
    _clientVersion: Optional[str] = None
    _ipAddress: Optional[str] = None
    _executablePath: Optional[str] = None
    _operatingSystem: Optional[str] = None
    _firstSeen: Optional[datetime] = None
    _isApproved: Optional[bool] = None
    _bridgeId: Optional[int] = None

    @property
    def id(self) -> Optional[UUID]:
        return self._id

    @id.setter
    def id(self, value):
        self._id = self.checkAndConvertNullable(value, UUID, "id")

    @property
    def host(self) -> Optional[str]:
        return self._host

    @host.setter
    def host(self, value):
        self._host = self.checkAndConvertNullable(value, str, "host")

    @property
    def clientVersion(self) -> Optional[str]:
        return self._clientVersion

    @clientVersion.setter
    def clientVersion(self, value):
        self._clientVersion = self.checkAndConvertNullable(value, str, "clientVersion")

    @property
    def ipAddress(self) -> Optional[str]:
        return self._ipAddress

    @ipAddress.setter
    def ipAddress(self, value):
        self._ipAddress = self.checkAndConvertNullable(value, str, "ipAddress")

    @property
    def executablePath(self) -> Optional[str]:
        return self._executablePath

    @executablePath.setter
    def executablePath(self, value):
        self._executablePath = self.checkAndConvertNullable(
            value, str, "executablePath"
        )

    @property
    def operatingSystem(self) -> Optional[str]:
        return self._operatingSystem

    @operatingSystem.setter
    def operatingSystem(self, value):
        self._operatingSystem = self.checkAndConvertNullable(
            value, str, "operatingSystem"
        )

    @property
    def firstSeen(self) -> Optional[datetime]:
        return self._firstSeen

    @firstSeen.setter
    def firstSeen(self, value):
        self._firstSeen = self.checkAndConvertNullable(value, datetime, "firstSeen")

    @property
    def isApproved(self) -> Optional[bool]:
        return self._isApproved

    @isApproved.setter
    def isApproved(self, value):
        self._isApproved = self.checkAndConvertNullable(value, bool, "isApproved")

    @property
    def bridgeId(self) -> Optional[int]:
        return self._bridgeId

    @bridgeId.setter
    def bridgeId(self, value):
        self._bridgeId = self.checkAndConvertNullable(value, int, "bridgeId")
