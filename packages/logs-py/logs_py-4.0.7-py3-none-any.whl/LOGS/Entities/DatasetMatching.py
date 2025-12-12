from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional, Sequence, Union

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Decorators import Endpoint
from LOGS.Auxiliary.Exceptions import LOGSException
from LOGS.Auxiliary.Tools import Tools
from LOGS.Entities.DatasetMatchTypes import MatchRequest, MatchResult
from LOGS.Entities.FileEntry import FileEntry
from LOGS.Entity.EntityConnector import EntityConnector
from LOGS.LOGSConnection import LOGSConnection


@dataclass
class DirectoryTreeNode:
    name: str = ""
    path: str = "/"
    type: Literal["dir", "file"] = "dir"
    content: Dict[str, "DirectoryTreeNode"] = field(default_factory=dict)
    fileCount: int = 0

    def print(self, countOnly=False, indent=""):
        if self.type == "file":
            if not countOnly:
                print("%s%s (f)" % (indent, self.name))
            return
        print(
            "%s%s (%s)%s"
            % (
                indent,
                self.name,
                Tools.getHumanReadableSize(self.fileCount),
                ": " + str(len(self.content.keys())) if countOnly else "",
            )
        )
        for entry in self.content.values():
            entry.print(indent=indent + "..", countOnly=countOnly)

    def splitTreeByFileCount(self, maxCount: int, parentPath="", level=0):
        forrest: List[DirectoryTreeNode] = []

        path = parentPath + "/" + self.name
        if path == "/":
            path = ""
        # print(
        #     "." * level + self.name,
        #     self.fileCount,
        #     "<",
        #     maxSize,
        #     "->",
        #     self.fileCount <= maxSize,
        #     "=>",
        #     path,
        # )
        if self.fileCount <= maxCount:
            self.path = path
            return [self]
        else:
            files = [item for item in self.content.values() if item.type == "file"]
            if len(files) > 0:
                forrest.append(
                    DirectoryTreeNode(
                        name=self.name,
                        path=path,
                        content={f.name: f for f in files},
                        fileCount=len(files),
                    )
                )

            for item in self.content.values():
                if item.type == "dir":
                    forrest.extend(
                        item.splitTreeByFileCount(
                            maxCount=maxCount, parentPath=path, level=level + 1
                        )
                    )

        return forrest


@Endpoint("data_formats")
class DatasetMatching(EntityConnector):
    _request: MatchRequest = MatchRequest()
    _formatIds: Optional[List[str]] = None
    _matchResult: Optional[MatchResult] = None
    _files: List[List[FileEntry]] = []
    _maxFileCountInDirectory = 20000

    def __init__(
        self,
        connection: LOGSConnection,
        files: Union[Constants.FILE_TYPE, Sequence[Constants.FILE_TYPE]],
        formatIds: Optional[List[str]] = None,
        ignoreReadErrors=False,
    ):
        self._connection = connection
        self._formatIds = formatIds
        self._files = self.splitFileList(
            FileEntry.entriesFromFiles(files, ignoreReadErrors)
        )

    @classmethod
    def fileListToTree(cls, files: List[FileEntry]):
        root = DirectoryTreeNode(name="")
        i = 0
        for file in files:
            path = file.path.split("/")
            rootPath = path.pop(0)
            fileName = path.pop()
            # fileSize = file.size if file.size else 0
            if rootPath != "":
                continue
            current = root
            for i, p in enumerate(path):
                current.fileCount += 1
                if p not in current.content:
                    current.content[p] = DirectoryTreeNode(
                        name=p, path="/".join(f for f in path[:i])
                    )

                current = current.content[p]
            current.fileCount += 1
            current.content[fileName] = DirectoryTreeNode(
                name=fileName, path=file.path, type="file", fileCount=1
            )

        return root

    @classmethod
    def TreeToFileList(cls, root: DirectoryTreeNode):
        if root.type == "file":
            file = FileEntry()
            file.fullPath = root.path
            file.id = root.path
            file.path = root.path
            return [file]

        files: List[FileEntry] = []
        for item in root.content.values():
            files.extend(cls.TreeToFileList(item))

        return files

    def splitFileList(self, files: List[FileEntry]):
        root = self.fileListToTree(files)
        forrest = root.splitTreeByFileCount(maxCount=self._maxFileCountInDirectory)
        return [self.TreeToFileList(tree) for tree in forrest]

    def __iter__(self):
        for files in self._files:
            self._request = MatchRequest()
            self._request.formatIds = self._formatIds
            self._request.files = files

            self._match()
            if not self._matchResult:
                return None
            for match in self._matchResult.matches:
                for dataset in match:
                    yield dataset

    def _match(self):
        connection, endpoint = self._getConnectionData()

        # print(
        #     ">>> request",
        #     len(self._request.files),
        #     len(str(self._request.toDict()).encode("utf-8")),
        #     "->",
        #     len(str(self._request.toDict()).encode("utf-8")) / len(self._request.files),
        #     "<",
        #     30000000,
        # )
        data, error = connection.postEndpoint(
            endpoint=endpoint + ["match"], data=self._request.toDict()
        )
        if error:
            raise LOGSException("Could not match dataset files: %a" % error)

        self._matchResult = MatchResult(data)

        if self._matchResult.missingFragments:
            lookUp = {e.id: e for e in self._request.files}
            for fileFragment in self._matchResult.missingFragments:
                if fileFragment.id not in lookUp:
                    continue

                file = lookUp[fileFragment.id]
                file.addFragment(fileFragment.fragments)

            data, error = connection.postEndpoint(
                endpoint=endpoint + ["match"], data=self._request.toDict()
            )
            if error:
                raise LOGSException("Could not match dataset files: %a" % error)
            self._matchResult = MatchResult(data)
