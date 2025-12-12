from typing import Any, Optional, cast

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import LOGSException
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.EntitiesRequestParameter import EntitiesRequestParameter
from LOGS.Entity.Entity import Entity
from LOGS.Entity.EntityIterator import EntityIterator
from LOGS.Entity.EntityMinimalWithType import EntityMinimalWithType
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.LOGSConnection import LOGSConnection


@Endpoint("entities")
class Entities(EntityIterator[Entity, EntityRequestParameter]):
    """LOGS connected multi Entity iterator"""

    _generatorType = EntityMinimalWithType  # type: ignore
    _parameterType = EntitiesRequestParameter  # type: ignore

    def __init__(
        self,
        connection: Optional[LOGSConnection],
        parameters: Optional[EntitiesRequestParameter] = None,
    ):
        super().__init__(connection=connection, parameters=cast(Any, parameters))

    def _convertToEntity(self, entity: EntityMinimalWithType):
        return MinimalModelGenerator.MinimalFromSingle(
            entity.toDict(), entity.type, None, connection=self._getConnection()
        )

    def __next__(self) -> EntityMinimalWithType:
        entity = cast(EntityMinimalWithType, super().__next__())
        result = self._convertToEntity(entity)
        if not result:
            raise LOGSException(
                "Unknown entity %a of type %a." % (str(entity), entity.type)
            )

        return result

    def fetch(self, uid: str):
        self._entityIterator = 0

        if not self._connection:
            raise LOGSException(
                "Entity connector %a is not connected" % type(self).__name__
            )

        if not self._endpoint:
            raise NotImplementedError(
                "Endpoint missing for of entity type %a."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        ref, responseError = self._connection.getEndpoint(self._endpoint + [str(uid)])
        if responseError:
            raise LOGSException(
                message="Could not fetch entity with uid %a: %s"
                % (uid, responseError.errorString()),
                responseError=responseError,
            )

        entity = Tools.checkAndConvert(ref, EntityMinimalWithType)
        return self._convertToEntity(entity)
