"""utils for orange widget"""

from __future__ import annotations


class WidgetLongProcessing:
    """Class to display processing for some widgets with long processing"""

    def processing_state(self, working: bool, info=None) -> None:
        """

        :param working:
        :param info:
        """
        # default orange version don't have Processing.
        try:
            if working:
                self.Processing._add_general(
                    info or "processing", text=None, shown=True
                )
            else:
                try:
                    self.Processing.clear()
                except Exception:
                    pass
        except AttributeError:
            # in case we are on an orange version not having `Processing`
            pass

    def setDryRun(self, dry_run):
        pass

    def _startProcessing(self, *args, **kwargs):
        self.processing_state(working=True, info="processing")

    def _endProcessing(self, *args, **kwargs):
        self.processing_state(working=False, info="processing")
