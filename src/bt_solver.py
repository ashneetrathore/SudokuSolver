from constraint_network import ConstraintNetwork
import time

class BTSolver:

    # ==================================================================
    # Constructors
    # ==================================================================

    def __init__ ( self, gb, trail, val_sh, var_sh, cc ):
        self.network = ConstraintNetwork(gb)
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
        Forward Checking Heuristic

        This function will do both Constraint Propagation and check the consistency of the network
        (1) If a variable is assigned then eliminate that value from the square's neighbors.
        Return: (dictionary, bool)
        The dictionary contains all MODIFIED variables, mapped to their MODIFIED domain.
        The bool is true if assignment is consistent, false otherwise.
    """
    def forwardChecking ( self ):
        dictVar = dict();
        for clist in self.network.getModifiedConstraints():
            for var in clist.vars:
                if var.isAssigned():
                    for n in self.network.getNeighborsOfVariable(var):
                        if var.getAssignment() in n.getValues():
                            self.trail.push(n)
                            n.removeValueFromDomain(var.getAssignment())
                            if n.getDomain().isEmpty():
                                return (dictVar, False)
                            dictVar[n] = n.getDomain()

        return (dictVar, self.assignmentsCheck())
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
        Norvig's Heuristics

        This function will do both Constraint Propagation and check the consistency of the network
        (1) If a variable is assigned then eliminate that value from the square's neighbors.
        (2) If a constraint has only one possible place for a value then put the value there.
        Return: (dictionary, bool)
        The dictionary contains all variables that were ASSIGNED during the whole NorvigCheck propagation, and mapped to the values that they were assigned.
        The bool is true if assignment is consistent, false otherwise.
    """
    def norvigCheck ( self ):
        dictVar = dict();
        for clist in self.network.getModifiedConstraints():
            for var in clist.vars:
                if var.isAssigned():
                    for n in self.network.getNeighborsOfVariable(var):
                        if var.getAssignment() in n.getValues():
                            self.trail.push(n)
                            n.removeValueFromDomain(var.getAssignment())
                            if n.getDomain().isEmpty():
                                return (dictVar, False)
                            dictVar[n] = n.getDomain()

        for clist in self.network.getConstraints():
            for i in range(1, self.gameboard.N + 1):
                count = 0
                index = 0
                chosenOne = 0
                for var in clist.vars:
                    if i in var.getValues():
                        count += 1
                        chosenOne = index
                    index += 1
                
                if count == 0:
                    return (dictVar, False)
                
                var = clist.vars[chosenOne]
                if (count == 1) and (not var.isAssigned()):
                    self.trail.push(var)
                    var.assignValue(i);
                    dictVar[var] = var.getDomain()

        return (dictVar, self.assignmentsCheck())

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
        Minimum Remaining Value Heuristic
        Return: The unassigned variable with the smallest domain
    """
    def getMRV ( self ):
        chosenOne = None
        
        for v in self.network.variables:
            if not v.isAssigned():
                domain_size = v.getDomain().size()
                if chosenOne != None:
                    if (domain_size < chosenOne.getDomain().size()):
                        chosenOne = v
                else:
                    chosenOne = v

        return chosenOne

    """
        Implement the Minimum Remaining Value Heuristic with Degree Heuristic as a Tie Breaker
        Return: A list containing unassigned variable(s) with the smallest domain and affecting the most unassigned neighbors (can be a list of size 1)
    """
    def MRVwithTieBreaker ( self ):
        smallestDomains = []
        minDomain = None
    
        for v in self.network.variables:
            if not v.isAssigned():
                domain_size = v.getDomain().size()
                if minDomain == None:
                    minDomain = domain_size
                    smallestDomains.append(v)
                else:
                    if (domain_size < minDomain):
                        smallestDomains = [v]
                        minDomain = domain_size
                    elif (domain_size == minDomain):
                        smallestDomains.append(v)
        
        if (len(smallestDomains) == 0):
            return [None]
        
        listOfChosen = []
        mostUnassignedNeighborsCount = -1

        for v in smallestDomains:
            neighbors = self.network.getNeighborsOfVariable(v)
            unassignedNeighbors = 0
            for n in neighbors:
                if not n.isAssigned():
                    unassignedNeighbors += 1
            
            if unassignedNeighbors > mostUnassignedNeighborsCount:
                listOfChosen = [v]
                mostUnassignedNeighborsCount = unassignedNeighbors

            elif unassignedNeighbors == mostUnassignedNeighborsCount:
                listOfChosen.append(v)
        
        return listOfChosen

    # ==================================================================
    # Value Selectors
    # ==================================================================

    # Default Value Ordering
    def getValuesInOrder ( self, v ):
        values = v.domain.values
        return sorted( values )

    """
        Least Constraining Value Heuristic
        The least constraining value is the one that will knock the least values out of it's neighbors domain.
        Return: A list of v's domain sorted by the LCV heuristic (LCV is first and MCV is last)
    """
    def getValuesLCVOrder ( self, v ):
        neighbors = self.network.getNeighborsOfVariable(v);
        constraintsForVal = []
        for val in v.domain.values:
            valuesKnocked = 0
            for n in neighbors:
                if val in n.getValues():
                    valuesKnocked += 1
            constraintsForVal.append(valuesKnocked);

        sortedByLCV = [v for k, v in sorted(zip(constraintsForVal, list(v.domain.values)), key=lambda pair: pair[0])]
        return sortedByLCV

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

        else:
            return self.assignmentsCheck()

    def selectNextVariable ( self ):
        if self.varHeuristics == "MinimumRemainingValue":
            return self.getMRV()

        if self.varHeuristics == "MRVwithTieBreaker":
            return self.MRVwithTieBreaker()[0]
        
        else:
            return self.getfirstUnassignedVariable()

    def getNextValues ( self, v ):
        if self.valHeuristics == "LeastConstrainingValue":
            return self.getValuesLCVOrder( v )
        else:
            return self.getValuesInOrder( v )

    def getSolution ( self ):
        return self.network.toSudokuBoard(self.gameboard.p, self.gameboard.q)