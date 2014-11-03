#!/usr/bin/env python

import csv
import sys


class Board:
  def __init__(self, grid=None):
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
    self.grid = [row for row in reader]
    # Validate givens.
    if len(self.grid) != 9:
      return False
    for row in self.grid:
      if len(row) != 9:
        return False
      for c in row:
        if not 0 <= int(c) <= 9:
          return False
    return True

  def write(self, f):
    "Write grid to the given file."
    writer = csv.writer(f)
    for row in self.grid: writer.writerow(row)

def solve(board):
  grid = [['123456789' for i in range(9)] for j in range(9)]
  for i in range(9):
    for j in range(9):
      c = board.grid[i][j]
      if c == '0': continue
      if not assign(grid, i, j, c):
        return None
  grid = search(grid)
  return Board(grid) if grid else None

def search(grid):
  # Check for violation.
  if not grid:
    return None

  # Check if the puzzle is already solved.
  if all(len(grid[i][j]) == 1 for i in range(9) for j in range(9)):
    return grid

  n, i, j = min((len(grid[i][j]), i, j) for i in range(9) for j in range(9)
            if len(grid[i][j]) > 1)
  for c in grid[i][j]:
    grid = grid.copy()
    if not assign(grid, i, j, c): continue
    grid = search(grid)
    if grid: return grid
  return None

def assign(grid, x, y, c):
  # Assign value to the given cell.
  grid[x][y] = c
  # Remove this value from the cell unit.
  # If another cell becomes single-valued in the process, recurse.
  singles = [(x, y)]
  while singles:
    x, y = singles.pop()
    c = grid[x][y]
    for i, j in Board.peers(x, y):
      if c not in grid[i][j]: continue
      grid[i][j] = grid[i][j].replace(c, '')
      if len(grid[i][j]) == 0:
        return False
      if len(grid[i][j]) == 1:
        singles.append((i,j))
  return True

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
    print "Improper puzzle."
    return 1
  print "Output"
  board_out.write(sys.stdout)
  return 0


if __name__ == '__main__':
  status = main()
  sys.exit(status)
