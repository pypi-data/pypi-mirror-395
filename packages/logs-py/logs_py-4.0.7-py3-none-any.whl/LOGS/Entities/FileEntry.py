import base64
import os
import uuid
from datetime import datetime
from hashlib import sha256
from typing import Any, List, Literal, Optional, Sequence, Union, cast

from LOGS.Auxiliary.Constants import Constants
from LOGS.Entity.SerializableContent import SerializableClass


class FingerprintFragment(SerializableClass):
    offset: int = 0
    length: int = 0
    bytes: str = ""


class FileFragment(SerializableClass):
    _typeMapper = {"fragments": FingerprintFragment}
    id: str = ""
    fragments: List[FingerprintFragment] = []


FormatFileState = Literal["NEW", "UNCHANGED", "NEEDSUPDATE", "DELETE"]


class FileEntry(SerializableClass):
    _typeMapper = {"fragments": FingerprintFragment}
    _noSerialize = ["isDir", "name"]
    id: Optional[str] = None
    # The naming here is confusing. FullPath is part of the LOGS API but it refers
    # to the full path in LOGS and not the actual file path.
    fullPath: str = ""
    path: str = ""
    isDir: bool = False
    name: str = ""
    fragments: Optional[List[FingerprintFragment]] = None
    hash: Optional[str] = None
    state: Optional[FormatFileState] = None
    mtime: Optional[datetime] = None

    def __init__(
        self,
        ref: Any = None,
        fullPath: Optional[str] = None,
        state: Optional[FormatFileState] = None,
    ):
        if isinstance(ref, FileEntry):
            super().__init__(self._fieldsFromPath(ref.path))
            self.fullPath = ref.fullPath
            self.state = ref.state
        elif isinstance(ref, os.DirEntry) and ref.path:
            super().__init__(self._fieldsFromPath(ref.path))
        elif isinstance(ref, str) or fullPath is not None:
            super().__init__(
                self._fieldsFromPath(str(ref if fullPath is None else fullPath))
            )
        else:
            super().__init__(ref)

        if fullPath is not None:
            self.fullPath = fullPath
        if state is not None:
            self.state = state

    @classmethod
    def _fieldsFromPath(cls, path: str):
        _path = os.path.realpath(path)
        return {
            "id": uuid.uuid4().hex,
            "fullPath": _path,
            "path": _path,
            "isDir": os.path.isdir(_path),
            "name": os.path.basename(_path),
        }

    def __str__(self):
        return "<%s %s%a>" % (
            type(self).__name__,
            ("<dir> " if self.isDir else ""),
            self.path,
        )

    def addFragment(self, fragments: List[FingerprintFragment]):
        with open(self.path, "rb") as read:
            if self.fragments is None:
                self.fragments = []
            for fragment in fragments:
                read.seek(fragment.offset)
                fragment.bytes = base64.b64encode(read.read(fragment.length)).decode(
                    "utf-8"
                )
                self.fragments.append(fragment)

    def addHash(self):
        with open(self.path, "rb") as read:
            self.hash = sha256(read.read()).hexdigest()

    def addMtime(self):
        self.mtime = datetime.fromtimestamp(os.path.getmtime(self.path))

    @classmethod
    def entriesFromFiles(
        cls,
        files: Union[Constants.FILE_TYPE, Sequence[Constants.FILE_TYPE]],
        ignoreReadErrors=False,
    ):
        if files == None:
            raise FileNotFoundError("Could not read file or directory from 'None' path")
        if not isinstance(files, list):
            files = [cast(Constants.FILE_TYPE, files)]

        result: List[FileEntry] = []

        while len(files) > 0:
            file = files.pop(0)
            if isinstance(file, (str, os.DirEntry, FileEntry)):
                f = FileEntry(file)
                if f.isDir:
                    with os.scandir(f.path) as entries:
                        files.extend(entries)
                else:
                    if not os.path.isfile(f.path) or not os.access(f.path, os.R_OK):
                        if not ignoreReadErrors:
                            raise PermissionError("Could not read file %a" % f.path)
                    else:
                        f.id = uuid.uuid4().hex
                        result.append(f)

        return result

    def modifyPathPrefix(
        self, prefixToStrip: Optional[str] = None, prefixToAdd: Optional[str] = None
    ):
        if prefixToStrip and self.fullPath.startswith(prefixToStrip):
            self.fullPath = self.fullPath[len(prefixToStrip) :]
        if prefixToAdd and not self.fullPath.startswith(prefixToAdd):
            self.fullPath = os.path.join(prefixToAdd, self.fullPath)
