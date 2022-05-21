def day_name_list():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return days


def covert_to_short_number(number):
    return numerize.numerize(number, 2)


def number_to_month(number):
    number = int(number)
    if number <= 12:
        month_name_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May',
                           'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return month_name_list[number-1]
    else:
        return 'Wrong Input'
