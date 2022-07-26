from pydantic import BaseModel


class Category:
    categories: dict = {}


class Worksheet(BaseModel):
    telegram_id: int = None
    name: str = None
    first_name: str = None
    last_name: str = None
    username: str = None
    category_id: int = None
    poll: list[list[str]] = None

    def as_dict(self) -> dict:
        return self.__dict__
