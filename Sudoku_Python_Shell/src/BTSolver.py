import SudokuBoard
import Variable
import Domain
import Trail
import Constraint
import ConstraintNetwork
import time
import random

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork.ConstraintNetwork(gb)
        self.hassolution = False
        self.gameboard = gb
        self.trail = trail

        self.varHeuristics = var_sh
        self.valHeuristics = val_sh
        self.cChecks = cc

    # ==================================================================
    # Consistency Checks
    # ==================================================================

    # Basic consistency check, no propagation done
    def assignmentsCheck ( self ):
        for c in self.network.getConstraints():
            if not c.isConsistent():
                return False
        return True

    """
        Part 1 TODO: Implement the Forward Checking Heuristic

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        Note: remember to trail.push variables before you assign them
        Return: a tuple of a dictionary and a bool. The dictionary contains all MODIFIED variables, mapped to their MODIFIED domain.
                The bool is true if assignment is consistent, false otherwise.
    """
    def forwardChecking ( self ):
        
        
        assignedVars = []
        for c in self.network.getModifiedConstraints():
            for v in c.vars:
                if v.isAssigned():
                    assignedVars.append(v)

        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if neighbor.getDomain().size() == 0:
                    return ({}, False)

                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    self.trail.push(neighbor)
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.getDomain().size() == 0:
                        return ({}, False)

        
        return ({}, self.assignmentsCheck())


    # =================================================================
	# Arc Consistency
	# =================================================================

    
    def arcConsistency( self ):
        assignedVars = []
        for c in self.network.constraints:
            for v in c.vars:
                if v.isAssigned():
                    assignedVars.append(v)
        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.domain.size() == 1:
                        neighbor.assignValue(neighbor.domain.values[0])
                        assignedVars.append(neighbor)
    
    
    """
        Part 2 TODO: Implement both of Norvig's Heuristics

        This function will do both Constraint Propagation and check
        the consistency of the network

        (1) If a variable is assigned then eliminate that value from
            the square's neighbors.

        (2) If a constraint has only one possible place for a value
            then put the value there.

        Note: remember to trail.push variables before you assign them
        Return: a pair of a dictionary and a bool. The dictionary contains all variables 
		        that were ASSIGNED during the whole NorvigCheck propagation, and mapped to the values that they were assigned.
                The bool is true if assignment is consistent, false otherwise.
    """
    def norvigCheck ( self ):

        #FC code:
        to_return = dict()
               
        assignedVars = []
        for c in self.network.getModifiedConstraints():
            for v in c.vars:
                if v.isAssigned():
                    assignedVars.append(v)

        while len(assignedVars) != 0:
            av = assignedVars.pop(0)
            for neighbor in self.network.getNeighborsOfVariable(av):
                if neighbor.getDomain().size() == 0:
                    return ({}, False)

                if neighbor.isChangeable and not neighbor.isAssigned() and neighbor.getDomain().contains(av.getAssignment()):
                    self.trail.push(neighbor)
                    neighbor.removeValueFromDomain(av.getAssignment())
                    if neighbor.getDomain().size() == 0:
                        return ({}, False)


        #Norvig's assignments
        for constraint in self.network.getModifiedConstraints():
            for value in range(1, self.gameboard.N + 1):      # for all possible values ex 1-9, 1-16
                counter = 0
                for var in constraint.vars:
                    if var.domain.contains(value):
                        counter += 1

                if counter == 1:
                    self.trail.push(var)
                    var.assignValue(value)
                    to_return[var] = value

                if counter == 0:
                    return ({}, False)


        
        return (to_return, self.assignmentsCheck())


    """
         Optional TODO: Implement your own advanced Constraint Propagation

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournCC ( self ):
        return False

    # ==================================================================
    # Variable Selectors
    # ==================================================================

    # Basic variable selector, returns first unassigned variable
    def getfirstUnassignedVariable ( self ):
        for v in self.network.variables:
            if not v.isAssigned():
                return v

        # Everything is assigned
        return None

    """
        Part 1 TODO: Implement the Minimum Remaining Value Heuristic

        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        temp = self.getfirstUnassignedVariable()
        if not temp:
            return None
            
        smallest_var_size = 100000
        smallest_var = None
        for variable in self.network.variables:
            if variable.domain.size() < smallest_var_size and not variable.assigned:
                smallest_var = variable
                smallest_var_size = variable.domain.size()
        
        return smallest_var


    """
        Part 2 TODO: Implement the Minimum Remaining Value Heuristic
                       with Degree Heuristic as a Tie Breaker

        Return: The unassigned variable with the smallest domain and affecting the  most unassigned neighbors.
                If there are multiple variables that have the same smallest domain with the same number of unassigned neighbors, add them to the list of Variables.
                If there is only one variable, return the list of size 1 containing that variable.
    """
    def MRVwithTieBreaker ( self ):
        size = self.getMRV().size()
        varList = []
        for variable in self.network.variables:
            if variable.domain.size() == size and not variable.assigned:
                varList.append(variable)

        
        if len(varList) == 1:
            return varList

        finalList = []
        largestDomain = -1000000000
        largestVar = None
        for variable in varList:
            neighborsSize = len(self.network.getNeighborsOfVariable(variable))
            if neighborsSize > largestDomain:
                largestDomain = neighborsSize
                largestVar = variable

        for variable in varList:   # if there's multiple with the same Degree and MRV
            neighborsSize = len(self.network.getNeighborsOfVariable(variable))
            if neighborsSize == largestDomain:
                finalList.append(variable)
        
        return finalList

    """
         Optional TODO: Implement your own advanced Variable Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVar ( self ):
        return None

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Part 1 TODO: Implement the Least Constraining Value Heuristic

        The Least constraining value is the one that will knock the least
        values out of it's neighbors domain.

        Return: A list of v's domain sorted by the LCV heuristic
                The LCV is first and the MCV is last
    """
    def getValuesLCVOrder ( self, v ):
        storage = dict()       # key: domain size    value: domain value

        # listOne: EACH DOMAIN Value
        list1 = list()
        # listTwo: SAME SIZE BUT INIT TO 0
        list2 = list()

        # loop through domain 
        #     loop through neighbors  
        #         if value in domain
        #             increment corresponding index in list2
        for domain_value in v.getDomain().values:
            list1.append(domain_value)
            list2.append(0)

        if len(list1) == 0:
            return []
        
        neighbors = self.network.getNeighborsOfVariable(v)
        for index in range(0, len(list1)):   # counts how many neighbors have this value in the domain
            for neighbor in neighbors:  # for each neighbor
                if not list1[index] in neighbor.getDomain().values:  # if that neighbor has the value in its domain
                    list2[index] += 1
        
        list_zip = list(zip(list1, list2))

        sorted(list_zip, key=lambda x: x[1])
        
        to_return = [tup[0] for tup in list_zip]
        # print("First: ")
        # print(to_return)
        # return to_return
            
        for value in v.getDomain().values:  # hypothetically pick value
            neighborsDomainSize = 0
            
            for neighbor in self.network.getNeighborsOfVariable(v):  # for each neighbor
                if not value in neighbor.getDomain().values:  # if that neighbor has the value in its domain
                    neighborsDomainSize += 1  # add that variables domain size - 1 bc we picked it 

            storage[value] = neighborsDomainSize

        # find the greatest value, apoend the key associated with value to storage list, remove from dictionary, repeat
        
        storage_list = []

        last_domain = -1
        last_key = -1
        for i in range(0, len(storage)):
            maxDomain = -1
            maxKey = -1
            for key in storage:
                if storage[key] > maxDomain:
                    maxDomain = storage[key]
                    maxKey = key
            if last_domain == maxDomain and maxKey < last_key:
                storage.pop(maxKey)
                storage_list.insert(i - 1, maxKey)
                last_domain = maxDomain
                last_key = maxKey
                continue
            storage.pop(maxKey)
            storage_list.append(maxKey)
            last_domain = maxDomain
            last_key = maxKey
        
        # print("Second: ")
        # print(storage_list)
        return storage_list
        # return storage_list

    """
         Optional TODO: Implement your own advanced Value Heuristic

         Completing the three tourn heuristic will automatically enter
         your program into a tournament.
     """
    def getTournVal ( self, v ):
        return None

    # ==================================================================
    # Engine Functions
    # ==================================================================

    def solve ( self, time_left=600):
        if time_left <= 60:
            return -1

        start_time = time.time()
        if self.hassolution:
            return 0

        # Variable Selection
        v = self.selectNextVariable()

        # check if the assigment is complete
        if ( v == None ):
            # Success
            self.hassolution = True
            return 0

        # Attempt to assign a value
        for i in self.getNextValues( v ):

            # Store place in trail and push variable's state on trail
            self.trail.placeTrailMarker()
            self.trail.push( v )

            # Assign the value
            v.assignValue( i )

            # Propagate constraints, check consistency, recur
            if self.checkConsistency():
                elapsed_time = time.time() - start_time 
                new_start_time = time_left - elapsed_time
                if self.solve(time_left=new_start_time) == -1:
                    return -1
                
            # If this assignment succeeded, return
            if self.hassolution:
                return 0

            # Otherwise backtrack
            self.trail.undo()
        
        return 0

    def checkConsistency ( self ):
        if self.cChecks == "forwardChecking":
            return self.forwardChecking()[1]

        if self.cChecks == "norvigCheck":
            return self.norvigCheck()[1]

        if self.cChecks == "tournCC":
            return self.getTournCC()

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()[0]

        if self.varHeuristics == "tournVar":
            return self.getTournVar()

        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )

        if self.valHeuristics == "tournVal":
            return self.getTournVal( v )

        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)
