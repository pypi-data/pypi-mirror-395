from typing import Optional

from LOGS.Entity.SerializableContent import SerializableContent


class HierarchyLeaf(SerializableContent):
    _track: Optional[str] = None

    @property
    def track(self) -> Optional[str]:
        return self._track

    @track.setter
    def track(self, value):
        self._track = self.checkAndConvertNullable(value, str, "track")
