import pathlib
import typing
import twain

from twain_extensions.registries import GENERAL_CAP_REGISTRY, IMAGE_CAP_REGISTRY, AUDIO_CAP_REGISTRY
from twain_extensions.enums import DATATYPE
from twain_extensions.registries.capability import Capability

from .template import TemplateField, render_model_config


def get_python_type(twain_type_id: int) -> type:
    """Map TWAIN type constants to Python type strings."""
    match twain_type_id:
        case DATATYPE.INT8 | DATATYPE.INT16 | DATATYPE.INT32 | DATATYPE.UINT8 | DATATYPE.UINT16 | DATATYPE.UINT32:
            return int
        case DATATYPE.BOOL:
            return bool
        case DATATYPE.FIX32:
            return float
        case DATATYPE.STR32 | DATATYPE.STR64 | DATATYPE.STR128 | DATATYPE.STR255 | DATATYPE.STR1024 | DATATYPE.UNI512:
            return str
        case DATATYPE.FRAME:
            return tuple[float, float, float, float]
        case _:
            return typing.Any  # type: ignore


def sanitize_twain_value(val: typing.Any) -> typing.Any:  # noqa: ANN401
    """Recursively converts ctypes objects (returned by pytwain for custom string caps) into standard Python types."""
    if val is None:
        return None

    if isinstance(val, list):
        return [sanitize_twain_value(v) for v in val]

    if hasattr(val, "value") and isinstance(val.value, bytes):
        try:
            return val.value.decode("utf-8", errors="replace").strip("\x00")
        except Exception:  # noqa: BLE001
            return str(val)

    if isinstance(val, bytes):
        try:
            return val.decode("utf-8", errors="replace").strip("\x00")
        except Exception:  # noqa: BLE001
            pass

    return val


def generate_scanner_model(
    device_name: str, source: twain.Source, output_file: pathlib.Path, try_all_caps: bool = False
) -> None:
    """
    Generate a pydantic model for the capabilities (available settings) of the source provided.

    Args:
      device_name: Only for naming the generated class.
      source: The source from which to extract capabilities.
      output_file: The file path where the generated model will be saved.
      try_all_caps: If True, attempts to query ALL capabilities in the local registry
        even if the scanner does not explicitly report them in CAP_SUPPORTEDCAPS.
    """
    fields_data = []

    all_caps: dict[int, Capability] = {**GENERAL_CAP_REGISTRY, **IMAGE_CAP_REGISTRY, **AUDIO_CAP_REGISTRY}

    CAP_SUPPORTEDCAPS = 0x1005
    capability_ids = set()

    try:
        cap_support_data = source.get_capability(CAP_SUPPORTEDCAPS)
        if isinstance(cap_support_data, tuple) and len(cap_support_data) == 2:
            _, payload = cap_support_data
            if isinstance(payload, list):
                capability_ids = set(payload)
            if try_all_caps:
                capability_ids.update(all_caps.keys())

    except ValueError as e:
        print(f"Warning: Could not query CAP_SUPPORTEDCAPS. {e}")  # noqa: T201
        print("Falling back to full local registry.")  # noqa: T201
        capability_ids = set(all_caps.keys())

    sorted_cap_ids = sorted(capability_ids)

    for cap_id in sorted_cap_ids:
        try:
            cap_data = source.get_capability(cap_id)
        except (ValueError, twain.exceptions.CapabilityFormatNotSupported, twain.exceptions.CapUnsupported):
            continue

        spec = all_caps.get(cap_id)

        tmp_field_info = {
            "name": spec.name if spec else f"cap_{hex(cap_id)}",
            "cap_id": cap_id,
            "py_type": typing.Any,
            "twain_type_id": 0,
            "current_value": None,
            "default_value": None,
            "options": None,
            "min": None,
            "max": None,
            "step": None,
            "doc": spec.doc if spec else "Extended/Custom Capability found on device Not listed in registry.",
        }

        # --- CASE 1: TWON_RANGE (Returns Dict) ---
        if isinstance(cap_data, dict):
            curr = sanitize_twain_value(cap_data.get("CurrentValue"))

            is_float = isinstance(curr, float)
            tmp_field_info["py_type"] = float if is_float else int

            if spec:
                tmp_field_info["twain_type_id"] = DATATYPE[spec.twain_type.strip("TW_")].value
            else:
                tmp_field_info["twain_type_id"] = DATATYPE.FIX32.value if is_float else DATATYPE.INT32.value

            tmp_field_info["current_value"] = cap_data.get("CurrentValue")
            tmp_field_info["default_value"] = cap_data.get("DefaultValue")
            tmp_field_info["min"] = cap_data.get("MinValue")
            tmp_field_info["max"] = cap_data.get("MaxValue")
            tmp_field_info["step"] = cap_data.get("StepSize")

        # --- CASE 2: Tuple Returns (ONEVALUE, ENUM, ARRAY) ---
        elif isinstance(cap_data, tuple) and len(cap_data) == 2:
            t_type, payload = cap_data

            tmp_field_info["twain_type_id"] = t_type
            tmp_field_info["py_type"] = get_python_type(t_type)

            # Case 2A: TWON_ENUMERATION
            if isinstance(payload, tuple) and len(payload) == 3 and isinstance(payload[2], list):
                curr_idx, def_idx, raw_values = payload

                values = sanitize_twain_value(raw_values)

                current_val = values[curr_idx] if 0 <= curr_idx < len(values) else None
                default_val = values[def_idx] if 0 <= def_idx < len(values) else None

                tmp_field_info["current_value"] = current_val
                tmp_field_info["default_value"] = default_val
                tmp_field_info["options"] = values

            # Case 2B: TWON_ARRAY
            elif isinstance(payload, list):
                sanitized_payload = sanitize_twain_value(payload)

                ttype = tmp_field_info["py_type"]
                tmp_field_info["py_type"] = list[ttype]
                tmp_field_info["current_value"] = sanitized_payload

                if sanitized_payload:
                    tmp_field_info["py_type"] = list[type(sanitized_payload[0])]
                else:
                    tmp_field_info["py_type"] = list

            # Case 2C: TWON_ONEVALUE
            else:
                tmp_field_info["current_value"] = sanitize_twain_value(payload)

        if isinstance(tmp_field_info["current_value"], str):
            tmp_field_info["py_type"] = str
            tmp_field_info["current_value"] = repr(tmp_field_info["current_value"])

        field_info = TemplateField[tmp_field_info["py_type"]](
            name=tmp_field_info["name"],
            py_type=tmp_field_info["py_type"],
            default=tmp_field_info["default_value"],
            doc=tmp_field_info["doc"],
            twain_id=cap_id,
            twain_type=tmp_field_info["twain_type_id"],
            min=tmp_field_info["min"],
            max=tmp_field_info["max"],
            current_value=tmp_field_info["current_value"],
            default_value=tmp_field_info["default_value"],
            step=tmp_field_info["step"],
        )

        fields_data.append(field_info)

    render_model_config(device_name=device_name, fields=fields_data, output_file=output_file)
