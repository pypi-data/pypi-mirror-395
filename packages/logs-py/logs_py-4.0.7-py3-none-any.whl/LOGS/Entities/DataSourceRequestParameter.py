from dataclasses import dataclass, field
from typing import List, Optional, Type, cast

from typing_extensions import Self

from LOGS.Entities.BridgeType import BridgeType
from LOGS.Entities.DataSource import DataSourceType
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Entity.IGenericEntityOrderBy import (
    IEntryRecordSortingOptions,
    IGenericEntitySortingOptions,
    IModificationRecordSortingOptions,
    INamedEntitySortingOptions,
)
from LOGS.Interfaces.IEntryRecord import IEntryRecordRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.IUniqueEntity import IUniqueEntityRequest


class DataSourceSortingOptions(
    IGenericEntitySortingOptions,
    INamedEntitySortingOptions,
    IEntryRecordSortingOptions,
    IModificationRecordSortingOptions,
):
    TYPE: Self = cast(Self, "TYPE")
    BRIDGE: Self = cast(Self, "BRIDGE")
    BRIDGE_TYPE: Self = cast(Self, "BRIDGE_TYPE")
    INTERVAL: Self = cast(Self, "INTERVAL")
    ENABLED: Self = cast(Self, "ENABLED")


@dataclass
class DataSourceRequestParameter(
    EntityRequestParameter[DataSourceSortingOptions],
    INamedEntityRequest,
    IUniqueEntityRequest,
    IEntryRecordRequest,
    IModificationRecordRequest,
    IPermissionedEntityRequest,
):
    _orderByType: Type[DataSourceSortingOptions] = field(
        default=DataSourceSortingOptions, init=False
    )

    enabled: Optional[bool] = None
    bridgeIds: Optional[List[int]] = None
    bridgeTypes: Optional[List[BridgeType]] = None
    datasetIds: Optional[List[int]] = None
    formatIds: Optional[List[str]] = None
    customImportIds: Optional[List[str]] = None
    directories: Optional[List[str]] = None
    sourceHostnames: Optional[List[str]] = None
    sourceIpAddresses: Optional[List[str]] = None
    types: Optional[List[DataSourceType]] = None
