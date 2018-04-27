# -*- coding: utf-8 -*-
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
    
   
    value_to_return = False
    tick = 0
    got_correct = 0
    if goal_part is not None:
        matrix_part = np.array(some_part)
        fixedMin = 0
        fixedUpper = 0
        for part_of_goal in goal_part:
            if isinstance(part_of_goal[0], int) == False:
                for goalPart in part_of_goal:
                   try: 
                       minIndex = len(matrix_part[0])
                       for maxIndex in list(range(minIndex, len(goalPart) + 1)):
                           if got_correct < len(some_part):
                               tick = 0
                               if fixedMin == 0 and fixedUpper == 0:
                                   for element, element2 in zip(some_part[got_correct], goalPart[maxIndex - minIndex : maxIndex]):
                                       
                                           if element == 0 or element == element2:
                                               tick = tick + 1
                                               if tick == minIndex:
                                                   #print(str(some_part[got_correct]) + " is equal to " + str(goalPart[maxIndex - minIndex : maxIndex]))
                                                   fixedMin = maxIndex - minIndex
                                                   fixedUpper = maxIndex
                                                   got_correct = got_correct + 1                                 
                                               
                               else:
                                   for element, element2 in zip(some_part[got_correct], goalPart[fixedMin : fixedUpper]):
                                       if element == 0 or element == element2:
                                           tick = tick + 1
                                           if tick == minIndex:
                                               #print(str(some_part[got_correct]) + " is equal to " + str(goalPart[fixedMin : fixedUpper]))
                                               got_correct = got_correct + 1
                   except:
                       got_correct = 0
            else:
               minIndex = len(matrix_part[0])
               for maxIndex in list(range(minIndex, len(part_of_goal) + 1)):
                   if got_correct < len(some_part):
                       tick = 0
                       if fixedMin == 0 and fixedUpper == 0:
                           for element, element2 in zip(some_part[got_correct], part_of_goal[maxIndex - minIndex : maxIndex]):
                               
                                   if element == 0 or element == element2:
                                       tick = tick + 1
                                       if tick == minIndex:
                                           #print(str(some_part[got_correct]) + " is equal to " + str(goalPart[maxIndex - minIndex : maxIndex]))
                                           fixedMin = maxIndex - minIndex
                                           fixedUpper = maxIndex
                                           got_correct = got_correct + 1                                 
                                       
                       else:
                           for element, element2 in zip(some_part[got_correct], part_of_goal[fixedMin : fixedUpper]):
                               if element == 0 or element == element2:
                                   tick = tick + 1
                                   if tick == minIndex:
                                       #print(str(some_part[got_correct]) + " is equal to " + str(goalPart[fixedMin : fixedUpper]))
                                       got_correct = got_correct + 1
        
    if some_part != None:
        if got_correct >= len(some_part):
            value_to_return = True
        
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
    
    appear_rotate = []
    make_object_part = TetrisPart(some_part)
    
    for rot in list(range(0,4)): 
        make_object_part.rotate90()
        matrix_part_rotated = make_object_part.get_frozen()
        if appear_as_subpart(matrix_part_rotated, goal_part):
            appear_rotate.append(rot)
           
    if appear_rotate == []:
        return np.inf
    else:
        return appear_rotate

    
    """
    for rot in 4:
        matrix_part = matrix_part.rotate90()
        value_to_return = np.in1d(matrix_part, matrix_full).all()
        print(matrix_part.shape)
        print(matrix_part)
        if value_to_return:
            return value_to_return
        else:
            return np.inf
    """   
    
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
        
        actionsToTake = []
        if state is not None:

            hold_state_parts = []
            for i in state:
                hold_state_parts.append(i)
            permutations_hold = itertools.permutations(hold_state_parts, 2)
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
        
        pa, pu, offset = action
        state_to_make_canonical = []
        
        make_object = TetrisPart(pa, part_under= pu, offset= offset)
        returned_state = make_object.get_frozen()

        for index in state:
            if index != pa and index != pu:
                state_to_make_canonical.append(index)
                
                
        print(state_to_make_canonical)
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
        #

        actionsToTake = []
        
        if state != None:
            hold_state_parts = []
            for i in state:
                hold_state_parts.append(i)
            permutations_hold = itertools.permutations(hold_state_parts, 2) # Permutations of state parts
            for part in permutations_hold:
                range_of_offset = offset_range(part[0], part[1]) # Get offset range
                range_offset = list(range(range_of_offset[0], range_of_offset[1]))
                for offset_number in range_offset:
                    make_object_part = TetrisPart(part[0], part_under= part[1], offset= offset_number)
                    part_object = make_object_part.get_frozen()
                    
                    if appear_as_subpart(part_object, self.finalGoal):
                        actionsToTake.append((part[0], part[1], offset_number))
                        
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
        # 
        actionsToTake = []
        if state is not None:
            
            hold_state_parts = []
            for part in state:
                hold_state_parts.append(part)
                actionsToTake.append((part, None, 0))
                                    
            permutations_hold = itertools.permutations(hold_state_parts, 2)

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
        #print("---------------------------------")
        pa, pu, offset = action
        state_to_make_canonical = list(state)
        final_state = ""
        
        
        if pu is not None:
            make_object = TetrisPart(pa, pu, offset) # Make new part with pa and pu
            returned_state = make_object.get_frozen() # get tuple
            state_to_make_canonical.remove(pa)
            state_to_make_canonical.remove(pu)
        else:
            make_object = TetrisPart(pa) # ???
            make_object.rotate90()
            returned_state = make_object.get_frozen()    
            state_to_make_canonical.remove(pa)
        
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

        actionsToTake = []
        if state is not None:
            
            hold_state_parts = []
            for part in state:
                hold_state_parts.append(part)
                actionsToTake.append((part, None, 0))
                                    
            permutations_hold = itertools.permutations(hold_state_parts, 2)

            for part in permutations_hold:
                range_of_offset = offset_range(part[0], part[1])
                range_offset = list(range(range_of_offset[0], range_of_offset[1]))
                
                for offset_number in range_offset:
                    make_object_part = TetrisPart(part[0], part_under= part[1], offset= offset_number)
                    part_object = make_object_part.get_frozen()
                    
                    if cost_rotated_subpart(part_object, self.goal) != np.inf:
                        print("sup")
                        actionsToTake.append((part[0], part[1], offset_number))
                                            
        
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
        cost_rotations = []
        k_n = len(n.state)
        k_g = len(self.goal)
        cost_rotations = cost_rotated_subpart(n.state, self.goal)
        if isinstance(cost_rotations, list):
            finalReturn = k_n - k_g + max(cost_rotations)
        else:
            finalReturn = k_n - k_g + cost_rotations
        
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
    if solution_for_assemblyproblem_4 == None:
        return 'no solution'
    else:
        return solution_for_assemblyproblem_4.solution()

    #         raise NotImplementedError
    #raise NotImplementedError
        
# ---------------------------------------------------------------------------


    
if __name__ == '__main__':
    pass
    
