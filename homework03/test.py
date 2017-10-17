import unittest
import random
import json

from life import GameOfLife


class TestGameOfLife(unittest.TestCase):

    def setUp(self):
        self.grid = [
            [1,1,0,0,1,1,1,1],
            [0,1,1,1,1,1,1,0],
            [1,0,1,1,0,0,0,0],
            [1,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,0,0],
            [1,1,1,1,0,1,1,1]
        ]
        self.height = 6
        self.width = 8

    def test_can_create_an_empty_grid(self):
        game = GameOfLife(width=3, height=3, cell_size=1)
        grid = game.cell_list(randomize=False)
        self.assertEqual([[0,0,0], [0,0,0], [0,0,0]], grid)

    def test_can_create_a_random_grid(self):
        game = GameOfLife(width=3, height=3, cell_size=1)
        random.seed(12345)
        grid = game.cell_list(randomize=True)
        self.assertEqual([[1,0,1], [1,0,1], [1,0,1]], grid)

    def test_get_neighbours(self):
        game = GameOfLife(width=self.width, height=self.height, cell_size=1)
        game.grid = self.grid
        neighbours = game.get_neighbours((2,3))
        self.assertEqual(8, len(neighbours))
        self.assertEqual(4, sum(neighbours))

    def test_get_neighbours_for_upper_left_corner(self):
        game = GameOfLife(width=self.width, height=self.height, cell_size=1)
        game.grid = self.grid
        neighbours = game.get_neighbours((0,0))
        self.assertEqual(3, len(neighbours))
        self.assertEqual(2, sum(neighbours))

    def test_get_neighbours_for_upper_right_corner(self):
        game = GameOfLife(width=self.width, height=self.height, cell_size=1)
        game.grid = self.grid
        neighbours = game.get_neighbours((0,7))
        self.assertEqual(3, len(neighbours))
        self.assertEqual(2, sum(neighbours))

    def test_get_neighbours_for_lower_left_corner(self):
        game = GameOfLife(width=self.width, height=self.height, cell_size=1)
        game.grid = self.grid
        neighbours = game.get_neighbours((5,0))
        self.assertEqual(3, len(neighbours))
        self.assertEqual(2, sum(neighbours))

    def test_get_neighbours_for_lower_right_corner(self):
        game = GameOfLife(width=self.width, height=self.height, cell_size=1)
        game.grid = self.grid
        neighbours = game.get_neighbours((5,7))
        self.assertEqual(3, len(neighbours))
        self.assertEqual(1, sum(neighbours))

    def test_can_update(self):
        game = GameOfLife(width=self.width, height=self.height, cell_size=1)
        game.grid = self.grid

        with open('steps.txt') as f:
            steps = json.load(f)

        num_updates = 0
        for step in sorted(steps.keys(), key=int):
            with self.subTest(step=step):
                for _ in range(int(step)-num_updates):
                    game.grid = game.update_cell_list(game.grid)
                self.assertEqual(steps[step], game.grid)
            num_updates += int(step)


loader = unittest.TestLoader()
suite = loader.loadTestsFromTestCase(TestGameOfLife)

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)