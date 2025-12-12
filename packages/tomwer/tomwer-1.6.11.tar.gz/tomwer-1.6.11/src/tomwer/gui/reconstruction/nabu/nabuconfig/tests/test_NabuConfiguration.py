from __future__ import annotations

from tomwer.tests.conftest import qtapp  # noqa F401
from tomwer.gui.reconstruction.nabu.nabuconfig.nabuconfig import (
    NabuConfiguration,
)
from nabu.pipeline.config import _extract_nabuconfig_keyvals
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)


def test_NabuConfiguration(
    qtapp,  # noqa F811
):
    """Test that the 'NabuConfiguration' produce only keys understandable by nabu"""
    widget = NabuConfiguration(parent=None)

    tomwer_config = widget.getConfiguration()
    nabu_config = _extract_nabuconfig_keyvals(nabu_fullfield_default_config)

    tomwer_section_keys = set(tomwer_config.keys())
    nabu_section_keys = set(nabu_config.keys())
    tomwer_section_keys.remove("tomwer_slices")
    assert tomwer_section_keys.issubset(
        nabu_section_keys
    ), f"tomwer provide sections undefined by nabu: {tomwer_section_keys - nabu_section_keys}"

    for section_key in nabu_config.keys():
        if section_key in tomwer_config:
            nabu_sub_section_keys = set(nabu_config[section_key].keys())
            tomwer_sub_section_keys = set(tomwer_config[section_key].keys())
            if section_key == "phase":
                # this key is pop by tomwer before calling nabu. It is used internally only
                tomwer_sub_section_keys.remove("beam_shape")
            elif section_key == "reconstruction":
                tomwer_sub_section_keys.remove("slice_plane")
            elif section_key == "output":
                tomwer_sub_section_keys.remove("output_dir_mode")
            assert tomwer_sub_section_keys.issubset(
                nabu_sub_section_keys
            ), f"tomwer provides keys undefined by nabu: {tomwer_sub_section_keys - nabu_sub_section_keys}"
