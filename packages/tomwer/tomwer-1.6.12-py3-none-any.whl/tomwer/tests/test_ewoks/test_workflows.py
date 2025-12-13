# coding: utf-8
from __future__ import annotations


import os
import tempfile
from glob import glob

from ewoks import execute_graph
from ewokscore.graph import analysis, load_graph
from ewokscore.graph.validate import validate_graph

from tomwer.core.utils.scanutils import HDF5MockContext
from tomwer.core.process.reconstruction.output import (
    PROCESS_FOLDER_RECONSTRUCTED_VOLUMES,
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


def test_simple_workflow_nabu():
    """Test the workflow: darkref -> axis -> nabu slices -> nabu volume"""

    with HDF5MockContext(
        scan_path=os.path.join(tempfile.mkdtemp(), "scan_test"), n_proj=100
    ) as scan:
        # insure no cfg yet
        assert len(glob(os.path.join(scan.path, "*.cfg"))) == 0

        graph = load_graph(
            source={
                "nodes": [
                    {
                        "id": "darkref",
                        "task_type": "class",
                        "task_identifier": "tomwer.core.process.reconstruction.darkref.darkrefs.DarkRefs",
                    },
                    {
                        "id": "axis",
                        "task_type": "class",
                        "task_identifier": "tomwer.core.process.reconstruction.axis.axis.AxisTask",
                        "default_inputs": [
                            {
                                "name": "axis_params",
                                "value": {
                                    "MODE": "manual",
                                    "POSITION_VALUE": 0.2,
                                },
                            },
                        ],
                    },
                    {
                        "id": "nabu slices",
                        "task_type": "class",
                        "task_identifier": "tomwer.core.process.reconstruction.nabu.nabuslices.NabuSlices",
                        "dry_run": True,  # as this is a mock dataset avoid to reconstruct it and only check for the .cfg file created
                        "default_inputs": [
                            {
                                "name": "nabu_params",
                                "value": {"tomwer_slices": 2},
                            }
                        ],
                    },
                    {
                        "id": "nabu volume",
                        "task_type": "class",
                        "task_identifier": "tomwer.core.process.reconstruction.nabu.nabuvolume.NabuVolume",
                        "dry_run": True,
                        "default_inputs": [
                            {
                                "name": "dry_run",
                                "value": True,
                            }
                        ],
                    },
                ],
                "links": [
                    {
                        "source": "darkref",
                        "target": "axis",
                        "map_all_data": True,
                    },
                    {
                        "source": "axis",
                        "target": "nabu slices",
                        "data_mapping": [  # same as all arguments but just here to test both
                            {
                                "source_output": "data",
                                "target_input": "data",
                            },
                        ],
                    },
                    {
                        "source": "nabu slices",
                        "target": "nabu volume",
                        "map_all_data": True,
                    },
                ],
            }
        )
        assert graph.is_cyclic is False, "graph is expected to be acyclic"
        assert analysis.start_nodes(graph=graph.graph) == {
            "darkref"
        }, "start node should be a single task `darkref`"
        validate_graph(graph.graph)
        result = execute_graph(
            graph,
            inputs=[
                {"id": "darkref", "name": "data", "value": scan},
            ],
        )
        assert analysis.end_nodes(graph=graph.graph) == {
            "nabu volume"
        }, "should only have one result nodes"
        assert "data" in result, f"cannot find `nabu volume` in {result}"
        assert os.path.exists(
            os.path.join(
                scan.path, PROCESS_FOLDER_RECONSTRUCTED_VOLUMES, "nabu_cfg_files"
            )
        ), "nabu has not been executed (even in dry mode)"
