'''Provides comparisons between multiple time course simulations.'''

"""
This module provides a class for comparing multiple models with common variables
for the same time course. The class allows for the simulation of a collection of models
with the same variables and generates plots and reports for the comparisons.
The class is designed to be used with the PhraSED-ML format and provides methods
for creating simulation objects, task objects, report objects, and plot objects.

The generation of PhraSED-ML strings is done through the `getPhrasedml` method,
which constructs the string by adding the necessary directives based on the provided
model references, simulation parameters, and display variables. This "late generation" approach
allows for flexibility in model definitions since the definitions in the constructor
can reference other model definitions that occur later on.
"""

import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.multiple_model_simple_sedml import MultipleModelSimpleSEDML # type:ignore

from typing import Optional, List, Union

SIM_ID = "mmtc_sim1"

class MultipleModelTimeCourse(MultipleModelSimpleSEDML):
    """Provides comparisons between time course multiple simulations."""

    def __init__(self,
                    model_refs:Optional[List[str]]=None,
                    project_id:Optional[str]=None,
                    simulation_type:str=cn.ST_UNIFORM,
                    project_dir:Optional[str]=None,
                    start:float=cn.D_START,
                    end:float=cn.D_END,
                    num_step:Optional[int]=None,
                    num_point:Optional[int]=None,
                    algorithm:Optional[str]=None,
                    display_variables:Optional[List[str]]=None,
                    is_plot:bool=True,
                    model_parameter_dct:Optional[dict]=None,
                    ):
        """Simulates a collection of models with common variables for the same time course.
        All models have the compared_variables. The outputs are:
            - plots comparing the models for each exposed variable
            - a report with the values of each variable for each model

        Args:
            project_dir (Optional[str], optional): Directory to save the files. Defaults to None.
            project_id (Optional[str], optional): Project ID. Defaults to None.
            simulation_type: type of the simulation
                    (e.g., "uniform", "uniform_stochastic", "steadystate", "onestep")
            start (float, optional): simulation start time. Defaults to cn.D_START.
            end (float, optional): simulation end time. Defaults to cn.D_END.
            num_step (int, optional): Defaults to cn.D_NUM_STEP.
            num_point (int, optional): Defaults to cn.D_NUM_POINT.
            algorithm (str, optional): Simulation algorithm. Defaults to cn.D_ALGORITHM.
            models (Optional[List[str]], optional): List of model references. Defaults to None.
            variables (Optional[List[str]], optional): List of variables to be compared. Defaults to None.
                if not provided, all variables in the model are used.
            is_plot (bool, optional): Whether to plot the results. Defaults to True.
            model_parameter_dct (Optional[dict], optional): Dictionary of model parameters whose values are changed

        Example 1: Compare two models with the same variables
            mmtc = MultipleModelTimeCourse(start=0, end=10, num_step=100,
                model_refs=[model1_file, model2_file])
            sedml_str = mmtc.getSEDMLString()
        """
        #
        self.start = start
        self.simulation_type = simulation_type
        self.end = end
        self.num_step = num_step
        self.num_point = num_point
        self.algorithm = algorithm
        #
        self.is_time = True # Time is a variable in the plots and reports
        super().__init__(
                    model_refs=model_refs,
                    project_id=project_id,
                    project_dir=project_dir,
                    display_variables=display_variables,
                    is_plot=is_plot,
                    model_parameter_dct=model_parameter_dct)
        

    # Methods that override the parent class methods
    def makeSimulationObject(self):
        if not SIM_ID in self.simulation_dct:
            # Create a simulation object if it does not exist
            self.addSimulation(SIM_ID,
                    simulation_type=self.simulation_type,
                    start=self.start, end=self.end, num_step=self.num_step,
                    num_point=self.num_point, algorithm=self.algorithm)
    
    def makeTaskObjects(self):
        """Make the task objects for the compared variables.
        Adds the task IDs to the scopes of the variable collection.

        Returns:
            str: task ids
        """
        if len(self.model_ids) == 0:
            raise ValueError("No models have been added to the simulation.")
        #
        task_ids = []
        for model_id in self.model_ids:
            if model_id is None:
                continue
            task_id = self._makeTaskID(model_id, cn.TASK_PREFIX)
            self.task_model_dct[task_id] = model_id
            if not task_id in self.task_dct:
                self.addTask(task_id, model_id, self.simulation_id)
                task_ids.append(task_id)
        self.variable_collection.addScopeStrs(task_ids)