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


class BotTexts(BaseModel):
    enter_name: str = 'Введите имя:'
    enter_link: str = 'Введите ссылку:'
    enter_category: str = 'Выберите категорию:'
    enter_price: str = 'Выберите бюджет:'
    category_list: str = 'Список категорий:'
    was_advertised: str = "Велась ли раньше работа над проектом?"
    what_after: str = "Что хотите видеть после сотрудничества со специалистом?"
