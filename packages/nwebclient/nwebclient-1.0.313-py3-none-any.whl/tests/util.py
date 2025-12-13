import unittest

from nwebclient import util as u

class BaseTestCase(unittest.TestCase):
    
    def test_Args(self):
        args = u.Args.from_cmd('docker run -it --name myubuntu')
        self.assertEqual(args['name'], 'myubuntu')

    def test_flatten_dict(self):
        nested = {
            'a': {'sub': 1},
            'b': {'x': {'y': 2}},
            'c': 3
        }
        expected = {
            'a_sub': 1,
            'b_x_y': 2,
            'c': 3
        }
        result = u.flatten_dict(nested)
        self.assertEqual(result, expected)

    def test_load_class(self):
        print("test_load_class")
        obj = u.load_class('nwebclient.runner:NamedJobs', True, {}, u.Args())
        self.assertTrue(isinstance(obj.args, u.Args))


if __name__ == '__main__':
    unittest.main()
