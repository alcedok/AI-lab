############################################################
# Sudoku Solver
# @author: kevin_alcedo
# 
# more info: www.wikipedia.org/wiki/Hidden_Markov_model
# description: the sudoku problem is solved as a AC-3
#              constraint satisfaction problem in three
#              different ways, in order to successfully
#              solve medium and hard problems.  
############################################################

from itertools import permutations,chain
from collections import deque, Counter
import copy 
import cPickle as pickle

############################################################
# Sudoku
############################################################

def sudoku_cells():
    # create and return list of tuples containing all valid cells of a sudoku puzzle
    return [(row,col) for col in xrange(9) for row in xrange(9)] 

def sudoku_arcs():

    # create and return a list of tuples containing all cells neighbors that constrain each other, i.e [((row1,col1),(row2,col2))...]
    # compute arcs of cols
    constraining_cells = [((row_1,col_1),(row_1,col)) for row_1,col_1 in [(row,col) for col in xrange(9) for row in xrange(9)] for col in xrange(9) if col_1!=col]
    # compute arcs of rows
    constraining_cells = constraining_cells + [((row_1,col_1),(row,col_1)) for row_1,col_1 in [(row,col) for col in xrange(9) for row in xrange(9)] for row in xrange(9) if row_1 != row]
    # compute arcs in boxes
    constraining_cells = list(set(constraining_cells + list(chain.from_iterable([list(permutations(boxes,2)) for boxes in [ [ (row+box_row*3,col+box_col*3) for row in xrange(3) for col in xrange(3)] for box_row in xrange(3) for box_col in xrange(3) ]] ))))

    return constraining_cells


def read_board(path):
    # read and return a dictionary that contains all cells and their corresponding values

    # possible values in each cell 
    possible_values = set(xrange(1,10))
    # go through lines in .txt file and append to a new list, removing \n and \r
    lines = [ [char for char in line if (char != '\n' and char != '\r')] for line in (open(path)).readlines()]
    # now create a dictionary that maps cell to values
    return {(row,col):(set(possible_values) if item == '*' else set([int(item)]) ) for row,values in enumerate(lines) for col,item in enumerate(values)}


def row_col_box_neighbors():
    # list of regions on board, [[row],[col],[box]] for each cell on the board
    return [  [[(cell[0],col) for col in xrange(9)]]+[[(row,cell[1]) for row in xrange(9)]]+[[(row+cell[0]-(cell[0]%3),col+cell[1]-(cell[1]%3)) for row in xrange(3) for col in xrange(3)]] for cell in sudoku_cells()]

############################################################
# Class
############################################################

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    ROW_COL_BOX_NEIGHBORS = row_col_box_neighbors()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):

        # if cell1 and cell2 are neighbors and cell2 has more than one value
        if ((cell1,cell2) in self.ARCS) and len(self.get_values(cell2)) == 1:
            # continue if values will change
            if (self.get_values(cell1)) != ((self.get_values(cell1))-(self.get_values(cell2))):
                # remove set that inconsistent values
                self.board[cell1] = (self.get_values(cell1))-(self.get_values(cell2))  
                return True
        else: return False
            
    def is_solved(self):
        # go through all values in the board 
        # if any of them has more than one value then mark as notSolved
        # if any of them are empty then return as unSolvable
        # otherwise the board is solved

        # 0: solved
        # 1: notSolved
        # 2: unSolvable

        flag = 0
        for value in (self.board).itervalues():
            if (len(list(value)) > 1): 
                flag = 1
            if len(list(value)) == 0:
                return 2
        return flag


    def get_board(self):
        return self.board

    def constraining_neighbors(self,cell):
        # function yields neighbors that constrain cell
        for  neighbor,current_cell in self.ARCS:
            if current_cell == cell:
                yield neighbor

    # def most_constraining_value(self):
    def infer_ac3(self):
        # put all arcs int a queue
        queue = deque(self.ARCS)
        # if queue not empty
        while queue:
            cell1,cell2 = queue.popleft()
            # if a value was removed 
            if self.remove_inconsistent_values(cell1,cell2):
                for neighbor in self.constraining_neighbors(cell1):
                    if (neighbor,cell1) != (cell2,cell1):
                        queue.append((neighbor,cell1))

    def infer_improved(self):
        # this flag checks if board has changed
        flag = True
        # loop while the board has not been solved
        while flag:
            flag = False

            # run AC3 first to minimie possible positions
            self.infer_ac3()

            # if the board is unSolvable then break out of loop
            if self.is_solved() == 2: 
                break
            # go through every cell and check the constrains by the neighbors in box, row and col
            for row,col,box in self.ROW_COL_BOX_NEIGHBORS:
                # check neighbors in box
                for cell in row+col+box:
                    # if the cell has more than one value  
                    if len(self.get_values(cell)) > 1:
                        current_values = self.get_values(cell)
                        # for every neighbor in the box check which values are possible 
                        for neighbor_in_box in box:
                            if neighbor_in_box != cell:
                                current_values = current_values - self.get_values(neighbor_in_box)

                        # if there are values that the cell can take then update 
                        if len(current_values) > 0:
                            self.board[cell] = current_values
                            flag = True

                    # if the cell has more than one value  
                    if len(self.get_values(cell)) > 1:
                        current_values = self.get_values(cell)

                        # for every neighbor in the row check which values are possible 
                        for neighbor_in_row in row:
                            if neighbor_in_row != cell: 
                                current_values = current_values - self.get_values(neighbor_in_row)

                        # if there are values that the cell can take then update
                        if len(current_values) > 0: 
                            self.board[cell] = current_values
                            flag = True            

                    # if the cell has more than one value  
                    if len(self.get_values(cell)) > 1:
                        current_values = self.get_values(cell)

                        # for every neighbor in the col check which values are possible 
                        for neighbor_in_col in col:
                            if neighbor_in_col != cell:
                                current_values = current_values - self.get_values(neighbor_in_col)

                        # if there are values that the cell can take then update
                        if len(current_values) > 0: 
                            self.board[cell] = current_values
                            flag = True

    def infer_with_guessing(self):
        # run AC3_improved 
        self.infer_improved() 
        self.board = self.helper_infer_with_guessing()


    def helper_infer_with_guessing(self):
        # 0: solved
        # 1: notSolved
        # 2: unSolvable
        # recursive function which solves sudoku through guessing   

        if self.is_solved() == 0:
            return  self.board

        # go through every left over unsolved cell 
        for cell in self.variable_ordering():
            # print cell
            # print len(list(self.variable_ordering())), "# of cell"
            if self.is_solved() == 0:
                return  self.board

            # loop through all possible values and choose one
            for value in self.value_ordering(cell):
            # for value,count in self.incomplete_cells():
                new_board = pickle.loads(pickle.dumps(self,-1))
                if self.is_solved() == 0:
                    return  self.board 
                # change the values in cell to chosen value
                new_board.board[cell] = set([value])

                new_board.infer_improved()
                if new_board.is_solved() == 0:
                    new_board.solved = True
                    self.board = new_board.get_board()
                    return new_board.get_board()

                # we need to check if solvable, or unsolvable
                # if the boar is not solved and if solvable then recurse
                # else ignore, move on for loop
                if new_board.is_solved() == 1:
                    return new_board.helper_infer_with_guessing()
            
    def variable_ordering(self):
        # order of cells given the number of values in each
        # count number of values in cell
        # order cells according to how many values they have inside
        # this funtion will generate a list of possible cells to look at 
        # currently in ascending 
        variable_ordering =sorted({key:(len(values)) for key,values in (self.board).iteritems() if len(values) > 1}.items(),key=lambda x:x[1]) 
        for cell,count in variable_ordering:
            yield cell

    def value_ordering(self,cell):
        # given possible arcs 
        # check how many times neighbors have the values 
        # order by the value count of all arcs
        # go thru every neighbor and count how many times it appears
        # currently in ascending
        values_in_cell =  self.get_values(cell)
        value_ordering =  sorted(Counter( value for value in list(chain.from_iterable([(self.get_values(cell)) for cell in self.constraining_neighbors(cell)])) if value in values_in_cell).items(),key=lambda x:x[1])
        for value, count in value_ordering:
            yield value

    def display(self):
        # Create dummy counters
        rows = 'ABCDEFGHI'
        cols = '123456789'

        # Iterate through board using dummy counters
        for i, r in enumerate(rows):
            if i in [3, 6]:
                print '------+-------+-------'
            for j, c in enumerate(cols):
                if j in [3, 6]:
                    print '|',
                you = list(self.get_values((i,j)))
                if len(you)>1 or len(you)==0: print '*' ,
                else: print you[0],
            print
