import unittest

import sidecar_terminator


class MainTest(unittest.TestCase):

    def test_without_processes(self):
        self.assertRaises(TypeError, sidecar_terminator.watch)
