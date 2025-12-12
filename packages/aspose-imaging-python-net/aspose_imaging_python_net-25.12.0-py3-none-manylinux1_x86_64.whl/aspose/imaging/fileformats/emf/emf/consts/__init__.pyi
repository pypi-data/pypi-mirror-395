"""The namespace contains types [MS-EMF]: Enhanced Metafile Format.
            2.1 EMF Enumerations"""
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

class EmfArcDirection(enum.Enum):
    AD_COUNTERCLOCKWISE = enum.auto()
    '''Figures drawn counterclockwise'''
    AD_CLOCKWISE = enum.auto()
    '''Figures drawn clockwise.'''

class EmfArmStyle(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any style.'''
    PAN_NO_FIT = enum.auto()
    '''The No fit.'''
    PAN_STRAIGHT_ARMS_HORZ = enum.auto()
    '''The Straight arms/horizontal.'''
    PAN_STRAIGHT_ARMS_WEDGE = enum.auto()
    '''The Straight arms/wedge'''
    PAN_STRAIGHT_ARMS_VERT = enum.auto()
    '''The Straight arms/vertical'''
    PAN_STRAIGHT_ARMS_SINGLE_SERIF = enum.auto()
    '''The Straight arms/single-serif.'''
    PAN_STRAIGHT_ARMS_DOUBLE_SERIF = enum.auto()
    '''The Straight arms/double-serif.'''
    PAN_BENT_ARMS_HORZ = enum.auto()
    '''The Non straight arms/horizontal.'''
    PAN_BENT_ARMS_WEDGE = enum.auto()
    '''The Non straight arms/wedge'''
    PAN_BENT_ARMS_VERT = enum.auto()
    '''The Non straight arms/vertical.'''
    PAN_BENT_ARMS_SINGLE_SERIF = enum.auto()
    '''The Non straight arms/single-serif.'''
    PAN_BENT_ARMS_DOUBLE_SERIF = enum.auto()
    '''The Non straight arms/double-serif.'''

class EmfBackgroundMode(enum.Enum):
    TRANSPARENT = enum.auto()
    '''The transparent - Background remains untouched.'''
    OPAQUE = enum.auto()
    '''The opaque - Background is filled with the current background color before the text, hatched brush, or pen is drawn'''

class EmfColorAdjustmentEnum(enum.Enum):
    CA_NEGATIVE = enum.auto()
    '''Specifies that the negative of the original image SHOULD be displayed.'''
    CA_LOG_FILTER = enum.auto()
    '''The Specifies that a logarithmic process SHOULD be applied to the final
    density of the output colors. This will increase the color contrast when the luminance is low'''

class EmfColorMatchToTarget(enum.Enum):
    COLORMATCHTOTARGET_NOTEMBEDDED = enum.auto()
    '''Indicates that a color profile has not been embedded in the metafile.'''
    COLORMATCHTOTARGET_EMBEDDED = enum.auto()
    '''Indicates that a color profile has been embedded in the metafile'''

class EmfColorSpace(enum.Enum):
    CS_ENABLE = enum.auto()
    '''Maps colors to the target device\'s color gamut. This enables color proofing.
    All subsequent draw commands to the playback device context will render colors as they would appear on the target device.'''
    CS_DISABLE = enum.auto()
    '''Disables color proofing.'''
    CS_DELETE_TRANSFORM = enum.auto()
    '''If color management is enabled for the target profile, disables it and deletes the concatenated transform.'''

class EmfContrast(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any contrast'''
    PAN_NO_FIT = enum.auto()
    '''The No fit.'''
    PAN_CONTRAST_NONE = enum.auto()
    '''None contrast.'''
    PAN_CONTRAST_VERY_LOW = enum.auto()
    '''Very low contrast.'''
    PAN_CONTRAST_LOW = enum.auto()
    '''Low contrast.'''
    PAN_CONTRAST_MEDIUM_LOW = enum.auto()
    '''The Medium low.'''
    PAN_CONTRAST_MEDIUM = enum.auto()
    '''The Medium.'''
    PAN_CONTRAST_MEDIUM_HIGH = enum.auto()
    '''The Medium high.'''
    PAN_CONTRAST_HIGH = enum.auto()
    '''The High contrast.'''
    PAN_CONTRAST_VERY_HIGH = enum.auto()
    '''The Very high.'''

class EmfDibColors(enum.Enum):
    DIB_RGB_COLORS = enum.auto()
    '''The color table contains literal RGB values'''
    DIB_PAL_COLORS = enum.auto()
    '''The color table consists of an array of 16-bit indexes into the LogPalette object (section 2.2.17) that is currently defined in the playback device context.'''
    DIB_PAL_INDICES = enum.auto()
    '''No color table exists. The pixels in the DIB are indices into the current logical palette in the playback device context.'''

class EmfEmrComment(enum.Enum):
    EMR_COMMENT_WINDOWS_METAFILE = enum.auto()
    '''This comment record contains a specification of an image in WMF. See [MS-WMF] for more information'''
    EMR_COMMENT_BEGINGROUP = enum.auto()
    '''This comment record identifies the beginning of a group of drawing records. It identifies an object within an EMF metafile'''
    EMR_COMMENT_ENDGROUP = enum.auto()
    '''This comment record identifies the end of a group of drawing records. For every EMR_COMMENT_BEGINGROUP
    record, an EMR_COMMENT_ENDGROUP record MUST be included in the metafile, and they MAY be nested.'''
    EMR_COMMENT_MULTIFORMATS = enum.auto()
    '''This comment record allows multiple definitions of an image to be included in the metafile.
    Using this comment, for example, an application can include encapsulated PostScript text as well as an EMF definition of an image.'''
    EMR_COMMENT_UNICODE_STRING = enum.auto()
    '''This comment record is reserved and MUST NOT be used in an EMF metafile'''
    EMR_COMMENT_UNICODE_END = enum.auto()
    '''This comment record is reserved and MUST NOT be used in an EMF metafile'''

class EmfExtTextOutOptions(enum.Enum):
    ETO_OPAQUE = enum.auto()
    '''This bit indicates that the current background color SHOULD be used to fill the rectangle'''
    ETO_CLIPPED = enum.auto()
    '''This bit indicates that the text SHOULD be clipped to the rectangle.'''
    ETO_GLYPH_INDEX = enum.auto()
    '''This bit indicates that the codes for characters in an output text string are actually
    indexes of the character glyphs in a TrueType font. Glyph indexes are font-specific,
    so to display the correct characters on playback, the font that is used MUST be
    identical to the font used to generate the indexes.'''
    ETO_RTLREADING = enum.auto()
    '''This bit indicates that the text MUST be laid out in right-to-left reading order,
    instead of the default left-to-right order. This SHOULD be applied only when the font
    selected into the playback device context is either Hebrew or Arabic'''
    ETO_NO_RECT = enum.auto()
    '''This bit indicates that the record does not specify a bounding rectangle for the text output.'''
    ETO_SMALL_CHARS = enum.auto()
    '''This bit indicates that the codes for characters in an output text string are 8 bits,
    derived from the low bytes of 16-bit Unicode UTF16-LE character codes,
    in which the high byte is assumed to be 0.'''
    ETO_NUMERICSLOCAL = enum.auto()
    '''This bit indicates that to display numbers, digits appropriate to the locale SHOULD be used'''
    ETO_NUMERICSLATIN = enum.auto()
    '''This bit indicates that to display numbers, European digits SHOULD be used'''
    ETO_IGNORELANGUAGE = enum.auto()
    '''This bit indicates that no special operating system processing for glyph placement should be
    performed on right-to-left strings; that is, all glyph positioning SHOULD be taken care of by
    drawing and state records in the metafile'''
    ETO_PDY = enum.auto()
    '''This bit indicates that both horizontal and vertical character displacement values SHOULD be provided'''
    ETO_REVERSE_INDEX_MAP = enum.auto()
    '''This bit is reserved and SHOULD NOT be used'''

class EmfFamilyType(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any type.'''
    PAN_NO_FIT = enum.auto()
    '''The No fit.'''
    PAN_FAMILY_TEXT_DISPLAY = enum.auto()
    '''Text and display.'''
    PAN_FAMILY_SCRIPT = enum.auto()
    '''Script flag.'''
    PAN_FAMILY_DECORATIVE = enum.auto()
    '''Decorative flag.'''
    PAN_FAMILY_PICTORIAL = enum.auto()
    '''Pictorial flag.'''

class EmfFloodFill(enum.Enum):
    FLOODFILLBORDER = enum.auto()
    '''The fill area is bounded by a specific color'''
    FLOODFILLSURFACE = enum.auto()
    '''The fill area is defined by a specific color. Filling continues outward in all directions
    as long as the color is encountered. This style is useful for filling areas with multicolored boundaries'''

class EmfFormatSignature(enum.Enum):
    ENHMETA_SIGNATURE = enum.auto()
    '''The value of this member is the sequence of ASCII characters "FME ",
    which happens to be the reverse of the string "EMF", and it denotes EMF record data.
    Note The space character in the string is significant and MUST be present.'''
    EPS_SIGNATURE = enum.auto()
    '''The value of this member is the sequence of ASCII characters "FSPE", which happens
    to be the reverse of the string "EPSF", and it denotes encapsulated PostScript (EPS) format data.'''

class EmfGradientFill(enum.Enum):
    GRADIENT_FILL_RECT_H = enum.auto()
    '''A mode in which color interpolation is performed along a gradient from the left to the right edges of a rectangle'''
    GRADIENT_FILL_RECT_V = enum.auto()
    '''A mode in which color interpolation is performed along a gradient from the top to the bottom edges of a rectangle.'''
    GRADIENT_FILL_TRIANGLE = enum.auto()
    '''A mode in which color interpolation is performed between vertexes of a triangleS'''

class EmfGraphicsMode(enum.Enum):
    GM_COMPATIBLE = enum.auto()
    '''TrueType text MUST be written from left to right and right side up, even if the rest of the graphics
    are rotated about the x-axis or y-axis because of the current world-to-device transformation in
    the playback device context. Only the height of the text SHOULD be scaled. Arcs MUST be drawn using
    the current arc direction in the playback device context, but they MUST NOT respect the current
    world-to-device transformation, which might require a rotation along the x-axis or y-axis.
    The world-to-device transformation SHOULD only be modified by changing the window and viewport
    extents and origins, using the EMR_SETWINDOWEXTEX (section 2.3.11.30) and EMR_SETVIEWPORTEXTEX
    (section 2.3.11.28) records, and the EMR_SETWINDOWORGEX (section 2.3.11.31) and EMR_SETVIEWPORTORGEX
    (section 2.3.11.30) records, respectively. bChanging the transformation directly by using the
    EMR_MODIFYWORLDTRANSFORM (section 2.3.12.1) or EMR_SETWORLDTRANSFORM (section 2.3.12.2) records MAY NOT be supported.
    In GM_COMPATIBLE graphics mode, bottom and rightmost edges MUST be excluded when rectangles are drawn'''
    GM_ADVANCED = enum.auto()
    '''TrueType text output MUST fully conform to the current world-to-device transformation in the playback device context.
    Arcs MUST be drawn in the counterclockwise direction in world space; however, both arc control points
    and the arcs themselves MUST fully respect the current world-to-device transformation in the playback device context.
    The world-to-device transform MAY be modified directly by using the EMR_MODIFYWORLDTRANSFORM or
    EMR_SETWORLDTRANSFORM records, or indirectly by changing the window and viewport extents and origins,
    using the EMR_SETWINDOWEXTEX (section 2.3.11.30) and EMR_SETVIEWPORTEXTEX (section 2.3.11.28) records,
    and the EMR_SETWINDOWORGEX (section 2.3.11.31) and EMR_SETVIEWPORTORGEX (section 2.3.11.30) records, respectively.
    In GM_ADVANCED graphics mode, bottom and rightmost edges MUST be included when rectangles are drawn.'''

class EmfHatchStyle(enum.Enum):
    HS_HORIZONTAL = enum.auto()
    '''A horizontal hatch.'''
    HS_VERTICAL = enum.auto()
    '''A vertical hatch.'''
    HS_FDIAGONAL = enum.auto()
    '''A 45-degree downward, left-to-right hatch.'''
    HS_BDIAGONAL = enum.auto()
    '''A 45-degree upward, left-to-right hatch.'''
    HS_CROSS = enum.auto()
    '''A horizontal and vertical cross-hatch.'''
    HS_DIAGCROSS = enum.auto()
    '''A 45-degree crosshatch.'''
    HS_SOLIDCLR = enum.auto()
    '''The hatch is not a pattern, but is a solid color.'''
    HS_DITHEREDCLR = enum.auto()
    '''The hatch is not a pattern, but is a solid color.'''
    HS_SOLIDTEXTCLR = enum.auto()
    '''The hatch is not a pattern, but is a solid color, defined by the current text (foreground) color'''
    HS_DITHEREDTEXTCLR = enum.auto()
    '''The hatch is not a pattern, but is a dithered color, defined by the current text (foreground) color.'''
    HS_SOLIDBKCLR = enum.auto()
    '''The hatch is not a pattern, but is a solid color, defined by the current background color'''
    HS_DITHEREDBKCLR = enum.auto()
    '''The hatch is not a pattern, but is a dithered color, defined by the current background color.'''

class EmfIcmMode(enum.Enum):
    ICM_OFF = enum.auto()
    '''Turns off Image Color Management (ICM) in the playback device context. Turns on old-style color correction of halftones'''
    ICM_ON = enum.auto()
    '''Turns on ICM in the playback device context. Turns off old-style color correction of halftones.'''
    ICM_QUERY = enum.auto()
    '''Queries the current state of color management in the playback device context.'''
    ICM_DONE_OUTSIDEDC = enum.auto()
    '''Turns off ICM in the playback device context, and turns off old-style color correction of halftones'''

class EmfIlluminant(enum.Enum):
    ILLUMINANT_DEVICE_DEFAULT = enum.auto()
    '''Device\'s default. Standard used by output devices.'''
    ILLUMINANT_TUNGSTEN = enum.auto()
    '''Tungsten lamp.'''
    ILLUMINANT_B = enum.auto()
    '''Noon sunlight.'''
    ILLUMINANT_DAYLIGHT = enum.auto()
    '''Daylight illumination'''
    ILLUMINANT_D50 = enum.auto()
    '''Normal print'''
    ILLUMINANT_D55 = enum.auto()
    '''Bond paper print.'''
    ILLUMINANT_D65 = enum.auto()
    '''Standard daylight. Standard for CRTs and pictures.'''
    ILLUMINANT_D75 = enum.auto()
    '''Northern daylight.'''
    ILLUMINANT_FLUORESCENT = enum.auto()
    '''Cool white lamp.'''

class EmfLetterform(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any letter form'''
    PAN_NO_FIT = enum.auto()
    '''The No fit.'''
    PAN_LETT_NORMAL_CONTACT = enum.auto()
    '''Normal / contact.'''
    PAN_LETT_NORMAL_WEIGHTED = enum.auto()
    '''Normal / weighted.'''
    PAN_LETT_NORMAL_BOXED = enum.auto()
    '''Normal / boxed.'''
    PAN_LETT_NORMAL_FLATTENED = enum.auto()
    '''Normal / flattened'''
    PAN_LETT_NORMAL_ROUNDED = enum.auto()
    '''Normal / rounded'''
    PAN_LETT_NORMAL_OFF_CENTER = enum.auto()
    '''Normal / off center.'''
    PAN_LETT_NORMAL_SQUARE = enum.auto()
    '''Normal / square'''
    PAN_LETT_OBLIQUE_CONTACT = enum.auto()
    '''Oblique / contact'''
    PAN_LETT_OBLIQUE_WEIGHTED = enum.auto()
    '''Oblique / weighted.'''
    PAN_LETT_OBLIQUE_BOXED = enum.auto()
    '''Oblique / boxed.'''
    PAN_LETT_OBLIQUE_FLATTENED = enum.auto()
    '''Oblique / flattened.'''
    PAN_LETT_OBLIQUE_ROUNDED = enum.auto()
    '''Oblique / rounded.'''
    PAN_LETT_OBLIQUE_OFF_CENTER = enum.auto()
    '''Oblique / off center'''
    PAN_LETT_OBLIQUE_SQUARE = enum.auto()
    '''Oblique / square'''

class EmfLogFontWeight(enum.Enum):
    FW_DONTCARE = enum.auto()
    '''The don\'t care'''
    FW_THIN = enum.auto()
    '''The thin weight.'''
    FW_EXTRALIGHT = enum.auto()
    '''The extralight weight.'''
    FW_ULTRALIGHT = enum.auto()
    '''The ultralight weight.'''
    FW_LIGHT = enum.auto()
    '''The light weight.'''
    FW_NORMAL = enum.auto()
    '''The normal weight.'''
    FW_REGULAR = enum.auto()
    '''The regular weight.'''
    FW_MEDIUM = enum.auto()
    '''The medium weight.'''
    FW_SEMIBOLD = enum.auto()
    '''The semibold weight.'''
    FW_DEMIBOLD = enum.auto()
    '''The demibold weight.'''
    FW_BOLD = enum.auto()
    '''The bold weight.'''
    FW_EXTRABOLD = enum.auto()
    '''The extrabold weight.'''
    FW_ULTRABOLD = enum.auto()
    '''The ultrabold weight.'''
    FW_BLACK = enum.auto()
    '''The black weight.'''
    FW_HEAVY = enum.auto()
    '''The heavy weight.'''

class EmfMapMode(enum.Enum):
    MM_TEXT = enum.auto()
    '''Each logical unit is mapped to one device pixel. Positive x is to the right; positive y is down.'''
    MM_LOMETRIC = enum.auto()
    '''Each logical unit is mapped to 0.1 millimeter. Positive x is to the right; positive y is up.'''
    MM_HIMETRIC = enum.auto()
    '''Each logical unit is mapped to 0.01 millimeter. Positive x is to the right; positive y is up.'''
    MM_LOENGLISH = enum.auto()
    '''Each logical unit is mapped to 0.01 inch. Positive x is to the right; positive y is up'''
    MM_HIENGLISH = enum.auto()
    '''Each logical unit is mapped to 0.001 inch. Positive x is to the right; positive y is up.'''
    MM_TWIPS = enum.auto()
    '''Each logical unit is mapped to one-twentieth of a printer\'s point
    (1/1440 inch, also called a "twip"). Positive x is to the right; positive y is up.'''
    MM_ISOTROPIC = enum.auto()
    '''Logical units are mapped to arbitrary units with equally scaled axes; that is, one unit
    along the x-axis is equal to one unit along the y-axis. The EMR_SETWINDOWEXTEX and
    EMR_SETVIEWPORTEXTEX records SHOULD be used to specify the units and the orientation
    of the axes.
    Adjustments MUST be made as necessary to ensure that the x and y units remain the same size.
    For example, when the window extent is set, the viewport MUST be adjusted to keep the units isotropic.'''
    MM_ANISOTROPIC = enum.auto()
    '''Logical units are mapped to arbitrary units with arbitrarily scaled axes.
    The EMR_SETWINDOWEXTEX and EMR_SETVIEWPORTEXTEX records SHOULD be used to specify the units,
    orientation, and scaling.'''

class EmfMetafileVersion(enum.Enum):
    META_FORMAT_ENHANCED = enum.auto()
    '''Specifies EMF metafile interoperability'''

class EmfMidLine(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any midline.'''
    PAN_NO_FIT = enum.auto()
    '''The No fit.'''
    PAN_MIDLINE_STANDARD_TRIMMED = enum.auto()
    '''Standard / trimmed.'''
    PAN_MIDLINE_STANDARD_POINTED = enum.auto()
    '''Standard / pointed.'''
    PAN_MIDLINE_STANDARD_SERIFED = enum.auto()
    '''Standard / serifed.'''
    PAN_MIDLINE_HIGH_TRIMMED = enum.auto()
    '''High / trimmed'''
    PAN_MIDLINE_HIGH_POINTED = enum.auto()
    '''High / pointed.'''
    PAN_MIDLINE_HIGH_SERIFED = enum.auto()
    '''High / serifed.'''
    PAN_MIDLINE_CONSTANT_TRIMMED = enum.auto()
    '''Constant / trimmed.'''
    PAN_MIDLINE_CONSTANT_POINTED = enum.auto()
    '''Constant / pointed'''
    PAN_MIDLINE_CONSTANT_SERIFED = enum.auto()
    '''Constant / serifed'''
    PAN_MIDLINE_LOW_TRIMMED = enum.auto()
    '''Low / trimmed.'''
    PAN_MIDLINE_LOW_POINTED = enum.auto()
    '''Low / pointed.'''
    PAN_MIDLINE_LOW_SERIFED = enum.auto()
    '''Low / serifed.'''

class EmfModifyWorldTransformMode(enum.Enum):
    MWT_IDENTITY = enum.auto()
    '''Reset the current transform using the identity matrix. In this mode, the specified transform data is ignored'''
    MWT_LEFTMULTIPLY = enum.auto()
    '''Multiply the current transform. In this mode, the specified transform data is the left multiplicand, and
    the transform that is currently defined in the playback device context is the right multiplicand'''
    MWT_RIGHTMULTIPLY = enum.auto()
    '''Multiply the current transform. In this mode, the specified transform data is the right multiplicand,
    and the transform that is currently defined in the playback device context is the left multiplicand'''
    MWT_SET = enum.auto()
    '''Perform the function of an EMR_SETWORLDTRANSFORM record (section 2.3.12.2).'''

class EmfPenStyle(enum.Enum):
    PS_COSMETIC = enum.auto()
    '''A pen type that specifies a line with a width of one logical unit and a style that is a solid color'''
    PS_ENDCAP_ROUND = enum.auto()
    '''A line cap that specifies round ends.'''
    PS_JOIN_ROUND = enum.auto()
    '''A line join that specifies round joins'''
    PS_SOLID = enum.auto()
    '''A line style that is a solid color'''
    PS_DASH = enum.auto()
    '''A line style that is dashed'''
    PS_DOT = enum.auto()
    '''A line style that is dotted.'''
    PS_DASHDOT = enum.auto()
    '''A line style that consists of alternating dashes and dots'''
    PS_DASHDOTDOT = enum.auto()
    '''A line style that consists of dashes and double dots.'''
    PS_NULL = enum.auto()
    '''A line style that is invisible.'''
    PS_INSIDEFRAME = enum.auto()
    '''A line style that is a solid color. When this style is specified in a drawing record
    that takes a bounding rectangle, the dimensions of the figure are shrunk so that
    it fits entirely in the bounding rectangle, taking into account the width of the pen.'''
    PS_USERSTYLE = enum.auto()
    '''A line style that is defined by a styling array, which specifies the lengths of dashes and gaps in the line'''
    PS_ALTERNATE = enum.auto()
    '''A line style in which every other pixel is set. This style is applicable only to a pen type of PS_COSMETIC'''
    PS_ENDCAP_SQUARE = enum.auto()
    '''A line cap that specifies square ends.'''
    PS_ENDCAP_FLAT = enum.auto()
    '''A line cap that specifies flat ends.'''
    PS_JOIN_BEVEL = enum.auto()
    '''A line join that specifies beveled joins.'''
    PS_JOIN_MITER = enum.auto()
    '''A line join that specifies mitered joins when the lengths of the joins are within the current miter
    length limit that is set in the playback device context.
    If the lengths of the joins exceed the miter limit, beveled joins are specified'''
    PS_GEOMETRIC = enum.auto()
    '''A pen type that specifies a line with a width that is measured in logical units
    and a style that can contain any of the attributes of a brush.'''
    STYLE_MASK = enum.auto()
    '''The style mask'''
    END_CAP_MASK = enum.auto()
    '''The end cap mask'''
    JOIN_MASK = enum.auto()
    '''The join mask'''
    TYPE_MASK = enum.auto()
    '''The type mask'''

class EmfPointEnum(enum.Enum):
    CLOSEFIGURE = enum.auto()
    '''A PT_LINETO or PT_BEZIERTO type can be combined with this value by using the bitwise
    operator OR to indicate that the corresponding point is the last point in a figure
    and the figure is closed'''
    LINETO = enum.auto()
    '''Specifies that a line is to be drawn from the current position to this point,
    which then becomes the new current position'''
    BEZIERTO = enum.auto()
    '''Specifies that this point is a control point or ending point for a Bezier curve.'''
    MOVETO = enum.auto()
    '''Specifies that this point starts a disjoint figure. This point becomes the new current position.'''

class EmfPolygonFillMode(enum.Enum):
    ALTERNATE = enum.auto()
    '''Selects alternate mode (fills the area between odd-numbered and even-numbered polygon sides on each scan line).'''
    WINDING = enum.auto()
    '''Selects winding mode (fills any region with a nonzero winding value).'''

class EmfProportion(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any proportion.'''
    PAN_NO_FIT = enum.auto()
    '''The No fit.'''
    PAN_PROP_OLD_STYLE = enum.auto()
    '''Old style.'''
    PAN_PROP_MODERN = enum.auto()
    '''The modern'''
    PAN_PROP_EVEN_WIDTH = enum.auto()
    '''The even width'''
    PAN_PROP_EXPANDED = enum.auto()
    '''The expanded'''
    PAN_PROP_CONDENSED = enum.auto()
    '''The condensed'''
    PAN_PROP_VERY_EXPANDED = enum.auto()
    '''The very expanded'''
    PAN_PROP_VERY_CONDENSED = enum.auto()
    '''The very condensed'''
    PAN_PROP_MONOSPACED = enum.auto()
    '''The mono spaced'''

class EmfRecordType(enum.Enum):
    EMR_HEADER = enum.auto()
    '''This record defines the start of the metafile and specifies its characteristics; its contents,
    including the dimensions of the embedded image; the number of records in the metafile; and the
    resolution of the device on which the embedded image was created. These values make it possible for the metafile to be device-independent.'''
    EMR_POLYBEZIER = enum.auto()
    '''This record defines one or more Bezier curves. Cubic Bezier curves are defined using
    specified endpoints and control points, and are stroked with the current pen.'''
    EMR_POLYGON = enum.auto()
    '''This record defines a polygon consisting of two or more vertexes connected by straight
    lines. The polygon is outlined by using the current pen and filled by using the current brush
    and polygon fill mode. The polygon is closed automatically by drawing a line from the last vertex to the first.'''
    EMR_POLYLINE = enum.auto()
    '''This record defines a series of line segments by connecting the points in the specified
    array.'''
    EMR_POLYBEZIERTO = enum.auto()
    '''This record defines one or more Bezier curves based upon the current position.'''
    EMR_POLYLINETO = enum.auto()
    '''This record defines one or more straight lines based upon the current position.
    A line is drawn from the current position to the first point specified by the points field
    by using the current pen. For each additional line, drawing is performed from the ending
    point of the previous line to the next point specified by points.'''
    EMR_POLYPOLYLINE = enum.auto()
    '''This record defines multiple series of connected line segments. The line segments are
    drawn by using the current pen. The figures formed by the segments are not filled. T
    he current position is neither used nor updated by this record.'''
    EMR_POLYPOLYGON = enum.auto()
    '''This record defines a series of closed polygons. Each polygon is outlined by using the
    current pen and filled by using the current brush and polygon fill mode. The polygons defined by this record can overlap.'''
    EMR_SETWINDOWEXTEX = enum.auto()
    '''This record defines the window extent.'''
    EMR_SETWINDOWORGEX = enum.auto()
    '''This record defines the window origin.'''
    EMR_SETVIEWPORTEXTEX = enum.auto()
    '''This record defines the viewport extent.'''
    EMR_SETVIEWPORTORGEX = enum.auto()
    '''This record defines the viewport origin.'''
    EMR_SETBRUSHORGEX = enum.auto()
    '''This record defines the origin of the current brush.'''
    EMR_EOF = enum.auto()
    '''This record indicates the end of the metafile.'''
    EMR_SETPIXELV = enum.auto()
    '''This record defines the color of the pixel at the specified logical coordinates.'''
    EMR_SETMAPPERFLAGS = enum.auto()
    '''This record specifies parameters of the process of matching logical fonts to physical
    fonts, which is performed by the font mapper.'''
    EMR_SETMAPMODE = enum.auto()
    '''This record defines the mapping mode of the playback device context. The mapping mode
    defines the unit of measure used to transform page space units into device space units,
    and also defines the orientation of the device\'s x-axis and y-axis.'''
    EMR_SETBKMODE = enum.auto()
    '''This record defines the background mix mode of the playback device context. The background mix
    mode is used with text, hatched brushes, and pen styles that are not solid lines.'''
    EMR_SETPOLYFILLMODE = enum.auto()
    '''This record defines polygon fill mode.'''
    EMR_SETROP2 = enum.auto()
    '''This record defines binary raster operation mode.'''
    EMR_SETSTRETCHBLTMODE = enum.auto()
    '''This record defines bitmap stretch mode.'''
    EMR_SETTEXTALIGN = enum.auto()
    '''This record defines text alignment.'''
    EMR_SETCOLORADJUSTMENT = enum.auto()
    '''This record defines the color adjustment values for the playback device context using the specified values.'''
    EMR_SETTEXTCOLOR = enum.auto()
    '''This record defines the current text color.'''
    EMR_SETBKCOLOR = enum.auto()
    '''This record defines the background color.'''
    EMR_OFFSETCLIPRGN = enum.auto()
    '''This record redefines the clipping region of the playback device context by the specified offsets.'''
    EMR_MOVETOEX = enum.auto()
    '''This record defines coordinates of the new current position, in logical units.'''
    EMR_SETMETARGN = enum.auto()
    '''This record intersects the current clipping region for the playback device context with the
    current meta region and saves the combined region as the new meta region. The clipping region is reset to a null region.'''
    EMR_EXCLUDECLIPRECT = enum.auto()
    '''This record defines a new clipping region that consists of the existing clipping region
    minus the specified rectangle.'''
    EMR_INTERSECTCLIPRECT = enum.auto()
    '''This record defines a new clipping region from the intersection of the current clipping
    region and the specified rectangle.'''
    EMR_SCALEVIEWPORTEXTEX = enum.auto()
    '''This record redefines the viewport for the playback device context using the ratios
    formed by the specified multiplicands and divisors.'''
    EMR_SCALEWINDOWEXTEX = enum.auto()
    '''This record redefines the window for the playback device context using the ratios formed
    by the specified multiplicands and divisors.'''
    EMR_SAVEDC = enum.auto()
    '''This record saves the current state of the playback device context by copying data
    describing selected objects and graphic modes—including the bitmap, brush, palette,
    font, pen, region, drawing mode, and mapping mode—to a stack of saved device contexts.'''
    EMR_RESTOREDC = enum.auto()
    '''This record restores the playback device context to the specified saved state.
    The playback device context is restored by popping state information off a stack of
    saved device contexts created by earlier EMR_SAVEDC (section 2.3.11) records.'''
    EMR_SETWORLDTRANSFORM = enum.auto()
    '''This record defines a two-dimensional linear transformation between world space and
    page space (for more information, see [MSDN-WRLDPGSPC]) for the playback device context.
    This transformation can be used to scale, rotate, shear, or translate graphics output.'''
    EMR_MODIFYWORLDTRANSFORM = enum.auto()
    '''This record redefines the world transformation for the playback device context using the specified mode.'''
    EMR_SELECTOBJECT = enum.auto()
    '''This record adds an object to the playback device context, identifying it by its
    index in the EMF Object Table (section 3.1.1.1).'''
    EMR_CREATEPEN = enum.auto()
    '''This record defines a logical pen that has the specified style, width, and color.
    The pen can subsequently be selected into the playback device context and used to draw lines and curves.'''
    EMR_CREATEBRUSHINDIRECT = enum.auto()
    '''This record defines a logical brush for figure filling in graphics operations.'''
    EMR_DELETEOBJECT = enum.auto()
    '''This record deletes a graphics object, clearing its index in the EMF Object Table.
    If the deleted object is selected in the playback device context, the default object
    for that context property MUST be restored.'''
    EMR_ANGLEARC = enum.auto()
    '''This record defines a line segment of an arc. The line segment is drawn from the
    current position to the beginning of the arc. The arc is drawn along the perimeter
    of a circle with the given radius and center. The length of the arc is defined by
    the given start and sweep angles.'''
    EMR_ELLIPSE = enum.auto()
    '''This record defines an ellipse. The center of the ellipse is the center of the
    specified bounding rectangle. The ellipse is outlined by using the current pen and
    is filled by using the current brush.'''
    EMR_RECTANGLE = enum.auto()
    '''This record defines a rectangle. The rectangle is outlined by using the current
    pen and filled by using the current brush.'''
    EMR_ROUNDRECT = enum.auto()
    '''This record defines a rectangle with rounded corners. The rectangle is outlined
    by using the current pen and filled by using the current brush.'''
    EMR_ARC = enum.auto()
    '''This record defines an elliptical arc.'''
    EMR_CHORD = enum.auto()
    '''This record defines a chord (a region bounded by the intersection of an ellipse
    and a line segment, called a secant). The chord is outlined by using the current
    pen and filled by using the current brush.'''
    EMR_PIE = enum.auto()
    '''This record defines a pie-shaped wedge bounded by the intersection of an ellipse
    and two radials. The pie is outlined by using the current pen and filled by using
    the current brush.'''
    EMR_SELECTPALETTE = enum.auto()
    '''This record adds a LogPalette (section 2.2.17) object to the playback device
    context, identifying it by its index in the EMF Object Table.'''
    EMR_CREATEPALETTE = enum.auto()
    '''This record defines a LogPalette object.'''
    EMR_SETPALETTEENTRIES = enum.auto()
    '''This record defines RGB (red-green-blue) color values in a range of entries
    in a LogPalette object.'''
    EMR_RESIZEPALETTE = enum.auto()
    '''This record increases or decreases the size of a logical palette.'''
    EMR_REALIZEPALETTE = enum.auto()
    '''This record maps entries from the current logical palette to the system palette.'''
    EMR_EXTFLOODFILL = enum.auto()
    '''This record fills an area of the display surface with the current brush.'''
    EMR_LINETO = enum.auto()
    '''This record defines a line from the current position up to, but not including,
    the specified point. It resets the current position to the specified point.'''
    EMR_ARCTO = enum.auto()
    '''This record defines an elliptical arc. It resets the current position to the
    end point of the arc.'''
    EMR_POLYDRAW = enum.auto()
    '''This record defines a set of line segments and Bezier curves.'''
    EMR_SETARCDIRECTION = enum.auto()
    '''This record defines the drawing direction to be used for arc and rectangle
    operations.'''
    EMR_SETMITERLIMIT = enum.auto()
    '''This record defines the limit for the length of miter joins for the playback
    device context.'''
    EMR_BEGINPATH = enum.auto()
    '''This record opens a path bracket in the playback device context.'''
    EMR_ENDPATH = enum.auto()
    '''This record closes a path bracket and selects the path defined by the bracket
    into the playback device context.'''
    EMR_CLOSEFIGURE = enum.auto()
    '''This record closes an open figure in a path.'''
    EMR_FILLPATH = enum.auto()
    '''This record closes any open figures in the current path and fills the path\'s interior
    by using the current brush and polygon-filling mode.'''
    EMR_STROKEANDFILLPATH = enum.auto()
    '''This record closes any open figures in a path, strokes the outline of the path by
    using the current pen, and fills its interior by using the current brush.'''
    EMR_STROKEPATH = enum.auto()
    '''This record renders the specified path by using the current pen.'''
    EMR_FLATTENPATH = enum.auto()
    '''This record transforms any curve in the path that is selected into the playback device
    context, turning each curve into a sequence of lines.'''
    EMR_WIDENPATH = enum.auto()
    '''This record redefines the current path as the area that would be painted if the path
    were stroked using the pen currently selected into the playback device context.'''
    EMR_SELECTCLIPPATH = enum.auto()
    '''This record defines the current path as a clipping region for the playback device
    context, combining the new region with any existing clipping region using the specified mode.'''
    EMR_ABORTPATH = enum.auto()
    '''This record aborts a path bracket or discards the path from a closed path bracket.'''
    EMR_COMMENT = enum.auto()
    '''This record specifies arbitrary private data.'''
    EMR_FILLRGN = enum.auto()
    '''This record fills the specified region by using the specified brush.'''
    EMR_FRAMERGN = enum.auto()
    '''This record draws a border around the specified region using the specified brush.'''
    EMR_INVERTRGN = enum.auto()
    '''This record inverts the colors in the specified region.'''
    EMR_PAINTRGN = enum.auto()
    '''This record paints the specified region by using the brush currently selected into
    the playback device context.'''
    EMR_EXTSELECTCLIPRGN = enum.auto()
    '''This record combines the specified region with the current clip region using the
    specified mode.'''
    EMR_BITBLT = enum.auto()
    '''This record specifies a block transfer of pixels from a source bitmap to a destination
    rectangle, optionally in combination with a brush pattern, according to a specified raster operation.'''
    EMR_STRETCHBLT = enum.auto()
    '''This record specifies a block transfer of pixels from a source bitmap to a destination
    rectangle, optionally in combination with a brush pattern, according to a specified raster
    operation, stretching or compressing the output to fit the dimensions of the destination, if necessary.'''
    EMR_MASKBLT = enum.auto()
    '''This record specifies a block transfer of pixels from a source bitmap to a destination
    rectangle, optionally in combination with a brush pattern and with the application of a
    color mask bitmap, according to specified foreground and background raster operations.'''
    EMR_PLGBLT = enum.auto()
    '''This record specifies a block transfer of pixels from a source bitmap to a destination
    parallelogram, with the application of a color mask bitmap.'''
    EMR_SETDIBITSTODEVICE = enum.auto()
    '''This record specifies a block transfer of pixels from specified scan lines of a source
    bitmap to a destination rectangle.'''
    EMR_STRETCHDIBITS = enum.auto()
    '''This record specifies a block transfer of pixels from a source bitmap to a destination
    rectangle, optionally in combination with a brush pattern, according to a specified raster operation,
    stretching or compressing the output to fit the dimensions of the destination, if necessary.'''
    EMR_EXTCREATEFONTINDIRECTW = enum.auto()
    '''This record defines a logical font that has the specified characteristics. The font
    can subsequently be selected as the current font for the playback device context.'''
    EMR_EXTTEXTOUTA = enum.auto()
    '''This record draws an ASCII text string using the current font and text colors.Note
    EMR_EXTTEXTOUTA SHOULD be emulated with an EMR_EXTTEXTOUTW record (section 2.3.5.8).
    This requires the ASCII text string in the EmrText object to be converted to Unicode UTF16-LE encoding.'''
    EMR_EXTTEXTOUTW = enum.auto()
    '''This record draws a Unicode text string using the current font and text colors.'''
    EMR_POLYBEZIER16 = enum.auto()
    '''This record defines one or more Bezier curves. The curves are drawn using the current pen.'''
    EMR_POLYGON16 = enum.auto()
    '''This record defines a polygon consisting of two or more vertexes connected by straight lines.
    The polygon is outlined by using the current pen and filled by using the current brush and polygon
    fill mode. The polygon is closed automatically by drawing a line from the last vertex to the first.'''
    EMR_POLYLINE16 = enum.auto()
    '''This record defines a series of line segments by connecting the points in the specified array.'''
    EMR_POLYBEZIERTO16 = enum.auto()
    '''This record defines one or more Bezier curves based on the current position.'''
    EMR_POLYLINETO16 = enum.auto()
    '''This record defines one or more straight lines based upon the current position.
    A line is drawn from the current position to the first point specified by the Points
    field by using the current pen. For each additional line, drawing is performed from the
    ending point of the previous line to the next point specified by Points.'''
    EMR_POLYPOLYLINE16 = enum.auto()
    '''This record defines multiple series of connected line segments.'''
    EMR_POLYPOLYGON16 = enum.auto()
    '''This record defines a series of closed polygons. Each polygon is outlined by using
    the current pen and filled by using the current brush and polygon fill mode. The polygons
    specified by this record can overlap.'''
    EMR_POLYDRAW16 = enum.auto()
    '''This record defines a set of line segments and Bezier curves.'''
    EMR_CREATEMONOBRUSH = enum.auto()
    '''This record defines a logical brush with the specified bitmap pattern. The bitmap can
    be a device-independent bitmap (DIB) section bitmap or it can be a device-dependent bitmap.'''
    EMR_CREATEDIBPATTERNBRUSHPT = enum.auto()
    '''This record defines a logical brush that has the pattern specified by the DIB.'''
    EMR_EXTCREATEPEN = enum.auto()
    '''This record defines a logical cosmetic or geometric pen that has the specified style,
    width, and brush attributes.'''
    EMR_POLYTEXTOUTA = enum.auto()
    '''This record draws one or more ASCII text strings using the current font and text colors.
    Note EMR_POLYTEXTOUTA SHOULD be emulated with a series of EMR_EXTTEXTOUTW records, one per string'''
    EMR_POLYTEXTOUTW = enum.auto()
    '''This record draws one or more Unicode text strings using the current font and text colors.
    Note EMR_POLYTEXTOUTW SHOULD be emulated with a series of EMR_EXTTEXTOUTW records, one per string'''
    EMR_SETICMMODE = enum.auto()
    '''This record specifies the mode of Image Color Management (ICM) for graphics operations.'''
    EMR_CREATECOLORSPACE = enum.auto()
    '''This record creates a logical color space object from a color profile with a name consisting of ASCII characters'''
    EMR_SETCOLORSPACE = enum.auto()
    '''This record defines the current logical color space object for graphics operations.'''
    EMR_DELETECOLORSPACE = enum.auto()
    '''This record deletes a logical color space object. Note An EMR_DELETEOBJECT record SHOULD be
    used instead of EMR_DELETECOLORSPACE to delete a logical color space object'''
    EMR_GLSRECORD = enum.auto()
    '''This record specifies an OpenGL function.'''
    EMR_GLSBOUNDEDRECORD = enum.auto()
    '''This record specifies an OpenGL function with a bounding rectangle for output.'''
    EMR_PIXELFORMAT = enum.auto()
    '''This record specifies the pixel format to use for graphics operations'''
    EMR_DRAWESCAPE = enum.auto()
    '''This record passes arbitrary information to the driver. The intent is that the information
    will result in drawing being done.'''
    EMR_EXTESCAPE = enum.auto()
    '''This record passes arbitrary information to the driver. The intent is that the information
    will not result in drawing being done.'''
    EMR_SMALLTEXTOUT = enum.auto()
    '''This record outputs a string.'''
    EMR_FORCEUFIMAPPING = enum.auto()
    '''This record forces the font mapper to match fonts based on their UniversalFontId in
    preference to their LogFont information.'''
    EMR_NAMEDESCAPE = enum.auto()
    '''This record passes arbitrary information to the given named driver.'''
    EMR_COLORCORRECTPALETTE = enum.auto()
    '''This record specifies how to correct the entries of a logical palette object using Windows
    Color System (WCS) 1.0 values'''
    EMR_SETICMPROFILEA = enum.auto()
    '''This record specifies a color profile in a file with a name consisting of ASCII characters,
    for graphics output.'''
    EMR_SETICMPROFILEW = enum.auto()
    '''This record specifies a color profile in a file with a name consisting of Unicode characters,
    for graphics output'''
    EMR_ALPHABLEND = enum.auto()
    '''This record specifies a block transfer of pixels from a source bitmap to a destination rectangle,
    including alpha transparency data, according to a specified blending operation.'''
    EMR_SETLAYOUT = enum.auto()
    '''This record specifies the order in which text and graphics are drawn'''
    EMR_TRANSPARENTBLT = enum.auto()
    '''This record specifies a block transfer of pixels from a source bitmap to a destination rectangle,
    treating a specified color as transparent, stretching or compressing the output to fit the dimensions of the destination, if necessary'''
    EMR_GRADIENTFILL = enum.auto()
    '''This record specifies filling rectangles or triangles with gradients of color'''
    EMR_SETLINKEDUFIS = enum.auto()
    '''This record sets the UniversalFontIds of linked fonts to use during character lookup.'''
    EMR_SETTEXTJUSTIFICATION = enum.auto()
    '''This record specifies the amount of extra space to add to break characters for justification
    purposes.'''
    EMR_COLORMATCHTOTARGETW = enum.auto()
    '''This record specifies whether to perform color matching with a color profile that is specified in a file with a name consisting of Unicode characters.'''
    EMR_CREATECOLORSPACEW = enum.auto()
    '''This record creates a logical color space object from a color profile with a name consisting of Unicode characters'''

class EmfRegionMode(enum.Enum):
    RGN_AND = enum.auto()
    '''The new clipping region includes the intersection (overlapping areas) of the current clipping region and the current path (or new region).'''
    RGN_OR = enum.auto()
    '''The new clipping region includes the union (combined areas) of the current clipping region and the current path (or new region).'''
    RGN_XOR = enum.auto()
    '''The new clipping region includes the union of the current clipping region and the current path (or new region) but without the overlapping areas'''
    RGN_DIFF = enum.auto()
    '''The new clipping region includes the areas of the current clipping region with those of the current path (or new region) excluded.'''
    RGN_COPY = enum.auto()
    '''The new clipping region is the current path (or the new region).'''

class EmfSerifStyle(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any Style.'''
    PAN_NO_FIT = enum.auto()
    '''The No fit Style.'''
    PAN_SERIF_COVE = enum.auto()
    '''The Cove Style.'''
    PAN_SERIF_OBTUSE_COVE = enum.auto()
    '''The Obtuse cove Style.'''
    PAN_SERIF_SQUARE_COVE = enum.auto()
    '''The Square cove Style.'''
    PAN_SERIF_OBTUSE_SQUARE_COVE = enum.auto()
    '''The Obtuse square cove Style.'''
    PAN_SERIF_SQUARE = enum.auto()
    '''The Square Style.'''
    PAN_SERIF_THIN = enum.auto()
    '''The Thin Style.'''
    PAN_SERIF_BONE = enum.auto()
    '''The Bone Style.'''
    PAN_SERIF_EXAGGERATED = enum.auto()
    '''The Exaggerated Style.'''
    PAN_SERIF_TRIANGLE = enum.auto()
    '''The Triangle Style.'''
    PAN_SERIF_NORMAL_SANS = enum.auto()
    '''The Normal sans Style.'''
    PAN_SERIF_OBTUSE_SANS = enum.auto()
    '''The Obtuse sans Style.'''
    PAN_SERIF_PERP_SANS = enum.auto()
    '''The Perp sans Style.'''
    PAN_SERIF_FLARED = enum.auto()
    '''The Flared Style.'''
    PAN_SERIF_ROUNDED = enum.auto()
    '''The Rounded Style.'''

class EmfSerifType(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any type.'''
    PAN_NO_FIT = enum.auto()
    '''The No fit Type.'''
    PAN_SERIF_COVE = enum.auto()
    '''The The cove Type.'''
    PAN_SERIF_OBTUSE_COVE = enum.auto()
    '''The Obtuse cove Type.'''
    PAN_SERIF_SQUARE_COVE = enum.auto()
    '''The Obtuse cove Type.'''
    PAN_SERIF_OBTUSE_SQUARE_COVE = enum.auto()
    '''The Obtuse square cove Type.'''
    PAN_SERIF_SQUARE = enum.auto()
    '''The The Square Type.'''
    PAN_SERIF_THIN = enum.auto()
    '''The The thin Type.'''
    PAN_SERIF_BONE = enum.auto()
    '''The The bone Type.'''
    PAN_SERIF_EXAGGERATED = enum.auto()
    '''The The exaggerated Type.'''
    PAN_SERIF_TRIANGLE = enum.auto()
    '''The The triangle Type.'''
    PAN_SERIF_NORMAL_SANS = enum.auto()
    '''The Normal sans Type.'''
    PAN_SERIF_OBTUSE_SANS = enum.auto()
    '''The Obtuse sans Type.'''
    PAN_SERIF_PERP_SANS = enum.auto()
    '''The Perp sans Type.'''
    PAN_SERIF_FLARED = enum.auto()
    '''The The Flared Type.'''
    PAN_SERIF_ROUNDED = enum.auto()
    '''The The Rounded Type.'''

class EmfStockObject(enum.Enum):
    WHITE_BRUSH = enum.auto()
    '''A white, solid-color brush that is equivalent to a logical brush
    (LogBrushEx object, section 2.2.12) with the following properties:
    BrushStyle: BS_SOLID (WMF BrushStyle enumeration, [MS-WMF] section 2.1.1.4)
    Color: 0x00FFFFFF (WMF ColorRef object, [MS-WMF] section 2.2.2.8)'''
    LTGRAY_BRUSH = enum.auto()
    '''A light gray, solid-color brush that is equivalent to a logical brush with the following properties:
    BrushStyle: BS_SOLID
    Color: 0x00C0C0C0'''
    GRAY_BRUSH = enum.auto()
    '''A gray, solid-color brush that is equivalent to a logical brush with the following properties:
    BrushStyle: BS_SOLID
    Color: 0x00808080'''
    DKGRAY_BRUSH = enum.auto()
    '''A dark gray, solid color brush that is equivalent to a logical brush with the following properties:
    BrushStyle: BS_SOLID
    Color: 0x00404040'''
    BLACK_BRUSH = enum.auto()
    '''A black, solid color brush that is equivalent to a logical brush with the following properties:
    BrushStyle: BS_SOLID
    Color: 0x00000000'''
    NULL_BRUSH = enum.auto()
    '''A null brush that is equivalent to a logical brush with the following properties:
    BrushStyle: BS_NULL'''
    WHITE_PEN = enum.auto()
    '''A white, solid-color pen that is equivalent to a logical pen (LogPen object, section 2.2.19)
    with the following properties:
    PenStyle: PS_COSMETIC + PS_SOLID (PenStyle enumeration, section 2.1.25)
    ColorRef: 0x00FFFFFF (WMF ColorRef object).'''
    BLACK_PEN = enum.auto()
    '''A black, solid-color pen that is equivalent to a logical pen with the following properties:
    PenStyle: PS_COSMETIC + PS_SOLID
    ColorRef: 0x00000000'''
    NULL_PEN = enum.auto()
    '''A null pen that is equivalent to a logical pen with the following properties:
    PenStyle: PS_NULL'''
    OEM_FIXED_FONT = enum.auto()
    '''A fixed-width, OEM character set font that is equivalent to a logical font
    (LogFont object, section 2.2.13) with the following properties:
    Charset: OEM_CHARSET (WMF CharacterSet enumeration, [MS-WMF] section 2.1.1.5)
    PitchAndFamily: FF_DONTCARE (WMF FamilyFont enumeration, [MS-WMF] section 2.1.1.8)
    + FIXED_PITCH (WMF PitchFont enumeration, [MS-WMF] section 2.1.1.24)'''
    ANSI_FIXED_FONT = enum.auto()
    '''A fixed-width font that is equivalent to a logical font with the following properties:
    Charset: ANSI_CHARSET
    PitchAndFamily: FF_DONTCARE + FIXED_PITCH'''
    ANSI_VAR_FONT = enum.auto()
    '''A variable-width font that is equivalent to a logical font with the following properties:
    Charset: ANSI_CHARSET
    PitchAndFamily: FF_DONTCARE + VARIABLE_PITCH'''
    SYSTEM_FONT = enum.auto()
    '''A font that is guaranteed to be available in the operating system.
    The actual font that is specified by this value is implementation-dependent'''
    DEVICE_DEFAULT_FONT = enum.auto()
    '''The default font that is provided by the graphics device driver for the current output device.
    The actual font that is specified by this value is implementation-dependent'''
    DEFAULT_PALETTE = enum.auto()
    '''The default palette that is defined for the current output device.
    The actual palette that is specified by this value is implementation-dependent'''
    SYSTEM_FIXED_FONT = enum.auto()
    '''A fixed-width font that is guaranteed to be available in the operating system.
    The actual font that is specified by this value is implementation-dependent'''
    DEFAULT_GUI_FONT = enum.auto()
    '''A fixed-width font that is guaranteed to be available in the operating system.
    The actual font that is specified by this value is implementation-dependent'''
    DC_BRUSH = enum.auto()
    '''The solid-color brush that is currently selected in the playback device context'''
    DC_PEN = enum.auto()
    '''The solid-color pen that is currently selected in the playback device context'''

class EmfStretchMode(enum.Enum):
    STRETCH_ANDSCANS = enum.auto()
    '''Performs a Boolean AND operation using the color values for the eliminated and existing pixels.
    If the bitmap is a monochrome bitmap, this mode preserves black pixels at the expense of white pixels'''
    STRETCH_ORSCANS = enum.auto()
    '''Performs a Boolean OR operation using the color values for the eliminated and existing pixels.
    If the bitmap is a monochrome bitmap, this mode preserves white pixels at the expense of black pixels.'''
    STRETCH_DELETESCANS = enum.auto()
    '''Deletes the pixels. This mode deletes all eliminated lines of pixels without trying to preserve their information.'''
    STRETCH_HALFTONE = enum.auto()
    '''Maps pixels from the source rectangle into blocks of pixels in the destination rectangle.
    The average color over the destination block of pixels approximates the color of the source pixels.'''

class EmfStrokeVariation(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any Stroke.'''
    PAN_NO_FIT = enum.auto()
    '''The No fit.'''
    PAN_STROKE_GRADUAL_DIAG = enum.auto()
    '''Gradual / diagonal'''
    PAN_STROKE_GRADUAL_TRAN = enum.auto()
    '''Gradual transitional'''
    PAN_STROKE_GRADUAL_VERT = enum.auto()
    '''Gradual vertical'''
    PAN_STROKE_GRADUAL_HORZ = enum.auto()
    '''Gradual horizontal'''
    PAN_STROKE_RAPID_VERT = enum.auto()
    '''Rapid vertical'''
    PAN_STROKE_RAPID_HORZ = enum.auto()
    '''Rapid horizontal'''
    PAN_STROKE_INSTANT_VERT = enum.auto()
    '''Instant vertical'''

class EmfWeight(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any weight.'''
    PAN_NO_FIT = enum.auto()
    '''The No fit.'''
    PAN_WEIGHT_VERY_LIGHT = enum.auto()
    '''Very light weight.'''
    PAN_WEIGHT_LIGHT = enum.auto()
    '''The light weight.'''
    PAN_WEIGHT_THIN = enum.auto()
    '''The thin weight.'''
    PAN_WEIGHT_BOOK = enum.auto()
    '''The book weight.'''
    PAN_WEIGHT_MEDIUM = enum.auto()
    '''The medium weight.'''
    PAN_WEIGHT_DEMI = enum.auto()
    '''The demi weight.'''
    PAN_WEIGHT_BOLD = enum.auto()
    '''The bold weight.'''
    PAN_WEIGHT_HEAVY = enum.auto()
    '''The heavy weight.'''
    PAN_WEIGHT_BLACK = enum.auto()
    '''The black weight.'''
    PAN_WEIGHT_NORD = enum.auto()
    '''The nord weight.'''

class EmfXHeight(enum.Enum):
    PAN_ANY = enum.auto()
    '''The Any height.'''
    PAN_NO_FIT = enum.auto()
    '''The No fit.'''
    PAN_XHEIGHT_CONSTANT_SMALL = enum.auto()
    '''Constant/small'''
    PAN_XHEIGHT_CONSTANT_STD = enum.auto()
    '''Constant/standard'''
    PAN_XHEIGHT_CONSTANT_LARGE = enum.auto()
    '''Constant/large'''
    PAN_XHEIGHT_DUCKING_SMALL = enum.auto()
    '''Ducking/small'''
    PAN_XHEIGHT_DUCKING_STD = enum.auto()
    '''Ducking/standard'''
    PAN_XHEIGHT_DUCKING_LARGE = enum.auto()
    '''Ducking/large'''

