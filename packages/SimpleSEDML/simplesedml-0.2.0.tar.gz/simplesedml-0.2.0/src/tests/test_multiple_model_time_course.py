import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.multiple_model_time_course import MultipleModelTimeCourse # type:ignore
from SimpleSEDML.simulation import Simulation # type:ignore
from SimpleSEDML.task import Task # type:ignore
from SimpleSEDML.model import Model # type:ignore
from SimpleSEDML.plot import Plot # type:ignore
from SimpleSEDML.report import Report # type:ignore

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
NUM_POINT = 100
MODEL_REFS = [MODEL_SBML, MODEL2_ANT]
START = 1
END = 15
NUM_POINT = 350
MODEL_PARAMETER_DCT = {"k1":0.1, "k2":0.3}


#############################
# Tests
#############################
class TestMultipleModelTimeCourse(unittest.TestCase):

    def setUp(self):
        self.remove_files = list(REMOVE_FILES)
        self.remove()
        self.model_refs = MODEL_REFS
        self.mmtc = MultipleModelTimeCourse(
                model_refs=self.model_refs,
                project_id="test_mmtc",
                project_dir=cn.TEST_DIR,
                simulation_type=cn.ST_UNIFORM,
                start=START,
                end=END,
                num_point=NUM_POINT,
                display_variables=DISPLAY_VARIABLES,
                is_plot=IS_PLOT,
                model_parameter_dct=MODEL_PARAMETER_DCT)
        self.num_model = len(self.model_refs)

    def tearDown(self):
        # Remove files if they exist
        self.remove_files.extend(self.mmtc._model_sources)
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
        self.assertTrue(isinstance(self.mmtc, MultipleModelTimeCourse))
        self.assertEqual(self.mmtc.project_id, "test_mmtc")
        self.assertEqual(self.mmtc.project_dir, cn.TEST_DIR)
        self.assertEqual(self.mmtc.simulation_type, cn.ST_UNIFORM)
        self.assertEqual(self.mmtc.start, START)
        self.assertEqual(self.mmtc.end, END)
        self.assertEqual(self.mmtc.num_point, NUM_POINT)
        self.assertEqual(self.mmtc.model_parameter_dct, MODEL_PARAMETER_DCT)
        self.assertEqual(self.mmtc.model_refs, MODEL_REFS)

    def testMakeNullModelObjects(self):
        if IGNORE_TEST:
            return
        mmtc = MultipleModelTimeCourse(is_plot=IS_PLOT)
        for model_ref in MODEL_REFS:
            mmtc.addModel(model_ref)
        self.evaluate(mmtc)

    def testMakeSimulationObject(self):
        """Test the makeSimulationObject method"""
        if IGNORE_TEST:
            return
        self.mmtc.makeSimulationObject()
        simulation = list(self.mmtc.simulation_dct.values())[0]
        self.assertTrue(isinstance(simulation, Simulation))
        self.assertTrue(str(NUM_POINT-1) in simulation.getPhraSEDML())

    def testMakeTaskID(self):
        """Test the makeTaskID method"""
        if IGNORE_TEST:
            return
        task_id = self.mmtc._makeTaskID(MODEL_ID, "t")
        self.assertEqual(task_id, "tmodel1")

    def testMakeModelObject(self):
        """Test the makeModelObject method"""
        if IGNORE_TEST:
            return
        self.mmtc.makeModelObjects()
        self.assertEqual(len(self.mmtc.model_dct), len(MODEL_REFS))
        trues = [m in ["model0", "model1"] for m in self.mmtc.model_dct.keys()]
        self.assertTrue(all(trues))

    def testMakeTaskObjects(self):
        """Test the makeTaskObject method"""
        if IGNORE_TEST:
            return
        self.mmtc.makeModelObjects()
        self.mmtc.makeSimulationObject()
        self.mmtc.makeTaskObjects()
        task = list(self.mmtc.task_dct.values())[0]
        self.assertTrue(isinstance(task, Task))
        self.assertTrue(task.id == cn.TASK_PREFIX + "model0")

    def testDisplayVariables(self):
        """Test the makeTaskObject method"""
        if IGNORE_TEST:
            return
        self.mmtc.makeModelObjects()
        if self.mmtc.initial_display_variables is None:
            raise ValueError("Display variables are not set.")
        self.assertEqual(self.mmtc.initial_display_variables[0], "S1")
        self.assertEqual(self.mmtc.initial_display_variables[1], "S2")
        #
        mmtc = MultipleModelTimeCourse(self.model_refs, is_plot=IS_PLOT,
                display_variables=["S1", "S2", "S3"])
        mmtc.makeModelObjects()
        self.remove_files.extend(mmtc._model_sources)
        if mmtc.initial_display_variables is None:
            raise ValueError("Display variables are not set.")
        self.assertEqual(mmtc.initial_display_variables[0], "S1")
        self.assertEqual(mmtc.initial_display_variables[1], "S2")
        self.assertEqual(mmtc.initial_display_variables[2], "S3")

    def testMakeReportObject(self):
        """Test the makeTaskObject method"""
        if IGNORE_TEST:
            return
        self.mmtc.makeModelObjects()
        self.mmtc.makeSimulationObject()
        self.mmtc.makeTaskObjects()
        self.mmtc.makeReportObject()
        report_directive = list(self.mmtc.report_dct.values())[0]
        self.assertEqual(str(report_directive).count("S1"), 2)
        self.assertEqual(str(report_directive).count("S2"), 2)

    def testStochasticSimulation(self):
        """Test the makeTaskObject method"""
        if IGNORE_TEST:
            return
        plot_dct = {cn.ST_UNIFORM_STOCHASTIC: IS_PLOT,
                    cn.ST_ONESTEP: False,
                    cn.ST_STEADYSTATE: False}
        for simulation_type, is_plot in plot_dct.items():
            mmtc = MultipleModelTimeCourse(MODEL_REFS,
                    simulation_type=simulation_type,
                    start=0,
                    end=10,
                    num_point=NUM_POINT,
                    model_parameter_dct=dict(k1=1.5),
                    display_variables=DISPLAY_VARIABLES,
                    is_plot=is_plot)
            self.evaluate(mmtc)

    def testMakePlotObject(self):
        """Test the makeTaskObject method"""
        if IGNORE_TEST:
            return
        self.mmtc.makeSimulationObject()
        self.mmtc.makeModelObjects()
        self.mmtc.makeTaskObjects()
        self.mmtc.makePlotObjects()
        # Variable plots may not appear in sequence
        directives = [str(v) for v in self.mmtc.plot_dct.values()]
        for idx in range(len(self.mmtc.plot_dct)):
            variable_name = "S" + str(idx + 1)
            true = any([variable_name in directive for directive in directives])
            self.assertTrue(true)

    def testExecute(self):
        if IGNORE_TEST:
            return
        self.evaluate(self.mmtc)
        self.evaluate(self.mmtc)  # Ensure works with repeated calls

    def testLegendBug(self):
        """Test the legend bug with multiple models"""
        if IGNORE_TEST:
            return
        mmtc = MultipleModelTimeCourse([MODEL_ANT, MODEL2_ANT],
                model_parameter_dct=dict(k1=10), num_point=100, is_plot=IS_PLOT)
        mmtc.execute()
        self.evaluate(mmtc)

    def evaluate(self, mmtc:MultipleModelTimeCourse):
        """Evaluate the sedml_str and sbml_str

        Args:
            phrasedml_str (str): phraSED-ML string
        """
        phrasedml_str = mmtc.getPhraSEDML()
        sedml_str = phrasedml.convertString(phrasedml_str)
        self.assertIsNotNone(sedml_str, "SED-ML conversion failed\n" + phrasedml.getLastError())
        try:
            df = mmtc.execute()
            self.assertTrue(isinstance(df, pd.DataFrame))
            if not (cn.ST_ONESTEP in phrasedml_str or cn.ST_STEADYSTATE in phrasedml_str):
                self.assertTrue(len([c for c in df.columns if cn.TIME in c]) == 1)
                self.assertTrue(len(df) > 0, "DataFrame is empty")
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")


if __name__ == '__main__':
    unittest.main()