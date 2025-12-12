import pytest

from tomwer.core.process.reconstruction.axis.params import AxisRP
from tomwer.core.process.reconstruction.darkref.params import DKRFRP
from tomwer.core.process.reconstruction.paramsbase import _get_db_fromstr, _ReconsParam


def test_paramsbase():
    """
    Test _ReconsParam class
    """
    params = _ReconsParam()
    assert isinstance(params.all_params, list)


def test_get_db_fromstr():
    """
    test '_get_db_fromstr' function
    """
    assert _get_db_fromstr(vals="12") == 12.0
    assert _get_db_fromstr(vals="12.0") == 12.0
    assert _get_db_fromstr(vals="(12.0, )") == 12.0
    assert _get_db_fromstr(vals="(12.0, 13.5)") == (12.0, 13.5)
    assert _get_db_fromstr(vals="[12.0, 13.5]") == (12.0, 13.5)


def test_basic_DKRFRP():
    """
    dummy test for DKRFRP
    """
    recons_params = DKRFRP()
    ddict = recons_params.to_dict()
    DKRFRP.from_dict(ddict)
    assert isinstance(
        recons_params.to_unique_recons_set(),
        tuple,
    )


@pytest.mark.parametrize("param_klass", [DKRFRP, AxisRP])
def test_ReconsParams_from_dict(param_klass):
    """
    Test from_dict with upper and lower case keys
    """
    ref_dict = param_klass().to_dict()

    # Default case (upper)
    result = param_klass.from_dict(ref_dict.copy())
    assert result.to_dict() == ref_dict

    # Lower case
    lower_dict = {key.lower(): value for key, value in ref_dict.items()}
    result = param_klass.from_dict(lower_dict.copy())
    assert result.to_dict() == ref_dict
