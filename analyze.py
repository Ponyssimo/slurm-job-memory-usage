import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import math
import sys

USAGE_THRESHOLD = 25. # Percent usage value below which a job will be flagged
TIME_THRESHOLD = dt.timedelta(minutes=5) # Run time below which job will be ignored
REQUESTED_THRESHOLD = 1024 * 50

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def main():
    in_path = sys.argv[1]
    pd.set_option('display.max_rows', 9999)
    df = pd.read_csv(in_path)

    in_path = sys.argv[2]
    total_df = pd.read_csv(in_path)

    percent_row = 0
    amount_row = 0
    offset = 0

    percent_time = df.get("Time")
    amount_time = total_df.get("Time")

    while percent_time[percent_row] != amount_time[amount_row]:
        if percent_time[percent_row] < amount_time[amount_row]:
            percent_row += 1
        else:
            amount_row += 1
    offset = percent_row - amount_row

    for (column_name, column_data) in df.items():
        if column_name == "Time":
            continue

        if np.nanmax(column_data.values) > USAGE_THRESHOLD:
            df.drop(columns=column_name, inplace=True)
            continue

        time, running = runtime(df, column_data)

        if time < TIME_THRESHOLD:
            df.drop(columns = column_name, inplace=True)
            continue

        i = percent_row
        err = False
        while math.isnan(column_data[i]):
            i += 1
        amount_col = total_df.get(column_name)
        while amount_col[i - offset] == 0 or column_data[i] == 0:
            i += 1
            if i >= len(df.index) - 1 or i >= len(total_df.index) - offset - 1:
                err = True
                break
        if not err:
            mib_req = (amount_col[i - offset] / column_data[i]) * 100
            if mib_req < REQUESTED_THRESHOLD:
                df.drop(columns=column_name, inplace=True)
                continue

        print(f'{column_name}:')
        if running:
            print('\trunning')
        print(f'\t{np.nanmax(column_data.values)}% maximum usage')
        if not err:
            print(f'\t{mib_req / 1024:.2f} GiB requested')
        print(f'\t{time}')     

def runtime(df, column_data):
    i = 0
    row_start = None
    row_end = None
    running = False
    while math.isnan(column_data[i]):
        i += 1
    row_start = i
    while not math.isnan(column_data[i]):
        i += 1
        try:
            column_data[i]
        except:
            running = True
            break
    row_end = i - 1

    times = df.get("Time")
    time_start = datetime.strptime(times[row_start], TIME_FORMAT)
    time_end = datetime.strptime(times[row_end], TIME_FORMAT)
    return (time_end - time_start, running)

if __name__ == "__main__":
    main()
