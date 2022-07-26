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

        return await cls._post_request(data=userdata, endpoint=endpoint)

    @classmethod
    @logger.catch
    async def get_texts(cls: 'UserAPI') -> bool:
        """Обновить тексты"""

        endpoint: str = cls.__URL + '/get_texts'

        result: 'DataStructure' = await cls._get_request(endpoint=endpoint)
        if result and result.status == 200 and result.data:
            bot_texts.update_all(result.data)
            return True

    @classmethod
    @logger.catch
    async def get_categories(cls: 'UserAPI') -> dict[int, str]:
        """Получить категории"""

        endpoint: str = cls.__URL + '/get_categories'

        result: 'DataStructure' = await cls._get_request(endpoint=endpoint)
        if result and result.status == 200 and result.data:
            return result.data
        logger.warning(f'Categories getting error: {result}')
        return {}

    @classmethod
    @logger.catch
    async def get_poll_by_category(cls: 'UserAPI', category_id: int) -> list[str]:
        """Получить список вопросов для категории отсортированный по порядку,
         в котором их нужно задавать"""

        endpoint: str = cls.__URL + f'/get_poll_by_category/{category_id}'

        result: 'DataStructure' = await cls._get_request(endpoint=endpoint)
        if result and result.status == 200 and result.data:
            return result.data
        logger.warning(f'Poll getting error: {result}')
        return []
