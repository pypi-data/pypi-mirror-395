# Copier Pydantic

[![pypi version](https://img.shields.io/pypi/v/copier-pydantic.svg)](https://pypi.org/project/copier-pydantic/)

Jinja2 extensions for Copier that enable using Pydantic Models for validation and within templates

## Installation

With pip:

```bash
pip install copier-pydantic
```

With uv:

```bash
uv tool install copier --with copier-pydantic
```

With pipx:

```bash
pipx install copier
pipx inject copier copier-pydantic
```

## Usage with Copier

In your copier template configuration:

```yaml
# Add the jinja extensions
_jinja_extensions:
  - copier_pydantic.MultilineValidation
  - copier_pydantic.PydanticExtension

# and exclude the model.py file from your template
_exclude:
  - models.py
# or use the best practice of having the template in a sub directory
_subdirectory: template
```

So your template will look something like this

```
📁 template_root
├── 📄 models.py
├── 📄 copier.yml
└── 📁 template
    ├── 📄 {{_copier_conf.answers_file}}.jinja
    └── 📄 ...
```

With `models.py` containing your Pydantic `BaseModel`'s like this

```python
from pydantic import BaseModel

class DatabaseConfig(BaseModel):
    db_host: str
    db_port: int
```

you can then use your model to validate the question input like this

```yaml
validated_example:
  type: yaml
  multiline: true
  default: |
    db_host: 'localhost'
    db_port: 5432
  validator: "{{ validated_example | validate_as(DatabaseConfig) }}"
```
