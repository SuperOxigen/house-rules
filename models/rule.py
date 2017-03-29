
class Part(object):
    def __init__(self, editable: bool):
        self._editable = editable
        pass

    @property
    def editable(self) -> bool:
        return self._editable

class TextPart(object):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str):
        if self.editable:
            self._text = str(value)
        else:
            raise ValueError("Cannot assign to a non-editable")

class NumberPart(object):
    def __init__(self, value: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = int(value)

class Rule(object):
    def __init__(self, number: int):
        self._number = number


    @property
    def number(self) -> int:
        return self._number
