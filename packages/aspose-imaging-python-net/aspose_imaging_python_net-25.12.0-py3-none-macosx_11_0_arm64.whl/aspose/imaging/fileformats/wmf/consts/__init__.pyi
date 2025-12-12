"""The namespace contains types [MS-WMF]: Windows Metafile Format
                2.1 WMF Constants"""
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

class StretchMode(enum.Enum):
    BLACK_ON_WHITE = enum.auto()
    '''Performs a Boolean AND operation by using the color values for the
    eliminated and existing pixels. If the bitmap is a monochrome
    bitmap, this mode preserves black pixels at the expense of white
    pixels'''
    WHITE_ON_BLACK = enum.auto()
    '''Performs a Boolean OR operation by using the color values for the
    eliminated and existing pixels. If the bitmap is a monochrome
    bitmap, this mode preserves white pixels at the expense of black
    pixels'''
    COLOR_ON_COLOR = enum.auto()
    '''Deletes the pixels. This mode deletes all eliminated lines of pixels
    without trying to preserve their information.'''
    HALF_TONE = enum.auto()
    '''Maps pixels from the source rectangle into blocks of pixels in the
    destination rectangle. The average color over the destination block
    of pixels approximates the color of the source pixels.'''

class WmfBinaryRasterOperation(enum.Enum):
    BLACK = enum.auto()
    '''0, Pixel is always 0.'''
    NOTMERGEPEN = enum.auto()
    '''DPon, Pixel is the inverse of the MERGEPEN color'''
    MASKNOTPEN = enum.auto()
    '''DPna, Pixel is a combination of the screen color and the inverse of the pen color.'''
    NOTCOPYPEN = enum.auto()
    '''Pn, Pixel is the inverse of the pen color.'''
    MASKPENNOT = enum.auto()
    '''PDna, Pixel is a combination of the colors common to both the pen and the
    inverse of the screen.'''
    NOT = enum.auto()
    '''Dn, Pixel is the inverse of the screen color.'''
    XORPEN = enum.auto()
    '''DPx, Pixel is a combination of the colors in the pen or in the screen, but not in both.'''
    NOTMASKPEN = enum.auto()
    '''DPan, Pixel is the inverse of the MASKPEN color.'''
    MASKPEN = enum.auto()
    '''DPa, Pixel is a combination of the colors common to both the pen and the screen.'''
    NOTXORPEN = enum.auto()
    '''DPxn, Pixel is the inverse of the XORPEN color.'''
    NOP = enum.auto()
    '''D, Pixel remains unchanged.'''
    MERGENOTPEN = enum.auto()
    '''DPno, Pixel is a combination of the colors common to both the screen and
    the inverse of the pen.'''
    COPYPEN = enum.auto()
    '''P, Pixel is the pen color.'''
    MERGEPENNOT = enum.auto()
    '''PDno, Pixel is a combination of the pen color and the inverse of the
    screen color.'''
    MERGEPEN = enum.auto()
    '''DPo, Pixel is a combination of the pen color and the screen color.'''
    WHITE = enum.auto()
    '''1, Pixel is always 1'''

class WmfBrushStyle(enum.Enum):
    SOLID = enum.auto()
    '''A brush that paints a single, constant color, either solid or dithered.'''
    NULL = enum.auto()
    '''A brush that does nothing. Using a NULL brush in a graphics operation
    MUST have the same effect as using no brush at all'''
    HATCHED = enum.auto()
    '''A brush that paints a predefined simple pattern, or "hatch", onto a solid background'''
    PATTERN = enum.auto()
    '''A brush that paints a pattern defined by a bitmap, which MAY be a Bitmap16 Object
    or a DeviceIndependentBitmap (DIB) Object.'''
    INDEXED = enum.auto()
    '''Not supported.'''
    DIBPATTERN = enum.auto()
    '''A pattern brush specified by a DIB.'''
    DIBPATTERNPT = enum.auto()
    '''A pattern brush specified by a DIB.'''
    PATTERN_8X8 = enum.auto()
    '''Not supported.'''
    DIBPATTERN_8X8 = enum.auto()
    '''Not supported.'''
    MONOPATTERN = enum.auto()
    '''Not supported.'''
    GRADIENT = enum.auto()
    '''The gradient
    Not suppoted in wmf, support in odg.'''

class WmfCharacterSet(enum.Enum):
    ANSI = enum.auto()
    '''Specifies the English character set.'''
    DEFAULT = enum.auto()
    '''Specifies a character set based on the current system locale; for
    example, when the system locale is United States English, the default character set is
    ANSI_CHARSET.'''
    SYMBOL = enum.auto()
    '''Specifies a character set of symbols.'''
    MAC = enum.auto()
    '''Specifies the Apple Macintosh character set.'''
    SHIFTJIS = enum.auto()
    '''Specifies the Japanese character set.'''
    HANGUL = enum.auto()
    '''Also spelled "Hangeul". Specifies the Hangul Korean character set.'''
    JOHAB = enum.auto()
    '''Also spelled "Johap". Specifies the Johab Korean character set.'''
    GB2312 = enum.auto()
    '''Specifies the "simplified" Chinese character set for People\'s Republic of China.'''
    CHINESEBIG5 = enum.auto()
    '''Specifies the "traditional" Chinese character set, used mostly in
    Taiwan and in the Hong Kong and Macao Special Administrative Regions.'''
    GREEK = enum.auto()
    '''Specifies the Greek character set.'''
    TURKISH = enum.auto()
    '''Specifies the Turkish character set.'''
    VIETNAMESE = enum.auto()
    '''Specifies the Vietnamese character set.'''
    HEBREW = enum.auto()
    '''Specifies the Vietnamese character set.'''
    ARABIC = enum.auto()
    '''Specifies the Arabic character set'''
    BALTIC = enum.auto()
    '''Specifies the Baltic (Northeastern European) character set'''
    RUSSIAN = enum.auto()
    '''Specifies the Russian Cyrillic character set.'''
    THAI = enum.auto()
    '''Specifies the Thai character set.'''
    EASTEUROPE = enum.auto()
    '''Specifies a Eastern European character set.'''
    OEM = enum.auto()
    '''Specifies a mapping to one of the OEM code pages, according to the current
    system locale setting.'''

class WmfClipPrecisionFlags(enum.Enum):
    DEFAULT = enum.auto()
    '''Specifies that default clipping MUST be used.'''
    CHARACTER = enum.auto()
    '''This value SHOULD NOT be used.'''
    STROKE = enum.auto()
    '''This value MAY be returned when enumerating rasterized, TrueType and
    vector fonts.
    [33] (Windows NT 3.1, Windows NT 3.5, Windows NT 3.51, Windows NT 4.0,
    Windows 2000, and Windows XP: This value is always returned when enumerating fonts.)'''
    LH_ANGLES = enum.auto()
    '''This value is used to control font rotation, as follows:
    - If set, the rotation for all fonts SHOULD be determined by the orientation
    of the coordinate system; that is, whether the orientation is left-handed
    or right-handed.
    - If clear, device fonts SHOULD rotate counterclockwise, but the rotation of
    other fonts SHOULD be determined by the orientation of the coordinate
    system.'''
    TT_ALWAYS = enum.auto()
    '''This value SHOULD NOT [34] be used.
    [34] This value is ignored in the following Windows versions:
    - Windows Vista
    - Windows Server 2008
    - Windows 7
    - Windows Server 2008 R2
    - Windows 8
    - Windows Server 2012
    - Windows 8.1
    - Windows Server 2012 R2'''
    DFA_DISABLE = enum.auto()
    '''This value specifies that font association SHOULD [35] be turned off.
    [35] This value is not supported.in Windows 95, Windows 98, and Windows Millennium Edition.
    Font association is turned off in Windows 2000, Windows XP, and Windows Server 2003.
    This value is ignored in these Windows versions:
    - Windows Vista
    - Windows Server 2008
    - Windows 7
    - Windows Server 2008 R2
    - Windows 8
    - Windows Server 2012
    - Windows 8.1
    - Windows Server 2012 R2'''
    EMBEDDED = enum.auto()
    '''This value specifies that font embedding MUST be used to render document
    content; embedded fonts are read-only.'''

class WmfColorUsageEnum(enum.Enum):
    DIB_RGB_COLORS = enum.auto()
    '''The color table contains RGB values specified by RGBQuad Objects (section 2.2.2.20).'''
    DIB_PAL_COLORS = enum.auto()
    '''The color table contains 16-bit indices into the current logical palette in the playback device context.'''
    DIB_PAL_INDICES = enum.auto()
    '''No color table exists. The pixels in the DIB are indices into the current
    logical palette in the playback device context.'''

class WmfCompression(enum.Enum):
    BI_RGB = enum.auto()
    '''The bitmap is in uncompressed red green blue (RGB) format that is not compressed and does not use color masks.'''
    BI_RLE8 = enum.auto()
    '''An RGB format that uses run-length encoding (RLE) compression for bitmaps with 8 bits per pixel.
    The compression uses a 2-byte format consisting of a count byte followed by a byte containing a color index.'''
    BI_RLE4 = enum.auto()
    '''An RGB format that uses RLE compression for bitmaps with 4 bits per pixel.
    The compression uses a 2-byte format consisting of a count byte followed by two word-length color indexes'''
    BI_BITFIELDS = enum.auto()
    '''The bitmap is not compressed and the color table consists of three DWORD color masks that
    specify the red, green, and blue components, respectively, of each pixel.
    This is valid when used with 16 and 32-bits per pixel bitmaps.'''
    BI_JPEG = enum.auto()
    '''The image is a JPEG image, as specified in [JFIF]. This value SHOULD only be used in certain bitmap
    operations, such as JPEG pass-through. The application MUST query for the pass-through support,
    since not all devices support JPEG pass-through. Using non-RGB bitmaps MAY limit the portability
    of the metafile to other devices. For instance, display device contexts generally do not support this pass-through'''
    BI_PNG = enum.auto()
    '''The image is a PNG image, as specified in [RFC2083]. This value SHOULD only be used certain bitmap operations,
    such as JPEG/PNG pass-through. The application MUST query for the pass-through support, because not all devices
    support JPEG/PNG pass-through. Using non-RGB bitmaps MAY limit the portability of the metafile to other devices.
    For instance, display device contexts generally do not support this pass-through.'''
    BI_CMYK = enum.auto()
    '''The image is an uncompressed CMYK format.'''
    BI_CMYKRLE8 = enum.auto()
    '''A CMYK format that uses RLE compression for bitmaps with 8 bits per pixel.
    The compression uses a 2-byte format consisting of a count byte followed by a byte containing a color index.'''
    BI_CMYKRLE4 = enum.auto()
    '''A CMYK format that uses RLE compression for bitmaps with 4 bits per pixel.
    The compression uses a 2-byte format consisting of a count byte followed by two word-length color indexes.'''

class WmfFamilyFont(enum.Enum):
    DONTCARE = enum.auto()
    '''The default font is specified, which is implementation-dependent.'''
    ROMAN = enum.auto()
    '''Fonts with variable stroke widths, which are proportional to the actual widths of
    the glyphs, and which have serifs. "MS Serif" is an example.'''
    SWISS = enum.auto()
    '''Fonts with variable stroke widths, which are proportional to the actual widths of the
    glyphs, and which do not have serifs. "MS Sans Serif" is an example.'''
    MODERN = enum.auto()
    '''Fonts with constant stroke width, with or without serifs. Fixed-width fonts are
    usually modern. "Pica", "Elite", and "Courier New" are examples.'''
    SCRIPT = enum.auto()
    '''Fonts designed to look like handwriting. "Script" and "Cursive" are examples.'''
    DECORATIVE = enum.auto()
    '''Novelty fonts. "Old English" is an example.'''

class WmfFloodFillMode(enum.Enum):
    FLOOD_FILL_BORDER = enum.auto()
    '''The fill area is bounded by the color specified by the Color member.
    This style is identical to the filling performed by the
    META_FLOODFILL record.'''
    FLOOD_FILL_SURFACE = enum.auto()
    '''The fill area is bounded by the color that is specified by the Color
    member. Filling continues outward in all directions as long as the
    color is encountered. This style is useful for filling areas with
    multicolored boundaries.'''

class WmfFontQuality(enum.Enum):
    DEFAULT = enum.auto()
    '''Specifies that the character quality of the font does not matter, so
    DRAFT can be used.'''
    DRAFT = enum.auto()
    '''Specifies that the character quality of the font is less important than the
    matching of logical attribuetes. For rasterized fonts, scaling SHOULD be enabled, which
    means that more font sizes are available.'''
    PROOF = enum.auto()
    '''Specifies that the character quality of the font is more important than the
    matching of logical attributes. For rasterized fonts, scaling SHOULD be disabled, and the font
    closest in size SHOULD be chosen.'''
    NONANTIALIASED = enum.auto()
    '''Specifies that anti-aliasing SHOULD NOT be used when
    rendering text'''
    ANTIALIASED = enum.auto()
    '''Specifies that anti-aliasing SHOULD be used when rendering text, if
    the font supports it.'''
    CLEARTYPE = enum.auto()
    '''Specifies that ClearType anti-aliasing SHOULD be used when
    rendering text, if the font supports it.'''

class WmfGamutMappingIntent(enum.Enum):
    LCS_GM_ABS_COLORIMETRIC = enum.auto()
    '''Specifies that the white point SHOULD be maintained.
    Typically used when logical colors MUST be matched to their nearest physical color in the
    destination color gamut.
    Intent: Match
    ICC name: Absolute Colorimetric'''
    LCS_GM_BUSINESS = enum.auto()
    '''Specifies that saturation SHOULD be maintained. Typically used for
    business charts and other situations in which dithering is not required.
    Intent: Graphic
    ICC name: Saturation'''
    LCS_GM_GRAPHICS = enum.auto()
    '''Specifies that a colorimetric match SHOULD be maintained. Typically
    used for graphic designs and named colors.
    Intent: Proof
    ICC name: Relative Colorimetric'''
    LCS_GM_IMAGES = enum.auto()
    '''Specifies that contrast SHOULD be maintained. Typically used for
    photographs and natural images.
    Intent: Picture
    ICC name: Perceptual'''

class WmfHatchStyle(enum.Enum):
    HORIZONTAL = enum.auto()
    '''A horizontal hatch'''
    VERTICAL = enum.auto()
    '''A vertical hatch.'''
    FDIAGONAL = enum.auto()
    '''A 45-degree downward, left-to-right hatch.'''
    BDIAGONAL = enum.auto()
    '''A 45-degree upward, left-to-right hatch.'''
    CROSS = enum.auto()
    '''A horizontal and vertical cross-hatch.'''
    DIAGCROSS = enum.auto()
    '''The A 45-degree crosshatch.'''

class WmfLogicalColorSpaceEnum(enum.Enum):
    LCS_CALIBRATED_RGB = enum.auto()
    '''Color values are calibrated red green blue (RGB) values.'''
    LCS_S_RGB = enum.auto()
    '''The value is an encoding of the ASCII characters "sRGB", and it indicates that the
    color values are sRGB values.'''
    LCS_WINDOWS_COLOR_SPACE = enum.auto()
    '''The value is an encoding of the ASCII characters "Win ",
    including the trailing space, and it indicates that the color values are Windows default color space values.'''

class WmfMapMode(enum.Enum):
    TEXT = enum.auto()
    '''The text
    Each logical unit is mapped to one device pixel. Positive x is to the right; positive y is down'''
    LOMETRIC = enum.auto()
    '''The lometric
    Each logical unit is mapped to 0.1 millimeter. Positive x is to the right; positive y is up.'''
    HIMETRIC = enum.auto()
    '''The himetric
    Each logical unit is mapped to 0.01 millimeter. Positive x is to the right; positive y is up.'''
    LOENGLISH = enum.auto()
    '''The loenglish
    Each logical unit is mapped to 0.01 inch. Positive x is to the right; positive y is up.'''
    HIENGLISH = enum.auto()
    '''The hienglish
    Each logical unit is mapped to 0.001 inch. Positive x is to the right; positive y is up.'''
    TWIPS = enum.auto()
    '''The twips
    Each logical unit is mapped to one twentieth (1/20) of a point. In printing, a point is 1/72 of an inch; therefore,
    1/20 of a point is 1/1440 of an inch. This unit is also known as a "twip".'''
    ISOTROPIC = enum.auto()
    '''The isotropic
    Logical units are mapped to arbitrary device units with equally scaled axes; that is, one unit along the x-axis is
    equal to one unit along the y-axis.
    The META_SETWINDOWEXT and META_SETVIEWPORTEXT records specify the units and the orientation of the axes.'''
    ANISOTROPIC = enum.auto()
    '''The anisotropic
    Logical units are mapped to arbitrary units with arbitrarily scaled axes.'''

class WmfMetafileEscapes(enum.Enum):
    NEWFRAME = enum.auto()
    '''Notifies the printer driver that the application has finished writing to a page.'''
    ABORTDOC = enum.auto()
    '''Stops processing the current document.'''
    NEXTBAND = enum.auto()
    '''Notifies the printer driver that the application has finished writing to a band.'''
    SETCOLORTABLE = enum.auto()
    '''Sets color table values.'''
    GETCOLORTABLE = enum.auto()
    '''Gets color table values.'''
    FLUSHOUT = enum.auto()
    '''Causes all pending output to be flushed to the output device.'''
    DRAFTMODE = enum.auto()
    '''Indicates that the printer driver SHOULD print text only, and no graphics.'''
    QUERYESCSUPPORT = enum.auto()
    '''Queries a printer driver to determine whether a specific escape function
    is supported on the output device it drives.'''
    SETABORTPROC = enum.auto()
    '''Sets the application-defined function that allows a print job to be canceled
    during printing.'''
    STARTDOC = enum.auto()
    '''Notifies the printer driver that a new print job is starting.'''
    ENDDOC = enum.auto()
    '''Notifies the printer driver that the current print job is ending.'''
    GETPHYSPAGESIZE = enum.auto()
    '''Retrieves the physical page size currently selected on an output device.'''
    GETPRINTINGOFFSET = enum.auto()
    '''Retrieves the offset from the upper-left corner of the physical page
    where the actual printing or drawing begins.'''
    GETSCALINGFACTOR = enum.auto()
    '''Retrieves the scaling factors for the x-axis and the y-axis of a printer.'''
    META_ESCAPE_ENHANCED_METAFILE = enum.auto()
    '''Used to embed an enhanced metafile format (EMF)
    metafile within a WMF metafile.'''
    SETPENWIDTH = enum.auto()
    '''Sets the width of a pen in pixels.'''
    SETCOPYCOUNT = enum.auto()
    '''Sets the number of copies.'''
    SETPAPERSOURCE = enum.auto()
    '''Sets the source, such as a particular paper tray or bin on a printer, for
    output forms.'''
    PASSTHROUGH = enum.auto()
    '''This record passes through arbitrary data.'''
    GETTECHNOLOGY = enum.auto()
    '''Gets information concerning graphics technology that is supported on a
    device.'''
    SETLINECAP = enum.auto()
    '''Specifies the line-drawing mode to use in output to a device.'''
    SETLINEJOIN = enum.auto()
    '''Specifies the line-joining mode to use in output to a device.'''
    SETMITERLIMIT = enum.auto()
    '''Sets the limit for the length of miter joins to use in output to a device.'''
    BANDINFO = enum.auto()
    '''Retrieves or specifies settings concerning banding on a device, such as the
    number of bands.'''
    DRAWPATTERNRECT = enum.auto()
    '''Draws a rectangle with a defined pattern.'''
    GETVECTORPENSIZE = enum.auto()
    '''Retrieves the physical pen size currently defined on a device.'''
    GETVECTORBRUSHSIZE = enum.auto()
    '''Retrieves the physical brush size currently defined on a device.'''
    ENABLEDUPLEX = enum.auto()
    '''Enables or disables double-sided (duplex) printing on a device.'''
    GETSETPAPERBINS = enum.auto()
    '''Retrieves or specifies the source of output forms on a device.'''
    GETSETPRINTORIENT = enum.auto()
    '''Retrieves or specifies the paper orientation on a device.'''
    ENUMPAPERBINS = enum.auto()
    '''Retrieves information concerning the sources of different forms on an
    output device.'''
    SETDIBSCALING = enum.auto()
    '''Specifies the scaling of device-independent bitmaps (DIBs).'''
    EPSPRINTING = enum.auto()
    '''Indicates the start and end of an encapsulated PostScript (EPS) section.'''
    ENUMPAPERMETRICS = enum.auto()
    '''Queries a printer driver for paper dimensions and other forms data.'''
    GETSETPAPERMETRICS = enum.auto()
    '''Retrieves or specifies paper dimensions and other forms data on an
    output device.'''
    POSTSCRIPT_DATA = enum.auto()
    '''Sends arbitrary PostScript data to an output device.'''
    POSTSCRIPT_IGNORE = enum.auto()
    '''Notifies an output device to ignore PostScript data.'''
    GETDEVICEUNITS = enum.auto()
    '''Gets the device units currently configured on an output device.'''
    GETEXTENDEDTEXTMETRICS = enum.auto()
    '''Gets extended text metrics currently configured on an output
    device.'''
    GETPAIRKERNTABLE = enum.auto()
    '''Gets the font kern table currently defined on an output device.'''
    EXTTEXTOUT = enum.auto()
    '''Draws text using the currently selected font, background color, and text color.'''
    GETFACENAME = enum.auto()
    '''Gets the font face name currently configured on a device.'''
    DOWNLOADFACE = enum.auto()
    '''Sets the font face name on a device.'''
    METAFILE_DRIVER = enum.auto()
    '''Queries a printer driver about the support for metafiles on an output
    device.'''
    QUERYDIBSUPPORT = enum.auto()
    '''Queries the printer driver about its support for DIBs on an output device.'''
    BEGIN_PATH = enum.auto()
    '''Opens a path.'''
    CLIP_TO_PATH = enum.auto()
    '''Defines a clip region that is bounded by a path. The input MUST be a 16-bit
    quantity that defines the action to take.'''
    END_PATH = enum.auto()
    '''Ends a path.'''
    OPEN_CHANNEL = enum.auto()
    '''The same as STARTDOC specified with a NULL document and output
    filename, data in raw mode, and a type of zero.'''
    DOWNLOADHEADER = enum.auto()
    '''Instructs the printer driver to download sets of PostScript procedures.'''
    CLOSE_CHANNEL = enum.auto()
    '''The same as ENDDOC. See OPEN_CHANNEL.'''
    POSTSCRIPT_PASSTHROUGH = enum.auto()
    '''Sends arbitrary data directly to a printer driver, which is
    expected to process this data only when in PostScript mode. :py:attr:`aspose.imaging.fileformats.wmf.consts.WmfMetafileEscapes.POSTSCRIPT_IDENTIFY`.'''
    ENCAPSULATED_POSTSCRIPT = enum.auto()
    '''Sends arbitrary data directly to the printer driver.'''
    POSTSCRIPT_IDENTIFY = enum.auto()
    '''Sets the printer driver to either PostScript or GDI mode.'''
    POSTSCRIPT_INJECTION = enum.auto()
    '''Inserts a block of raw data into a PostScript stream. The input
    MUST be a 32-bit quantity specifying the number of bytes to inject, a 16-bit quantity
    specifying the injection point, and a 16-bit quantity specifying the page number, followed by
    the bytes to inject.'''
    CHECKJPEGFORMAT = enum.auto()
    '''Checks whether the printer supports a JPEG image.'''
    CHECKPNGFORMAT = enum.auto()
    '''Checks whether the printer supports a PNG image.'''
    GET_PS_FEATURESETTING = enum.auto()
    '''Gets information on a specified feature setting for a PostScript
    printer driver.'''
    MXDC_ESCAPE = enum.auto()
    '''Enables applications to write documents to a file or to a printer in XML Paper
    Specification (XPS) format.'''
    SPCLPASSTHROUGH2 = enum.auto()
    '''Enables applications to include private procedures and other arbitrary
    data in documents.'''

class WmfMetafileVersion(enum.Enum):
    METAVERSION100 = enum.auto()
    '''DIBs are not supported.'''
    METAVERSION300 = enum.auto()
    '''DIBs are supported.'''

class WmfMixMode(enum.Enum):
    TRANSPARENT = enum.auto()
    '''The background remains untouched.'''
    OPAQUE = enum.auto()
    '''The background is filled with the
    background color that is currently defined in the playback device context before the text, hatched brush, or pen is
    drawn.'''

class WmfOutPrecision(enum.Enum):
    DEFAULT = enum.auto()
    '''A value that specifies default behavior.'''
    STRING = enum.auto()
    '''A value that is returned when rasterized fonts are enumerated.'''
    STROKE = enum.auto()
    '''A value that is returned when TrueType and other outline fonts, and
    vector fonts are enumerated.'''
    TT = enum.auto()
    '''A value that specifies the choice of a TrueType font when the system
    contains multiple fonts with the same name.'''
    DEVICE = enum.auto()
    '''A value that specifies the choice of a device font when the system
    contains multiple fonts with the same name.'''
    RASTER = enum.auto()
    '''A value that specifies the choice of a rasterized font when the system
    contains multiple fonts with the same name.'''
    TT_ONLY = enum.auto()
    '''A value that specifies the requirement for only TrueType fonts. If
    there are no TrueType fonts installed in the system, default behavior is specified.'''
    OUTLINE = enum.auto()
    '''A value that specifies the requirement for TrueType and other outline fonts.'''
    SCREEN_OUTLINE = enum.auto()
    '''A value that specifies a preference for TrueType and other
    outline fonts.'''
    PS_ONLY = enum.auto()
    '''A value that specifies a requirement for only PostScript fonts. If there
    are no PostScript fonts installed in the system, default behavior is specified.'''

class WmfPenStyle(enum.Enum):
    COSMETIC = enum.auto()
    '''The cosmetic'''
    ENDCAP_ROUND = enum.auto()
    '''The line end caps are round.'''
    JOIN_ROUND = enum.auto()
    '''Line joins are round.'''
    SOLID = enum.auto()
    '''The pen is solid.'''
    DASH = enum.auto()
    '''The pen is dashed.'''
    DOT = enum.auto()
    '''The pen is dotted.'''
    DASHDOT = enum.auto()
    '''The pen has alternating dashes and dots.'''
    DASHDOTDOT = enum.auto()
    '''The pen has dashes and double dots.'''
    NULL = enum.auto()
    '''The pen is invisible.'''
    INSIDEFRAME = enum.auto()
    '''The pen is solid. When this pen is used in any drawing record that takes a bounding rectangle, the dimensions of
    the figure are shrunk so that it fits entirely in the bounding rectangle, taking into account the width of the pen.'''
    USERSTYLE = enum.auto()
    '''The pen uses a styling array supplied by the user.'''
    ALTERNATE = enum.auto()
    '''The pen sets every other pixel (this style is applicable only for cosmetic pens).'''
    ENDCAP_SQUARE = enum.auto()
    '''Line end caps are square.'''
    ENDCAP_FLAT = enum.auto()
    '''Line end caps are flat.'''
    JOIN_BEVEL = enum.auto()
    '''Line joins are beveled.'''
    JOIN_MITER = enum.auto()
    '''Line joins are mitered when they are within the current
    limit set by the SETMITERLIMIT META_ESCAPE record. A join is beveled when it would exceed the limit.'''

class WmfPitchFont(enum.Enum):
    DEFAULT_PITCH = enum.auto()
    '''The default pitch, which is implementation-dependent.'''
    FIXED_PITCH = enum.auto()
    '''A fixed pitch, which means that all the characters in the font occupy the same
    width when output in a string.'''
    VARIABLE_PITCH = enum.auto()
    '''A variable pitch, which means that the characters in the font occupy widths
    that are proportional to the actual widths of the glyphs when output in a string. For example,
    the "i" and space characters usually have much smaller widths than a "W" or "O" character.'''

class WmfPolyFillMode(enum.Enum):
    ALTERNATE = enum.auto()
    '''Selects alternate mode (fills the area between odd-numbered and even-numbered polygon sides on each scan line).'''
    WINDING = enum.auto()
    '''Selects winding mode (fills any region with a nonzero winding value)'''

class WmfPostScriptCap(enum.Enum):
    POST_SCRIPT_NOT_SET = enum.auto()
    '''Specifies that the line-ending style has not been set, and that a default style
    MAY [24] be used.'''
    POST_SCRIPT_FLAT_CAP = enum.auto()
    '''Specifies that the line ends at the last point. The end is squared off.'''
    POST_SCRIPT_ROUND_CAP = enum.auto()
    '''Specifies a circular cap. The center of the circle is the last point in the
    line. The diameter of the circle is the same as the line width; that is, the thickness of the line.'''
    POST_SCRIPT_SQUARE_CAP = enum.auto()
    '''Specifies a square cap. The center of the square is the last point in the
    line. The height and width of the square are the same as the line width; that is, the thickness
    of the line.'''

class WmfPostScriptClipping(enum.Enum):
    CLIP_SAVE = enum.auto()
    '''Saves the current PostScript clipping path.'''
    CLIP_RESTORE = enum.auto()
    '''Restores the PostScript clipping path to the last clipping path that was saved
    by a previous CLIP_SAVE function applied by a CLIP_TO_PATH record (section 2.3.6.6).'''
    CLIP_INCLUSIVE = enum.auto()
    '''Intersects the current PostScript clipping path with the current clipping path
    and saves the result as the new PostScript clipping path.'''

class WmfRecordType(enum.Enum):
    EOF = enum.auto()
    '''The EOF record type'''
    REALIZE_PALETTE = enum.auto()
    '''The realizepalette'''
    SET_PALENTRIES = enum.auto()
    '''The setpalentries'''
    SET_BK_MODE = enum.auto()
    '''The setbkmode'''
    SET_MAP_MODE = enum.auto()
    '''The setmapmode'''
    SET_ROP2 = enum.auto()
    '''The setrop2'''
    SET_RELABS = enum.auto()
    '''The setrelabs'''
    SET_POLYFILL_MODE = enum.auto()
    '''The setpolyfillmode'''
    SET_STRETCHBLT_MODE = enum.auto()
    '''The setstretchbltmode'''
    SET_TEXT_CHAR_EXTRA = enum.auto()
    '''The settextcharextra'''
    RESTORE_DC = enum.auto()
    '''The restoredc'''
    RESIZE_PALETTE = enum.auto()
    '''The resizepalette'''
    DIB_CREATE_PATTERN_BRUSH = enum.auto()
    '''The dibcreatepatternbrush'''
    SET_LAYOUT = enum.auto()
    '''The setlayout'''
    SET_BK_COLOR = enum.auto()
    '''The setbkcolor'''
    SET_TEXT_COLOR = enum.auto()
    '''The settextcolor'''
    OFFSET_VIEW_PORT_ORG = enum.auto()
    '''The offsetviewportorg'''
    LINE_TO = enum.auto()
    '''The lineto'''
    MOVE_TO = enum.auto()
    '''The moveto'''
    OFFSET_CLIP_RGN = enum.auto()
    '''The offsetcliprgn'''
    FILL_REGION = enum.auto()
    '''The fillregion'''
    SET_MAPPER_FLAGS = enum.auto()
    '''The setmapperflags'''
    SELECT_PALETTE = enum.auto()
    '''The selectpalette'''
    POLYGON = enum.auto()
    '''The polygon'''
    POLY_LINE = enum.auto()
    '''The polyline'''
    SET_TEXT_JUSTIFICATION = enum.auto()
    '''The settextjustification'''
    SET_WINDOW_ORG = enum.auto()
    '''The setwindoworg'''
    SET_WINDOW_EXT = enum.auto()
    '''The setwindowext'''
    SET_VIEW_PORT_ORG = enum.auto()
    '''The setviewportorg'''
    SET_VIEWPORT_EXT = enum.auto()
    '''The setviewportext'''
    OFFSET_WINDOW_ORG = enum.auto()
    '''The offsetwindoworg'''
    SCALE_WINDOW_EXT = enum.auto()
    '''The scalewindowext'''
    SCALE_VIEWPORT_EXT = enum.auto()
    '''The scaleviewportext'''
    EXCLUDE_CLIP_RECT = enum.auto()
    '''The excludecliprect'''
    INTERSECT_CLIP_RECT = enum.auto()
    '''The intersectcliprect'''
    ELLIPSE = enum.auto()
    '''The ellipse'''
    FLOOD_FILL = enum.auto()
    '''The floodfill'''
    FRAME_REGION = enum.auto()
    '''The frameregion'''
    ANIMATE_PALETTE = enum.auto()
    '''The animatepalette'''
    TEXT_OUT = enum.auto()
    '''The textout'''
    POLY_POLYGON = enum.auto()
    '''The polypolygon'''
    EXT_FLOOD_FILL = enum.auto()
    '''The extfloodfill'''
    RECTANGLE = enum.auto()
    '''The rectangle'''
    SET_PIXEL = enum.auto()
    '''The setpixel'''
    ROUND_RECT = enum.auto()
    '''The roundrect'''
    PAT_BLT = enum.auto()
    '''The patblt'''
    SAVE_DC = enum.auto()
    '''The savedc'''
    PIE = enum.auto()
    '''The pie record type'''
    STRETCH_BLT = enum.auto()
    '''The stretchblt'''
    ESCAPE = enum.auto()
    '''The escape'''
    INVERT_REGION = enum.auto()
    '''The invertregion'''
    PAINT_REGION = enum.auto()
    '''The paintregion'''
    SELECT_CLIP_REGION = enum.auto()
    '''The selectclipregion'''
    SELECT_OBJECT = enum.auto()
    '''The selectobject'''
    SET_TEXT_ALIGN = enum.auto()
    '''The settextalign'''
    ARC = enum.auto()
    '''The arc record type'''
    CHORD = enum.auto()
    '''The chord record type'''
    BIT_BLT = enum.auto()
    '''The bitblt'''
    EXT_TEXT_OUT = enum.auto()
    '''The exttextout'''
    SET_DIB_TO_DEV = enum.auto()
    '''The setdibtodev'''
    DIB_BIT_BLT = enum.auto()
    '''The dibbitblt'''
    DIB_STRETCH_BLT = enum.auto()
    '''The dibstretchblt'''
    STRETCH_DIB = enum.auto()
    '''The stretchdib'''
    DELETE_OBJECT = enum.auto()
    '''The deleteobject'''
    CREATE_PALETTE = enum.auto()
    '''The createpalette'''
    CREATE_PATTERN_BRUSH = enum.auto()
    '''The createpatternbrush'''
    CREATE_PEN_IN_DIRECT = enum.auto()
    '''The createpenindirect'''
    CREATE_FONT_IN_DIRECT = enum.auto()
    '''The createfontindirect'''
    CREATE_BRUSH_IN_DIRECT = enum.auto()
    '''The createbrushindirect'''
    CREATE_REGION = enum.auto()
    '''The createregion'''
    NONE = enum.auto()
    '''The record type none.'''

class WmfTernaryRasterOperation(enum.Enum):
    BLACKNESS = enum.auto()
    '''Fills the destination rectangle using the color associated with index 0 in the physical palette. (This color is
    black for the default physical palette.)'''
    DPSOON = enum.auto()
    DPSONA = enum.auto()
    PSON = enum.auto()
    SDPONA = enum.auto()
    DPON = enum.auto()
    PDSXNON = enum.auto()
    PDSAON = enum.auto()
    SDPNAA = enum.auto()
    PDSXON = enum.auto()
    DPNA = enum.auto()
    PSDNAON = enum.auto()
    SPNA = enum.auto()
    PDSNAON = enum.auto()
    PDSONON = enum.auto()
    PN = enum.auto()
    PDSONA = enum.auto()
    NOTSRCERASE = enum.auto()
    '''Combines the colors of the source and destination rectangles by using the Boolean OR operator and then inverts the
    resultant color.'''
    SDPXNON = enum.auto()
    SDPAON = enum.auto()
    DPSXNON = enum.auto()
    DPSAON = enum.auto()
    PSDPSANAXX = enum.auto()
    SSPXDSXAXN = enum.auto()
    SPXPDXA = enum.auto()
    SDPSANAXN = enum.auto()
    PDSPAOX = enum.auto()
    SDPSXAXN = enum.auto()
    PSDPAOX = enum.auto()
    DSPDXAXN = enum.auto()
    PDSOX = enum.auto()
    PDSOAN = enum.auto()
    DPSNAA = enum.auto()
    SDPXON = enum.auto()
    DSNA = enum.auto()
    SPDNAON = enum.auto()
    SPXDSXA = enum.auto()
    PDSPANAXN = enum.auto()
    SDPSAOX = enum.auto()
    SDPSXNOX = enum.auto()
    DPSXA = enum.auto()
    PSDPSAOXXN = enum.auto()
    DPSANA = enum.auto()
    SSPXPDXAXN = enum.auto()
    SPDSOAX = enum.auto()
    PSDNOX = enum.auto()
    PSDPXOX = enum.auto()
    PSDNOAN = enum.auto()
    PSNA = enum.auto()
    SDPNAON = enum.auto()
    SDPSOOX = enum.auto()
    NOTSRCCOPY = enum.auto()
    '''Copies the inverted source rectangle to the destination.'''
    SPDSAOX = enum.auto()
    SPDSXNOX = enum.auto()
    SDPOX = enum.auto()
    SDPOAN = enum.auto()
    PSDPOAX = enum.auto()
    SPDNOX = enum.auto()
    SPDSXOX = enum.auto()
    SPDNOAN = enum.auto()
    PSX = enum.auto()
    SPDSONOX = enum.auto()
    SPDSNAOX = enum.auto()
    PSAN = enum.auto()
    PSDNAA = enum.auto()
    DPSXON = enum.auto()
    SDXPDXA = enum.auto()
    SPDSANAXN = enum.auto()
    SRCERASE = enum.auto()
    '''Combines the inverted colors of the destination rectangle with the colors of the source rectangle by using the
    Boolean AND operator.'''
    DPSNAON = enum.auto()
    DSPDAOX = enum.auto()
    PSDPXAXN = enum.auto()
    SDPXA = enum.auto()
    PDSPDAOXXN = enum.auto()
    DPSDOAX = enum.auto()
    PDSNOX = enum.auto()
    SDPANA = enum.auto()
    SSPXDSXOXN = enum.auto()
    PDSPXOX = enum.auto()
    PDSNOAN = enum.auto()
    PDNA = enum.auto()
    DSPNAON = enum.auto()
    DPSDAOX = enum.auto()
    SPDSXAXN = enum.auto()
    DPSONON = enum.auto()
    DSTINVERT = enum.auto()
    '''Inverts the destination rectangle.'''
    DPSOX = enum.auto()
    DPSOAN = enum.auto()
    PDSPOAX = enum.auto()
    DPSNOX = enum.auto()
    PATINVERT = enum.auto()
    '''Combines the colors of the brush currently selected in hdcDest, with the colors of the destination rectangle by
    using the Boolean XOR operator.'''
    DPSDONOX = enum.auto()
    DPSDXOX = enum.auto()
    DPSNOAN = enum.auto()
    DPSDNAOX = enum.auto()
    DPAN = enum.auto()
    PDSXA = enum.auto()
    DSPDSAOXXN = enum.auto()
    DSPDOAX = enum.auto()
    SDPNOX = enum.auto()
    SDPSOAX = enum.auto()
    DSPNOX = enum.auto()
    SRCINVERT = enum.auto()
    '''Combines the colors of the source and destination rectangles by using the Boolean XOR operator.'''
    SDPSONOX = enum.auto()
    DSPDSONOXXN = enum.auto()
    PDSXXN = enum.auto()
    DPSAX = enum.auto()
    PSDPSOAXXN = enum.auto()
    SDPAX = enum.auto()
    PDSPDOAXXN = enum.auto()
    SDPSNOAX = enum.auto()
    PDXNAN = enum.auto()
    PDSANA = enum.auto()
    SSDXPDXAXN = enum.auto()
    SDPSXOX = enum.auto()
    SDPNOAN = enum.auto()
    DSPDXOX = enum.auto()
    DSPNOAN = enum.auto()
    SDPSNAOX = enum.auto()
    DSAN = enum.auto()
    PDSAX = enum.auto()
    DSPDSOAXXN = enum.auto()
    DPSDNOAX = enum.auto()
    SDPXNAN = enum.auto()
    SPDSNOAX = enum.auto()
    DPSXNAN = enum.auto()
    SPXDSXO = enum.auto()
    DPSAAN = enum.auto()
    DPSAA = enum.auto()
    SPXDSXON = enum.auto()
    DPSXNA = enum.auto()
    SPDSNOAXN = enum.auto()
    SDPXNA = enum.auto()
    PDSPNOAXN = enum.auto()
    DSPDSOAXX = enum.auto()
    PDSAXN = enum.auto()
    SRCAND = enum.auto()
    '''Combines the colors of the source and destination rectangles by using the Boolean AND operator.'''
    SDPSNAOXN = enum.auto()
    DSPNOA = enum.auto()
    DSPDXOXN = enum.auto()
    SDPNOA = enum.auto()
    SDPSXOXN = enum.auto()
    SSDXPDXAX = enum.auto()
    PDSANAN = enum.auto()
    PDSXNA = enum.auto()
    SDPSNOAXN = enum.auto()
    DPSDPOAXX = enum.auto()
    SPDAXN = enum.auto()
    PSDPSOAXX = enum.auto()
    DPSAXN = enum.auto()
    DPSXX = enum.auto()
    PSDPSONOXX = enum.auto()
    SDPSONOXN = enum.auto()
    DSXN = enum.auto()
    DPSNAX = enum.auto()
    SDPSOAXN = enum.auto()
    SPDNAX = enum.auto()
    DSPDOAXN = enum.auto()
    DSPDSAOXX = enum.auto()
    PDSXAN = enum.auto()
    DPA = enum.auto()
    PDSPNAOXN = enum.auto()
    DPSNOA = enum.auto()
    DPSDXOXN = enum.auto()
    PDSPONOXN = enum.auto()
    PDXN = enum.auto()
    DSPNAX = enum.auto()
    PDSPOAXN = enum.auto()
    DPSOA = enum.auto()
    DPSOXN = enum.auto()
    D = enum.auto()
    DPSONO = enum.auto()
    SPDSXAX = enum.auto()
    DPSDAOXN = enum.auto()
    DSPNAO = enum.auto()
    DPNO = enum.auto()
    PDSNOA = enum.auto()
    PDSPXOXN = enum.auto()
    SSPXDSXOX = enum.auto()
    SDPANAN = enum.auto()
    PSDNAX = enum.auto()
    DPSDOAXN = enum.auto()
    DPSDPAOXX = enum.auto()
    SDPXAN = enum.auto()
    PSDPXAX = enum.auto()
    DSPDAOXN = enum.auto()
    DPSNAO = enum.auto()
    MERGEPAINT = enum.auto()
    '''Merges the colors of the inverted source rectangle with the colors of the destination rectangle by using the
    Boolean OR operator.'''
    SPDSANAX = enum.auto()
    SDXPDXAN = enum.auto()
    DPSXO = enum.auto()
    DPSANO = enum.auto()
    MERGECOPY = enum.auto()
    '''Merges the colors of the source rectangle with the brush currently selected in hdcDest, by using the Boolean AND
    operator.'''
    SPDSNAOXN = enum.auto()
    SPDSONOXN = enum.auto()
    PSXN = enum.auto()
    SPDNOA = enum.auto()
    SPDSXOXN = enum.auto()
    SDPNAX = enum.auto()
    PSDPOAXN = enum.auto()
    SDPOA = enum.auto()
    SPDOXN = enum.auto()
    DPSDXAX = enum.auto()
    SPDSAOXN = enum.auto()
    SRCCOPY = enum.auto()
    '''Copies the source rectangle directly to the destination rectangle.'''
    SDPONO = enum.auto()
    SDPNAO = enum.auto()
    SPNO = enum.auto()
    PSDNOA = enum.auto()
    PSDPXOXN = enum.auto()
    PDSNAX = enum.auto()
    SPDSOAXN = enum.auto()
    SSPXPDXAX = enum.auto()
    DPSANAN = enum.auto()
    PSDPSAOXX = enum.auto()
    DPSXAN = enum.auto()
    PDSPXAX = enum.auto()
    SDPSAOXN = enum.auto()
    DPSDANAX = enum.auto()
    SPXDSXAN = enum.auto()
    SPDNAO = enum.auto()
    SDNO = enum.auto()
    SDPXO = enum.auto()
    SDPANO = enum.auto()
    PDSOA = enum.auto()
    PDSOXN = enum.auto()
    DSPDXAX = enum.auto()
    PSDPAOXN = enum.auto()
    SDPSXAX = enum.auto()
    PDSPAOXN = enum.auto()
    SDPSANAX = enum.auto()
    SPXPDXAN = enum.auto()
    SSPXDSXAX = enum.auto()
    DSPDSANAXXN = enum.auto()
    DPSAO = enum.auto()
    DPSXNO = enum.auto()
    SDPAO = enum.auto()
    SDPXNO = enum.auto()
    SRCPAINT = enum.auto()
    '''Combines the colors of the source and destination rectangles by using the Boolean OR operator.'''
    SDPNOO = enum.auto()
    PATCOPY = enum.auto()
    '''Copies the brush currently selected in hdcDest, into the destination bitmap.'''
    PDSONO = enum.auto()
    PDSNAO = enum.auto()
    PSNO = enum.auto()
    PSDNAO = enum.auto()
    PDNO = enum.auto()
    PDSXO = enum.auto()
    PDSANO = enum.auto()
    PDSAO = enum.auto()
    PDSXNO = enum.auto()
    DPO = enum.auto()
    PATPAINT = enum.auto()
    '''Combines the colors of the brush currently selected in hdcDest, with the colors of the inverted source rectangle by
    using the Boolean OR operator. The result of this operation is combined with the colors of the destination
    rectangle by using the Boolean OR operator.'''
    PSO = enum.auto()
    PSDNOO = enum.auto()
    DPSOO = enum.auto()
    WHITENESS = enum.auto()
    '''Fills the destination rectangle using the color associated with index 1 in the physical palette. (This color is
    white for the default physical palette.)'''

class WmfTernaryRasterOperationOperand(enum.Enum):
    D = enum.auto()
    '''Destination bitmap'''
    P = enum.auto()
    '''Selected brush (also called pattern)'''
    S = enum.auto()
    '''Source bitmap'''
    A = enum.auto()
    '''Bitwise AND'''
    N = enum.auto()
    '''Bitwise NOT (inverse)'''
    O = enum.auto()
    '''Bitwise OR'''
    X = enum.auto()
    '''Bitwise exclusive OR (XOR)'''

class WmfTextAlignmentModeFlags(enum.Enum):
    NOUPDATECP = enum.auto()
    '''The drawing position in the playback device context MUST NOT be updated after each
    text output call. The reference point MUST be passed to the text output function.'''
    LEFT = enum.auto()
    '''The reference point MUST be on the left edge of the bounding rectangle.'''
    TOP = enum.auto()
    '''The reference point MUST be on the top edge of the bounding rectangle.'''
    UPDATECP = enum.auto()
    '''The drawing position in the playback device context MUST be updated after each text
    output call. It MUST be used as the reference point.'''
    RIGHT = enum.auto()
    '''The reference point MUST be on the right edge of the bounding rectangle.'''
    CENTER = enum.auto()
    '''The reference point MUST be aligned horizontally with the center of the bounding rectangle.'''
    BOTTOM = enum.auto()
    '''The reference point MUST be on the bottom edge of the bounding rectangle.'''
    BASELINE = enum.auto()
    '''The reference point MUST be on the baseline of the text.'''
    RTLREADING = enum.auto()
    '''The text MUST be laid out in right-to-left reading order, instead of the default left-to right order. This SHOULD
    be applied only when the font that is defined in the playback
    device context is either Hebrew or Arabic.'''
    HORIZONTAL = enum.auto()
    '''Represents Horizontal text algin sets (Left | Right | Center)'''
    VERTICAL = enum.auto()
    '''Represents Vertical text align sets (Top | Bottom | Baseline)'''

class WmfVerticalTextAlignmentModeFlags(enum.Enum):
    VTA_TOP = enum.auto()
    '''The reference point MUST be on the top edge of the bounding rectangle.'''
    VTA_RIGHT = enum.auto()
    '''The reference point MUST be on the right edge of the bounding rectangle.'''
    VTA_BOTTOM = enum.auto()
    '''The reference point MUST be on the bottom edge of the bounding rectangle.'''
    VTA_CENTER = enum.auto()
    '''The reference point MUST be aligned vertically with the center of the bounding rectangle.'''
    VTA_LEFT = enum.auto()
    '''The reference point MUST be on the left edge of the bounding rectangle.'''
    VTA_BASELINE = enum.auto()
    '''The reference point MUST be on the baseline of the text.'''

