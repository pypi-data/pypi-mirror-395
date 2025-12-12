'''Abstraction for a task, the combination of a model and a simulation.'''

from SimpleSEDML import constants as cn # type:ignore
from SimpleSEDML.model import Model # type:ignore
from SimpleSEDML.variable_collection import VariableCollection # type: ignore
from SimpleSEDML.single_model_time_course import SingleModelTimeCourse # type:ignore

import unittest


IGNORE_TEST = False
IS_PLOT = False
MODEL_ID = "model1"
DISPLAY_NAME1 = "species1"
DISPLAY_NAME2 = "species2"
MODEL_ANT = f"""
model {MODEL_ID} 
    S1 -> S2; k1*S1
    S2 -> S3; k2*S2
    S3 -> S4; k3*S3

    S1 is "{DISPLAY_NAME1}"
    S2 is "{DISPLAY_NAME2}"

    k1 = 0.1
    k2 = 0.2
    k3 = 0.3
    S1 = 10
    S2 = 0
    S3 = 0
    S4 = 0
end
"""
WOLF_URL = "https://www.ebi.ac.uk/biomodels/services/download/get-files/MODEL3352181362/3/BIOMD0000000206_url.xml"

#############################
# Tests
#############################
class TestVariableCollection(unittest.TestCase):

    def setUp(self):
        self.remove()
        self.model = Model(MODEL_ID, MODEL_ANT)
        self.variable_collection = VariableCollection(self.model)

    def tearDown(self):
        self.remove()
    
    def remove(self):
        """Remove the files created during the test"""
        if hasattr(self, 'model'):
            self.model.cleanUp()

    def testDisplayVariables(self):
        if IGNORE_TEST:
            return
        display_variables = self.variable_collection.display_variables
        self.assertIn(cn.TIME, display_variables)
        for var in ["S1", "S2", "S3", "S4"]:
            self.assertIn(var, display_variables)
        #
        variables = ["S1", "S2"]
        variable_collection = VariableCollection(self.model, display_variables=variables)
        for var in variables:
            self.assertIn(var, variable_collection.display_variables)

    def testAddParameters(self):
        if IGNORE_TEST:
            return
        self.assertEqual(len(self.variable_collection.scan_parameters), 0)
        self.variable_collection.addScanParameters(["k1", "k2"])
        self.assertEqual(len(self.variable_collection.scan_parameters), 2)

    def testGetScopedVariables(self):
        if IGNORE_TEST:
            return
        scope_str = "test_scope"
        DISPLAY_VARIABLES = ["S1", "S2"]
        PARAMETERS = ["k1", "k2"]
        variable_collection = VariableCollection(self.model, display_variables=DISPLAY_VARIABLES)
        variable_collection.addScanParameters(PARAMETERS)
        # Case 1
        scope_dct = variable_collection.getScopedVariables(scope_str,
                is_time=True, is_scan_parameters=True, is_display_variables=True).dct
        self.assertEqual(scope_dct[cn.TIME], [cn.TIME])
        self.assertEqual(len(scope_dct), 5)
        count = len([v for v in scope_dct.values() if scope_str in v[0]])
        self.assertEqual(count, 4)
        # Case 1a
        scope_dct = variable_collection.getScopedVariables([scope_str],
                is_time=True, is_scan_parameters=True, is_display_variables=True).dct
        self.assertEqual(scope_dct[cn.TIME], [cn.TIME])
        self.assertEqual(len(scope_dct), 5)
        count = len([v for v in scope_dct.values() if scope_str in v[0]])
        self.assertEqual(count, 4)
        # Case 1b
        scope_dct = variable_collection.getScopedVariables([],
                is_time=True, is_scan_parameters=True, is_display_variables=True).dct
        self.assertEqual(scope_dct[cn.TIME], [cn.TIME])
        self.assertEqual(len(scope_dct), 5)
        # Case 1c
        scope_dct = variable_collection.getScopedVariables(['scope1', 'scope2'],
                is_time=True, is_scan_parameters=True, is_display_variables=True).dct
        self.assertEqual(scope_dct[cn.TIME], [cn.TIME])
        self.assertEqual(len(scope_dct), 5)
        count = len([v for v in scope_dct.values() if len(v) == 2])
        self.assertEqual(count, 4)
        # Case 2
        scope_dct = variable_collection.getScopedVariables(scope_str,
                is_time=False, is_scan_parameters=True, is_display_variables=True).dct
        self.assertNotIn(cn.TIME, scope_dct.values())
        self.assertEqual(len(scope_dct), 4)
        # Case 3
        scope_dct = variable_collection.getScopedVariables(scope_str,
                is_time=False, is_scan_parameters=False, is_display_variables=True).dct
        self.assertNotIn(cn.TIME, scope_dct.values())
        self.assertEqual(len(scope_dct), 2)

    def testGetDisplayNameDct(self):
        if IGNORE_TEST:
            return
        DISPLAY_VARIABLES = ["S1", "S2"]
        variable_collection = VariableCollection(self.model, display_variables=DISPLAY_VARIABLES)
        display_name_dct = variable_collection.getDisplayNameDct()
        self.assertEqual(len(display_name_dct), 2)
        self.assertEqual(set(display_name_dct.values()), set([DISPLAY_NAME1, DISPLAY_NAME2]))
        #
        display_name2_dct = variable_collection.getDisplayNameDct()
        self.assertEqual(display_name_dct, display_name2_dct)
    
    def testDisplayVariables2(self):
        if IGNORE_TEST:
            return
        smtc = SingleModelTimeCourse(WOLF_URL, num_point=200, is_plot=IS_PLOT)
        display_variables = smtc.variable_collection.display_variables
        self.assertIn(cn.TIME, display_variables)
        display_name_dct = smtc.variable_collection.getDisplayNameDct()
        self.assertTrue(display_name_dct['s1']=='Glucose')
        smtc.execute()


if __name__ == '__main__':
    unittest.main()