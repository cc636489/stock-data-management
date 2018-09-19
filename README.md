# An object-oriented programming solution to compute average error between actual and predicted stock prices. 

Before deploying a machine learning model for predicting real-time stock market data, it's necessary to know how accurate our predictions are over time by comparing our predictions with newly arriving real-time stock prices. This program was designed on the purpose of calculating average error of stock price in data streams.

## Description

The idea was to use `unordered map` (Dictionary in Python Implementation) to store actual and predicted stock prices. 

### data structure:
	key: stock id
	value: 
		double-ended queue[0] for storing [hour, price] pair in actual.txt
		double-ended queue[1] for storing [hour, price] pair in predicted.txt

### control flow chart:
	
* read in one window size of data from actual.txt, keep track of the breakline information, save into gap_line
* read in one window size of data from predicted.txt, keep track of the breakline information, save into gap_line
* calculate all the possible output inside this current window.(edge case: there is large hour gap inside actual.txt)
* write the calculated average error into output file.
* update window start/end information.
* pop out all not-in-the-window data.
* append gap_line information last. 

### Complexity:

Given that n represents number of hours,  m represents number of stocks, k represents the window size:
time complexity is `O(nm)`, space complexity is `O(km)`.

### Feature:

* actual hours can start from any integer hour(>0). For instance, actual hour can be in range(144, 1440).
* predicted hours can be outside of actual hours. For instance, predicted hour can be in range(2, 6) while actual hour is ranging (2, 5).
* stock ids in each hour presented in actual.txt and predicted.txt can have different order.
* both actual and predicted data can have missing hours.

## Dependencies

- import sys (standard Python module to obtain command line argument.)
- from collections import deque (for high performance Python data structure.)
- Python 2.7

## Exectuion

To execute the code use the `run.sh` script.

	./run.sh


## Tests

6 Additional tests have been added in the _insight\_testsuite/tests_ folder. Those can be run by executing the _run\_tests.sh_ script.  

	cd ./insight_testsuite/
	bash run_tests.sh


Or you can go to ./src/, run `test_all.py`

	cd ./src/
	python test_all.py

