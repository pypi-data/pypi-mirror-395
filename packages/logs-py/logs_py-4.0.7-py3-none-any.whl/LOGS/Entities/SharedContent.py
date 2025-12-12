from typing import TYPE_CHECKING, List, Optional

from deprecation import deprecated  # type: ignore

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.MinimalModelGenerator import MinimalModelGenerator
from LOGS.Entity.EntityWithIntId import IEntityWithIntId
from LOGS.Interfaces.IEntryRecord import IEntryRecord
from LOGS.Interfaces.IModificationRecord import IModificationRecord
from LOGS.Interfaces.INamedEntity import INamedEntity
from LOGS.Interfaces.IOwnedEntity import IOwnedEntity
from LOGS.Interfaces.IPermissionedEntity import IGenericPermissionEntity
from LOGS.Interfaces.IUniqueEntity import IUniqueEntity

if TYPE_CHECKING:
    from LOGS.Entities.DatasetMinimal import DatasetMinimal


@Endpoint("shared_content")
class SharedContent(
    IEntityWithIntId,
    IGenericPermissionEntity,
    IUniqueEntity,
    INamedEntity,
    IOwnedEntity,
    IEntryRecord,
    IModificationRecord,
):

    _shareId: Optional[str] = None
    _allowContentDownload: Optional[bool] = None
    _publicNotes: Optional[str] = None
    _privateNotes: Optional[str] = None
    _password: Optional[str] = None
    _datasets: Optional[List["DatasetMinimal"]] = None

    @property
    def shareId(self) -> Optional[str]:
        return self._shareId

    @shareId.setter
    def shareId(self, value):
        self._shareId = self.checkAndConvertNullable(value, str, "shareId")

    @property
    def allowContentDownload(self) -> Optional[bool]:
        return self._allowContentDownload

    @allowContentDownload.setter
    def allowContentDownload(self, value):
        self._allowContentDownload = self.checkAndConvertNullable(
            value, bool, "allowContentDownload"
        )

    @property
    def publicNotes(self) -> Optional[str]:
        return self._publicNotes

    @publicNotes.setter
    def publicNotes(self, value):
        self._publicNotes = self.checkAndConvertNullable(value, str, "publicNotes")

    @property
    def privateNotes(self) -> Optional[str]:
        return self._privateNotes

    @privateNotes.setter
    def privateNotes(self, value):
        self._privateNotes = self.checkAndConvertNullable(value, str, "privateNotes")

    @property
    def password(self) -> Optional[str]:
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.checkAndConvertNullable(value, str, "password")

    @property
    def datasets(self) -> Optional[List["DatasetMinimal"]]:
        return self._datasets

    @datasets.setter
    def datasets(self, value):
        self._datasets = MinimalModelGenerator.MinimalFromList(
            value, "DatasetMinimal", "datasets", connection=self._getConnection()
        )
