from LOGS.Auxiliary.Decorators import FullModel
from LOGS.Entities.Attachment import Attachment
from LOGS.Entity.EntityMinimalWithIntId import EntityMinimalWithIntId


@FullModel(Attachment)
class AttachmentMinimal(EntityMinimalWithIntId[Attachment]):
    pass
