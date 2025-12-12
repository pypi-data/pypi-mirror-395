#!/usr/bin/env python3
"""
A library to access the LOGS API via Python
"""

import json
import os
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)
from uuid import UUID

from LOGS.Auxiliary import (
    Constants,
    EntityCreatingException,
    EntityDeletingException,
    EntityNotFoundException,
    EntityUpdatingException,
    LOGSException,
    Tools,
)
from LOGS.Auxiliary.CustomEntityClassGenerator import CustomEntityClassGenerator
from LOGS.Entities.Attachment import Attachment
from LOGS.Entities.AttachmentRequestParameter import AttachmentRequestParameter
from LOGS.Entities.Attachments import Attachments
from LOGS.Entities.Bridge import Bridge
from LOGS.Entities.BridgeRequestParameter import BridgeRequestParameter
from LOGS.Entities.Bridges import Bridges
from LOGS.Entities.CustomField import CustomField
from LOGS.Entities.CustomFieldRequestParameter import CustomFieldRequestParameter
from LOGS.Entities.CustomFields import CustomFields
from LOGS.Entities.CustomType import CustomType
from LOGS.Entities.CustomTypeRequestParameter import CustomTypeRequestParameter
from LOGS.Entities.CustomTypes import CustomTypes
from LOGS.Entities.DataFormat import DataFormat
from LOGS.Entities.DataFormatInstrument import DataFormatInstrument
from LOGS.Entities.DataFormatInstrumentRequestParameter import (
    DataFormatInstrumentRequestParameter,
)
from LOGS.Entities.DataFormatInstruments import DataFormatInstruments
from LOGS.Entities.DataFormatRequestParameter import DataFormatRequestParameter
from LOGS.Entities.DataFormats import DataFormats
from LOGS.Entities.Dataset import Dataset
from LOGS.Entities.DatasetCreator import DatasetCreator
from LOGS.Entities.DatasetMatching import DatasetMatching
from LOGS.Entities.DatasetMatchTypes import DatasetsUpdatableFiles
from LOGS.Entities.DatasetRequestParameter import DatasetRequestParameter
from LOGS.Entities.Datasets import Datasets
from LOGS.Entities.DataSource import DataSource
from LOGS.Entities.DataSourceRequestParameter import DataSourceRequestParameter
from LOGS.Entities.DataSources import DataSources
from LOGS.Entities.Entities import Entities
from LOGS.Entities.EntitiesRequestParameter import EntitiesRequestParameter
from LOGS.Entities.EntityOriginWriteModelWithId import EntityOriginWriteModelWithId
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entities.InventoryItem import InventoryItem
from LOGS.Entities.InventoryItemRequestParameter import InventoryItemRequestParameter
from LOGS.Entities.InventoryItems import InventoryItems
from LOGS.Entities.LabNotebook import LabNotebook
from LOGS.Entities.LabNotebookEntries import LabNotebookEntries
from LOGS.Entities.LabNotebookEntry import LabNotebookEntry
from LOGS.Entities.LabNotebookEntryRequestParameter import (
    LabNotebookEntryRequestParameter,
)
from LOGS.Entities.LabNotebookExperiment import LabNotebookExperiment
from LOGS.Entities.LabNotebookExperimentRequestParameter import (
    LabNotebookExperimentRequestParameter,
)
from LOGS.Entities.LabNotebookExperiments import LabNotebookExperiments
from LOGS.Entities.LabNotebookRequestParameter import LabNotebookRequestParameter
from LOGS.Entities.LabNotebooks import LabNotebooks
from LOGS.Entities.LabNotebookTemplate import LabNotebookTemplate
from LOGS.Entities.LabNotebookTemplateRequestParameter import (
    LabNotebookTemplateRequestParameter,
)
from LOGS.Entities.LabNotebookTemplates import LabNotebookTemplates
from LOGS.Entities.Method import Method
from LOGS.Entities.MethodRequestParameter import MethodRequestParameter
from LOGS.Entities.Methods import Methods
from LOGS.Entities.Origin import Origin
from LOGS.Entities.OriginRequestParameter import OriginRequestParameter
from LOGS.Entities.Origins import Origins
from LOGS.Entities.Person import Person
from LOGS.Entities.PersonRequestParameter import PersonRequestParameter
from LOGS.Entities.Persons import Persons
from LOGS.Entities.Project import Project
from LOGS.Entities.ProjectRequestParameter import ProjectRequestParameter
from LOGS.Entities.Projects import Projects
from LOGS.Entities.Role import Role
from LOGS.Entities.RoleRequestParameter import RoleRequestParameter
from LOGS.Entities.Roles import Roles
from LOGS.Entities.Sample import Sample
from LOGS.Entities.SampleRequestParameter import SampleRequestParameter
from LOGS.Entities.Samples import Samples
from LOGS.Entities.SharedContent import SharedContent
from LOGS.Entities.SharedContentRequestParameter import SharedContentRequestParameter
from LOGS.Entities.SharedContents import SharedContents
from LOGS.Entities.Vendor import Vendor
from LOGS.Entities.VendorRequestParameter import VendorRequestParameter
from LOGS.Entities.Vendors import Vendors
from LOGS.Entity import Entity, EntityIterator
from LOGS.Entity.ConnectedEntity import ConnectedEntity
from LOGS.Interfaces.ISoftDeletable import ISoftDeletable
from LOGS.Interfaces.ITypedEntity import ITypedEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity
from LOGS.LOGSConnection import LOGSConnection
from LOGS.LOGSOptions import LOGSOptions
from LOGS.ServerMetaData import ServerMetaData

if TYPE_CHECKING:
    from LOGS.Entities.DataFormatMinimal import DataFormatMinimal
    from LOGS.Entities.ProjectMinimal import ProjectMinimal

_T = TypeVar("_T", bound=Union[Constants.ENTITIES, Entity])


class test:
    pass


class LOGS:
    """Python class to access the LOGS web API"""

    _connection: LOGSConnection
    _entities: Sequence[Type[Constants.ENTITIES]] = [
        Bridge,
        CustomField,
        CustomType,
        Dataset,
        DataSource,
        InventoryItem,
        LabNotebook,
        LabNotebookEntry,
        LabNotebookExperiment,
        Origin,
        Person,
        Project,
        Sample,
        DataFormat,
        Role,
        Vendor,
        DataFormatInstrument,
        Method,
        Attachment,
    ]
    _entityByName = {t.__name__: t for t in _entities}
    _defaultConfigFile: str = "logs.json"
    _currentUser: Person
    _cacheDir: Optional[str] = None

    def __init__(
        self,
        url: Optional[str] = None,
        apiKey: Optional[str] = None,
        configFile: Optional[str] = None,
        options: Optional[LOGSOptions] = None,
        verify: bool = True,
    ):
        """Checks the connection to the server on creation

        :param url: URL to specific LOGS group (e.g. https://mylogs/mygroup or https://mylogs:80/mygroup/api/0.1)
        :param api_key: The API key that grants access to LOGS (you need to generate on in LOGS and copy it)
        :param verbose: If set you see some information about the server connection. Defaults to False.

        :raises: Exception: URL does not defined or is invalid.
        :raises: Exception: The URL does not define a group.
        :raises: Exception: Server cannot be reached.
        """
        self._options = Tools.checkAndConvert(
            options, LOGSOptions, "options", initOnNone=True
        )

        _url = url
        _apiKey = apiKey

        if not configFile and os.path.isfile(self._defaultConfigFile):
            configFile = self._defaultConfigFile

        if configFile:
            config = self._readConfig(configFile)
            if "url" in config:
                _url = config["url"]
            if "apiKey" in config:
                _apiKey = config["apiKey"]
            if "proxyTargetUrl" in config:
                self._options.proxyTargetUrl = config["proxyTargetUrl"]

        if url:
            _url = url

        if apiKey:
            _apiKey = apiKey

        if not _url:
            raise LOGSException("The url to the LOGS server must be provided.")

        if not _apiKey:
            raise LOGSException(
                "The API key to access the server %a must be provided" % _url
            )

        self.promptPrefix = "LOGSAPI>"

        self._connection = LOGSConnection(
            url=_url, apiKey=_apiKey, options=self._options, verify=verify
        )
        self._currentUser = self._fetchCurrentUser()

    def _fetchCurrentUser(self) -> Person:
        data, responseError = self._connection.getEndpoint(["session"])
        if responseError:
            raise LOGSException(responseError=responseError)

        if not isinstance(data, dict):
            raise LOGSException(
                "Unexpected response from session endpoint. Could not get current user."
            )

        person = None
        if "person" in data:
            personClass = self.getTypedEntityClass(None, Person)
            person = personClass(data["person"], connection=self._connection)

        if not person or not person.id:
            raise LOGSException(
                "Unexpected response from session endpoint. Could not get current user."
            )

        return person

    def _readConfig(self, path: str) -> dict:
        if not os.path.isfile(path):
            raise LOGSException("Could not find config file %a" % path)

        with open(path, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError as e:
                raise LOGSException(
                    "Could not read config from file %a: %s" % (path, str(e))
                )
        return config

    @classmethod
    def getHumanReadableSize(cls, size: float, suffix="B"):
        for unit in Constants.byteUnits:
            if abs(size) < 1024.0:
                return "%3.1f%s%s" % (size, unit, suffix)
            size /= 1024.0
        return "%.1f%s%s" % (size, "Yi", suffix)

    def getDatasetDir(self, dataset: Dataset):
        if self.cacheDir:
            if not os.path.isdir(self.cacheDir):
                raise LOGSException(
                    f"Specified cache directory '{self.cacheDir}' cannot be opened or is not a directory."
                )

            dataDir = os.path.join(self.cacheDir, dataset.cacheId)
            if dataDir and not os.path.exists(dataDir):
                os.mkdir(dataDir)
            return dataDir
        return None

    def _fetchEntity(self, entityType: Type[_T], id: Union[int, str]) -> _T:
        e = cast(Type[Entity], entityType)(id=id, connection=self._connection)
        if isinstance(e, Dataset):
            e.cacheDir = self.getDatasetDir(e)
        e.fetch()
        if isinstance(e, ITypedEntity):
            e = e._getTypedInstance()

        return cast(_T, e)

    def _restoreEntitiesByTypeName(self, typeDict: Dict[str, Any]):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)
            if not t:
                continue
            self._restoreEntities(cast(Any, t), entities)

    def _restoreEntities(
        self, entityType: Type[Entity], entities: List[Constants.ENTITIES]
    ):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Restoring of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if len(entities) < 1:
            return
        elif len(entities) == 1:
            if not entities[0].id:
                raise EntityNotFoundException(entities[0])

            data, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["restore", str(entities[0].id)],
                data=entities[0].toDict(),
            )
            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
                and len(data["results"]) > 0
            ):
                entities[0].override(data["results"][0])
        else:
            data, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_restore"],
                data=[e.id for e in entities],
            )
            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
            ):
                for i, d in enumerate(data["results"]):
                    entities[i].override(d)

        if responseError:
            raise EntityUpdatingException(entity=entities, responseError=responseError)

    def _updateEntitiesByTypeName(self, typeDict: Dict[str, Any]):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)
            if not t:
                continue
            self._updateEntities(cast(Any, t), entities)

    def _updateEntities(
        self, entityType: Type[Entity], entities: List[Constants.ENTITIES]
    ):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Updating of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if len(entities) < 1:
            return
        elif len(entities) == 1:
            if not entities[0].id:
                raise EntityNotFoundException(entities[0])

            data, responseError = self._connection.putEndpoint(
                entityType._endpoint + [str(entities[0].id)],
                data=entities[0]._toDictWithSlack(),
            )
            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
                and len(data["results"]) > 0
            ):
                entities[0].override(data["results"][0])
        else:
            data, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_edit"],
                data=[e._toDictWithSlack() for e in entities],
            )
            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
            ):
                for i, d in enumerate(data["results"]):
                    entities[i].override(d)

        if responseError:
            raise EntityUpdatingException(entity=entities, responseError=responseError)

    def _createDataset(self, dataset: Union[Dataset, Attachment]):
        data = DatasetCreator(connection=self._connection, dataset=dataset).create()
        # TODO: The following is not optimal. DatasetCreator should directly set the dataset properties (add dataset write model to multipart)
        if (
            "results" in data
            and isinstance(data["results"], list)
            and len(data["results"]) == 1
        ):
            dataset._connection = self._connection
            dataset.override(data["results"][0])

    def _createEntitiesByTypeName(self, typeDict: Dict[str, Entity]):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)

            if not t:
                continue

            self._createEntities(cast(Any, t), cast(Any, entities))

    def _addOriginToEntity(
        self, endpoint: List[str], entity: Optional[EntityOriginWriteModelWithId]
    ):
        return self._addOriginToEntities(endpoint, [entity])

    def _addOriginToEntities(
        self,
        endpoint: List[str],
        entities: List[Optional[EntityOriginWriteModelWithId]],
    ):
        entities = [e for e in entities if e]
        if len(entities) == 1:
            data, responseError = self._connection.postEndpoint(
                endpoint + ["origin"], data=[e.toDict() for e in entities if e]
            )
            if responseError:
                indent = Constants.exceptionIndentation
                message = ""
                if isinstance(data, list):
                    message = "%sCould not add origin to %s %a" % (
                        (
                            "\n" + indent
                            if responseError and len(responseError.errorStringList) > 1
                            else ""
                        ),
                        Tools.plural("entity", entities),
                        Tools.eclipsesJoin(", ", [e.id for e in entities if e]),
                    )

                # indent *= 2
                if responseError:
                    message += ": " + responseError.errorString(indent)

                raise LOGSException(message=message, responseError=responseError)

        # for o in entities:
        #     print(">>>>>", o.toDict())
        # data, errors = self._connection.postEndpoint(
        #     entityType._endpoint + ["bulk_create"],
        #     data=[e.toDict() for e in entities],
        # )

    def _createEntityOriginWriteModel(
        self, entity: Union[Entity, IUniqueEntity]
    ) -> Optional[EntityOriginWriteModelWithId]:
        if isinstance(entity, IUniqueEntity) and (
            entity._foreignUid or entity._foreignOrigin
        ):
            if isinstance(entity, Entity):
                model = EntityOriginWriteModelWithId(
                    id=entity.id, uid=entity._foreignUid, origin=entity._foreignOrigin
                )
                if model.uid:
                    setattr(entity, "uid", model.uid)
                if model.uid:
                    setattr(entity, "origin", model.origin)
                return model

        return None

    def _createEntities(self, entityType: Type[Entity], entities: List[Entity]):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Creating of entity type %a is not implemented."
                % (
                    entityType.__name__
                    if entityType.__name__ != Entity.__name__
                    else "unknown"
                )
            )

        datasets = [e for e in entities if isinstance(e, Dataset)]
        attachments = [e for e in entities if isinstance(e, Attachment)]
        entities = [e for e in entities if not isinstance(e, (Dataset, Attachment))]

        if len(datasets) > 0:
            for dataset in datasets:
                self._createDataset(dataset)
                self._addOriginToEntity(
                    entityType._endpoint, self._createEntityOriginWriteModel(dataset)
                )

        if len(attachments) > 0:
            for attachment in attachments:
                self._createDataset(attachment)
                self._addOriginToEntity(
                    entityType._endpoint, self._createEntityOriginWriteModel(attachment)
                )

        responseError = None
        if len(entities) == 1:
            data, responseError = self._connection.postEndpoint(
                entityType._endpoint, data=entities[0].toDict()
            )
            if responseError:
                raise EntityCreatingException(
                    entity=entities, responseError=responseError
                )

            entities[0]._connection = self._connection
            entities[0].override(data)
            self._addOriginToEntity(
                entityType._endpoint, self._createEntityOriginWriteModel(entities[0])
            )

        elif len(entities) > 1:
            data, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_create"],
                data=[e.toDict() for e in entities],
            )
            if responseError:
                raise EntityCreatingException(
                    entity=entities, responseError=responseError
                )

            if (
                isinstance(data, dict)
                and "results" in data
                and isinstance(data["results"], list)
            ):
                for i, d in enumerate(data["results"]):
                    entities[i]._connection = self._connection
                    entities[i].override(d)
                self._addOriginToEntities(
                    entityType._endpoint,
                    [self._createEntityOriginWriteModel(e) for e in entities],
                )

    def _deleteEntitiesByTypeName(
        self,
        typeDict: Dict[str, List[Union[Constants.ID_TYPE, None]]],
        permanently: bool = False,
    ):
        for typeName, entities in typeDict.items():
            if not entities:
                continue
            t = self._entityByName.get(typeName, None)
            if not t:
                continue
            self._deleteEntities(cast(Any, t), [e for e in entities if e], permanently)

    def _deleteEntities(
        self,
        entityType: Type[Entity],
        entityIds: List[Constants.ID_TYPE],
        permanently: bool = False,
    ):
        if not entityType._endpoint:
            raise NotImplementedError(
                "Deleting of entity type %a is not implemented."
                % (
                    type(self).__name__
                    if type(self).__name__ != Entity.__name__
                    else "unknown"
                )
            )

        if len(entityIds) < 1:
            return
        elif len(entityIds) == 1:
            _, responseError = self._connection.deleteEndpoint(
                entityType._endpoint + [str(entityIds[0])],
                parameters={"deletePermanently": permanently} if permanently else {},
            )
        else:
            _, responseError = self._connection.postEndpoint(
                entityType._endpoint + ["bulk_delete"],
                data=[id for id in entityIds],
                parameters={"deletePermanently": permanently} if permanently else {},
            )

        if responseError:
            raise EntityDeletingException(
                entityIds=entityIds, responseError=responseError
            )

    @classmethod
    def _collectTypes(cls, entities: Sequence) -> Dict[str, Any]:
        result: Dict[str, Any] = {k: [] for k in cls._entityByName.keys()}
        result["unknown"] = []

        for entity in entities:
            unknown = True

            for k, v in cls._entityByName.items():
                if isinstance(entity, v):
                    result[k].append(entity)
                    unknown = False
                    break

            if unknown:
                result["unknown"].append(entity)
        return result

    def printServerStatus(self):
        self._connection.printServerStatus()

    @overload
    def restore(self, entities: Constants.ENTITIES): ...

    @overload
    def restore(self, entities: List[Constants.ENTITIES]): ...

    # Implementation of overload
    def restore(self, entities: Any):
        def decorator(entities: Any):
            types = self._collectTypes(entities)
            if len(types["unknown"]) > 0:
                raise EntityUpdatingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action."
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._restoreEntitiesByTypeName(types)

        if not isinstance(entities, list):
            entities = [entities]
        return decorator(entities)

    @overload
    def update(self, entities: Constants.ENTITIES): ...

    @overload
    def update(self, entities: List[Constants.ENTITIES]): ...

    # Implementation of overload
    def update(self, entities: Any):
        def decorator(entities: Any):
            types = self._collectTypes(entities)
            if len(types["unknown"]) > 0:
                raise EntityUpdatingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action."
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._updateEntitiesByTypeName(types)

        if not isinstance(entities, list):
            entities = [entities]
        return decorator(entities)

    @overload
    def create(self, entities: Constants.ENTITIES): ...

    @overload
    def create(self, entities: Sequence[Constants.ENTITIES]): ...

    # Implementation of overload
    def create(self, entities: Any):
        def decorator(entities: Sequence[Entity]):
            types = self._collectTypes(entities)
            if len(types["unknown"]) > 0:
                raise EntityCreatingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action"
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._createEntitiesByTypeName(types)

        if not isinstance(entities, list):
            entities = [entities]
        decorator(entities)

    @overload
    def delete(self, entities: Constants.ENTITIES, permanently=False): ...

    @overload
    def delete(self, entities: Sequence[Constants.ENTITIES], permanently=False): ...

    # Implementation of overload
    def delete(self, entities: Any = None, permanently=False):
        def decorator(entities: Any):
            types: Dict[str, List[Union[Constants.ID_TYPE, None]]] = self._collectTypes(
                entities
            )
            typesIds = {
                typeName: cast(List, [cast(Entity, e).id for e in entities if e])
                for typeName, entities in types.items()
            }
            if len(types["unknown"]) > 0:
                raise EntityDeletingException(
                    types["unknown"][0],
                    errors=[
                        "Entity type %a not valid for this action"
                        % type(types["unknown"][0]).__name__
                    ],
                )

            self._deleteEntitiesByTypeName(typesIds, permanently=permanently)

            for entityList in types.values():
                for entity in entityList:
                    if permanently and isinstance(entity, ConnectedEntity):
                        entity._connection = None
                    if isinstance(entity, ISoftDeletable):
                        entity.isDeleted = True

        if isinstance(entities, EntityIterator):
            raise LOGSException(
                "An %a cannot be used for delete. Please convert it to a list first."
                % EntityIterator.__name__
            )
        elif not isinstance(entities, list):
            entities = [entities]
        return decorator(entities)

    @overload
    def deleteById(
        self, entityType: Type[Constants.ENTITIES], ids: int, permanently: bool = False
    ): ...

    @overload
    def deleteById(
        self, entityType: Type[Constants.ENTITIES], ids: str, permanently: bool = False
    ): ...

    @overload
    def deleteById(
        self,
        entityType: Type[Constants.ENTITIES],
        ids: Constants.ID_TYPE,
        permanently: bool = False,
    ): ...

    @overload
    def deleteById(
        self,
        entityType: Type[Constants.ENTITIES],
        ids: List[int],
        permanently: bool = False,
    ): ...

    @overload
    def deleteById(
        self,
        entityType: Type[Constants.ENTITIES],
        ids: List[str],
        permanently: bool = False,
    ): ...

    @overload
    def deleteById(
        self,
        entityType: Type[Constants.ENTITIES],
        ids: List[Constants.ID_TYPE],
        permanently: bool = False,
    ): ...

    # Implementation of overload
    def deleteById(self, entityType=None, ids: Any = None, permanently: bool = False):
        if not entityType:
            raise Exception("Parameter 'entityType' must be provided.")

        if not issubclass(entityType, Entity):
            raise Exception(
                f"Parameter 'entityType' must be a subclass of {Entity.__name__}."
            )

        def decorator(entityType: Any):
            self._deleteEntities(entityType, ids, permanently=permanently)

        if ids and not isinstance(ids, list):
            ids = [ids]
        return decorator(entityType)

    def getTypedEntityClass(
        self, customTypeOrId: Optional[Union[CustomType, int]], entityType: Type[_T]
    ) -> Type[_T]:
        if not issubclass(entityType, Entity):
            raise Exception(
                f"Type '{entityType.__name__}' is not an LOGS entity. (Got '{type(entityType).__name__}')"
            )

        if customTypeOrId is None:
            return CustomEntityClassGenerator.generate(
                None,
                connection=self._connection,
                limitToEntityType=entityType,
            )
        elif not issubclass(entityType, ITypedEntity):
            raise Exception(
                f"Entity type '{entityType.__name__}' is not a typed entity and cannot be used with custom types."
            )

        if isinstance(customTypeOrId, int):
            customType = CustomEntityClassGenerator.fetchCustomType(
                customTypeOrId, self._connection
            )
        elif isinstance(customTypeOrId, CustomType):
            customType = customTypeOrId
        else:
            raise Exception(
                f"Parameter 'customTypeOrId' must be of type {CustomType.__name__} or int. (Got '{type(customTypeOrId).__name__}')"
            )

        return CustomEntityClassGenerator.generate(
            customType=customType,
            connection=self._connection,
            limitToEntityType=entityType,
        )

    def newSample(
        self,
        entityOrCustomTypeOrId: Optional[Union[CustomType, int]] = None,
        ref=None,
        name: str = "",
        projects: Optional[List[Union["ProjectMinimal", "Project"]]] = None,
    ) -> Sample:
        return self.getTypedEntityClass(entityOrCustomTypeOrId, Sample)(
            ref=ref, connection=self._connection, name=name, projects=projects
        )

    def sample(self, id: int) -> Sample:
        return self._fetchEntity(Sample, id)

    def samples(self, parameter: Optional[SampleRequestParameter] = None) -> Samples:
        if parameter and not isinstance(parameter, SampleRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.samples.__name__,
                    SampleRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Samples(connection=self._connection, parameters=parameter)

    def newProject(
        self,
        entityOrCustomTypeOrId: Optional[Union[CustomType, int]] = None,
        ref=None,
        name: str = "",
    ) -> Project:
        return self.getTypedEntityClass(entityOrCustomTypeOrId, Project)(
            ref=ref, connection=self._connection, name=name
        )

    def project(self, id: int) -> Project:
        return self._fetchEntity(Project, id)

    def projects(self, parameter: Optional[ProjectRequestParameter] = None) -> Projects:
        if parameter and not isinstance(parameter, ProjectRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.projects.__name__,
                    ProjectRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Projects(connection=self._connection, parameters=parameter)

    def newDataset(
        self,
        entityOrCustomTypeOrId: Optional[Union[CustomType, int]] = None,
        ref=None,
        files: Optional[Sequence[Constants.FILE_TYPE]] = None,
        formatOrFormatId: Optional[Union[str, "DataFormatMinimal"]] = None,
        pathPrefixToStrip: Optional[str] = None,
        pathPrefixToAdd: Optional[str] = None,
    ) -> Dataset:
        return self.getTypedEntityClass(entityOrCustomTypeOrId, Dataset)(
            ref=ref,
            connection=self._connection,
            files=files,
            formatOrFormatId=formatOrFormatId,
            pathPrefixToStrip=pathPrefixToStrip,
            pathPrefixToAdd=pathPrefixToAdd,
        )

    def dataset(self, id: int) -> Dataset:
        return self._fetchEntity(Dataset, id)

    def datasets(self, parameter: Optional[DatasetRequestParameter] = None) -> Datasets:
        if parameter and not isinstance(parameter, DatasetRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.datasets.__name__,
                    DatasetRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Datasets(connection=self._connection, parameters=parameter)

    def newAttachment(
        self,
        ref=None,
        files: Optional[Sequence[Constants.FILE_TYPE]] = None,
        pathPrefixToStrip: Optional[str] = None,
        pathPrefixToAdd: Optional[str] = None,
    ) -> Attachment:
        return self.getTypedEntityClass(None, Attachment)(
            ref=ref,
            connection=self._connection,
            files=files,
            pathPrefixToStrip=pathPrefixToStrip,
            pathPrefixToAdd=pathPrefixToAdd,
        )

    def attachment(self, id: int) -> Attachment:
        return self._fetchEntity(Attachment, id)

    def attachments(
        self, parameter: Optional[AttachmentRequestParameter] = None
    ) -> Attachments:
        if parameter and not isinstance(parameter, AttachmentRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.attachments.__name__,
                    AttachmentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Attachments(connection=self._connection, parameters=parameter)

    def newPerson(
        self, entityOrCustomTypeOrId: Optional[Union[CustomType, int]] = None, ref=None
    ) -> Person:
        return self.getTypedEntityClass(entityOrCustomTypeOrId, Person)(
            ref=ref, connection=self._connection
        )

    def person(self, id: int) -> Person:
        return self._fetchEntity(Person, id)

    def persons(self, parameter: Optional[PersonRequestParameter] = None) -> Persons:
        if parameter and not isinstance(parameter, PersonRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.persons.__name__,
                    PersonRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Persons(connection=self._connection, parameters=parameter)

    def newOrigin(
        self,
        ref=None,
        name: Optional[str] = None,
        url: Optional[str] = None,
        uid: Optional[UUID] = None,
    ) -> Origin:
        return self.getTypedEntityClass(None, Origin)(
            ref=ref, connection=self._connection, name=name, url=url, uid=uid
        )

    def origin(self, id: int) -> Origin:
        return self._fetchEntity(Origin, id)

    def origins(self, parameter: Optional[OriginRequestParameter] = None) -> Origins:
        if parameter and not isinstance(parameter, OriginRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.origins.__name__,
                    OriginRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Origins(connection=self._connection, parameters=parameter)

    def newDataFormat(self, ref=None) -> DataFormat:
        return self.getTypedEntityClass(None, DataFormat)(
            ref=ref, connection=self._connection
        )

    def dataFormat(self, id: str) -> DataFormat:
        return self._fetchEntity(DataFormat, id)

    def dataFormats(
        self, parameter: Optional[DataFormatRequestParameter] = None
    ) -> DataFormats:
        if parameter and not isinstance(parameter, DataFormatRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.dataFormats.__name__,
                    DataFormatRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return DataFormats(connection=self._connection, parameters=parameter)

    def newRole(self, ref=None) -> Role:
        return self.getTypedEntityClass(None, Role)(
            ref=ref, connection=self._connection
        )

    def role(self, id: int) -> Role:
        return self._fetchEntity(Role, id)

    def roles(self, parameter: Optional[RoleRequestParameter] = None) -> Roles:
        if parameter and not isinstance(parameter, RoleRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.roles.__name__,
                    RoleRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Roles(connection=self._connection, parameters=parameter)

    def newBridge(self, ref=None) -> Bridge:
        return self.getTypedEntityClass(None, Bridge)(
            ref=ref, connection=self._connection
        )

    def bridge(self, id: int) -> Bridge:
        return self._fetchEntity(Bridge, id)

    def bridges(self, parameter: Optional[BridgeRequestParameter] = None) -> Bridges:
        if parameter and not isinstance(parameter, BridgeRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.bridges.__name__,
                    BridgeRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Bridges(connection=self._connection, parameters=parameter)

    def newDataSource(self, ref=None) -> DataSource:
        return self.getTypedEntityClass(None, DataSource)(
            ref=ref, connection=self._connection
        )

    def dataSource(self, id: int) -> DataSource:
        return self._fetchEntity(DataSource, id)

    def dataSources(
        self, parameter: Optional[DataSourceRequestParameter] = None
    ) -> DataSources:
        if parameter and not isinstance(parameter, DataSourceRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.dataSources.__name__,
                    DataSourceRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return DataSources(connection=self._connection, parameters=parameter)

    def newLabNotebook(self, ref=None) -> LabNotebook:
        return self.getTypedEntityClass(None, LabNotebook)(
            ref=ref, connection=self._connection
        )

    def labNotebook(self, id: int) -> LabNotebook:
        return self._fetchEntity(LabNotebook, id)

    def labNotebooks(
        self, parameter: Optional[LabNotebookRequestParameter] = None
    ) -> LabNotebooks:
        if parameter and not isinstance(parameter, LabNotebookRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.labNotebooks.__name__,
                    LabNotebookRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return LabNotebooks(connection=self._connection, parameters=parameter)

    def newLabNotebookTemplate(self, ref=None) -> LabNotebookTemplate:
        return self.getTypedEntityClass(None, LabNotebookTemplate)(
            ref=ref, connection=self._connection
        )

    def labNotebookTemplate(self, id: int) -> LabNotebookTemplate:
        return self._fetchEntity(LabNotebookTemplate, id)

    def labNotebookTemplates(
        self, parameter: Optional[LabNotebookTemplateRequestParameter] = None
    ) -> LabNotebookTemplates:
        if parameter and not isinstance(parameter, LabNotebookTemplateRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.labNotebookTemplates.__name__,
                    LabNotebookTemplateRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return LabNotebookTemplates(connection=self._connection, parameters=parameter)

    def newLabNotebookExperiment(self, ref=None) -> LabNotebookExperiment:
        return self.getTypedEntityClass(None, LabNotebookExperiment)(
            ref=ref, connection=self._connection
        )

    def labNotebookExperiment(self, id: int) -> LabNotebookExperiment:
        return self._fetchEntity(LabNotebookExperiment, id)

    def labNotebookExperiments(
        self, parameter: Optional[LabNotebookExperimentRequestParameter] = None
    ) -> LabNotebookExperiments:
        if parameter and not isinstance(
            parameter, LabNotebookExperimentRequestParameter
        ):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.labNotebookExperiments.__name__,
                    LabNotebookExperimentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return LabNotebookExperiments(connection=self._connection, parameters=parameter)

    def newLabNotebookEntry(self, ref=None) -> LabNotebookEntry:
        return self.getTypedEntityClass(None, LabNotebookEntry)(
            ref=ref, connection=self._connection
        )

    def labNotebookEntry(self, id: int) -> LabNotebookEntry:
        return self._fetchEntity(LabNotebookEntry, id)

    def labNotebookEntries(
        self, parameter: Optional[LabNotebookEntryRequestParameter] = None
    ) -> LabNotebookEntries:
        if parameter and not isinstance(parameter, LabNotebookEntryRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.labNotebookEntries.__name__,
                    LabNotebookEntryRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return LabNotebookEntries(connection=self._connection, parameters=parameter)

    def newVendor(self, ref=None) -> Vendor:
        return self.getTypedEntityClass(None, Vendor)(
            ref=ref, connection=self._connection
        )

    def vendor(self, id: int) -> Vendor:
        return self._fetchEntity(Vendor, id)

    def vendors(self, parameter: Optional[VendorRequestParameter] = None) -> Vendors:
        if parameter and not isinstance(parameter, VendorRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.vendors.__name__,
                    VendorRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Vendors(connection=self._connection, parameters=parameter)

    def newMethod(self, ref=None) -> Method:
        return self.getTypedEntityClass(None, Method)(
            ref=ref, connection=self._connection
        )

    def method(self, id: int) -> Method:
        return self._fetchEntity(Method, id)

    def methods(self, parameter: Optional[MethodRequestParameter] = None) -> Methods:
        if parameter and not isinstance(parameter, MethodRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.methods.__name__,
                    MethodRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Methods(connection=self._connection, parameters=parameter)

    def newDataFormatInstrument(self, ref=None) -> DataFormatInstrument:
        return self.getTypedEntityClass(None, DataFormatInstrument)(
            ref=ref, connection=self._connection
        )

    def dataFormatInstrument(self, id: int) -> DataFormatInstrument:
        return self._fetchEntity(DataFormatInstrument, id)

    def dataFormatInstruments(
        self, parameter: Optional[DataFormatInstrumentRequestParameter] = None
    ) -> DataFormatInstruments:
        if parameter and not isinstance(
            parameter, DataFormatInstrumentRequestParameter
        ):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.dataFormatInstruments.__name__,
                    DataFormatInstrumentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return DataFormatInstruments(connection=self._connection, parameters=parameter)

    def newCustomField(self, ref=None) -> CustomField:
        return self.getTypedEntityClass(None, CustomField)(
            ref=ref, connection=self._connection
        )

    def customField(self, id: int) -> CustomField:
        return self._fetchEntity(CustomField, id)

    def customFields(
        self, parameter: Optional[CustomFieldRequestParameter] = None
    ) -> CustomFields:
        if parameter and not isinstance(parameter, CustomFieldRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.customFields.__name__,
                    CustomFieldRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return CustomFields(connection=self._connection, parameters=parameter)

    def newCustomType(self, ref=None) -> CustomType:
        return self.getTypedEntityClass(None, CustomType)(
            ref=ref, connection=self._connection
        )

    def customType(self, id: int) -> CustomType:
        return self._fetchEntity(CustomType, id)

    def customTypes(
        self, parameter: Optional[CustomTypeRequestParameter] = None
    ) -> CustomTypes:
        if parameter and not isinstance(parameter, CustomTypeRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.customTypes.__name__,
                    CustomTypeRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return CustomTypes(connection=self._connection, parameters=parameter)

    def newInventoryItem(
        self, customTypeOrId: Optional[Union[CustomType, int]] = None, ref=None
    ) -> InventoryItem:
        return self.getTypedEntityClass(customTypeOrId, InventoryItem)(
            ref=ref, connection=self._connection
        )

    def inventoryItem(self, id: int) -> InventoryItem:
        return self._fetchEntity(InventoryItem, id)

    def inventoryItems(
        self, parameter: Optional[InventoryItemRequestParameter] = None
    ) -> InventoryItems:
        if parameter and not isinstance(parameter, InventoryItemRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.inventoryItems.__name__,
                    InventoryItemRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return InventoryItems(connection=self._connection, parameters=parameter)

    def newSharedContent(self, ref=None) -> SharedContent:
        return self.getTypedEntityClass(None, SharedContent)(
            ref=ref, connection=self._connection
        )

    def sharedContent(self, id: int) -> SharedContent:
        return self._fetchEntity(SharedContent, id)

    def sharedContents(
        self, parameter: Optional[SharedContentRequestParameter] = None
    ) -> SharedContents:
        if parameter and not isinstance(parameter, SharedContentRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.sharedContents.__name__,
                    SharedContentRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return SharedContents(connection=self._connection, parameters=parameter)

    def entity(self, uid: str):
        return Entities(connection=self._connection).fetch(uid=uid)

    def entities(
        self, parameter: Optional[EntitiesRequestParameter] = None
    ) -> Entities:
        if parameter and not isinstance(parameter, EntitiesRequestParameter):
            raise LOGSException(
                "Parameter for %s.%s must be of type %a. (Got %a)"
                % (
                    type(self).__name__,
                    self.entities.__name__,
                    EntitiesRequestParameter.__name__,
                    type(parameter).__name__,
                )
            )
        return Entities(connection=self._connection, parameters=parameter)

    def datasetMatching(
        self,
        files: Union[Constants.FILE_TYPE, Sequence[Constants.FILE_TYPE]],
        formatIds: Optional[List[str]] = None,
        ignoreReadErrors=False,
    ) -> DatasetMatching:
        return DatasetMatching(
            connection=self._connection,
            files=files,
            formatIds=formatIds,
            ignoreReadErrors=ignoreReadErrors,
        )

    def updatableDatasetFiles(
        self, files: Sequence[Constants.FILE_TYPE], formatIds: List[str]
    ):
        datasets = Datasets(
            connection=self._connection, parameters=cast(DatasetRequestParameter, {})
        ).findDatasetByFiles(files=files, formatIds=formatIds)
        for dataset in datasets:
            yield DatasetsUpdatableFiles(
                datasetId=dataset.logsId,
                files=[
                    FileEntry(fullPath=file.fullPath, state=file.state)
                    for file in dataset.files
                ],
            )

    @property
    def instanceOrigin(self) -> Origin:
        return Origin(name="LOGS (%s)" % self.group, url=self.url, uid=self.uid)

    @property
    def url(self) -> str:
        return self._connection.url

    @property
    def apiUrl(self) -> str:
        return self._connection.apiUrl

    @property
    def uid(self) -> Optional[UUID]:
        return self._connection.metadata.uid

    @property
    def group(self) -> Optional[str]:
        return self._connection._group

    @property
    def currentUser(self) -> Person:
        return self._currentUser

    @property
    def cacheDir(self) -> Optional[str]:
        return self._cacheDir

    @cacheDir.setter
    def cacheDir(self, value):
        self._cacheDir = Tools.checkAndConvert(value, str, "cacheDir")

    def version(self) -> Optional[str]:
        return self._connection.metadata.version

    @property
    def metadata(self) -> ServerMetaData:
        return self._connection.metadata


if __name__ == "__main__":
    api_key = input("Please specify api key: ")
    _url = input("Please specify LOGS url: ")

    # Example input:
    # api_key = "8V6oQ804t2nPgGPDJIk4CuneRI5q48ERUxgEpk+YqXzX9uLuMUySycHkeXP6DefN"
    # url = "http://localhost:900/sandbox"

    logs = LOGS(
        _url, api_key, options=LOGSOptions(showRequestUrl=True, showRequestBody=False)
    )
