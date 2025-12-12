'''Class that acquires information about the model.'''

import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.model import Model # type: ignore

import tellurium as te  # type: ignore
from typing import Optional, List
import warnings

class ModelInformation(object):
    """Class that holds information about the model.

    Attributes:
        model_name (str): name of the model
        parameters (list): list of global parameters
        floating_species (list): list of floating species
        boundary_species (list): list of boundary species
        num_reaction (int): number of reactions
        num_species (int): number of species
        model_id (str): ID of the model
        roadrunner (object): RoadRunner object for the model
    """
    def __init__(self, roadrunner, model_id:Optional[str]=None):
        ##
        def makeDict(names)->dict:
            my_dict = {}
            for name in names:
                my_dict[name] = self.roadrunner[name]
            return my_dict
        ##
        self.model_id = model_id
        self.roadrunner = roadrunner
        # Extract the model name
        MODEL_NAME = "modelName"
        self.roadrunner = roadrunner
        # Get the model name
        info_str = self.roadrunner.getInfo()
        pos = info_str.find(MODEL_NAME)
        info_str = info_str[pos:]
        pos = info_str.find(":") + 2
        info_str = info_str[pos:]
        end_pos = info_str.find("\n")
        self.model_name = info_str[:end_pos]
        # Extract dictionary information
        self.is_time = cn.TIME in self.roadrunner.keys()
        self.boundary_species_dct = makeDict(self.roadrunner.getBoundarySpeciesConcentrationIds())
        self.floating_species_dct = makeDict(self.roadrunner.getFloatingSpeciesIds())
        self.parameter_dct = makeDict(self.roadrunner.getGlobalParameterIds())
        self.num_reaction = self.roadrunner.getNumReactions()
        self.num_species = self.roadrunner.getNumFloatingSpecies() + self.roadrunner.getNumBoundarySpecies()

    @classmethod
    def get(cls, model_ref:str,
            ref_type:Optional[str]=None)->'ModelInformation':
        """Get the model global parameters and floating species.

        Args:
            model_ref: reference to the model (cannot be a model ID)
            ref_type: type of the reference (e.g. "sbml_str", "ant_str", "sbml_file", "ant_file", "sbml_url")

        Returns:
            model.ModelInformation: named tuple with the following fields:
                - model_name: name of the model
                - parameters: list of global parameters
                - floating_species: list of floating species
                - boundary_species: list of boundary species
                - num_reaction: number of reactions
                - num_species: number of species
        """
        model = Model("model_information", model_ref=model_ref, ref_type=ref_type,
                is_overwrite=True)
        return cls.getFromModel(model)
    
    @classmethod
    def getFromModel(cls, model:Model)->'ModelInformation':
        """Get the model global parameters and floating species.

        Args:
            model: Model object from which to extract information.

        Returns:
            model.ModelInformation: named tuple with the following fields:
                - model_name: name of the model
                - parameters: list of global parameters
                - floating_species: list of floating species
                - boundary_species: list of boundary species
                - num_reaction: number of reactions
                - num_species: number of species
        """
        return cls(model.roadrunner, model_id=model.id)

    def __repr__(self):
        """Returns a string representation of the model information"""
        result_str = f"Model: {self.model_name}"
        result_str += f"\nParameters: {self.parameter_dct}"
        result_str += f"\nFloating Species: {self.floating_species_dct}"
        result_str += f"\nBoundary Species: {self.boundary_species_dct}"
        result_str += f"\nNumber of Reactions: {self.num_reaction}"
        result_str += f"\nNumber of Species: {self.num_species}"
        return result_str