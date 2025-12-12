import dataclasses
import os
import random
import string
import sys
from datetime import datetime, time, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Type, TypeVar, Union, cast
from unicodedata import normalize
from uuid import UUID

from regex import Regex

from LOGS.Auxiliary.DateTimeConverter import DateTimeConverter


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, data):
        self.stream.writelines(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


_T = TypeVar("_T")


class UnbufferedStdout(Unbuffered):
    def __init__(self):
        super().__init__(sys.stdout)


class Tools:
    messageStrMaxLength = 25
    __byteUnits = ["", "K", "M", "G", "T", "P", "E", "Z"]

    @classmethod
    def ObjectToString(cls, obj: Any) -> str:
        name = getattr(obj, "name") if hasattr(obj, "name") else None
        id = getattr(obj, "id") if hasattr(obj, "id") else None
        i = " id:'%s'" % id if id is not None else ""
        n = " name:'%s'" % name if name is not None else ""
        return "<%s%s%s>" % (type(obj).__name__, i, n)

    @classmethod
    def unbufferStdout(cls):
        unbuffered = UnbufferedStdout()
        sys.stdout = cast(Any, unbuffered)

    @classmethod
    def getHumanReadableSize(cls, size, suffix="B"):
        for unit in cls.__byteUnits:
            if abs(size) < 1024.0:
                return "%3.1f%s%s" % (size, unit, suffix)
            size /= 1024.0
        return "%.1f%s%s" % (size, "Yi", suffix)

    @classmethod
    def osPathSeparators(cls):
        seps = []
        for sep in os.path.sep, os.path.altsep:
            if sep:
                seps.append(sep)
        return seps

    @classmethod
    def sanitizeFileName(cls, fileName: Optional[str], defaultName: str = "Unknown"):
        if not fileName:
            fileName = defaultName
        # Sort out unicode characters
        valid_filename = (
            normalize("NFKD", fileName).encode("ascii", "ignore").decode("ascii")
        )
        # Replace path separators with underscores
        for sep in cls.osPathSeparators():
            valid_filename = valid_filename.replace(sep, "_")
        # Ensure only valid characters
        valid_chars = "-_.() {0}{1}".format(string.ascii_letters, string.digits)
        valid_filename = "".join(ch for ch in valid_filename if ch in valid_chars)
        # Ensure at least one letter or number to ignore names such as '..'
        valid_chars = "{0}{1}".format(string.ascii_letters, string.digits)
        test_filename = "".join(ch for ch in fileName if ch in valid_chars)
        if len(test_filename) == 0:
            # Replace empty file name or file path part with the following
            valid_filename = defaultName
        if valid_filename[0] not in string.ascii_letters:
            valid_filename = "_" + valid_filename
        return valid_filename

    @classmethod
    def timeToString(cls, dt: Optional[time]) -> str:
        if dt is None:
            return ""
        return dt.strftime("%H:%M:%S") + f".{dt.microsecond:03d}"

    @classmethod
    def datetimeToUTCString(cls, dt: Optional[datetime]) -> str:
        if dt is None:
            return ""
        dt = dt.astimezone(
            timezone.utc
        )  # we convert all datetimes to UTC for the LOGS server
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    @classmethod
    def eclipsesJoin(cls, separator: str, items: List, maxCount: int = 3):
        if len(items) > maxCount:
            items = items[:maxCount]
            return separator.join(items) + "..."

        return separator.join(items)

    @classmethod
    def wordToPlural(cls, word: str):
        if word[-1] == "y":
            return word[:-1] + "ies"

        return word + "s"

    @classmethod
    def plural(cls, word: str, count: Union[int, list, set]):
        if isinstance(count, (list, set)):
            count = len(count)

        if count == 1:
            return word

        return cls.wordToPlural(word)

    @classmethod
    def numberPlural(cls, word: str, count: Union[int, List]):
        if isinstance(count, list):
            count = len(count)

        if count < 1:
            return "no %s" % cls.wordToPlural(word)

        if count < 2:
            return "%d %s" % (count, word)

        return "%d %s" % (count, cls.wordToPlural(word))

    @classmethod
    def getTypeFromTypeEntry(cls, item: dict, types: list):
        if isinstance(item, dict) and "type" in item:
            type = item["type"]
            for t in types:
                if t._type == type:
                    return t
            return None
        else:
            return None

    _uidRegex = Regex(
        r"^[0-9a-f]{8}\-?[0-9a-f]{4}\-?[0-9a-f]{4}\-?[0-9a-f]{4}\-?[0-9a-f]{12}$"
    )

    @classmethod
    def uuidConverter(cls, value):
        if isinstance(value, UUID):
            return value
        else:
            v = str(value)
            if not cls._uidRegex.match(v):
                raise Exception(
                    "The provided uid %a does not fit the format 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'"
                )
            return UUID(v)

    @classmethod
    def dataClassConverterGenerator(cls, dataClassType: type) -> Callable:

        if dataclasses.is_dataclass(dataClassType):

            def converter(value):
                if isinstance(value, dataClassType):
                    return value
                if isinstance(value, dict):
                    fieldTypes = set(f.name for f in dataclasses.fields(dataClassType))
                    fieldValues = {k: v for k, v in value.items() if k in fieldTypes}

                    return dataClassType(**fieldValues)
                raise Exception(f"Cannot convert to type {dataClassType.__name__}")

            return converter

        return lambda value: None

    @classmethod
    def checkAndConvert(
        cls,
        value: Any,
        fieldType: Union[Type[_T], str],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone=False,
        initOnNone=False,
    ) -> _T:
        if isinstance(fieldType, list):
            fieldType = cast(Any, cls.getTypeFromTypeEntry(value, fieldType))

        if not fieldType:
            return value

        if not isinstance(fieldType, type) and converter is None:
            raise Exception(
                f"Manual field type '{fieldType}' cannot be used without a converter definition."
            )

        if not converter:
            if isinstance(fieldType, type) and isinstance(value, fieldType):
                return value

            if issubclass(cast(Type[_T], fieldType), Enum):
                if allowNone and value == None:
                    return cast(Any, None)

                try:
                    enum = cast(Any, fieldType)
                    return enum(value)
                except ValueError:
                    raise Exception(
                        "Field %a cannot be converted to enum type %a. (Got invalid value %a)"
                        % (
                            fieldName,
                            cast(type, fieldType).__name__,
                            cls.truncString(str(value)),
                        )
                    )

            if cast(type, fieldType).__name__ == datetime.__name__:
                converter = cast(Callable, DateTimeConverter.convertDateTime)
            elif cast(type, fieldType).__name__ == time.__name__:
                converter = cast(Callable, DateTimeConverter.convertTime)
            elif cast(type, fieldType).__name__ == UUID.__name__:
                converter = cast(Callable, cls.uuidConverter)
            elif dataclasses.is_dataclass(fieldType):
                converter = cls.dataClassConverterGenerator(fieldType)
            else:
                converter = cast(Callable, fieldType)

        if fieldName == None:
            fieldName = "field"
        fieldName = cast(str, fieldName)

        if value == None:
            if initOnNone and hasattr(fieldType, "__init__"):
                return cast(Callable, fieldType)()
            if allowNone:
                return cast(Any, None)
            else:
                raise Exception("Field %a cannot be 'None'." % (fieldName))

        typeName = (
            cast(type, fieldType).__name__
            if isinstance(fieldType, type)
            else str(fieldType)
        )

        # print(f"{fieldName}({fieldType}) = {value}")
        try:
            value = converter(value)
        except:
            raise Exception(
                "Field %a cannot be converted to type %a. (Got value %a of type %a)"
                % (
                    fieldName,
                    typeName,
                    cls.truncString(str(value)),
                    type(value).__name__,
                )
            )

        # print(f"{fieldName}({fieldType}) => {value}")

        if value == None:
            if allowNone:
                return cast(Any, None)
            else:
                raise Exception("%s cannot be 'None'." % (fieldName))

        return value

    @classmethod
    def checkListAndConvert(
        cls,
        value: Any,
        fieldType: Union[Type[_T], str],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone: bool = False,
        singleToList: bool = False,
        length: int = -1,
    ) -> List[_T]:
        if fieldName == None:
            fieldName = "field"
        fieldName = cast(str, fieldName)

        if value == None:
            value = []

        if singleToList:
            if not isinstance(value, (list, tuple)):
                value = [value]

        typeName = (
            cast(type, fieldType).__name__
            if isinstance(fieldType, type)
            else str(fieldType)
        )
        if not isinstance(value, (list, tuple)):
            raise Exception(
                "%s must be of type 'list[%s]'. (Got type %a)"
                % (fieldName, typeName, type(value).__name__)
            )

        if length >= 0 and len(value) != length:
            raise Exception(
                "%s must have length %d. (Got length %a)"
                % (fieldName, length, len(value))
            )

        return [
            cls.checkAndConvert(
                f,
                fieldType=fieldType,
                fieldName="%s[%d]" % (fieldName, i),
                converter=converter,
                allowNone=allowNone,
            )
            for i, f in enumerate(value)
        ]

    @staticmethod
    def checkDirectory(dir):
        if not os.path.isdir(dir):
            return "could not find directory '%s'" % dir

        list_of_entries = []
        try:
            with os.scandir(dir) as entries:
                for entry in entries:
                    list_of_entries.append(entry.name)
        except PermissionError:
            return "permission denied for directory '%s' on server" % dir
        except:
            return "could not access directory '%s'" % dir

        return False

    @staticmethod
    def convertToNativeNewline(text: str):
        return text.replace("\n", os.linesep)

    @staticmethod
    def namedSwitchConverter(switchList: List[str]) -> Dict[str, bool]:
        result = {}
        for s in switchList:
            result[s] = True

        return result

    @staticmethod
    def stringToId(s: str):
        if not isinstance(s, str):
            s = str(s)
        return "".join([c if c.isalpha() or c.isdigit() else "_" for c in s]).rstrip()

    @classmethod
    def truncString(cls, text: str, length: int = 30) -> str:
        return "%s%s" % (text[:length], "..." if len(text) > length else "")

    @classmethod
    def checkSubFieldAndConvert(
        cls,
        value: dict,
        fieldType: Union[Type[_T], str],
        fieldName: Union[str, None],
        subFieldName: str,
        allowNone=False,
    ):
        name = f"{fieldName}.{subFieldName}" if fieldName else None
        v = value.get(subFieldName, None) if isinstance(value, dict) else None
        return Tools.checkAndConvert(v, fieldType, name, allowNone=allowNone)

    @classmethod
    def resolveKeyConflictWithPrefix(
        cls,
        name: str,
        prefix: str,
        lookup: Union[Dict, Set],
        separator="_",
        startIndex=1,
    ) -> str:
        originalName = name
        index = startIndex
        while name in lookup or prefix + name in lookup:
            name = f"{originalName}{separator}{index}"
            index += 1
        return name

    @classmethod
    def resolveKeyConflict(
        cls, name: str, lookup: Union[Dict, Set], separator="_", startIndex=1
    ) -> str:
        originalName = name
        index = startIndex
        while name in lookup:
            name = f"{originalName}{separator}{index}"
            index += 1
        return name

    @classmethod
    def generateRandomString(cls, len=10):
        return "".join(map(lambda r: chr(random.randint(65, 90)), range(len)))

    @classmethod
    def gerundVerb(cls, verb: str):
        if verb.endswith("ing"):
            return verb
        elif verb.endswith("e"):
            verb = verb[:-1]

        return verb + "ing"
