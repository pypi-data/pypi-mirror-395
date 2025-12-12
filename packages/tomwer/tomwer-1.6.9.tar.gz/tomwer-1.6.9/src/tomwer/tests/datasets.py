import os
from tomoscan.tests.datasets import GitlabProject

TomwerCIDatasets = GitlabProject(
    branch_name="tomwer",
    host="https://gitlab.esrf.fr",
    cache_dir=os.path.join(
        os.path.dirname(__file__),
        "__archive__",
    ),
    token=None,
    project_id=4299,  # https://gitlab.esrf.fr/tomotools/ci_datasets
)
