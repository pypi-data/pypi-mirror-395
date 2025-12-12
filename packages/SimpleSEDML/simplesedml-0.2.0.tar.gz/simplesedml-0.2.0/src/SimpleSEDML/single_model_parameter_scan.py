'''Evaluates multiple values of parameters on a single model.'''

"""
Produces a plot with a curve for each display variable and the x-axis are
the values of the scan parameters.
Produces a report but it only contains information on the last parameter combination.
"""

# FIXME: steadystate doesn't work


from SimpleSEDML.simple_sedml import SimpleSEDML # type:ignore
from SimpleSEDML import constants as cn # type:ignore

import numpy as np # type:ignore
import pandas as pd # type:ignore
from typing import Optional, List
import warnings


class SingleModelParameterScan(SimpleSEDML):

    def __init__(self,
            model_ref:str,
            scan_parameter_dct:dict,
            project_id:Optional[str]=None,
            ref_type:Optional[str]=None,
            simulation_type:str=cn.ST_STEADYSTATE,
            project_dir:Optional[str]=None,
            display_variables:Optional[List[str]]=None,
            time_interval:float=0.5,
            title:Optional[str]=None,
            algorithm:Optional[str]=None,
            model_parameter_dct:Optional[dict]=None,
            is_plot:bool=True,):

        """Creates a time course simulation

        Args:
            model_ref: reference to the model
            scan_parameter_dct: dictionary of parameters to scan over multiple values
                    Each key is a parameter name, and the value is a list of values to scan.
            project_id: ID of the project, if None, uses the default project ID
            ref_type: type of the reference (e.g. "sbml_str", "ant_str", "sbml_file", "ant_file", "sbml_url")
            simulation_type: type of the simulation
                    (i.e., "steadystate", "onestep")
            project_dir: directory to save the files
            display_variables: variables to be plotted and included the report
            time_interval: time interval for the simulation, used for onestep simulations
            end: end time
            num_step: number of steps
            time_course_id: ID of the time course simulation
            algorithm: algorithm to use for the simulation
            title: title of the plot
            is_plot: if True, plot the results
            model_parameter_dct: dictionary of parameters whose values are changed

        Returns:
            SingleModelTimeCourse: a time course simulation object
        """
        # Ensure that scan parameters have the same number of values
        lengths = [len(v) for v in scan_parameter_dct.values()]
        if len(lengths) == 0:
            raise ValueError("Must provide at least one scan parameter.")
        if np.std(lengths) != 0:
            raise ValueError("All scan parameters must have the same number of values.")
        if not simulation_type in [cn.ST_STEADYSTATE, cn.ST_ONESTEP]:
            raise ValueError(f"Invalid simulation type: {simulation_type}. "
                    "Only 'steadystate' and 'onestep' are supported for parameter scans.")
        #
        super().__init__(project_dir=project_dir, project_id=project_id,
                display_variables=display_variables)
        # Construct the IDs
        self.model_id = f"{cn.MODEL_PREFIX}{self.project_id}"
        self.sim_id = f"{cn.SIMULATION_PREFIX}{self.project_id}"
        self.subtask_id = f"{cn.SUBTASK_PREFIX}{self.project_id}" # base task for the repeated task
        self.repeatedtask_id = f"{cn.REPEATED_TASK}{self.project_id}" # repeated task
        self.report_id = f"{cn.REPORT_PREFIX}{self.project_id}"   # type: ignore
        self.plot_id = f"{cn.PLOT_PREFIX}{self.project_id}"  # type: ignore
        self.simulation_type = simulation_type
        # Create the ScopedCollection
        self.scan_parameter_dct = scan_parameter_dct
        # Set the title
        self.is_plot = is_plot
        self.title = title
        self.addModel(self.model_id, model_ref=model_ref, ref_type=ref_type,
                is_overwrite=True,
                parameter_dct=model_parameter_dct)
        self.addSimulation(self.sim_id, simulation_type=self.simulation_type,
                algorithm=algorithm, time_interval=time_interval)
        self.addTask(self.subtask_id, model_id=self.model_id,
                simulation_id=self.sim_id)
        self.base_model = self.model_dct[self.model_id]
        # Parameter scan does not include time as a display variable
        if cn.TIME in self.initial_display_variables:  # type:ignore
            self._display_variables = self._display_variables.remove(cn.TIME)   # type:ignore
        self._addRepeatedTask()
        self._addReport()
        self._addPlot()

    def _addRepeatedTask(self):
        """Adds a repeated task for the parameter scan"""
        # Make the dataframe with the parameters to be scanned
        parameter_df = pd.DataFrame(self.scan_parameter_dct)
        # Create the repeated task
        self.addRepeatedTask(self.repeatedtask_id, subtask_id=self.subtask_id,
                parameter_df=parameter_df, reset=True)
        # Add the repeated task to the variable collection
        
    def _addReport(self):
        """Adds a report for the parameter scan"""
        # Make the parameter variables
        # Add the report
        all_variables_without_time = self.variable_collection.getScopedVariables(
                self.repeatedtask_id, is_time=False, is_scan_parameters=True,
                is_display_variables=True).lst
        self.addReport(*all_variables_without_time, id=self.report_id,
                title=f"Parameter scan for {self.model_id}")
        
    def _addPlot(self):
        """Adds a plot for the parameter scan"""
        # Add the plot
        scoped_variables = self.variable_collection.getScopedVariables(
                self.repeatedtask_id, is_time=False, is_scan_parameters=True,
                is_display_variables=False).lst
        if len(scoped_variables) > 1:
            warnings.warn("Multiple scan parameters detected. "
                    "Only the first scan parameter will be used for the x-axis. ")
        x_var = scoped_variables[0]
        y_vars = self.variable_collection.getScopedVariables(
                self.repeatedtask_id, is_time=False, is_scan_parameters=False,
                is_display_variables=True).lst
        if self.title is None:
            title = f"Parameter scan for {self.model_id}"
        else:
            title = self.title
        self.addPlot(x_var=x_var, y_var=y_vars,
                title=title,
                id=self.plot_id, is_plot=self.is_plot)
        
    def execute(self, *args)-> pd.DataFrame:  # type:ignore
        """Executes the parameter scan and returns the results as a DataFrame.

        Returns:
            pd.DataFrame: DataFrame with the results of the parameter scan.
        """
        if self.simulation_type == cn.ST_STEADYSTATE:
            # For steadystate, we can execute the repeated task directly
            msg = "Cannot execute parameter scan for steadystate. "
            msg += "\n   Consider using onestep with a large time_interval."
            raise NotImplementedError(msg)
        else:
            return super().execute(*args)  # type:ignore