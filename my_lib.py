
# get current nifty strike
def current_strike(price):
    res = price % 50
    if res < 25:
        return price - res
    elif res > 25:
        return price-res+50


# get CE strike dropdwon list
def ce_strike_list(price):
    ce_strike = current_strike(price)
    ce_strike_list = []
    append_ce_string = 'CE'

    for i in range(1, 11):
        ce_strike_list.append(str(ce_strike + (i * 50)) + append_ce_string)

    return ce_strike_list


# get PE strike dropdwon list
def pe_strike_list(price):
    pe_strike = current_strike(price)
    pe_strike_list = []
    append_pee_string = 'PE'

    for i in range(1, 11):
        pe_strike_list.append(str(pe_strike - (i * 50)) + append_pee_string)

    return pe_strike_list


def day_name_list():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return days


def get_symbol(symbol):
    if symbol == 'BANKNIFTY':
        return 'NSE:NIFTYBANK-INDEX'
    elif symbol == 'NIFTY50':
        return 'NSE:NIFTY50-INDEX'
