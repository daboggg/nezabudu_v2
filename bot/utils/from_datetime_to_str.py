from datetime import datetime

months = ["","января","февраля","марта","апреля",
          "мая","июня","июля","августа","сентября",
          "октября","ноября","декабря",]

day_of_week = ["в понедельник","во вторник","в среду","в четверг",
               "в пятницу","в субботу","в воскресенье",]

def datetime_to_str(date: datetime):
    return f"{date.day} {months[date.month]} {date.year} г. ({day_of_week[date.weekday()]}) в {date.hour}:{date.minute}"

