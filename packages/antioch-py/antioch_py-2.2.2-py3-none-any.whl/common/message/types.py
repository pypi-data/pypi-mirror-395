from common.message.base import Message


class Bool(Message):
    """
    Boolean value message.
    """

    _type = "antioch/bool"
    value: bool


class Int(Message):
    """
    Integer value message.
    """

    _type = "antioch/int"
    value: int


class Float(Message):
    """
    Float value message.
    """

    _type = "antioch/float"
    value: float


class String(Message):
    """
    String value message.
    """

    _type = "antioch/string"
    value: str
