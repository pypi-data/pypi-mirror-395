from typing import Any, Optional, cast

from LOGS.Auxiliary import MinimalModelGenerator, Tools
from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Exceptions import (
    EntityDeletingException,
    EntityFetchingException,
    EntityNotFoundException,
    EntityUpdatingException,
)
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.LOGSConnection import LOGSConnection

# SELF = TypeVar("SELF", bound="Entity")


class Entity(ConnectedEntity):
    _id: Constants.ID_TYPE
    _defaultRequestParameter: dict = EntityRequestParameter().toDict()

    def __init__(
        self,
        ref=None,
        id: Optional[Constants.ID_TYPE] = None,
        connection: Optional[LOGSConnection] = None,
    ):
        """Represents a connected LOGS entity type"""
        if id:
            self._id = id

        super().__init__(ref=ref, connection=connection)

    def _getConnectionData(self):
        (connection, endpoint) = super()._getConnectionData()

        if not self.id:
            raise EntityNotFoundException(self)

        return connection, endpoint, self.id

    def __str__(self):
        return Tools.ObjectToString(self)

    def getUIUrl(self) -> str:
        uiEndpoint = self._uiEndpoint
        if not uiEndpoint:
            raise NotImplementedError(
                "No UI endpoint specified for entity type %a."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )
        connection = self._getConnection()

        return connection.getUIEndpointUrl(uiEndpoint + [str(self.id)])

    def _fetchEntity(self, connection: LOGSConnection):
        if not self._endpoint:
            raise NotImplementedError(
                "Fetching of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        ref, responseError = connection.getEndpoint(
            cast(Any, self._endpoint + [str(self.id)]), self._defaultRequestParameter
        )
        if responseError:
            raise EntityFetchingException(entity=self, responseError=responseError)

        if isinstance(ref, dict) and "url" in ref:
            del ref["url"]
        self._fromRef(ref, type(self))
        self._setConnection(connection)

    def fetch(self):
        self._fetchEntity(self._getConnection())

    def _restoreEntity(self, connection: LOGSConnection):
        if not self._endpoint:
            raise NotImplementedError(
                "Updating of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if not self.id:
            raise EntityNotFoundException(self)

        data, responseError = connection.postEndpoint(
            self._endpoint + ["restore", self.id], data=self.toDict()
        )
        if responseError:
            raise EntityUpdatingException(entity=self, responseError=responseError)

        self.override(data)

    def _updateEntity(self, connection: LOGSConnection):
        if not self._endpoint:
            raise NotImplementedError(
                "Updating of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if not self.id:
            raise EntityNotFoundException(self)

        data, responseError = connection.putEndpoint(
            self._endpoint + [self.id], data=self.toDict()
        )
        if responseError:
            raise EntityUpdatingException(entity=self, responseError=responseError)

        self.override(data)

    def _deleteEntity(self, connection: LOGSConnection, permanently: bool = False):
        if not self._endpoint:
            raise NotImplementedError(
                "Deleting of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if not self.id:
            raise EntityNotFoundException(self)

        _, responseError = connection.deleteEndpoint(
            self._endpoint + [self.id], parameters={"deletePermanently": permanently}
        )
        if hasattr(self, "isDeleted"):
            setattr(self, "isDeleted", True)

        if permanently:
            self._connection = None

        if responseError:
            if [
                e
                for e in responseError.errorStringList
                if "Soft-Delete is not supported" in e
            ]:
                raise EntityDeletingException(
                    entityIds=self.id,
                    errors=[
                        "This entity cannot be trashed.",
                        "Please use 'permanently = true' parameter.",
                    ],
                )
            else:
                raise EntityDeletingException(
                    entityIds=self.id, responseError=responseError
                )

    def update(self):
        self._updateEntity(self._getConnection())

    def restore(self):
        self._restoreEntity(self._getConnection())

    def delete(self, permanently: bool = False):
        self._deleteEntity(self._getConnection(), permanently=permanently)

    def toMinimal(self):
        return MinimalModelGenerator.MinimalFromSingle(
            self.toDict(), type(self).__name__, None, self._getConnection()
        )

    @property
    def identifier(self):
        name = (
            f" '{getattr(self, 'name')}'"
            if hasattr(self, "name") and getattr(self, "name")
            else ""
        )
        return "%s(id:%s)%s" % (
            type(self).__name__,
            str(self.id),
            name,
        )

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value
