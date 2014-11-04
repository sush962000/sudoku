#!/usr/bin/env python

import os
import sys
import unittest

import sudoku


class BoardTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass


class SolverTest(unittest.TestCase):
  def setUp(self):
    pass

  def tearDown(self):
    pass

def generate_solver_test(filepath):
  def test(self):
    with open(filepath) as f:
      grid_in = sudoku.read(f)
      self.assertIsNotNone(grid_in)

      grid_out = sudoku.solve(grid_in)
      self.assertIsNotNone(grid_out)
  return test


if __name__ == '__main__':
  # Generate one test function for each test board.
  script_dir = os.path.dirname(os.path.realpath(__file__))
  test_dir = os.path.join(script_dir, 'test')
  test_files = [f for f in os.listdir(test_dir)
      if os.path.isfile(os.path.join(test_dir, f))
      and f.endswith('.csv')]
  for filename in test_files:
    test_func = generate_solver_test(os.path.join(test_dir, filename))
    setattr(SolverTest, 'test_{0}'.format(filename), test_func)

  unittest.main()
