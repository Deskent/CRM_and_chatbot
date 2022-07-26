from app_api.models import Texts, Client, Order, Category


class DBITexts:
    model = Texts

    @classmethod
    def get_texts(cls):
        texts = cls.model.objects.all()
        result = {}
        for text in texts:
            result[text.title] = text.text

        return result


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
            target_link='',
            price=0,
            was_advertised=False,
            what_after='',
            **kwargs
    ):
        return {
            'category_id': category_id,
            'target_link': target_link,
            'price': price,
            'was_advertised': was_advertised,
            'what_after': what_after,
        }


class DBICategories:
    model = Category

    @classmethod
    def get_texts(cls):
        categories = cls.model.objects.all()
        result = {}
        for category in categories:
            result[category.id] = category.description

        return result
