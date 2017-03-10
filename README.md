## Summary 

- Create map randomly
- Sweep empty block for the first time
- Sweep or flag cells with given condition
- AI should pick random cell if there is no cell that could be revealed with given condition
  - Target : Revealed 'number' cells which has at least one unrevealed cell locally
	- Varaibles : 'Sum of probabilities', '# of mines around', '# of revealed cells around', '# of unrevealed cell around'
	- Supervised Learning : Compare with real data
	- Logistic classification : Determine that mine exists or not
  - Optimization
	  - Use ReLu rather than Sigmoid
		- Data initialization
		- Dropout rate = 0.7
		- Learning rate = 0.01
- Training sets : Repeat above procedure to minimize error
- Test sets : Measure accuracy of model with machine learning

## Result (TBD)

- After 1000 training sets, average accuracy ~= N(%)
