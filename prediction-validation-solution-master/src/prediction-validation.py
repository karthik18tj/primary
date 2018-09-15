import pandas as pd
import numpy as np
import sys
import os
import csv

pd.set_option('precision', 5)

def get_min_hour_value(df):
	'''
		Returns minimum hour value
	'''
	return min(df)


def get_max_hour_value(df):
	'''
		Returns maximum hour value
	'''
	return max(df)


def get_window_size(window):
	'''
		Reads window file
		Returns window size as integer
	'''
	with open(window, "r") as f:
		window_size = f.read()
		assert (len(window_size) == 1), "File contains more characters, something wrong"
		return int(window_size)


def get_actual_values(actual):
	'''
		Reads actual file
		Returns actual values as dataframe
	'''
	return pd.read_csv(actual, sep='|', header=None)


def get_predict_values(predict):
	'''
		Reads predict file
		Returns predict values as dataframe
	'''
	return pd.read_csv(predict, sep='|', header=None)


def calculate_error(actual_values, predict_values):
	'''
		Iterate through actual and predict values based on hours
		Subtract actual hours from predict hours and store it in error dictionary
		Returns error 
	'''
	error  = {}
	for current_hour in predict_values[0].unique(): # iterating through unique hours
		print("Calculating the error for {} hour".format(current_hour))	
		current_predict = predict_values[predict_values[0] == current_hour][[1,2]] # getting all predict values for choosen current_hour
		current_actual = actual_values[actual_values[0] == current_hour][[1,2]] # getting all actual values for choosen current_hour
		diff = current_actual.set_index(1).subtract(current_predict.set_index(1)).abs().dropna() # subtract the actual value from predict value
		error[current_hour] = np.round_(diff[2].values, decimals=2)
	return error


def calculate_average_error(error, min_hour, max_hour, window_size):
	'''
		Calculates average error for every time-window
		Returns a list of lists of average errors with time-window
	'''
	rows = []
	for current_hour in range(min_hour, max_hour + 1):
		if current_hour+window_size - 1 > max_hour:
			break
		if current_hour not in error.keys():
			continue
		sliding_window = current_hour
		total_error = None
		print("Calculating Average error for the time window {}|{}".format(current_hour, current_hour + window_size-1))
		for i in range(current_hour, current_hour + window_size, window_size - 1):
			if total_error is None:
				total_error = error[i]
				continue
			total_error = np.append(total_error, error[i])
			current_row = []
			current_row.extend( ( current_hour, current_hour + window_size -1, '{:.2f}'.format(np.round_(np.average(total_error), decimals=2)) ) )
			rows.append(current_row)
	return rows

def write_ouput(rows, output):
	'''
		Writes ouput to a file with delimiter '|'
	'''
	print(rows)
	with open(output, "w") as f:
	    writer = csv.writer(f, delimiter='|')
	    writer.writerows(rows)
	    print("Ouput file written to {}".format(output))


def run(window, actual, predicted, output):
	print("Processing Started.")
	window_size = get_window_size(window)
	actual_values = get_actual_values(actual)
	predict_values = get_predict_values(predict)
	error = calculate_error(actual_values, predict_values)
	rows = calculate_average_error(error, get_min_hour_value(actual_values[0]), get_max_hour_value(actual_values[0]), window_size)
	# rows = calculate_average_error(error, 299, 302, window_size)

	write_ouput(rows, output)
	print("Processing Completed.")


if __name__ == '__main__':
	window = sys.argv[1]
	actual = sys.argv[2]
	predict = sys.argv[3]
	output = sys.argv[4]
 
	run(window, actual, predict, output)