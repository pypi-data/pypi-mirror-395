"""The namespace handles Cdr file format processing."""
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

class CdrColor:
    '''The cdr color'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def color_model(self) -> aspose.imaging.fileformats.cdr.const.CdrColorModel:
        '''Gets the color model.'''
        raise NotImplementedError()
    
    @color_model.setter
    def color_model(self, value : aspose.imaging.fileformats.cdr.const.CdrColorModel) -> None:
        '''Sets the color model.'''
        raise NotImplementedError()
    
    @property
    def color_value(self) -> int:
        '''Gets the color value.'''
        raise NotImplementedError()
    
    @color_value.setter
    def color_value(self, value : int) -> None:
        '''Sets the color value.'''
        raise NotImplementedError()
    
    @property
    def rgb_color_value(self) -> int:
        '''Gets the RGB color value.'''
        raise NotImplementedError()
    
    @rgb_color_value.setter
    def rgb_color_value(self, value : int) -> None:
        '''Sets the RGB color value.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> int:
        '''Gets the opacity.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : int) -> None:
        '''Sets the opacity.'''
        raise NotImplementedError()
    

class CdrGradient:
    '''The cdr gradient'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.cdr.types.CdrGradient` class.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> int:
        '''Gets the type.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : int) -> None:
        '''Sets the type.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> int:
        '''Gets the mode.'''
        raise NotImplementedError()
    
    @mode.setter
    def mode(self, value : int) -> None:
        '''Sets the mode.'''
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets the angle.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets the angle.'''
        raise NotImplementedError()
    
    @property
    def mid_point(self) -> float:
        '''Gets the mid point.'''
        raise NotImplementedError()
    
    @mid_point.setter
    def mid_point(self, value : float) -> None:
        '''Sets the mid point.'''
        raise NotImplementedError()
    
    @property
    def edge_offset(self) -> int:
        '''Gets the edge offset.'''
        raise NotImplementedError()
    
    @edge_offset.setter
    def edge_offset(self, value : int) -> None:
        '''Sets the edge offset.'''
        raise NotImplementedError()
    
    @property
    def center_x_offset(self) -> int:
        '''Gets the center x offset.'''
        raise NotImplementedError()
    
    @center_x_offset.setter
    def center_x_offset(self, value : int) -> None:
        '''Sets the center x offset.'''
        raise NotImplementedError()
    
    @property
    def center_y_offset(self) -> int:
        '''Gets the center y offset.'''
        raise NotImplementedError()
    
    @center_y_offset.setter
    def center_y_offset(self, value : int) -> None:
        '''Sets the center y offset.'''
        raise NotImplementedError()
    
    @property
    def stops(self) -> List[aspose.imaging.fileformats.cdr.types.CdrGradientStop]:
        '''Gets the stops.'''
        raise NotImplementedError()
    
    @stops.setter
    def stops(self, value : List[aspose.imaging.fileformats.cdr.types.CdrGradientStop]) -> None:
        '''Sets the stops.'''
        raise NotImplementedError()
    

class CdrGradientStop:
    '''The cdr gradient stop'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def color(self) -> aspose.imaging.fileformats.cdr.types.CdrColor:
        '''Gets the color.'''
        raise NotImplementedError()
    
    @color.setter
    def color(self, value : aspose.imaging.fileformats.cdr.types.CdrColor) -> None:
        '''Sets the color.'''
        raise NotImplementedError()
    
    @property
    def offset(self) -> float:
        '''Gets the offset.'''
        raise NotImplementedError()
    
    @offset.setter
    def offset(self, value : float) -> None:
        '''Sets the offset.'''
        raise NotImplementedError()
    

class CdrImageFill:
    '''The cdr image fill'''
    
    def __init__(self, id : int, width : float, height : float, is_relative : bool, x_offset : float, y_offset : float, rcp_offset : float, flags : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.cdr.types.CdrImageFill` class.
        
        :param id: The identifier.
        :param width: The width.
        :param height: The height.
        :param is_relative: if set to ``true`` [is relative].
        :param x_offset: The x offset.
        :param y_offset: The y offset.
        :param rcp_offset: The RPC offset.
        :param flags: The flags.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    
    @property
    def is_relative(self) -> bool:
        '''Gets a value indicating whether this instance is relative.'''
        raise NotImplementedError()
    
    @is_relative.setter
    def is_relative(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is relative.'''
        raise NotImplementedError()
    
    @property
    def x_offset(self) -> float:
        '''Gets the x offset.'''
        raise NotImplementedError()
    
    @x_offset.setter
    def x_offset(self, value : float) -> None:
        '''Sets the x offset.'''
        raise NotImplementedError()
    
    @property
    def y_offset(self) -> float:
        '''Gets the y offset.'''
        raise NotImplementedError()
    
    @y_offset.setter
    def y_offset(self, value : float) -> None:
        '''Sets the y offset.'''
        raise NotImplementedError()
    
    @property
    def rcp_offset(self) -> float:
        '''Gets the RCP offset.'''
        raise NotImplementedError()
    
    @rcp_offset.setter
    def rcp_offset(self, value : float) -> None:
        '''Sets the RCP offset.'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> int:
        '''Gets the flags.'''
        raise NotImplementedError()
    
    @flags.setter
    def flags(self, value : int) -> None:
        '''Sets the flags.'''
        raise NotImplementedError()
    

class CdrTextCollection:
    '''The Cdr text collection'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add(self, key : int, cdr_text : aspose.imaging.fileformats.cdr.objects.CdrText) -> None:
        '''Adds the text.
        
        :param key: Key of the text.
        :param cdr_text: The CDR text.'''
        raise NotImplementedError()
    
    def get_text(self, key : int) -> List[aspose.imaging.fileformats.cdr.objects.CdrText]:
        '''Gets the text.
        
        :param key: Key of the text
        :returns: The cdr text instance'''
        raise NotImplementedError()
    

class PointD:
    '''The point double'''
    
    @overload
    def __init__(self, x : float, y : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.cdr.types.PointD` struct.
        
        :param x: The x value.
        :param y: The y value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def to_point_f(self) -> aspose.imaging.PointF:
        '''Converts :py:class:`aspose.imaging.PointF`  to the :py:class:`aspose.imaging.fileformats.cdr.types.PointD` structure.
        
        :returns: The :py:class:`aspose.imaging.PointF` structure'''
        raise NotImplementedError()
    
    def from_point_f(self, point : aspose.imaging.PointF) -> None:
        '''Converts :py:class:`aspose.imaging.fileformats.cdr.types.PointD`  to the :py:class:`aspose.imaging.PointF` structure.
        
        :param point: The :py:class:`aspose.imaging.fileformats.cdr.types.PointD` structure.'''
        raise NotImplementedError()
    
    @property
    def x(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @x.setter
    def x(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def y(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @y.setter
    def y(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    

