import dataclasses


@dataclasses.dataclass
class Frame:
    """
    Represents a TWAIN scanning frame region in image layout coordinates.

    The Frame defines the rectangular area of the image to acquire, expressed in
    the same units as `ICAP_UNITS`.

    A sketch of the Frame coordinate system is shown below.

    Attributes:
      left (float): Distance from the origin of the scanner to the left edge
        of the frame.
      top (float): Distance from the origin of the scanner to the top edge
        of the frame.
      right (float): Distance from the origin of the scanner to the right
        edge of the frame.
      bottom (float): Distance from the origin of the scanner to the bottom
        edge of the frame.

    +--------------------------------------------------------------+
    | ↖                                                            |
    | Origin of Scanner                    ↑         ↑             |
    |   +----------------------------------|---------|-------+     |
    |   | ↖                                |         |       |     |
    |   | Origin of Page              Top  |         |       |     |
    |   |                                  |         |       |     |
    |   |                                  |         |       |     |
    |   |                                  ↓         |       |     |
    |<--|------- Left ------->+-------------------+  |Bottom |     |
    |   |                     |                   |  |       |     |
    |   |                     |   Acquired Image  |  |       |     |
    |   |                     |                   |  |       |     |
    |   |                     +-------------------+  ↓       |     |
    |<--|------------------ Right ---------------->          |     |
    |   |                                                    |     |
    |   |                                                    |     |
    |   |                                                    |     |
    |   +----------------------------------------------------+     |
    |                                                              |
    |                                                              |
    |                                                              |
    |                                                              |
    |                                                              |
    |                                                              |
    |                                                              |
    |                                                              |
    |                                                              |
    +--------------------------------------------------------------+
    """

    left: float
    top: float
    right: float
    bottom: float
