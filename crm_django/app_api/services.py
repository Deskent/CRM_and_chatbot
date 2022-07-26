from app_api.models import Client, Order, Category, Poll


class DBIClient:
    model = Client

    @classmethod
    def get_dict(
            cls,
            telegram_id,
            name='',
            first_name='',
            last_name='',
            username='',
            description='',
            **kwargs
    ):
        return {
            'telegram_id': telegram_id,
            'name': name,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'description': description,
        }


class DBIOrder:
    model = Order

    @classmethod
    def get_dict(
            cls,
            category_id: int,
            **kwargs
    ):
        return {
            'category_id': category_id,
        }


class DBICategories:
    model = Category

    @classmethod
    def get_categories(cls) -> dict:
        categories = cls.model.objects.all()
        result = {}
        for category in categories:
            result[category.id] = category.description

        return result


class DBIPoll:
    model = Poll

    @classmethod
    def get_poll(cls, category_id: int) -> list[str]:
        poll = cls.model.objects.filter(category_id=category_id).all()

        return [question.text for question in poll]
