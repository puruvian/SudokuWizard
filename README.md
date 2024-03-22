# SudokuWizard

This project is an AI based Sudoku solver. It implements a backtracking search with various heuristics and includes a board generator program.


## How it works
<br>

The backtracking search algorithm treats each state of a Sudoku board as an (implicit) node in a tree. It then recursively iterates through each of these implicit states, using heuristics to choose a value more likely to lead to a solution, or to skip branches which will not be successful. Each square on the Sudoku Board is considered a variable and  initially contains all possible values as part of the domain. The heuristics implemented are outlined below.   


| Heuristic Name | Description |
| ----------- | ----------- |
| Minimum Remaining Value | The backtracking function chooses the variable with the smallest number of values in its domain. |
| Minimum Remaining Value with Degree Heuristic as tie breaker | When multiple variables have equivalently sized domains, the Degree heuristic chooses the variable with the *largest* number of unassigned neighbors. Neighbors are considered to be all variables in the same row, column, or square. |
| Least Constraining Value | Given a variable, choose the *value* which rules out the fewest values in the domains of the neighboring variables. |
| Forward Checking | After assigning a value to a variable, remove that value from the variable's neighbors. |
| Norvig's Heuristic | If within a constraint (row, column, or square) there is only one legal place to assign a value, assign it there. |  

## How to run the solver
<br>


To run the project, clone the repository, cd into the Sudoku_Python_Shell file and run the following command:

    python3 bin/Main.pyc [options]

Options are space seperated, and ordering has no effect:

- `MRV`: Minimum Remaining Value Variable
- `MAD`: MRV and DEG Tie Breaker
- `LCV`: Least Constraining Value Value 
- `FC`: Forward Checking Constraint Propagation
- `NOR`: Norvig's Sudoku Constraint Propagation

