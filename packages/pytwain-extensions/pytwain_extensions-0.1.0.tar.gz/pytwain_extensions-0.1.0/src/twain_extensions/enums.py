import enum


class FILE_FORMAT(enum.IntEnum):
    """Enumeration of file formats."""

    TIFF = 0
    PICT = 1
    BMP = 2
    XBM = 3
    JFIF = 4
    FPX = 5
    TIFFMULTI = 6
    PNG = 7
    SPIFF = 8
    EXIF = 9
    PDF = 10
    JP2 = 11
    JPX = 13
    DEJAVU = 14
    PDFA = 15
    PDFA2 = 16


class COMPRESSION_ALGORITHM(enum.IntEnum):
    """Enumeration of compression algorithms."""

    NONE = 0
    PACKBITS = 1
    GROUP31D = 2
    GROUP31DEOL = 3
    GROUP32D = 4
    GROUP4 = 5
    JPEG = 6
    LZW = 7
    JBIG = 8
    PNG = 9
    RLE4 = 10
    RLE8 = 11
    BITFIELDS = 12


class DATATYPE(enum.IntEnum):
    """Enumeration of TWAIN data types."""

    INT8 = 0
    INT16 = 1
    INT32 = 2
    UINT8 = 3
    UINT16 = 4
    UINT32 = 5
    BOOL = 6
    FIX32 = 7
    FRAME = 8
    STR32 = 9
    STR64 = 10
    STR128 = 11
    STR255 = 12
    STR1024 = 13
    UNI512 = 14


class LIGHTPATH(enum.IntEnum):
    """Enumeration of TWAIN light paths."""

    REFLECTIVE = 0
    TRANSMISSIVE = 1


class LIGHTSOURCE(enum.IntEnum):
    """Enumeration of TWAIN light sources."""

    RED = 0
    GREEN = 1
    BLUE = 2
    NONE = 3
    WHITE = 4
    CYAN = 5
    MAGENTA = 6
    YELLOW = 7
    BLACK = 8


class ORIENTATION(enum.IntEnum):
    """Enumeration of TWAIN orientation constants."""

    ROT0 = 0
    ROT90 = 1
    ROT180 = 2
    ROT270 = 3
    PORTRAIT = 1
    LANDSCAPE = 2
    AUTO = 4
    AUTOTEXT = 5
    AUTOPICTURE = 6


class OVERSCAN(enum.IntEnum):
    """
    Enumeration for ICAP_OVERSCAN capability modes.

    This enumeration defines the overscan settings used by TWAIN-compliant
    scanners to capture image areas beyond the normal frame boundaries.
    Overscan helps recover data lost due to skewing and supports image
    processing tasks such as deskewing and border removal.
    """

    NONE = 0
    AUTO = 1
    TOP_BOTTOM = 2
    LEFT_RIGHT = 3
    ALL = 4


class PIXELFLAVOR(enum.IntEnum):
    """
    Enumeration of TWAIN pixel flavor constants.

    TWAIN internal definition of polarity.
    Describes the polarity of grayscale or monochrome images — that is,
    whether darker areas are represented by higher or lower pixel values.
    It doesn't affect color images, only those that rely on intensity levels.

    Chocolate: Darker areas have higher pixel values (e.g., black = 255, white = 0).
    Vanilla: Darker areas have lower pixel values (e.g., black = 0, white = 255).
    """

    CHOCOLATE = 0
    VANILLA = 1


class PIXELTYPE(enum.IntEnum):
    """Enumeration of TWAIN pixel types."""

    BLACKWHITE = 0
    GRAY = 1
    RGB = 2
    PALETTE = 3
    CMY = 4
    CMYK = 5
    YUV = 6
    YUVK = 7
    CIEXYZ = 8
    LAB = 9
    SRGB = 10
    SCRGB = 11
    INFRARED = 16


class PLANARCHUNKY(enum.IntEnum):
    """
    Enumeration of TWAIN planar/chunky pixel storage formats.

    Allows the application and Source to identify which color data formats are available. There are
    two options, “planar” and “chunky.”
    For example, planar RGB data is transferred with the entire red plane of data first, followed by the
    entire green plane, followed by the entire blue plane (typical for three-pass scanners). “Chunky”
    mode repetitively interlaces a pixel from each plane until all the data is transferred (R-G-B-R-G-
    B…) (typical for one-pass scanners).
    """

    CHUNKY = 0
    PLANAR = 1


class FILTER(enum.IntEnum):
    """
    Describes the color characteristic of the subtractive filter applied to the image data.

    Multiple filters may be applied to a single acquisition.
    If the Source supports DAT_FILTER as well, then it will apply the filter set by the last SET
    operation invoked by the Application. Setting/Resetting ICAP_FILTER will clear the filter
    associated with DAT_FILTER. Setting/Resetting DAT_FILTER will clear the filter associated with
    ICAP_FILTER.
    """

    BLACK = 8
    BLUE = 2
    CYAN = 5
    GREEN = 1
    MAGENTA = 6
    NONE = 3
    RED = 0
    WHITE = 4
    YELLOW = 7
