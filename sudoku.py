#!/usr/bin/env python

import csv
import sys


class Board:
  def __init__(self, grid=None):
    self.grid = grid

  def read(self, filename):
    "Read grid from the given filename."
    with open(filename) as f:
      reader = csv.reader(f)
      self.grid = [row for row in reader]
    # Validate givens.
    assert len(self.grid) == 9
    for row in self.grid:
      assert len(row) == 9
      for c in row: assert 0 <= int(c) <= 9

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
      assign(grid, i, j, c)
  return Board(grid)

def assign(grid, i, j, c):
  #print '{0},{1}'.format(i, j)
  # Assign value to the given cell.
  grid[i][j] = c
  # Remove from row.
  for k in range(0, 9):
    if k == j: continue
    grid[i][k] = grid[i][k].replace(c, '')
  # Remove from column.
  for k in range(0, 9):
    if k == i: continue
    grid[k][j] = grid[k][j].replace(c, '')
  # Remove from block.
  b_i = 3 * (i / 3)
  b_j = 3 * (j / 3)
  for p in range(b_i, b_i+3):
    for q in range(b_j, b_j+3):
      if p == i and q == j: continue
      grid[p][q] = grid[p][q].replace(c, '')

if __name__ == '__main__':
  board_in = Board()
  board_in.read(sys.argv[1])
  print "Input"
  board_in.write(sys.stdout)

  board_out = solve(board_in)
  print "Output"
  board_out.write(sys.stdout)
