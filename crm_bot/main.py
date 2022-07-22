import logging

from aiogram import executor
from config import bot, dp, settings
from _resources import __appname__, __build__, __version__

from handlers.main_handlers import register_main_handlers
from handlers.cancel_handler import register_cancel_handlers
from handlers.worksheet_handlers import register_worksheet_handlers

register_cancel_handlers(dp=dp)
register_worksheet_handlers(dp=dp)
register_main_handlers(dp=dp)

logger = logging.getLogger(__name__)


async def send_report_to_admins(text: str) -> None:
    for admin in settings.ADMINS:
        try:
            await bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logger.error(f'{err} chat_id={admin}')


async def on_startup(_):
    """Функция выполняющаяся при старте бота."""

    text: str = (
        f"{__appname__} started."
        f"\nBuild: {__build__}"
        f"\nVersion: {__version__}"
        f"\nStage: {settings.STAGE}"
    )
    if settings.DEBUG:
        text += "\nDEBUG = TRUE"
    try:
        await send_report_to_admins(text)
    except Exception as err:
        logger.error(err)
    logger.info(f'Bot started {__appname__}')


async def on_shutdown(dp) -> None:
    try:
        await send_report_to_admins(f'bot {__appname__} shutdown')
    except Exception:
        pass
    logger.info(f'Bot {__appname__} shutdown')
    await dp.storage.wait_closed()


def start_bot() -> None:
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )


if __name__ == '__main__':
    start_bot()
