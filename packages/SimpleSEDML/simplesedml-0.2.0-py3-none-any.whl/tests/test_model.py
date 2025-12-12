import SimpleSEDML.constants as cn  # type: ignore
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
MODEL_SBML = te.antimonyToSBML(MODEL_ANT)
SBML_FILE_PATH = os.path.join(cn.SRC_DIR, MODEL_ID + ".xml")
ANT_FILE_PATH = os.path.join(cn.SRC_DIR, MODEL_ID + ".ant")
WOLF_ID = "Wolf2000_Glycolytic_Oscillations"
WOLF_FILE = "Wolf2000_Glycolytic_Oscillations" + ".xml"
REMOVE_FILES = [SBML_FILE_PATH, WOLF_ID, ANT_FILE_PATH]
WOLF_URL = "https://www.ebi.ac.uk/biomodels/services/download/get-files/MODEL3352181362/3/BIOMD0000000206_url.xml"

#############################
# Tests
#############################
class TestModel(unittest.TestCase):

    def setUp(self):
        self.remove_files = list(REMOVE_FILES)
        self.remove()
        if IGNORE_TEST:
            return
        self.model = Model(MODEL_ID, MODEL_ANT, ref_type=cn.ANT_STR, is_overwrite=True)
        self.remove_files.append(self.model.source)

    def tearDown(self):
        self.remove()
    
    def remove(self):
        """Remove the files created during the test"""
        for file in self.remove_files:
            if os.path.exists(file):
                os.remove(file)

    def testUsageSBMLString(self):
        # model = model model1 sbml_str
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_SBML, is_overwrite=True)
        self.remove_files.append(model.source)
        phrasedml_str = model.getPhraSEDML()
        self.evaluate(phrasedml_str)
        self.checkFile(model)
    
    def testDesigateTargetDirectoryPath(self):
        # model = model model1 sbml_str
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_SBML, project_dir=cn.TEST_DIR, is_overwrite=True)
        self.remove_files.append(model.source)
        phrasedml_str = model.getPhraSEDML()
        self.evaluate(phrasedml_str)
        self.checkFile(model)
    
    def testStringParameters(self):
        # model = model model1 sbml_str
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_SBML,
                parameter_dct=dict(k1=10, k2=20), is_overwrite=True)
        self.remove_files.append(model.source)
        phrasedml_str = model.getPhraSEDML()
        self.evaluate(phrasedml_str)
        self.checkFile(model)

    def testUsageAntimonyString(self):
        # model = model model1 sbml_str
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_ANT, ref_type=cn.ANT_STR, is_overwrite=True)
        self.remove_files.append(model.source)
        phrasedml_str = model.getPhraSEDML()
        self.evaluate(phrasedml_str)
        self.checkFile(model)

    def testUsageStringNoOverwrite(self):
        # model = model model1 sbml_str
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_SBML, is_overwrite=True)
        self.remove_files.append(model.source)
        with self.assertWarns(UserWarning):
            _ = Model(MODEL_ID, MODEL_SBML, 
                    project_dir=model.project_dir, is_overwrite=False)
    
    def testUsageFile(self):
        # model = model model1 file-path
        if IGNORE_TEST:
            return
        with open(SBML_FILE_PATH, "w") as f:
            f.write(MODEL_SBML)
        model = Model(MODEL_ID, SBML_FILE_PATH, ref_type=cn.SBML_FILE, is_overwrite=True)
        self.remove_files.append(model.source)
        phrasedml_str = model.getPhraSEDML()
        self.evaluate(phrasedml_str)
        self.checkFile(model)

    def checkFile(self, model:Model):
        """Check if the file exists and is not empty"""
        filename = model.id + cn.XML_EXT
        self.assertTrue(filename in os.listdir(model.project_dir),
                f"File {filename} not created.")

    def testUsageURL(self):
        # model = model model1 URL
        if IGNORE_TEST:
            return
        model_id = "Wolf2000_Glycolytic_Oscillations"
        model = Model(model_id, WOLF_URL, ref_type=cn.SBML_URL, is_overwrite=True)
        self.remove_files.append(model.source)
        phrasedml_str = model.getPhraSEDML()
        self.evaluate(phrasedml_str)
        self.checkFile(model)
    
    def testUsageModelid(self):
        # model = model model1 sbml_str
        if IGNORE_TEST:
            return
        model = Model(MODEL_ID, MODEL_ANT, ref_type=cn.ANT_STR, is_overwrite=True)
        self.remove_files.append(model.source)
        phrasedml_str = model.getPhraSEDML()
        model = Model("model2", MODEL_ID, ref_type=cn.MODEL_ID, is_overwrite=True)
        self.remove_files.append(model.source)
        phrasedml_str += "\n" + model.getPhraSEDML()
        self.evaluate(phrasedml_str)

    def testFindReferenceType(self):
        if IGNORE_TEST:
            return
        model_ids = ["model1", "model2"]
        def test(model_ref:str, expected_ref_type, ref_type:Optional[str]=None):
            ref_type = Model._findReferenceType(model_ref, model_ids=model_ids, ref_type=ref_type)
            self.assertEqual(ref_type, expected_ref_type, f"Expected {expected_ref_type}, got {ref_type}")
        #
        model = Model(WOLF_ID, WOLF_URL, ref_type=cn.SBML_URL, is_overwrite=True)  # Create file
        test(model.source, cn.SBML_FILE)
        with open(ANT_FILE_PATH, "w") as f:
            f.write(MODEL_ANT)
        test(ANT_FILE_PATH, cn.ANT_FILE)
        test(MODEL_ID, cn.ANT_STR, ref_type=cn.ANT_STR)
        test(MODEL_ANT, cn.ANT_STR)
        test(MODEL_SBML, cn.SBML_STR)
        test(WOLF_URL, cn.SBML_URL)

    def evaluate(self, phrasedml_str:str):
        """Evaluate the sedml_str and sbml_str

        Args:
            phrasedml_str (str): phraSED-ML string
        """
        sedml_str = phrasedml.convertString(phrasedml_str)
        try:
            te.executeSEDML(sedml_str)
        except Exception as e:
            self.assertTrue(False, f"SED-ML execution failed: {e}")



if __name__ == '__main__':
    unittest.main()