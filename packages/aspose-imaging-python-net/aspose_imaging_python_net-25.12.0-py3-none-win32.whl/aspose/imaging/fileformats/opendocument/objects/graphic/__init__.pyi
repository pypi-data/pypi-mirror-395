"""The Open document graphic objects"""
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

class OdAngleEllipse(OdStyledObject):
    '''The Enhanced angle ellipse'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdAngleEllipse` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def start_angle(self) -> float:
        '''Gets the start angle.'''
        raise NotImplementedError()
    
    @start_angle.setter
    def start_angle(self, value : float) -> None:
        '''Sets the start angle.'''
        raise NotImplementedError()
    
    @property
    def end_angle(self) -> float:
        '''Gets the end angle.'''
        raise NotImplementedError()
    
    @end_angle.setter
    def end_angle(self, value : float) -> None:
        '''Sets the end angle.'''
        raise NotImplementedError()
    
    @property
    def closed(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdAngleEllipse` is closed.'''
        raise NotImplementedError()
    
    @closed.setter
    def closed(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdAngleEllipse` is closed.'''
        raise NotImplementedError()
    
    @property
    def kind(self) -> aspose.imaging.fileformats.opendocument.enums.OdObjectKind:
        '''Gets the kind.'''
        raise NotImplementedError()
    
    @kind.setter
    def kind(self, value : aspose.imaging.fileformats.opendocument.enums.OdObjectKind) -> None:
        '''Sets the kind.'''
        raise NotImplementedError()
    

class OdArc(OdGraphicObject):
    '''The Enhanced Arc'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdArc` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def is_arc_to(self) -> bool:
        '''Gets a value indicating whether this instance is arc to.'''
        raise NotImplementedError()
    
    @is_arc_to.setter
    def is_arc_to(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is arc to.'''
        raise NotImplementedError()
    
    @property
    def is_elliptical_qundrant_x(self) -> bool:
        '''Gets a value indicating whether this instance is elliptical quadrant x.'''
        raise NotImplementedError()
    
    @is_elliptical_qundrant_x.setter
    def is_elliptical_qundrant_x(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is elliptical quadrant x.'''
        raise NotImplementedError()
    
    @property
    def is_elliptical_qundrant_y(self) -> bool:
        '''Gets a value indicating whether this instance is elliptical quadrant y.'''
        raise NotImplementedError()
    
    @is_elliptical_qundrant_y.setter
    def is_elliptical_qundrant_y(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is elliptical quadrant y.'''
        raise NotImplementedError()
    
    @property
    def clock_wise(self) -> bool:
        '''Gets a value indicating whether [clock wise].'''
        raise NotImplementedError()
    
    @clock_wise.setter
    def clock_wise(self, value : bool) -> None:
        '''Sets a value indicating whether [clock wise].'''
        raise NotImplementedError()
    
    @property
    def point1(self) -> aspose.imaging.PointF:
        '''Gets the point1.'''
        raise NotImplementedError()
    
    @point1.setter
    def point1(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point1.'''
        raise NotImplementedError()
    
    @property
    def point2(self) -> aspose.imaging.PointF:
        '''Gets the point2.'''
        raise NotImplementedError()
    
    @point2.setter
    def point2(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point2.'''
        raise NotImplementedError()
    
    @property
    def point3(self) -> aspose.imaging.PointF:
        '''Gets the point3.'''
        raise NotImplementedError()
    
    @point3.setter
    def point3(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point3.'''
        raise NotImplementedError()
    
    @property
    def point4(self) -> aspose.imaging.PointF:
        '''Gets the point4.'''
        raise NotImplementedError()
    
    @point4.setter
    def point4(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point4.'''
        raise NotImplementedError()
    

class OdCircle(OdAngleEllipse):
    '''The circle object'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdCircle` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def start_angle(self) -> float:
        '''Gets the start angle.'''
        raise NotImplementedError()
    
    @start_angle.setter
    def start_angle(self, value : float) -> None:
        '''Sets the start angle.'''
        raise NotImplementedError()
    
    @property
    def end_angle(self) -> float:
        '''Gets the end angle.'''
        raise NotImplementedError()
    
    @end_angle.setter
    def end_angle(self, value : float) -> None:
        '''Sets the end angle.'''
        raise NotImplementedError()
    
    @property
    def closed(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdAngleEllipse` is closed.'''
        raise NotImplementedError()
    
    @closed.setter
    def closed(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdAngleEllipse` is closed.'''
        raise NotImplementedError()
    
    @property
    def kind(self) -> aspose.imaging.fileformats.opendocument.enums.OdObjectKind:
        '''Gets the kind.'''
        raise NotImplementedError()
    
    @kind.setter
    def kind(self, value : aspose.imaging.fileformats.opendocument.enums.OdObjectKind) -> None:
        '''Sets the kind.'''
        raise NotImplementedError()
    

class OdClosePath(OdGraphicObject):
    '''The close path'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdClosePath` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    

class OdConnector(OdStyledObject):
    '''The  connector'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdConnector` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def path_commands(self) -> List[aspose.imaging.fileformats.opendocument.objects.graphic.OdGraphicObject]:
        '''Gets the path commands.'''
        raise NotImplementedError()
    
    @path_commands.setter
    def path_commands(self, value : List[aspose.imaging.fileformats.opendocument.objects.graphic.OdGraphicObject]) -> None:
        '''Sets the path commands.'''
        raise NotImplementedError()
    
    @property
    def point1(self) -> aspose.imaging.PointF:
        '''Gets the point1.'''
        raise NotImplementedError()
    
    @point1.setter
    def point1(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point1.'''
        raise NotImplementedError()
    
    @property
    def point2(self) -> aspose.imaging.PointF:
        '''Gets the point2.'''
        raise NotImplementedError()
    
    @point2.setter
    def point2(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point2.'''
        raise NotImplementedError()
    

class OdContainer(OdStyledObject):
    '''The Container'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdContainer` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class OdCurveTo(OdGraphicObject):
    '''The Enhanced CurveTo'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdCurveTo` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.PointF]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.PointF]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    

class OdCustomShape(OdStyledObject):
    '''The open document custom-shape.'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdCustomShape` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def style_name(self) -> str:
        '''Gets the name of the style.'''
        raise NotImplementedError()
    
    @style_name.setter
    def style_name(self, value : str) -> None:
        '''Sets the name of the style.'''
        raise NotImplementedError()
    
    @property
    def text_style_name(self) -> str:
        '''Gets the name of the text style.'''
        raise NotImplementedError()
    
    @text_style_name.setter
    def text_style_name(self, value : str) -> None:
        '''Sets the name of the text style.'''
        raise NotImplementedError()
    
    @property
    def layer(self) -> str:
        '''Gets the layer.'''
        raise NotImplementedError()
    
    @layer.setter
    def layer(self, value : str) -> None:
        '''Sets the layer.'''
        raise NotImplementedError()
    

class OdEllipticalQundrant(OdGraphicObject):
    '''The elliptical quadrant'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdEllipticalQundrant` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.PointF:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    
    @property
    def axis_x(self) -> bool:
        '''Gets a value indicating whether [axis x].'''
        raise NotImplementedError()
    
    @axis_x.setter
    def axis_x(self, value : bool) -> None:
        '''Sets a value indicating whether [axis x].'''
        raise NotImplementedError()
    

class OdEndPath(OdGraphicObject):
    '''The enhanced end path'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdEndPath` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def fill(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdEndPath` is fill.'''
        raise NotImplementedError()
    
    @fill.setter
    def fill(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdEndPath` is fill.'''
        raise NotImplementedError()
    

class OdEnhancedGeometry(OdGraphicObject):
    '''The Enhanced geometry object.'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdEnhancedGeometry` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def enhanced_path(self) -> List[aspose.imaging.fileformats.opendocument.objects.graphic.OdGraphicObject]:
        '''Gets the enhanced path.'''
        raise NotImplementedError()
    
    @enhanced_path.setter
    def enhanced_path(self, value : List[aspose.imaging.fileformats.opendocument.objects.graphic.OdGraphicObject]) -> None:
        '''Sets the enhanced path.'''
        raise NotImplementedError()
    
    @property
    def view_box(self) -> aspose.imaging.Rectangle:
        '''Gets the view box.'''
        raise NotImplementedError()
    
    @view_box.setter
    def view_box(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the view box.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> str:
        '''Gets the type.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : str) -> None:
        '''Sets the type.'''
        raise NotImplementedError()
    

class OdEquation(OdGraphicObject):
    '''The open document equation'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdEquation` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets the name.'''
        raise NotImplementedError()
    
    @property
    def formula(self) -> str:
        '''Gets the formula.'''
        raise NotImplementedError()
    
    @formula.setter
    def formula(self, value : str) -> None:
        '''Sets the formula.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> float:
        '''Gets the value.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : float) -> None:
        '''Sets the value.'''
        raise NotImplementedError()
    

class OdFrame(OdStyledObject):
    '''The open document object frame'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdFrame` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class OdGraphicObject(aspose.imaging.fileformats.opendocument.OdObject):
    '''The open document graphic object.'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdGraphicObject` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    

class OdImageObject(OdGraphicObject):
    '''The open document image'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdImageObject` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def image_link(self) -> str:
        '''Gets the image link.'''
        raise NotImplementedError()
    
    @image_link.setter
    def image_link(self, value : str) -> None:
        '''Sets the image link.'''
        raise NotImplementedError()
    
    @property
    def bitmap(self) -> List[int]:
        '''Gets the bitmap.'''
        raise NotImplementedError()
    
    @bitmap.setter
    def bitmap(self, value : List[int]) -> None:
        '''Sets the bitmap.'''
        raise NotImplementedError()
    

class OdLine(OdStyledObject):
    '''The line object'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdPage` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def point1(self) -> aspose.imaging.PointF:
        '''Gets the point1.'''
        raise NotImplementedError()
    
    @point1.setter
    def point1(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point1.'''
        raise NotImplementedError()
    
    @property
    def point2(self) -> aspose.imaging.PointF:
        '''Gets the point2.'''
        raise NotImplementedError()
    
    @point2.setter
    def point2(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point2.'''
        raise NotImplementedError()
    

class OdLineTo(OdGraphicObject):
    '''The enhanced lineTo'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdLineTo` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def coordinates(self) -> aspose.imaging.PointF:
        '''Gets the coordinates.'''
        raise NotImplementedError()
    
    @coordinates.setter
    def coordinates(self, value : aspose.imaging.PointF) -> None:
        '''Sets the coordinates.'''
        raise NotImplementedError()
    
    @property
    def vertical(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdLineTo` is vertical.'''
        raise NotImplementedError()
    
    @vertical.setter
    def vertical(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdLineTo` is vertical.'''
        raise NotImplementedError()
    
    @property
    def horizontal(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdLineTo` is vertical.'''
        raise NotImplementedError()
    
    @horizontal.setter
    def horizontal(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdLineTo` is vertical.'''
        raise NotImplementedError()
    

class OdList(OdStyledObject):
    '''The List object'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdList` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class OdListItem(OdGraphicObject):
    '''The list item'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdListItem` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    

class OdMarker(OdGraphicObject):
    '''The Marker'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdMarker` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def path_commands(self) -> List[aspose.imaging.fileformats.opendocument.objects.graphic.OdGraphicObject]:
        '''Gets the path commands.'''
        raise NotImplementedError()
    
    @path_commands.setter
    def path_commands(self, value : List[aspose.imaging.fileformats.opendocument.objects.graphic.OdGraphicObject]) -> None:
        '''Sets the path commands.'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets the name.'''
        raise NotImplementedError()
    

class OdMeasure(OdStyledObject):
    '''The Measure'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdMeasure` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def point1(self) -> aspose.imaging.PointF:
        '''Gets the point1.'''
        raise NotImplementedError()
    
    @point1.setter
    def point1(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point1.'''
        raise NotImplementedError()
    
    @property
    def point2(self) -> aspose.imaging.PointF:
        '''Gets the point2.'''
        raise NotImplementedError()
    
    @point2.setter
    def point2(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point2.'''
        raise NotImplementedError()
    
    @property
    def point3(self) -> aspose.imaging.PointF:
        '''Gets the point3.'''
        raise NotImplementedError()
    
    @point3.setter
    def point3(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point3.'''
        raise NotImplementedError()
    
    @property
    def point4(self) -> aspose.imaging.PointF:
        '''Gets the point4.'''
        raise NotImplementedError()
    
    @point4.setter
    def point4(self, value : aspose.imaging.PointF) -> None:
        '''Sets the point4.'''
        raise NotImplementedError()
    

class OdMoveTo(OdGraphicObject):
    '''The Enhanced moveTo'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdMoveTo` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def coordinates(self) -> aspose.imaging.PointF:
        '''Gets the coordinates.'''
        raise NotImplementedError()
    
    @coordinates.setter
    def coordinates(self, value : aspose.imaging.PointF) -> None:
        '''Sets the coordinates.'''
        raise NotImplementedError()
    

class OdNoFillPath(OdGraphicObject):
    '''The no fill path marker'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdNoFillPath` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    

class OdNoStrokePath(OdGraphicObject):
    '''Specifies that the current set of sub-paths will not be stroked.'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdNoStrokePath` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    

class OdPage(OdGraphicObject):
    '''The Open document page.'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdPage` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def name(self) -> str:
        '''Gets the name.'''
        raise NotImplementedError()
    
    @name.setter
    def name(self, value : str) -> None:
        '''Sets the name.'''
        raise NotImplementedError()
    
    @property
    def master_page_name(self) -> str:
        '''Gets the name of the master page.'''
        raise NotImplementedError()
    
    @master_page_name.setter
    def master_page_name(self, value : str) -> None:
        '''Sets the name of the master page.'''
        raise NotImplementedError()
    
    @property
    def style_name(self) -> str:
        '''Gets the name of the style.'''
        raise NotImplementedError()
    
    @style_name.setter
    def style_name(self, value : str) -> None:
        '''Sets the name of the style.'''
        raise NotImplementedError()
    

class OdPath(OdStyledObject):
    '''The open document object path'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdPath` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def style_name(self) -> str:
        '''Gets the name of the style.'''
        raise NotImplementedError()
    
    @style_name.setter
    def style_name(self, value : str) -> None:
        '''Sets the name of the style.'''
        raise NotImplementedError()
    
    @property
    def text_style_name(self) -> str:
        '''Gets the name of the text style.'''
        raise NotImplementedError()
    
    @text_style_name.setter
    def text_style_name(self, value : str) -> None:
        '''Sets the name of the text style.'''
        raise NotImplementedError()
    
    @property
    def layer(self) -> str:
        '''Gets the layer.'''
        raise NotImplementedError()
    
    @layer.setter
    def layer(self, value : str) -> None:
        '''Sets the layer.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> str:
        '''Gets the data.'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : str) -> None:
        '''Sets the data.'''
        raise NotImplementedError()
    
    @property
    def enhanced_path(self) -> List[aspose.imaging.fileformats.opendocument.objects.graphic.OdGraphicObject]:
        '''Gets the enhanced path.'''
        raise NotImplementedError()
    
    @enhanced_path.setter
    def enhanced_path(self, value : List[aspose.imaging.fileformats.opendocument.objects.graphic.OdGraphicObject]) -> None:
        '''Sets the enhanced path.'''
        raise NotImplementedError()
    

class OdPolyLine(OdPolygon):
    '''The polyline'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdPolyLine` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.PointF]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.PointF]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    

class OdPolygon(OdStyledObject):
    '''The polygon'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdPolygon` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.PointF]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.PointF]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    

class OdRectangle(OdStyledObject):
    '''The rectangle object'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdRectangle` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def corner_radius(self) -> float:
        '''Gets the corner radius.'''
        raise NotImplementedError()
    
    @corner_radius.setter
    def corner_radius(self, value : float) -> None:
        '''Sets the corner radius.'''
        raise NotImplementedError()
    

class OdShortCurveTo(OdCurveTo):
    '''The short CurveTo'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdShortCurveTo` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.PointF]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.PointF]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    

class OdStyledObject(OdGraphicObject):
    '''The open document styled graphic object.'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdStyledObject` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class OdText(aspose.imaging.fileformats.opendocument.OdObject):
    '''The text object'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.OdObject` class.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the text.'''
        raise NotImplementedError()
    
    @text.setter
    def text(self, value : str) -> None:
        '''Sets the text.'''
        raise NotImplementedError()
    

class OdTextBox(OdGraphicObject):
    '''The text box'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdTextBox` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class OdTextMeasure(OdStyledObject):
    '''The text measure'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdTextMeasure` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the value.'''
        raise NotImplementedError()
    
    @text.setter
    def text(self, value : str) -> None:
        '''Sets the value.'''
        raise NotImplementedError()
    
    @property
    def kind(self) -> aspose.imaging.fileformats.opendocument.enums.OdMeasureTextKind:
        '''Gets the kind.'''
        raise NotImplementedError()
    
    @kind.setter
    def kind(self, value : aspose.imaging.fileformats.opendocument.enums.OdMeasureTextKind) -> None:
        '''Sets the kind.'''
        raise NotImplementedError()
    

class OdTextParagraph(OdStyledObject):
    '''The text paragraph'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdTextParagraph` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the text.'''
        raise NotImplementedError()
    
    @text.setter
    def text(self, value : str) -> None:
        '''Sets the text.'''
        raise NotImplementedError()
    

class OdTextSpan(OdStyledObject):
    '''The text span'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.graphic.OdTextSpan` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def absolute_coordinates(self) -> bool:
        '''Gets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @absolute_coordinates.setter
    def absolute_coordinates(self, value : bool) -> None:
        '''Sets a value indicating whether [absolute coordinates].'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the text.'''
        raise NotImplementedError()
    
    @text.setter
    def text(self, value : str) -> None:
        '''Sets the text.'''
        raise NotImplementedError()
    

