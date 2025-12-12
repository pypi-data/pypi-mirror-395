'''Abstraction for a task, the combination of a model and a simulation.'''

import pandas as pd; # type: ignore


class Task:
    def __init__(self, id:str, model_id:str, simulation_id:str):
        self.id = id
        self.model_id = model_id
        self.simulation_id = simulation_id

    def getPhraSEDML(self, **kwargs)->str:
        if len(kwargs) > 0:
            raise ValueError("No keyword arguments are allowed.")
        result = f'{self.id} = run {self.simulation_id} on {self.model_id}'
        return result
    
    def __str__(self)->str:
        """String representation of the task object. This is used to
        generate the SED-ML string.

        Returns:
            str: PhraSED-ML string
        """
        return self.getPhraSEDML()


class RepeatedTask:
    # A RepeatedTask executes a task with changes in the values of global parameters.
    # Ex: repeat1 = repeat nested_task for S1 in [1, 3, 5], S2 in [0, 10, 3], reset=true
    # Note that it is not necessary to specify functions as in the original phraSED-ML since python provides this.

    def __init__(self, id:str, subtask_id:str, parameter_df:pd.DataFrame, reset:bool=True):
        """Repeats a single task with changes in global parameters.

        Args:
            id (str): Identity of repeated task
            subtask_id (Task): Task to be repeated
            parameter_df (pd.DataFrame): DataFrame with the parameters to be changed. Column names must be global parameters.
            reset (bool, optional): _description_. Defaults to True.
        """
        #
        self.id = id
        self.subtask_id = subtask_id
        self.parameter_df = parameter_df
        self.reset = reset

    def _makeChangeValues(self)->str:
        """Creates a string with the changes in the values of global parameters.

        Args:
            ser (pd.Series): Series with the changes in the values of global parameters.

        Returns:
            str: String with the changes in the values of global parameters.
        """
        lines = []
        for col in self.parameter_df.columns:
            values = ", ".join([str(v) for v in self.parameter_df[col].values])
            lines.append(f'{col} in [{values}]')
        result = ", ".join(lines)
        return result

    def getPhraSEDML(self)->str:
        line = f'{self.id} = repeat {self.subtask_id} for '
        line += self._makeChangeValues()
        line += f', reset={str(self.reset).lower()}'
        return line
    
    def __str__(self)->str:
        """PhrasedML string representation.

        Returns:
            str: PhraSED-ML string
        """
        return self.getPhraSEDML()