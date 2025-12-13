# coding: utf-8
from __future__ import annotations


import os
import pytest

import numpy

from tomwer.core.process.reconstruction.saaxis.params import SAAxisParams
from tomwer.core.process.reconstruction.saaxis.saaxis import SAAxisTask
from tomwer.core.process.reconstruction.scores.scores import (
    _METHOD_TO_FCT,
    compute_score_contrast_std,
)
from tomwer.core.utils.scanutils import MockNXtomo


def test_img_contrast_std_score():
    """simple test of the API to call compute_score_contrast_std"""
    data = numpy.random.random(100 * 100).reshape(100, 100)
    compute_score_contrast_std(data)


@pytest.mark.parametrize("fct", _METHOD_TO_FCT.values())
def test_method_to_function(fct):
    """Test the dictionary used to for linking the score method to the
    callback function"""
    data = numpy.random.random(100 * 100).reshape(100, 100)
    res = fct(data)
    assert res is not None
    assert isinstance(res, float)


def testSAAxisProcess(tmp_path):
    """Test the SAAxisProcess class"""
    scan_path = tmp_path / "mock_nxtomo"
    scan_path.mkdir()
    # set up
    dim = 10
    mock = MockNXtomo(
        scan_path=scan_path, n_proj=10, n_ini_proj=10, scan_range=180, dim=dim
    )
    mock.add_alignment_radio(index=10, angle=90)
    mock.add_alignment_radio(index=10, angle=0)
    scan = mock.scan

    default_saaxis_params = SAAxisParams()
    default_saaxis_params.output_dir = os.path.join(scan_path, "output_dir")
    default_saaxis_params.slice_indexes = {"slice": 4}
    default_saaxis_params.nabu_config = {}
    default_saaxis_params.dry_run = True
    default_saaxis_params.file_format = "hdf5"

    # test processing
    process = SAAxisTask(
        inputs={
            "data": scan,
            "sa_axis_params": default_saaxis_params.to_dict(),
            "serialize_output_data": False,
            "dry_run": True,
        }
    )

    default_saaxis_params.estimated_cor = 11
    default_saaxis_params.research_width = 2
    process = SAAxisTask(
        inputs={
            "data": scan,
            "sa_axis_params": default_saaxis_params.to_dict(),
            "serialize_output_data": False,
            "dry_run": True,
        },
    )
    process.run()
    process = SAAxisTask(
        inputs={
            "data": scan,
            "sa_axis_params": default_saaxis_params.to_dict(),
            "serialize_output_data": False,
            "dry_run": True,
        },
    )
    process.run()
