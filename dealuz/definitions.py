"""Defining types which are returned by core functions"""


__all__ = [
    "DEAResult",
]


import pandas as pd


class DEAResult:
    def __init__(
        self,
        efficiencies: pd.DataFrame,
        weights: pd.DataFrame,
        model_params: dict[str, list[str] | bool]
    ) -> None:
        self.efficiencies = efficiencies
        self.weights = weights
        self.model_params = model_params

    def __iter__(self):
        return iter([self.efficiencies, self.weights, self.model_params])
