from LOGS.Entities.LabNotebookEntryContent.EntryContentItem import EntryContentItem
from LOGS.Entities.LabNotebookEntryContent.IEntryContentWithAttribute import (
    IEntryContentWithAttribute,
)
from LOGS.Entities.LabNotebookEntryContent.TextMarkAtributes import (
    TextMarkAttributeDefault,
    TextMarkAttributeLink,
    TextMarkAttributeTextColor,
    TextMarkAttributeTextHighlight,
)


class TextMarkBold(EntryContentItem, IEntryContentWithAttribute):
    _type = "bold"
    _attrType = TextMarkAttributeDefault


class TextMarkItalic(EntryContentItem, IEntryContentWithAttribute):
    _type = "italic"
    _attrType = TextMarkAttributeDefault


class TextMarkUnderline(EntryContentItem, IEntryContentWithAttribute):
    _type = "underline"
    _attrType = TextMarkAttributeDefault


class TextMarkStrike(EntryContentItem, IEntryContentWithAttribute):
    _type = "strike"
    _attrType = TextMarkAttributeDefault


class TextMarkSup(EntryContentItem, IEntryContentWithAttribute):
    _type = "sup"
    _attrType = TextMarkAttributeDefault


class TextMarkSub(EntryContentItem, IEntryContentWithAttribute):
    _type = "sub"
    _attrType = TextMarkAttributeDefault


class TextMarkCode(EntryContentItem, IEntryContentWithAttribute):
    _type = "code"
    _attrType = TextMarkAttributeDefault


class TextMarkTextColor(
    EntryContentItem, IEntryContentWithAttribute[TextMarkAttributeTextColor]
):
    _type = "textColor"
    _attrType = TextMarkAttributeTextColor


class TextMarkTextHighlight(
    EntryContentItem, IEntryContentWithAttribute[TextMarkAttributeTextHighlight]
):
    _type = "textHighlight"
    _attrType = TextMarkAttributeTextHighlight


class TextMarkLink(EntryContentItem, IEntryContentWithAttribute[TextMarkAttributeLink]):
    _type = "link"
    _attrType = TextMarkAttributeLink


class TextMarkContentPlaceholder(
    EntryContentItem, IEntryContentWithAttribute[TextMarkAttributeLink]
):
    _type = "contentPlaceholder"
    _attrType = TextMarkAttributeLink
