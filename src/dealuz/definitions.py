"""Defining types which are used by core functions"""


__all__ = [
    "DEAResult",
]


import pandas as pd


class DEAResult:
    """DEA results that should be returned from core estimator functions"""

    def __init__(
        self,
        efficiencies: pd.DataFrame,
        weights: pd.DataFrame,
        model_params: dict[str, list[str] | bool]
    ) -> None:
        """Initializes a result object that is returned by core estimator functions


        Parameters
        ----------
        efficiencies : pd.DataFrame
            A DataFrame which indices are DMUs and columns are the
            efficiency score (the DEA objective function value) and,
            if `reference_set = True`, the `SET` reference of efficient
            DMUs for each DMU

        weights : pd.DataFrame
            A DataFrame with the weights yielded by each DMU problem
            in DEA. The indices represent the DMUs and the columns
            the variables used by the model

        model_params : dict
            A dict containing the params used for the model. This dict
            can be used to run similar models and contain the following
            keys:
                input_oriented : bool
                    Boolean value that defines if model assume constant
                    returns to scale (CRS) if `VRS = False`, else it
                    assumes variable returns to scale (VRS) `VRS = True`
                inputs_list : list
                    List of features that constitute the model's input.
                    Containing the `VRS` column if the model is output-
                    oriented and assume variable returns to scale
                outputs_list : list
                    List of features that constitute the model's output.
                    Containing the `VRS` column if the model is input-
                    oriented and assume variable returns to scale
                input_oriented : bool
                    Boolean value that define an input-oriented model.
                    If False, defines an output-oriented model
        
        """

        self.efficiencies = efficiencies
        self.weights = weights
        self.model_params = model_params

    # Defining this method just so this
    # object can be unpacked and itered
    def __iter__(self):
        return iter([self.efficiencies, self.weights, self.model_params])

