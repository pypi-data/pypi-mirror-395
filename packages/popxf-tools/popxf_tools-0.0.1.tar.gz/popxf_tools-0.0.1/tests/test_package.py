import unittest

class TestPackage(unittest.TestCase):

    def test_import(self):
        try:
            import popxf.tools as tools
        except ImportError:
            self.fail("Importing popxf.tools failed.")
        else:
            self.assertIsNotNone(tools)

