import dataclasses
import pathlib
import typing
from jinja2 import Template
import datetime

TEMPLATE = """
from pydantic import BaseModel, Field

class {{ class_name }}(BaseModel):
    \"\"\"
    Auto-generated configuration for {{ device_name }}.
    Generated on: {{ date }}
    \"\"\"

    {% for field in fields %}
    # TWAIN ID: {{ "0x%04X"|format(field.twain_id) }}
    {{ field.name }}: {{ field.py_type_str }} = Field(
        default={{ field.default_value }},
        description=\"\"\"{{ field.doc }}\"\"\",
        {% if field.min is not none %}ge={{ field.min }},{% endif %}
        {% if field.max is not none %}le={{ field.max }},{% endif %}
        {% if field.step is not none %}multiple_of={{ field.step }},{% endif %}
        json_schema_extra={
            "twain_id": {{ field.twain_id }},
            "twain_type": {{ field.twain_type }},
            "current": {{ field.current_value }},
        }
    )
    {% endfor %}
"""

T = typing.TypeVar("T")


@dataclasses.dataclass
class TemplateField(typing.Generic[T]):
    """
    TemplateField represents a field in the template with type information and constraints.

    Args:
      name: The name of the field.
      py_type: The Python type of the field.
      default: The default value for the field.
      doc: Documentation string for the field.
      twain_id: The TWAIN identifier for the field.
      twain_type: The TWAIN data type for the field.
      min: Minimum constraint for the field, if applicable.
      max: Maximum constraint for the field, if applicable.
    """

    name: str
    py_type: type[T]
    default: T
    doc: str
    twain_id: int
    twain_type: int
    min: T | None = None
    max: T | None = None
    current_value: T | None = None
    default_value: T | None = None
    step: T | None = None

    @property
    def py_type_str(self) -> str:
        """Returns the string representation of the type for code generation."""
        if self.py_type is typing.Any:
            return "typing.Any"

        if isinstance(self.py_type, type):
            return self.py_type.__name__

        return str(self.py_type)


def render_model_config(device_name: str, fields: list[TemplateField], output_file: pathlib.Path) -> None:
    """
    Render a configuration model for a given scanning device.

    Args:
      device_name: the name of the device for which to generate the config.
      fields: A list of capabilities supported by the device to include in the model.
      output_file: The file path where the rendered model configuration will be saved.
    """
    t = Template(TEMPLATE)
    class_name = device_name.replace(" ", "") + "Config"
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    code = t.render(class_name=class_name, device_name=device_name, date=date, fields=fields)

    with output_file.open("w") as f:
        f.write(code)
