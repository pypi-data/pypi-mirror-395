'''Executes the script represented in a SimpleSEDML.'''

import SimpleSEDML.constants as cn # type: ignore
from SimpleSEDML.simple_sedml import SimpleSEDML # type:ignore

import collections # type: ignore
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
import pandas as pd # type: ignore
from typing import Optional, List, Union, Any
import warnings # type: ignore

# Handle multiple scan parameters by using color/markers and a legend


ScopeResult = collections.namedtuple('ScopeResult', ['task_ids', 'repeated_task_ids'])
PlotResult = collections.namedtuple('PlotResult', ['ax', 'plot_ids'])


class Executor(object):
    """Executes the script represented in a SimpleSEDML."""

    def __init__(self, simple: SimpleSEDML):
        """Initializes the executor with a SimpleSEDML object.
        Must have completed all API calls before running executor. Subsequent API calls
        are ignored.

        Args:
            simple (SimpleSEDML): The SimpleSEDML object to execute.
        """
        self.simple = simple

    def executeTask(self, task_id:Optional[str]=None,
            scan_parameter_dct:Optional[dict]=None)->pd.DataFrame:
        """Executes a task by its ID and returns the results as a DataFrame.
        The result is saved in self.result_df.

        Args:
            task_id (str): The ID of the task to execute.
            scan_parameter_dct (Optional[dict]): Dictionary of parameters to change for the task execution.

        Returns:
            pd.DataFrame: The results of the task execution.
        """
        if (len(self.simple.task_dct) == 0) and (len(self.simple.repeated_task_dct) == 0):
            _ = self.simple.getPhraSEDML()  # Ensure that the object dictionaries are populated
        # Initialization
        if scan_parameter_dct is None:
            parameter_dct:dict = {}
        else:
            parameter_dct = dict(scan_parameter_dct)  # type: ignore
        #
        if task_id is None:
            if len(self.simple.task_dct) == 0:
                raise ValueError("No task ID provided and no tasks available.")
            if len(self.simple.task_dct) > 1:
                raise ValueError("Multiple tasks available, please provide a task ID.")
            task_id = list(self.simple.task_dct.keys())[0]
        task = self.simple.task_dct.get(task_id, None)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found.")
        model = self.simple.model_dct[task.model_id]
        simulation = self.simple.simulation_dct[task.simulation_id]
        selections = self.simple.variable_collection.display_variables
        # Initialize the roadrunner model
        roadrunner = model.roadrunner
        roadrunner.resetAll()  # Reset the model before simulation
        roadrunner.integragtor = simulation.option_dct.get('algorithm', None)
        parameter_dct.update(model.parameter_dct)  # Include model parameters
        for parameter, value in parameter_dct.items():
            if not parameter in roadrunner.keys():
                raise ValueError(f"Parameter {parameter} not found in model {model.id}.")
            roadrunner[parameter] = value
        # Run the simulation
        if simulation.simulation_type == cn.ST_ONESTEP:
            end = simulation.start + simulation.time_interval
            result_arr = roadrunner.simulate(simulation.start, end, 2,
                    selections=selections)
        elif simulation.simulation_type == cn.ST_UNIFORM:
            result_arr = roadrunner.simulate(simulation.start, simulation.end,
                    simulation.num_point, selections=selections)
        elif simulation.simulation_type == cn.ST_UNIFORM_STOCHASTIC:
            result_arr = roadrunner.simulate(simulation.start, simulation.end,
                    simulation.num_point, selections=selections)
        elif simulation.simulation_type == cn.ST_STEADYSTATE:
            roadrunner.steadyStateSelections = selections
            result_arr = roadrunner.getSteadyStateValues()
            result_arr = np.reshape(result_arr, (1, len(result_arr)))  # Convert to 2D array
        else:
            raise ValueError(f"Unknown simulation type: {simulation.simulation_type}")
        # Convert to a DataFrame
        return pd.DataFrame(result_arr, columns=selections)

    def executeRepeatedTask(self, repeated_task_id:Optional[str]=None)-> pd.DataFrame:
        """Executes a repeated task by its ID and returns the results as a DataFrame.

        Args:
            repeated_task_id (str): The ID of the repeated task to execute.

        Returns:
            pd.DataFrame: The results of the repeated task execution.
        """
        if (len(self.simple.task_dct) == 0) and (len(self.simple.repeated_task_dct) == 0):
            _ = self.simple.getPhraSEDML()  # Ensure that the object dictionaries are populated
        # Initialization
        if repeated_task_id is None:
            if len(self.simple.repeated_task_dct) == 0:
                raise ValueError("No repeated task ID provided and no repeated tasks available.")
            if len(self.simple.repeated_task_dct) > 1:
                raise ValueError("Multiple repeated tasks available, please provide a repeated task ID.")
            repeated_task_id = list(self.simple.repeated_task_dct.keys())[0]
        #
        repeated_task = self.simple.repeated_task_dct.get(repeated_task_id, None)
        if not repeated_task:
            raise ValueError(f"Repeated task with ID {repeated_task_id} not found.")
        scan_parameter_df = repeated_task.parameter_df
        dfs:list =  []
        for _, row in scan_parameter_df.iterrows():
            parameter_dct = row.to_dict()
            df = self.executeTask(repeated_task.subtask_id, scan_parameter_dct=parameter_dct)
            for name, value in parameter_dct.items():
                df[name] = value
            dfs.append(df)
        # Construct the result
        return pd.concat(dfs, ignore_index=True)

    def getScopeResult(self, variables:List[str])->ScopeResult:
            """Find the scopes, the ids of tasks and repeated tasks referenced."""
            task_ids:list = []
            repeated_task_ids:list = []
            # Check if variables are scoped
            if all([len(variable.split('.')) > 1 for variable in variables]):
                is_scoped = True
            else:
                if any([len(variable.split('.')) > 1 for variable in variables]):
                    raise ValueError("All variables must be scoped or none must be scoped.")
                is_scoped = False
            # Update tasks
            if not is_scoped:
                task_ids = list(self.simple.task_dct.keys())
            else:
                # Extract the task ids
                scope_ids = [variable.split('.')[0] for variable in variables]
                for scope_id in scope_ids:
                    if scope_id in self.simple.task_dct:
                        task_ids.append(scope_id)
                    elif scope_id in self.simple.repeated_task_dct:
                        repeated_task_ids.append(scope_id)
                    else:
                        raise ValueError(f"Scope ID {scope_id} not found in tasks or repeated tasks.")
            task_ids = list(set(task_ids))  # Remove duplicates
            repeated_task_ids = list(set(repeated_task_ids))
            return ScopeResult(task_ids=task_ids, repeated_task_ids=repeated_task_ids)
    
    def executePlot2d(self, plot_id:Optional[str]=None,
            ax=None, kind:str='line', is_plot:bool=True)->PlotResult:
        """Executes a 2D plot

        Args:
            plot_id (str): identifier of the plot to execute
            ax: Matplotlib Axes
            kind (str, optional): Type of plot to create. Defaults to 'line'.

        Returns:
            PlotResult:
                ax (Axes): Matplotlib Axes object with the plot
                plot_ids (List[str]): List of plot IDs present in the SimpleSEDML object
        """
        if (len(self.simple.task_dct) == 0) and (len(self.simple.repeated_task_dct) == 0):
            _ = self.simple.getPhraSEDML()  # Ensure that the object dictionaries are populated
        # Initialization
        plot_ids = list(self.simple.plot_dct.keys())
        if plot_id is None:
            if len(self.simple.plot_dct) == 0:
                raise ValueError("No plot ID provided and no plots available.")
            if len(self.simple.plot_dct) > 1:
                warnings.warn("Multiple plots available. Plotting the first.")
            plot_id = plot_ids[0]
        # Get the plot object
        plot = self.simple.plot_dct.get(plot_id, None)
        if not plot:
            raise ValueError(f"Plot with ID {plot_id} not found.")
        if plot.z_var is not None:
            raise ValueError("Cannot do 3D plot.")
        # Get the variables
        x_var = plot.x_var
        if isinstance(plot.y_var, str):
            y_vars = [plot.y_var]
        else:
            y_vars = plot.y_var
        y_vars = y_vars
        # Run the tasks that produce data
        scoped_variables = [x_var]
        scoped_variables.extend(y_vars)
        scope_result = self.getScopeResult(scoped_variables)
        dfs:list = []
        for task_id in scope_result.task_ids:
            dfs.append(self.executeTask(task_id))
        for repeated_task_id in scope_result.repeated_task_ids:
            dfs.append(self.executeRepeatedTask(repeated_task_id))
        data_df = pd.concat(dfs, axis=1, ignore_index=True)
        data_df.columns = dfs[0].columns
        # Construct the plot dataframe
        scoped_unscoped_dct = self.simple.variable_collection.getInvertedScopeDct()
        display_dct = self.simple.variable_collection.getDisplayNameDct()
        columns = [scoped_unscoped_dct[v] for v in scoped_variables]
        unscoped_x_var = scoped_unscoped_dct[x_var]
        columns.remove(unscoped_x_var)  # Remove x_var from the columns
        columns.insert(0, unscoped_x_var)  # Insert x_var at the beginning
        plot_df = data_df[columns]
        display_names = [display_dct.get(v, v) for v in columns]
        plot_df.columns = display_names
        # Do the plot
        if ax is None:
            _, ax = plt.subplots()
        if is_plot:
            ax = plot_df.plot(x=columns[0], y=display_names[1:], kind=kind, ax=ax)  # type: ignore
        if not is_plot:
            ax.clear()
            ax = None
        return PlotResult(ax=ax, plot_ids=plot_ids)
    
    def cleanUp(self):
        """Cleans up the executor by clearing the SimpleSEDML object."""
        self.simple.cleanUp()