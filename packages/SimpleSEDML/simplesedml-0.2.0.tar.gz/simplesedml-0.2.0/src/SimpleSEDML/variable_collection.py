'''Manage variables in SED-ML documents.'''

"""
Display variables are used in plots and reports.
Parameters are used in parameter scans to specify values for the simulation.
Find default display variables.
Find display names for display variables.
Modify SEDML to use display names for display variables.
"""

import SimpleSEDML.constants as cn # type:ignore
from SimpleSEDML.model_information import ModelInformation # type:ignore
from SimpleSEDML.model import Model # type:ignore
import SimpleSEDML.utils as utils # type:ignore

import collections
from typing import Optional, List, Dict, Union
import warnings


ScopedVariableResult = collections.namedtuple("ScopedVariableResult",["dct", "lst"])


class VariableCollection(object):

    def __init__(self,
                model:Model,
                display_variables:Optional[List[str]]=None,
                scan_parameters:Optional[List[str]]=None,
                scope_strs:Optional[List[str]]=None,
                is_time:bool=True) -> None:
        """
        Args:
            model (Model): _description_
            display_variables (Optional[List[str]], optional): _description_. Defaults to None.
            scan_parameters (Optional[List[str]], optional): Parameters for scans. Defaults to None.
            scope_strs (Optional[List[str]], optional): List of scopes for display variables. Defaults to None.
            is_time (bool, optional): Whether to include time in the display variables. Defaults to True.
        """
        if scan_parameters is None:
            scan_parameters = []
        #
        self.model = model
        self._display_variables = display_variables
        self.scan_parameters:List[str] = scan_parameters
        self.is_time = is_time
        if scope_strs is None:
            scope_strs = []
        #
        self.scope_strs:List[str] = scope_strs

    @property
    def display_variables(self)->List[str]:
        """Returns list of display variables. If unspecified, use all variables
        from the first model.

        Returns:
            Optional[List[str]]: list of display variables
        """
        if self._display_variables is None:
            model_info = ModelInformation.getFromModel(self.model)
            display_variables = list(model_info.floating_species_dct.keys())
        else:
            display_variables = list(self._display_variables)
        if self.is_time and (not cn.TIME in display_variables):
            display_variables.insert(0, cn.TIME)   # type: ignore
        return display_variables

    def addScanParameters(self, variable_names:List[str]) -> None:
        self.scan_parameters.extend(variable_names)

    def addDisplayVariables(self, variable_names:List[str]) -> None:
        self.display_variables.extend(variable_names)
    
    def addScopeStrs(self, scope_strs:List[str]) -> None:
        """Adds scope strings to the variable collection.

        Args:
            scope_strs (List[str]): List of scope strings to add
        """
        for scope_str in scope_strs:
            if not scope_str in self.scope_strs:
                self.scope_strs.append(scope_str)

    def getScopedVariables(self, 
            scope_str:Union[str, List[str]],
            is_time:bool=True, 
            is_scan_parameters:bool=True,
            is_display_variables:bool=True) -> ScopedVariableResult:
        """Adds scope to the variables requested

        Args:
            scope_str (str or List[str]): string used to scope variables
            is_time (bool, optional): Include time
            is_parameters (bool, optional): Include parameters (from repeated task)
            is_display_variables (bool, optional): Include display variables

        Returns:
            ScopedVariableResult: Named tuple with two elements:
                dct (Dict[str, str]): Dictionary of scoped variables
                    key: variable name
                    value: Names of scoped variables
                list (List[str]): List of scoped variable names
        """
        ##
        def addScopeStr(variables:List[str])->Dict[str, str]:
            """Adds scope to the variables"""
            result_dct:dict = {}
            if len(scope_strs) == 0:  # No scoping
                result_dct = {v: [v] for v in variables}
            else:
                for scope_str in scope_strs:
                    dct = {v: f"{scope_str}{cn.SCOPE_INDICATOR}{v}" for v in variables
                        if v != cn.TIME}
                    for k in dct.keys():
                        if not k in result_dct:
                            result_dct[k] = []
                    [result_dct[k].append(dct[k]) for k, v in dct.items()]
                if is_time and cn.TIME in variables:
                    result_dct[cn.TIME] = [cn.TIME]
            return result_dct
        ##
        if isinstance(scope_str, str):
            scope_strs = [scope_str]
        else:
            scope_strs = scope_str
        scope_strs.extend(self.scope_strs)
        #
        variables = []
        if is_scan_parameters:
            variables.extend(self.scan_parameters)
        if is_display_variables:
            variables.extend(self.display_variables)
        if not is_time:
            if cn.TIME in variables:
                variables.remove(cn.TIME)
        result_dct = addScopeStr(variables)
        result_list:list = []
        [result_list.extend(v) for v in result_dct.values()]   # type:ignore
        return ScopedVariableResult(dct=result_dct, lst=result_list)
    
    def getDisplayNameDct(self,
            #scope_str:Optional[Union[str, List[str]]]=None,
            is_time:bool=True) -> Dict[str, str]:
        """Finds the display names for display variables and scan parameters.
        If an element does not have a display name, its element id is used.
        This dictionary is used in editing SEDML to use display names.

        Args:
            is_time (bool): Whether to include time in the display names

        Returns:
            Dict[str, str]: Dictionary of display names
                key: unscoped variable name
                value: display name
        """
        dct = utils.makeDisplayNameDct(self.model.source)
        result_dct = {k: v for k, v in dct.items()
                if (k in self.display_variables) or (k in self.scan_parameters)}
        return result_dct
    
    def getScopedTime(self) -> str:
        """Get the first scoped time variable.

        Returns:
            str: first task ID
        """
        if len(self.scope_strs) == 0:
            raise ValueError("No scope strings have been added. Call addScopeStrs() first.")
        return self.scope_strs[0] + cn.SCOPE_INDICATOR + cn.TIME
    
    def getScopedDisplayDct(self, scoped_variables:Optional[List[str]]=None)->Dict[str, str]:
        """Dictionary maps scoped variable to its display name.

        Args:
            scoped_variables (List[str]): List of scoped variables to get display names
                If None, all display variables are used.

        Returns:
            Dict[str, str]: Dictionary of scoped display variables
                key: scoped variable name
                value: displayname
        """
        if scoped_variables is None:
            scoped_variables = self.display_variables
        #
        scoped_display_dct = {}
        scope_dct = self.getScopedVariables([]).dct
        display_dct = self.getDisplayNameDct()
        for scoped_var in scoped_variables:
            for unscoped_var, scoped_vars in scope_dct.items():
                if scoped_var in scoped_vars:
                    scoped_display_dct[scoped_var] = display_dct.get(unscoped_var,
                            unscoped_var)
        return scoped_display_dct

    def getInvertedScopeDct(self,  scope_strs:Optional[List[str]]=None) -> Dict[str, str]:
        """Dictionary maps scoped variable to unscoped variable.

        Args:
            scope_strs (List[str]): List of scope strings

        Returns:
            Dict[str, str]: Dictionary of scoped display variables
                key: scoped variable name
                value: unscoped variable name 
        """
        if scope_strs is None:
            scope_strs = []
        scoped_dct = self.getScopedVariables(scope_strs).dct
        result_dct = {}
        #
        for unscoped_var, scoped_vars in scoped_dct.items():
            for scoped_var in scoped_vars:
                if not scoped_var in result_dct:
                    result_dct[scoped_var] = unscoped_var
        return result_dct