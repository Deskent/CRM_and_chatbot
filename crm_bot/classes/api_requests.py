from decimal import Decimal, getcontext

from config import logger, settings
from classes.request_classes import PostRequest, GetRequest
from datastructurepack import DataStructure

getcontext().prec = 5
Litecoin = Decimal
Dollars = Decimal


class API:
    __BASE_SERVER_URL: str = settings.BASE_API_URL

    @classmethod
    @logger.catch
    async def _post_request(cls, data: dict, endpoint: str) -> 'DataStructure':
        """Отправляет запрос к АПИ и возвращает ответ."""

        url: str = cls.__BASE_SERVER_URL + endpoint
        logger.success(f'URL: {url}'
                       f'\nData: {data}')
        return await PostRequest(data=data, url=url).send_request()

    @classmethod
    @logger.catch
    async def _get_request(cls, endpoint: str) -> 'DataStructure':
        """Отправляет запрос к АПИ и возвращает ответ."""

        url: str = cls.__BASE_SERVER_URL + endpoint
        logger.success(f'URL: {url}')
        return await GetRequest(url=url).send_request()


class ProductAPI(API):
    """Класс для работы с АПИ продуктов"""

    __PRODUCTS_URL: str = '/product'

    @classmethod
    @logger.catch
    async def add_product(cls: 'ProductAPI', product_name: str) -> 'DataStructure':
        """Добавляет продукт в БД"""

        endpoint: str = cls.__PRODUCTS_URL + '/add_product'
        filename: str = product_name.lower().replace(' ', '_') + '_client'
        data = {
            "name": product_name,
            "filename": filename,
        }
        return await cls._post_request(data=data, endpoint=endpoint)

    @classmethod
    @logger.catch
    async def get_product(cls: 'ProductAPI', product_id: int) -> 'dict':
        """Добавляет продукт в БД"""

        endpoint: str = cls.__PRODUCTS_URL + f'/get_product/{product_id}'

        result: DataStructure = await cls._get_request(endpoint=endpoint)

        return result.data if result and result.data else {}

    @classmethod
    @logger.catch
    async def delete_product(cls: 'ProductAPI', **kwargs) -> 'DataStructure':
        """Удаляет продукт из БД"""

        endpoint: str = cls.__PRODUCTS_URL + '/delete_product'
        return await cls._post_request(data=kwargs, endpoint=endpoint)

    @classmethod
    @logger.catch
    async def get_all_products(cls: 'ProductAPI') -> list[dict]:
        """Возвращает список всех продуктов"""

        endpoint: str = cls.__PRODUCTS_URL + '/get_all_products'
        result: 'DataStructure' = await cls._get_request(endpoint=endpoint)

        return result.data if result and result.data else []

    @classmethod
    @logger.catch
    async def get_product_name(cls: 'ProductAPI', product_id: int) -> str:
        """Возвращает название товара по его pk"""

        product: dict = await cls.get_product(product_id=product_id)
        return product.get("name")


class LicenseAPI(API):
    """Класс для работы с АПИ лицензий"""

    __LICENSE_URL: str = '/license'

    @classmethod
    @logger.catch
    async def add_license_key(
            cls: 'LicenseAPI', telegram_id: int, license_key: str, product_id: int
    ) -> 'DataStructure':
        """Добавить лицензию для пользователя"""

        endpoint: str = cls.__LICENSE_URL + '/add_license_key'
        data = {
            "telegram_id": telegram_id,
            "product_id": product_id,
            "license_key": license_key,
        }
        return await cls._post_request(data=data, endpoint=endpoint)

    @classmethod
    @logger.catch
    async def confirm_license(
            cls: 'LicenseAPI', confirmed: bool, check_status_id: int, telegram_id: int
    ) -> 'DataStructure':
        """Сохраняет данные о том, что пользователь подтвердил лицензию в телеграме"""

        endpoint: str = cls.__LICENSE_URL
        data = {
            "check_status_id": check_status_id,
            "telegram_id": telegram_id
        }
        if confirmed:
            endpoint += '/confirm_license'
        else:
            endpoint += '/not_confirm_license'
        return await cls._post_request(data=data, endpoint=endpoint)


class WalletAPI(API):

    __WALLET_URL: str = '/wallet'

    @classmethod
    @logger.catch
    async def get_wallet(cls: 'WalletAPI', telegram_id: int) -> dict:

        endpoint: str = cls.__WALLET_URL + f'/get_wallet/{telegram_id}'
        result: 'DataStructure' = await cls._get_request(endpoint=endpoint)
        return result.data if result and result.success else {}

    @classmethod
    @logger.catch
    async def check_payment(
            cls: 'WalletAPI', telegram_id: int, price: str) -> 'DataStructure':
        """Отправляет запрос на ожидание платежа
        :returns

        result = {
            "balance_before": balance_before,
            "balance_after": balance_after,
        }
        """

        endpoint: str = cls.__WALLET_URL + '/check_payment'
        data = {
            "telegram_id": telegram_id,
            "price_ltc": price
        }
        return await cls._post_request(data=data, endpoint=endpoint)

    @staticmethod
    def get_wallet_name(telegram_id: int) -> str:
        return f"w{telegram_id}"


class UserAPI(API):
    """Класс для работы с АПИ лицензий"""

    __URL: str = '/users'

    @classmethod
    @logger.catch
    async def create_user(
            cls: 'UserAPI', telegram_id: int, nick_name: str) -> 'DataStructure':
        """Добавить пользователя"""

        endpoint: str = cls.__URL + '/create_user'
        data = {
            "telegram_id": telegram_id,
            "nick_name": nick_name,
        }
        return await cls._post_request(data=data, endpoint=endpoint)

    @classmethod
    @logger.catch
    async def buy_subscribe(
            cls: 'UserAPI', telegram_id: int) -> dict:
        """Купить подписку"""

        endpoint: str = cls.__URL + '/buy_subscribe'
        data = {
            "telegram_id": telegram_id,
        }
        result: 'DataStructure' = await cls._post_request(data=data, endpoint=endpoint)
        return result.data if result.success else {}

    @classmethod
    @logger.catch
    async def buy_subscription(
            cls: 'UserAPI', telegram_id: int) -> dict:
        """Купить подписку"""

        endpoint: str = cls.__URL + '/buy_subscription'
        data = {
            "telegram_id": telegram_id,
        }
        result: 'DataStructure' = await cls._post_request(data=data, endpoint=endpoint)
        return result.data if result.success else {}

    @classmethod
    @logger.catch
    async def activate_user(
            cls: 'UserAPI', telegram_id: int) -> dict:
        """Активировать пользователя"""

        endpoint: str = cls.__URL + '/activate_user'
        data = {
            "telegram_id": telegram_id,
        }
        result: 'DataStructure' = await cls._post_request(data=data, endpoint=endpoint)
        return result.data if result.success else {}

    @classmethod
    @logger.catch
    async def get_user_licenses_info(
            cls: 'UserAPI', telegram_id: int) -> dict:
        """Активировать пользователя"""

        endpoint: str = cls.__URL + '/get_user_licenses_info'
        data = {
            "telegram_id": telegram_id,
        }
        result: 'DataStructure' = await cls._post_request(data=data, endpoint=endpoint)
        return result.data

    @classmethod
    @logger.catch
    async def set_user_admin(
            cls: 'UserAPI', telegram_id: int) -> dict:
        """Активировать пользователя"""

        endpoint: str = cls.__URL + '/set_user_admin'
        data = {
            "telegram_id": telegram_id,
        }
        result: 'DataStructure' = await cls._post_request(data=data, endpoint=endpoint)
        return result.data

    @classmethod
    @logger.catch
    async def get_user_status(
            cls: 'UserAPI', telegram_id: int) -> dict:
        """Активировать пользователя"""

        endpoint: str = cls.__URL + '/get_user_status'
        data = {
            "telegram_id": telegram_id,
        }
        result: 'DataStructure' = await cls._post_request(data=data, endpoint=endpoint)
        return result.data

    @classmethod
    @logger.catch
    async def get_active_users(cls: 'UserAPI') -> list[dict]:
        """Получить список пользователей которые могут находиться в чате"""

        endpoint: str = cls.__URL + '/get_active_users'
        result: 'DataStructure' = await cls._get_request(endpoint=endpoint)
        return result.data


class ServiceAPI(API):
    """Класс для работы с служебным АПИ """

    __URL: str = '/service'

    @classmethod
    @logger.catch
    async def add_channel(
            cls: 'ServiceAPI', chat_id: int, name: str) -> 'DataStructure':
        """Добавить канал"""

        endpoint: str = cls.__URL + '/add_channel'
        data = {
            "chat_id": chat_id,
            "name": name,
        }
        return await cls._post_request(data=data, endpoint=endpoint)

    @classmethod
    @logger.catch
    async def get_channels(cls: 'ServiceAPI') -> list[dict]:
        """Получить список каналов"""

        endpoint: str = cls.__URL + '/get_channels'
        data = await cls._get_request(endpoint=endpoint)
        result: list[dict] = data.data.get('result', [])
        return result
