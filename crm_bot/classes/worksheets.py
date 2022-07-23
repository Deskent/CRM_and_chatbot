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


class BotTexts(BaseModel):
    enter_name: str = 'Введите имя:'
    enter_link: str = 'Введите ссылку:'
    enter_category: str = 'Выберите категорию:'
    enter_price: str = 'Выберите бюджет:'
    category_list: str = 'Список категорий:'
    was_advertised: str = "Велась ли раньше работа над проектом?"
    what_after: str = "Что хотите видеть после сотрудничества со специалистом?"



if __name__ == '__main__':
    data = {
        'enter_name': 'Enter your name',
        'enter_link': 'Enter link ',
        'something': 123
    }
    texts = BotTexts(**data)
    # for key, value in data.items():
    #     if key in texts.__annotations__:
    #         texts.__setattr__(key, value)
    # print(texts.__annotations__)
    print(texts.enter_name, texts.enter_link, texts.__dict__)