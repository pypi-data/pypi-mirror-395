"""The namespace contains Tiff file format enumerations."""
from typing import List, Optional, Dict, Iterable, Any, overload
import enum
import io
import collections.abc
from collections.abc import Sequence
from datetime import datetime, timedelta
from aspose.pyreflection import Type
import aspose.pycore
import aspose.pydrawing
from uuid import UUID
import aspose.imaging
import aspose.imaging.apsbuilder
import aspose.imaging.apsbuilder.dib
import aspose.imaging.asynctask
import aspose.imaging.brushes
import aspose.imaging.dithering
import aspose.imaging.exif
import aspose.imaging.exif.enums
import aspose.imaging.extensions
import aspose.imaging.fileformats
import aspose.imaging.fileformats.apng
import aspose.imaging.fileformats.avif
import aspose.imaging.fileformats.bigtiff
import aspose.imaging.fileformats.bmp
import aspose.imaging.fileformats.bmp.structures
import aspose.imaging.fileformats.cdr
import aspose.imaging.fileformats.cdr.const
import aspose.imaging.fileformats.cdr.enum
import aspose.imaging.fileformats.cdr.objects
import aspose.imaging.fileformats.cdr.types
import aspose.imaging.fileformats.cmx
import aspose.imaging.fileformats.cmx.objectmodel
import aspose.imaging.fileformats.cmx.objectmodel.enums
import aspose.imaging.fileformats.cmx.objectmodel.specs
import aspose.imaging.fileformats.cmx.objectmodel.styles
import aspose.imaging.fileformats.core
import aspose.imaging.fileformats.core.vectorpaths
import aspose.imaging.fileformats.dicom
import aspose.imaging.fileformats.djvu
import aspose.imaging.fileformats.dng
import aspose.imaging.fileformats.dng.decoder
import aspose.imaging.fileformats.emf
import aspose.imaging.fileformats.emf.dtyp
import aspose.imaging.fileformats.emf.dtyp.commondatastructures
import aspose.imaging.fileformats.emf.emf
import aspose.imaging.fileformats.emf.emf.consts
import aspose.imaging.fileformats.emf.emf.objects
import aspose.imaging.fileformats.emf.emf.records
import aspose.imaging.fileformats.emf.emfplus
import aspose.imaging.fileformats.emf.emfplus.consts
import aspose.imaging.fileformats.emf.emfplus.objects
import aspose.imaging.fileformats.emf.emfplus.records
import aspose.imaging.fileformats.emf.emfspool
import aspose.imaging.fileformats.emf.emfspool.records
import aspose.imaging.fileformats.emf.graphics
import aspose.imaging.fileformats.eps
import aspose.imaging.fileformats.eps.consts
import aspose.imaging.fileformats.gif
import aspose.imaging.fileformats.gif.blocks
import aspose.imaging.fileformats.ico
import aspose.imaging.fileformats.jpeg
import aspose.imaging.fileformats.jpeg2000
import aspose.imaging.fileformats.opendocument
import aspose.imaging.fileformats.opendocument.enums
import aspose.imaging.fileformats.opendocument.objects
import aspose.imaging.fileformats.opendocument.objects.brush
import aspose.imaging.fileformats.opendocument.objects.font
import aspose.imaging.fileformats.opendocument.objects.graphic
import aspose.imaging.fileformats.opendocument.objects.pen
import aspose.imaging.fileformats.pdf
import aspose.imaging.fileformats.png
import aspose.imaging.fileformats.psd
import aspose.imaging.fileformats.svg
import aspose.imaging.fileformats.svg.graphics
import aspose.imaging.fileformats.tga
import aspose.imaging.fileformats.tiff
import aspose.imaging.fileformats.tiff.enums
import aspose.imaging.fileformats.tiff.filemanagement
import aspose.imaging.fileformats.tiff.filemanagement.bigtiff
import aspose.imaging.fileformats.tiff.instancefactory
import aspose.imaging.fileformats.tiff.pathresources
import aspose.imaging.fileformats.tiff.tifftagtypes
import aspose.imaging.fileformats.webp
import aspose.imaging.fileformats.wmf
import aspose.imaging.fileformats.wmf.consts
import aspose.imaging.fileformats.wmf.graphics
import aspose.imaging.fileformats.wmf.objects
import aspose.imaging.fileformats.wmf.objects.escaperecords
import aspose.imaging.imagefilters
import aspose.imaging.imagefilters.complexutils
import aspose.imaging.imagefilters.convolution
import aspose.imaging.imagefilters.filteroptions
import aspose.imaging.imageloadoptions
import aspose.imaging.imageoptions
import aspose.imaging.interfaces
import aspose.imaging.magicwand
import aspose.imaging.magicwand.imagemasks
import aspose.imaging.masking
import aspose.imaging.masking.options
import aspose.imaging.masking.result
import aspose.imaging.memorymanagement
import aspose.imaging.metadata
import aspose.imaging.multithreading
import aspose.imaging.palettehelper
import aspose.imaging.progressmanagement
import aspose.imaging.shapes
import aspose.imaging.shapesegments
import aspose.imaging.sources
import aspose.imaging.watermark
import aspose.imaging.watermark.options
import aspose.imaging.xmp
import aspose.imaging.xmp.schemas
import aspose.imaging.xmp.schemas.dicom
import aspose.imaging.xmp.schemas.dublincore
import aspose.imaging.xmp.schemas.pdf
import aspose.imaging.xmp.schemas.photoshop
import aspose.imaging.xmp.schemas.xmpbaseschema
import aspose.imaging.xmp.schemas.xmpdm
import aspose.imaging.xmp.schemas.xmpmm
import aspose.imaging.xmp.schemas.xmprm
import aspose.imaging.xmp.types
import aspose.imaging.xmp.types.basic
import aspose.imaging.xmp.types.complex
import aspose.imaging.xmp.types.complex.colorant
import aspose.imaging.xmp.types.complex.dimensions
import aspose.imaging.xmp.types.complex.font
import aspose.imaging.xmp.types.complex.resourceevent
import aspose.imaging.xmp.types.complex.resourceref
import aspose.imaging.xmp.types.complex.thumbnail
import aspose.imaging.xmp.types.complex.version
import aspose.imaging.xmp.types.derived

class Group3Options(enum.Enum):
    ENCODING_1D = enum.auto()
    '''1-dimensional coding. (default)'''
    ENCODING_2D = enum.auto()
    '''2-dimensional coding.'''
    UNCOMPRESSED = enum.auto()
    '''Data not compressed.'''
    FILL_BITS = enum.auto()
    '''Fill to byte boundary.'''

class TiffAlphaStorage(enum.Enum):
    UNSPECIFIED = enum.auto()
    '''The alpha is not specified and stored in the tiff file.'''
    ASSOCIATED = enum.auto()
    '''The alpha value is stored in premultiplied form. When alpha is restored there may be some rounding effects and restored value may be different from the original.'''
    UNASSOCIATED = enum.auto()
    '''The alpha value is stored in unassociated form. That means that alpha restored is exactly the same as it was stored to the tiff.'''

class TiffByteOrder(enum.Enum):
    BIG_ENDIAN = enum.auto()
    '''The big endian byte order (Motorola).'''
    LITTLE_ENDIAN = enum.auto()
    '''The little endian byte order (Intel).'''

class TiffCompressions(enum.Enum):
    NONE = enum.auto()
    '''Dump mode.'''
    CCITT_RLE = enum.auto()
    '''CCITT modified Huffman RLE.'''
    CCITT_FAX3 = enum.auto()
    '''CCITT Group 3 fax encoding.'''
    CCITT_FAX4 = enum.auto()
    '''CCITT Group 4 fax encoding.'''
    LZW = enum.auto()
    '''Lempel-Ziv & Welch.'''
    OJPEG = enum.auto()
    '''Original JPEG / Old-style JPEG (6.0).'''
    JPEG = enum.auto()
    '''JPEG DCT compression. Introduced post TIFF rev 6.0.'''
    NEXT = enum.auto()
    '''NeXT 2-bit RLE.'''
    CCITT_RLE_W = enum.auto()
    '''CCITT RLE.'''
    PACKBITS = enum.auto()
    '''Macintosh RLE.'''
    THUNDERSCAN = enum.auto()
    '''ThunderScan RLE.'''
    IT_8_CTPAD = enum.auto()
    '''IT8 CT w/padding. Reserved for ANSI IT8 TIFF/IT.'''
    IT_8_LW = enum.auto()
    '''IT8 Linework RLE. Reserved for ANSI IT8 TIFF/IT.'''
    IT_8_MP = enum.auto()
    '''IT8 Monochrome picture. Reserved for ANSI IT8 TIFF/IT.'''
    IT_8_BL = enum.auto()
    '''IT8 Binary line art. Reserved for ANSI IT8 TIFF/IT.'''
    PIXAR_FILM = enum.auto()
    '''Pixar companded 10bit LZW. Reserved for Pixar.'''
    PIXAR_LOG = enum.auto()
    '''Pixar companded 11bit ZIP. Reserved for Pixar.'''
    DEFLATE = enum.auto()
    '''Deflate compression.'''
    ADOBE_DEFLATE = enum.auto()
    '''Deflate compression, as recognized by Adobe.'''
    DCS = enum.auto()
    '''Kodak DCS encoding.
    Reserved for Oceana Matrix'''
    JBIG = enum.auto()
    '''ISO Jpeg big.'''
    SGILOG = enum.auto()
    '''SGI Log Luminance RLE.'''
    SGILOG24 = enum.auto()
    '''SGI Log 24-bit packed.'''
    JP2000 = enum.auto()
    '''Leadtools JPEG2000.'''

class TiffDataTypes(enum.Enum):
    BYTE = enum.auto()
    '''8-bit unsigned integer.'''
    ASCII = enum.auto()
    '''8-bit bytes with last byte ``null``.'''
    SHORT = enum.auto()
    '''16-bit unsigned integer.'''
    LONG = enum.auto()
    '''32-bit unsigned integer.'''
    RATIONAL = enum.auto()
    '''64-bit unsigned fraction.'''
    SBYTE = enum.auto()
    '''8-bit signed integer.'''
    UNDEFINED = enum.auto()
    '''8-bit untyped data.'''
    SSHORT = enum.auto()
    '''16-bit signed integer.'''
    SLONG = enum.auto()
    '''32-bit signed integer.'''
    SRATIONAL = enum.auto()
    '''64-bit signed fraction.'''
    FLOAT = enum.auto()
    '''32-bit IEEE floating point.'''
    DOUBLE = enum.auto()
    '''64-bit IEEE floating point.'''
    IFD = enum.auto()
    '''Pointer to Exif image file directory (IFD).'''
    LONG8 = enum.auto()
    '''Unsigned 64-bit integer.'''
    S_LONG8 = enum.auto()
    '''Signed 64-bit integer.'''
    IFD8 = enum.auto()
    '''Unsigned 64-bit IFD offset.'''

class TiffExpectedFormat(enum.Enum):
    DEFAULT = enum.auto()
    '''The default TIFF format is no compression with B/W 1 bit per pixel only format. You can also use this setting to get an empty options and initialize with your tags or other settings.'''
    TIFF_LZW_BW = enum.auto()
    '''The TIFF having LZW compression and B/W 1 bit per pixel only format.'''
    TIFF_LZW_RGB = enum.auto()
    '''The TIFF having LZW compression and RGB color format.'''
    TIFF_LZW_RGBA = enum.auto()
    '''The TIFF having LZW compression and ARGB with transparency color format.'''
    TIFF_LZW_CMYK = enum.auto()
    '''The TIFF having LZW compression and CMYK color mode.'''
    TIFF_LZW_CMYKA = enum.auto()
    '''The TIFF having LZW compression and CMYKA color mode with transparency.'''
    TIFF_CCITT_FAX3 = enum.auto()
    '''The TIFF having CCITT FAX3 encoding. B/W 1 bit per pixel only supported for that scheme.'''
    TIFF_CCITT_FAX4 = enum.auto()
    '''The TIFF having CCITT FAX4 encoding. B/W 1 bit per pixel only supported for that scheme.'''
    TIFF_DEFLATE_BW = enum.auto()
    '''The TIFF having Deflate compression and B/W 1 bit per pixel only format.'''
    TIFF_DEFLATE_RGB = enum.auto()
    '''The TIFF having Deflate compression and RGB color format.'''
    TIFF_DEFLATE_RGBA = enum.auto()
    '''The TIFF having Deflate compression and ARGB color format.'''
    TIFF_DEFLATE_CMYK = enum.auto()
    '''The TIFF having Deflate compression and CMYK color format.'''
    TIFF_DEFLATE_CMYKA = enum.auto()
    '''The TIFF having Deflate compression and CMYKA color format with transparency.'''
    TIFF_CCIT_RLE = enum.auto()
    '''The TIFF havingCCITT RLE encoding. B/W 1 bit per pixel only supported for that scheme.'''
    TIFF_JPEG_RGB = enum.auto()
    '''The TIFF having Jpeg compression and RGB color format.'''
    TIFF_JPEG_Y_CB_CR = enum.auto()
    '''The TIFF having Jpeg compression and YCBCR color format.'''
    TIFF_NO_COMPRESSION_BW = enum.auto()
    '''The uncompressed TIFF having B/W 1 bit per pixel only format.'''
    TIFF_NO_COMPRESSION_RGB = enum.auto()
    '''The uncompressed TIFF having RGB color format.'''
    TIFF_NO_COMPRESSION_RGBA = enum.auto()
    '''The uncompressed TIFF having ARGB color format with transparency.'''
    TIFF_NO_COMPRESSION_CMYK = enum.auto()
    '''The uncompressed TIFF having CMYK color format.'''
    TIFF_NO_COMPRESSION_CMYKA = enum.auto()
    '''The uncompressed TIFF having CMYK color format with transparency.'''

class TiffFileStandards(enum.Enum):
    BASELINE = enum.auto()
    '''The Baseline TIFF 6.0 file standard. This standard is formally known as TIFF 6.0, Part 1: Baseline TIFF.'''
    EXTENDED = enum.auto()
    '''The Extended TIFF 6.0 file standard. This standard is formally known as Extended TIFF 6.0, Part 2: TIFF Extensions.'''

class TiffFillOrders(enum.Enum):
    MSB_2_LSB = enum.auto()
    '''Most significant -> least.'''
    LSB_2_MSB = enum.auto()
    '''Least significant -> most.'''

class TiffNewSubFileTypes(enum.Enum):
    FILE_TYPE_DEFAULT = enum.auto()
    '''The default filetype.'''
    FILE_TYPE_REDUCED_IMAGE = enum.auto()
    '''The reduced image filetype.'''
    FILE_TYPE_PAGE = enum.auto()
    '''The page filetype.'''
    FILE_TYPE_MASK = enum.auto()
    '''The mask filetype.'''
    FILE_TYPE_LAST = enum.auto()
    '''The last filetype.'''

class TiffOrientations(enum.Enum):
    TOP_LEFT = enum.auto()
    '''Row 0 top, Column 0 lhs.'''
    TOP_RIGHT = enum.auto()
    '''Row 0 top, Column 0 rhs.'''
    BOTTOM_RIGHT = enum.auto()
    '''Row 0 bottom, Column 0 rhs.'''
    BOTTOM_LEFT = enum.auto()
    '''Row 0 bottom, Column 0 lhs.'''
    LEFT_TOP = enum.auto()
    '''Row 0 lhs, Column 0 top.'''
    RIGHT_TOP = enum.auto()
    '''Row 0 rhs, Column 0 top.'''
    RIGHT_BOTTOM = enum.auto()
    '''Row 0 rhs, Column 0 bottom.'''
    LEFT_BOTTOM = enum.auto()
    '''Row 0 lhs, Column 0 bottom.'''

class TiffPhotometrics(enum.Enum):
    MIN_IS_WHITE = enum.auto()
    '''Min value is white.'''
    MIN_IS_BLACK = enum.auto()
    '''Min value is black.'''
    RGB = enum.auto()
    '''RGB color model.'''
    PALETTE = enum.auto()
    '''Color map indexed.'''
    MASK = enum.auto()
    '''[obsoleted by TIFF rev. 6.0] Holdout mask.'''
    SEPARATED = enum.auto()
    '''Color separations.'''
    YCBCR = enum.auto()
    '''The CCIR 601.'''
    CIELAB = enum.auto()
    '''1976 CIE L*a*b*.'''
    ICCLAB = enum.auto()
    '''ICC L*a*b*. Introduced post TIFF rev 6.0 by Adobe TIFF Technote 4.'''
    ITULAB = enum.auto()
    '''ITU L*a*b*.'''
    LOGL = enum.auto()
    '''CIE Log2(L).'''
    LOGLUV = enum.auto()
    '''CIE Log2(L) (u\',v\').'''

class TiffPlanarConfigs(enum.Enum):
    CONTIGUOUS = enum.auto()
    '''Single image plane.'''
    SEPARATE = enum.auto()
    '''Separate planes of data.'''

class TiffPredictor(enum.Enum):
    NONE = enum.auto()
    '''No prediction scheme used.'''
    HORIZONTAL = enum.auto()
    '''Horizontal differencing.'''

class TiffResolutionUnits(enum.Enum):
    NONE = enum.auto()
    '''No meaningful units.'''
    INCH = enum.auto()
    '''English system.'''
    CENTIMETER = enum.auto()
    '''Metric system.'''

class TiffSampleFormats(enum.Enum):
    UINT = enum.auto()
    '''Unsigned integer data'''
    INT = enum.auto()
    '''Signed integer data'''
    IEEE_FP = enum.auto()
    '''IEEE floating point data'''
    VOID = enum.auto()
    '''Untyped data'''
    COMPLEX_INT = enum.auto()
    '''Complex signed int'''
    COMPLEX_IEEE_FP = enum.auto()
    '''Complex ieee floating'''

class TiffTags(enum.Enum):
    SUB_FILE_TYPE = enum.auto()
    '''Subfile data descriptor.'''
    OSUBFILE_TYPE = enum.auto()
    '''[obsoleted by TIFF rev. 5.0]
    
    Kind of data in subfile.'''
    IMAGE_WIDTH = enum.auto()
    '''Image width in pixels.'''
    IMAGE_LENGTH = enum.auto()
    '''Image height in pixels.'''
    BITS_PER_SAMPLE = enum.auto()
    '''Bits per channel (sample).'''
    COMPRESSION = enum.auto()
    '''Data compression technique.'''
    PHOTOMETRIC = enum.auto()
    '''Photometric interpretation.'''
    THRESHOLDING = enum.auto()
    '''[obsoleted by TIFF rev. 5.0]
    
    Thresholding used on data.'''
    CELL_WIDTH = enum.auto()
    '''[obsoleted by TIFF rev. 5.0]
    
    Dithering matrix width.'''
    CELL_LENGTH = enum.auto()
    '''[obsoleted by TIFF rev. 5.0]
    
    Dithering matrix height.'''
    FILL_ORDER = enum.auto()
    '''Data order within a byte.'''
    DOCUMENT_NAME = enum.auto()
    '''Name of document which holds for image.'''
    IMAGE_DESCRIPTION = enum.auto()
    '''Information about image.'''
    MAKE = enum.auto()
    '''Scanner manufacturer name.'''
    MODEL = enum.auto()
    '''Scanner model name/number.'''
    STRIP_OFFSETS = enum.auto()
    '''Offsets to data strips.'''
    ORIENTATION = enum.auto()
    '''[obsoleted by TIFF rev. 5.0]
    
    Image orientation.'''
    SAMPLES_PER_PIXEL = enum.auto()
    '''Samples per pixel.'''
    ROWS_PER_STRIP = enum.auto()
    '''Rows per strip of data.'''
    STRIP_BYTE_COUNTS = enum.auto()
    '''Bytes counts for strips.'''
    MIN_SAMPLE_VALUE = enum.auto()
    '''[obsoleted by TIFF rev. 5.0]
    
    Minimum sample value.'''
    MAX_SAMPLE_VALUE = enum.auto()
    '''[obsoleted by TIFF rev. 5.0]
    
    Maximum sample value.'''
    XRESOLUTION = enum.auto()
    '''Pixels/resolution in x.'''
    YRESOLUTION = enum.auto()
    '''Pixels/resolution in y.'''
    PLANAR_CONFIG = enum.auto()
    '''Storage organization.'''
    PAGE_NAME = enum.auto()
    '''Page name image is from.'''
    XPOSITION = enum.auto()
    '''X page offset of image lhs.'''
    YPOSITION = enum.auto()
    '''Y page offset of image lhs.'''
    FREE_OFFSETS = enum.auto()
    '''[obsoleted by TIFF rev. 5.0]
    
    Byte offset to free block.'''
    FREE_BYTE_COUNTS = enum.auto()
    '''[obsoleted by TIFF rev. 5.0]
    
    Sizes of free blocks.'''
    GRAY_RESPONSE_UNIT = enum.auto()
    '''[obsoleted by TIFF rev. 6.0]
    
    Gray scale curve accuracy.'''
    GRAY_RESPONSE_CURVE = enum.auto()
    '''[obsoleted by TIFF rev. 6.0]
    
    Gray scale response curve.'''
    T4_OPTIONS = enum.auto()
    '''TIFF 6.0 proper name alias for GROUP3OPTIONS.
    Options for CCITT Group 3 fax encoding. 32 flag bits.'''
    T6_OPTIONS = enum.auto()
    '''Options for CCITT Group 4 fax encoding. 32 flag bits.
    TIFF 6.0 proper name alias for GROUP4OPTIONS.'''
    RESOLUTION_UNIT = enum.auto()
    '''Units of resolutions.'''
    PAGE_NUMBER = enum.auto()
    '''Page numbers of multi-page.'''
    COLOR_RESPONSE_UNIT = enum.auto()
    '''[obsoleted by TIFF rev. 6.0]
    
    Color curve accuracy.'''
    TRANSFER_FUNCTION = enum.auto()
    '''Colorimetry info.'''
    SOFTWARE = enum.auto()
    '''Name & release.'''
    DATE_TIME = enum.auto()
    '''Creation date and time.'''
    ARTIST = enum.auto()
    '''Creator of image.'''
    HOST_COMPUTER = enum.auto()
    '''Machine where created.'''
    PREDICTOR = enum.auto()
    '''Prediction scheme w/ LZW.'''
    WHITE_POINT = enum.auto()
    '''Image white point.'''
    PRIMARY_CHROMATICITIES = enum.auto()
    '''Primary chromaticities.'''
    COLOR_MAP = enum.auto()
    '''RGB map for pallette image.'''
    HALFTONE_HINTS = enum.auto()
    '''Highlight + shadow info.'''
    TILE_WIDTH = enum.auto()
    '''Tile width in pixels.'''
    TILE_LENGTH = enum.auto()
    '''Tile height in pixels.'''
    TILE_OFFSETS = enum.auto()
    '''Offsets to data tiles.'''
    TILE_BYTE_COUNTS = enum.auto()
    '''Byte counts for tiles.'''
    BAD_FAX_LINES = enum.auto()
    '''Lines with wrong pixel count.'''
    CLEAN_FAX_DATA = enum.auto()
    '''Regenerated line info.'''
    CONSECUTIVE_BAD_FAX_LINES = enum.auto()
    '''Max consecutive bad lines.'''
    SUB_IFD = enum.auto()
    '''Subimage descriptors.'''
    INK_SET = enum.auto()
    '''Inks in separated image.'''
    INK_NAMES = enum.auto()
    '''ASCII names of inks.'''
    NUMBER_OF_INKS = enum.auto()
    '''Number of inks.'''
    DOT_RANGE = enum.auto()
    '''0% and 100% dot codes.'''
    TARGET_PRINTER = enum.auto()
    '''Separation target.'''
    EXTRA_SAMPLES = enum.auto()
    '''Information about extra samples.'''
    SAMPLE_FORMAT = enum.auto()
    '''Data sample format.'''
    SMIN_SAMPLE_VALUE = enum.auto()
    '''Variable MinSampleValue.'''
    SMAX_SAMPLE_VALUE = enum.auto()
    '''Variable MaxSampleValue.'''
    TRANSFER_RANGE = enum.auto()
    '''Variable TransferRange'''
    CLIP_PATH = enum.auto()
    '''ClipPath. Introduced post TIFF rev 6.0 by Adobe TIFF technote 2.'''
    XCLIPPATHUNITS = enum.auto()
    '''XClipPathUnits. Introduced post TIFF rev 6.0 by Adobe TIFF technote 2.'''
    YCLIPPATHUNITS = enum.auto()
    '''YClipPathUnits. Introduced post TIFF rev 6.0 by Adobe TIFF technote 2.'''
    INDEXED = enum.auto()
    '''Indexed. Introduced post TIFF rev 6.0 by Adobe TIFF Technote 3.'''
    JPEG_TABLES = enum.auto()
    '''JPEG table stream. Introduced post TIFF rev 6.0.'''
    OPI_PROXY = enum.auto()
    '''OPI Proxy. Introduced post TIFF rev 6.0 by Adobe TIFF technote.'''
    JPEG_PROC = enum.auto()
    '''[obsoleted by Technical Note #2 which specifies a revised JPEG-in-TIFF scheme]
    
    JPEG processing algorithm.'''
    JPEG_INERCHANGE_FORMAT = enum.auto()
    '''[obsoleted by Technical Note #2 which specifies a revised JPEG-in-TIFF scheme]
    
    Pointer to SOI marker.'''
    JPEG_INTERCHANGE_FORMAT_LENGTH = enum.auto()
    '''[obsoleted by Technical Note #2 which specifies a revised JPEG-in-TIFF scheme]
    
    JFIF stream length'''
    JPEG_RESTART_INTERVAL = enum.auto()
    '''[obsoleted by Technical Note #2 which specifies a revised JPEG-in-TIFF scheme]
    
    Restart interval length.'''
    JPEG_LOSSLESS_PREDICTORS = enum.auto()
    '''[obsoleted by Technical Note #2 which specifies a revised JPEG-in-TIFF scheme]
    
    Lossless proc predictor.'''
    JPEG_POINT_TRANSFORM = enum.auto()
    '''[obsoleted by Technical Note #2 which specifies a revised JPEG-in-TIFF scheme]
    
    Lossless point transform.'''
    JPEG_Q_TABLES = enum.auto()
    '''[obsoleted by Technical Note #2 which specifies a revised JPEG-in-TIFF scheme]
    
    Q matrice offsets.'''
    JPEG_D_CTABLES = enum.auto()
    '''[obsoleted by Technical Note #2 which specifies a revised JPEG-in-TIFF scheme]
    
    DCT table offsets.'''
    JPEG_A_CTABLES = enum.auto()
    '''[obsoleted by Technical Note #2 which specifies a revised JPEG-in-TIFF scheme]
    
    AC coefficient offsets.'''
    YCBCR_COEFFICIENTS = enum.auto()
    '''RGB -> YCbCr transform.'''
    YCBCR_SUB_SAMPLING = enum.auto()
    '''YCbCr subsampling factors.'''
    YCBCR_POSITIONING = enum.auto()
    '''Subsample positioning.'''
    REFERENCE_BLACK_WHITE = enum.auto()
    '''Colorimetry info.'''
    XML_PACKET = enum.auto()
    '''XML packet. Introduced post TIFF rev 6.0 by Adobe XMP Specification, January 2004.'''
    OPI_IMAGEID = enum.auto()
    '''OPI ImageID. Introduced post TIFF rev 6.0 by Adobe TIFF technote.'''
    REFPTS = enum.auto()
    '''Image reference points. Private tag registered to Island Graphics.'''
    COPYRIGHT = enum.auto()
    '''Copyright string. This tag is listed in the TIFF rev. 6.0 w/ unknown ownership.'''
    PHOTOSHOP_RESOURCES = enum.auto()
    '''Photoshop image resources.'''
    ICC_PROFILE = enum.auto()
    '''The embedded ICC device profile'''
    EXIF_IFD_POINTER = enum.auto()
    '''A pointer to the Exif IFD.'''
    XP_TITLE = enum.auto()
    '''Information about image, used by Windows Explorer.
    The :py:attr:`aspose.imaging.fileformats.tiff.enums.TiffTags.XP_TITLE` is ignored by Windows Explorer if the :py:attr:`aspose.imaging.fileformats.tiff.enums.TiffTags.IMAGE_DESCRIPTION` tag exists.'''
    XP_COMMENT = enum.auto()
    '''Comment on image, used by Windows Explorer.'''
    XP_AUTHOR = enum.auto()
    '''Image Author, used by Windows Explorer.
    The :py:attr:`aspose.imaging.fileformats.tiff.enums.TiffTags.XP_AUTHOR` is ignored by Windows Explorer if the :py:attr:`aspose.imaging.fileformats.tiff.enums.TiffTags.ARTIST` tag exists.'''
    XP_KEYWORDS = enum.auto()
    '''Image Keywords, used by Windows Explorer.'''
    XP_SUBJECT = enum.auto()
    '''Subject image, used by Windows Explorer.'''

class TiffThresholds(enum.Enum):
    NO_DITHERING = enum.auto()
    '''No dithering is performed.'''
    HALF_TONE = enum.auto()
    '''Dithered scan.'''
    ERROR_DIFFUSE = enum.auto()
    '''Usually Floyd-Steinberg.'''

