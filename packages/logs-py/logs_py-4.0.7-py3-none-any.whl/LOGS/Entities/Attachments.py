import dataclasses
from typing import List, Optional

from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Entities.Attachment import Attachment
from LOGS.Entities.AttachmentRequestParameter import AttachmentRequestParameter
from LOGS.Entities.DatasetModels import ViewableEntityTypes
from LOGS.Entity.EntityIterator import EntityIterator
from LOGS.LOGSConnection import LOGSConnection


class _AttachmentRequestParameter(AttachmentRequestParameter):
    isViewableEntity: bool = True
    viewableEntityTypes: List[ViewableEntityTypes] = [ViewableEntityTypes.CustomField]

    def __init__(self, ref: Optional[AttachmentRequestParameter] = None):
        if ref is None:
            super().__init__()
            return
        fieldValues = {f.name: getattr(ref, f.name) for f in dataclasses.fields(ref)}
        super().__init__(**fieldValues)


@Endpoint("datasets")
class Attachments(EntityIterator[Attachment, AttachmentRequestParameter]):
    """LOGS connected class Attachments iterator"""

    _generatorType = Attachment
    _parameterType = AttachmentRequestParameter

    def __init__(
        self,
        connection: Optional[LOGSConnection],
        parameters: Optional[AttachmentRequestParameter] = None,
    ):
        self._parameterType = _AttachmentRequestParameter
        parameters = (
            _AttachmentRequestParameter(parameters)
            if parameters
            else _AttachmentRequestParameter()
        )

        super().__init__(connection=connection, parameters=parameters)

    def __next__(self):
        attachment = super().__next__()

        if self._parameters.includeInfo:
            attachment.fetchInfo()
        if self._parameters.includeZipSize:
            attachment.fetchZipSize()

        return attachment
