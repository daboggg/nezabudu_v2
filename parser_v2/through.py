import re

from datetime import datetime
from dateutil.relativedelta import relativedelta

from parser_v2.data import through_data


# выделяет временные метки из сообщения
def extract_date__time(message: str) -> tuple[str, dict[str, int]]:
    # словарь для значений времени {"year": 2, ...}
    tmp_dict = dict()

    parts_of_time = through_data.keys()

    for part_of_time in parts_of_time:
        variants = through_data.get(part_of_time)
        pattern = f".*?(?P<num>(\d+)?(^|\W)({'|'.join(variants)})).*"
        try:
            result = re.fullmatch(pattern, message)
            match_found = result.group("num").strip()
            match_found_list = match_found.split(" ")
            if len(match_found_list) == 2:
                tmp_dict[part_of_time] = int(match_found_list[0])
            else:
                tmp_dict[part_of_time] = 1
            message = message.replace(match_found, "")
        except Exception as e:
            pass

    # удаляю лишние пробелы из строки
    message = " ".join(re.split("\s+", message.strip()))

    return message, tmp_dict


def create_datetime(date__time_dict: dict[str, int]) -> datetime:
    return datetime.now() + relativedelta(**date__time_dict)


def start(message: str) -> dict[str, str | dict[str, datetime]]:
    msg, date__time_dict = extract_date__time(message)
    return {
        "params": {"run_date": create_datetime(date__time_dict)},
        "msg": msg
    }


if __name__ == '__main__':
    print(start("все равно через 26 минут, 8 недель 58 любой! текстЖ 85, месяц день 3 года  никого не поймают"))
