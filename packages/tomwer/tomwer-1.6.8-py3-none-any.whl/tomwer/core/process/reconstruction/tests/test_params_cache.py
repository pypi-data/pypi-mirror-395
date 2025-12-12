import os
from tomwer.core.process.reconstruction.params_cache import (
    _CACHE,
    _CACHE_SIZE,
    save_reconstruction_parameters_to_cache,
    clear_reconstruction_parameters_cache,
)
from tomwer.core.utils.scanutils import MockNXtomo


def test_cache(tmp_path):
    nxtomos = [
        MockNXtomo(
            scan_path=os.path.join(tmp_path, f"my_nxtomo_{i_scan}"),
            n_proj=10,
        ).scan
        for i_scan in range(31)
    ]
    new_nxtomo = MockNXtomo(
        scan_path=os.path.join(tmp_path, "my_nxtomo_99"),
        n_proj=10,
    ).scan

    clear_reconstruction_parameters_cache()
    # test saving it in the original order
    [save_reconstruction_parameters_to_cache(scan=scan) for scan in nxtomos]
    assert len(_CACHE) == _CACHE_SIZE
    assert _CACHE == {
        nxtomo.get_identifier().to_str(): (None, None) for nxtomo in nxtomos[1:]
    }

    # try updating the next last one to make sure it won't be removed
    save_reconstruction_parameters_to_cache(scan=nxtomos[1])
    save_reconstruction_parameters_to_cache(scan=new_nxtomo)
    assert nxtomos[1].get_identifier().to_str() in _CACHE
    assert nxtomos[2].get_identifier().to_str() not in _CACHE
    clear_reconstruction_parameters_cache()
