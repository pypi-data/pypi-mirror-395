from LOGS.Entities.LabNotebookEntryContent.TextMarks import (
    TextMarkBold,
    TextMarkCode,
    TextMarkContentPlaceholder,
    TextMarkItalic,
    TextMarkLink,
    TextMarkStrike,
    TextMarkSub,
    TextMarkSup,
    TextMarkTextColor,
    TextMarkTextHighlight,
    TextMarkUnderline,
)


class TextMarkConverter:
    @staticmethod
    def convert(mark: dict):
        if "type" not in mark:
            raise ValueError(f"TextMark must contain a 'type' field. (Got '{mark}')")
        _type = mark["type"]
        if _type == "bold":
            return TextMarkBold(mark)
        if _type == "italic":
            return TextMarkItalic(mark)
        elif _type == "underline":
            return TextMarkUnderline(mark)
        elif _type == "strike":
            return TextMarkStrike(mark)
        elif _type == "sup":
            return TextMarkSup(mark)
        elif _type == "sub":
            return TextMarkSub(mark)
        elif _type == "code":
            return TextMarkCode(mark)
        elif _type == "textColor":
            return TextMarkTextColor(mark)
        elif _type == "textHighlight":
            return TextMarkTextHighlight(mark)
        elif _type == "link":
            return TextMarkLink(mark)
        elif _type == "contentPlaceholder":
            return TextMarkContentPlaceholder(mark)
        else:
            raise ValueError(f"TextMark type '{_type}' is not supported.")
