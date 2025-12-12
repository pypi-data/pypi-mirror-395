from tomwer.core.utils.deprecation import deprecated_warning

deprecated_warning(
    "module",
    name="tomwer.app.darkref",
    reason="Has been moved",
    replacement="tomwer.app.reducedarkflat",
    only_once=True,
)
from tomwer.app.reducedarkflat import *  # noqa F401
