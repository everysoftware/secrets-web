from aiogram.types import BotCommand

BOT_COMMAND_LIST = (
    ("start", "Запустить бота"),
    ("suggest", "Предложить пароль"),
    ("logout", "Выйти"),
    ("help", "Помощь"),
    ("about", "О боте"),
)

BOT_COMMANDS = [
    BotCommand(command=name, description=desc) for name, desc in BOT_COMMAND_LIST
]

BOT_COMMANDS_STR = "\n".join("/" + (" - ".join(cmd)) for cmd in BOT_COMMAND_LIST)
