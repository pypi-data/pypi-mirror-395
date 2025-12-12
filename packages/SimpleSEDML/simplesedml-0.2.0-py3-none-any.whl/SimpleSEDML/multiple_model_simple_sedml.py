'''SimpleSEDML for multiple model tasks, like multiple model simulations.'''

"""
This module provides a superclass for comparing multiple models with common variables.

The generation of PhraSED-ML strings is done through the `getPhrasedml` method,
which constructs the string by adding the necessary directives based on the provided
model references, simulation parameters, and display variables. This "late generation" approach
allows for flexibility in model definitions since the definitions in the constructor
can reference other model definitions that occur later on.

Using this class requires implementing two subclasses:
1. _makeSimulationObject` method to create the simulation object
2. _makePlotObjects method to create plot objects for the variables.
3. _makeTaskObjects method to create a task objects for each model.
4. set self.is_time to indicate whether the simulation is time-based.
"""

import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.simple_sedml import SimpleSEDML  # type:ignore
from SimpleSEDML.simulation import Simulation  # type:ignore

import pandas as pd # type:ignore
from typing import Optional, List
import warnings

REPORT_ID = "report"
PLOT_ID = "plot"

class MultipleModelSimpleSEDML(SimpleSEDML):
    """Provides comparisons between multiple simulations."""

    def __init__(self,
                    model_refs:Optional[List[str]]=None,
                    project_id:Optional[str]=None,
                    project_dir:Optional[str]=None,
                    display_variables:Optional[List[str]]=None,
                    is_plot:bool=True,
                    model_parameter_dct:Optional[dict]=None,
                    scan_parameters:Optional[List[str]]=None,
                    title:Optional[str]=None,
                    is_time:bool=True,
                    ):
        """Simulates a collection of models with common variables for the same time course.
        All models have the compared_variables. The outputs are:
            - plots comparing the models for each exposed variable
            - a report with the values of each variable for each model

        Args: Caller must have added a simulation object.
            model refs: List of model references. Defaults to None.
            project_dir (Optional[str], optional): Directory to save the files. Defaults to None.
            project_id (Optional[str], optional): Project ID. Defaults to None.
            variables (Optional[List[str]], optional): List of variables to be compared. Defaults to None.
                if not provided, all variables in the model are used.
            is_plot (bool, optional): Whether to plot the results. Defaults to True.
            model_parameter_dct (Optional[dict], optional): Dictionary of model parameters whose values are changed
            title (str, optional): Title of the plot. Defaults to "Multiple Model Comparison".
            is_time (bool, optional): Whether the simulation is time-based. Defaults to True.
        """
        #
        super().__init__(project_dir=project_dir, 
                project_id=project_id, display_variables=display_variables,
                scan_parameters=scan_parameters, is_time=is_time)
        #
        if model_refs is None:
            model_refs = []
        self.model_refs = model_refs
        self.task_model_dct:dict = {}  # Model associated with each task or repeated task
        self.model_parameter_dct = model_parameter_dct
        self.title = title
        self.is_plot = is_plot

    """ @property
    def model_ref_dct(self)->dict:
        # Relates the model reference to the model ID. Needed for late creation of models.
        result_dct = {}
        for model_id, model in self.model_dct.items():
            result_dct[model.model_ref] = model_id
        return result_dct """

    @property
    def model_ids(self)->List[str]:
        return [m.id for m in self.model_dct.values()] 
    
    @property
    def simulation_id(self)->str:
        """Get the simulation ID for the simulation."""
        simulation = list(self.simulation_dct.values())[0]
        if simulation is None:
            raise RuntimeError("No simulation has been created. Please create a simulation first.")
        return simulation.id
    
    @staticmethod
    def _makeTaskID(model_id:str, prefix:str)->str:
        """Make a task ID from the model ID and simulation ID.

        Args:
            model_id (str): model ID

        Returns:
            str: task ID
        """
        return f"{prefix}{model_id}"
    
    def makeModelObjects(self):
        for model_ref in self.model_refs:
            _ = self.addModel(model_ref, is_overwrite=True,
                    parameter_dct=self.model_parameter_dct)

    def _makeReportID(self)->str:
        """Make a report ID for the variable."""
        return REPORT_ID

    def _makePlotID(self, variable:str)->str:
        """Make a report ID for the variable."""
        return f"{PLOT_ID}_{variable}"

    def makeReportObject(self):
        """Make the report objects for the compared variables.
        """
        # Calculate the task ids to consider
        #
        report_id = self._makeReportID()
        if report_id in self.report_dct:
            return
        report_variables = self.variable_collection.getScopedVariables(
                #self.task_ids, is_time=False, is_scan_parameters=True,
                [], is_time=False, is_scan_parameters=True,
                is_display_variables=True).lst
        if cn.TIME in self.variable_collection.display_variables:
            report_variables.insert(0, self.variable_collection.getScopedTime())
        self.addReport(*report_variables, id=report_id)
    
    def makeSimulationObject(self):
        """Make the simulation object for the compared variables."""
        raise NotImplementedError("This method should be implemented in the subclass.")
    
    def makeTaskObjects(self):
        """Make the task objects for the compared variables."""
        raise NotImplementedError("This method should be implemented in the subclass.")

    def getPhraSEDML(self, is_basename_source:bool=False)->str:
        """Construct the PhraSED-ML string. This requires:
            1. Create simulation and task directives
            2. Changing the model and report
        
        Returns:
            str: Phrased-ML string
        """
        # Make the objects if they have not been created yet
        self.makeModelObjects()
        self.makeSimulationObject()
        self.makeTaskObjects()
        self.makeReportObject()
        self.makePlotObjects()
        #
        return super().getPhraSEDML(is_basename_source=is_basename_source)
    
    def getSEDML(self, is_basename_source:bool=False, display_name_dct:Optional[dict]=None)->str:
        """Uses models as legend names on plots.

        Args:
            is_basename_source: if True, use the basename of the model source files
            display_name_dct: dictionary of display names for the variables

        Returns:
            str: SED-ML string
        Raises:
            ValueError: if the conversion failsk
        """
        # Handle defaults
        if display_name_dct is None:
            display_name_dct = {}
        # Do initial replacements
        sedml_str = super().getSEDML(is_basename_source=is_basename_source)
        # Make legend lines be the model IDs
        for task_id, model_id in self.task_model_dct.items():
            # Handle x-axis
            if self.is_time:
                search_str = f"name=\"{task_id}{cn.SCOPE_INDICATOR}{cn.TIME}\""
                replace_str = f"name=\"{cn.TIME}\""
            else:
                x_var = list(self.variable_collection.getScopedVariables([],
                        is_time=False,
                        is_scan_parameters=True,
                        is_display_variables=False).dct.keys())[0]
                search_str = f"name=\"{task_id}{cn.SCOPE_INDICATOR}{x_var}\""
                replace_str = f"name=\"{x_var}\""
            sedml_str = sedml_str.replace(search_str, replace_str)
            # Handle other variables
            for variable in display_name_dct.keys():
                # Handle legend lines
                search_str = f"name=\"{task_id}{cn.SCOPE_INDICATOR}{variable}\""
                replace_str = f"name=\"{model_id}\""
                sedml_str = sedml_str.replace(search_str, replace_str)
        return sedml_str
    
    def makePlotObjects(self):
        """Make the report objects for the compared variables.
        There is one plot for each variable that plots comparisons of the models.
        This method is called by getPhrasedml to generate the plots for the variables.
        """
        scoped_variable_dct = self.variable_collection.getScopedVariables([],
            is_time=False, 
            is_scan_parameters=False,
            is_display_variables=True).dct
        scoped_scan_parameters = self.variable_collection.getScopedVariables([],
            is_time=False, 
            is_scan_parameters=True,
            is_display_variables=False).lst
        if len(scoped_scan_parameters) > 1:
            warnings.warn("Can only plot one parameter on the x-axis. ")
        if self.is_time:
            x_var = self.variable_collection.getScopedTime()
        else:
            x_var = scoped_scan_parameters[0]
        for variable, scoped_names in scoped_variable_dct.items():
            if variable == x_var:
                continue
            plot_id = self._makePlotID(variable)
            display_name = self.variable_collection.getDisplayNameDct()[variable]
            if self.title is None:
                title = display_name
            else:
                title = f"{self.title}: {display_name}"
            if not plot_id in self.plot_dct:
                self.addPlot(x_var=x_var, y_var=scoped_names,
                    title=title, id=plot_id, is_plot=self.is_plot)
    
    def __str__(self)->str:
        """Return PhraSED-ML string.
        
        Returns:
            str:
        """
        return self.getPhraSEDML()