import SimpleSEDML.constants as cn # type: ignore
import SimpleSEDML.utils as utils # type: ignore

import phrasedml # type: ignore
import pandas as pd; # type: ignore
import os
import unittest


SBML_PATH = os.path.join(cn.TEST_DIR, "BIOMD0000000206.xml")

IGNORE_TEST = False
IS_PLOT = False

#############################
# Tests
#############################
class TestFunctions(unittest.TestCase):

    def testMakeDefaultProjectDir(self):
        if IGNORE_TEST:
            return
        project_dir = utils.makeDefaultProjectDir(None)
        self.assertTrue(os.path.exists(project_dir))
        self.assertTrue(os.path.isdir(project_dir))
        # Clean up
        os.rmdir(project_dir)

    def testMakeDisplayNameDct(self):
        if IGNORE_TEST:
            return
        display_name_dct = utils.makeDisplayNameDct(SBML_PATH)
        self.assertTrue(isinstance(display_name_dct, dict))
        self.assertGreater(len(display_name_dct), 0)
        self.assertEqual(display_name_dct['s1'], "Glucose")
        # Check that the keys are strings
        for key in display_name_dct.keys():
            self.assertTrue(isinstance(key, str))
        # Check that the values are strings
        for value in display_name_dct.values():
            self.assertTrue(isinstance(value, str))


if __name__ == '__main__':
    unittest.main()