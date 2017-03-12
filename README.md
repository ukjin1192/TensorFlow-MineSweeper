## Summary

- Proof of concept for using TensorFlow to improve AI at <a href="https://minemine.io">this Minesweeper game</a>
- Mission : Improve accuracy(=predictive power) when AI should sweep or flag random cell with given condition

## Procedure

- Create map randomly
- Sweep empty block for the first time
- Sweep or flag cells if AI could sweep or flag certain cell with given condition
- Collect data when AI should sweep or flag random cell with given condition
  - Target
	  - Unrevealed cell which has at least one revealed number cell(=not empty or mine) around
	- X data
		- Sum of probabilities
		- Number of revealed mines around
		- Number of revealed cells around
		- Number of unrevealed cell around
	- Y data
		- 0 or 1 (Mine exists or not)
	- Method
	  - Supervised Learning
		- Logistic classification
  - Optimization
		- Data initialization
		- Learning rate = 0.1
	  - Use ReLu rather than Sigmoid
		- Dropout rate = 0.7
- Get data set : Repeat above procedure many times to get big data
- Training sets : Create reliable model with machine learning
- Test sets : Measure accuracy of model

## Prerequisite

- Python 3
- Numpy
- TensorFlow

## Command

~~~~
$ python3 ai.py
~~~~

## Result

- Collect data with 1000 games
- 2000 training sets
- (With test sets) Accuracy ~= 87(%)
