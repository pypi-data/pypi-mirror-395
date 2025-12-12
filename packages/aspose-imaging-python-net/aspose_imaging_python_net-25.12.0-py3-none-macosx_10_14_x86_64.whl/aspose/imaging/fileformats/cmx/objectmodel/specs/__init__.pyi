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

class CmxArrowSpec(CmxPathSpec):
    '''Represents geometric info specified for outline arrow (marker).'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.specs.CmxPathPointSpec]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.fileformats.cmx.objectmodel.specs.CmxPathPointSpec]) -> None:
        '''Sets the points.'''
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
    def arrow_offset(self) -> float:
        '''Gets the arrow offset.'''
        raise NotImplementedError()
    
    @arrow_offset.setter
    def arrow_offset(self, value : float) -> None:
        '''Sets the arrow offset.'''
        raise NotImplementedError()
    

class CmxEllipseSpec(ICmxObjectSpec):
    '''Represents geometric info specified for an ellipse.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def angle1(self) -> float:
        '''Gets the first angle used for defining of pie sector.
        Does no affect if :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.specs.CmxEllipseSpec.pie` is ``false``.
        Measures in radians.'''
        raise NotImplementedError()
    
    @angle1.setter
    def angle1(self, value : float) -> None:
        '''Sets the first angle used for defining of pie sector.
        Does no affect if :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.specs.CmxEllipseSpec.pie` is ``false``.
        Measures in radians.'''
        raise NotImplementedError()
    
    @property
    def angle2(self) -> float:
        '''Gets the second angle used for defining of pie sector.
        Does no affect if :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.specs.CmxEllipseSpec.pie` is ``false``.
        Measures in radians.'''
        raise NotImplementedError()
    
    @angle2.setter
    def angle2(self, value : float) -> None:
        '''Sets the second angle used for defining of pie sector.
        Does no affect if :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.specs.CmxEllipseSpec.pie` is ``false``.
        Measures in radians.'''
        raise NotImplementedError()
    
    @property
    def rotation(self) -> float:
        '''Gets the angle of rotation of the ellipse.
        Measures in radians.'''
        raise NotImplementedError()
    
    @rotation.setter
    def rotation(self, value : float) -> None:
        '''Sets the angle of rotation of the ellipse.
        Measures in radians.'''
        raise NotImplementedError()
    
    @property
    def pie(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cmx.objectmodel.specs.CmxEllipseSpec` is a pie.'''
        raise NotImplementedError()
    
    @pie.setter
    def pie(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cmx.objectmodel.specs.CmxEllipseSpec` is a pie.'''
        raise NotImplementedError()
    
    @property
    def center_x(self) -> float:
        '''Gets the X coordinate for the center of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @center_x.setter
    def center_x(self, value : float) -> None:
        '''Sets the X coordinate for the center of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def center_y(self) -> float:
        '''Gets the Y coordinate for the center of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @center_y.setter
    def center_y(self, value : float) -> None:
        '''Sets the Y coordinate for the center of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def diameter_x(self) -> float:
        '''Gets the diameter for X dimension of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @diameter_x.setter
    def diameter_x(self, value : float) -> None:
        '''Sets the diameter for X dimension of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def diameter_y(self) -> float:
        '''Gets the diameter for Y dimension of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @diameter_y.setter
    def diameter_y(self, value : float) -> None:
        '''Sets the diameter for Y dimension of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def bounding_box(self) -> aspose.imaging.RectangleF:
        '''Gets the bounding box.'''
        raise NotImplementedError()
    
    @bounding_box.setter
    def bounding_box(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounding box.'''
        raise NotImplementedError()
    

class CmxImageSpec(ICmxObjectSpec):
    '''Represents info specified for raster images.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def bound_box(self) -> aspose.imaging.RectangleF:
        '''Gets the bound box.'''
        raise NotImplementedError()
    
    @bound_box.setter
    def bound_box(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bound box.'''
        raise NotImplementedError()
    
    @property
    def crop_box(self) -> aspose.imaging.RectangleF:
        '''Gets the crop box.'''
        raise NotImplementedError()
    
    @crop_box.setter
    def crop_box(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the crop box.'''
        raise NotImplementedError()
    
    @property
    def matrix(self) -> aspose.imaging.Matrix:
        '''Gets the transformation matrix.'''
        raise NotImplementedError()
    
    @matrix.setter
    def matrix(self, value : aspose.imaging.Matrix) -> None:
        '''Sets the transformation matrix.'''
        raise NotImplementedError()
    
    @property
    def image_type(self) -> int:
        '''Gets the type of the image.'''
        raise NotImplementedError()
    
    @image_type.setter
    def image_type(self, value : int) -> None:
        '''Sets the type of the image.'''
        raise NotImplementedError()
    
    @property
    def images(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.specs.CmxRasterImage]:
        '''Gets the images.'''
        raise NotImplementedError()
    
    @images.setter
    def images(self, value : List[aspose.imaging.fileformats.cmx.objectmodel.specs.CmxRasterImage]) -> None:
        '''Sets the images.'''
        raise NotImplementedError()
    
    @property
    def is_cmx_3_image(self) -> bool:
        '''Gets a value indicating whether this instance is CMX3 image.'''
        raise NotImplementedError()
    
    @is_cmx_3_image.setter
    def is_cmx_3_image(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is CMX3 image.'''
        raise NotImplementedError()
    

class CmxPathPointSpec:
    '''Represents geometric info specified for a path point.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def x(self) -> float:
        '''Gets the X coordinate of the point.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @x.setter
    def x(self, value : float) -> None:
        '''Sets the X coordinate of the point.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def y(self) -> float:
        '''Gets the Y coordinate of the point.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @y.setter
    def y(self, value : float) -> None:
        '''Sets the Y coordinate of the point.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def jump_type(self) -> aspose.imaging.fileformats.cmx.objectmodel.enums.PathJumpTypes:
        '''Gets the type of the jump.'''
        raise NotImplementedError()
    
    @jump_type.setter
    def jump_type(self, value : aspose.imaging.fileformats.cmx.objectmodel.enums.PathJumpTypes) -> None:
        '''Sets the type of the jump.'''
        raise NotImplementedError()
    
    @property
    def is_closed_path(self) -> bool:
        '''Gets a value indicating whether this point closes its path.'''
        raise NotImplementedError()
    
    @is_closed_path.setter
    def is_closed_path(self, value : bool) -> None:
        '''Sets a value indicating whether this point closes its path.'''
        raise NotImplementedError()
    
    @property
    def bezier_order(self) -> int:
        '''Gets the bezier order.'''
        raise NotImplementedError()
    
    @bezier_order.setter
    def bezier_order(self, value : int) -> None:
        '''Sets the bezier order.'''
        raise NotImplementedError()
    

class CmxPathSpec(ICmxObjectSpec):
    '''Represents geometric info specified for a path.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.specs.CmxPathPointSpec]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.fileformats.cmx.objectmodel.specs.CmxPathPointSpec]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> int:
        '''Gets the type.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : int) -> None:
        '''Sets the type.'''
        raise NotImplementedError()
    

class CmxRasterImage(ICmxObjectSpec):
    '''Represents the data specified for raster images.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def type(self) -> int:
        '''Gets the type of the image.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : int) -> None:
        '''Sets the type of the image.'''
        raise NotImplementedError()
    
    @property
    def compression(self) -> int:
        '''Gets the compression.'''
        raise NotImplementedError()
    
    @compression.setter
    def compression(self, value : int) -> None:
        '''Sets the compression.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the size of the image.
        Measures in bytes.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Sets the size of the image.
        Measures in bytes.'''
        raise NotImplementedError()
    
    @property
    def compressed_size(self) -> int:
        '''Gets the compressed size of the image.
        Measures in bytes.'''
        raise NotImplementedError()
    
    @compressed_size.setter
    def compressed_size(self, value : int) -> None:
        '''Sets the compressed size of the image.
        Measures in bytes.'''
        raise NotImplementedError()
    
    @property
    def is_mask(self) -> bool:
        '''Gets a value indicating whether this instance is mask.'''
        raise NotImplementedError()
    
    @is_mask.setter
    def is_mask(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is mask.'''
        raise NotImplementedError()
    
    @property
    def color_model(self) -> int:
        '''Gets the color model.'''
        raise NotImplementedError()
    
    @color_model.setter
    def color_model(self, value : int) -> None:
        '''Sets the color model.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width of the image.
        Measures in pixels.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the width of the image.
        Measures in pixels.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height of the image.
        Measures in pixels.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the height of the image.
        Measures in pixels.'''
        raise NotImplementedError()
    
    @property
    def bits_per_pixel(self) -> int:
        '''Gets the bits per pixel.'''
        raise NotImplementedError()
    
    @bits_per_pixel.setter
    def bits_per_pixel(self, value : int) -> None:
        '''Sets the bits per pixel.'''
        raise NotImplementedError()
    
    @property
    def bytes_per_line(self) -> int:
        '''Gets the size of the line.
        Measures in bytes.'''
        raise NotImplementedError()
    
    @bytes_per_line.setter
    def bytes_per_line(self, value : int) -> None:
        '''Sets the size of the line.
        Measures in bytes.'''
        raise NotImplementedError()
    
    @property
    def color_palette(self) -> List[int]:
        '''Gets the color palette array.
        Elements is ARGB color values represents in :py:class:`int`'''
        raise NotImplementedError()
    
    @color_palette.setter
    def color_palette(self, value : List[int]) -> None:
        '''Sets the color palette array.
        Elements is ARGB color values represents in :py:class:`int`'''
        raise NotImplementedError()
    
    @property
    def raw_data(self) -> List[int]:
        '''Gets the raw byte data of the image.'''
        raise NotImplementedError()
    
    @raw_data.setter
    def raw_data(self, value : List[int]) -> None:
        '''Sets the raw byte data of the image.'''
        raise NotImplementedError()
    

class CmxRectangleSpec(ICmxObjectSpec):
    '''Represents geometric info specified for a rectangle.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def center_x(self) -> float:
        '''Gets the X coordinate for the center of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @center_x.setter
    def center_x(self, value : float) -> None:
        '''Sets the X coordinate for the center of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def center_y(self) -> float:
        '''Gets the Y coordinate for the center of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @center_y.setter
    def center_y(self, value : float) -> None:
        '''Sets the Y coordinate for the center of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the width of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the width of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the height of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the height of the rectangle.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def radius(self) -> float:
        '''Gets the radius of rounded rectangle corners.
        If its value is ``0`` then the rectangle has not rounded corners.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @radius.setter
    def radius(self, value : float) -> None:
        '''Sets the radius of rounded rectangle corners.
        If its value is ``0`` then the rectangle has not rounded corners.
        Measures in common document distance units.'''
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets the angle of rotation of the rectangle.
        Measures in radians.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets the angle of rotation of the rectangle.
        Measures in radians.'''
        raise NotImplementedError()
    

class CmxTextBlockSpec(ICmxObjectSpec):
    '''Represents info specified for text blocks.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def paragraph_style(self) -> aspose.imaging.fileformats.cmx.objectmodel.styles.CmxParagraphStyle:
        '''Gets the paragraph style.'''
        raise NotImplementedError()
    
    @paragraph_style.setter
    def paragraph_style(self, value : aspose.imaging.fileformats.cmx.objectmodel.styles.CmxParagraphStyle) -> None:
        '''Sets the paragraph style.'''
        raise NotImplementedError()
    
    @property
    def font(self) -> aspose.imaging.Font:
        '''Gets the font.'''
        raise NotImplementedError()
    
    @font.setter
    def font(self, value : aspose.imaging.Font) -> None:
        '''Sets the font.'''
        raise NotImplementedError()
    
    @property
    def matrix(self) -> aspose.imaging.Matrix:
        '''Gets the transformation matrix.'''
        raise NotImplementedError()
    
    @matrix.setter
    def matrix(self, value : aspose.imaging.Matrix) -> None:
        '''Sets the transformation matrix.'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the text.'''
        raise NotImplementedError()
    
    @text.setter
    def text(self, value : str) -> None:
        '''Sets the text.'''
        raise NotImplementedError()
    
    @property
    def char_locations(self) -> List[aspose.imaging.PointF]:
        '''Gets the character locations.'''
        raise NotImplementedError()
    
    @char_locations.setter
    def char_locations(self, value : List[aspose.imaging.PointF]) -> None:
        '''Sets the character locations.'''
        raise NotImplementedError()
    

class ICmxObjectSpec:
    '''Specification of graphics object'''
    

