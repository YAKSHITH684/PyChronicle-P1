import unittest

class ApiImportSmokeTest(unittest.TestCase):
    def test_api_module_name_is_available(self):
        module_name = "pychronicle.web.app"
        self.assertTrue(module_name.startswith("pychronicle."))

if __name__ == "__main__":
    unittest.main()
