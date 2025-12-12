import os

import numpy
import pytest

from tomwer.core.process.reconstruction.axis.params import (
    AxisCalculationInput,
    AxisResource,
)
from tomwer.core.utils.scanutils import MockNXtomo


def test_axis_resource(tmp_path):
    """
    Test AxisResource class
    """

    mock = MockNXtomo(
        scan_path=os.path.join(tmp_path, "scan1"),
        n_proj=10,
        n_ini_proj=10,
        scan_range=180,
        dim=100,
    )
    scan = mock.scan

    first_proj = list(scan.projections.keys())[0]
    data_url = scan.projections[first_proj]

    axis_resource = AxisResource(url=data_url)
    assert axis_resource.data is not None

    with pytest.raises(TypeError):
        axis_resource.normalize_data(scan=None, log_=True)

    assert isinstance(
        axis_resource.normalize_data(scan=scan, log_=False), numpy.ndarray
    )
    assert isinstance(axis_resource.normalize_data(scan=scan, log_=True), numpy.ndarray)

    assert isinstance(axis_resource.normalized_data_paganin, numpy.ndarray)

    assert isinstance(str(axis_resource), str)
    axis_resource.data = None
    assert axis_resource is not None


def test_AxisCalculationInput():
    """test all class AxisCalculationInput which is a bit 'malformed'"""
    assert (
        AxisCalculationInput.from_value("transmission_withpag")
        is AxisCalculationInput.transmission_pag
    )
    assert (
        AxisCalculationInput.from_value("transmission_nopag")
        is AxisCalculationInput.transmission
    )
    assert (
        AxisCalculationInput.from_value("transmission")
        is AxisCalculationInput.transmission
    )
