"""Enable multiline validation messages with Copier."""

import prompt_toolkit
from jinja2 import Environment
from jinja2.ext import Extension

_validation_toolbar_init = prompt_toolkit.widgets.ValidationToolbar.__init__


def _validation_toolbar_init_patched(
    self: prompt_toolkit.widgets.ValidationToolbar,
    *args: tuple,
    **kwargs: dict,
) -> None:
    """Wrap ValidationToolbar __init__ for patching."""
    _validation_toolbar_init(self, *args, **kwargs)

    # Uncap validation message length to enable multiline error messages
    self.container.content.height = None


class MultilineValidation(Extension):
    """Enable multiline error messages for Copier by loading."""

    def __init__(self, environment: Environment) -> None:
        """Implement extension logic."""
        super().__init__(environment)

        prompt_toolkit.widgets.ValidationToolbar.__init__ = (
            _validation_toolbar_init_patched
        )
