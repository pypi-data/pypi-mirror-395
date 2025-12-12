from typing import TypedDict, NotRequired


class ChatMessage(TypedDict):
    """
    The structure of messages returned by the hackmud chat API.

    As not all attributes may be present, it is reccomended any "optional" attributes are fetched with the `get` method.

    Attributes:
        id (str): The unique message ID.
        t (float): Timestamp of when the message was sent.
        from_user (str): Message sender.
        msg (str): Message content.
        to_user (str, optional): The target user of a tell.
        channel (str, optional): The channel in which the message was sent.
        is_leave (str, optional): If the message is a leave message.
        is_join (str, optional): If the message is a join message.
    """

    id: str
    t: float
    from_user: str
    msg: str
    to_user: NotRequired[str]
    channel: NotRequired[str]
    is_leave: NotRequired[bool]
    is_join: NotRequired[bool]


class TokenError(ConnectionError):
    """
    Error thrown when an invalid token is encountered.
    """
