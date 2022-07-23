from decimal import Decimal, getcontext

from classes.bot_texts import BotTexts
from config import logger, settings, bot_texts
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


class UserAPI(API):
    """Класс для работы с АПИ пользователя"""

    __URL: str = ''

    @classmethod
    @logger.catch
    async def send_worksheet(cls: 'UserAPI', userdata: dict) -> 'DataStructure':
        """Отправить анкету"""

        endpoint: str = cls.__URL + '/send_worksheet'
        data = {
            "worksheet": userdata
        }
        return await cls._post_request(data=data, endpoint=endpoint)

    @classmethod
    @logger.catch
    async def get_texts(cls: 'UserAPI') -> bool:
        """Обновить тексты"""

        endpoint: str = cls.__URL + '/get_texts'

        result: 'DataStructure' = await cls._get_request(endpoint=endpoint)
        if result and result.success and result.data:
            bot_texts.update_all(result.data)
            return True

    @classmethod
    @logger.catch
    async def get_categories(cls: 'UserAPI') -> dict:
        """Получить категории"""

        endpoint: str = cls.__URL + '/get_categories'

        result: 'DataStructure' = await cls._get_request(endpoint=endpoint)
        return result.data if result else {}