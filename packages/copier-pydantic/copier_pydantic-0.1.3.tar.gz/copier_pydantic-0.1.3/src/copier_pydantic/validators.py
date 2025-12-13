"""Pydantic model integration helpers."""

import importlib.util
import inspect
import sys
from typing import Any

from jinja2 import Environment
from jinja2.ext import Extension
from pydantic import BaseModel, RootModel, ValidationError


def _to_model(value: Any, model: type[BaseModel], **kwargs: dict) -> BaseModel:
    """Jinja filter for instantiating model instance.

    `{{ value | to_model(Example) }}`
    """
    return model.model_validate(value, strict=True, **kwargs)


def _to_model_dict(value: Any, model: type[BaseModel], **kwargs: dict) -> dict:
    """Jinja filter for instantiating model instance as dictionary.

    `{{ value | to_model_dict(Example) }}`

    Useful if you want simpler usage in jinja, but supports default values etc
    """
    return model.model_validate(value, strict=True, **kwargs).model_dump()


def _validate_as(value: Any, model: type[BaseModel]) -> str:
    """Jinja filter for model validation string in copier.yml.

    ```
    input:
      type: yaml
      multiline: true
      validator: {{ input | validate_as(Example) }}
    ```
    """
    try:
        model.model_validate(value, strict=True)
    except ValidationError as err:
        return str(err)
    return ''


def _is_valid_as(model: type[BaseModel]) -> callable:
    """Construct jinja test for compatibility with model."""

    def test(value: dict) -> bool:
        try:
            model.model_validate(value, strict=True)
        except ValidationError:
            return False
        return True

    return test


def _is_model_instance_test(model: type[BaseModel]) -> callable:
    """Construct jinja test for model instance."""

    def test(value: Any) -> bool:
        return isinstance(value, model)

    return test


# Source: https://stackoverflow.com/questions/5362771/how-to-load-a-module-from-code-in-a-string
def _import_module_from_string(name: str, source: str) -> None:
    """Import module from source string.

    Example use:
    import_module_from_string("m", "f = lambda: print('hello')")
    m.f()
    """
    spec = importlib.util.spec_from_loader(name, loader=None)
    module = importlib.util.module_from_spec(spec)
    exec(source, module.__dict__)  # noqa: S102
    sys.modules[name] = module
    globals()[name] = module


def _is_pydantic_model(obj: Any) -> bool:
    """Check if pydantic model itself (not instance)."""
    return (
        inspect.isclass(obj)
        and issubclass(obj, BaseModel)
        and obj not in (BaseModel, RootModel)
    )


class PydanticExtension(Extension):
    """Adds Pydantic models and helpers."""

    def __init__(self, environment: Environment) -> None:
        """Implement extension logic."""
        super().__init__(environment)

        self._load_models()

        # Enable lookup via alias
        environment.globals['models'] = self.models

        for model in self.models.values():
            # Add models to namespace for use with generic functions
            environment.globals[model.__name__] = model

            # Add generic functions
            # `{{ input | to_model(Example) }}` e.g. for default values
            environment.filters['to_model'] = _to_model
            # `{{ input | to_model_dict(Example) }}` e.g. for default values
            environment.filters['to_model_dict'] = _to_model_dict
            # `validator: {{ input | validate_as(Example) }}`
            environment.filters['validate_as'] = _validate_as

            # Pre-create other helpers
            # `{% if input is Example %}`
            environment.tests[f'{model.__name__}'] = _is_valid_as(model)
            # `{% if input is Example_Model %}`
            environment.tests[f'{model.__name__}_Model'] = _is_model_instance_test(
                model,
            )

    def _load_models(self) -> None:
        models_code, *_ = self.environment.loader.get_source(
            self.environment,
            'models.py',
        )
        _import_module_from_string('models_module', models_code)
        self.models = dict(inspect.getmembers(models_module, _is_pydantic_model))  # noqa: F821
