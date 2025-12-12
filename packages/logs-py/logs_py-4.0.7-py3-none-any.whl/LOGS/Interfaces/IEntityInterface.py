class IEntityInterface:
    def _getEntityConnection(self):
        from LOGS.Entity.ConnectedEntity import ConnectedEntity

        if isinstance(self, ConnectedEntity):
            return self._getConnection()
        return None
