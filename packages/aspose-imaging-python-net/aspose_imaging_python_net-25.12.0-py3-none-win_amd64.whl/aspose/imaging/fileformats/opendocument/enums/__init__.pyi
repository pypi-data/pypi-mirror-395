"""The Enumerations of open document"""
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

class OdGradientStyle(enum.Enum):
    AXIAL = enum.auto()
    '''The axial
    defines a bi-linear gradient that is also known as reflected gradient or mirrored linear gradient.
    It is created as a linear gradient that is mirrored (or reflected) along its axis.'''
    ELLIPSOID = enum.auto()
    '''The ellipsoid
    defines a gradient where the colors are blend along the radius from the center of an
    ellipsoid as defined with the draw:cx and draw:cy attributes.
    The length of the semi major-axis is the width of the filled area and the length of the semi-minor'''
    LINEAR = enum.auto()
    '''The linear
    defines a gradient where the colors blend along the linear axis of the gradient.
    The axis of the gradient is specified with the draw:angle attribute clockwise to the vertical axis.'''
    RADIAL = enum.auto()
    '''The radial
    defines a gradient where the colors are blend along the radius from the center
    of a circle as defined with the draw:cx and draw:cy attributes.
    The outside of the circle is filled with the end color.'''
    RECTANGLE = enum.auto()
    '''The rectangle
    defines a gradient that produces a rectangular blend from the center of the rectangle to the shortest
    of the 4 borders. The center of the rectangle is defined with the attributes draw:cx and draw:cy.
    The width of the rectangle is the width of the filled area,
    the height of the rectangle is the height of the filled area.
    The outside of the square is filled with the end color.'''
    SQUARE = enum.auto()
    '''The square
    defines a gradient that produces a square blend, imitating the visual perspective in a corridor or the
    aerial view of a pyramid.
    Also known as "box gradient" and "pyramidal gradient".
    The center of the square is defined with the draw:cx and draw:cy attributes.
    The width and height of the square is the minimum value of either the width or the height of the filled area.
    The outside of the square is filled with the end color.'''
    NONE = enum.auto()
    '''The gradient style is none'''

class OdMarkerType(enum.Enum):
    OD_NONE = enum.auto()
    '''The none marker'''
    OD_ARROW = enum.auto()
    '''The arrow marker'''
    OD_SQUERE = enum.auto()
    '''The square marker'''
    OD_CIRCLE = enum.auto()
    '''The circle marker'''

class OdMeasureTextKind(enum.Enum):
    NONE = enum.auto()
    '''The Measure text kind is none'''
    GAP = enum.auto()
    '''The Measure text kind is gap'''
    VALUE = enum.auto()
    '''The Measure text kind is value'''
    UNIT = enum.auto()
    '''The Measure text kind is unit'''

class OdObjectKind(enum.Enum):
    NONE = enum.auto()
    '''The object kind is none'''
    SECTION = enum.auto()
    '''The object kind is section'''
    CUT = enum.auto()
    '''The object kind is cut'''
    ARC = enum.auto()
    '''The object kind is arc'''

class OdTextAlignModeFlags(enum.Enum):
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
    JUSTIFY = enum.auto()
    '''The text must be aligned in a way each text line of a paragraph has the same length.'''
    BOTTOM = enum.auto()
    '''The reference point MUST be on the bottom edge of the bounding rectangle.'''
    BASELINE = enum.auto()
    '''The reference point MUST be on the baseline of the text.'''
    RTLREADING = enum.auto()
    '''The text MUST be laid out in right-to-left reading order, instead of the default left-to right order. This SHOULD
    be applied only when the font that is defined in the playback
    device context is either Hebrew or Arabic.'''
    HORIZONTAL = enum.auto()
    '''Represents Horisontal text algin sets (Left | Right | Center)'''
    VERTICAL = enum.auto()
    '''Represents Vertical text algin sets (Top | Bottom | Baseline)'''

