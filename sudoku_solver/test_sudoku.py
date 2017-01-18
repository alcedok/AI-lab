############################################################
# Unit Test of Sudoku Solver
############################################################

from sudoku import *
import unittest

class sudoku_TestCase(unittest.TestCase):
	def test_z(self):
		# b = read_board("sudoku/medium1.txt")
		# print Sudoku(b).get_values((0, 0))
		# set([1, 2, 3, 4, 5, 6, 7, 8, 9])

		# b = read_board("sudoku/medium1.txt")
		# print Sudoku(b).get_values((0, 1))
		# set([1])
		# print len(sudoku_cells())
		# [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), ..., (8, 5), (8, 6), (8, 7), (8, 8)]

		# print ((0, 0), (0, 8)) in sudoku_arcs()
		# # True
		# print ((0, 0), (8, 0)) in sudoku_arcs()
		# # True
		# print ((0, 8), (0, 0)) in sudoku_arcs()
		# # True

		# print ((0, 0), (2, 1)) in sudoku_arcs()
		# # True
		# print ((2, 2), (0, 0)) in sudoku_arcs()
		# # # True
		# print ((2, 3), (0, 0)) in sudoku_arcs()
		# # False
		# print ((8, 8), (0, 0)) in sudoku_arcs()


		# sudoku = Sudoku(read_board("sudoku/easy.txt")) # See below for a picture.
		# print sudoku.get_values((0, 3))
		# # set([1, 2, 3, 4, 5, 6, 7, 8, 9])
		# for col in [0, 1, 4]:
		# 	removed = sudoku.remove_inconsistent_values((0, 3), (0, col))
		# 	print removed, sudoku.get_values((0, 3))

		# True set([1, 2, 3, 4, 5, 6, 7, 9])
		# True set([1, 3, 4, 5, 6, 7, 9])
		# False set([1, 3, 4, 5, 6, 7, 9])
		# sudoku = Sudoku(read_board("sudoku/medium2.txt"))
		sudoku = Sudoku(read_board("sudoku/hardest2.txt"))
		# sudoku = Sudoku(read_board("sudoku/edge.txt"))
		# sudoku = Sudoku(read_board("sudoku/hard1_edge.txt"))
		# sudoku = Sudoku(read_board("sudoku/tough1.txt"))
		# sudoku = Sudoku(read_board("sudoku/hard2.txt"))
		# sudoku = Sudoku(read_board("sudoku/empty.txt"))
		# sudoku = Sudoku(read_board("sudoku/easy.txt"))
		# sudoku.display()
		print
		
		# sudoku.display()
		print
		# sudoku.infer_ac3()
		# sudoku.infer_improved()
		# sudoku.variable_ordering()
		sudoku.infer_with_guessing()
		# print "State: ",sudoku.is_solved()

		# sudoku.display()

		print sudoku.get_board()





		# for row,col,box in row_col_box_neighbors():
		# 	print "row", row
		# 	print "col", col
		# 	print "box", box
		# 	print "--"
		# print len(row_col_box_neighbors())
		
if __name__ == '__main__':
	unittest.main()
