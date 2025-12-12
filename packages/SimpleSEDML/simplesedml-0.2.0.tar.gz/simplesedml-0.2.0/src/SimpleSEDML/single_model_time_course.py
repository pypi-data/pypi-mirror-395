from SimpleSEDML.simple_sedml import SimpleSEDML # type:ignore
from SimpleSEDML.model_information import ModelInformation # type:ignore
from SimpleSEDML import constants as cn # type:ignore

from typing import Optional, List


class SingleModelTimeCourse(SimpleSEDML):
    """Class to create a time course simulation for a single model"""

    def __init__(self,
            model_ref:str,
            project_id:Optional[str]=None,
            ref_type:Optional[str]=None,
            simulation_type:str=cn.ST_UNIFORM,
            project_dir:Optional[str]=None,
            display_variables:Optional[List[str]]=None,
            start:float=0,
            end:float=5,
            num_step:Optional[int]=None,
            num_point:Optional[int]=None,
            title:Optional[str]=None,
            algorithm:Optional[str]=None,
            is_plot:bool=True,
            model_parameter_dct:Optional[dict]=None):
        """Creates a time course simulation

        Args:
            model_ref: reference to the model
            project_id: ID of the project, if None, uses the default project ID
            ref_type: type of the reference (e.g. "sbml_str", "ant_str", "sbml_file", "ant_file", "sbml_url")
            simulation_type: type of the simulation
                    (e.g., "uniform", "uniform_stochastic", "steadystate", "onestep")
            project_dir: directory to save the files
            display_variables: variables to be plotted and included the report
            start: start time
            end: end time
            num_step: number of steps
            num_point: number of points to be plotted
            algorithm: algorithm to use for the simulation
            title: title of the plot
            is_plot: if True, plot the results
            model_parameter_dct: dictionary of parameters whose values are changed

        Returns:
            SingleModelTimeCourse: a time course simulation object
        """
        super().__init__(project_dir=project_dir, project_id=project_id,
                display_variables=display_variables)
        #
        model_id = f"{self.project_id}_model"
        sim_id = f"{self.project_id}_sim"
        task_id = f"{self.project_id}_task"
        if title is None:
            title = ""
        #
        self.addModel(model_id, model_ref=model_ref, ref_type=ref_type, is_overwrite=True,
                parameter_dct=model_parameter_dct)
        self.model = self.model_dct[model_id]
        self.addSimulation(sim_id, simulation_type=simulation_type,
                start=start, end=end, num_step=num_step, num_point=num_point,
                algorithm=algorithm)
        self.addTask(task_id, model_id, sim_id)
        if display_variables is None:
            model_information = ModelInformation.getFromModel(self.model)
            display_variables = list(model_information.floating_species_dct.keys())
            display_variables = [task_id + cn.SCOPE_INDICATOR + var for var in display_variables]
            display_variables.insert(0, "time")   # type: ignore
        self.addReport(*display_variables, title=title)
        x1_var = display_variables[0]
        y_vars = display_variables[1:]
        self.addPlot(x1_var, y_vars, title=title, is_plot=is_plot)