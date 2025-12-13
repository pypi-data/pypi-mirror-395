import enum
import typing


class Capability(typing.NamedTuple):
    """
    Represents a TWAIN capability specification.

    Args:
      id: The numeric ID as defined in the TWAIN specifications.
      name: The Pythonic name for the capability.
      tw_type: The TWAIN wire type (e.g., 'TW_FIX32', 'TW_BOOL').
      doc: A combined description and application note from the spec.
      version: The TWAIN version in which this capability was introduced.
      allowed_values: Defines the allowed values for this capability (not standardized).
      containers: A list of supported MSG_GET containers (e.g., 'TW_ONEVALUE', 'TW_RANGE').
    """

    id: int
    name: str
    twain_type: str
    doc: str
    version: str
    allowed_values: typing.Any
    containers: list[str]


class CapabilityTypes(enum.Enum):
    """The three different types of TWAIN capabilities & their prefixes."""

    GENERAL = "CAP_"
    IMAGE = "ICAP_"
    AUDIO = "ACAP_"


def to_twain_name(capability_name: str, capability_type: CapabilityTypes) -> str:
    """
    Convert a Pythonic capability name to its corresponding TWAIN name.

    Args:
      capability_name: The Pythonic name of the capability (e.g., 'brightness').
      capability_type: The type of capability ('general', 'image', or 'audio').

    Returns:
      The TWAIN name of the capability (e.g., 'CAP_BRIGHTNESS', 'ICAP_BRIGHTNESS', 'ACAP_BRIGHTNESS').
    """
    return capability_type.value + capability_name.upper().replace("_", "")
