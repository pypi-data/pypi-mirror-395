import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.plot import Plot # type: ignore
from SimpleSEDML.task import Task # type: ignore
from SimpleSEDML.model import Model # type: ignore
from SimpleSEDML.simulation import Simulation # type: ignore

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
TITLE = "my plot"


#############################
def execute(phrasedml_str:str):
    """Evaluate the sedml_str and sbml_str

    Args:
        phrasedml_str (str): phraSED-ML string
    """
    sedml_str = phrasedml.convertString(phrasedml_str)
    try:
        te.executeSEDML(sedml_str)
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
class TestPlot(unittest.TestCase):

    def setUp(self):
        self.remove()
        self.plot = Plot("time", "S1", title=TITLE, is_plot=IS_PLOT)

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
        self.assertTrue(isinstance(self.plot, Plot), "Plot object not created.")
        self.assertEqual(self.plot.title, TITLE, f"Title not set correctly. Expected {TITLE}, got {self.plot.title}")

    def testMultipleYvariables(self):
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_SBML, is_overwrite=True)
        simulation = Simulation("simulation1", "uniform", 0, 10, 100)
        task = Task("task1", model.id, simulation.id)
        plot = Plot("time", ["S1", "S2"], title="2D: time vs S1, S2", is_plot=IS_PLOT)
        phrasedml_str = assemble(model.getPhraSEDML(), simulation.getPhraSEDML(),
                                    task.getPhraSEDML(), plot.getPhraSEDML())
        execute(phrasedml_str)

    def testXYZ(self):
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_SBML, is_overwrite=True)
        simulation = Simulation("simulation1", "uniform", 0, 10, 100)
        task = Task("task1", model.id, simulation.id)
        plot = Plot("time", "S1", "S2", title="3d: time, S1, S2.", is_plot=IS_PLOT)
        phrasedml_str = assemble(model.getPhraSEDML(), simulation.getPhraSEDML(),
                                    task.getPhraSEDML(), plot.getPhraSEDML())
        execute(phrasedml_str)


if __name__ == '__main__':
    unittest.main()