import SimpleSEDML.constants as cn  # type: ignore
from SimpleSEDML.model_information import ModelInformation # type: ignore
from SimpleSEDML.model import Model # type: ignore

import os
import phrasedml # type: ignore
import unittest
import tellurium as te # type: ignore
from typing import Optional


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
WOLF_URL = "https://www.ebi.ac.uk/biomodels/services/download/get-files/MODEL3352181362/3/BIOMD0000000206_url.xml"

#############################
# Tests
#############################
class TestModel(unittest.TestCase):

    def setUp(self):
        if IGNORE_TEST:
            return
        self.model = Model(MODEL_ID, MODEL_ANT, ref_type=cn.ANT_STR, is_overwrite=True)

    def tearDown(self):
        if hasattr(self, 'model'):
            self.model.cleanUp()

    def testGetInformation(self):
        if IGNORE_TEST:
            return
        model_information = ModelInformation.get(self.model.source)
        self.assertEqual(model_information.model_name, MODEL_ID)
        self.assertTrue(model_information.parameter_dct, ["k1", "k2", "k3"])
        self.assertEqual(list(model_information.floating_species_dct), ["S1", "S2", "S3", "S4"])
        self.assertEqual(model_information.boundary_species_dct, {})
        self.assertEqual(model_information.num_reaction, 3)

    def testRepr(self):
        if IGNORE_TEST:
            return
        model_information = ModelInformation.get(self.model.source)
        self.assertTrue(MODEL_ID in str(model_information))
        self.assertTrue("S1" in str(model_information))


if __name__ == '__main__':
    unittest.main()