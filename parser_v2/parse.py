import logging

import through

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start(reminder_str: str) -> dict[str, str | dict]:
    if reminder_str.endswith("."): reminder_str = reminder_str[:-1]

    if "через" in reminder_str:
        reminder_str = reminder_str.replace("через", "")
        result = through.start(reminder_str)
        result["params"]["trigger"] = "date"
        logger.info(f"возвращенное из парсера значение: {result}")
        return result
    else:
        pass


if __name__ == '__main__':
    start("все равно через 8 лет 7 дней  никого не поймают 8 минут.")
