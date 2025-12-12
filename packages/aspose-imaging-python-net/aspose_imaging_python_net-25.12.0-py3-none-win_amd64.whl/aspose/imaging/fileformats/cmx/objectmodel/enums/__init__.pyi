"""The namespace handles Tiff file format processing."""
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

class CapsTypes(enum.Enum):
    SQUARE = enum.auto()
    '''Add square end shapes to the line.'''
    ROUND = enum.auto()
    '''Add round end shapes to the line.'''
    EXTENDED_SQUARE = enum.auto()
    '''The extended squareAdd square end shapes that extend the length of the line.'''

class CmxCommandCodes(enum.Enum):
    ADD_CLIPPING_REGION = enum.auto()
    '''The add clipping region command'''
    ADD_GLOBAL_TRANSFORM = enum.auto()
    '''The add global transform command'''
    BEGIN_EMBEDDED = enum.auto()
    '''The begin embedded file command'''
    BEGIN_GROUP = enum.auto()
    '''The begin group command'''
    BEGIN_LAYER = enum.auto()
    '''The begin layer command'''
    BEGIN_PAGE = enum.auto()
    '''The begin page command'''
    BEGIN_PARAGRAPH = enum.auto()
    '''The begin paragraph command'''
    BEGIN_PROCEDURE = enum.auto()
    '''The begin procedure command'''
    BEGIN_TEXT_GROUP = enum.auto()
    '''The begin text group command'''
    BEGIN_TEXT_OBJECT = enum.auto()
    '''The begin text object command'''
    BEGIN_TEXT_STREAM = enum.auto()
    '''The begin text stream command'''
    CHAR_INFO = enum.auto()
    '''The character information command'''
    CHARACTERS = enum.auto()
    '''The characters command'''
    CLEAR_CLIPPING = enum.auto()
    '''The clear clipping command'''
    COMMENT = enum.auto()
    '''The comment command'''
    DRAW_IMAGE = enum.auto()
    '''The draw image command'''
    DRAW_CHARS = enum.auto()
    '''The draw chars command'''
    ELLIPSE = enum.auto()
    '''The ellipse command'''
    END_EMBEDDED = enum.auto()
    '''The end embedded file command'''
    END_GROUP = enum.auto()
    '''The end group command'''
    END_LAYER = enum.auto()
    '''The end layer command'''
    END_PAGE = enum.auto()
    '''The end page command'''
    END_PARAGRAPH = enum.auto()
    '''The end paragraph command'''
    END_SECTION = enum.auto()
    '''The end section command'''
    END_TEXT_GROUP = enum.auto()
    '''The end text group command'''
    END_TEXT_OBJECT = enum.auto()
    '''The end text object command'''
    END_TEXT_STREAM = enum.auto()
    '''The end text stream command'''
    JUMP_ABSOLUTE = enum.auto()
    '''The jump to absolute position command'''
    POLY_CURVE = enum.auto()
    '''The poly curve command'''
    POP_MAPPING_MODE = enum.auto()
    '''The pop mapping mode command'''
    POP_TINT = enum.auto()
    '''The pop tint command'''
    PUSH_MAPPING_MODE = enum.auto()
    '''The push mapping mode command'''
    PUSH_TINT = enum.auto()
    '''The push tint command'''
    RECTANGLE = enum.auto()
    '''The rectangle command'''
    REMOVE_LAST_CLIPPING_REGION = enum.auto()
    '''The remove last clipping region command'''
    RESTORE_LAST_GLOBAL_TRANSFO = enum.auto()
    '''The restore last global transformation command'''
    SET_CHAR_STYLE = enum.auto()
    '''The set character style command'''
    SET_GLOBAL_TRANSFO = enum.auto()
    '''The set global transformation command'''
    SIMPLE_WIDE_TEXT = enum.auto()
    '''The simple wide text command'''
    TEXT_FRAME = enum.auto()
    '''The text frame command'''

class ColorModels(enum.Enum):
    INVALID = enum.auto()
    '''Invalid color model.'''
    PANTONE = enum.auto()
    '''PANTONE palette.'''
    CMYK = enum.auto()
    '''CMYK color model, represented in 0-100 byte ranges.'''
    CMYK255 = enum.auto()
    '''CMYK color model, represented in 0-255 byte ranges.'''
    CMY = enum.auto()
    '''CMY color model.'''
    RGB = enum.auto()
    '''RGM color model.'''
    HSB = enum.auto()
    '''HSB color model.'''
    HLS = enum.auto()
    '''HLS color model.'''
    BW = enum.auto()
    '''Black and White colors.'''
    GRAY = enum.auto()
    '''Grayscale color model.'''
    YIQ255 = enum.auto()
    '''YIQ color model, represented in 0-255 byte ranges.'''
    LAB = enum.auto()
    '''Lab color model.'''
    BGR = enum.auto()
    '''The color model BGR'''
    LAB255 = enum.auto()
    '''Lab color model LAB255.'''

class FillTypes(enum.Enum):
    UNKNOWN = enum.auto()
    '''Unknown fill type.'''
    NO_FILL = enum.auto()
    '''No fill needed'''
    UNIFORM = enum.auto()
    '''Uniform fill.
    Apply a solid fill color.'''
    FOUNTAIN = enum.auto()
    '''Fountain fill.
    Apply a gradient of colors or shades.'''
    POSTSCRIPT = enum.auto()
    '''Postscript fill.
    Apply an intricate PostScript texture fill.'''
    TWO_COLOR_PATTERN = enum.auto()
    '''Two-color pattern fill.'''
    IMPORTED_BITMAP = enum.auto()
    '''Bitmap pattern fill.'''
    FULL_COLOR_PATTERN = enum.auto()
    '''Vector pattern fill.'''
    TEXTURE = enum.auto()
    '''Texture fill.'''

class GradientTypes(enum.Enum):
    LINEAR = enum.auto()
    '''Linear fountain fill.
    Apply a fill that gradually changes color along a linear path.'''
    ELLIPTICAL = enum.auto()
    '''Elliptical fountain fill.
    Apply a fill that gradually changes color in concrete ellipses from the center outwards.'''
    CONICAL = enum.auto()
    '''Conical fountain fill.
    Apply a fill that gradually changes color in a conical shape.'''
    RECTANGULAR = enum.auto()
    '''Rectangular fountain fill.
    Apply a fill that gradually changes color in concrete rectangles from the center outwards.'''

class JoinTypes(enum.Enum):
    MITERED_CORNERS = enum.auto()
    '''Create pointed corners.'''
    ROUND_CORNERS = enum.auto()
    '''Create rounded corners in the line or outline.'''
    BEVELED_CORNERS = enum.auto()
    '''Beveled (square off) corners in the line or outline.'''

class LineTypes(enum.Enum):
    NONE = enum.auto()
    '''Not used line'''
    SOLID = enum.auto()
    '''Solid line.'''
    DASHED = enum.auto()
    '''Dashed line.'''
    BEHIND_FILL = enum.auto()
    '''The line must be rendered behind fill of shape.'''
    SCALE_PEN = enum.auto()
    '''The line width is scaled relative to size of shape.'''

class ParagraphHorizontalAlignment(enum.Enum):
    NO_ALIGN = enum.auto()
    '''Do not align text with the text frame.'''
    LEFT = enum.auto()
    '''Align text with the left side of the text frame.'''
    CENTER = enum.auto()
    '''Center text between the left and right sides of the text frame.'''
    RIGHT = enum.auto()
    '''Align text with the right side of the text frame.'''
    FULL_JUSTIFY = enum.auto()
    '''Align text, excluding the last line, with the left and right sides of the text frame.'''
    FORCE_JUSTIFY = enum.auto()
    '''Align text with both left and right sides of the text frame.'''

class PathJumpTypes(enum.Enum):
    MOVE_TO = enum.auto()
    '''The point is not connected to the previous one. Uses for visible points.'''
    LINE_TO = enum.auto()
    '''The point is connected to the previous one through a straight line. Uses for visible points.'''
    BEZIER_TO = enum.auto()
    '''The point is connected to the previous visible point through a bi-cubic bezier curve. Uses for visible points.'''
    BEZIER_SUPPORT = enum.auto()
    '''Uses for invisible auxiliary point to build a bi-cubic bezier curve.'''

class TileOffsetTypes(enum.Enum):
    ROW_OFFSET = enum.auto()
    '''Offset between adjacent rows.'''
    COLUMN_OFFSET = enum.auto()
    '''Offset between adjacent columns.'''

class Units(enum.Enum):
    INCHES = enum.auto()
    '''The inches.'''
    METERS = enum.auto()
    '''The meters.'''

