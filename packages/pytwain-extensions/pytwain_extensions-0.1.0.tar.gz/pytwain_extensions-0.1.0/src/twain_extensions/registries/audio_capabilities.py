# ruff: noqa: E501
"""
The audio capabilities registry holds all the TWAIN audio capabilities (ACAP_*).

TWAIN:
ACAP_xxxx: Capabilities whose names begin with ACAP are capabilities that apply to
devices that support audio. The “A” stands for audio.
"""

from .capability import Capability

AUDIO_CAP_REGISTRY: dict[int, Capability] = {
    0x1201: Capability(
        id=0x1201,
        name="file_format",
        twain_type="None",
        doc="This is not really a capability but a enum, but as it was named by TWAIN as ACAP_FILEFORMAT, it is included here for completeness.",
        version="None",
        allowed_values="None",
        containers=[],
    ),
    0x1202: Capability(
        id=0x1202,
        name="xfer_mech",
        twain_type="TW_UINT16",
        doc="""Description:
Allows the Application and Source to identify which audio transfer mechanisms they have in common.

Application:
The current setting of ACAP_XFERMECH must match the constant used by the application to specify the audio transfer mechanism when starting the transfer using the triplet: DG_AUDIO / DAT_AUDIOxxxxXFER / MSG_GET.""",
        version="1.8",
        allowed_values=["TWSX_NATIVE", "TWSX_FILE"],
        containers=["TW_ENUMERATION", "TW_ONEVALUE"],
    ),
}
