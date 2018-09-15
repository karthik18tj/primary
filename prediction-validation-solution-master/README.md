# Table of Contents
1. [Introduction](README.md#introduction)
1. [Problem Summary](README.md#problem-summary)
1. [Details of the problem](README.md#details-of-problem)
1. [Input files](README.md#input-files)
1. [Output file](README.md#output-file)
1. [Example](README.md#example)



## Introduction

You are a data engineer working at a financial institution that analyzes real-time stock market data. To determine the best trading strategy, the company's data scientists created a machine learning model to predict the future price of a stock every hour, and they want to test it on real-time stock data.

Before deploying the model, they want you to help test how accurate their predictions are over time by comparing their predictions with newly arriving real-time stock prices.


## Problem Summary

You will read two different files, one provides the actual value of each stock every hour and the second lists the predicted value of various stocks at a certain hour during the same time period.

You will obtain the `average error` by calculating the average difference between the actual stock prices and predicted values over a specified sliding time window.


## Details of problem

You are given the following input files

1. `actual.txt`: A time-ordered file listing the actual value of stocks at a given hour.
1. `predicted.txt`: A time-ordered file of the predicted value of certain stocks at a given hour. 
1. `window.txt`: Holds a single integer value denoting the window size (in hours) for which you must calculate the `average error`.

You may have multiple stocks for the same hour. While stock prices in the real world can change every second, for the purposes of this challenge, you can assume they only change every hour.

You are expected to produce the following output file

1. `comparison.txt`: A time-ordered file containing the average error of stock predictions for a certain time period


### How are the predictions made?

The data scientists have trained a complex model to predict the price of every stock at a given time. They have set thresholds on how confident their predictions are and filtered out predictions that have a low confidence value. The file,`predicted.txt`, contains only **high confidence predictions**.


### Calculations

To compute the average error in a given time window, find the absolute difference between the actual and predicted values of every matched stock and time pair. Let's call this result `error`. You then compute the average of all errors within a certain time window to get the `average error`.

To better gauge the algorithm's performance, you are asked to compute this `average error` over a sliding window, moving one hour at a time until the end of the file.


## Input Files

Lines in both input files, `actual.txt` and `predicted.txt`, are listed in chronological order. Both contain the following pipe-delimited fields: 

* `time`: An integer greater than 0 designating the hour.
* `stock`: ID of a stock 
* `price`: Price of a given stock at the given hour.

The file, `window.txt`, will contain one value (an integer greater than 0), specifying the size of the sliding window in hours.


### Input file considerations

For this challenge, you may assume the following:

1. No headers for any file.
2. Sliding window values are inclusive (e.g., a sliding window of 2 would include data at hour 5 and hour 6)
1. Stocks prices are ordered by time (e.g., the price for a particular stock id `BJKRRX` at hour `100` will **NOT** appear in the file before hour `50`.

You should **NOT** assume that the stock ids will ever be sorted.

## Output File

You must create an output file named `comparison.txt` where each line has the following pipe-delimited fields:

1. Starting hour time window
1. Ending hour time window
1. `average error` rounded off to 2 decimal places. Given rounding issues some applicants have run into, we're going to accept values that are +/- 0.01 of the expected value. For example, if the expected value is 0.17, we will accept 0.16, 0.17, or 0.18 as the correct answer.

The output file also has no headers and the lines should be listed in chronological order.

## Example

To make reading the below example easier, there is a new line between each hour of information in `actual.txt` and `predicted.txt`. There will **NOT** be that extra new line in the actual input files we'll test your code on.

##### window.txt
```
2
```

##### actual.txt
```
1|SLKWVA|94.51
1|CMWTQH|81.27
1|ATAYJP|25.74
1|HVIWZR|22.81

2|ATAYJP|29.62
2|SLKWVA|81.87
2|CMWTQH|116.11
2|HVIWZR|22.15

3|ATAYJP|21.93
3|HVIWZR|22.24
3|SLKWVA|78.01
3|CMWTQH|113.63

```


##### predicted.txt
```
1|ATAYJP|25.71
1|HVIWZR|22.80
1|SLKWVA|94.49
1|CMWTQH|81.22

2|ATAYJP|29.92
2|HVIWZR|22.06

3|ATAYJP|21.84
3|HVIWZR|22.36
3|SLKWVA|79.49

```


This example provides the value for stocks `SLKWVA`, `CMWTQH`, `ATAYJP` and `HVIWZR` for hours `1, 2 and 3`.

You have noticed that the predicted file is shorter than the actual file. This is because it only contains high confidence predictions. 

In this example, because `window.txt` contains the value `2`, we will compute the `average error` over two hour time windows. 

We compare every stock and time pair in `actual.txt` with its companion in `predicted.txt` and calculate the `error` between them. If we do not have a match for a stock at a particular time, we ignore the row and continue. 

Below is an example of that comparison:

#### Time window: `1 to 2`
```
actual              predicted           error
1|ATAYJP|25.74      1|ATAYJP|25.71      0.03
1|SLKWVA|94.51      1|SLKWVA|94.49      0.02
1|CMWTQH|81.27      1|CMWTQH|81.22      0.05
1|HVIWZR|22.81      1|HVIWZR|22.80      0.01
2|SLKWVA|81.87      no data present     ignore
2|ATAYJP|29.62      2|ATAYJP|29.92      0.30
2|HVIWZR|22.15      2|HVIWZR|22.06      0.09
2|CMWTQH|116.11     no data present     ignore
```

#### Time window: `2 to 3`
```
actual              predicted           error
2|SLKWVA|81.87      no data present     ignore
2|ATAYJP|29.62      2|ATAYJP|29.92      0.30
2|HVIWZR|22.15      2|HVIWZR|22.06      0.09
2|CMWTQH|116.11     no data present     ignore
3|ATAYJP|21.93      3|ATAYJP|21.84      0.09
3|HVIWZR|22.24      3|HVIWZR|22.36      0.12
3|SLKWVA|78.01      3|SLKWVA|79.49      1.48
3|CMWTQH|113.63     no data present     ignore
```

### Calculating average error

We take the average of the error for each time window ignoring those entries that have no data present in `predicted.txt`. 

For the first time window, the `average error` is `0.08` or `(0.03 + 0.02 + 0.05 + 0.01 + 0.30 + 0.09)/6` 

And for the second time window, the `average error` is `0.42` or `(0.30 + 0.09 + 0.09 + 0.12 + 1.48)/5`

The results would be written to the output file as seen below. 

##### comparison.txt
```
1|2|0.08
2|3|0.42
```


Happy coding!


