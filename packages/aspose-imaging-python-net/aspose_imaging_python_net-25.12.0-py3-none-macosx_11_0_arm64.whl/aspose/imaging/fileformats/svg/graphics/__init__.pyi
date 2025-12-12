"""The namespace for drawing on Svg."""
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

class SvgGraphics2D:
    '''Provides drawing commmands to compose an Svg image.'''
    
    @overload
    def __init__(self, width : int, height : int, dpi : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.svg.graphics.SvgGraphics2D` class.
        
        :param width: The width of the output Svg image.
        :param height: The width of the output Svg image.
        :param dpi: The device resolution, e.g. 96 dots per inch.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.fileformats.svg.SvgImage) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.svg.graphics.SvgGraphics2D` class.
        
        :param image: The image to perform drawing operations on.'''
        raise NotImplementedError()
    
    @overload
    def draw_image(self, image : aspose.imaging.RasterImage, origin : aspose.imaging.Point) -> None:
        '''Draws the specified image at the specified location.
        
        :param image: The drawn image.
        :param origin: The location of the drawn image.'''
        raise NotImplementedError()
    
    @overload
    def draw_image(self, image : aspose.imaging.RasterImage, origin : aspose.imaging.Point, size : aspose.imaging.Size) -> None:
        '''Draws the specified image of the specified size at the specified location.
        
        :param image: The drawn image.
        :param origin: The location of the drawn image.
        :param size: The desired size of the drawn image.'''
        raise NotImplementedError()
    
    @overload
    def draw_image(self, src_rect : aspose.imaging.Rectangle, dest_rect : aspose.imaging.Rectangle, image : aspose.imaging.RasterImage) -> None:
        '''Draws the specified portion of the specified image at the specified location and with the specified size.
        
        :param src_rect: The portion of the image object to draw.
        :param dest_rect: The location and size of the drawn image. The image is scaled to fit the rectangle.
        :param image: The image to draw.'''
        raise NotImplementedError()
    
    def draw_image_point_size(self, image : aspose.imaging.RasterImage, origin : aspose.imaging.Point, size : aspose.imaging.Size) -> None:
        '''Draws the specified image of the specified size at the specified location.
        
        :param image: The drawn image.
        :param origin: The location of the drawn image.
        :param size: The desired size of the drawn image.'''
        raise NotImplementedError()
    
    def draw_image_src_dst_rects(self, src_rect : aspose.imaging.Rectangle, dest_rect : aspose.imaging.Rectangle, image : aspose.imaging.RasterImage) -> None:
        '''Draws the specified portion of the specified image at the specified location and with the specified size.
        
        :param src_rect: The portion of the image object to draw.
        :param dest_rect: The location and size of the drawn image. The image is scaled to fit the rectangle.
        :param image: The image to draw.'''
        raise NotImplementedError()
    
    def draw_arc(self, pen : aspose.imaging.Pen, rect : aspose.imaging.Rectangle, start_angle : float, arc_angle : float) -> None:
        '''Draws an arc representing a portion of an ellipse specified by a Rectangle structure.
        
        :param pen: The pen to draw the outline of the figure.
        :param rect: The boundaries of the ellipse.
        :param start_angle: The angle in degrees measured clockwise from the x-axis to the starting point of the arc.
        :param arc_angle: The angle in degrees measured clockwise from the startAngle parameter to ending point of the arc.'''
        raise NotImplementedError()
    
    def fill_arc(self, pen : aspose.imaging.Pen, brush : aspose.imaging.Brush, rect : aspose.imaging.Rectangle, start_angle : float, arc_angle : float) -> None:
        '''Fills an arc representing a portion of an ellipse specified by a Rectangle structure.
        
        :param pen: The pen to draw the outline of the figure.
        :param brush: The brush to fill the interior of the figure.
        :param rect: The boundaries of the ellipse.
        :param start_angle: The angle in degrees measured clockwise from the x-axis to the starting point of the arc.
        :param arc_angle: The angle in degrees measured clockwise from the startAngle parameter to ending point of the arc.'''
        raise NotImplementedError()
    
    def draw_cubic_bezier(self, pen : aspose.imaging.Pen, pt1 : aspose.imaging.PointF, pt2 : aspose.imaging.PointF, pt3 : aspose.imaging.PointF, pt4 : aspose.imaging.PointF) -> None:
        '''Draws the cubic bezier.
        
        :param pen: The pen that determines the color, width, and style of the figure.
        :param pt1: The starting point of the curve.
        :param pt2: The first control point for the curve.
        :param pt3: The second control point for the curve.
        :param pt4: The ending point of the curve.'''
        raise NotImplementedError()
    
    def draw_string(self, font : aspose.imaging.Font, text : str, origin : aspose.imaging.Point, text_color : aspose.imaging.Color) -> None:
        '''Draws the text string.
        
        :param font: The font used to render text.
        :param text: The unicode text string.
        :param origin: The top-left corner of the text run.
        :param text_color: The text color.'''
        raise NotImplementedError()
    
    def draw_line(self, pen : aspose.imaging.Pen, x1 : int, y1 : int, x2 : int, y2 : int) -> None:
        '''Draws the line.
        
        :param pen: The pen that determines the color, width, and style of the figure.
        :param x1: The x-coordinate of the first point.
        :param y1: The y-coordinate of the first point.
        :param x2: The x-coordinate of the second point.
        :param y2: The y-coordinate of the second point.'''
        raise NotImplementedError()
    
    def draw_path(self, pen : aspose.imaging.Pen, path : aspose.imaging.GraphicsPath) -> None:
        '''Draws the path.
        
        :param pen: The pen to draw the outline of the figure.
        :param path: The path to draw.'''
        raise NotImplementedError()
    
    def fill_path(self, pen : aspose.imaging.Pen, brush : aspose.imaging.Brush, path : aspose.imaging.GraphicsPath) -> None:
        '''Fills the path.
        
        :param pen: The pen to draw the outline of the figure.
        :param brush: The brush to fill the interior of the figure.
        :param path: The path to draw.'''
        raise NotImplementedError()
    
    def draw_rectangle(self, pen : aspose.imaging.Pen, x : int, y : int, width : int, height : int) -> None:
        '''Draws the rectangle.
        
        :param pen: The pen to draw the outline of the figure.
        :param x: The x-coordinate of the upper-left corner of the rectangle to draw.
        :param y: The y-coordinate of the upper-left corner of the rectangle to draw.
        :param width: The width of the rectangle to draw.
        :param height: The height of the rectangle to draw.'''
        raise NotImplementedError()
    
    def fill_rectangle(self, pen : aspose.imaging.Pen, brush : aspose.imaging.Brush, x : int, y : int, width : int, height : int) -> None:
        '''Fills the rectangle.
        
        :param pen: The pen to draw the outline of the figure.
        :param brush: The brush to fill the interior of the figure.
        :param x: The x-coordinate of the upper-left corner of the rectangle to draw.
        :param y: The y-coordinate of the upper-left corner of the rectangle to draw.
        :param width: The width of the rectangle to draw.
        :param height: The height of the rectangle to draw.'''
        raise NotImplementedError()
    
    def end_recording(self) -> aspose.imaging.fileformats.svg.SvgImage:
        '''Gets the final Svg image which includes all drawing commands performed via :py:class:`aspose.imaging.fileformats.svg.graphics.SvgGraphics2D` object.
        
        :returns: The final Svg image.'''
        raise NotImplementedError()
    

