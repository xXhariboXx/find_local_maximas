# -*- coding: utf-8 -*-
"""
@author: dnowak
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import lfilter


"""
Opening JSON file

"""

# file_path = input('Enter a file path in format: C:/xxx/xxx/data.json: ')
file = open(r"E:\GIT foldery\dnowka\data.json")


# file = open("") # if you want use directly path use this line


json_data = json.load(file)

new_dict = {}
for item in json_data:
    time = item.pop("time")
    data = item.pop("data")
    new_dict[time, data] = item

keysList = list(new_dict.keys())

Time = [x[0] for x in keysList]
Data = [x[1] for x in keysList]

time_data = list(zip(Time, Data))

time_data_arr = np.asarray(time_data)

plt.plot(Time, Data)

"""
Data smoothing

"""

window_size = 3
i = 0

# Initialize an empty list to store moving averages
moving_averages = []

# Loop with moving average procedure
while i < len(Data) - window_size + 3:

    # Calculate the average of current window
    window_average = round(np.sum(Data[i : i + window_size]) / window_size, 2)

    # Store the average
    moving_averages.append(window_average)

    # Shift window to right by one position
    i += 1

# plt.plot(Time,moving_averages)

time_arr = np.asarray(Time)
data_arr = np.asanyarray(Data)

"""
Smoother

"""
n = 11
b = [1.0 / n] * n
a = 1
moving_averages_smooth = lfilter(b, a, moving_averages)

# plot of smoothing data
plt.plot(time_arr, moving_averages_smooth)

"""
Local Maximum

"""
moving_averages_smooth = np.array(moving_averages_smooth)
result_index = argrelextrema(data_arr, np.greater, order=5)
print(result_index)
result_data = moving_averages_smooth[argrelextrema(moving_averages_smooth, np.greater)[0]]

"""
Ordering results

"""

result_time = time_arr[result_index]

result = list(zip(result_time, result_data))

plt.plot(result_time, result_data, "o", color="red")
plt.show()

Result = str(result)

"""
Saving results

"""
# result_path = input('Enter a result path: ')
# with open(result_path, 'w') as f:
# f.write(Result)
