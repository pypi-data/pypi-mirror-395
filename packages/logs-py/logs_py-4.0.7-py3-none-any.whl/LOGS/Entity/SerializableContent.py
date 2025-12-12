import dataclasses
import inspect
import json
import math
from datetime import datetime, time, timedelta
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

import numpy as np

from LOGS.Auxiliary.Constants import Constants
from LOGS.Auxiliary.Exceptions import EntityIncompleteException
from LOGS.Auxiliary.ReplaceMessage import ReplaceMessage
from LOGS.Auxiliary.Tools import Tools

_T = TypeVar("_T")


class SerializableContent:
    _indentationString: str = "  "

    _noSerialize: List[str] = []
    _typeMapper: Optional[Dict[str, Any]] = None
    _slack: Dict[str, Any] = {}
    _mappingErrors: List[Dict[str, str]] = []

    _planeClass: bool = False
    _includeNone: bool = False
    _debugPrintRef: bool = False
    _includeSlack: bool = False

    def __init__(self, ref=None):
        if ref != None:
            self._fromRef(ref=ref, selfClass=type(self))

    def override(self, ref):
        self._fromRef(ref=ref, selfClass=type(self))

    def _fromRef(
        self,
        ref,
        selfClass,
        convertOtherType: Optional[Tuple[type, Callable[[Any], Any]]] = None,
    ):
        if self._debugPrintRef:
            print("FromRef", selfClass.__name__, "\n", self._dictToJson(ref))

        if convertOtherType and isinstance(ref, convertOtherType[0]):
            ref = convertOtherType[1](ref)

        serializableAncestors = tuple(
            [c for c in inspect.getmro(selfClass) if issubclass(c, SerializableContent)]
        )

        # if isinstance(ref, selfClass):
        if isinstance(ref, serializableAncestors):
            self.fromInstance(ref)
        elif isinstance(ref, dict):
            if hasattr(self, "_typeMapper") and self._typeMapper:
                for k, t in self._typeMapper.items():
                    if k in ref:
                        if isinstance(ref[k], list):
                            self.checkFieldAndConvertToList(
                                ref, fieldName=k, fieldType=t
                            )
                        else:
                            self.checkFieldAndConvert(
                                elements=ref, fieldName=k, fieldType=t, allowNone=True
                            )

            self.fromDict(ref)
        else:
            if isinstance(ref, str):
                try:
                    self.fromString(ref)
                    return
                except NotImplementedError:
                    pass

            types: List[type] = [dict, type(self)]
            if convertOtherType:
                if isinstance(convertOtherType[0], (tuple, list)):
                    types.extend(convertOtherType[0])
                else:
                    types.append(convertOtherType[0])
            raise Exception(
                "%s instance cannot be derived from type %a. (Expected one of %s)"
                % (
                    selfClass.__name__,
                    type(ref).__name__,
                    ", ".join([f"'{t.__name__}'" for t in types]),
                )
            )

    def fromString(self, text: str):
        raise NotImplementedError("fromString is not implemented.")

    def fromInstance(self, ref):
        attrList = self._getAttrList()
        if "customType" in attrList:
            attrList.remove(
                "customType"
            )  # do not copy customType in fromInstance as the customType is part of the class definition
        for k in attrList:
            if hasattr(ref, k):
                try:
                    setattr(self, k, getattr(ref, k))
                except AttributeError:
                    pass

    def _getSlack(self, ignoreClasses: Optional[List[Type]] = None):
        slack = {"class": type(self).__name__, "slack": {}}
        if self._slack:
            slack["slack"]["self"] = self._slack
        attrList = self._getAttrList()
        for k in attrList:
            try:
                if hasattr(self, k):
                    item = getattr(self, k)
                    if isinstance(item, list):
                        slacks = {}
                        for i, e in enumerate(item):
                            if ignoreClasses and any(
                                type(e) == c for c in ignoreClasses
                            ):
                                continue
                            if isinstance(e, SerializableContent):
                                s = e._getSlack(ignoreClasses=ignoreClasses)
                                if s["slack"]:
                                    slacks[f"{k}[{i}]"] = s
                        if slacks:
                            slack["slack"].update(slacks)

                    if isinstance(item, SerializableContent):
                        if ignoreClasses and any(
                            type(item) == c for c in ignoreClasses
                        ):
                            continue
                        s = item._getSlack(ignoreClasses=ignoreClasses)
                        if s["slack"]:
                            slack["slack"][k] = s
            except AttributeError:
                pass

        return slack

    def _printSlackDict(self, slack: dict, prefix=""):
        if not slack or "slack" not in slack or not slack["slack"]:
            return

        prefix += slack["class"] if prefix == "" else f"({slack['class']})"
        if "self" in slack["slack"]:
            print(f"{prefix}:")
            for k, v in slack["slack"]["self"].items():
                print(f"  {prefix}.{k}: {self.truncString(str(v), length=100)}")
        for k, v in slack["slack"].items():
            if k == "self":
                continue
            self._printSlackDict(v, "  " + prefix + f".{k}")

    def _printSlack(self, ignoreClasses: Optional[List[Type]] = None):
        self._printSlackDict(self._getSlack(ignoreClasses=ignoreClasses))

    def _printMappingErrors(self):
        if self._mappingErrors:
            print(f"Mapping errors in {type(self).__name__}:")
            for e in self._mappingErrors:
                path = ".".join(e["path"]) if "path" in e else ""
                print(
                    f" - Field '{e['field']}' with value '{e['value']}' could not be mapped: {e['error']}"
                    + (f" (at {path})" if path else "")
                )

    def fromDict(self, ref) -> None:
        # print("ref", ref)
        # print("ref", type(self).__name__)
        if not hasattr(self, "_noSerialize"):
            self._noSerialize = []

        self._mappingErrors = []

        mappedKey = {
            k: False
            for k, v in ref.items()
            if v is not None and k not in self._noSerialize
        }

        for k in dir(self):
            # print(
            #     f"[{type(self).__name__}] Attribute",
            #     k,
            #     k in ref and hasattr(self, k) and not callable(getattr(self, k)),
            #     "->",
            #     ref[k] if k in ref else "NULL",
            # )

            try:
                hasAttr = hasattr(self, k)
            except (
                EntityIncompleteException
            ):  # while deserializing we want to ignore incomplete fields
                hasAttr = False

            if k in ref and hasAttr and not callable(getattr(self, k)):
                try:
                    # print("  ", k, "->", ref[k])
                    setattr(self, k, ref[k])
                    mappedKey[k] = True
                except AttributeError as e:
                    # comment in for debugging mapping errors
                    # print(
                    #     f"[{type(self).__name__}] ERROR:",
                    #     k,
                    #     "->",
                    #     ref[k],
                    #     "Message:",
                    #     e,
                    # )
                    # import traceback
                    # traceback.print_exc()

                    self._mappingErrors.append(
                        {
                            "class": type(self).__name__,
                            "field": k,
                            "value": Tools.truncString(str(ref[k]), length=100),
                            "error": str(e),
                        }
                    )

        self._slack = {k: ref[k] for k, v in mappedKey.items() if not v}

        # if self._slack:
        #     print(type(self).__name__, "->", ", ".join(self._slack.keys()))

    @classmethod
    def toBaseclassString(cls, obj):
        if isinstance(obj, SerializableContent):
            return obj.toString()
        if isinstance(obj, dict):
            return "<%s>" % obj["type"] if "type" in obj else "unknown"
        return "<%s>" % type(obj).__name__

    def toString(self):
        return str(self)

    def _typeSerializer(self, item: Any):

        if isinstance(item, SerializableContent):
            if self._includeSlack:
                return item._toDictWithSlack()
            else:
                return item.toDict()
        if dataclasses.is_dataclass(item):
            return (dataclasses.asdict(item) if not isinstance(item, type) else None,)
        elif isinstance(item, cast(Any, np.float32)):
            return item.item()
        elif isinstance(item, (list, np.ndarray)):
            l: Any = []
            for e in item:
                l.append(self._serializeItem(e))
            return l
        elif isinstance(item, timedelta):
            return item.total_seconds()
        elif isinstance(item, time):
            return Tools.timeToString(item)
        elif isinstance(item, datetime):
            return Tools.datetimeToUTCString(item)
        elif isinstance(item, Enum):
            return item.value
        elif isinstance(item, UUID):
            return str(item)
        elif isinstance(item, float):
            if math.isnan(item):
                item = 0
            elif math.isinf(item):
                item = 0
            return item
        elif hasattr(
            item, "__dict__"
        ):  # check if it is a defined class -> is this robust?
            return None

        return item

    def _serializeItem(self, item):
        if isinstance(item, dict):
            return {i: self._serializeItem(v) for i, v in item.items()}
        elif isinstance(item, list):
            return [self._serializeItem(v) for v in item]
        elif isinstance(item, tuple):
            return [self._serializeItem(v) for v in item]

        return self._typeSerializer(item)

    def _getAttrList(self):
        result = None
        if self._planeClass:
            result = [
                a[0]
                for a in inspect.getmembers(self, lambda a: not inspect.isroutine(a))
                if a[0][0] != "_"
            ]
        else:
            realAttributes = [
                a[1:]
                for a in dir(self)
                if a[0] == "_" and hasattr(self, a) and not callable(getattr(self, a))
            ]

            result = []
            for a in realAttributes:
                try:
                    if hasattr(self, a):
                        result.append(a)
                except (
                    EntityIncompleteException
                ):  # while serializing we want to ignore incomplete fields
                    pass

        return result

    def _toDictWithSlack(self):
        tmp = self._includeSlack
        self._includeSlack = True
        result = self.toDict()
        self._includeSlack = tmp
        return result

    def _truncFieldString(self, text: str, indentation: int, length: int = 100) -> str:
        tab = self._indentationString * indentation

        lines = [
            Tools.truncString(l, length) for l in text.split("\n") if l.strip() != ""
        ]
        if len(lines) > 4:
            lines = lines[:4]
            return "\n".join(lines) + f"\n{tab}..."
        else:
            return "\n".join(lines)

    def _serializableContentToString(self, item: Any, indentation: int, hideNone: bool):
        from LOGS.Entity.EntityMinimal import EntityMinimal

        if isinstance(item, (SerializableContent, EntityMinimal)):
            return self._truncFieldString(
                item.contentToString(indentation + 1, hideNone=hideNone),
                indentation + 1,
            )
        elif isinstance(item, str):
            return self._truncFieldString(item, indentation + 1)
        else:
            return Tools.truncString(str(self._typeSerializer(item)), 100)

    def contentToString(self, indentation: int = 1, hideNone: bool = False) -> str:
        from LOGS.Interfaces.ITypedEntity import ITypedEntity

        if not hasattr(self, "_noSerialize"):
            self._noSerialize = []

        attrList = self._getAttrList()

        # s = f"{type(self).__name__}"
        s = str(self)

        if isinstance(self, ITypedEntity):
            if self.customType:
                s += f" <{self.customType.name}>"
            if "customType" in attrList:
                attrList.remove("customType")
            if "customValues" in attrList:
                attrList.remove("customValues")

        s += "\n"

        tab = self._indentationString * indentation

        v: Optional[str] = None
        for k in attrList:
            if k in self._noSerialize:
                continue
            # s += f"{tab}{k}:\n"
            a = getattr(self, k)

            if a is None and hideNone:  # skip None values if hiding is enabled
                continue

            if isinstance(a, list):
                if len(a) == 0:
                    if not hideNone:
                        s += f"{tab}{k} = []\n"
                    continue
                l = []
                for i, e in enumerate(a):
                    l.append(
                        f"{tab}{self._indentationString }{self._serializableContentToString(e, indentation + 1, hideNone)}",
                    )
                    if i > 3:
                        break

                sub = ",\n".join(l)
                s += f"{tab}{k} = [\n{sub}\n{tab}]\n"
                continue

            if isinstance(a, dict):
                l = []
                for i, e in enumerate(a.keys()):
                    l.append(
                        f"{tab}{self._indentationString }{self._serializableContentToString(e, indentation + 1, hideNone)}",
                    )
                    if i > 3:
                        break

                sub = ",\n".join(l)
                s += f"{tab}{k} = {{\n{sub}\n{tab}}}\n"
                continue

            v = self._serializableContentToString(a, indentation, hideNone)
            s += f"{tab}{k} = {v}\n"

        if isinstance(self, ITypedEntity) and self.customValues:
            content = self.customValues._contentToString(
                indentation + 1, hideNone=hideNone
            )
            if content or not hideNone:
                s += f"{tab}customValues =\n{content}"

        return s

    def printContent(self, hideNone: bool = False) -> None:
        print(self.contentToString(hideNone=hideNone))

    def toDict(self) -> Dict[str, Any]:
        # print("toDict", type(self).__name__)
        if not hasattr(self, "_noSerialize"):
            self._noSerialize = []
        d = {}

        # customFields = self._getICustomValueFields()

        attrList = self._getAttrList()

        for k in attrList:
            if k in self._noSerialize:
                continue

            a = getattr(self, k)

            if a != None or self._includeNone:
                d[k] = self._serializeItem(a)

        if self._includeSlack:
            d.update({k: v for k, v in self._slack.items() if k not in d})

        return d

    @classmethod
    def _objectDictToDict(cls, item):
        # print("  item", item)
        if isinstance(item, dict):
            d = {}
            for k, v in item.items():
                # item[k] = cls._objectDictToDict(v)
                d[k] = cls._objectDictToDict(v)
            return d
        if isinstance(item, list):
            l = []
            for v in item:
                # item[k] = cls._objectDictToDict(v)
                l.append(cls._objectDictToDict(v))
            return l
        else:
            if hasattr(item, "toDict") and callable(getattr(item, "toDict")):
                return item.toDict()

        return item

    @classmethod
    def _dictToJson(cls, dict, indent=2, sort_keys=True, compact=False):
        separators = None
        if compact:
            indent = None
            separators = (",", ":")
        return json.dumps(
            dict, indent=indent, sort_keys=sort_keys, separators=separators
        )

    def toJson(self, indent=2, sort_keys=True, compact=False, validate=False):
        return self._dictToJson(
            self.toDict(), indent=indent, sort_keys=sort_keys, compact=compact
        )

    def printJson(self, indent=2, sort_keys=True, compact=False, validate=False):
        print(
            self.toJson(
                validate=validate, indent=indent, sort_keys=sort_keys, compact=compact
            )
        )

    @classmethod
    def truncString(cls, text: str, length: int = 30) -> str:
        return Tools.truncString(text=str(text), length=length)

    @staticmethod
    def delEntryFromDict(d: dict, entry: str):
        if entry in d:
            del d[entry]

    def dictToString(self, element, length=30):
        text = ""
        if "name" in element:
            text = "Name: " + str(element["name"])

        return self.truncString(text, length=length)

    @classmethod
    def plural(cls, word, count):
        if isinstance(count, list):
            count = len(count)

        if word[-1] == "y" and count > 1:
            word = word[:-1] + "ie"

        return word + ("s" if count > 1 else "")

    def createOnDemand(self, attr: str, typeOfValue: type):
        if getattr(self, attr) == None:
            setattr(self, attr, typeOfValue())

        return getattr(self, attr)

    def checkAndConvertNullable(
        self,
        value: Any,
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
    ):
        return self.checkAndConvert(
            value=value,
            fieldType=fieldType,
            fieldName=fieldName,
            converter=converter,
            allowNone=True,
        )

    def checkAndConvert(
        self,
        value: Any,
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone=False,
    ) -> _T:
        if (
            inspect.isclass(fieldType)
            and issubclass(fieldType, SerializableContent)
            and isinstance(value, dict)
            and not dataclasses.is_dataclass(fieldType)
        ):
            return cast(Any, fieldType)(ref=value)
        return cast(
            _T,
            Tools.checkAndConvert(
                value=value,
                fieldType=cast(Any, fieldType),
                fieldName=fieldName,
                converter=converter,
                allowNone=allowNone,
            ),
        )

    def checkFieldAndConvert(
        self,
        elements: Dict[str, Any],
        fieldType: Union[Type[_T], List[Type[_T]]],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone=False,
    ):
        if fieldName in elements:
            elements[fieldName] = self.checkAndConvert(
                elements[fieldName],
                fieldType=fieldType,
                fieldName=fieldName,
                converter=converter,
                allowNone=allowNone,
            )

    def checkFieldAndConvertToList(
        self,
        elements: Dict[str, Any],
        fieldType: Type[_T],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone: bool = False,
        singleToList: bool = False,
        length: int = -1,
    ):
        if fieldName in elements:
            elements[fieldName] = self.checkListAndConvert(
                elements[fieldName],
                fieldType=fieldType,
                fieldName=fieldName,
                converter=converter,
                allowNone=allowNone,
                singleToList=singleToList,
                length=length,
            )

    def checkListAndConvertNullable(
        self,
        value: Any,
        fieldType: Type[_T],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        length: int = -1,
    ):
        return self.checkListAndConvert(
            value=value,
            fieldType=fieldType,
            fieldName=fieldName,
            converter=converter,
            length=length,
            singleToList=True,
            allowNone=True,
        )

    def checkListAndConvert(
        self,
        value: Any,
        fieldType: Type[_T],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone: bool = False,
        singleToList: bool = False,
        length: int = -1,
    ) -> List[_T]:
        if (
            inspect.isclass(fieldType)
            and issubclass(fieldType, SerializableContent)
            and not dataclasses.is_dataclass(fieldType)
        ):
            if isinstance(value, tuple):
                value = list(value)
            if isinstance(value, list):
                for i in range(0, len(value)):
                    if isinstance(value[i], dict):
                        value[i] = cast(Any, fieldType)(ref=value[i])

        return Tools.checkListAndConvert(
            value=value,
            fieldType=fieldType,
            fieldName=fieldName,
            converter=converter,
            allowNone=allowNone,
            singleToList=singleToList,
            length=length,
        )

    def checkAndAppend(
        self,
        value: Any,
        fieldType: Type[_T],
        fieldName: Optional[str] = None,
        converter: Optional[Callable[[Any], _T]] = None,
        allowNone: bool = False,
    ):
        if not converter:
            converter = fieldType

        if value == None:
            value = []

        if fieldName == None:
            fieldName = "field"
        fieldName = cast(str, fieldName)

        if not isinstance(value, list):
            raise Exception(
                "%s must be of type 'list'. (Got type %a)"
                % (fieldName.capitalize(), type(value).__name__)
            )

        return [
            self.checkAndConvert(
                f,
                fieldName=fieldName,
                fieldType=fieldType,
                converter=converter,
                allowNone=allowNone,
            )
            for f in value
        ]

    def checkInstance(self, instance, path: List[str] = []):
        # print("check", path, instance)
        if isinstance(instance, SerializableContent):
            instance.check(path)

    def checkProperty(self, property: str, path: List[str] = []):
        if hasattr(self, property):
            item = getattr(self, property)
            if isinstance(item, list):
                for k, v in enumerate(item):
                    self.checkInstance(v, path + [str(self), "%s[%d]" % (property, k)])
            elif isinstance(item, dict):
                for k, v in item.items():
                    self.checkInstance(v, path + [str(self), "%s[%s]" % (property, k)])
            else:
                self.checkInstance(item, path + [str(self), "%s" % (property)])

    def check(self, path: List[str] = []):
        for k in dir(self):
            if hasattr(self, k) and not callable(getattr(self, k)) and k[0] != "_":
                self.checkProperty(k, path)

    def __str__(self):
        return "<%s>" % (type(self).__name__)

    @classmethod
    def replaceControlCharacters(
        cls,
        text: Optional[Union[str, Dict[str, str], List[str]]],
        excludeCharacters: List[str] = [],
        mergeMessages: bool = False,
        excludeKeys: List[str] = [],
    ):
        if text is None:
            return "", [ReplaceMessage(message="No text defined")]

        messages: List[ReplaceMessage] = []

        if isinstance(text, dict):
            if (
                "type" in text
                and text["type"] == "parameter"
                and "multiline" in text
                and text["multiline"]
            ):
                excludeCharacters.append("line feed")
            for k in text.keys():
                if k not in excludeKeys:
                    text[k], messages = cast(
                        Any,
                        cls.replaceControlCharacters(
                            text[k],
                            excludeKeys=excludeKeys,
                            excludeCharacters=excludeCharacters,
                            mergeMessages=mergeMessages,
                        ),
                    )
                    if messages:
                        for m in messages:
                            m.unshiftPath(k)
        elif isinstance(text, list):
            for i in range(0, len(text)):
                s, messages = cls.replaceControlCharacters(
                    text[i],
                    excludeKeys=excludeKeys,
                    excludeCharacters=excludeCharacters,
                    mergeMessages=mergeMessages,
                )
                text[i] = str(s)
                if messages:
                    for m in messages:
                        m.unshiftPath(i)
        elif isinstance(text, str):
            for k in Constants._control_character:
                if Constants._control_character[k][1] in excludeCharacters:
                    continue
                l = len(text)
                text = text.replace(Constants._control_character[k][0], "")
                if len(text) != l:
                    if mergeMessages:
                        messages.append(
                            ReplaceMessage("'%s'" % Constants._control_character[k][1])
                        )
                    else:
                        messages.append(
                            ReplaceMessage(
                                "contained special character '%s'"
                                % Constants._control_character[k][1]
                            )
                        )
        elif isinstance(text, float):
            if math.isnan(text):
                text = None
                messages.append(
                    ReplaceMessage(message="contained a float with 'NaN' value")
                )

        if mergeMessages and messages:
            if len(messages) > 1:
                messages = [
                    ReplaceMessage(
                        message="contained special characters "
                        + ", ".join(m.message for m in messages)
                    )
                ]
            else:
                messages = [
                    ReplaceMessage(
                        message="contained special character " + messages[0].message
                    )
                ]
            # for idx in range(0, len(messages)):
            #     msg = messages[idx]
            #     i = msg.index(0)
            #     if i > 0:
            #         m = ".".join(msg[0:i]) + ": " + " ".join(msg[i + 1 :])
            #         messages[idx] = m

        return text, messages

    @classmethod
    def generateID(cls, len=10):
        return Tools.generateRandomString(len=len)


class SerializableClass(SerializableContent):
    _planeClass = True
