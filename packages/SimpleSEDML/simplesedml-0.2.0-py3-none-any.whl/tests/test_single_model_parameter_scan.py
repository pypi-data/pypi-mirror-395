import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.single_model_parameter_scan import SingleModelParameterScan # type: ignore

import numpy as np # type: ignore
import os
import pandas as pd # type: ignore
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

#############################
# Tests
#############################
class TestSingleModelTimeCourse(unittest.TestCase):

    def make(self, simulation_type:str=cn.ST_STEADYSTATE, time_interval:float=-1):
        return SingleModelParameterScan(
            model_ref=MODEL_ANT,
            #scan_parameter_dct={"k1": [0.1, 0.2, 0.3], "k2": [0.2, 0.3, 0.4]}, 
            scan_parameter_dct={"k2": [0.2, 0.3, 0.4]}, 
            project_id="test_project",
            simulation_type=simulation_type,
            display_variables=["S1", "S4"],
            time_interval=time_interval,
            title="Test Single Model Parameter Scan",
            is_plot=IS_PLOT
        )

    def evaluate(self, smps:SingleModelParameterScan):
        """Evaluate the sedml_str and sbml_str

        Args:
            phrasedml_str (str): phraSED-ML string
        """
        try:
            phrasedml_str = smps.getPhraSEDML()
            self.assertIsNotNone(phrasedml_str, "SED-ML string is None.")
        except Exception as e:
            self.assertTrue(False, f"Failed to get phraSED-ML: {e}")
        try: 
            sedml_str = smps.getSEDML()
            self.assertIsNotNone(sedml_str, "SED-ML string is None.")
        except Exception as e:
            self.assertTrue(False, f"Failed to get SED-ML: {e}")
        try:
            df = smps.execute()
            self.assertIsInstance(df, pd.DataFrame, "Execution did not return a DataFrame.")
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")

    def testOnestep(self):
        if IGNORE_TEST:
            return
        smps = self.make(cn.ST_ONESTEP, time_interval=10)
        self.evaluate(smps)

    def testSteadyState(self):
        if IGNORE_TEST:
            return
        smps = self.make(cn.ST_STEADYSTATE, time_interval=10)
        with self.assertRaises(NotImplementedError):
            smps.execute()

    def testBug(self):
        """Bug with labels"""
        if IGNORE_TEST:
            return
        smps = SingleModelParameterScan(cn.WOLF_URL, simulation_type="onestep",
                project_id="Wolf", title="Wolf",
                time_interval=10, display_variables=["at", "na"],
                scan_parameter_dct=dict(k1=[50, 550, 5000]), is_plot=IS_PLOT)
        _ = smps.execute()


if __name__ == '__main__':
    unittest.main()