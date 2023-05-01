WEEKDAYS = {
    1: "Понедельник",
    2: "Вторник",
    3: "Среда",
    4: "Четверг",
    5: "Пятница",
    6: "Суббота",
    7: "Воскресенье"
}


def convert_weekdays(day_numbers: list | tuple, weekdays_dict=None):
    if weekdays_dict is None:
        weekdays_dict = WEEKDAYS
    days = []
    for day_number in day_numbers:
        if isinstance(day_number, int) or isinstance(day_number, str):
            if int(day_number) in weekdays_dict.keys():
                days.append(
                    weekdays_dict[int(day_number)]
                )
            else:
                continue
        else:
            continue
    return days
