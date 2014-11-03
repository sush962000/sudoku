#!/usr/bin/env python

import csv
import sys


class Board:
  def __init__(self, grid=None):
    if not grid:
      grid = [['123456789' for i in range(9)] for j in range(9)]
    self.grid = grid

  @staticmethod
  def peers(x, y):
    "Returns coordinates for the peers of the given cell."
    # Columns.
    for j in range(0, 9):
      if j == y: continue
      yield x, j
    # Rows.
    for i in range(0, 9):
      if i == x: continue
      yield i, y
    # Block.
    bx = 3 * (x / 3)
    by = 3 * (y / 3)
    for i in range(bx, bx + 3):
      for j in range(by, by + 3):
        if i == x or j == y: continue
        yield i, j

  def read(self, f):
    "Read grid from the given file."
    reader = csv.reader(f)
    grid = [row for row in reader]
    if len(grid) != 9:
      return False

    for i, row in enumerate(grid):
      if len(row) != 9:
        return False
      for j, d in enumerate(row):
        if not 0 <= int(d) <= 9:
          return False
        if d == '0': continue
        if not self.assign(i, j, d):
          return False
    return True

  def write(self, f):
    "Write grid to the given file."
    writer = csv.writer(f)
    for row in self.grid: writer.writerow(row)

  def copy(self):
    "Returns a copy of this board."
    return Board([row[:] for row in self.grid])

  def cell(self, x, y):
    "Returns the current value of the current cell."
    return self.grid[x][y]

  def solved(self):
    "Returns True if the board is already solved."
    return all(len(self.grid[i][j]) == 1 for i in range(9) for j in range(9))

  def assign(self, x, y, d):
    """Assigns d to the cell at (x,y).
       Returns True if the value can be assigned without violating rules"""
    self.grid[x][y] = d
    # Remove this value from the cell unit.
    # If another cell becomes single-valued in the process, recurse.
    singles = [(x, y)]
    while singles:
      x, y = singles.pop()
      d = self.grid[x][y]
      for i, j in Board.peers(x, y):
        if d not in self.grid[i][j]: continue
        self.grid[i][j] = self.grid[i][j].replace(d, '')
        if len(self.grid[i][j]) == 0:
          return False
        if len(self.grid[i][j]) == 1:
          singles.append((i,j))
    return True


def solve(board):
  "Solve the sudoku puzzle for the given board."
  # Check for violation.
  if not board:
    return None

  # Check if the puzzle is already solved.
  if board.solved():
    return board

  n, i, j = min((len(board.cell(i,j)), i, j) for i in range(9) for j in range(9)
            if len(board.cell(i,j)) > 1)
  for d in board.cell(i, j):
    board_copy = board.copy()
    if not board_copy.assign(i, j, d):
      continue
    board_solved = solve(board_copy)
    if board_solved:
      return board_solved
  return None


def main():
  board_in = Board()
  with open(sys.argv[1]) as f:
    if not board_in.read(f):
      print "Invalid input."
      return 1
  print "Input"
  board_in.write(sys.stdout)

  board_out = solve(board_in)
  if not board_out:
    print "Invalid puzzle."
    return 1
  print "Output"
  board_out.write(sys.stdout)
  return 0


if __name__ == '__main__':
  sys.exit(main())
