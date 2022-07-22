import logging

from aiogram import executor
from config import bot, dp, admins, NAME_PROJECT

from handlers import register_handlers
register_handlers(dp=dp)

logger = logging.getLogger(__name__)


async def send_report_to_admins(text: str) -> None:
    for admin in admins:
        try:
            await bot.send_message(chat_id=admin, text=text)
        except Exception as err:
            logger.error(f'{err} chat_id={admin}')


async def on_startup(_):
    try:
        await send_report_to_admins(f'bot {NAME_PROJECT} started')
    except Exception as err:
        logger.error(err)
    logger.info(f'Bot started {NAME_PROJECT}')


async def on_shutdown(dp) -> None:
    try:
        await send_report_to_admins(f'bot {NAME_PROJECT} shutdown')
    except Exception:
        pass
    logger.info(f'Bot {NAME_PROJECT} shutdown')
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
