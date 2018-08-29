# Insight Data Engineering Coding Challenge

A Python2.7 solution to the Insight Data Engineering coding challenge (Aug 2018).  The challenge was to calculate average error of stock price for all matched pairs in two files over a user-defined time window.

## Summary

The code can process the valid sample file containing 99 stocks in 1440 hours in around one second on a Macbook Air with 8GB of RAM, 1.8 GHz Intel Core i5. It could process ugly dataset, like missing one or more field of infomation in a line, input typo of stock prices, one empty line in the middle of the file, window size is larger than the actual hours, etc. 

### Feature:

* actual hours can start from any integer hour(>0). For instance, actual hour can be in range(144, 1440).
* predicted hours can be outside of actual hours. For instance, predicted hour can be in range(2, 6) while actual hour is ranging (2, 5).
* stock ids in each hour presented in actual.txt and predicted.txt can have different order.
* both actual and predicted data can have missing hours.

### Complexity:

Given that n represents number of hours and m represents number of stocks, time complexity is `O(nm)`, space complexity is `O(nm)`.

### Assumption:

* There are much less missing hours in both actual.txt and predicted.txt, comparing to the entire hour range.
* First line in actual.txt and predicted.txt is non empty, with the first field read as integer.
* All stock ids and stock prices in actual.txt and predicted.txt, can be memorized by a single machine.  

## Description

My main idea was to use `unordered map` (Dictionary in Python Implementation) to store actual and predicted stock prices. I used stock id as keys and a 2D nested list as values, in which it consists of stock price time series from actual.txt and predicted.txt. 

## Dependencies

- sys (standard Python module to obtain command line argument.)
- Python 2.7

## Exectuion

To execute the code use the _run.sh_ script.

	./run.sh


Or you can simply go to ./src/ and execute the _prediction-validation.py_ script with 4 command line options.

	cd ./src/
	python prediction-validation.py <path to window.txt> <path to actual.txt> <path to predicted.txt> <path to comparison.txt>


## Tests

Additional tests have been added in the _insight\_testsuite/tests_ folder. Those can be run by executing the _run\_tests.sh_ script.  

	cd ./insight_testsuite/
	bash run_tests.sh


