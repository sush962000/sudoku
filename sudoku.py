#!/usr/bin/env python

import csv
import sys


class Board:
  def __init__(self, grid=None):
    self.grid = grid

  @classmethod
  def blank(cls):
    """Creates a blank sudoku board.
    A blank cell is initialized with all possible values."""
    return cls([['123456789' for i in range(9)] for j in range(9)])

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
    if not 1 <= int(d) <= 9:
      return False

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

def read(f):
  """Read sudoku grid from the given file.
     The missing values are represented by '0'.
     Returns None if the given grid is invalid."""
  reader = csv.reader(f)
  grid = [row for row in reader]
  # Validate givens.
  if len(grid) != 9:
    return None
  for row in grid:
    if len(row) != 9:
      return None
    for d in row:
      if not 0 <= int(d) <= 9:
        return None
  return grid

def write(grid, f):
    "Write grid to the given file."
    writer = csv.writer(f)
    for row in grid: writer.writerow(row)

def solve(grid):
  "Solve the sudoku puzzle for the given grid."
  assert(grid)
  board_in = Board.blank()
  for i in range(9):
    for j in range(9):
      if grid[i][j] == '0':
        continue
      if not board_in.assign(i, j, grid[i][j]):
        return None
  board_out = _search(board_in)
  return board_out.grid if board_out else None

def _search(board_in):
  # Check for violation.
  if not board_in:
    return None

  # Check if the puzzle is already solved.
  if board_in.solved():
    return board_in

  # Guess a value for one of the blank cells.
  # Return as soon as a valid solution is found.
  # Prioritize cells that fewer number of possible values.
  n, x, y = min(
      (len(board_in.cell(i, j)), i, j) for i in range(9) for j in range(9)
          if len(board_in.cell(i, j)) > 1)
  for d in board_in.cell(x, y):
    board_out = board_in.copy()
    if not board_out.assign(x, y, d):
      continue
    board_out = _search(board_out)
    if board_out:
      return board_out
  return None


def main():
  with open(sys.argv[1]) as f:
    grid_in = read(f)
    if not grid_in:
      print "Invalid input."
      return 1
  print "Input"
  write(grid_in, sys.stdout)

  grid_out = solve(grid_in)
  if not grid_out:
    print "Invalid puzzle."
    return 1
  print "Output"
  write(grid_out, sys.stdout)
  return 0


if __name__ == '__main__':
  sys.exit(main())
