import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.simulation import Simulation # type: ignore

import numpy as np
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
SIMULATION_ID = "sim1"

#############################
# Tests
#############################
class TestModel(unittest.TestCase):

    def setUp(self):
        self.remove()

    def tearDown(self):
        self.remove()
    
    def remove(self):
        """Remove the files created during the test"""
        for file in REMOVE_FILES:
            if os.path.exists(file):
                os.remove(file)

    def testUniform(self):
        if IGNORE_TEST:
            return
        simulation = Simulation(SIMULATION_ID,
                simulation_type=cn.ST_UNIFORM, start=0, end=10, num_point=100)
        self.evaluate(simulation.getPhraSEDML())

    def testOptions(self):
        if IGNORE_TEST:
            return
        options = [
                "absolute_tolerance",
                "initial_time_step",
                "maximum_adams_order",
                "maximum_bdf_order",
                "maximum_iterations",
                "maximum_num_steps",
                "maximum_time_step",
                "minimum_damping",
                "minimum_time_step",
                "relative_tolerance",
                "seed",
                "variable_step_size",
        ]
        kwargs = {}
        kwargs["algorithm"] = "CVODE"
        kwargs = {k: np.random.rand() for k in options if k != "algorithm"}
        simulation = Simulation(SIMULATION_ID,
                simulation_type=cn.ST_UNIFORM_STOCHASTIC,
                start=0, end=10, num_point=100)  # type: ignore
        self.evaluate(simulation.getPhraSEDML())

    def testSteadyState(self):
        if IGNORE_TEST:
            return
        simulation = Simulation(SIMULATION_ID,
                simulation_type=cn.ST_STEADYSTATE, start=0, end=10, num_point=100)
        self.evaluate(simulation.getPhraSEDML())
    
    def testUniformUniformStochastic(self):
        if IGNORE_TEST:
            return
        simulation = Simulation(SIMULATION_ID,
                simulation_type=cn.ST_UNIFORM_STOCHASTIC, start=0, end=10, num_point=100)
        self.evaluate(simulation.getPhraSEDML())

    def testUniformOnestep(self):
        if IGNORE_TEST:
            return
        simulation = Simulation(SIMULATION_ID,
                simulation_type=cn.ST_ONESTEP, start=5)
        self.evaluate(simulation.getPhraSEDML())

    def evaluate(self, phrasedml_str:str):
        """Evaluate the sedml_str and sbml_str

        Args:
            phrasedml_str (str): phraSED-ML string
        """
        # Convert the phrasedml string to sedml
        sedml_str = phrasedml.convertString(phrasedml_str)
        self.assertIsNotNone(sedml_str, phrasedml.getLastError())
        # See if the sedml can be executed
        try:
            te.executeSEDML(sedml_str)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")


if __name__ == '__main__':
    unittest.main()