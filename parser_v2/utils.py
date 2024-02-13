import re


# удаляет все лишние пробелы в начале, середине и конце строки
def remove_extra_spaces(message: str) -> str:
    return " ".join(re.split("\s+", message.strip()))
