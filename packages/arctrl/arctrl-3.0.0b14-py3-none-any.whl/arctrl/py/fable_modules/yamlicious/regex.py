
KeyPattern: str = ("^(?P<key>[^\\{\\[]+):\\s*(" + "\\<c f=(?P<comment>\\d+)\\/\\>") + ")?$"

LineCommentPattern: str = ("^" + "\\<c f=(?P<comment>\\d+)\\/\\>") + "$"

ValuePattern: str = ("^(?P<value>.*?)\\s*?(" + "\\<c f=(?P<comment>\\d+)\\/\\>") + ")?$"

InlineSequencePattern: str = ("^\\[(?P<inlineSequence>.+)\\]\\s*?(" + "\\<c f=(?P<comment>\\d+)\\/\\>") + ")?$"

InlineJSONPattern: str = ("^\\{(?P<inlineSequence>.+)\\}\\s*?(" + "\\<c f=(?P<comment>\\d+)\\/\\>") + ")?$"

SequenceOpenerPattern: str = ("^\\[\\s*(" + "\\<c f=(?P<comment>\\d+)\\/\\>") + ")?$"

SequenceCloserPattern: str = ("^\\]\\s*(" + "\\<c f=(?P<comment>\\d+)\\/\\>") + ")?$"

JSONOpenerPattern: str = ("^(?P<key>[^\\{\\[]+):\\s+\\{\\s*(" + "\\<c f=(?P<comment>\\d+)\\/\\>") + ")?$"

JSONCloserPattern: str = ("^\\}\\s*(" + "\\<c f=(?P<comment>\\d+)\\/\\>") + ")?$"

__all__ = ["KeyPattern", "LineCommentPattern", "ValuePattern", "InlineSequencePattern", "InlineJSONPattern", "SequenceOpenerPattern", "SequenceCloserPattern", "JSONOpenerPattern", "JSONCloserPattern"]

