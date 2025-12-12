from datetime import datetime
from typing import Optional
from uuid import UUID

from LOGS.Entity.SerializableContent import SerializableContent


class ServerMetaData(SerializableContent):
    _application: Optional[str] = None
    _vendor: Optional[str] = None
    _version: Optional[str] = None
    _uid: Optional[UUID] = None
    _apiVersion: Optional[str] = None
    _edition: Optional[str] = None
    _groups: Optional[int] = None
    _licensedTo: Optional[str] = None
    _daysUntilExpiration: Optional[int] = None
    _expirationDate: Optional[datetime] = None
    _homepage: Optional[str] = None
    _email: Optional[str] = None

    @property
    def application(self) -> Optional[str]:
        return self._application

    @application.setter
    def application(self, value):
        self._application = self.checkAndConvertNullable(value, str, "application")

    @property
    def vendor(self) -> Optional[str]:
        return self._vendor

    @vendor.setter
    def vendor(self, value):
        self._vendor = self.checkAndConvertNullable(value, str, "vendor")

    @property
    def version(self) -> Optional[str]:
        return self._version

    @version.setter
    def version(self, value):
        self._version = self.checkAndConvertNullable(value, str, "version")

    @property
    def uid(self) -> Optional[UUID]:
        return self._uid

    @uid.setter
    def uid(self, value):
        self._uid = self.checkAndConvertNullable(value, UUID, "uid")

    @property
    def apiVersion(self) -> Optional[str]:
        return self._apiVersion

    @apiVersion.setter
    def apiVersion(self, value):
        self._apiVersion = self.checkAndConvertNullable(value, str, "apiVersion")

    @property
    def edition(self) -> Optional[str]:
        return self._edition

    @edition.setter
    def edition(self, value):
        self._edition = self.checkAndConvertNullable(value, str, "edition")

    @property
    def groups(self) -> Optional[int]:
        return self._groups

    @groups.setter
    def groups(self, value):
        self._groups = self.checkAndConvertNullable(value, int, "groups")

    @property
    def licensedTo(self) -> Optional[str]:
        return self._licensedTo

    @licensedTo.setter
    def licensedTo(self, value):
        self._licensedTo = self.checkAndConvertNullable(value, str, "licensedTo")

    @property
    def daysUntilExpiration(self) -> Optional[int]:
        return self._daysUntilExpiration

    @daysUntilExpiration.setter
    def daysUntilExpiration(self, value):
        self._daysUntilExpiration = self.checkAndConvertNullable(
            value, int, "daysUntilExpiration"
        )

    @property
    def expirationDate(self) -> Optional[datetime]:
        return self._expirationDate

    @expirationDate.setter
    def expirationDate(self, value):
        self._expirationDate = self.checkAndConvertNullable(
            value, datetime, "expirationDate"
        )

    @property
    def homepage(self) -> Optional[str]:
        return self._homepage

    @homepage.setter
    def homepage(self, value):
        self._homepage = self.checkAndConvertNullable(value, str, "homepage")

    @property
    def email(self) -> Optional[str]:
        return self._email

    @email.setter
    def email(self, value):
        self._email = self.checkAndConvertNullable(value, str, "email")
