# coding: utf-8
from __future__ import annotations

from tomwer.core.process.reconstruction.nabu.utils import retrieve_lst_of_value_from_str
from tomwer.core.process.reconstruction.scores.params import SABaseParams


class SADeltaBetaParams(SABaseParams):
    """Parameters for the semi-automatic axis calculation"""

    def __init__(self):
        super().__init__()
        self._delta_beta_values = (100,)
        self._selected_db = None

    @property
    def delta_beta_values(self):
        return self._delta_beta_values

    @delta_beta_values.setter
    def delta_beta_values(self, delta_beta_values):
        if isinstance(delta_beta_values, str):
            self._delta_beta_values = retrieve_lst_of_value_from_str(
                delta_beta_values, type_=float
            )
        else:
            self._delta_beta_values = delta_beta_values

    def set_db_selected_value(self, value):
        self._selected_db = value

    @property
    def selected_delta_beta_value(self) -> float | None:
        return self._selected_db

    def to_dict(self) -> dict:
        my_dict = super().to_dict()
        my_dict.update(
            {
                "delta_beta_values": self.delta_beta_values,
                "selected_db_value": self.selected_delta_beta_value,
            }
        )
        return my_dict

    def load_from_dict(self, dict_: dict):
        if not isinstance(dict_, dict):
            raise TypeError(f"dict_ should be an instance of dict not {type(dict_)}")
        super().load_from_dict(dict_)
        if "delta_beta_values" in dict_:
            self.delta_beta_values = dict_["delta_beta_values"]
        if "selected_db_value" in dict_:
            self.set_db_selected_value(value=dict_["selected_db_value"])

    @staticmethod
    def from_dict(dict_):
        params = SADeltaBetaParams()
        params.load_from_dict(dict_=dict_)
        return params

    def check_configuration(self):
        """
        Insure all requested information for processing the SAAXis are here.
        :raises: ValueError if some information are missing
        """
        missing_information = []
        if self.delta_beta_values is None or len(self.delta_beta_values) == 0:
            missing_information.append("no values for center of rotation provided")
        if self.slice_indexes is None:
            missing_information.append("slice index not provided")
        if len(missing_information) > 0:
            missing_information_str = " ; ".join(missing_information)
            raise ValueError(
                f"Some informations are missing: {missing_information_str}"
            )

    def __str__(self):
        return str(self.to_dict())
