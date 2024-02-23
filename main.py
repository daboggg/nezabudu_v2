import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.comands import set_commands
from bot.handlers.cmd import cmd_router
from bot.handlers.main_handlers import main_handler
from bot.middlewares.apschedmiddleware import SchedulerMiddleware
from db.db_helper import db_helper
from settings import settings


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')


scheduler: AsyncIOScheduler


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')
    scheduler.shutdown()

async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s - %(name)s - '
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'

                        )
    logger = logging.getLogger(__name__)

    # Создаю и запускаю шедулер
    global scheduler
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    # слушатель на событие удаления job
    # scheduler.add_listener(delete_remind_from_db, apscheduler.events.EVENT_JOB_REMOVED)
    scheduler.start()

    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    # восстановление заданий при старте из базы данных
    # await recovery_job_to_scheduler(scheduler, bot)

    storage = MemoryStorage()
    dp = Dispatcher(storage=storage, session=db_helper.get_scoped_session())

    # регистрация middlewares
    dp.update.middleware.register(SchedulerMiddleware(scheduler))

    # подключение роутеров
    dp.include_routers(
        cmd_router,
        main_handler,
    )

    # подключение диалогов
    setup_dialogs(dp)

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    logger.info('start')


    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
