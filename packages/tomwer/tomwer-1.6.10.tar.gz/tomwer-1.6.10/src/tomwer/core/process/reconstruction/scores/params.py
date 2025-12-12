from __future__ import annotations

from tomwer.core.cluster.cluster import SlurmClusterConfiguration
from tomwer.core.process.reconstruction.scores.scores import ScoreMethod
from tomwer.core.utils.deprecation import deprecated


class SABaseParams:
    """Parameters for the semi-automatic axis calculation"""

    _VALID_FILE_FORMAT = ("hdf5", "h5", "hdf", "npy", "npz", "tiff", "jp2", "jp2k")

    def __init__(self):
        self._n_reconstruction = 20
        self._slice_indexes = "middle"
        self._nabu_recons_params = {}
        self._dry_run = False
        self._output_dir = None
        self._score_method = ScoreMethod.TV
        self._scores = None
        self._autofcous = None
        "scores. expected cor value as key and a tuple (score, url) as value"
        self._file_format = "hdf5"
        self._image_width = None
        self._cluster_config = None

    @property
    def autofocus(self):
        return self._autofcous

    @autofocus.setter
    def autofocus(self, autofocus):
        self._autofcous = autofocus

    @property
    def n_reconstruction(self):
        return self._n_reconstruction

    @n_reconstruction.setter
    def n_reconstruction(self, n):
        self._n_reconstruction = n

    @property
    def slice_indexes(self) -> dict | str | None:
        return self._slice_indexes

    @slice_indexes.setter
    def slice_indexes(self, indexes: dict | str | None):
        if isinstance(indexes, str):
            if not indexes == "middle":
                raise ValueError("the only valid indexes values is 'middle'")
        elif not isinstance(indexes, (type(None), dict)):
            raise TypeError(
                f"index should be an instance of int or None and not {type(indexes)}"
            )
        self._slice_indexes = indexes

    @property
    def nabu_recons_params(self) -> dict:
        return self._nabu_recons_params

    @nabu_recons_params.setter
    def nabu_recons_params(self, params: dict):
        if not isinstance(params, dict):
            raise TypeError(f"params should be a dictionary and not {type(params)}")
        self._nabu_recons_params = params

    @property
    @deprecated(replacement="nabu_recons_params", since_version="1.2")
    def nabu_params(self) -> dict:
        return self.nabu_recons_params

    @nabu_params.setter
    @deprecated(replacement="nabu_recons_params", since_version="1.2")
    def nabu_params(self, params: dict):
        self.nabu_recons_params = params

    @property
    def dry_run(self) -> bool:
        return self._dry_run

    @dry_run.setter
    def dry_run(self, dry_run: bool):
        if not isinstance(dry_run, bool):
            raise ValueError("dry_run should be a bool")
        self._dry_run = dry_run

    @property
    def output_dir(self) -> str | None:
        """nabu cfg_files output dir. If not provided will use nabu slice output with saaxis/cfg_files as postfix"""
        return self._output_dir

    @output_dir.setter
    def output_dir(self, output_dir: str | None) -> None:
        if not isinstance(output_dir, (str, type(None))):
            raise TypeError("output_dir should be None or a str")
        self._output_dir = output_dir

    @property
    def score_method(self):
        return self._score_method

    @score_method.setter
    def score_method(self, method):
        self._score_method = ScoreMethod(method)

    @property
    def scores(self) -> dict | None:
        return self._scores

    @scores.setter
    def scores(self, scores: dict | None):
        if not isinstance(scores, (type(None), dict)):
            raise TypeError("scores should be None or a dictionary")
        self._scores = scores

    @property
    def file_format(self) -> str:
        return self._file_format

    @file_format.setter
    def file_format(self, format_: str):
        if not isinstance(format_, str):
            raise TypeError("format should be a str")
        if format_ not in self._VALID_FILE_FORMAT:
            raise ValueError(
                f"requested format ({format_}) is invalid. valid ones are {self._VALID_FILE_FORMAT}"
            )
        self._file_format = format_

    @property
    def cluster_config(self) -> dict | None:
        return self._cluster_config

    @cluster_config.setter
    def cluster_config(self, config: dict | None):
        if isinstance(config, SlurmClusterConfiguration):
            config = config.to_dict()
        if not isinstance(config, (dict, type(None))):
            raise TypeError(
                "config is expected to be None, a dict or SlurmClusterConfiguration"
            )
        self._cluster_config = config

    def to_dict(self) -> dict:
        return {
            "slice_index": self.slice_indexes or "",
            "nabu_params": self.nabu_recons_params,
            "dry_run": self.dry_run,
            "output_dir": self.output_dir or "",
            "score_method": self.score_method.value,
            "cluster_config": (
                self.cluster_config if self.cluster_config is not None else ""
            ),
        }

    def load_from_dict(self, dict_: dict):
        if "slice_index" in dict_:
            slice_index = dict_["slice_index"]
            if slice_index == "":
                slice_index = None
            self.slice_indexes = slice_index
        if "nabu_params" in dict_:
            self.nabu_recons_params = dict_["nabu_params"]
        if "dry_run" in dict_:
            self.dry_run = bool(dict_["dry_run"])
        if "output_dir" in dict_:
            output_dir = dict_["output_dir"]
            if output_dir == "":
                output_dir = None
            self.output_dir = output_dir
        if "score_method" in dict_:
            self.score_method = ScoreMethod(dict_["score_method"])
        if "cluster_config" in dict_:
            if dict_["cluster_config"] in (None, ""):
                self.cluster_config = None
            else:
                self.cluster_config = dict_["cluster_config"]

    @staticmethod
    def from_dict(dict_):
        res = SABaseParams()
        res.load_from_dict(dict_=dict_)
        return res
