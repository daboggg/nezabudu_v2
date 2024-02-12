from datetime import datetime

import through


def start(reminder_str: str):
    if reminder_str.endswith("."): reminder_str = reminder_str[:-1]


    if "через" in reminder_str:
        reminder_str = reminder_str.replace("через", "")
        result = through.start(reminder_str)
        result["params"]["trigger"] = "date"
        return result
    else:
        pass


if __name__ == '__main__':
    print(start("все равно через 26 минут, 8 недель 58 любой! текстЖ 85, месяц день 3 года  никого не поймают."))
