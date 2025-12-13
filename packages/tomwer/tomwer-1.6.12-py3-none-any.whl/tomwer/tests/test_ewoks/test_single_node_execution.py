# coding: utf-8
from __future__ import annotations


import os
import tempfile
from glob import glob

import pytest
from ewokscore.graph import analysis, load_graph
from ewokscore.graph.validate import validate_graph

from tomwer.core.utils.scanutils import HDF5MockContext
from nabu.pipeline.config import get_default_nabu_config
from nabu.pipeline.fullfield.nabu_config import (
    nabu_config as nabu_fullfield_default_config,
)

try:
    from nabu.pipeline.fullfield.reconstruction import (  # noqa F401
        FullFieldReconstructor,
    )
except ImportError:
    try:
        from nabu.pipeline.fullfield.local_reconstruction import (  # noqa F401
            ChunkedReconstructor,
        )
    except ImportError:
        has_nabu = False
    else:
        has_nabu = True
else:
    has_nabu = True

pytest.mark.skipif(condition=not has_nabu, reason="nabu not installed")


classes_to_test = {
    "darkref": "tomwer.core.process.reconstruction.darkref.darkrefs.DarkRefs",
    "axis": "tomwer.core.process.reconstruction.axis.axis.AxisTask",
    "nabu slices": "tomwer.core.process.reconstruction.nabu.nabuslices.NabuSlices",
}


@pytest.mark.parametrize("node_name, node_qual_name", classes_to_test.items())
def test_single_class_instanciation(node_name, node_qual_name):
    with HDF5MockContext(
        scan_path=os.path.join(tempfile.mkdtemp(), "scan_test"), n_proj=100
    ) as scan:
        # insure no cfg yet
        assert len(glob(os.path.join(scan.path, "*.cfg"))) == 0

        graph = load_graph(
            {
                "nodes": [
                    {
                        "id": node_name,
                        "task_type": "class",
                        "task_identifier": node_qual_name,
                        "default_inputs": [
                            {
                                "name": "data",
                                "value": scan,
                            },
                            {
                                "name": "nabu_params",
                                "value": get_default_nabu_config(
                                    nabu_fullfield_default_config
                                ),
                            },
                        ],
                    },
                ]
            }
        )

        assert graph.is_cyclic is False, "graph is expected to be acyclic"
        assert analysis.start_nodes(graph.graph) == {
            node_name
        }, "graph is expected to have only on start nodes"
        validate_graph(graph.graph)
        result = graph.execute(varinfo=None)

        assert analysis.end_nodes(graph.graph) == {
            node_name
        }, "graph is expected to have only one end node"
        assert "data" in result, "data is expected to be part of the output_values"
