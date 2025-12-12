import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.executor import Executor # type: ignore
from SimpleSEDML.simple_sedml import SimpleSEDML # type: ignore
from SimpleSEDML.multiple_model_parameter_scan import MultipleModelParameterScan # type: ignore
import SimpleSEDML.utils as utils # type: ignore

import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore
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

    S1 is "species1"
end
""" % MODEL_ID
MODEL_SBML = te.antimonyToSBML(MODEL_ANT)


#############################
# Tests
#############################
class TestExecutor(unittest.TestCase):

    def setUp(self):
        self.simple = SimpleSEDML()
        self.simple.addModel(MODEL_ID, MODEL_SBML, is_overwrite=True)
        self.simple.addSimulation("simulation1", "uniform", 0, 10, 100)
        self.simple.addTask("task1", MODEL_ID, "simulation1")
        self.executor = Executor(self.simple)

    def testConstructor(self):
        """Test the constructor of Executor."""
        if IGNORE_TEST:
            return
        self.assertIsInstance(self.executor, Executor)
        self.assertEqual(self.executor.simple, self.simple)

    def testExecuteTask(self):
        if IGNORE_TEST:
            return
        """Test the executeTask method."""
        result_df = self.executor.executeTask("task1")
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIn("time", result_df.columns)
        self.assertIn("S1", result_df.columns)
        self.assertGreater(len(result_df), 0, "Result DataFrame should not be empty")
        # Verify works with default
        _ = self.executor.executeTask()

    def testExecuteTaskSteadyState(self):
        if IGNORE_TEST:
            return
        # Verify works with default
        _ = self.executor.executeTask()
        """Test the executeTask method."""
        _ = self.simple.addSimulation("simulation2", "steadystate")
        self.simple.addTask("task2", MODEL_ID, "simulation2")
        result_df = self.executor.executeTask("task2")
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIn("time", result_df.columns)
        self.assertIn("S1", result_df.columns)
        self.assertGreater(len(result_df), 0, "Result DataFrame should not be empty")

    def testExecuteRepeatedTask(self):
        if IGNORE_TEST:
            return
        """Test the executeTask method."""
        self.simple.addRepeatedTask("repeat1", "task1",
            parameter_df=pd.DataFrame({"k1": [1, 3, 5], "k2": [0.10, 0.3, 0.2]}), reset=True)
        result_df = self.executor.executeRepeatedTask("repeat1")
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertIn("time", result_df.columns)
        self.assertIn("S1", result_df.columns)
        self.assertGreater(len(result_df), 0, "Result DataFrame should not be empty")
        # Verify works with default
        _ = self.executor.executeRepeatedTask()

    def testExecutePlot(self):
        """Test the executePlot method."""
        if IGNORE_TEST:
            return
        self.simple.addPlot("time", "S1", id="plot1", title="Plot 1")
        for kind in ['line', 'scatter', 'bar']:
            result = self.executor.executePlot2d("plot1", kind=kind, is_plot=IS_PLOT)
            if IS_PLOT:
                result.ax.set_title(kind)
                self.assertTrue("axes" in str(type(result.ax)).lower(), "Axes should be returned")
            utils.showPlot(result.ax)
            self.assertGreater(len(result.plot_ids), 0, "Plot IDs should not be empty")
        # Verify works with default
        _ = self.executor.executePlot2d(is_plot=IS_PLOT)

    def testMultipleModelScan(self):
        """Test the executeMultipleModelScan method."""
        if IGNORE_TEST:
            return
        scan_parameter_df = pd.DataFrame(dict(k1=[50, 550, 5000]))
        mmps = MultipleModelParameterScan(scan_parameter_df,
                                                model_refs=[cn.WOLF_URL],
                                                simulation_type="onestep",
                                                project_id="Wolf", 
                                                title="Wolf",
                                                time_interval=10, 
                                                display_variables=['at', 'na'])
        executor = Executor(mmps)
        result = executor.executePlot2d(kind="scatter", is_plot=IS_PLOT)
        if IS_PLOT:
            self.assertTrue("axes" in str(type(result.ax)).lower(), "Axes should be returned")
        self.assertGreater(len(result.plot_ids), 0, "Plot IDs should not be empty")
        utils.showPlot(result.ax)
        executor.cleanUp()



if __name__ == '__main__':
    unittest.main()