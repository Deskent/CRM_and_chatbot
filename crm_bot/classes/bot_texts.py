class BotTexts:
    enter_name: str = 'Введите имя:'
    enter_link: str = 'Введите ссылку:'
    enter_category: str = 'Выберите категорию:'
    enter_price: str = 'Выберите бюджет:'
    category_list: str = 'Список категорий:'
    was_advertised: str = "Велась ли раньше работа над проектом?"
    what_after: str = "Что хотите видеть после сотрудничества со специалистом?"

    @classmethod
    def update_all(cls, data: dict):
        for key, value in data.items():
            if key in cls.__dict__:
                setattr(cls, key, value)
