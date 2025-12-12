'''Class that handles model definitions and their parameters.'''

import SimpleSEDML.constants as cn # type: ignore
import SimpleSEDML.utils as utils # type: ignore

import codecs
import urllib3
import os
import shutil
import tellurium as te  # type: ignore
from typing import Optional, List
import warnings

INVALID_MODEL_ID = "invalid_model_id"

"""
Issues
1. To eliminate the warning for urllib3, need to create a virtual environment with a higher version of python.
"""

class Model:
    def __init__(self, id:str,
                    model_ref:Optional[str]=None,
                    ref_type:Optional[str]=None, 
                    source:Optional[str]=None, 
                    is_overwrite:bool=False,
                    existing_model_ids:Optional[List[str]]=None,
                    project_dir:Optional[str]=None,
                    parameter_dct:Optional[dict]=None):
        """Provide information about the model and a model identifier.

        Args:
            id (str): identifier for the model
            model_ref (str): reference to the file; reference type is specified separately
            ref_type (str):
                - "sbml_str": string representation of the SBML model
                - "ant_str": string representation of the SBML model
                - "sbml_file": file path to the SBML model
                - "ant_file": file path to the Antimony model
                - "sbml_url": URL to the SBML model
                - "model_id": ID of a previously defined model
            is_overwrite (bool): if True, overwrite the model if it already exists
            source (str): source for the SBML model. If None, the source is a file with the same name as the model ID
                in the current directory.
            existing_model_ids (List[str]): list of existing model IDs. This is used to resolve the model reference
                and to check if the model ID is unique.
            project_dir (str): directory to save the model file. If None, the current directory is used.
            parameter_dct (dict): dictionary of parameters whose values are changed
        """
        if existing_model_ids is None:
            existing_model_ids = []
        if project_dir is not None:
            # Check if the target directory exists
            if not os.path.exists(project_dir):
                os.makedirs(project_dir)
        else:
            project_dir = utils.makeDefaultProjectDir(project_dir)
        self.project_dir = project_dir
        # Model reference to use as arguments until it is resolved
        if model_ref is None:
            model_ref = id
            id = INVALID_MODEL_ID
        #
        if ref_type is None:
            ref_type = self._findReferenceType(model_ref, existing_model_ids)
        # Now we can resolve the model reference and id
        if id == INVALID_MODEL_ID:
            if "file" in ref_type:
                # id is a file path to an SBML model
                _, filename = os.path.split(model_ref)
                splits = filename.split(".")
                id = splits[0]
            else:
                # Create a unique ID for the model
                id = "model" + str(len(existing_model_ids))
        # Have resolved: id, model_ref, ref_type
        self.id = id
        self.model_ref = model_ref
        self.ref_type = ref_type
        if parameter_dct is None:
            parameter_dct = {}
        self.parameter_dct = parameter_dct 
        self.is_overwrite = is_overwrite
        #
        self.sbml_str = self._getSBMLFromReference()
        self.source = self._makeModelSource(source)
        self._roadrunner = None

    @property
    def roadrunner(self):
        """Returns the RoadRunner object for the model"""
        if self._roadrunner is None:
            self._roadrunner = te.loadSBMLModel(self.sbml_str)
        self._roadrunner.resetAll()
        return self._roadrunner

    def _makeModelSource(self, source:Optional[str]=None)->str:
        """Saves the model to a file. The file name is the model_id.xml
        """
        if self.ref_type == cn.MODEL_ID:
            # model_ref is the ID of a previously defined model
            return self.model_ref + cn.XML_EXT
        if source is None:
            # Use the current directory
            source = os.path.join(self.project_dir, self.id + cn.XML_EXT)
        source = str(source)
        if (not self.is_overwrite and os.path.exists(source)):
            msg = "*** File {model_source_path} already exists and will be used as model source."
            msg += "\n  Use is_overwrite=True to overwrite."
            warnings.warn(msg)
        with open(source, "wb") as f:
            f.write(self.sbml_str.encode('utf-8'))
            f.flush()
        return source

    def _getSBMLFromReference(self)->str:
        """Extracts an SBML strong from the model reference

        Args:
            self.model_ref (str): reference to the file; reference type is specified separately
            self.ref_type (str): One of self.cn.MODEL_self.REF_TYPES

        Returns:
            SBML string
        """
        if self.ref_type in [cn.SBML_FILE, cn.ANT_FILE]:
            with open(self.model_ref, "r") as f:
                lines = f.read()
            if self.ref_type == cn.SBML_FILE:
                sbml_str = lines
            else:
                sbml_str = te.antimonyToSBML(lines)
        elif self.ref_type == cn.SBML_STR:
            sbml_str = self.model_ref
        elif self.ref_type == cn.ANT_STR:
            sbml_str = te.antimonyToSBML(self.model_ref)
        elif self.ref_type == cn.MODEL_ID:
            # self.model_ref is the ID of a previously defined model
            sbml_str = "" 
        else:
            # self.ref_type == cn.SBML_URL
            response = urllib3.request("GET", self.model_ref)
            if response.status == 200:
                sbml_str = codecs.decode(response.data, 'utf-8')
            else:
                raise ValueError(f"Failed to fetch SBML from URL: {self.model_ref}")
        return sbml_str

    def getPhraSEDML(self, is_basename_source:bool=False)->str:
        params = ", ".join(f"{param} = {val}" for param, val in self.parameter_dct.items())
        if len(params) > 0:
            params = f" with {params}"
        if self.ref_type == cn.MODEL_ID:
            source = self.model_ref
        else:
            if is_basename_source:
                source = os.path.basename(self.source)
            else:
                source = self.source
            source = f'"{source}"'
        return f'{self.id} = model {source} {params}'
    
    def __str__(self)->str:
        """
        Construct the PhraSED-ML string. This requires:
        """
        return self.getPhraSEDML()

    @staticmethod 
    def _findReferenceType(model_ref:str, model_ids:List[str], ref_type:Optional[str]=None)->str:
        """Infers the reference type from the model reference.

        Args:
            model_ref (str): reference to the file; reference type is specified separately
            model_ids (List[str]): List of known model IDs
            refer_type (str): One of self.cn.MODEL_REF_TYPES

        Returns:
            str: reference type
        """
        # Use the ref_type if it is specified
        if ref_type is not None:
            return ref_type
        # Check if this is a model ID
        if model_ref in model_ids:
            try:
                is_file = os.path.exists(model_ref)
            except:
                is_file = False
            if is_file:
                warnings.warn(f"Model ID {model_ref} is also a file path. Using model ID.")
            return cn.MODEL_ID
        # Check for Antimony string
        try:
            _ = te.loada(model_ref)
            if " ->" in model_ref:
                return cn.ANT_STR
        except:
            pass
        # Check for SBML string
        try:
            _ = te.loadSBMLModel(model_ref)
            if "<sbml" in model_ref:
                return cn.SBML_STR
        except:
            pass
        # Check if this is a URL
        if ("http://" in model_ref) or ("https://" in model_ref):
            return cn.SBML_URL
        # Check if this is a file path
        try:
            is_file = os.path.exists(model_ref)
        except:
            is_file = False
        if is_file:
            try:
                with open(model_ref, "r") as f:
                    lines = f.read()
                if lines.startswith("<"):
                    return cn.SBML_FILE
                else:
                    return cn.ANT_FILE
            except:
                pass
        # Report error
        msg = f"Unidentifiable model reference: {model_ref}. "
        msg += f"\nFix the reference and/or specify the reference type.\nMust be one of {cn.MODEL_REF_TYPES}."
        raise ValueError(msg)
    
    def cleanUp(self):
        """Clean up the model files"""
        if self.project_dir is not None and os.path.exists(self.project_dir):
            shutil.rmtree(self.project_dir)