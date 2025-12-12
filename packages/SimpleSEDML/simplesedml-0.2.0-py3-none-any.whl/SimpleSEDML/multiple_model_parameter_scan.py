'''Provides comparisons between multiple parameter scan simulations.'''

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

import pandas as pd # type: ignore
from typing import Optional, List, Union

SIM_ID = "mmps_sim1"


class MultipleModelParameterScan(MultipleModelSimpleSEDML):
    """Provides comparisons between time course multiple simulations."""

    def __init__(self,
                    scan_parameter_df:pd.DataFrame,
                    model_refs:Optional[List[str]]=None,
                    project_id:Optional[str]=None,
                    simulation_type:str=cn.ST_ONESTEP,
                    project_dir:Optional[str]=None,
                    time_interval:float=cn.D_TIME_INTERVAL,
                    algorithm:Optional[str]=None,
                    display_variables:Optional[List[str]]=None,
                    title:Optional[str]=None,
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
            model_refs (List[str]): List of model references.
            scan_parameter_df (pd.DataFrame): DataFrame of parameters to scan over multiple values.
                    Each column is a parameter name, and the values are the values to scan.
            simulation_type: type of the simulation
                    (e.g., "uniform", "uniform_stochastic", "steadystate", "onestep")
            time_interval (float, optional): time interval for the simulation. Defaults to cn.D_TIME_INTERVAL.
            algorithm (str, optional): Simulation algorithm. Defaults to cn.D_ALGORITHM.
            models (Optional[List[str]], optional): List of model references. Defaults to None.
            variables (Optional[List[str]], optional): List of variables to be compared. Defaults to None.
                if not provided, all variables in the model are used.
            title (str, optional): Title of the plot. Defaults to "Multiple Model Comparison".
            is_plot (bool, optional): Whether to plot the results. Defaults to True.
            model_parameter_dct (Optional[dict], optional): Dictionary of model parameters whose values are changed

        Example 1: Compare parameterizations of the same model
            mmps = MultipleModelTimeCourse([MODEL1, MODEL2], time_interval=20,
                compared_variables=["S1", "S2", "S3"],
                scan_parameters=["k1", "k2"])
            sedml_str = mmtc.getSEDMLString()
        """
        #
        self.scan_parameter_df = scan_parameter_df
        scan_parameters = list(scan_parameter_df.columns)
        self.time_interval = time_interval
        self.simulation_type = simulation_type
        self.algorithm = algorithm
        super().__init__(
                    model_refs=model_refs,
                    project_id=project_id,
                    project_dir=project_dir,
                    display_variables=display_variables,
                    is_plot=is_plot,
                    model_parameter_dct=model_parameter_dct,
                    scan_parameters=scan_parameters,
                    title=title,
                    is_time=False)  # Time is not a variable in the plots or reports
    
    def makeTaskObjects(self):
        """Make  task objects for the compared variables.
        For each model, creates a task and repeated task object.
        Adds the task IDs to the scopes of the variable collection.

        Returns:
            str: task ids
        """
        if len(self.model_ids) == 0:
            raise ValueError("No models have been added to the simulation.")
        #
        repeated_task_ids = []
        for model_id in self.model_ids:
            if model_id is None:
                continue
            task_id = self._makeTaskID(model_id, cn.TASK_PREFIX)
            if not task_id in self.task_dct:
                self.addTask(task_id, model_id,simulation_id=SIM_ID)
                self.task_model_dct[task_id] = model_id
                repeated_task_id = self._makeTaskID(model_id, cn.REPEATED_TASK_PREFIX)
                self.addRepeatedTask(repeated_task_id, task_id,
                        self.scan_parameter_df, reset=True)
                self.task_model_dct[repeated_task_id] = model_id
                repeated_task_ids.append(repeated_task_id)
        self.variable_collection.addScopeStrs(repeated_task_ids) 

    # Methods that override the parent class methods
    def makeSimulationObject(self):
        if not SIM_ID in self.simulation_dct:
            # Create a simulation object if it does not exist
            self.addSimulation(SIM_ID,
                    simulation_type=self.simulation_type,
                    time_interval=self.time_interval,
                    algorithm=self.algorithm)