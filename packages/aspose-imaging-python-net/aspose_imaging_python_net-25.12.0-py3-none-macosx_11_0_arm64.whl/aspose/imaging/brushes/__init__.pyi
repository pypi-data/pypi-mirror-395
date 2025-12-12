"""The namespace provides helper classes and methods to work with different brush types."""
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

class HatchBrush(aspose.imaging.Brush):
    '''Defines a rectangular brush with a hatch style, a foreground color, and a background color. This class cannot be inherited.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def foreground_color(self) -> aspose.imaging.Color:
        '''Gets the color of hatch lines.'''
        raise NotImplementedError()
    
    @foreground_color.setter
    def foreground_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the color of hatch lines.'''
        raise NotImplementedError()
    
    @property
    def background_color(self) -> aspose.imaging.Color:
        '''Gets the color of spaces between the hatch lines.'''
        raise NotImplementedError()
    
    @background_color.setter
    def background_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the color of spaces between the hatch lines.'''
        raise NotImplementedError()
    
    @property
    def hatch_style(self) -> aspose.imaging.HatchStyle:
        '''Gets the hatch style of this brush.'''
        raise NotImplementedError()
    
    @hatch_style.setter
    def hatch_style(self, value : aspose.imaging.HatchStyle) -> None:
        '''Sets the hatch style of this brush.'''
        raise NotImplementedError()
    

class LinearGradientBrush(LinearGradientBrushBase):
    '''Encapsulates a :py:class:`aspose.imaging.Brush` with a linear gradient. This class cannot be inherited.'''
    
    @overload
    def __init__(self, rect : aspose.imaging.RectangleF, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color, angle : float, is_angle_scalable : bool) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class.
        
        :param rect: The rectangle.
        :param color1: The color1.
        :param color2: The color2.
        :param angle: The angle.
        :param is_angle_scalable: if set to ``true`` [is angle scalable].'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, rect : aspose.imaging.Rectangle, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color, angle : float, is_angle_scalable : bool) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class.
        
        :param rect: The rectangle.
        :param color1: The color1.
        :param color2: The color2.
        :param angle: The angle.
        :param is_angle_scalable: if set to ``true`` [is angle scalable].'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, rect : aspose.imaging.RectangleF, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color, angle : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class.
        
        :param rect: The rectangle.
        :param color1: The color1.
        :param color2: The color2.
        :param angle: The angle.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, rect : aspose.imaging.Rectangle, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color, angle : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class.
        
        :param rect: The rectangle.
        :param color1: The color1.
        :param color2: The color2.
        :param angle: The angle.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, point1 : aspose.imaging.PointF, point2 : aspose.imaging.PointF, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class.
        
        :param point1: The point1.
        :param point2: The point2.
        :param color1: The color1.
        :param color2: The color2.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, point1 : aspose.imaging.Point, point2 : aspose.imaging.Point, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class.
        
        :param point1: The point1.
        :param point2: The point2.
        :param color1: The color1.
        :param color2: The color2.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class with default parameters.
        The starting color is black, the ending color is white, the angle is 45 degrees and the rectangle is located in (0,0) with size (1,1).'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` by prepending the specified :py:class:`aspose.imaging.Matrix`.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix, order : aspose.imaging.MatrixOrder) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float) -> None:
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float) -> None:
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float) -> None:
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        raise NotImplementedError()
    
    @overload
    def set_sigma_bell_shape(self, focus : float) -> None:
        '''Creates a gradient falloff based on a bell-shaped curve.
        
        :param focus: A value from 0 through 1 that specifies the center of the gradient (the point where the starting color and ending color are blended equally).'''
        raise NotImplementedError()
    
    @overload
    def set_sigma_bell_shape(self, focus : float, scale : float) -> None:
        '''Creates a gradient falloff based on a bell-shaped curve.
        
        :param focus: A value from 0 through 1 that specifies the center of the gradient (the point where the gradient is composed of only the ending color).
        :param scale: A value from 0 through 1 that specifies how fast the colors falloff from the ``focus``.'''
        raise NotImplementedError()
    
    @overload
    def set_blend_triangular_shape(self, focus : float) -> None:
        '''Creates a linear gradient with a center color and a linear falloff to a single color on both ends.
        
        :param focus: A value from 0 through 1 that specifies the center of the gradient (the point where the gradient is composed of only the ending color).'''
        raise NotImplementedError()
    
    @overload
    def set_blend_triangular_shape(self, focus : float, scale : float) -> None:
        '''Creates a linear gradient with a center color and a linear falloff to a single color on both ends.
        
        :param focus: A value from 0 through 1 that specifies the center of the gradient (the point where the gradient is composed of only the ending color).
        :param scale: A value from 0 through1 that specifies how fast the colors falloff from the starting color to ``focus`` (ending color)'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    def reset_transform(self) -> None:
        '''Resets the :py:attr:`aspose.imaging.brushes.TransformBrush.transform` property to identity.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points(point1 : aspose.imaging.Point, point2 : aspose.imaging.Point, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color) -> aspose.imaging.brushes.LinearGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class with the specified points and colors.
        
        :param point1: A :py:class:`aspose.imaging.Point` structure that represents the starting point of the linear gradient.
        :param point2: A :py:class:`aspose.imaging.Point` structure that represents the endpoint of the linear gradient.
        :param color1: A :py:class:`aspose.imaging.Color` structure that represents the starting color of the linear gradient.
        :param color2: A :py:class:`aspose.imaging.Color` structure that represents the ending color of the linear gradient.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points_f(point1 : aspose.imaging.PointF, point2 : aspose.imaging.PointF, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color) -> aspose.imaging.brushes.LinearGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class with the specified points and colors.
        
        :param point1: A :py:class:`aspose.imaging.PointF` structure that represents the starting point of the linear gradient.
        :param point2: A :py:class:`aspose.imaging.PointF` structure that represents the endpoint of the linear gradient.
        :param color1: A :py:class:`aspose.imaging.Color` structure that represents the starting color of the linear gradient.
        :param color2: A :py:class:`aspose.imaging.Color` structure that represents the ending color of the linear gradient.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_rect_colors_angle(rect : aspose.imaging.Rectangle, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color, angle : float) -> aspose.imaging.brushes.LinearGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class based on a rectangle, starting and ending colors, and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param color1: A :py:class:`aspose.imaging.Color` structure that represents the starting color for the gradient.
        :param color2: A :py:class:`aspose.imaging.Color` structure that represents the ending color for the gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_rect_f_colors_angle(rect : aspose.imaging.RectangleF, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color, angle : float) -> aspose.imaging.brushes.LinearGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class based on a rectangle, starting and ending colors, and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param color1: A :py:class:`aspose.imaging.Color` structure that represents the starting color for the gradient.
        :param color2: A :py:class:`aspose.imaging.Color` structure that represents the ending color for the gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_rect_colors_angle_scalable(rect : aspose.imaging.Rectangle, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color, angle : float, is_angle_scalable : bool) -> aspose.imaging.brushes.LinearGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class based on a rectangle, starting and ending colors, and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param color1: A :py:class:`aspose.imaging.Color` structure that represents the starting color for the gradient.
        :param color2: A :py:class:`aspose.imaging.Color` structure that represents the ending color for the gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.
        :param is_angle_scalable: if set to ``true`` the angle is changed during transformations with this :py:class:`aspose.imaging.brushes.LinearGradientBrush`.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_rect_f_colors_angle_scalable(rect : aspose.imaging.RectangleF, color1 : aspose.imaging.Color, color2 : aspose.imaging.Color, angle : float, is_angle_scalable : bool) -> aspose.imaging.brushes.LinearGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearGradientBrush` class based on a rectangle, starting and ending colors, and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param color1: A :py:class:`aspose.imaging.Color` structure that represents the starting color for the gradient.
        :param color2: A :py:class:`aspose.imaging.Color` structure that represents the ending color for the gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.
        :param is_angle_scalable: if set to ``true`` the angle is changed during transformations with this :py:class:`aspose.imaging.brushes.LinearGradientBrush`.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.WrapMode:
        '''Gets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.WrapMode) -> None:
        '''Sets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def is_transform_changed(self) -> bool:
        '''Gets a value indicating whether transformations were changed in some way. For example setting the transformation matrix or
        calling any of the methods altering the transformation matrix. The property is introduced for backward compatibility with GDI+.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets a rectangular region that defines the starting and ending points of the gradient.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets a rectangular region that defines the starting and ending points of the gradient.'''
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets the gradient angle.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets the gradient angle.'''
        raise NotImplementedError()
    
    @property
    def is_angle_scalable(self) -> bool:
        '''Gets a value indicating whether :py:attr:`aspose.imaging.brushes.LinearGradientBrushBase.angle` is changed during trasnformations with this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @is_angle_scalable.setter
    def is_angle_scalable(self, value : bool) -> None:
        '''Sets a value indicating whether :py:attr:`aspose.imaging.brushes.LinearGradientBrushBase.angle` is changed during trasnformations with this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @property
    def gamma_correction(self) -> bool:
        '''Gets a value indicating whether gamma correction is enabled for this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @gamma_correction.setter
    def gamma_correction(self, value : bool) -> None:
        '''Sets a value indicating whether gamma correction is enabled for this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @property
    def interpolation_colors(self) -> aspose.imaging.ColorBlend:
        '''Gets a :py:class:`aspose.imaging.ColorBlend` that defines a multicolor linear gradient.'''
        raise NotImplementedError()
    
    @interpolation_colors.setter
    def interpolation_colors(self, value : aspose.imaging.ColorBlend) -> None:
        '''Sets a :py:class:`aspose.imaging.ColorBlend` that defines a multicolor linear gradient.'''
        raise NotImplementedError()
    
    @property
    def linear_colors(self) -> List[aspose.imaging.Color]:
        '''Gets the starting and ending colors of the gradient.'''
        raise NotImplementedError()
    
    @linear_colors.setter
    def linear_colors(self, value : List[aspose.imaging.Color]) -> None:
        '''Sets the starting and ending colors of the gradient.'''
        raise NotImplementedError()
    
    @property
    def start_color(self) -> aspose.imaging.Color:
        '''Gets the starting gradient color.'''
        raise NotImplementedError()
    
    @start_color.setter
    def start_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the starting gradient color.'''
        raise NotImplementedError()
    
    @property
    def end_color(self) -> aspose.imaging.Color:
        '''Gets the ending gradient color.'''
        raise NotImplementedError()
    
    @end_color.setter
    def end_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the ending gradient color.'''
        raise NotImplementedError()
    
    @property
    def blend(self) -> aspose.imaging.Blend:
        '''Gets a :py:class:`aspose.imaging.Blend` that specifies positions and factors that define a custom falloff for the gradient.'''
        raise NotImplementedError()
    
    @blend.setter
    def blend(self, value : aspose.imaging.Blend) -> None:
        '''Sets a :py:class:`aspose.imaging.Blend` that specifies positions and factors that define a custom falloff for the gradient.'''
        raise NotImplementedError()
    

class LinearGradientBrushBase(TransformBrush):
    '''Represents a :py:class:`aspose.imaging.Brush` with gradient capabilities and appropriate properties.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` by prepending the specified :py:class:`aspose.imaging.Matrix`.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix, order : aspose.imaging.MatrixOrder) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float) -> None:
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float) -> None:
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float) -> None:
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    def reset_transform(self) -> None:
        '''Resets the :py:attr:`aspose.imaging.brushes.TransformBrush.transform` property to identity.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.WrapMode:
        '''Gets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.WrapMode) -> None:
        '''Sets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def is_transform_changed(self) -> bool:
        '''Gets a value indicating whether transformations were changed in some way. For example setting the transformation matrix or
        calling any of the methods altering the transformation matrix. The property is introduced for backward compatibility with GDI+.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets a rectangular region that defines the starting and ending points of the gradient.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets a rectangular region that defines the starting and ending points of the gradient.'''
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets the gradient angle.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets the gradient angle.'''
        raise NotImplementedError()
    
    @property
    def is_angle_scalable(self) -> bool:
        '''Gets a value indicating whether :py:attr:`aspose.imaging.brushes.LinearGradientBrushBase.angle` is changed during trasnformations with this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @is_angle_scalable.setter
    def is_angle_scalable(self, value : bool) -> None:
        '''Sets a value indicating whether :py:attr:`aspose.imaging.brushes.LinearGradientBrushBase.angle` is changed during trasnformations with this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @property
    def gamma_correction(self) -> bool:
        '''Gets a value indicating whether gamma correction is enabled for this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @gamma_correction.setter
    def gamma_correction(self, value : bool) -> None:
        '''Sets a value indicating whether gamma correction is enabled for this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    

class LinearMulticolorGradientBrush(LinearGradientBrushBase):
    '''Represents a :py:class:`aspose.imaging.Brush` with linear gradient defined by multiple colors and appropriate positions. This class cannot be inherited.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class with default parameters.
        The starting color is black, the ending color is white, the angle is 45 degrees and the rectangle is located in (0,0) with size (1,1).'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, point1 : aspose.imaging.Point, point2 : aspose.imaging.Point) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class with the specified points.
        
        :param point1: A :py:class:`aspose.imaging.Point` structure that represents the starting point of the linear gradient.
        :param point2: A :py:class:`aspose.imaging.Point` structure that represents the endpoint of the linear gradient.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, point1 : aspose.imaging.PointF, point2 : aspose.imaging.PointF) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class with the specified points.
        
        :param point1: A :py:class:`aspose.imaging.PointF` structure that represents the starting point of the linear gradient.
        :param point2: A :py:class:`aspose.imaging.PointF` structure that represents the endpoint of the linear gradient.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, rect : aspose.imaging.Rectangle, angle : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class based on a rectangle and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, rect : aspose.imaging.RectangleF, angle : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class based on a rectangle and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, rect : aspose.imaging.Rectangle, angle : float, is_angle_scalable : bool) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class based on a rectangle and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.
        :param is_angle_scalable: if set to ``true`` the angle is changed during transformations with this :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush`.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, rect : aspose.imaging.RectangleF, angle : float, is_angle_scalable : bool) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class based on a rectangle and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.
        :param is_angle_scalable: if set to ``true`` the angle is changed during transformations with this :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush`.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` by prepending the specified :py:class:`aspose.imaging.Matrix`.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix, order : aspose.imaging.MatrixOrder) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float) -> None:
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float) -> None:
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float) -> None:
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    def reset_transform(self) -> None:
        '''Resets the :py:attr:`aspose.imaging.brushes.TransformBrush.transform` property to identity.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points(point1 : aspose.imaging.Point, point2 : aspose.imaging.Point) -> aspose.imaging.brushes.LinearMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class with the specified points.
        
        :param point1: A :py:class:`aspose.imaging.Point` structure that represents the starting point of the linear gradient.
        :param point2: A :py:class:`aspose.imaging.Point` structure that represents the endpoint of the linear gradient.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points_f(point1 : aspose.imaging.PointF, point2 : aspose.imaging.PointF) -> aspose.imaging.brushes.LinearMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class with the specified points.
        
        :param point1: A :py:class:`aspose.imaging.PointF` structure that represents the starting point of the linear gradient.
        :param point2: A :py:class:`aspose.imaging.PointF` structure that represents the endpoint of the linear gradient.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_rect(rect : aspose.imaging.Rectangle, angle : float) -> aspose.imaging.brushes.LinearMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class based on a rectangle and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_rect_f(rect : aspose.imaging.RectangleF, angle : float) -> aspose.imaging.brushes.LinearMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class based on a rectangle and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_rect_angle_scalable(rect : aspose.imaging.Rectangle, angle : float, is_angle_scalable : bool) -> aspose.imaging.brushes.LinearMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class based on a rectangle and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.
        :param is_angle_scalable: if set to ``true`` the angle is changed during transformations with this :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush`.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_rect_f_angle_scalable(rect : aspose.imaging.RectangleF, angle : float, is_angle_scalable : bool) -> aspose.imaging.brushes.LinearMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush` class based on a rectangle and an orientation angle.
        
        :param rect: A :py:class:`aspose.imaging.RectangleF` structure that specifies the bounds of the linear gradient.
        :param angle: The angle, measured in degrees clockwise from the x-axis, of the gradient\'s orientation line.
        :param is_angle_scalable: if set to ``true`` the angle is changed during transformations with this :py:class:`aspose.imaging.brushes.LinearMulticolorGradientBrush`.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.WrapMode:
        '''Gets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.WrapMode) -> None:
        '''Sets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def is_transform_changed(self) -> bool:
        '''Gets a value indicating whether transformations were changed in some way. For example setting the transformation matrix or
        calling any of the methods altering the transformation matrix. The property is introduced for backward compatibility with GDI+.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets a rectangular region that defines the starting and ending points of the gradient.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets a rectangular region that defines the starting and ending points of the gradient.'''
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets the gradient angle.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets the gradient angle.'''
        raise NotImplementedError()
    
    @property
    def is_angle_scalable(self) -> bool:
        '''Gets a value indicating whether :py:attr:`aspose.imaging.brushes.LinearGradientBrushBase.angle` is changed during trasnformations with this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @is_angle_scalable.setter
    def is_angle_scalable(self, value : bool) -> None:
        '''Sets a value indicating whether :py:attr:`aspose.imaging.brushes.LinearGradientBrushBase.angle` is changed during trasnformations with this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @property
    def gamma_correction(self) -> bool:
        '''Gets a value indicating whether gamma correction is enabled for this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @gamma_correction.setter
    def gamma_correction(self, value : bool) -> None:
        '''Sets a value indicating whether gamma correction is enabled for this :py:class:`aspose.imaging.brushes.LinearGradientBrushBase`.'''
        raise NotImplementedError()
    
    @property
    def interpolation_colors(self) -> aspose.imaging.ColorBlend:
        '''Gets a :py:class:`aspose.imaging.ColorBlend` that defines a multicolor linear gradient.'''
        raise NotImplementedError()
    
    @interpolation_colors.setter
    def interpolation_colors(self, value : aspose.imaging.ColorBlend) -> None:
        '''Sets a :py:class:`aspose.imaging.ColorBlend` that defines a multicolor linear gradient.'''
        raise NotImplementedError()
    

class PathGradientBrush(PathGradientBrushBase):
    '''Encapsulates a :py:class:`aspose.imaging.Brush` object with a gradient. This class cannot be inherited.'''
    
    @overload
    def __init__(self, path_points : List[aspose.imaging.PointF]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrushBase` class with the specified points.
        
        :param path_points: An array of :py:class:`aspose.imaging.PointF` structures that represents the points that make up the vertices of the path.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, path_points : List[aspose.imaging.PointF], wrap_mode : aspose.imaging.WrapMode) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrushBase` class with the specified points and wrap mode.
        
        :param path_points: An array of :py:class:`aspose.imaging.PointF` structures that represents the points that make up the vertices of the path.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` that specifies how fills drawn with this :py:class:`aspose.imaging.brushes.PathGradientBrushBase` are tiled.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, path_points : List[aspose.imaging.Point]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrushBase` class with the specified points.
        
        :param path_points: An array of :py:class:`aspose.imaging.Point` structures that represents the points that make up the vertices of the path.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, path_points : List[aspose.imaging.Point], wrap_mode : aspose.imaging.WrapMode) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrushBase` class with the specified points and wrap mode.
        
        :param path_points: An array of :py:class:`aspose.imaging.Point` structures that represents the points that make up the vertices of the path.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` that specifies how fills drawn with this :py:class:`aspose.imaging.brushes.PathGradientBrushBase` are tiled.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, path : aspose.imaging.GraphicsPath) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrushBase` class with the specified path.
        
        :param path: The :py:attr:`aspose.imaging.brushes.PathGradientBrushBase.graphics_path` that defines the area filled by this :py:class:`aspose.imaging.brushes.PathGradientBrushBase`.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` by prepending the specified :py:class:`aspose.imaging.Matrix`.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix, order : aspose.imaging.MatrixOrder) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float) -> None:
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float) -> None:
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float) -> None:
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        raise NotImplementedError()
    
    @overload
    def set_sigma_bell_shape(self, focus : float) -> None:
        '''Creates a gradient brush that changes color starting from the center of the path outward to the path\'s boundary. The transition from one color to another is based on a bell-shaped curve.
        
        :param focus: A value from 0 through 1 that specifies where, along any radial from the center of the path to the path\'s boundary, the center color will be at its highest intensity. A value of 1 (the default) places the highest intensity at the center of the path.'''
        raise NotImplementedError()
    
    @overload
    def set_sigma_bell_shape(self, focus : float, scale : float) -> None:
        '''Creates a gradient brush that changes color starting from the center of the path outward to the path\'s boundary. The transition from one color to another is based on a bell-shaped curve.
        
        :param focus: A value from 0 through 1 that specifies where, along any radial from the center of the path to the path\'s boundary, the center color will be at its highest intensity. A value of 1 (the default) places the highest intensity at the center of the path.
        :param scale: A value from 0 through 1 that specifies the maximum intensity of the center color that gets blended with the boundary color. A value of 1 causes the highest possible intensity of the center color, and it is the default value.'''
        raise NotImplementedError()
    
    @overload
    def set_blend_triangular_shape(self, focus : float) -> None:
        '''Creates a gradient with a center color and a linear falloff to one surrounding color.
        
        :param focus: A value from 0 through 1 that specifies where, along any radial from the center of the path to the path\'s boundary, the center color will be at its highest intensity. A value of 1 (the default) places the highest intensity at the center of the path.'''
        raise NotImplementedError()
    
    @overload
    def set_blend_triangular_shape(self, focus : float, scale : float) -> None:
        '''Creates a gradient with a center color and a linear falloff to each surrounding color.
        
        :param focus: A value from 0 through 1 that specifies where, along any radial from the center of the path to the path\'s boundary, the center color will be at its highest intensity. A value of 1 (the default) places the highest intensity at the center of the path.
        :param scale: A value from 0 through 1 that specifies the maximum intensity of the center color that gets blended with the boundary color. A value of 1 causes the highest possible intensity of the center color, and it is the default value.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    def reset_transform(self) -> None:
        '''Resets the :py:attr:`aspose.imaging.brushes.TransformBrush.transform` property to identity.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points_f(path_points : List[aspose.imaging.PointF]) -> aspose.imaging.brushes.PathGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrush` class with the specified points.
        
        :param path_points: An array of :py:class:`aspose.imaging.PointF` structures that represents the points that make up the vertices of the path.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points_f_wrap_mode(path_points : List[aspose.imaging.PointF], wrap_mode : aspose.imaging.WrapMode) -> aspose.imaging.brushes.PathGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrush` class with the specified points and wrap mode.
        
        :param path_points: An array of :py:class:`aspose.imaging.PointF` structures that represents the points that make up the vertices of the path.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` that specifies how fills drawn with this :py:class:`aspose.imaging.brushes.PathGradientBrush` are tiled.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points(path_points : List[aspose.imaging.Point]) -> aspose.imaging.brushes.PathGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrush` class with the specified points.
        
        :param path_points: An array of :py:class:`aspose.imaging.Point` structures that represents the points that make up the vertices of the path.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points_wrap_mode(path_points : List[aspose.imaging.Point], wrap_mode : aspose.imaging.WrapMode) -> aspose.imaging.brushes.PathGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrush` class with the specified points and wrap mode.
        
        :param path_points: An array of :py:class:`aspose.imaging.Point` structures that represents the points that make up the vertices of the path.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` that specifies how fills drawn with this :py:class:`aspose.imaging.brushes.PathGradientBrush` are tiled.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_path(path : aspose.imaging.GraphicsPath) -> aspose.imaging.brushes.PathGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathGradientBrush` class with the specified path.
        
        :param path: The :py:class:`aspose.imaging.GraphicsPath` that defines the area filled by this :py:class:`aspose.imaging.brushes.PathGradientBrush`.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.WrapMode:
        '''Gets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.WrapMode) -> None:
        '''Sets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def is_transform_changed(self) -> bool:
        '''Gets a value indicating whether transformations were changed in some way. For example setting the transformation matrix or
        calling any of the methods altering the transformation matrix. The property is introduced for backward compatibility with GDI+.'''
        raise NotImplementedError()
    
    @property
    def path_points(self) -> List[aspose.imaging.PointF]:
        '''Gets the path points this brush was build upon.'''
        raise NotImplementedError()
    
    @property
    def graphics_path(self) -> aspose.imaging.GraphicsPath:
        '''Gets the graphics path this brush was build upon.'''
        raise NotImplementedError()
    
    @property
    def center_point(self) -> aspose.imaging.PointF:
        '''Gets the center point of the path gradient.'''
        raise NotImplementedError()
    
    @center_point.setter
    def center_point(self, value : aspose.imaging.PointF) -> None:
        '''Sets the center point of the path gradient.'''
        raise NotImplementedError()
    
    @property
    def focus_scales(self) -> aspose.imaging.PointF:
        '''Gets the focus point for the gradient falloff.'''
        raise NotImplementedError()
    
    @focus_scales.setter
    def focus_scales(self, value : aspose.imaging.PointF) -> None:
        '''Sets the focus point for the gradient falloff.'''
        raise NotImplementedError()
    
    @property
    def interpolation_colors(self) -> aspose.imaging.ColorBlend:
        '''Gets a :py:class:`aspose.imaging.ColorBlend` that defines a multicolor linear gradient.'''
        raise NotImplementedError()
    
    @interpolation_colors.setter
    def interpolation_colors(self, value : aspose.imaging.ColorBlend) -> None:
        '''Sets a :py:class:`aspose.imaging.ColorBlend` that defines a multicolor linear gradient.'''
        raise NotImplementedError()
    
    @property
    def center_color(self) -> aspose.imaging.Color:
        '''Gets the color at the center of the path gradient.'''
        raise NotImplementedError()
    
    @center_color.setter
    def center_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the color at the center of the path gradient.'''
        raise NotImplementedError()
    
    @property
    def surround_colors(self) -> List[aspose.imaging.Color]:
        '''Gets an array of colors that correspond to the points in the path this :py:class:`aspose.imaging.brushes.PathGradientBrush` fills.'''
        raise NotImplementedError()
    
    @surround_colors.setter
    def surround_colors(self, value : List[aspose.imaging.Color]) -> None:
        '''Sets an array of colors that correspond to the points in the path this :py:class:`aspose.imaging.brushes.PathGradientBrush` fills.'''
        raise NotImplementedError()
    
    @property
    def blend(self) -> aspose.imaging.Blend:
        '''Gets a :py:class:`aspose.imaging.Blend` that specifies positions and factors that define a custom falloff for the gradient.'''
        raise NotImplementedError()
    
    @blend.setter
    def blend(self, value : aspose.imaging.Blend) -> None:
        '''Sets a :py:class:`aspose.imaging.Blend` that specifies positions and factors that define a custom falloff for the gradient.'''
        raise NotImplementedError()
    

class PathGradientBrushBase(TransformBrush):
    '''Represents a :py:class:`aspose.imaging.Brush` with base path gradient functionality.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` by prepending the specified :py:class:`aspose.imaging.Matrix`.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix, order : aspose.imaging.MatrixOrder) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float) -> None:
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float) -> None:
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float) -> None:
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    def reset_transform(self) -> None:
        '''Resets the :py:attr:`aspose.imaging.brushes.TransformBrush.transform` property to identity.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.WrapMode:
        '''Gets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.WrapMode) -> None:
        '''Sets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def is_transform_changed(self) -> bool:
        '''Gets a value indicating whether transformations were changed in some way. For example setting the transformation matrix or
        calling any of the methods altering the transformation matrix. The property is introduced for backward compatibility with GDI+.'''
        raise NotImplementedError()
    
    @property
    def path_points(self) -> List[aspose.imaging.PointF]:
        '''Gets the path points this brush was build upon.'''
        raise NotImplementedError()
    
    @property
    def graphics_path(self) -> aspose.imaging.GraphicsPath:
        '''Gets the graphics path this brush was build upon.'''
        raise NotImplementedError()
    
    @property
    def center_point(self) -> aspose.imaging.PointF:
        '''Gets the center point of the path gradient.'''
        raise NotImplementedError()
    
    @center_point.setter
    def center_point(self, value : aspose.imaging.PointF) -> None:
        '''Sets the center point of the path gradient.'''
        raise NotImplementedError()
    
    @property
    def focus_scales(self) -> aspose.imaging.PointF:
        '''Gets the focus point for the gradient falloff.'''
        raise NotImplementedError()
    
    @focus_scales.setter
    def focus_scales(self, value : aspose.imaging.PointF) -> None:
        '''Sets the focus point for the gradient falloff.'''
        raise NotImplementedError()
    

class PathMulticolorGradientBrush(PathGradientBrushBase):
    '''Encapsulates a :py:class:`aspose.imaging.Brush` object with a gradient. This class cannot be inherited.'''
    
    @overload
    def __init__(self, path_points : List[aspose.imaging.PointF]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified points.
        
        :param path_points: An array of :py:class:`aspose.imaging.PointF` structures that represents the points that make up the vertices of the path.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, path_points : List[aspose.imaging.PointF], wrap_mode : aspose.imaging.WrapMode) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified points and wrap mode.
        
        :param path_points: An array of :py:class:`aspose.imaging.PointF` structures that represents the points that make up the vertices of the path.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` that specifies how fills drawn with this :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` are tiled.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, path_points : List[aspose.imaging.Point]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified points.
        
        :param path_points: An array of :py:class:`aspose.imaging.Point` structures that represents the points that make up the vertices of the path.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, path_points : List[aspose.imaging.Point], wrap_mode : aspose.imaging.WrapMode) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified points and wrap mode.
        
        :param path_points: An array of :py:class:`aspose.imaging.Point` structures that represents the points that make up the vertices of the path.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` that specifies how fills drawn with this :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` are tiled.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, path : aspose.imaging.GraphicsPath) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified path.
        
        :param path: The :py:class:`aspose.imaging.GraphicsPath` that defines the area filled by this :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush`.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` by prepending the specified :py:class:`aspose.imaging.Matrix`.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix, order : aspose.imaging.MatrixOrder) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float) -> None:
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float) -> None:
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float) -> None:
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    def reset_transform(self) -> None:
        '''Resets the :py:attr:`aspose.imaging.brushes.TransformBrush.transform` property to identity.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points(path_points : List[aspose.imaging.PointF]) -> aspose.imaging.brushes.PathMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified points.
        
        :param path_points: An array of :py:class:`aspose.imaging.PointF` structures that represents the points that make up the vertices of the path.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points_f_wrap_mode(path_points : List[aspose.imaging.PointF], wrap_mode : aspose.imaging.WrapMode) -> aspose.imaging.brushes.PathMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified points and wrap mode.
        
        :param path_points: An array of :py:class:`aspose.imaging.PointF` structures that represents the points that make up the vertices of the path.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` that specifies how fills drawn with this :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` are tiled.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points_f(path_points : List[aspose.imaging.Point]) -> aspose.imaging.brushes.PathMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified points.
        
        :param path_points: An array of :py:class:`aspose.imaging.Point` structures that represents the points that make up the vertices of the path.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_points_wrap_mode(path_points : List[aspose.imaging.Point], wrap_mode : aspose.imaging.WrapMode) -> aspose.imaging.brushes.PathMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified points and wrap mode.
        
        :param path_points: An array of :py:class:`aspose.imaging.Point` structures that represents the points that make up the vertices of the path.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` that specifies how fills drawn with this :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` are tiled.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_path(path : aspose.imaging.GraphicsPath) -> aspose.imaging.brushes.PathMulticolorGradientBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush` class with the specified path.
        
        :param path: The :py:class:`aspose.imaging.GraphicsPath` that defines the area filled by this :py:class:`aspose.imaging.brushes.PathMulticolorGradientBrush`.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.WrapMode:
        '''Gets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.WrapMode) -> None:
        '''Sets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def is_transform_changed(self) -> bool:
        '''Gets a value indicating whether transformations were changed in some way. For example setting the transformation matrix or
        calling any of the methods altering the transformation matrix. The property is introduced for backward compatibility with GDI+.'''
        raise NotImplementedError()
    
    @property
    def path_points(self) -> List[aspose.imaging.PointF]:
        '''Gets the path points this brush was build upon.'''
        raise NotImplementedError()
    
    @property
    def graphics_path(self) -> aspose.imaging.GraphicsPath:
        '''Gets the graphics path this brush was build upon.'''
        raise NotImplementedError()
    
    @property
    def center_point(self) -> aspose.imaging.PointF:
        '''Gets the center point of the path gradient.'''
        raise NotImplementedError()
    
    @center_point.setter
    def center_point(self, value : aspose.imaging.PointF) -> None:
        '''Sets the center point of the path gradient.'''
        raise NotImplementedError()
    
    @property
    def focus_scales(self) -> aspose.imaging.PointF:
        '''Gets the focus point for the gradient falloff.'''
        raise NotImplementedError()
    
    @focus_scales.setter
    def focus_scales(self, value : aspose.imaging.PointF) -> None:
        '''Sets the focus point for the gradient falloff.'''
        raise NotImplementedError()
    
    @property
    def interpolation_colors(self) -> aspose.imaging.ColorBlend:
        '''Gets a :py:class:`aspose.imaging.ColorBlend` that defines a multicolor linear gradient.'''
        raise NotImplementedError()
    
    @interpolation_colors.setter
    def interpolation_colors(self, value : aspose.imaging.ColorBlend) -> None:
        '''Sets a :py:class:`aspose.imaging.ColorBlend` that defines a multicolor linear gradient.'''
        raise NotImplementedError()
    

class SolidBrush(aspose.imaging.Brush):
    '''Solid brush is intended for drawing continiously with specific color. This class cannot be inherited.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.SolidBrush` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, color : aspose.imaging.Color) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.SolidBrush` class.
        
        :param color: The solid brush color.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def color(self) -> aspose.imaging.Color:
        '''Gets the brush color.'''
        raise NotImplementedError()
    
    @color.setter
    def color(self, value : aspose.imaging.Color) -> None:
        '''Sets the brush color.'''
        raise NotImplementedError()
    

class TextureBrush(TransformBrush):
    '''Each property of the :py:class:`aspose.imaging.brushes.TextureBrush` class is a :py:class:`aspose.imaging.Brush` object that uses an image to fill the interior of a shape. This class cannot be inherited.'''
    
    @overload
    def __init__(self, image : aspose.imaging.Image, destination_rectangle : aspose.imaging.Rectangle, image_attributes : aspose.imaging.ImageAttributes) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image, bounding rectangle, and image attributes.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param destination_rectangle: A :py:class:`aspose.imaging.Rectangle` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.
        :param image_attributes: An :py:class:`aspose.imaging.ImageAttributes` object that contains additional information about the image used by this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.Image, destination_rectangle : aspose.imaging.Rectangle) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image and bounding rectangle.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param destination_rectangle: A :py:class:`aspose.imaging.Rectangle` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.Image, destination_rectangle : aspose.imaging.RectangleF) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image and bounding rectangle.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param destination_rectangle: A :py:class:`aspose.imaging.RectangleF` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.Image, wrap_mode : aspose.imaging.WrapMode, destination_rectangle : aspose.imaging.Rectangle) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image, wrap mode, and bounding rectangle.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` enumeration that specifies how this :py:class:`aspose.imaging.brushes.TextureBrush` object is tiled.
        :param destination_rectangle: A :py:class:`aspose.imaging.Rectangle` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.Image, wrap_mode : aspose.imaging.WrapMode, destination_rectangle : aspose.imaging.RectangleF) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image, wrap mode, and bounding rectangle.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` enumeration that specifies how this :py:class:`aspose.imaging.brushes.TextureBrush` object is tiled.
        :param destination_rectangle: A :py:class:`aspose.imaging.RectangleF` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.Image, wrap_mode : aspose.imaging.WrapMode) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image and wrap mode.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` enumeration that specifies how this :py:class:`aspose.imaging.brushes.TextureBrush` object is tiled.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.Image) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.Image, destination_rectangle : aspose.imaging.RectangleF, image_attributes : aspose.imaging.ImageAttributes) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image, bounding rectangle, and image attributes.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param destination_rectangle: A :py:class:`aspose.imaging.RectangleF` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.
        :param image_attributes: An :py:class:`aspose.imaging.ImageAttributes` object that contains additional information about the image used by this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` by prepending the specified :py:class:`aspose.imaging.Matrix`.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix, order : aspose.imaging.MatrixOrder) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float) -> None:
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float) -> None:
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float) -> None:
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    def reset_transform(self) -> None:
        '''Resets the :py:attr:`aspose.imaging.brushes.TransformBrush.transform` property to identity.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_image_wrap_mode(image : aspose.imaging.Image, wrap_mode : aspose.imaging.WrapMode) -> aspose.imaging.brushes.TextureBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image and wrap mode.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` enumeration that specifies how this :py:class:`aspose.imaging.brushes.TextureBrush` object is tiled.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_image_wrap_mode_rect_f(image : aspose.imaging.Image, wrap_mode : aspose.imaging.WrapMode, destination_rectangle : aspose.imaging.RectangleF) -> aspose.imaging.brushes.TextureBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image, wrap mode, and bounding rectangle.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` enumeration that specifies how this :py:class:`aspose.imaging.brushes.TextureBrush` object is tiled.
        :param destination_rectangle: A :py:class:`aspose.imaging.RectangleF` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_image_wrap_mode_rect(image : aspose.imaging.Image, wrap_mode : aspose.imaging.WrapMode, destination_rectangle : aspose.imaging.Rectangle) -> aspose.imaging.brushes.TextureBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image, wrap mode, and bounding rectangle.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param wrap_mode: A :py:class:`aspose.imaging.WrapMode` enumeration that specifies how this :py:class:`aspose.imaging.brushes.TextureBrush` object is tiled.
        :param destination_rectangle: A :py:class:`aspose.imaging.Rectangle` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_image_rect_f(image : aspose.imaging.Image, destination_rectangle : aspose.imaging.RectangleF) -> aspose.imaging.brushes.TextureBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image and bounding rectangle.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param destination_rectangle: A :py:class:`aspose.imaging.RectangleF` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_image_rect_f_attribs(image : aspose.imaging.Image, destination_rectangle : aspose.imaging.RectangleF, image_attributes : aspose.imaging.ImageAttributes) -> aspose.imaging.brushes.TextureBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image, bounding rectangle, and image attributes.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param destination_rectangle: A :py:class:`aspose.imaging.RectangleF` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.
        :param image_attributes: An :py:class:`aspose.imaging.ImageAttributes` object that contains additional information about the image used by this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_image_rect(image : aspose.imaging.Image, destination_rectangle : aspose.imaging.Rectangle) -> aspose.imaging.brushes.TextureBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image and bounding rectangle.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param destination_rectangle: A :py:class:`aspose.imaging.Rectangle` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_image_rect_attribs(image : aspose.imaging.Image, destination_rectangle : aspose.imaging.Rectangle, image_attributes : aspose.imaging.ImageAttributes) -> aspose.imaging.brushes.TextureBrush:
        '''Initializes a new instance of the :py:class:`aspose.imaging.brushes.TextureBrush` class that uses the specified image, bounding rectangle, and image attributes.
        
        :param image: The :py:class:`aspose.imaging.Image` object with which this :py:class:`aspose.imaging.brushes.TextureBrush` object fills interiors.
        :param destination_rectangle: A :py:class:`aspose.imaging.Rectangle` structure that represents the bounding rectangle for this :py:class:`aspose.imaging.brushes.TextureBrush` object.
        :param image_attributes: An :py:class:`aspose.imaging.ImageAttributes` object that contains additional information about the image used by this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.WrapMode:
        '''Gets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.WrapMode) -> None:
        '''Sets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def is_transform_changed(self) -> bool:
        '''Gets a value indicating whether transformations were changed in some way. For example setting the transformation matrix or
        calling any of the methods altering the transformation matrix. The property is introduced for backward compatibility with GDI+.'''
        raise NotImplementedError()
    
    @property
    def image(self) -> aspose.imaging.Image:
        '''Gets the :py:class:`aspose.imaging.Image` object associated with this :py:class:`aspose.imaging.brushes.TextureBrush` object.'''
        raise NotImplementedError()
    
    @property
    def image_attributes(self) -> aspose.imaging.ImageAttributes:
        '''Gets the :py:attr:`aspose.imaging.brushes.TextureBrush.image_attributes` associated with this :py:class:`aspose.imaging.brushes.TextureBrush`.'''
        raise NotImplementedError()
    
    @property
    def image_rectangle(self) -> aspose.imaging.RectangleF:
        '''Gets the :py:class:`aspose.imaging.Rectangle` associated with this :py:class:`aspose.imaging.brushes.TextureBrush`.'''
        raise NotImplementedError()
    

class TransformBrush(aspose.imaging.Brush):
    '''A :py:class:`aspose.imaging.Brush` with transform capabilities.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` by prepending the specified :py:class:`aspose.imaging.Matrix`.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.'''
        raise NotImplementedError()
    
    @overload
    def multiply_transform(self, matrix : aspose.imaging.Matrix, order : aspose.imaging.MatrixOrder) -> None:
        '''Multiplies the :py:class:`aspose.imaging.Matrix` that represents the local geometric transform of this :py:class:`aspose.imaging.brushes.LinearGradientBrush` by the specified :py:class:`aspose.imaging.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.imaging.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float) -> None:
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        raise NotImplementedError()
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float) -> None:
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        raise NotImplementedError()
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float) -> None:
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        raise NotImplementedError()
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.imaging.MatrixOrder) -> None:
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.imaging.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.imaging.Brush`.
        
        :returns: A new :py:class:`aspose.imaging.Brush` which is the deep clone of this :py:class:`aspose.imaging.Brush` instance.'''
        raise NotImplementedError()
    
    def reset_transform(self) -> None:
        '''Resets the :py:attr:`aspose.imaging.brushes.TransformBrush.transform` property to identity.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.WrapMode:
        '''Gets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.WrapMode) -> None:
        '''Sets a :py:class:`aspose.imaging.WrapMode` enumeration that indicates the wrap mode for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets a copy :py:class:`aspose.imaging.Matrix` that defines a local geometric transform for this :py:class:`aspose.imaging.brushes.TransformBrush`.'''
        raise NotImplementedError()
    
    @property
    def is_transform_changed(self) -> bool:
        '''Gets a value indicating whether transformations were changed in some way. For example setting the transformation matrix or
        calling any of the methods altering the transformation matrix. The property is introduced for backward compatibility with GDI+.'''
        raise NotImplementedError()
    

