from functools import wraps
from typing import Callable, Any

from aiogram.types import Message

from config import logger


@logger.catch
def check_message_private(func: Callable) -> Callable:
    """decorator for handler check message is private"""

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        message: Message = args[0]
        message_chat_id = message.from_user.id
        chat_id = message.chat.id
        if message_chat_id == chat_id:
            logger.debug(f"Message {message_chat_id} == {chat_id}.")
            return await func(*args, **kwargs)
        logger.debug(f"Message {message_chat_id} != {chat_id}.")

    return wrapper
