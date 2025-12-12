import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.report import Report # type: ignore
from SimpleSEDML.task import Task # type: ignore
from SimpleSEDML.model import Model # type: ignore
from SimpleSEDML.simulation import Simulation # type: ignore

import pandas as pd; # type: ignore
import os
import phrasedml # type: ignore
import unittest
import tellurium as te # type: ignore


IGNORE_TEST = False
IS_PLOT = False
MODEL_ID = "model1"
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
""" % MODEL_ID
MODEL_SBML = te.antimonyToSBML(MODEL_ANT)
SBML_FILE_PATH = os.path.join(cn.PROJECT_DIR, MODEL_ID)
WOLF_FILE = "Wolf2000_Glycolytic_Oscillations"
REMOVE_FILES = [SBML_FILE_PATH, WOLF_FILE]
TITLE = "report"


#############################
def execute(phrasedml_str:str)->pd.DataFrame:
    """Evaluate the sedml_str and sbml_str

    Args:
        phrasedml_str (str): phraSED-ML string
    """
    sedml_str = phrasedml.convertString(phrasedml_str)
    try:
        te.executeSEDML(sedml_str)
        return te.getLastReport()  # type: ignore
    except Exception as e:
        raise RuntimeError(f"SED-ML execution failed: {e}")

def assemble(*args):
        directives = ""
        for arg in args:
            directives += "\n" + "".join(str(arg))
        return directives


#############################
# Tests
#############################
class TestReport(unittest.TestCase):

    def setUp(self):
        self.remove()
        self.report = Report(metadata={'a': 1}, title=TITLE)

    def tearDown(self):
        # Remove files if they exist
        self.remove()

    def remove(self):
        # Remove files if they exist
        for file in REMOVE_FILES:
            if os.path.exists(file):
                os.remove(file)

    def testConstructor(self):
        # task = task task1 run simulation1 on model1
        if IGNORE_TEST:
            return
        self.assertTrue(isinstance(self.report, Report), "Report object not created.")
        self.assertEqual(self.report.title, TITLE, f"Title not set correctly. Expected {TITLE}, got {self.report.title}")

    def testAddVariables(self):
        if IGNORE_TEST:
            return
        self.report.addVariables("time", "task1.S1", "S2", "S3", "S4")
        self.assertTrue("task1.S1" in self.report.variables, "task1.S1 not in report variables.")
        self.assertTrue("S2" in self.report.variables, "S2 not in report variables.")
        self.assertTrue("S3" in self.report.variables, "S3 not in report variables.")
        self.assertTrue("S4" in self.report.variables, "S4 not in report variables.")

    def testExecute(self):
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_SBML, is_overwrite=True)
        simulation = Simulation("simulation1", "uniform", 0, 10, 100)
        task = Task("task1", model.id, simulation.id)
        self.report.addVariables("time", "S1", "S2", "S3", "S4")
        phrasedml_str = assemble(str(model), str(simulation), str(task), str(self.report))
        result_df = execute(phrasedml_str)
        self.assertTrue(isinstance(result_df, pd.DataFrame), "Result is not a DataFrame.")
        self.assertTrue("S1" in result_df.columns, "S1 not in result DataFrame.")
        self.assertTrue("S2" in result_df.columns, "S2 not in result DataFrame.")
        self.assertTrue("S3" in result_df.columns, "S3 not in result DataFrame.")
        self.assertTrue("S4" in result_df.columns, "S4 not in result DataFrame.")
        self.assertTrue("time" in result_df.columns, "time not in result DataFrame.")


if __name__ == '__main__':
    unittest.main()