#!/usr/bin/env python

import csv
import sys


class Board:
  def __init__(self):
    self.grid = []

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
    "Write grid to stdout."
    writer = csv.writer(f)
    for row in self.grid: writer.writerow(row)

def solve(board):
  return board


if __name__ == '__main__':
  board_in = Board()
  board_in.read(sys.argv[1])
  print "Input"
  board_in.write(sys.stdout)

  board_out = solve(board_in)
  print "Output"
  board_out.write(sys.stdout)
