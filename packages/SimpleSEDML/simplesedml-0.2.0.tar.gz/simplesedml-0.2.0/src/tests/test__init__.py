'''Tests the API'''

import SimpleSEDML as ss  # type: ignore

import numpy as np # type: ignore
import os
import pandas as pd # type: ignore
import phrasedml # type: ignore
import unittest
import tellurium as te # type: ignore


IGNORE_TEST = False
IS_PLOT = False
MODEL_NAME = "model1"
MODEL_ANT = """
model %s
    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
    S3 -> S4; k3*S3

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
SBML_FILE_PATH = os.path.join(ss.cn.PROJECT_DIR, MODEL_NAME)
REMOVE_FILES = [SBML_FILE_PATH]
WOLF_URL = "https://www.ebi.ac.uk/biomodels/services/download/get-files/MODEL3352181362/3/BIOMD0000000206_url.xml"

#############################
# Tests
#############################
class TestSimpleSEDML(unittest.TestCase):

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

    def evaluate(self, phrasedml_str:str):
        """Evaluate the sedml_str and sbml_str

        Args:
            phrasedml_str (str): phraSED-ML string
        """
        sedml_str = phrasedml.convertString(phrasedml_str)
        try:
            te.executeSEDML(sedml_str)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")

    def testGetModelInformation(self):
        if IGNORE_TEST:
            return
        model_information = ss.getModelInformation(MODEL_ANT)
        self.assertTrue(model_information.model_name == MODEL_NAME)

    def testMakeSingleModelTimeCourse(self):
        if IGNORE_TEST:
            return
        smtc = None
        try:
            smtc = ss.makeSingleModelTimeCourse(MODEL_ANT)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        try:
            smtc = ss.makeSingleModelTimeCourse(MODEL_ANT,
                    display_variables=["time", "S1", "S2"], start=0, end=10, num_step=100)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        try:
            smtc = ss.makeSingleModelTimeCourse(MODEL_ANT, title="my plot")
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        try:
            smtc = ss.makeSingleModelTimeCourse(WOLF_URL, title="Wolf2000")
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        try:
            smtc = ss.makeSingleModelTimeCourse(WOLF_URL, ref_type="sbml_url", title="Wolf2000")
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        if smtc is not None:
            self.remove_files.extend(smtc._model_sources)
            if IS_PLOT:
                _ = smtc.execute()

    def testMakeMultipleModelTimeCourse(self):
        if IGNORE_TEST:
            return
        mmtc = None
        try:
            mmtc = ss.makeMultipleModelTimeCourse(
                    [MODEL_ANT, MODEL2_ANT],
                    start=0,
                    end=10,
                    num_step=100,
                    model_parameter_dct=dict(k1=1.5),
                    display_variables=["S1", "S2"],
                    is_plot=IS_PLOT,
                    )
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")
        if mmtc is not None:
            if IS_PLOT:
                _ = mmtc.execute()


if __name__ == '__main__':
    unittest.main()