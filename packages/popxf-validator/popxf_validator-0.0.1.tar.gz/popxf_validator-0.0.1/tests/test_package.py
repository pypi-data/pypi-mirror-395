import unittest

class TestPackage(unittest.TestCase):

    def test_import(self):
        try:
            import popxf.validator as validator
        except ImportError:
            self.fail("Importing popxf.validator failed.")
        else:
            self.assertIsNotNone(validator)

