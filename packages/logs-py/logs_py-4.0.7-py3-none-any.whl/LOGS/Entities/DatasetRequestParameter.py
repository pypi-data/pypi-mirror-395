from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Type, cast

from typing_extensions import Self

from LOGS.Auxiliary.Constants import Constants
from LOGS.Entity.EntityRequestParameter import EntityRequestParameter
from LOGS.Entity.IGenericEntityOrderBy import (
    IEntryRecordSortingOptions,
    IGenericEntitySortingOptions,
    IModificationRecordSortingOptions,
    INamedEntitySortingOptions,
    ITypedEntitySortingOptions,
)
from LOGS.Interfaces.IEntryRecord import IEntryRecordRequest
from LOGS.Interfaces.ILockableEntity import ILockableEntityRequest
from LOGS.Interfaces.IModificationRecord import IModificationRecordRequest
from LOGS.Interfaces.INamedEntity import INamedEntityRequest
from LOGS.Interfaces.IOwnedEntity import IOwnedEntityRequest
from LOGS.Interfaces.IPermissionedEntity import IPermissionedEntityRequest
from LOGS.Interfaces.IProjectBased import IProjectBasedRequest
from LOGS.Interfaces.ISignableEntity import ISignableEntityRequest
from LOGS.Interfaces.ISoftDeletable import ISoftDeletableRequest
from LOGS.Interfaces.ITypedEntity import ITypedEntityRequest
from LOGS.Interfaces.IUniqueEntity import IUniqueEntityRequest


class ParsingStates(Enum):
    ParsedSuccessfully = "ParsedSuccessfully"
    NotParsable = "NotParsable"
    ParsingFailed = "ParsingFailed"
    NotYetParsed = "NotYetParsed"


class DatasetSortingOptions(
    IGenericEntitySortingOptions,
    INamedEntitySortingOptions,
    IEntryRecordSortingOptions,
    IModificationRecordSortingOptions,
    ITypedEntitySortingOptions,
):
    CREATION_DATE: Self = cast(Self, "CREATION_DATE")
    PARSING_STATE: Self = cast(Self, "PARSING_STATE")
    FORMAT_ID: Self = cast(Self, "FORMAT_ID")
    OWNER: Self = cast(Self, "OWNER")


@dataclass
class DatasetRequestParameter(
    EntityRequestParameter[DatasetSortingOptions],
    IPermissionedEntityRequest,
    IUniqueEntityRequest,
    INamedEntityRequest,
    IOwnedEntityRequest,
    IProjectBasedRequest,
    IEntryRecordRequest,
    IModificationRecordRequest,
    ISoftDeletableRequest,
    ILockableEntityRequest,
    ISignableEntityRequest,
    ITypedEntityRequest,
):
    _orderByType: Type[DatasetSortingOptions] = field(
        default=DatasetSortingOptions, init=False
    )
    includeSource: Optional[bool] = None
    hasCustomImport: Optional[bool] = None
    creationDateFrom: Optional[datetime] = None
    creationDateTo: Optional[datetime] = None
    autoloadServerIds: Optional[List[int]] = None
    bridgeIds: Optional[List[int]] = None
    dataSourceIds: Optional[List[int]] = None
    excludeUndeleted: Optional[bool] = None
    files: Optional[Sequence[Constants.FILE_TYPE]] = None
    formatIds: Optional[List[str]] = None
    hashes: Optional[List[str]] = None
    includeUnclaimed: Optional[Optional[bool]] = None
    isClaimed: Optional[Optional[bool]] = None
    isReferencedByLabNotebook: Optional[Optional[bool]] = None
    parameters: Optional[Dict[str, Any]] = None
    parsingState: Optional[List[ParsingStates]] = None
    pathContains: Optional[str] = None
    searchTermIncludeParameters: Optional[bool] = None
    searchTermIncludePaths: Optional[bool] = None

    # Additional fetch options
    includeParameters: Optional[bool] = None
    includeInfo: Optional[bool] = None
    includeZipSize: Optional[bool] = None
    includeExports: Optional[bool] = None
