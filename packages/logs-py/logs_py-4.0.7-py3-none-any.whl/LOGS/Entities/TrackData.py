from LOGS.Entity.SerializableContent import SerializableContent


class TrackData(SerializableContent):
    def fetchFull(self):
        raise NotImplementedError(
            "Specific %a class for this track type is not implemented yet."
            % type(self).__name__
        )

    def toData(self):
        from LOGS.Entities.Datatrack import Datatrack

        d = {}
        for key in self.__dict__:
            if key.startswith("_"):
                a = getattr(self, key)
                if isinstance(a, Datatrack):
                    d[key[1:]] = a.id
        return d
