import SimpleSEDML.constants as cn # type: ignore

from typing import Optional, List, Union

class Plot:
    def __init__(self, x_var:str, y_var:Union[str, List[str]], z_var:Optional[str]=None, title:Optional[str]=None,
            is_plot:bool=True)->None:  
        """
        Plot class to represent a plot in the script. The following cases are supported:
            plot x vs y (z is None, y is str)
            plot x vs y1, y2, y3 (z is None, y is a list of str)
            plot x vs y vs z  (z is a str, y is str)

        Args:
            x_var (str): x variable
            y_var (str): y variable
            z_var (str, optional): z variable. Defaults to None.
            title (str, optional): title of the plot. Defaults to None.
        """
        self.x_var = x_var
        self.y_var = y_var
        self.z_var = z_var
        self.title = title
        self.is_plot = is_plot

    def getPhraSEDML(self, **kwargs)->str:
        if len(kwargs) > 0:
            raise ValueError("No keyword arguments are allowed.")
        if not self.is_plot:
            return ""
        if self.z_var is None:
            if isinstance(self.y_var, str):
                y_vars = [self.y_var]
            else:
                y_vars = self.y_var
            var_clause = f'{self.x_var} vs {", ".join(y_vars)}'
        else:
            if not isinstance(self.y_var, str):
                raise ValueError("y_var must be a string when z_var is provided")
            var_clause = f"{self.x_var} vs {self.y_var} vs {self.z_var}"
        if self.title is None:
            return f"plot {var_clause}"
        else:
            return f"plot \"{self.title}\" {var_clause}"
        
    def __str__(self)->str:
        """String representation of the plot object. This is used to
        generate the SED-ML string.

        Returns:
            str: PhraSED-ML string
        """
        return self.getPhraSEDML()