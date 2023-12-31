import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler,
                                            setup_application)
from aiohttp import web

from app.cache import Cache
from app.core import get_async_engine, get_async_session_maker
from core.config import cfg
from .dispatcher import create_dispatcher, create_redis_storage


def start_polling(bot: Bot, dp: Dispatcher) -> None:
    asyncio.run(dp.start_polling(bot))


def start_webhook(bot: Bot, dp: Dispatcher) -> None:
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot, secret_token=dp["secret_token"]
    )

    webhook_requests_handler.register(app, path=cfg.webhook.path)
    setup_application(app, dp, bot=bot)

    web.run_app(app, host=cfg.webhook.host, port=cfg.webhook.port)


def main() -> None:
    logging.basicConfig(level=cfg.logging_level, stream=sys.stdout)

    bot = Bot(cfg.bot.tg_token, parse_mode="HTML")
    cache = Cache()
    storage = create_redis_storage(cache.client)
    pool = get_async_session_maker(get_async_engine(cfg.dsl))
    dp = create_dispatcher(storage, cache, pool)

    if cfg.webhook.on:
        start_webhook(bot, dp)
    else:
        start_polling(bot, dp)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
