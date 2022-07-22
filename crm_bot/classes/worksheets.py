from pydantic import BaseModel


class Worksheet(BaseModel):
    telegram_id: int = None
    name: str = None
    first_name: str = None
    last_name: str = None
    username: str = None
    target_link: str = None
    category: str = None
    price: int = None
    was_advertised: bool = None
    what_after: str = None

    def as_dict(self) -> dict:
        return self.__dict__
