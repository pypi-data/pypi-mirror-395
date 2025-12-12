import SimpleSEDML.constants as cn # type: ignore

import libsbml # type: ignore
import matplotlib.pyplot as plt # type: ignore
import tempfile
from typing import Union


def makeDefaultProjectDir(project_dir:Union[str, None])->str:
        """Creates a default project directory in a temporary location

        Args:
            project_dir: path to the project directory. If None, a temporary directory is created.

        Returns:
            str: path to the project directory
        """
        if project_dir is not None:
            new_project_dir = str(project_dir)
        else:
            new_project_dir = tempfile.mkdtemp()
        return new_project_dir

def makeDisplayNameDct(sbml_path:str)->dict:
    """Finds the display names in a model.
        If an element does not have a display name, its element id is used.

        Args:
            sbml_path - path to the SBML file
            element_ids - list of element ids

        Returns:
            dict:
                key: element_id
                value: display name
    """
    # Get the model
    document = libsbml.SBMLReader().readSBML(sbml_path)  # type:ignore
    model = document.getModel()
    # Collect IDs from all element types
    element_types = [
        ('Species', model.getListOfSpecies()),
        ('Parameters', model.getListOfParameters()),
        ('Reactions', model.getListOfReactions()),
        ('Compartments', model.getListOfCompartments()),
        ('Functions', model.getListOfFunctionDefinitions()),
        ('Events', model.getListOfEvents())
    ]
    # Find the element names if they exist
    result_dct = {}
    for type_name, element_list in element_types:
        for i in range(element_list.size()):
            element = element_list.get(i)
            element_id = element.getId()
            element_name = element.getName() if element.isSetName() else element_id
            result_dct[element_id] = element_name
    #
    return result_dct

def showPlot(ax):
    """Displays the plot if the is an Axis"""
    if ax is not None:
        plt.show()