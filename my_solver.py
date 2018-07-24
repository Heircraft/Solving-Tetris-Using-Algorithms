d# -*- coding: utf-8 -*-
"""
Created on  Feb 27 2018

@author: frederic

Scaffholding code for CAB320 Assignment One

This is the only file that you have to modify and submit for the assignment.

"""
import time

import numpy as np

import itertools

import generic_search

from assignment_one import (TetrisPart, AssemblyProblem, offset_range, 
#                            display_state, 
                            make_state_canonical, play_solution, 
#                            load_state, make_random_state
                            )

# ---------------------------------------------------------------------------

def print_the_team():
    '''
    Print details of the members of your team 
    (full name + student number)
    '''
    
    #raise NotImplementedError

    print('Abdulaziz Alahmadi, n8938938')
    print('Alexander Santander, n9684026')
    print('Hrushikesh Lakkola, n9654780')
    
# ---------------------------------------------------------------------------
        
def appear_as_subpart(some_part, goal_part):
    '''    
    Determine whether the part 'some_part' appears in another part 'goal_part'.
    
    Formally, we say that 'some_part' appears in another part 'goal_part',
    when the matrix representation 'S' of 'some_part' is a a submatrix 'M' of
    the matrix representation 'G' of 'goal_part' and the following constraints
    are satisfied:
        for all indices i,j
            S[i,j] == 0 or S[i,j] == M[i,j]
            
    During an assembly sequence that does not use rotations, any part present 
    on the workbench has to appear somewhere in a goal part!
    
    @param
        some_part: a tuple representation of a tetris part
        goal_part: a tuple representation of another tetris part
        
    @return
        True if 'some_part' appears in 'goal_part'
        False otherwise    

    '''
   

   # Initilizing values
    value_to_return = False # The value to return, init as fals
    got_correct = 0 # How many elements match
    gotcorrect_sub_arrays = 0
    
    # If the given goal state is not none
    if goal_part is not None:
        # Define variables 
        matrix_part = np.array(some_part)
        fixedMin = 0 # Define the min index to search from
        fixedUpper = 0 # Define the max index to search to
        
        # loop through the goal part
        for part_of_goal in goal_part:
            # Check if the first element of the goal part is not an integar
            if isinstance(part_of_goal[0], int) == False:
                # if not, it means there is another tuple inside, loop through it
                for goalPart in part_of_goal:
                   try: # Check if the calculations are going to fail
                       # Define the min sub array length
                       minIndex = len(matrix_part[0])
                       # Loop through the range of the min length to the upper length of goal part
                       for maxIndex in list(range(minIndex, len(goalPart) + 1)):
                           # If the number of elements matched correctly is less than the length of the sub part
                           # then continue on, else exit the loop
                           if got_correct < len(some_part):
                               gotcorrect_sub_arrays = 0 # Begin counting the elments that matched in the sub arrays
                               # If the min and max index are not selected yet, go into this
                               if fixedMin == 0 and fixedUpper == 0:
                                   # Loop through the sub part and the goal part simultaneously
                                   for some_part_element, goal_part_element in zip(some_part[got_correct], goalPart[maxIndex - minIndex : maxIndex]):
                                           # If the elment from some_part is zero or equal to the goal_part, then get in
                                           # else, contunie the for loop
                                           if some_part_element == 0 or some_part_element == goal_part_element:
                                               # Add one to the correct count of the sub arrays
                                               gotcorrect_sub_arrays = gotcorrect_sub_arrays + 1
                                               # if the correct count has reached the min index
                                               if gotcorrect_sub_arrays == minIndex:
                                                   # Define the windows to search through
                                                   fixedMin = maxIndex - minIndex
                                                   fixedUpper = maxIndex
                                                   # Add one to confirm that the full sub part appear in goal
                                                   got_correct = got_correct + 1                                 
                                               
                               else:
                                   # Loop through the window of the values
                                   for some_part_element, goal_part_element in zip(some_part[got_correct], goalPart[fixedMin : fixedUpper]):
                                       # If the elment from some_part is zero or equal to the goal_part, then get in
                                       # else, contunie the for loop
                                       if some_part_element == 0 or some_part_element == goal_part_element:
                                           # Add one to the correct count of the sub arrays
                                           gotcorrect_sub_arrays = gotcorrect_sub_arrays + 1
                                           # if the correct count has reached the min index
                                           if gotcorrect_sub_arrays == minIndex:
                                               # Add one to confirm that the full sub part appear in goal
                                               got_correct = got_correct + 1
                   except: # If they failed, the sub part will not appear in goal part
                       got_correct = 0
            else:
                # Define the min sub array length
               minIndex = len(matrix_part[0])
               # Loop through the range of the min length to the upper length of goal part
               for maxIndex in list(range(minIndex, len(part_of_goal) + 1)):
                   # If the number of elements matched correctly is less than the length of the sub part
                   # then continue on, else exit the loop
                   if got_correct < len(some_part):
                       gotcorrect_sub_arrays = 0 # Begin counting the elments that matched in the sub arrays
                       # If the min and max index are not selected yet, go into this
                       if fixedMin == 0 and fixedUpper == 0:
                           # Loop through the sub part and the goal part simultaneously
                           for some_part_element, goal_part_element in zip(some_part[got_correct], part_of_goal[maxIndex - minIndex : maxIndex]):
                                   # If the elment from some_part is zero or equal to the goal_part, then get in
                                   # else, contunie the for loop
                                   if some_part_element == 0 or some_part_element == goal_part_element:
                                       # Add one to the correct count of the sub arrays
                                       gotcorrect_sub_arrays = gotcorrect_sub_arrays + 1
                                       # if the correct count has reached the min index
                                       if gotcorrect_sub_arrays == minIndex:
                                           # Define the windows to search through
                                           fixedMin = maxIndex - minIndex
                                           fixedUpper = maxIndex
                                           # Add one to confirm that the full sub part appear in goal
                                           got_correct = got_correct + 1                                 
                                       
                       else:
                           # Loop through the window of the values
                           for some_part_element, goal_part_element in zip(some_part[got_correct], part_of_goal[fixedMin : fixedUpper]):
                               if some_part_element == 0 or some_part_element == goal_part_element:
                                   gotcorrect_sub_arrays = gotcorrect_sub_arrays + 1
                                   # if the correct count has reached the min index
                                   if gotcorrect_sub_arrays == minIndex:
                                       # Add one to confirm that the full sub part appear in goal
                                       got_correct = got_correct + 1
    # If the some part is not none
    if some_part != None:
        # Check if all the elments are the same
        if got_correct >= len(some_part):
            # Change the value to True, to signal that the sub part appear in goal part
            value_to_return = True
        
    # Return the the flag
    return value_to_return


# ---------------------------------------------------------------------------
        
def cost_rotated_subpart(some_part, goal_part):
    '''    
    Determine whether the part 'some_part' appears in another part 'goal_part'
    as a rotated subpart. If yes, return the number of 'rotate90' needed, if 
    no return 'np.inf'
    
    The definition of appearance is the same as in the function 
    'appear_as_subpart'.
                   
    @param
        some_part: a tuple representation of a tetris part
        goal_part: a tuple representation of another tetris part
    
    @return
        the number of rotation needed to see 'some_part' appear in 'goal_part'
        np.inf  if no rotated version of 'some_part' appear in 'goal_part'
    
    '''
    # Create TetrisPart object of some_part tuple, to access TetrisPart functions.
    make_object_part = TetrisPart(some_part)
    
    # Rotate above tetris part 90 degrees clockwise, 4 times.
    for rot in list(range(1,5)): 
        make_object_part.rotate90()
        
        # Get tuple of tetris part
        matrix_part_rotated = make_object_part.get_frozen() 
        
        # Call appear_as_subpart and If rotated some_part appears in goal_part, 
        # return current iteration value as it is the number of rotations. 
        if appear_as_subpart(matrix_part_rotated, goal_part):
            return rot
           
    # Return np.inf if no solution found.
    return np.inf
    
# ---------------------------------------------------------------------------

class AssemblyProblem_1(AssemblyProblem):
    '''
    
    Subclass of 'assignment_one.AssemblyProblem'
    
    * The part rotation action is not available for AssemblyProblem_1 *

    The 'actions' method of this class simply generates
    the list of all legal actions. The 'actions' method of this class does 
    *NOT* filtered out actions that are doomed to fail. In other words, 
    no pruning is done in the 'actions' method of this class.
        
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_1, self).__init__(initial, goal, use_rotation=False)
    
    def actions(self, state):
        """
        Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        @param
          state : a state of an assembly problem.
        
        @return 
           the list of all legal drop actions available in the 
            state passed as argument.
        
        """
        # Declare results array to store legal drop actions.
        actionsToTake = []
        
        # Continue if there is a state.
        if state is not None:
            
            # Store separate parts of state in hold_state_parts array by 
            # looping through state.
            hold_state_parts = []
            for i in state:
                hold_state_parts.append(i)
            
            # Store all combinations of both parts (all actions).
            permutations_hold = itertools.permutations(hold_state_parts, 2)
            
            # Loop through all combinations, find offset and store each part with offset
            # range in actionsToTake array. Return actionsToTake array.
            for part in permutations_hold:
                range_of_offset = offset_range(part[0], part[1])
                range_offset = list(range(range_of_offset[0], range_of_offset[1]))
                for offset_number in range_offset:
                    actionsToTake.append((part[0], part[1], offset_number))
        
        return actionsToTake

    def result(self, state, action):
        """
        Return the state (as a tuple of parts in canonical order)
        that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        
        @return
          a state in canonical order
        
        """
        
        # Store action[0] - [2] in corresponding part and offset variables (pa = part above, pu = part under).
        pa, pu, offset = action
        
        # Resulting array of combined state.
        state_to_make_canonical = []
        
        # Create TetrisPart object and return tuple of object.
        make_object = TetrisPart(pa, pu, offset)
        returned_state = make_object.get_frozen()
        
        # Loop parts in state and avoid existing parts (pa & pu), then append current part to
        # results array (state_make_canonical).
        for index in state:
            if index != pa and index != pu:
                state_to_make_canonical.append(index)    
                
        # Add new Tetris part to resulting array as well and make state canonical with call to 
        # respective function and return canonical final_state array. 
        state_to_make_canonical.append(returned_state)
        final_state = make_state_canonical(state_to_make_canonical)
        return final_state
        


# ---------------------------------------------------------------------------

class AssemblyProblem_2(AssemblyProblem_1):
    '''
    
    Subclass of 'assignment_one.AssemblyProblem'
        
    * Like for AssemblyProblem_1,  the part rotation action is not available 
       for AssemblyProblem_2 *

    The 'actions' method of this class  generates a list of legal actions. 
    But pruning is performed by detecting some doomed actions and 
    filtering them out.  That is, some actions that are doomed to 
    fail are not returned. In this class, pruning is performed while 
    generating the legal actions.
    However, if an action 'a' is not doomed to fail, it has to be returned. 
    In other words, if there exists a sequence of actions solution starting 
    with 'a', then 'a' has to be returned.
        
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        self.finalGoal = goal
        super(AssemblyProblem_2, self).__init__(initial, goal)
    
    def actions(self, state):
        """
        Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        A candidate action is eliminated if and only if the new part 
        it creates does not appear in the goal state.
        """
        
        # Declare results array to store legal drop actions.
        actionsToTake = []
        
        # Continue if there is a state.
        if state != None:
            
            # Store separate parts of state in hold_state_parts array by 
            # looping through state.
            hold_state_parts = []
            for i in state:
                hold_state_parts.append(i)
            
            # Store all combinations of both parts (all actions).
            permutations_hold = itertools.permutations(hold_state_parts, 2) # Permutations of state parts
            
            # Loop through all combinations, find offset and store each part with offset
            # range in actionsToTake array. 
            for part in permutations_hold:
                range_of_offset = offset_range(part[0], part[1]) # Get offset range
                range_offset = list(range(range_of_offset[0], range_of_offset[1]))
                for offset_number in range_offset:
                    make_object_part = TetrisPart(part[0], part_under= part[1], offset= offset_number)
                    part_object = make_object_part.get_frozen()
                    
                    # Perform search tree pruning by checking if current part appears in final 
                    # goal part by calling appear_as_subpart function.
                    if appear_as_subpart(part_object, self.finalGoal):
                        actionsToTake.append((part[0], part[1], offset_number))
        
        # Return resulting array
        return actionsToTake
    

# ---------------------------------------------------------------------------

class AssemblyProblem_3(AssemblyProblem_1):
    '''
    
    Subclass 'assignment_one.AssemblyProblem'
    
    * The part rotation action is available for AssemblyProblem_3 *

    The 'actions' method of this class simply generates
    the list of all legal actions including rotation. 
    The 'actions' method of this class does 
    *NOT* filter out actions that are doomed to fail. In other words, 
    no pruning is done in this method.
        
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_3, self).__init__(initial, goal)
        self.use_rotation = True

    
    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        Rotations are allowed, but no filtering out the actions that 
        lead to doomed states.
        
        """
        
        # Declare results array to store legal actions.
        actionsToTake = []
        
        # Continue if there is a state.
        if state is not None:
            
            # Store separate parts of state in hold_state_parts array by 
            # looping through state.
            hold_state_parts = []
            for part in state:
                hold_state_parts.append(part)
                actionsToTake.append((part, None, 0))
            
            # Store all combinations of both parts (all actions).
            permutations_hold = itertools.permutations(hold_state_parts, 2)
            
            # Loop through all combinations, find offset and store each part with offset
            # range in actionsToTake array.  Return actionsToTake array.
            for part in permutations_hold:
                range_of_offset = offset_range(part[0], part[1])
                range_offset = list(range(range_of_offset[0], range_of_offset[1]))
                
                for offset_number in range_offset:     
                    actionsToTake.append((part[0], part[1], offset_number))     
        
        return actionsToTake

        
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).

        The action can be a drop or rotation.        
        """
        
        # Store action[0] - [2] in corresponding part and offset variables (pa = part above, pu = part under).
        pa, pu, offset = action
        
        # Resulting list of combined state. Currently lists all parts in state.
        state_to_make_canonical = list(state)
        final_state = ""
        
        # Conditional statement to check if there is a part to drop onto or not. 
        if pu is not None:
            
            # Make new part with pa and pu.
            make_object = TetrisPart(pa, pu, offset)
            
            # Get tuple of tetris part.
            returned_state = make_object.get_frozen()
            
            # Remove existing parts from list 
            state_to_make_canonical.remove(pa)
            state_to_make_canonical.remove(pu)
        else:
            
            # Make new part with pa, rotate and get tuple of new part. 
            make_object = TetrisPart(pa) 
            make_object.rotate90()
            returned_state = make_object.get_frozen()    
            
            # Remove old part above from state list.
            state_to_make_canonical.remove(pa)
        
        # Append new state to resulting list, make canonical and return. 
        state_to_make_canonical.append(returned_state)
        final_state = make_state_canonical(state_to_make_canonical)


        return final_state


# ---------------------------------------------------------------------------

class AssemblyProblem_4(AssemblyProblem_3):
    '''
    
    Subclass 'assignment_one.AssemblyProblem3'
    
    * Like for its parent class AssemblyProblem_3, 
      the part rotation action is available for AssemblyProblem_4  *

    AssemblyProblem_4 introduces a simple heuristic function and uses
    action filtering.
    See the details in the methods 'self.actions()' and 'self.h()'.
    
    '''

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        # Call the parent class constructor.
        # Here the parent class is 'AssemblyProblem' 
        # which itself is derived from 'generic_search.Problem'
        super(AssemblyProblem_4, self).__init__(initial, goal)

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        
        Filter out actions (drops and rotations) that are doomed to fail 
        using the function 'cost_rotated_subpart'.
        A candidate action is eliminated if and only if the new part 
        it creates does not appear in the goal state.
        This should  be checked with the function "cost_rotated_subpart()'.
                
        """
        
        # Declare results array to store legal actions.
        actionsToTake = []
        
        # Continue if there is a state.
        if state is not None:
            
            # Store separate parts of state in hold_state_parts array by 
            # looping through state.
            hold_state_parts = []
            for part in state:
                hold_state_parts.append(part)
                actionsToTake.append((part, None, 0))
            
            # Store all combinations of both parts (all actions).                        
            permutations_hold = itertools.permutations(hold_state_parts, 2)

            # Loop through all combinations, find offset and store each part with offset
            # range in actionsToTake array. 
            for part in permutations_hold:
                range_of_offset = offset_range(part[0], part[1])
                range_offset = list(range(range_of_offset[0], range_of_offset[1]))
                
                for offset_number in range_offset:
                    make_object_part = TetrisPart(part[0], part_under= part[1], offset= offset_number)
                    part_object = make_object_part.get_frozen()
                    
                    # Check if part exists in final goal part with consideration of all rotations.
                    if cost_rotated_subpart(part_object, self.goal) != np.inf:
                        actionsToTake.append((part[0], part[1], offset_number))
                                            
        # Return results array.
        return actionsToTake
        
        
        
    def h(self, n):
        '''
        This heuristic computes the following cost; 
        
           Let 'k_n' be the number of parts of the state associated to node 'n'
           and 'k_g' be the number of parts of the goal state.
          
        The cost function h(n) must return 
            k_n - k_g + max ("cost of the rotations")  
        where the list of cost of the rotations is computed over the parts in 
        the state 'n.state' according to 'cost_rotated_subpart'.
        
        
        @param
          n : node of a search tree
          
        '''
        
        finalReturn = 0
        
        # Declare array to store cost of rotations for each part in state. 
        cost_rotations = []
        
        # Number of parts in given state associated with node 'n'.
        k_n = len(n.state)
        
        # Number of parts of the goal state.
        k_g = len(self.goal)
        
        # Loop through given state. 
        for index in n.state:
            
            # Get cost of rotations needed for current part to appear in final part and store 
            # in cost_rotation array. 
            cost_rotations.append(cost_rotated_subpart(index, self.goal))
            
        # ALEX COMMENT THIS.
#        if isinstance(cost_rotations, list):
            finalReturn = k_n - k_g + max(cost_rotations)
#        else:
#            finalReturn = k_n - k_g + cost_rotations
        
        return finalReturn
        

# ---------------------------------------------------------------------------
       
def solve_1(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_1
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_1
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    print('\n++  busy searching in solve_1() ...  ++\n')
    
    assembly_problem = AssemblyProblem_1(initial, goal) # HINT
    solution_for_assemblyproblem_1 = generic_search.depth_first_graph_search(assembly_problem)
    
    # If solution is found, return the solution tuple. Else return string 'no solution'.
    if solution_for_assemblyproblem_1 is not None:
        return solution_for_assemblyproblem_1.solution()
    else:
        return 'no solution'        
    

# ---------------------------------------------------------------------------
        
def solve_2(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_2
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_2
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    print('\n++  busy searching in solve_2() ...  ++\n')
    
    assembly_problem = AssemblyProblem_2(initial, goal)
    solution_for_assemblyproblem_2 = generic_search.depth_first_graph_search(assembly_problem)
    
    # If solution is found, return the solution tuple. Else return string 'no solution'.
    if solution_for_assemblyproblem_2 is not None:
        return solution_for_assemblyproblem_2.solution()
    else:
        return 'no solution'
    
# ---------------------------------------------------------------------------

def solve_3(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_3
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_3
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''

    print('\n++  busy searching in solve_3() ...  ++\n')
    
    assembly_problem = AssemblyProblem_3(initial, goal)
    solution_for_assemblyproblem_3 = generic_search.depth_first_graph_search(assembly_problem)
    
    # If solution is found, return the solution tuple. Else return string 'no solution'.
    if solution_for_assemblyproblem_3 == None:
        return 'no solution'
    else:
        return solution_for_assemblyproblem_3.solution()

    '''raise NotImplementedError'''
    
# ---------------------------------------------------------------------------
        
def solve_4(initial, goal):
    '''
    Solve a problem of type AssemblyProblem_4
    
    The implementation has to 
    - use an instance of the class AssemblyProblem_4
    - make a call to an appropriate functions of the 'generic_search" library
    
    @return
        - the string 'no solution' if the problem is not solvable
        - otherwise return the sequence of actions to go from state
        'initial' to state 'goal'
    
    '''
    
    print('\n++  busy searching in solve_4() ...  ++\n')
    
    assembly_problem = AssemblyProblem_4(initial, goal)
    solution_for_assemblyproblem_4 = generic_search.astar_graph_search(assembly_problem)
    
    # If solution is found, return the solution tuple. Else return string 'no solution'.
    if solution_for_assemblyproblem_4 == None:
        return 'no solution'
    else:
        return solution_for_assemblyproblem_4.solution()

    #         raise NotImplementedError
    #raise NotImplementedError
        
# ---------------------------------------------------------------------------


    
if __name__ == '__main__':
    pass
    
