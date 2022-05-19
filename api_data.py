
# get nifty data between two date range
def nifty_date_range_data(range_from, range_to, selected_day, selected_symbol):
    model = get_fyers_model()
    tiker = {"symbol": selected_symbol, "resolution": "D", "date_format": "1",
             "range_from": range_from, "range_to": range_to, "cont_flag": "1"}

    data = model.history(tiker)

    cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame.from_dict(data['candles'])

    df.columns = cols
    df['Date'] = pd.to_datetime(df['Date'], unit='s')

    df['Date'] = df['Date'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    df['Date'] = df['Date'].dt.tz_localize(None)
    df['Day'] = df['Date'].dt.day_name()
    df['Date'] = df['Date'].dt.strftime('%d-%b-%Y')

    df['Range'] = df['High'] - df['Low']
    df['Previou Close'] = df['Close'].shift()
    df['Gap Up/Down'] = df['Open'] - df['Previou Close']
    df['Day Result'] = df['Close'] - df['Previou Close']
    df['Price Move'] = df['Open'] - df['Close']
    df['Gap Up/Down'] = df['Open'] - df['Previou Close']

    df['Gap %'] = (df['Gap Up/Down'] * 100) / df['Previou Close']

    df = df[['Day', 'Date', 'Previou Close', 'Gap Up/Down', 'Gap %', 'Open',
             'Close', 'Day Result', 'Price Move', 'Range']]

    df = df.set_index('Date')

    return df.loc[df['Day'].isin(selected_day)]

# get nifty data between two date range with 5 min time frame


def nifty_date_range_data_5_min(range_from, range_to, selected_day, selected_symbol, entry_time, exit_time):
    model = get_fyers_model()
    tiker = {"symbol": selected_symbol, "resolution": "5", "date_format": "1",
             "range_from": range_from, "range_to": range_to, "cont_flag": "1"}

    data = model.history(tiker)

    cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame.from_dict(data['candles'])

    df.columns = cols
    df['Date'] = pd.to_datetime(df['Date'], unit='s')

    df['Date'] = df['Date'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    df['Date'] = df['Date'].dt.tz_localize(None)
    df['Day'] = df['Date'].dt.day_name()
    df['Time'] = df['Date'].dt.strftime('%H:%M')
    df['Date'] = df['Date'].dt.strftime('%d-%b-%Y')

    df = df[['Day', 'Date', 'Open', 'Close', 'Time']]

    selected_time = [entry_time, exit_time]

    df = df.set_index('Date')

    result = df.loc[df['Day'].isin(
        selected_day) & df['Time'].isin(selected_time)]

    data_entry = pd.DataFrame(result.iloc[::2])
    data_entry.reset_index(inplace=True)

    data_exit = pd.DataFrame(result[1::2])
    data_exit.reset_index(inplace=True)

    data_entry['Entry Time'] = data_entry['Time']
    data_entry['Exit Time'] = data_exit['Time']
    data_entry['Close'] = data_exit['Close']
    data_entry['Price Move'] = data_entry['Close'] - data_entry['Open']
    data_entry['% Change'] = (
        (data_entry['Price Move'] * 100) / data_entry['Open']).round(2)

    data_entry = data_entry[['Date', 'Day', 'Entry Time',
                             'Exit Time', 'Open', 'Close', 'Price Move', '% Change']]

    return data_entry


# get nifty data between two date range for gap up / gap down report
def nifty_date_range_data_gap_report(range_from, range_to, selected_day, selected_symbol):
    model = get_fyers_model()
    tiker = {"symbol": selected_symbol, "resolution": "D", "date_format": "1",
             "range_from": range_from, "range_to": range_to, "cont_flag": "1"}

    data = model.history(tiker)

    cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    df = pd.DataFrame.from_dict(data['candles'])

    df.columns = cols
    df['Date'] = pd.to_datetime(df['Date'], unit='s')

    df['Date'] = df['Date'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    df['Date'] = df['Date'].dt.tz_localize(None)
    df['Day'] = df['Date'].dt.day_name()
    df['Date'] = df['Date'].dt.strftime('%d-%b-%Y')

    df['Range'] = df['High'] - df['Low']
    df['Previou Close'] = df['Close'].shift()

    df['Gap Up/Down'] = df['Open'] - df['Previou Close']
    df['Day Result'] = df['Close'] - df['Previou Close']

    df = df[['Day', 'Date', 'Gap Up/Down', 'Day Result', 'Range']]

    df = df.set_index('Date')

    return df.loc[df['Day'].isin(selected_day)]
