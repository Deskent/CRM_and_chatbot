from app_api.models import Texts, Client, Order


class DBITexts:
    model = Texts

    @classmethod
    def get_texts(cls):
        texts = cls.model.objects.all()
        answer = {}
        for text in texts:
            answer[text.title] = text.text

        return answer


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
            category: int,
            target_link='',
            price=0,
            was_advertised=False,
            what_after='',
            **kwargs
    ):
        return {
            'category_id': category,
            'target_link': target_link,
            'price': price,
            'was_advertised': was_advertised,
            'what_after': what_after,
        }