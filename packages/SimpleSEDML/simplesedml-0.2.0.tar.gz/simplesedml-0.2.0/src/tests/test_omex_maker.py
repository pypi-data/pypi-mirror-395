import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.multiple_model_time_course import MultipleModelTimeCourse # type:ignore
from SimpleSEDML.omex_maker import OMEXMaker, ValidationResult # type:ignore

import pandas as pd; # type: ignore
import os
import shutil  # type: ignore
import tellurium as te # type: ignore
import unittest
import zipfile

IGNORE_TEST = False
IS_PLOT = False
MODEL0_ID = "model0"
MODEL1_ID = "model1"
MODEL0_ANT = """
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
""" % MODEL0_ID
MODEL1_ANT = """
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
""" % MODEL1_ID
MODEL0_SBML = te.antimonyToSBML(MODEL0_ANT)
MODEL1_SBML = te.antimonyToSBML(MODEL1_ANT)
OMEX_PATH = os.path.join(cn.TEST_DIR, "project.omex")
OMEX_PROJECT_DIR = os.path.join(cn.TEST_DIR, "project")
REMOVE_DIRS = [OMEX_PROJECT_DIR]
DISPLAY_VARIABLES = ["S1", "S2"]
NUM_POINT = 100
MODEL_REFS = [MODEL0_SBML, MODEL1_SBML]
SEDML_PATH = os.path.join(OMEX_PROJECT_DIR, "project.sedml")
REMOVE_FILES = [SEDML_PATH, OMEX_PATH]


#############################


def assemble(*args):
        return "\n".join([str(arg) for arg in args])


#############################
# Tests
#############################
class TestMakeOmex(unittest.TestCase):

    def setUp(self):
        self.remove_files = list(REMOVE_FILES)
        self.mmtc = MultipleModelTimeCourse(MODEL_REFS, start=0,
                end=10, num_point=NUM_POINT,
                model_parameter_dct=dict(k1=1.5),
                display_variables=DISPLAY_VARIABLES,
                project_dir=OMEX_PROJECT_DIR,
                is_plot=False)
        sedml_str = self.mmtc.getSEDML(is_basename_source=True)
        self.remove_files.extend(self.mmtc._model_sources)
        for directory in REMOVE_DIRS:
            os.makedirs(directory, exist_ok=True)
        with open(SEDML_PATH, "w") as f:
            f.write(sedml_str)
        self.maker = OMEXMaker(project_id="project", project_path=OMEX_PROJECT_DIR,
                omex_path=OMEX_PATH)
    
    def tearDown(self):
        # Remove files if they exist
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
        if IGNORE_TEST:
            return
        """Test the constructor"""
        self.assertEqual(self.maker.project_id, "project")
        self.assertEqual(self.maker.project_path, OMEX_PROJECT_DIR)
        self.assertEqual(self.maker.omex_path, OMEX_PATH)
        self.assertEqual(self.maker.temp_dir, None)
        self.assertEqual(self.maker.archive, None)
        self.assertEqual(self.maker.project_id, "project")
        self.assertEqual(self.maker.project_path, OMEX_PROJECT_DIR)

    def testMake(self):
        if IGNORE_TEST:
            return
        self.maker.make()
        with zipfile.ZipFile(OMEX_PATH, 'r') as zipf:
            ffiles = zipf.namelist()
        self.assertIn("metadata.rdf", ffiles)
        self.assertIn("manifest.xml", ffiles)
        self.assertIn("project.sedml", ffiles)
        self.assertIn("model0.xml", ffiles)
        self.assertIn("model1.xml", ffiles)

    def testValidateOmex(self):
        if IGNORE_TEST:
            return
        self.maker.make()
        result = self.maker.validateOMEXFile()
        self.assertTrue(result)
        # Check the contents of the validation result
        self.assertIsInstance(result, ValidationResult)
        self.assertTrue(result)

    def testCleanUp(self):
        if IGNORE_TEST:
            return
        self.maker.make()
        self.maker.validateOMEXFile()
        temp_dir = self.maker.temp_dir
        self.assertTrue(os.path.exists(str(temp_dir)))
        self.maker.cleanUp()
        self.assertFalse(os.path.exists(str(temp_dir)))


if __name__ == '__main__':
    unittest.main()