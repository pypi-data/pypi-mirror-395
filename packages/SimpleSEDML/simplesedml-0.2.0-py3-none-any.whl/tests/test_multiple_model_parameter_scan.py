import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.multiple_model_parameter_scan import MultipleModelParameterScan # type:ignore
from SimpleSEDML.simulation import Simulation # type:ignore
from SimpleSEDML.task import RepeatedTask # type:ignore

import pandas as pd; # type: ignore
import os
import phrasedml # type: ignore
import shutil  # type: ignore
import tellurium as te # type: ignore
import unittest


IGNORE_TEST = False
IS_PLOT = False
MODEL_ID = "model1"
MODEL2_ID = "model2"
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

    S1 is "species1"
    S2 is "species2"
end
""" % MODEL_ID
MODEL2_ANT = """
model %s
    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
    S3 -> S4; k3*S3
    S3 -> S1; k3*S3

    k1 = 0.1
    k2 = 0.2
    k3 = 0.3
    S1 = 10
    S2 = 0
    S3 = 0
    S4 = 0
end
""" % MODEL2_ID
MODEL_SBML = te.antimonyToSBML(MODEL_ANT)
SBML_FILE_PATH = os.path.join(cn.PROJECT_DIR, MODEL_ID)
WOLF_FILE = "Wolf2000_Glycolytic_Oscillations"
REMOVE_FILES = [SBML_FILE_PATH, WOLF_FILE]
OMEX_DIR = os.path.join(cn.TEST_DIR, "omex")
OMEX_PROJECT_DIR = os.path.join(cn.TEST_DIR, "project")
REMOVE_DIRS = [OMEX_DIR, OMEX_PROJECT_DIR]
DISPLAY_VARIABLES = ["S1", "S2"]
SCAN_PARAMETER_DF = pd.DataFrame({"k1":[0.1, 0.2], "k2":[0.2, 0.3]})
NUM_POINT = 100
MODEL_REFS = [MODEL_SBML, MODEL2_ANT]
TIME_INTERVAL = 10  # Default time interval for simulations



#############################
# Tests
#############################
class TestMultipleModelParameterScan(unittest.TestCase):

    def setUp(self):
        self.remove_files = list(REMOVE_FILES)
        self.remove()
        self.model_refs = MODEL_REFS
        self.mmps = MultipleModelParameterScan(
                SCAN_PARAMETER_DF,
                model_refs=self.model_refs,
                project_id="test_project",
                time_interval=TIME_INTERVAL,
                model_parameter_dct=dict(k1=1.5),
                display_variables=DISPLAY_VARIABLES,
                is_plot=IS_PLOT)
        self.num_model = len(self.model_refs)

    def tearDown(self):
        # Remove files if they exist
        self.remove_files.extend(self.mmps._model_sources)
        self.remove()

    def remove(self):
        # Remove files if they exist
        for file in self.remove_files:
            if os.path.exists(file):
                os.remove(file)
        for directory in REMOVE_DIRS:
            if os.path.exists(directory):
                shutil.rmtree(directory)

    def testConstructor(self):
        """Test the constructor of MultipleModelTimeCourse"""
        if IGNORE_TEST:
            return
        self.assertEqual(self.mmps.time_interval, TIME_INTERVAL)

    def testNullConstructor(self):
        """Test the constructor of MultipleModelTimeCourse"""
        if IGNORE_TEST:
            return
        mmps = MultipleModelParameterScan(SCAN_PARAMETER_DF, is_plot=IS_PLOT)
        for model_ref in MODEL_REFS:
            mmps.addModel(model_ref)
        mmps.execute()

    def testMakeSimulationObject(self):
        """Test the makeSimulationObject method"""
        if IGNORE_TEST:
            return
        self.mmps.makeSimulationObject()
        simulation = list(self.mmps.simulation_dct.values())[0]
        self.assertTrue(isinstance(simulation, Simulation))

    def testMakeTaskID(self):
        """Test the makeTaskID method"""
        if IGNORE_TEST:
            return
        task_id = self.mmps._makeTaskID(MODEL_ID, "rt")
        self.assertEqual(task_id, "rtmodel1")

    def testMakeModelObject(self):
        """Test the makeModelObject method"""
        if IGNORE_TEST:
            return
        self.mmps.makeModelObjects()
        self.assertEqual(len(self.mmps.model_dct), len(MODEL_REFS))
        trues = [m in ["model0", "model1"] for m in self.mmps.model_dct.keys()]
        self.assertTrue(all(trues))

    def testMakeTaskObjects(self):
        """Test the makeTaskObject method"""
        #if IGNORE_TEST:
        #    return
        self.mmps.makeModelObjects()
        self.mmps.makeSimulationObject()
        self.mmps.makeTaskObjects()
        repeated_task = list(self.mmps.repeated_task_dct.values())[0]
        self.assertTrue(isinstance(repeated_task, RepeatedTask))
        self.assertTrue(repeated_task.id == f"{cn.REPEATED_TASK_PREFIX}model0")

    def testMakeReportObject(self):
        """Test the makeTaskObject method"""
        #if IGNORE_TEST:
        #    return
        self.mmps.makeModelObjects()
        self.mmps.makeSimulationObject()
        self.mmps.makeTaskObjects()
        self.mmps.makeReportObject()
        report_directive = list(self.mmps.report_dct.values())[0]
        self.assertEqual(str(report_directive).count("S1"), 2)
        self.assertEqual(str(report_directive).count("S2"), 2)

    def testMakePlotObject(self):
        """Test the makeTaskObject method"""
        if IGNORE_TEST:
            return
        self.mmps.makeModelObjects()
        self.mmps.makeTaskObjects()
        self.mmps.makePlotObjects()
        # Variable plots may not appear in sequence
        directives = [str(v) for v in self.mmps.plot_dct.values()]
        for idx in range(len(self.mmps.plot_dct)):
            variable_name = "S" + str(idx + 1)
            true = any([directive.find(variable_name) > 0 for directive in directives])
            self.assertTrue(true)

    def testExecute(self):
        if IGNORE_TEST:
            return
        self.evaluate(self.mmps)
        self.evaluate(self.mmps)  # Ensure works with repeated calls

    def evaluate(self, mmps:MultipleModelParameterScan):
        """Evaluate the sedml_str and sbml_str

        Args:
            phrasedml_str (str): phraSED-ML string
        """
        phrasedml_str = mmps.getPhraSEDML()
        sedml_str = phrasedml.convertString(phrasedml_str)
        self.assertIsNotNone(sedml_str, "SED-ML conversion failed\n" + phrasedml.getLastError())
        try:
            df = mmps.execute()
            self.assertTrue(isinstance(df, pd.DataFrame))
            if not (cn.ST_ONESTEP in phrasedml_str or cn.ST_STEADYSTATE in phrasedml_str):
                self.assertTrue(len([c for c in df.columns if cn.TIME in c]) == 1)
                self.assertTrue(df.shape[0] == NUM_POINT)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")


if __name__ == '__main__':
    unittest.main()