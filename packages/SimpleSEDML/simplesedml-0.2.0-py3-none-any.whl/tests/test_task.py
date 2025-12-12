import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.task import Task, RepeatedTask # type: ignore
from SimpleSEDML.model import Model # type: ignore
from SimpleSEDML.simulation import Simulation # type: ignore

import pandas as pd; # type: ignore
import os
import phrasedml # type: ignore
import unittest
import tellurium as te # type: ignore
from typing import Optional, List, Tuple, Union


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


#############################
def evaluate(phrasedml_str:str):
    """Evaluate the sedml_str and sbml_str

    Args:
        phrasedml_str (str): phraSED-ML string
    """
    sedml_str = phrasedml.convertString(phrasedml_str)
    try:
        te.executeSEDML(sedml_str)
        return True, ""
    except Exception as e:
        return False, f"SED-ML execution failed: {e}"

def assemble(*args):
        return "\n".join([arg.getPhraSEDML() for arg in args])


#############################
# Tests
#############################
class TestTask(unittest.TestCase):

    def setUp(self):
        self.remove()

    def tearDown(self):
        # Remove files if they exist
        self.remove()

    def remove(self):
        # Remove files if they exist
        for file in REMOVE_FILES:
            if os.path.exists(file):
                os.remove(file)

    def testTask(self):
        # task = task task1 run simulation1 on model1
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_SBML, is_overwrite=True)
        simulation = Simulation("simulation1", "uniform", 0, 10, 100)
        task = Task("task1", model.id, simulation.id)
        phrasedml_str = assemble(model, simulation, task)
        result, explanation_str = evaluate(phrasedml_str)
        self.assertTrue(result, explanation_str)
    
class TestRepeatedTask(unittest.TestCase):

    def setUp(self):
        self.remove()

    def tearDown(self):
        # Remove files if they exist
        self.remove()

    def remove(self):
        # Remove files if they exist
        for file in REMOVE_FILES:
            if os.path.exists(file):
                os.remove(file)

    def makeTask(self, parameter_dct:Optional[dict]=None)->Tuple[Task, str]:
        model = Model(MODEL_ID, MODEL_SBML, is_overwrite=True, parameter_dct=parameter_dct)
        simulation = Simulation("simulation1", "uniform", 0, 10, 100)
        task = Task("task1", model.id, simulation.id)
        return task, assemble(model, simulation, task)

    def testRepeatedTask1(self):
        # task = task task1 run simulation1 on model1
        # repeated_task1 = repeat task1 for k1 in [1, 3, 5], reset=true
        if IGNORE_TEST:
            return
        task, phrasedml_str = self.makeTask()
        # Create a repeated task
        parameter_df = pd.DataFrame({"k1": [1, 3, 5]})
        repeated_task = RepeatedTask("repeat1", task.id, parameter_df=parameter_df, reset=True)
        phrasedml_str += "\n" + repeated_task.getPhraSEDML()
        result, explanation_str = evaluate(phrasedml_str)
        self.assertTrue(result, explanation_str)
    
    def testRepeatedTask2(self):
        # task = task task1 run simulation1 on model1
        # repeated_task1 = repeat task1 for k1 in [1, 3, 5], reset=true
        if IGNORE_TEST:
            return
        task, phrasedml_str = self.makeTask(parameter_dct=dict(k3=13))
        # Create a repeated task
        parameter_df = pd.DataFrame({"k1": [1, 3, 5], "k2": [0, 10, 3]})
        repeated_task = RepeatedTask("repeat1", task.id, parameter_df=parameter_df, reset=True)
        phrasedml_str += "\n" + repeated_task.getPhraSEDML()
        result, explanation_str = evaluate(phrasedml_str)
        self.assertTrue(result, explanation_str)


if __name__ == '__main__':
    unittest.main()