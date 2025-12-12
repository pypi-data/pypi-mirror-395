from tomwer.core.utils.deprecation import deprecated_warning

deprecated_warning(
    "module",
    name="tomwer.app.darkrefpatch",
    reason="Has been moved",
    replacement="tomwer.app.patchrawdarkflat",
    only_once=True,
)
from tomwer.app.patchrawdarkflat import *  # noqa F401
