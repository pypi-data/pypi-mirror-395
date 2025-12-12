import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.single_model_time_course import SingleModelTimeCourse # type: ignore

import numpy as np # type: ignore
import os
import pandas as pd # type: ignore
import phrasedml # type: ignore
import unittest
import tellurium as te # type: ignore


IGNORE_TEST = True
IS_PLOT = False
MODEL_NAME = "model1"
MODEL_ANT = """
model %s
    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
    S3 -> S4; k3*S3

    S1 is "Species 1"

    k1 = 0.1
    k2 = 0.2
    k3 = 0.3
    S1 = 10
    S2 = 0
    S3 = 0
    S4 = 0
end
""" % MODEL_NAME
MODEL2_NAME = "model2"
MODEL2_ANT = """
model %s
    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
    S3 -> S4; k3*S3
    S4 -> S5; k4*S3

    k1 = 0.1
    k2 = 0.2
    k3 = 0.3
    k4 = 0.3
    S1 = 10
    S2 = 0
    S3 = 0
    S4 = 0
    S5 = 0
end
""" % MODEL2_NAME
MODEL_SBML = te.antimonyToSBML(MODEL_ANT)
SBML_FILE_PATH = os.path.join(cn.PROJECT_DIR, MODEL_NAME)
REMOVE_FILES = [SBML_FILE_PATH]
WOLF_URL = "https://www.ebi.ac.uk/biomodels/services/download/get-files/MODEL3352181362/3/BIOMD0000000206_url.xml"

#############################
# Tests
#############################
class TestSingleModelTimeCourse(unittest.TestCase):

    def setUp(self):
        self.remove_files = list(REMOVE_FILES)
        self.remove()

    def tearDown(self):
        # Remove files if they exist
        self.remove()

    def remove(self):
        # Remove files if they exist
        for file in self.remove_files:
            if os.path.exists(file):
                os.remove(file)

    def evaluate(self, smtc:SingleModelTimeCourse):
        """Evaluate the sedml_str and sbml_str

        Args:
            phrasedml_str (str): phraSED-ML string
        """
        try:
            smtc.execute()
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")

    def testMakeSingleModelTimeCourse(self):
        #if IGNORE_TEST:
        #    return
        smtc = None
        try:
            smtc = SingleModelTimeCourse(MODEL_ANT, num_point=200, is_plot=IS_PLOT)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        try:
            smtc = SingleModelTimeCourse(MODEL_ANT,
                    display_variables=["time", "S1", "S2"], start=0, end=10, num_step=100,
                    is_plot=IS_PLOT)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        try:
            smtc = SingleModelTimeCourse(MODEL_ANT, title="my plot", is_plot=IS_PLOT)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        try:
            smtc = SingleModelTimeCourse(WOLF_URL, title="Wolf2000", is_plot=IS_PLOT)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        try:
            smtc = SingleModelTimeCourse(WOLF_URL, ref_type="sbml_url", title="Wolf2000",
                    num_point=200, is_plot=IS_PLOT)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        if smtc is None:
            self.assertTrue(False, "SingleModelTimeCourse object is None")
        else:
            self.remove_files.extend(smtc._model_sources)
            _ = smtc.execute()


if __name__ == '__main__':
    unittest.main()