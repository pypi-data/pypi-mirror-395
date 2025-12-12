from typing import Optional

from LOGS.Entity.SerializableContent import SerializableClass


class PersonCategory(SerializableClass):
    id: Optional[int] = None
    name: Optional[str] = None

    def __str__(self):
        s = (" name:'%s'" % self.name) if self.name else ""
        return "<%s id:%s%s>" % (type(self).__name__, str(self.id), s)
