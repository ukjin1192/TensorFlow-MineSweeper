## Summary

- Proof of concept for using TensorFlow to improve AI at <a href="https://minemine.io">this Minesweeper game</a>

## Procedure

- Create map randomly
- Sweep empty block for the first time
- Sweep or flag cells with given condition
- Pick random cell if there is no cell that could be revealed with given condition
  - Target
	  - Unrevealed cell which has at least one revealed number cell(=not empty or mine) around
	- X data
		- Sum of probabilities
		- Number of mines around
		- Number of revealed cells around
		- Number of unrevealed cell around
	- Y data
		- 0 or 1 (Mine exists or not)
	- Method
	  - Supervised Learning
		- Logistic classification
  - Optimization
	  - Use ReLu rather than Sigmoid
		- Data initialization
		- Dropout rate = 0.7
		- Learning rate = 0.01
- Training sets : Repeat above procedure to minimize error
- Test sets : Measure accuracy of model with machine learning

## Result (TBD)

- After 1000 training sets, average accuracy ~= N(%)
