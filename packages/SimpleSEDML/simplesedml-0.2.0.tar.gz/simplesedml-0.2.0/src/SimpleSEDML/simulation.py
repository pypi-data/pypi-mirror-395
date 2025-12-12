'''Simulation directives for PhraSEDML'''
import SimpleSEDML.constants as cn # type: ignore

from typing import Optional




class Simulation:
    def __init__(self, id:str, 
            simulation_type:str=cn.ST_UNIFORM,
            start:Optional[float]=None,
            end:Optional[float]=None,
            num_step:Optional[int]=None,
            num_point:Optional[int]=None,
            time_interval:float=0.5, # required for onestep
            absolute_tolerance:Optional[float]=None,
            algorithm:Optional[str]=None,
            initial_time_step:Optional[float]=None,
            maximum_adams_order:Optional[int]=None,
            maximum_bdf_order:Optional[int]=None,
            maximum_iterations:Optional[int]=None,
            maximum_num_steps:Optional[int]=None,
            maximum_time_step:Optional[float]=None,
            minimum_damping:Optional[float]=None,
            minimum_time_step:Optional[float]=None,
            relative_tolerance:Optional[float]=None,
            seed:Optional[int]=None,
            variable_step_size:Optional[bool]=None):
        """Simulation class for SED-ML
        Args: 
            id (str): identifier for the simulation
            simulation_type (str): type of simulation
                - "uniform": uniform simulation
                - "uniform_stochastic": stochastic simulation
                - "steadystate": one-step simulation
            start (float): start time for the simulation
            end (float): end time for the simulation
            num_step (int): number of steps for the simulation
            num_point (int): number of points for the simulation must be num_step + 1
            time_interval (float): time interval for the simulation
            algorithm (str): algorithm to use for the simulation. Defaults are:
                - "CVODE": CVODE algorithm
                - "gillespie": Gillespie algorithm
        """
        if simulation_type not in cn.ST_SIMULATION_TYPES:
            raise ValueError(f"simulation_type must be one of {cn.ST_SIMULATION_TYPES}")
        if simulation_type in [cn.ST_ONESTEP, cn.ST_UNIFORM]:
            if algorithm is None:
                algorithm = cn.D_SIM_UNIFORM_ALGORITHM
        elif simulation_type == cn.ST_UNIFORM_STOCHASTIC:
            if algorithm is None:
                algorithm = cn.D_SIM_UNIFORM_STOCHASTIC_ALGORITHM
        #
        self.id = id
        self.simulation_type = simulation_type
        self.time_interval = time_interval
        # Handle start
        if simulation_type in [cn.ST_UNIFORM, cn.ST_UNIFORM_STOCHASTIC, cn.ST_ONESTEP]:
            if start is None:
                self.start = cn.D_START
            else:
                self.start = start
        if simulation_type in [cn.ST_UNIFORM, cn.ST_UNIFORM_STOCHASTIC]:
            # Handle end
            if end is None:
                self.end = cn.D_END
            else:
                self.end = float(end)
            if self.start >= self.end:
                raise ValueError("start must be less than end")
            # Handle num_step and num_point
            if (num_step is None) and (num_point is None):
                self.num_step = cn.D_NUM_STEP
            elif (num_step is None) and (num_point is not None):
                self.num_step = num_point - 1
            elif (num_step is not None) and (num_point is None):
                self.num_step = num_step
            else:
                if num_step != num_point - 1:  # type: ignore
                    raise ValueError("num_point must be num_step + 1")
                self.num_step = num_step
            self.num_point = self.num_step + 1   # type: ignore
        # Determine the simulation algorithm
        if algorithm is None:
            if simulation_type == cn.ST_UNIFORM:
                algorithm = cn.D_ALGORITHM
            elif simulation_type == cn.ST_UNIFORM_STOCHASTIC:
                algorithm = "gillespie"
        self.algorithm = algorithm
        # Setup the options
        self.option_dct =  dict(
                absolute_tolerance=absolute_tolerance,
                algorithm=algorithm,
                initial_time_step=initial_time_step,
                maximum_adams_order=maximum_adams_order,
                maximum_bdf_order=maximum_bdf_order,
                maximum_iterations=maximum_iterations,
                maximum_num_steps=maximum_num_steps,
                maximum_time_step=maximum_time_step,
                minimum_damping=minimum_damping,
                minimum_time_step=minimum_time_step,
                relative_tolerance=relative_tolerance,
                seed=seed,
                variable_step_size=variable_step_size
            )

    def getPhraSEDML(self, **kwargs)->str:
        if len(kwargs) > 0:
            raise ValueError("No keyword arguments are allowed.")
        #
        line = f'{self.id} = simulate %s' % self.simulation_type
        if self.simulation_type == cn.ST_UNIFORM:
            line += f'({self.start}, {self.end}, {self.num_step})'
        elif self.simulation_type == cn.ST_UNIFORM_STOCHASTIC:
            line += f'({self.start}, {self.end}, {self.num_step})'
        elif self.simulation_type == cn.ST_ONESTEP:
            line += f'({self.time_interval})'
        # Include the options
        lines = [line]
        option_lines:list = []
        if self.simulation_type != cn.ST_ONESTEP:
            option_lines = [f"{self.id}.algorithm.{k} = {str(v)} "
                    for k, v in self.option_dct.items() 
                    if (v is not None) and (k != "algorithm")]
            if self.algorithm is not None:
                option_lines.append(f"{self.id}.algorithm = {self.algorithm}")
            lines.extend(option_lines)
        section = "\n".join(lines)
        return section
    
    def __str__(self)->str:
        return self. getPhraSEDML()