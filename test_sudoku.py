#!/usr/bin/env python

import os
import sys
import unittest

import sudoku


class BoardTest(unittest.TestCase):
  def test_blank(self):
    blank = sudoku.Board.blank()
    for i in range(9):
      for j in range(9):
        self.assertEqual(blank.cell(i, j), '123456789')

  def test_peer_len(self):
    for i in range(9):
      for j in range(9):
        peers = [peer for peer in sudoku.Board.peers(i, j)]
        self.assertEqual(len(peers), 20)

  def test_peers_21(self):
    expected = [
        (2, 0), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
        (0, 1), (1, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1),
        (0, 0), (0, 2), (1, 0), (1, 2)]
    peers = [peer for peer in sudoku.Board.peers(2, 1)]
    self.assertEqual(peers, expected)

  def test_assign(self):
    blank = sudoku.Board.blank()
    # Assigning values outside [1, 9] must fail
    self.assertFalse(blank.assign(2, 1, '0'))
    self.assertFalse(blank.assign(2, 1, '10'))
    # Assigning valid values must pass
    self.assertTrue(blank.assign(2, 1, '1'))
    self.assertTrue(blank.assign(2, 0, '2'))
    # Assiging the same value to any peer must fail
    self.assertFalse(blank.assign(2, 8, '2'))


class SolverTest(unittest.TestCase):
  def setUp(self):
    pass

def generate_solver_test(filepath):
  def test(self):
    with open(filepath) as f:
      grid_in = sudoku.read(f)
      self.assertIsNotNone(grid_in)

    grid_out = sudoku.solve(grid_in)
    self.assertIsNotNone(grid_out)

    filename, ext = os.path.splitext(filepath)
    expectation_filepath = filename + '_expected.csv'
    with open(expectation_filepath) as f:
      grid_expected = sudoku.read(f)
      self.assertEqual(grid_out, grid_expected)
  return test


if __name__ == '__main__':
  # Generate one test function for each test board.
  script_dir = os.path.dirname(os.path.realpath(__file__))
  test_dir = os.path.join(script_dir, 'test')
  test_files = [f for f in os.listdir(test_dir)
      if os.path.isfile(os.path.join(test_dir, f))
      and f.endswith('.csv')
      and not 'expected' in f]
  for filename in test_files:
    test_func = generate_solver_test(os.path.join(test_dir, filename))
    setattr(SolverTest, 'test_{0}'.format(filename), test_func)

  unittest.main()
