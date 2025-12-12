import unittest

def suite():
    loader = unittest.TestLoader()


    suite = loader.discover('.', pattern='test_*.py')

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
