import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import math
import sys

USAGE_THRESHOLD = 25. # Percent usage value below which a job will be flagged
TIME_THRESHOLD = dt.timedelta(minutes=5) # Run time below which job will be ignored
REQUESTED_THRESHOLD = 50

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def main():
    in_path = sys.argv[1]
    pd.set_option('display.max_rows', 9999)
    df = pd.read_csv(in_path)
    for (column_name, column_data) in df.items():
        if column_name == "Time":
            continue
        if np.nanmax(column_data.values) > USAGE_THRESHOLD:
            df.drop(columns=column_name, inplace=True)

    print("\nDropped")
    for (column_name, column_data) in df.items():
        if column_name == "Time":
            continue
        
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
        time = time_end - time_start
        if time < TIME_THRESHOLD:
            df.drop(columns = column_name, inplace=True)

    for (column_name, column_data) in df.items():
        if column_name == "Time":
            continue
        print(f'{column_name}: {np.nanmax(column_data.values)}')

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
        print(f'\t{row_start}, {row_end}')
        if running:
            print('\trunning')

        times = df.get("Time")
        time_start = datetime.strptime(times[row_start], TIME_FORMAT)
        time_end = datetime.strptime(times[row_end], TIME_FORMAT)
        time = time_end - time_start
        print(f'\t{time}')


if __name__ == "__main__":
    main()
