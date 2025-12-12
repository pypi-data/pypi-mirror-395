"""The namespace contains types [MS-EMFPLUS]: Enhanced Metafile Format Plus Extensions
            2.2 EMF+ Objects"""
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

class EmfPlusBaseBitmapData(EmfPlusStructureObjectType):
    '''Base class for bitmap data types.'''
    

class EmfPlusBaseBrushData(EmfPlusStructureObjectType):
    '''Base class for Brush data types.'''
    

class EmfPlusBaseImageData(EmfPlusStructureObjectType):
    '''Base class for image data types.'''
    

class EmfPlusBasePointType:
    '''The base point type.'''
    

class EmfPlusBitmap(EmfPlusBaseImageData):
    '''The EmfPlusBitmap object specifies a bitmap that contains a graphics image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def bitmap_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBaseBitmapData:
        '''Gets bitmap data
        BitmapData (variable): Variable-length data that defines the bitmap data object specified in the Type field. The
        content and format of the data can be different for every bitmap type.'''
        raise NotImplementedError()
    
    @bitmap_data.setter
    def bitmap_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBaseBitmapData) -> None:
        '''Sets bitmap data
        BitmapData (variable): Variable-length data that defines the bitmap data object specified in the Type field. The
        content and format of the data can be different for every bitmap type.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets bitmap height
        Height (4 bytes): A 32-bit signed integer that specifies the height in pixels of the area occupied by the bitmap.
        If the image is compressed, according to the Type field, this value is undefined and MUST be ignored.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets bitmap height
        Height (4 bytes): A 32-bit signed integer that specifies the height in pixels of the area occupied by the bitmap.
        If the image is compressed, according to the Type field, this value is undefined and MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def pixel_format(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPixelFormat:
        '''Gets pixel format
        PixelFormat (4 bytes): A 32-bit unsigned integer that specifies the format of the pixels that make up the bitmap
        image. The supported pixel formats are specified in the :py:class:`aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPixelFormat` enumeration (section
        2.1.1.25).
        If the image is compressed, according to the Type field, this value is undefined and MUST be ignored.'''
        raise NotImplementedError()
    
    @pixel_format.setter
    def pixel_format(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPixelFormat) -> None:
        '''Sets pixel format
        PixelFormat (4 bytes): A 32-bit unsigned integer that specifies the format of the pixels that make up the bitmap
        image. The supported pixel formats are specified in the :py:class:`aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPixelFormat` enumeration (section
        2.1.1.25).
        If the image is compressed, according to the Type field, this value is undefined and MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def stride(self) -> int:
        '''Gets stride of the image
        Stride (4 bytes): A 32-bit signed integer that specifies the byte offset between the beginning of one scan-line and
        the next. This value is the number of bytes per pixel, which is specified in the PixelFormat field, multiplied by
        the width in pixels, which is specified in the Width field. The value of this field MUST be a multiple of four.
        If the image is compressed, according to the Type field, this value is undefined and MUST be ignored.'''
        raise NotImplementedError()
    
    @stride.setter
    def stride(self, value : int) -> None:
        '''Sets stride of the image
        Stride (4 bytes): A 32-bit signed integer that specifies the byte offset between the beginning of one scan-line and
        the next. This value is the number of bytes per pixel, which is specified in the PixelFormat field, multiplied by
        the width in pixels, which is specified in the Width field. The value of this field MUST be a multiple of four.
        If the image is compressed, according to the Type field, this value is undefined and MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBitmapDataType:
        '''Gets type of the image
        Type (4 bytes): A 32-bit unsigned integer that specifies the type of data in the BitmapData field. This value MUST
        be defined in the :py:class:`aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBitmapDataType` enumeration (section 2.1.1.2).'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBitmapDataType) -> None:
        '''Sets type of the image
        Type (4 bytes): A 32-bit unsigned integer that specifies the type of data in the BitmapData field. This value MUST
        be defined in the :py:class:`aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBitmapDataType` enumeration (section 2.1.1.2).'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets image Width
        Width (4 bytes): A 32-bit signed integer that specifies the width in pixels of the area occupied by the bitmap.
        If the image is compressed, according to the Type field, this value is undefined and MUST be ignored.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets image Width
        Width (4 bytes): A 32-bit signed integer that specifies the width in pixels of the area occupied by the bitmap.
        If the image is compressed, according to the Type field, this value is undefined and MUST be ignored.'''
        raise NotImplementedError()
    

class EmfPlusBitmapData(EmfPlusBaseBitmapData):
    '''The EmfPlusBitmapData object specifies a bitmap image with pixel data.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def colors(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPalette:
        '''Gets the palette colors
        Colors (variable): An optional :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPalette` object (section 2.2.2.28), which specifies the palette
        of colors used in the pixel data. This field MUST be present if the I flag is set in the PixelFormat field of the
        :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBitmap` object.'''
        raise NotImplementedError()
    
    @colors.setter
    def colors(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPalette) -> None:
        '''Sets the palette colors
        Colors (variable): An optional :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPalette` object (section 2.2.2.28), which specifies the palette
        of colors used in the pixel data. This field MUST be present if the I flag is set in the PixelFormat field of the
        :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBitmap` object.'''
        raise NotImplementedError()
    
    @property
    def pixel_data(self) -> List[int]:
        '''Gets pixel data
        PixelData (variable): An array of bytes that specify the pixel data. The size and format of this data can be
        computed from fields in the EmfPlusBitmap object, including the pixel format from the
        :py:class:`aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPixelFormat` enumeration (section 2.1.1.25).'''
        raise NotImplementedError()
    
    @pixel_data.setter
    def pixel_data(self, value : List[int]) -> None:
        '''Sets pixel data
        PixelData (variable): An array of bytes that specify the pixel data. The size and format of this data can be
        computed from fields in the EmfPlusBitmap object, including the pixel format from the
        :py:class:`aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPixelFormat` enumeration (section 2.1.1.25).'''
        raise NotImplementedError()
    

class EmfPlusBlendBase(EmfPlusStructureObjectType):
    '''Base object for blend objects'''
    
    @property
    def blend_positions(self) -> List[float]:
        '''Gets blend positions
        An array of PositionCount 32-bit floating-point values
        that specify proportions of distance along the gradient line.
        Each element MUST be a number between 0.0 and 1.0 inclusive.
        For a linear gradient brush, 0.0 represents the starting point
        and 1.0 represents the ending point. For a path gradient brush,
        0.0 represents the midpoint and 1.0 represents an endpoint'''
        raise NotImplementedError()
    
    @blend_positions.setter
    def blend_positions(self, value : List[float]) -> None:
        '''Sets blend positions
        An array of PositionCount 32-bit floating-point values
        that specify proportions of distance along the gradient line.
        Each element MUST be a number between 0.0 and 1.0 inclusive.
        For a linear gradient brush, 0.0 represents the starting point
        and 1.0 represents the ending point. For a path gradient brush,
        0.0 represents the midpoint and 1.0 represents an endpoint'''
        raise NotImplementedError()
    

class EmfPlusBlendColors(EmfPlusBlendBase):
    '''The EmfPlusBlendColors object specifies positions and colors for the blend pattern of a gradient brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def blend_positions(self) -> List[float]:
        '''Gets blend positions
        An array of PositionCount 32-bit floating-point values
        that specify proportions of distance along the gradient line.
        Each element MUST be a number between 0.0 and 1.0 inclusive.
        For a linear gradient brush, 0.0 represents the starting point
        and 1.0 represents the ending point. For a path gradient brush,
        0.0 represents the midpoint and 1.0 represents an endpoint'''
        raise NotImplementedError()
    
    @blend_positions.setter
    def blend_positions(self, value : List[float]) -> None:
        '''Sets blend positions
        An array of PositionCount 32-bit floating-point values
        that specify proportions of distance along the gradient line.
        Each element MUST be a number between 0.0 and 1.0 inclusive.
        For a linear gradient brush, 0.0 represents the starting point
        and 1.0 represents the ending point. For a path gradient brush,
        0.0 represents the midpoint and 1.0 represents an endpoint'''
        raise NotImplementedError()
    
    @property
    def blend_argb_32_colors(self) -> List[int]:
        '''Gets an array of PositionCount EmfPlusARGB objects (section 2.2.2.1) that
        specify colors at the positions defined in the BlendPositions field.'''
        raise NotImplementedError()
    
    @blend_argb_32_colors.setter
    def blend_argb_32_colors(self, value : List[int]) -> None:
        '''Sets an array of PositionCount EmfPlusARGB objects (section 2.2.2.1) that
        specify colors at the positions defined in the BlendPositions field.'''
        raise NotImplementedError()
    

class EmfPlusBlendFactors(EmfPlusBlendBase):
    '''The EmfPlusBlendFactors object specifies positions and factors for the blend pattern of a gradient brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def blend_positions(self) -> List[float]:
        '''Gets blend positions
        An array of PositionCount 32-bit floating-point values
        that specify proportions of distance along the gradient line.
        Each element MUST be a number between 0.0 and 1.0 inclusive.
        For a linear gradient brush, 0.0 represents the starting point
        and 1.0 represents the ending point. For a path gradient brush,
        0.0 represents the midpoint and 1.0 represents an endpoint'''
        raise NotImplementedError()
    
    @blend_positions.setter
    def blend_positions(self, value : List[float]) -> None:
        '''Sets blend positions
        An array of PositionCount 32-bit floating-point values
        that specify proportions of distance along the gradient line.
        Each element MUST be a number between 0.0 and 1.0 inclusive.
        For a linear gradient brush, 0.0 represents the starting point
        and 1.0 represents the ending point. For a path gradient brush,
        0.0 represents the midpoint and 1.0 represents an endpoint'''
        raise NotImplementedError()
    
    @property
    def blend_factors(self) -> List[float]:
        '''Gets an array of PositionCount 32-bit floating point values that
        specify proportions of colors at the positions defined in the BlendPositions field.
        Each value MUST be a number between 0.0 and 1.0 inclusive.'''
        raise NotImplementedError()
    
    @blend_factors.setter
    def blend_factors(self, value : List[float]) -> None:
        '''Sets an array of PositionCount 32-bit floating point values that
        specify proportions of colors at the positions defined in the BlendPositions field.
        Each value MUST be a number between 0.0 and 1.0 inclusive.'''
        raise NotImplementedError()
    

class EmfPlusBlurEffect(EmfPlusImageEffectsObjectType):
    '''The BlurEffect object specifies a decrease in the difference in intensity between pixels in an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def blur_radius(self) -> float:
        '''Gets a 32-bit floating-point number that specifies the blur radius in pixels,
        which determines the number of pixels involved in calculating the new value of a given pixel.
        This value MUST be in the range 0.0 through 255.0.'''
        raise NotImplementedError()
    
    @blur_radius.setter
    def blur_radius(self, value : float) -> None:
        '''Sets a 32-bit floating-point number that specifies the blur radius in pixels,
        which determines the number of pixels involved in calculating the new value of a given pixel.
        This value MUST be in the range 0.0 through 255.0.'''
        raise NotImplementedError()
    
    @property
    def expand_edge(self) -> bool:
        '''Gets a 32-bit Boolean value that specifies whether the bitmap expands by
        an amount equal to the value of the BlurRadius to produce soft edges. This value MUST be
        one of the following:
        FALSE
        0x00000000
        The size of the bitmap MUST NOT change, and its soft edges SHOULD be clipped to
        the size of the BlurRadius.
        TRUE
        0x00000001
        The size of the bitmap SHOULD expand by an amount equal to the BlurRadius to
        produce soft edges.'''
        raise NotImplementedError()
    
    @expand_edge.setter
    def expand_edge(self, value : bool) -> None:
        '''Sets a 32-bit Boolean value that specifies whether the bitmap expands by
        an amount equal to the value of the BlurRadius to produce soft edges. This value MUST be
        one of the following:
        FALSE
        0x00000000
        The size of the bitmap MUST NOT change, and its soft edges SHOULD be clipped to
        the size of the BlurRadius.
        TRUE
        0x00000001
        The size of the bitmap SHOULD expand by an amount equal to the BlurRadius to
        produce soft edges.'''
        raise NotImplementedError()
    

class EmfPlusBoundaryBase(EmfPlusStructureObjectType):
    '''Base class for boundary objects'''
    

class EmfPlusBoundaryPathData(EmfPlusBoundaryBase):
    '''The EmfPlusBoundaryPathData object specifies a graphics path boundary for a gradient brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def boundary_path_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath:
        '''Gets an EmfPlusPath object (section 2.2.1.6) that specifies the boundary of the brush'''
        raise NotImplementedError()
    
    @boundary_path_data.setter
    def boundary_path_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath) -> None:
        '''Sets an EmfPlusPath object (section 2.2.1.6) that specifies the boundary of the brush'''
        raise NotImplementedError()
    

class EmfPlusBoundaryPointData(EmfPlusBoundaryBase):
    '''The EmfPlusBoundaryPointData object specifies a closed cardinal spline boundary for a gradient brush'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def boundary_point_data(self) -> List[aspose.imaging.PointF]:
        '''Gets an array of BoundaryPointCount EmfPlusPointF objects that specify the boundary of the brush.'''
        raise NotImplementedError()
    
    @boundary_point_data.setter
    def boundary_point_data(self, value : List[aspose.imaging.PointF]) -> None:
        '''Sets an array of BoundaryPointCount EmfPlusPointF objects that specify the boundary of the brush.'''
        raise NotImplementedError()
    

class EmfPlusBrightnessContrastEffect(EmfPlusImageEffectsObjectType):
    '''The BrightnessContrastEffect object specifies an expansion or contraction of the lightest and darkest areas of an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def brightness_level(self) -> int:
        '''Gets a 32-bit signed integer that specifies the brightness level. This
        value MUST be in the range -255 through 255, with effects as follows:
        -255 ≤ value < 0 As the value decreases, the brightness of the image SHOULD decrease.
        0 A value of 0 specifies that the brightness MUST NOT change.
        0 < value ≤ 255 As the value increases, the brightness of the image SHOULD increase.'''
        raise NotImplementedError()
    
    @brightness_level.setter
    def brightness_level(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the brightness level. This
        value MUST be in the range -255 through 255, with effects as follows:
        -255 ≤ value < 0 As the value decreases, the brightness of the image SHOULD decrease.
        0 A value of 0 specifies that the brightness MUST NOT change.
        0 < value ≤ 255 As the value increases, the brightness of the image SHOULD increase.'''
        raise NotImplementedError()
    
    @property
    def contrast_level(self) -> int:
        '''Gets a 32-bit signed integer that specifies the contrast level. This value
        MUST be in the range -100 through 100, with effects as follows:
        -100 ≤ value < 0 As the value decreases, the contrast of the image SHOULD decrease.
        0 A value of 0 specifies that the contrast MUST NOT change.
        0 < value ≤ 100 As the value increases, the contrast of the image SHOULD increase.'''
        raise NotImplementedError()
    
    @contrast_level.setter
    def contrast_level(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the contrast level. This value
        MUST be in the range -100 through 100, with effects as follows:
        -100 ≤ value < 0 As the value decreases, the contrast of the image SHOULD decrease.
        0 A value of 0 specifies that the contrast MUST NOT change.
        0 < value ≤ 100 As the value increases, the contrast of the image SHOULD increase.'''
        raise NotImplementedError()
    

class EmfPlusBrush(EmfPlusGraphicsObjectType):
    '''The EmfPlusBrush object specifies a graphics brush for filling regions.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def brush_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBaseBrushData:
        '''Gets the Brush data
        Variable-length data that defines the brush object specified in the Type field.
        The content and format of the data can be different for every brush type.
        EmfPlusHatchBrushData (section 2.2.2.20) (done)
        EmfPlusLinearGradientBrushData object (section 2.2.2.24) (done)
        EmfPlusPathGradientBrushData object (section 2.2.2.29) (done)
        EmfPlusSolidBrushData object (section 2.2.2.43) (done)
        EmfPlusTextureBrushData object (section 2.2.2.45) (done)'''
        raise NotImplementedError()
    
    @brush_data.setter
    def brush_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBaseBrushData) -> None:
        '''Sets the Brush data
        Variable-length data that defines the brush object specified in the Type field.
        The content and format of the data can be different for every brush type.
        EmfPlusHatchBrushData (section 2.2.2.20) (done)
        EmfPlusLinearGradientBrushData object (section 2.2.2.24) (done)
        EmfPlusPathGradientBrushData object (section 2.2.2.29) (done)
        EmfPlusSolidBrushData object (section 2.2.2.43) (done)
        EmfPlusTextureBrushData object (section 2.2.2.45) (done)'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBrushType:
        '''Gets the type.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBrushType) -> None:
        '''Sets the type.'''
        raise NotImplementedError()
    

class EmfPlusCharacterRange(EmfPlusStructureObjectType):
    '''EmfPlusCharacterRange description'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def first(self) -> int:
        '''Gets a 32-bit signed integer that
        specifies the first position of this range.'''
        raise NotImplementedError()
    
    @first.setter
    def first(self, value : int) -> None:
        '''Sets a 32-bit signed integer that
        specifies the first position of this range.'''
        raise NotImplementedError()
    
    @property
    def length(self) -> int:
        '''Gets a 32-bit signed integer that specifies
        the number of positions in this range'''
        raise NotImplementedError()
    
    @length.setter
    def length(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies
        the number of positions in this range'''
        raise NotImplementedError()
    

class EmfPlusColorBalanceEffect(EmfPlusImageEffectsObjectType):
    '''The ColorBalanceEffect object specifies adjustments to the relative amounts of red, green, and blue in an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def cyan_red(self) -> int:
        '''Gets a 32-bit signed integer that specifies a change in the amount of red in the
        image. This value MUST be in the range -100 through 100, with effects as follows:
        -100 ≤ value < 0
        As the value decreases, the amount of red in the image SHOULD decrease and the
        amount of cyan SHOULD increase.
        0 A value of 0 specifies that the amounts of red and cyan MUST NOT change.
        0 < value ≤ 100
        As the value increases, the amount of red in the image SHOULD increase and the
        amount of cyan SHOULD decrease.'''
        raise NotImplementedError()
    
    @cyan_red.setter
    def cyan_red(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies a change in the amount of red in the
        image. This value MUST be in the range -100 through 100, with effects as follows:
        -100 ≤ value < 0
        As the value decreases, the amount of red in the image SHOULD decrease and the
        amount of cyan SHOULD increase.
        0 A value of 0 specifies that the amounts of red and cyan MUST NOT change.
        0 < value ≤ 100
        As the value increases, the amount of red in the image SHOULD increase and the
        amount of cyan SHOULD decrease.'''
        raise NotImplementedError()
    
    @property
    def magenta_green(self) -> int:
        '''Gets a 32-bit signed integer that specifies a change in the amount of
        green in the image. This value MUST be in the range -100 through 100, with effects as
        follows:
        -100 ≤ value < 0
        As the value decreases, the amount of green in the image SHOULD decrease and
        the amount of magenta SHOULD increase.
        0 A value of 0 specifies that the amounts of green and magenta MUST NOT change.
        0 < value ≤ 100
        As the value increases, the amount of green in the image SHOULD increase and
        the amount of magenta SHOULD decrease.'''
        raise NotImplementedError()
    
    @magenta_green.setter
    def magenta_green(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies a change in the amount of
        green in the image. This value MUST be in the range -100 through 100, with effects as
        follows:
        -100 ≤ value < 0
        As the value decreases, the amount of green in the image SHOULD decrease and
        the amount of magenta SHOULD increase.
        0 A value of 0 specifies that the amounts of green and magenta MUST NOT change.
        0 < value ≤ 100
        As the value increases, the amount of green in the image SHOULD increase and
        the amount of magenta SHOULD decrease.'''
        raise NotImplementedError()
    
    @property
    def yellow_blue(self) -> int:
        '''Gets a 32-bit signed integer that specifies a change in the amount of blue in
        the image. This value MUST be in the range -100 through 100, with effects as follows:
        -100 ≤ value < 0
        As the value decreases, the amount of blue in the image SHOULD decrease and
        the amount of yellow SHOULD increase.
        0 A value of 0 specifies that the amounts of blue and yellow MUST NOT change.
        0 < value ≤ 100
        As the value increases, the amount of blue in the image SHOULD increase and the
        amount of yellow SHOULD decrease.'''
        raise NotImplementedError()
    
    @yellow_blue.setter
    def yellow_blue(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies a change in the amount of blue in
        the image. This value MUST be in the range -100 through 100, with effects as follows:
        -100 ≤ value < 0
        As the value decreases, the amount of blue in the image SHOULD decrease and
        the amount of yellow SHOULD increase.
        0 A value of 0 specifies that the amounts of blue and yellow MUST NOT change.
        0 < value ≤ 100
        As the value increases, the amount of blue in the image SHOULD increase and the
        amount of yellow SHOULD decrease.'''
        raise NotImplementedError()
    

class EmfPlusColorCurveEffect(EmfPlusImageEffectsObjectType):
    '''The ColorCurveEffect object specifies one of eight adjustments to the color curve of an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def curve_adjustment(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusCurveAdjustments:
        '''Gets a 32-bit unsigned integer that specifies the curve adjustment to
        apply to the colors in bitmap. This value MUST be defined in the CurveAdjustments
        enumeration (section 2.1.1.7).'''
        raise NotImplementedError()
    
    @curve_adjustment.setter
    def curve_adjustment(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusCurveAdjustments) -> None:
        '''Sets a 32-bit unsigned integer that specifies the curve adjustment to
        apply to the colors in bitmap. This value MUST be defined in the CurveAdjustments
        enumeration (section 2.1.1.7).'''
        raise NotImplementedError()
    
    @property
    def curve_channel(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusCurveChannel:
        '''Gets a 32-bit unsigned integer that specifies the color channel to which
        the curve adjustment applies. This value MUST be defined in the CurveChannel
        enumeration (section 2.1.1.8).'''
        raise NotImplementedError()
    
    @curve_channel.setter
    def curve_channel(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusCurveChannel) -> None:
        '''Sets a 32-bit unsigned integer that specifies the color channel to which
        the curve adjustment applies. This value MUST be defined in the CurveChannel
        enumeration (section 2.1.1.8).'''
        raise NotImplementedError()
    
    @property
    def adjustment_intensity(self) -> int:
        '''Gets a 32-bit signed integer that specifies the intensity of the
        curve adjustment to the color channel specified by CurveChannel. The ranges of meaningful
        values for this field vary according to the CurveAdjustment value, as follows:
        Exposure adjustment range:
        -255 ≤ value < 0 As the value decreases, the exposure of the image SHOULD decrease.
        0 A value of 0 specifies that the exposure MUST NOT change.
        0 < value ≤ 255 As the value increases, the exposure of the image SHOULD increase.
        Density adjustment range:
        -255 ≤ value < 0
        As the value decreases, the density of the image SHOULD decrease, resulting in
        a darker image.
        0 A value of 0 specifies that the density MUST NOT change.
        0 < value ≤ 255
        As the value increases, the density of the image SHOULD increase.
        Contrast adjustment range:
        -100 ≤ value < 0 As the value decreases, the contrast of the image SHOULD decrease.
        0 A value of 0 specifies that the contrast MUST NOT change.
        0 < value ≤ 100 As the value increases, the contrast of the image SHOULD increase.
        Highlight adjustment range:
        -100 ≤ value < 0 As the value decreases, the light areas of the image SHOULD appear darker.
        0 A value of 0 specifies that the highlight MUST NOT change.
        0 < value ≤ 100 As the value increases, the light areas of the image SHOULD appear lighter.
        Shadow adjustment range:
        -100 ≤ value < 0 As the value decreases, the dark areas of the image SHOULD appear darker.
        0 A value of 0 specifies that the shadow MUST NOT change.
        0 < value ≤ 100 As the value increases, the dark areas of the image SHOULD appear lighter.
        White saturation adjustment range:
        0 — 255 As the value increases, the upper limit of the range of color channel intensities increases.
        Black saturation adjustment range:
        0 — 255 As the value increases, the lower limit of the range of color channel intensities increases.'''
        raise NotImplementedError()
    
    @adjustment_intensity.setter
    def adjustment_intensity(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the intensity of the
        curve adjustment to the color channel specified by CurveChannel. The ranges of meaningful
        values for this field vary according to the CurveAdjustment value, as follows:
        Exposure adjustment range:
        -255 ≤ value < 0 As the value decreases, the exposure of the image SHOULD decrease.
        0 A value of 0 specifies that the exposure MUST NOT change.
        0 < value ≤ 255 As the value increases, the exposure of the image SHOULD increase.
        Density adjustment range:
        -255 ≤ value < 0
        As the value decreases, the density of the image SHOULD decrease, resulting in
        a darker image.
        0 A value of 0 specifies that the density MUST NOT change.
        0 < value ≤ 255
        As the value increases, the density of the image SHOULD increase.
        Contrast adjustment range:
        -100 ≤ value < 0 As the value decreases, the contrast of the image SHOULD decrease.
        0 A value of 0 specifies that the contrast MUST NOT change.
        0 < value ≤ 100 As the value increases, the contrast of the image SHOULD increase.
        Highlight adjustment range:
        -100 ≤ value < 0 As the value decreases, the light areas of the image SHOULD appear darker.
        0 A value of 0 specifies that the highlight MUST NOT change.
        0 < value ≤ 100 As the value increases, the light areas of the image SHOULD appear lighter.
        Shadow adjustment range:
        -100 ≤ value < 0 As the value decreases, the dark areas of the image SHOULD appear darker.
        0 A value of 0 specifies that the shadow MUST NOT change.
        0 < value ≤ 100 As the value increases, the dark areas of the image SHOULD appear lighter.
        White saturation adjustment range:
        0 — 255 As the value increases, the upper limit of the range of color channel intensities increases.
        Black saturation adjustment range:
        0 — 255 As the value increases, the lower limit of the range of color channel intensities increases.'''
        raise NotImplementedError()
    

class EmfPlusColorLookupTableEffect(EmfPlusImageEffectsObjectType):
    '''The ColorLookupTableEffect object specifies adjustments to the colors in an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def blue_lookup_table(self) -> List[int]:
        '''Gets an array of 256 bytes that specifies the adjustment for the blue color channel.'''
        raise NotImplementedError()
    
    @blue_lookup_table.setter
    def blue_lookup_table(self, value : List[int]) -> None:
        '''Sets an array of 256 bytes that specifies the adjustment for the blue color channel.'''
        raise NotImplementedError()
    
    @property
    def green_lookup_table(self) -> List[int]:
        '''Gets an array of 256 bytes that specifies the adjustment for the green color channel.'''
        raise NotImplementedError()
    
    @green_lookup_table.setter
    def green_lookup_table(self, value : List[int]) -> None:
        '''Sets an array of 256 bytes that specifies the adjustment for the green color channel.'''
        raise NotImplementedError()
    
    @property
    def red_lookup_table(self) -> List[int]:
        '''Gets an array of 256 bytes that specifies the adjustment for the red color channel.'''
        raise NotImplementedError()
    
    @red_lookup_table.setter
    def red_lookup_table(self, value : List[int]) -> None:
        '''Sets an array of 256 bytes that specifies the adjustment for the red color channel.'''
        raise NotImplementedError()
    
    @property
    def alpha_lookup_table(self) -> List[int]:
        '''Gets an array of 256 bytes that specifies the adjustment for the alpha color channel.'''
        raise NotImplementedError()
    
    @alpha_lookup_table.setter
    def alpha_lookup_table(self, value : List[int]) -> None:
        '''Sets an array of 256 bytes that specifies the adjustment for the alpha color channel.'''
        raise NotImplementedError()
    

class EmfPlusColorMatrixEffect(EmfPlusImageEffectsObjectType):
    '''The ColorMatrixEffect object specifies an affine transform to be applied to an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def matrix_n0(self) -> List[int]:
        '''Gets the Matrix[N][0] of the 5x5 color matrix. This row is used for transforms.'''
        raise NotImplementedError()
    
    @matrix_n0.setter
    def matrix_n0(self, value : List[int]) -> None:
        '''Sets the Matrix[N][0] of the 5x5 color matrix. This row is used for transforms.'''
        raise NotImplementedError()
    
    @property
    def matrix_n1(self) -> List[int]:
        '''Gets the Matrix[N][1] of the 5x5 color matrix. This row is used for transforms.'''
        raise NotImplementedError()
    
    @matrix_n1.setter
    def matrix_n1(self, value : List[int]) -> None:
        '''Sets the Matrix[N][1] of the 5x5 color matrix. This row is used for transforms.'''
        raise NotImplementedError()
    
    @property
    def matrix_n2(self) -> List[int]:
        '''Gets the Matrix[N][2] of the 5x5 color matrix. This row is used for transforms.'''
        raise NotImplementedError()
    
    @matrix_n2.setter
    def matrix_n2(self, value : List[int]) -> None:
        '''Sets the Matrix[N][2] of the 5x5 color matrix. This row is used for transforms.'''
        raise NotImplementedError()
    
    @property
    def matrix_n3(self) -> List[int]:
        '''Gets the Matrix[N][3] of the 5x5 color matrix. This row is used for transforms.'''
        raise NotImplementedError()
    
    @matrix_n3.setter
    def matrix_n3(self, value : List[int]) -> None:
        '''Sets the Matrix[N][3] of the 5x5 color matrix. This row is used for transforms.'''
        raise NotImplementedError()
    
    @property
    def matrix_n4(self) -> List[int]:
        '''Gets the Matrix[N][4] of the 5x5 color matrix. This row is used for color translations.'''
        raise NotImplementedError()
    
    @matrix_n4.setter
    def matrix_n4(self, value : List[int]) -> None:
        '''Sets the Matrix[N][4] of the 5x5 color matrix. This row is used for color translations.'''
        raise NotImplementedError()
    
    @property
    def matrix(self) -> List[List[int]]:
        '''Gets the matrix.'''
        raise NotImplementedError()
    
    @matrix.setter
    def matrix(self, value : List[List[int]]) -> None:
        '''Sets the matrix.'''
        raise NotImplementedError()
    

class EmfPlusCompoundLineData(EmfPlusStructureObjectType):
    '''The EmfPlusCompoundLineData object specifies line and space data for a compound line.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def compound_line_data(self) -> List[float]:
        '''Gets an array of CompoundLineDataSize floating-point values
        that specify the compound line of a pen. The elements
        MUST be in increasing order, and their values MUST be
        between 0.0 and 1.0, inclusive'''
        raise NotImplementedError()
    
    @compound_line_data.setter
    def compound_line_data(self, value : List[float]) -> None:
        '''Sets an array of CompoundLineDataSize floating-point values
        that specify the compound line of a pen. The elements
        MUST be in increasing order, and their values MUST be
        between 0.0 and 1.0, inclusive'''
        raise NotImplementedError()
    

class EmfPlusCompressedImage(EmfPlusBaseBitmapData):
    '''The EmfPlusCompressedImage object specifies an image with compressed data.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def compressed_image_data(self) -> List[int]:
        '''Gets an array of bytes, which specify the compressed image.
        The type of compression MUST be determined from the data itself.'''
        raise NotImplementedError()
    
    @compressed_image_data.setter
    def compressed_image_data(self, value : List[int]) -> None:
        '''Sets an array of bytes, which specify the compressed image.
        The type of compression MUST be determined from the data itself.'''
        raise NotImplementedError()
    

class EmfPlusCustomBaseLineCap(EmfPlusStructureObjectType):
    '''Base class for custom line cap types.'''
    

class EmfPlusCustomEndCapData(EmfPlusStructureObjectType):
    '''The EmfPlusCustomEndCapData object specifies a custom line cap for the end of a line.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def custom_end_cap(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomLineCap:
        '''Gets a custom line cap that defines the shape to draw at the end
        of a line. It can be any of various shapes, including a
        square, circle, or diamond'''
        raise NotImplementedError()
    
    @custom_end_cap.setter
    def custom_end_cap(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomLineCap) -> None:
        '''Sets a custom line cap that defines the shape to draw at the end
        of a line. It can be any of various shapes, including a
        square, circle, or diamond'''
        raise NotImplementedError()
    

class EmfPlusCustomLineCap(EmfPlusGraphicsObjectType):
    '''The EmfPlusCustomLineCap object specifies the shape to use at the ends of a line drawn by a graphics pen.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusCustomLineCapDataType:
        '''Gets a 32-bit signed integer that specifies the type of custom line cap object,
        which determines the contents of the CustomLineCapData field.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusCustomLineCapDataType) -> None:
        '''Sets a 32-bit signed integer that specifies the type of custom line cap object,
        which determines the contents of the CustomLineCapData field.'''
        raise NotImplementedError()
    
    @property
    def custom_line_cap_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomBaseLineCap:
        '''Gets Variable-length data that defines the custom line cap data object specified in the Type field. The content
        and format of the data can be different for every custom line cap type.'''
        raise NotImplementedError()
    
    @custom_line_cap_data.setter
    def custom_line_cap_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomBaseLineCap) -> None:
        '''Sets Variable-length data that defines the custom line cap data object specified in the Type field. The content
        and format of the data can be different for every custom line cap type.'''
        raise NotImplementedError()
    

class EmfPlusCustomLineCapArrowData(EmfPlusCustomBaseLineCap):
    '''The EmfPlusCustomLineCapArrowData object specifies adjustable arrow data for a custom line cap.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets a 32-bit floating-point value that specifies
        the width of the arrow cap'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies
        the width of the arrow cap'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets a 32-bit floating-point value that specifies
        the height of the arrow cap.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies
        the height of the arrow cap.'''
        raise NotImplementedError()
    
    @property
    def middle_inset(self) -> float:
        '''Gets a 32-bit floating-point value that specifies the number of pixels between the outline of the arrow
        cap and the fill of the arrow cap.'''
        raise NotImplementedError()
    
    @middle_inset.setter
    def middle_inset(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies the number of pixels between the outline of the arrow
        cap and the fill of the arrow cap.'''
        raise NotImplementedError()
    
    @property
    def fill_state(self) -> bool:
        '''Gets a 32-bit Boolean value that specifies whether the arrow cap is filled. If the arrow cap is
        not filled, only the outline is drawn'''
        raise NotImplementedError()
    
    @fill_state.setter
    def fill_state(self, value : bool) -> None:
        '''Sets a 32-bit Boolean value that specifies whether the arrow cap is filled. If the arrow cap is
        not filled, only the outline is drawn'''
        raise NotImplementedError()
    
    @property
    def line_start_cap(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType:
        '''Gets a 32-bit unsigned integer that specifies the value in the LineCap enumeration that indicates the line cap to
        be used at the start of the line to be drawn'''
        raise NotImplementedError()
    
    @line_start_cap.setter
    def line_start_cap(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType) -> None:
        '''Sets a 32-bit unsigned integer that specifies the value in the LineCap enumeration that indicates the line cap to
        be used at the start of the line to be drawn'''
        raise NotImplementedError()
    
    @property
    def line_end_cap(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType:
        '''Gets a 32-bit unsigned integer that specifies the value in the LineCap enumeration that indicates the line cap to
        be used at the end of the line to be drawn'''
        raise NotImplementedError()
    
    @line_end_cap.setter
    def line_end_cap(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType) -> None:
        '''Sets a 32-bit unsigned integer that specifies the value in the LineCap enumeration that indicates the line cap to
        be used at the end of the line to be drawn'''
        raise NotImplementedError()
    
    @property
    def line_join(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineJoinType:
        '''Gets a 32-bit unsigned integer that specifies the value in the LineJoin
        enumeration that specifies how to join two lines that are drawn by
        the same pen and whose ends meet. At the intersection of the two line ends,
        a line join makes the connection look more continuous.'''
        raise NotImplementedError()
    
    @line_join.setter
    def line_join(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineJoinType) -> None:
        '''Sets a 32-bit unsigned integer that specifies the value in the LineJoin
        enumeration that specifies how to join two lines that are drawn by
        the same pen and whose ends meet. At the intersection of the two line ends,
        a line join makes the connection look more continuous.'''
        raise NotImplementedError()
    
    @property
    def line_miter_limit(self) -> float:
        '''Gets a 32-bit floating-point value that specifies the limit of the
        thickness of the join on a mitered corner by setting
        the maximum allowed ratio of miter length to line width'''
        raise NotImplementedError()
    
    @line_miter_limit.setter
    def line_miter_limit(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies the limit of the
        thickness of the join on a mitered corner by setting
        the maximum allowed ratio of miter length to line width'''
        raise NotImplementedError()
    
    @property
    def width_scale(self) -> float:
        '''Gets a 32-bit floating-point value that specifies the amount by
        which to scale an EmfPlusCustomLineCap object with respect to the width
        of the graphics pen that is used to draw the lines'''
        raise NotImplementedError()
    
    @width_scale.setter
    def width_scale(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies the amount by
        which to scale an EmfPlusCustomLineCap object with respect to the width
        of the graphics pen that is used to draw the lines'''
        raise NotImplementedError()
    
    @property
    def fill_hot_spot(self) -> aspose.imaging.PointF:
        '''Gets EmfPlusPointF object that is not currently used. It MUST be set to {0.0, 0.0}.'''
        raise NotImplementedError()
    
    @fill_hot_spot.setter
    def fill_hot_spot(self, value : aspose.imaging.PointF) -> None:
        '''Sets EmfPlusPointF object that is not currently used. It MUST be set to {0.0, 0.0}.'''
        raise NotImplementedError()
    
    @property
    def line_hot_spot(self) -> aspose.imaging.PointF:
        '''Gets an EmfPlusPointF object that is not currently used. It MUST be set to {0.0, 0.0}.'''
        raise NotImplementedError()
    
    @line_hot_spot.setter
    def line_hot_spot(self, value : aspose.imaging.PointF) -> None:
        '''Sets an EmfPlusPointF object that is not currently used. It MUST be set to {0.0, 0.0}.'''
        raise NotImplementedError()
    

class EmfPlusCustomLineCapData(EmfPlusCustomBaseLineCap):
    '''The EmfPlusCustomLineCapData object specifies default data for a custom line cap.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def custom_line_cap_data_flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusCustomLineCapDataFlags:
        '''Gets 32-bit unsigned integer that specifies the data in the OptionalData field'''
        raise NotImplementedError()
    
    @custom_line_cap_data_flags.setter
    def custom_line_cap_data_flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusCustomLineCapDataFlags) -> None:
        '''Sets 32-bit unsigned integer that specifies the data in the OptionalData field'''
        raise NotImplementedError()
    
    @property
    def base_cap(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType:
        '''Gets 32-bit unsigned integer that specifies the value from the LineCap enumeration (section 2.1.1.18)
        on which the custom line cap is based.'''
        raise NotImplementedError()
    
    @base_cap.setter
    def base_cap(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType) -> None:
        '''Sets 32-bit unsigned integer that specifies the value from the LineCap enumeration (section 2.1.1.18)
        on which the custom line cap is based.'''
        raise NotImplementedError()
    
    @property
    def base_inset(self) -> float:
        '''Gets  32-bit floating-point value that specifies the distance between the beginning
        of the line cap and the end of the line.'''
        raise NotImplementedError()
    
    @base_inset.setter
    def base_inset(self, value : float) -> None:
        '''Sets  32-bit floating-point value that specifies the distance between the beginning
        of the line cap and the end of the line.'''
        raise NotImplementedError()
    
    @property
    def stroke_start_cap(self) -> int:
        '''Gets  32-bit unsigned integer that specifies the value in the LineCap enumeration that indicates the
        line cap used at the start of the line to be drawn'''
        raise NotImplementedError()
    
    @stroke_start_cap.setter
    def stroke_start_cap(self, value : int) -> None:
        '''Sets  32-bit unsigned integer that specifies the value in the LineCap enumeration that indicates the
        line cap used at the start of the line to be drawn'''
        raise NotImplementedError()
    
    @property
    def stroke_end_cap(self) -> int:
        '''Gets  32-bit unsigned integer that specifies the value in the LineCap enumeration that indicates what
        line cap is to be used at the end of the line to be drawn.'''
        raise NotImplementedError()
    
    @stroke_end_cap.setter
    def stroke_end_cap(self, value : int) -> None:
        '''Sets  32-bit unsigned integer that specifies the value in the LineCap enumeration that indicates what
        line cap is to be used at the end of the line to be drawn.'''
        raise NotImplementedError()
    
    @property
    def stroke_join(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineJoinType:
        '''Gets 32-bit unsigned integer that specifies the value in the LineJoin enumeration
        (section 2.1.1.19), which specifies how to join two lines that are drawn by
        the same pen and whose ends meet. At the intersection of the two line ends,
        a line join makes the connection look more continuous.'''
        raise NotImplementedError()
    
    @stroke_join.setter
    def stroke_join(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineJoinType) -> None:
        '''Sets 32-bit unsigned integer that specifies the value in the LineJoin enumeration
        (section 2.1.1.19), which specifies how to join two lines that are drawn by
        the same pen and whose ends meet. At the intersection of the two line ends,
        a line join makes the connection look more continuous.'''
        raise NotImplementedError()
    
    @property
    def stroke_miter_limit(self) -> float:
        '''Gets  32-bit floating-point value that contains the limit of the thickness
        of the join on a mitered corner by setting  the maximum allowed ratio
        of miter length to line width.'''
        raise NotImplementedError()
    
    @stroke_miter_limit.setter
    def stroke_miter_limit(self, value : float) -> None:
        '''Sets  32-bit floating-point value that contains the limit of the thickness
        of the join on a mitered corner by setting  the maximum allowed ratio
        of miter length to line width.'''
        raise NotImplementedError()
    
    @property
    def width_scale(self) -> float:
        '''Gets 32-bit floating-point value that specifies the amount by which to
        scale the custom line cap with respect to the width of the EmfPlusPen
        object (section 2.2.1.7) that is used to draw the lines.'''
        raise NotImplementedError()
    
    @width_scale.setter
    def width_scale(self, value : float) -> None:
        '''Sets 32-bit floating-point value that specifies the amount by which to
        scale the custom line cap with respect to the width of the EmfPlusPen
        object (section 2.2.1.7) that is used to draw the lines.'''
        raise NotImplementedError()
    
    @property
    def fill_hot_spot(self) -> aspose.imaging.PointF:
        '''Gets EmfPlusPointF object that is not currently used. It MUST be set to {0.0, 0.0}.'''
        raise NotImplementedError()
    
    @fill_hot_spot.setter
    def fill_hot_spot(self, value : aspose.imaging.PointF) -> None:
        '''Sets EmfPlusPointF object that is not currently used. It MUST be set to {0.0, 0.0}.'''
        raise NotImplementedError()
    
    @property
    def stroke_hot_spot(self) -> aspose.imaging.PointF:
        '''Gets EmfPlusPointF object that is not currently used. It MUST be set to {0.0, 0.0}.'''
        raise NotImplementedError()
    
    @stroke_hot_spot.setter
    def stroke_hot_spot(self, value : aspose.imaging.PointF) -> None:
        '''Sets EmfPlusPointF object that is not currently used. It MUST be set to {0.0, 0.0}.'''
        raise NotImplementedError()
    
    @property
    def optional_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomLineCapOptionalData:
        '''Gets  optional EmfPlusCustomLineCapOptionalData object (section 2.2.2.14)
        that specifies additional data for the custom graphics line cap. T
        he specific contents of this field are determined
        by the value of the CustomLineCapDataFlags field.'''
        raise NotImplementedError()
    
    @optional_data.setter
    def optional_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomLineCapOptionalData) -> None:
        '''Sets  optional EmfPlusCustomLineCapOptionalData object (section 2.2.2.14)
        that specifies additional data for the custom graphics line cap. T
        he specific contents of this field are determined
        by the value of the CustomLineCapDataFlags field.'''
        raise NotImplementedError()
    

class EmfPlusCustomLineCapOptionalData(EmfPlusStructureObjectType):
    '''The EmfPlusCustomLineCapOptionalData object specifies optional fill and outline data for a custom line cap.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def fill_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusFillPath:
        '''Gets optional EmfPlusFillPath object (section 2.2.2.17) that specifies the path for filling a custom
        graphics line cap. This field MUST be present if the CustomLineCapDataFillPath flag is set in the CustomLineCapDataFlags
        field of the EmfPlusCustomLineCapData object.'''
        raise NotImplementedError()
    
    @fill_data.setter
    def fill_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusFillPath) -> None:
        '''Sets optional EmfPlusFillPath object (section 2.2.2.17) that specifies the path for filling a custom
        graphics line cap. This field MUST be present if the CustomLineCapDataFillPath flag is set in the CustomLineCapDataFlags
        field of the EmfPlusCustomLineCapData object.'''
        raise NotImplementedError()
    
    @property
    def outline_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusLinePath:
        '''Gets optional EmfPlusLinePath object (section 2.2.2.26)
        that specifies the path for outlining a custom graphics line cap. This field MUST be present if the CustomLineCapDataLinePath flag is set in the CustomLineCapDataFlags
        field of the EmfPlusCustomLineCapData object.'''
        raise NotImplementedError()
    
    @outline_data.setter
    def outline_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusLinePath) -> None:
        '''Sets optional EmfPlusLinePath object (section 2.2.2.26)
        that specifies the path for outlining a custom graphics line cap. This field MUST be present if the CustomLineCapDataLinePath flag is set in the CustomLineCapDataFlags
        field of the EmfPlusCustomLineCapData object.'''
        raise NotImplementedError()
    

class EmfPlusCustomStartCapData(EmfPlusStructureObjectType):
    '''The EmfPlusCustomStartCapData object specifies a custom line cap for the start of a line.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def custom_start_cap(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomLineCap:
        '''Gets custom line cap that defines the shape to draw at the end
        of a line. It can be any of various shapes, including a
        square, circle, or diamond'''
        raise NotImplementedError()
    
    @custom_start_cap.setter
    def custom_start_cap(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomLineCap) -> None:
        '''Sets custom line cap that defines the shape to draw at the end
        of a line. It can be any of various shapes, including a
        square, circle, or diamond'''
        raise NotImplementedError()
    

class EmfPlusDashedLineData(EmfPlusStructureObjectType):
    '''The EmfPlusDashedLineData object specifies properties of a dashed line for a graphics pen.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def dashed_line_data(self) -> List[float]:
        '''Gets array of DashedLineDataSize floating-point values
        that specify the lengths of the dashes and spaces in
        a dashed line'''
        raise NotImplementedError()
    
    @dashed_line_data.setter
    def dashed_line_data(self, value : List[float]) -> None:
        '''Sets array of DashedLineDataSize floating-point values
        that specify the lengths of the dashes and spaces in
        a dashed line'''
        raise NotImplementedError()
    

class EmfPlusFillPath(EmfPlusStructureObjectType):
    '''The EmfPlusFillPath object specifies a graphics path for filling a custom line cap'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def fill_path(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath:
        '''Gets EmfPlusPath object (section 2.2.1.6) that specifies the area to fill.'''
        raise NotImplementedError()
    
    @fill_path.setter
    def fill_path(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath) -> None:
        '''Sets EmfPlusPath object (section 2.2.1.6) that specifies the area to fill.'''
        raise NotImplementedError()
    

class EmfPlusFocusScaleData(EmfPlusStructureObjectType):
    '''The EmfPlusFocusScaleData object specifies focus scales for the blend pattern of a path gradient brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def focus_scale_x(self) -> float:
        '''Gets a floating-point value that defines the horizontal focus scale.
        The focus scale MUST be a value between 0.0 and 1.0, exclusive.'''
        raise NotImplementedError()
    
    @focus_scale_x.setter
    def focus_scale_x(self, value : float) -> None:
        '''Sets a floating-point value that defines the horizontal focus scale.
        The focus scale MUST be a value between 0.0 and 1.0, exclusive.'''
        raise NotImplementedError()
    
    @property
    def focus_scale_y(self) -> float:
        '''Gets a floating-point value that defines the vertical focus scale.
        The focus scale MUST be a value between 0.0 and 1.0, exclusive.'''
        raise NotImplementedError()
    
    @focus_scale_y.setter
    def focus_scale_y(self, value : float) -> None:
        '''Sets a floating-point value that defines the vertical focus scale.
        The focus scale MUST be a value between 0.0 and 1.0, exclusive.'''
        raise NotImplementedError()
    
    @property
    def focus_scale_count(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of focus scales.
        This value MUST be 2.'''
        raise NotImplementedError()
    
    @focus_scale_count.setter
    def focus_scale_count(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of focus scales.
        This value MUST be 2.'''
        raise NotImplementedError()
    

class EmfPlusFont(EmfPlusGraphicsObjectType):
    '''The EmfPlusFont object specifies properties that determine the appearance of text, including
    typeface, size, and style.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def family_name(self) -> str:
        '''Gets a string of Length Unicode characters that contains
        the name of the font family'''
        raise NotImplementedError()
    
    @family_name.setter
    def family_name(self, value : str) -> None:
        '''Sets a string of Length Unicode characters that contains
        the name of the font family'''
        raise NotImplementedError()
    
    @property
    def font_style_flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusFontStyleFlags:
        '''Gets a 32-bit signed integer that specifies attributes of the
        character glyphs that affect the appearance of the font,
        such as bold and italic. This value MUST be composed of
        FontStyle flags (section 2.1.2.4).'''
        raise NotImplementedError()
    
    @font_style_flags.setter
    def font_style_flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusFontStyleFlags) -> None:
        '''Sets a 32-bit signed integer that specifies attributes of the
        character glyphs that affect the appearance of the font,
        such as bold and italic. This value MUST be composed of
        FontStyle flags (section 2.1.2.4).'''
        raise NotImplementedError()
    
    @property
    def size_unit(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusUnitType:
        '''Gets a 32-bit unsigned integer that specifies the units used for
        the EmSize field. These are typically the units that were
        employed when designing the font. The value MUST be in the
        UnitType enumeration (section 2.1.1.33).'''
        raise NotImplementedError()
    
    @size_unit.setter
    def size_unit(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusUnitType) -> None:
        '''Sets a 32-bit unsigned integer that specifies the units used for
        the EmSize field. These are typically the units that were
        employed when designing the font. The value MUST be in the
        UnitType enumeration (section 2.1.1.33).'''
        raise NotImplementedError()
    
    @property
    def em_size(self) -> float:
        '''Gets a 32-bit floating-point value that specifies the em size of the
        font in units specified by the SizeUnit field.'''
        raise NotImplementedError()
    
    @em_size.setter
    def em_size(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies the em size of the
        font in units specified by the SizeUnit field.'''
        raise NotImplementedError()
    

class EmfPlusGraphicsObjectType(EmfPlusObject):
    '''The Graphics Objects specify parameters for graphics output. They are part of the playback device context and are persistent during the playback of an EMF+ metafile.'''
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    

class EmfPlusGraphicsVersion(EmfPlusStructureObjectType):
    '''The EmfPlusGraphicsVersion object specifies the version of operating system graphics that is used to create an EMF+
    metafile.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def metafile_signature(self) -> int:
        '''Gets a MetafileSignature (20 bits): A value that identifies the type of metafile. The value for an EMF+ metafile is
        0xDBC01.'''
        raise NotImplementedError()
    
    @metafile_signature.setter
    def metafile_signature(self, value : int) -> None:
        '''Gets a MetafileSignature (20 bits): A value that identifies the type of metafile. The value for an EMF+ metafile is
        0xDBC01.'''
        raise NotImplementedError()
    
    @property
    def graphics_version(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusGraphicsVersionEnum:
        '''Gets a GraphicsVersion (12 bits): The version of operating system graphics. This value MUST be defined in the
        :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion` enumeration'''
        raise NotImplementedError()
    
    @graphics_version.setter
    def graphics_version(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusGraphicsVersionEnum) -> None:
        '''Gets a GraphicsVersion (12 bits): The version of operating system graphics. This value MUST be defined in the
        :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion` enumeration'''
        raise NotImplementedError()
    

class EmfPlusHatchBrushData(EmfPlusBaseBrushData):
    '''The EmfPlusHatchBrushData object specifies a hatch pattern for a graphics brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def back_argb_32_color(self) -> int:
        '''Gets a 32-bit EmfPlusArgb object that specifies the color used to paint the background of the hatch pattern.'''
        raise NotImplementedError()
    
    @back_argb_32_color.setter
    def back_argb_32_color(self, value : int) -> None:
        '''Sets a 32-bit EmfPlusArgb object that specifies the color used to paint the background of the hatch pattern.'''
        raise NotImplementedError()
    
    @property
    def fore_argb_32_color(self) -> int:
        '''Gets a 32-bit EmfPlusArgb object that specifies the color used to draw the lines of the hatch pattern.'''
        raise NotImplementedError()
    
    @fore_argb_32_color.setter
    def fore_argb_32_color(self, value : int) -> None:
        '''Sets a 32-bit EmfPlusArgb object that specifies the color used to draw the lines of the hatch pattern.'''
        raise NotImplementedError()
    
    @property
    def hatch_style(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusHatchStyle:
        '''Gets a 32-bit unsigned integer that specifies the brush hatch style. It MUST be defined in the :py:class:`aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusHatchStyle` enumeration.'''
        raise NotImplementedError()
    
    @hatch_style.setter
    def hatch_style(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusHatchStyle) -> None:
        '''Sets a 32-bit unsigned integer that specifies the brush hatch style. It MUST be defined in the :py:class:`aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusHatchStyle` enumeration.'''
        raise NotImplementedError()
    

class EmfPlusHueSaturationLightnessEffect(EmfPlusImageEffectsObjectType):
    '''The HueSaturationLightnessEffect object specifies adjustments to the hue, saturation, and lightness of an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def hue_level(self) -> int:
        '''Gets the Specifies the adjustment to the hue.
        -180 ≤ value < 0 Negative values specify clockwise rotation on the color wheel.
        0 A value of 0 specifies that the hue MUST NOT change.
        0 < value ≤ 180 Positive values specify counter-clockwise rotation on the color wheel.'''
        raise NotImplementedError()
    
    @hue_level.setter
    def hue_level(self, value : int) -> None:
        '''Sets the Specifies the adjustment to the hue.
        -180 ≤ value < 0 Negative values specify clockwise rotation on the color wheel.
        0 A value of 0 specifies that the hue MUST NOT change.
        0 < value ≤ 180 Positive values specify counter-clockwise rotation on the color wheel.'''
        raise NotImplementedError()
    
    @property
    def saturation_level(self) -> int:
        '''Gets the Specifies the adjustment to the saturation.
        -100 ≤ value < 0 Negative values specify decreasing saturation.
        0 A value of 0 specifies that the saturation MUST NOT change.
        0 < value ≤ 100 Positive values specify increasing saturation.'''
        raise NotImplementedError()
    
    @saturation_level.setter
    def saturation_level(self, value : int) -> None:
        '''Sets the Specifies the adjustment to the saturation.
        -100 ≤ value < 0 Negative values specify decreasing saturation.
        0 A value of 0 specifies that the saturation MUST NOT change.
        0 < value ≤ 100 Positive values specify increasing saturation.'''
        raise NotImplementedError()
    
    @property
    def lightness_level(self) -> int:
        '''Gets the Specifies the adjustment to the lightness.
        -100 ≤ value < 0 Negative values specify decreasing lightness.
        0 A value of 0 specifies that the lightness MUST NOT change.
        0 < value ≤ 100 Positive values specify increasing lightness.'''
        raise NotImplementedError()
    
    @lightness_level.setter
    def lightness_level(self, value : int) -> None:
        '''Sets the Specifies the adjustment to the lightness.
        -100 ≤ value < 0 Negative values specify decreasing lightness.
        0 A value of 0 specifies that the lightness MUST NOT change.
        0 < value ≤ 100 Positive values specify increasing lightness.'''
        raise NotImplementedError()
    

class EmfPlusImage(EmfPlusGraphicsObjectType):
    '''The EmfPlusImage object specifies a graphics image in the form of a bitmap or metafile.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def image_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBaseImageData:
        '''Gets the Image data
        Variable-length data that defines the image data specified
        in the Type field. The content and format of the data can
        be different for every image type.'''
        raise NotImplementedError()
    
    @image_data.setter
    def image_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBaseImageData) -> None:
        '''Sets the Image data
        Variable-length data that defines the image data specified
        in the Type field. The content and format of the data can
        be different for every image type.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusImageDataType:
        '''Gets image type
        A 32-bit unsigned integer that specifies the type of data
        in the ImageData field. This value MUST be defined in the
        ImageDataType enumeration (section 2.1.1.15).'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusImageDataType) -> None:
        '''Sets image type
        A 32-bit unsigned integer that specifies the type of data
        in the ImageData field. This value MUST be defined in the
        ImageDataType enumeration (section 2.1.1.15).'''
        raise NotImplementedError()
    

class EmfPlusImageAttributes(EmfPlusGraphicsObjectType):
    '''The EmfPlusImageAttributes object specifies how bitmap image
    colors are manipulated during rendering.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusWrapMode:
        '''Gets a 32-bit unsigned integer that specifies how to handle edge conditions with
        a value from the WrapMode enumeration (section 2.1.1.34).'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusWrapMode) -> None:
        '''Sets a 32-bit unsigned integer that specifies how to handle edge conditions with
        a value from the WrapMode enumeration (section 2.1.1.34).'''
        raise NotImplementedError()
    
    @property
    def clamp_argb_32_color(self) -> int:
        '''Gets EmfPlusARGB (section 2.2.2.1) object that specifies the edge color to use
        when the WrapMode value is WrapModeClamp. This color is visible when the
        source rectangle processed by an EmfPlusDrawImage (section 2.3.4.8) record
        is larger than the image itself.'''
        raise NotImplementedError()
    
    @clamp_argb_32_color.setter
    def clamp_argb_32_color(self, value : int) -> None:
        '''Sets EmfPlusARGB (section 2.2.2.1) object that specifies the edge color to use
        when the WrapMode value is WrapModeClamp. This color is visible when the
        source rectangle processed by an EmfPlusDrawImage (section 2.3.4.8) record
        is larger than the image itself.'''
        raise NotImplementedError()
    
    @property
    def object_clamp(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusObjectClamp:
        '''Gets 32-bit signed integer that specifies the object clamping behavior.
        It is not used until this object is applied to an image being
        drawn. This value MUST be one of the values defined in the
        following table.'''
        raise NotImplementedError()
    
    @object_clamp.setter
    def object_clamp(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusObjectClamp) -> None:
        '''Sets 32-bit signed integer that specifies the object clamping behavior.
        It is not used until this object is applied to an image being
        drawn. This value MUST be one of the values defined in the
        following table.'''
        raise NotImplementedError()
    

class EmfPlusImageEffectsObjectType(EmfPlusObject):
    '''The Image Effects Objects specify parameters for graphics image effects, which can be applied to bitmap images'''
    

class EmfPlusLanguageIdentifier(EmfPlusStructureObjectType):
    '''The EmfPlusLanguageIdentifier object specifies a language identifier that corresponds to the natural
    language in a locale, including countries, geographical regions, and administrative districts.
    Each language identifier is an encoding of a primary language value and sublanguage value.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def value(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLanguageIdentifierType:
        '''Gets the value of the field
        0 1 2 3 4 5 6 7 8 9 1 0 1 2 3 4 5 6 7 8 9 2 0 1 2 3 4 5 6 7 8 9 3 0 1
        SubLanguageId|   PrimaryLanguageId |
        SubLanguageId (6 bits): The country, geographic region or administrative district for the natural language specified in the PrimaryLanguageId field.
        Sublanguage identifiers are vendor-extensible. Vendor-defined sublanguage identifiers MUST be in the range 0x20 to 0x3F, inclusive.
        PrimaryLanguageId (10 bits): The natural language.
        Primary language identifiers are vendor-extensible. Vendor-defined primary language identifiers MUST be in the range 0x0200 to 0x03FF, inclusive.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLanguageIdentifierType) -> None:
        '''Sets the value of the field
        0 1 2 3 4 5 6 7 8 9 1 0 1 2 3 4 5 6 7 8 9 2 0 1 2 3 4 5 6 7 8 9 3 0 1
        SubLanguageId|   PrimaryLanguageId |
        SubLanguageId (6 bits): The country, geographic region or administrative district for the natural language specified in the PrimaryLanguageId field.
        Sublanguage identifiers are vendor-extensible. Vendor-defined sublanguage identifiers MUST be in the range 0x20 to 0x3F, inclusive.
        PrimaryLanguageId (10 bits): The natural language.
        Primary language identifiers are vendor-extensible. Vendor-defined primary language identifiers MUST be in the range 0x0200 to 0x03FF, inclusive.'''
        raise NotImplementedError()
    

class EmfPlusLevelsEffect(EmfPlusImageEffectsObjectType):
    '''The LevelsEffect object specifies adjustments to the highlights, midtones, and shadows of an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def highlight(self) -> int:
        '''Gets the Specifies how much to lighten the highlights of an image. The color
        channel values at the high end of the intensity range are altered more than values near the
        middle or low ends, which means an image can be lightened without losing the contrast
        between the darker portions of the image.
        0 ≤ value < Specifies that highlights with a percent of intensity above this threshold SHOULD
        100 be increased.
        100 Specifies that highlights MUST NOT change.'''
        raise NotImplementedError()
    
    @highlight.setter
    def highlight(self, value : int) -> None:
        '''Sets the Specifies how much to lighten the highlights of an image. The color
        channel values at the high end of the intensity range are altered more than values near the
        middle or low ends, which means an image can be lightened without losing the contrast
        between the darker portions of the image.
        0 ≤ value < Specifies that highlights with a percent of intensity above this threshold SHOULD
        100 be increased.
        100 Specifies that highlights MUST NOT change.'''
        raise NotImplementedError()
    
    @property
    def mid_tone(self) -> int:
        '''Gets the Specifies how much to lighten or darken the midtones of an image. Color
        channel values in the middle of the intensity range are altered more than values near the high
        or low ends, which means an image can be lightened or darkened without losing the contrast
        between the darkest and lightest portions of the image.
        -100 ≤ value < 0 Specifies that midtones are made darker.
        0 Specifies that midtones MUST NOT change.
        0 < value ≤ 100 Specifies that midtones are made lighter.'''
        raise NotImplementedError()
    
    @mid_tone.setter
    def mid_tone(self, value : int) -> None:
        '''Sets the Specifies how much to lighten or darken the midtones of an image. Color
        channel values in the middle of the intensity range are altered more than values near the high
        or low ends, which means an image can be lightened or darkened without losing the contrast
        between the darkest and lightest portions of the image.
        -100 ≤ value < 0 Specifies that midtones are made darker.
        0 Specifies that midtones MUST NOT change.
        0 < value ≤ 100 Specifies that midtones are made lighter.'''
        raise NotImplementedError()
    
    @property
    def shadow(self) -> int:
        '''Gets the Specifies how much to darken the shadows of an image. Color channel
        values at the low end of the intensity range are altered more than values near the middle or
        high ends, which means an image can be darkened without losing the contrast between the
        lighter portions of the image.
        0 Specifies that shadows MUST NOT change.
        0 < value ≤ 100
        Specifies that shadows with a percent of intensity below this threshold are made
        darker.'''
        raise NotImplementedError()
    
    @shadow.setter
    def shadow(self, value : int) -> None:
        '''Sets the Specifies how much to darken the shadows of an image. Color channel
        values at the low end of the intensity range are altered more than values near the middle or
        high ends, which means an image can be darkened without losing the contrast between the
        lighter portions of the image.
        0 Specifies that shadows MUST NOT change.
        0 < value ≤ 100
        Specifies that shadows with a percent of intensity below this threshold are made
        darker.'''
        raise NotImplementedError()
    

class EmfPlusLinePath(EmfPlusStructureObjectType):
    '''The EmfPlusLinePath object specifies a graphics path for outlining a custom line cap.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def line_path(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath:
        '''Gets an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath` object that defines the outline.'''
        raise NotImplementedError()
    
    @line_path.setter
    def line_path(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath) -> None:
        '''Sets an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath` object that defines the outline.'''
        raise NotImplementedError()
    

class EmfPlusLinearGradientBrushData(EmfPlusBaseBrushData):
    '''The EmfPlusLinearGradientBrushData object specifies a linear gradient for a graphics brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def brush_data_flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBrushDataFlags:
        '''Gets the brush data flags.'''
        raise NotImplementedError()
    
    @brush_data_flags.setter
    def brush_data_flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBrushDataFlags) -> None:
        '''Sets the brush data flags.'''
        raise NotImplementedError()
    
    @property
    def end_argb_32_color(self) -> int:
        '''Gets the end color.'''
        raise NotImplementedError()
    
    @end_argb_32_color.setter
    def end_argb_32_color(self, value : int) -> None:
        '''Sets the end color.'''
        raise NotImplementedError()
    
    @property
    def optional_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusLinearGradientBrushOptionalData:
        '''Gets the optional data.'''
        raise NotImplementedError()
    
    @optional_data.setter
    def optional_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusLinearGradientBrushOptionalData) -> None:
        '''Sets the optional data.'''
        raise NotImplementedError()
    
    @property
    def rect_f(self) -> aspose.imaging.RectangleF:
        '''Gets the rect f.'''
        raise NotImplementedError()
    
    @rect_f.setter
    def rect_f(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rect f.'''
        raise NotImplementedError()
    
    @property
    def start_argb_32_color(self) -> int:
        '''Gets the start color.'''
        raise NotImplementedError()
    
    @start_argb_32_color.setter
    def start_argb_32_color(self, value : int) -> None:
        '''Sets the start color.'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusWrapMode:
        '''Gets the wrap mode.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusWrapMode) -> None:
        '''Sets the wrap mode.'''
        raise NotImplementedError()
    

class EmfPlusLinearGradientBrushOptionalData(EmfPlusStructureObjectType):
    '''The EmfPlusLinearGradientBrushOptionalData object specifies optional data for a linear gradient brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def transform_matrix(self) -> aspose.imaging.Matrix:
        '''Gets an optional EmfPlusTransformMatrix object (section 2.2.2.47) that specifies a
        world space to device space transform for the linear gradient brush.
        This field MUST be present if the BrushDataTransform flag is set in the
        BrushDataFlags field of the EmfPlusLinearGradientBrushData object.'''
        raise NotImplementedError()
    
    @transform_matrix.setter
    def transform_matrix(self, value : aspose.imaging.Matrix) -> None:
        '''Sets an optional EmfPlusTransformMatrix object (section 2.2.2.47) that specifies a
        world space to device space transform for the linear gradient brush.
        This field MUST be present if the BrushDataTransform flag is set in the
        BrushDataFlags field of the EmfPlusLinearGradientBrushData object.'''
        raise NotImplementedError()
    
    @property
    def blend_pattern(self) -> List[aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBlendBase]:
        '''Gets an optional blend pattern for the linear gradient brush. If this field is present,
        it MUST contain either an EmfPlusBlendColors object (section 2.2.2.4),
        or one or two EmfPlusBlendFactors objects (section 2.2.2.5),
        but it MUST NOT contain both. The table below shows the valid combinations of
        EmfPlusLinearGradientBrushData BrushData flags and the corresponding blend patterns:
        EmfPlusBlendFactors'''
        raise NotImplementedError()
    
    @blend_pattern.setter
    def blend_pattern(self, value : List[aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBlendBase]) -> None:
        '''Sets an optional blend pattern for the linear gradient brush. If this field is present,
        it MUST contain either an EmfPlusBlendColors object (section 2.2.2.4),
        or one or two EmfPlusBlendFactors objects (section 2.2.2.5),
        but it MUST NOT contain both. The table below shows the valid combinations of
        EmfPlusLinearGradientBrushData BrushData flags and the corresponding blend patterns:
        EmfPlusBlendFactors'''
        raise NotImplementedError()
    
    @property
    def blend_pattern_as_preset_colors(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBlendColors:
        '''Gets the blend pattern as preset colors.'''
        raise NotImplementedError()
    
    @property
    def blend_pattern_as_blend_factors_h(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBlendFactors:
        '''Gets the blend pattern as blend factors h.'''
        raise NotImplementedError()
    
    @property
    def blend_pattern_as_blend_factors_v(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBlendFactors:
        '''Gets the blend pattern as blend factors v.'''
        raise NotImplementedError()
    

class EmfPlusMetafile(EmfPlusBaseImageData):
    '''The EmfPlusMetafileData object specifies a metafile that contains a graphics image'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusMetafile` class.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusMetafileDataType:
        '''Gets 32-bit unsigned integer that specifies the type of metafile that is embedded
        in the MetafileData field. This value MUST be defined in the MetafileDataType
        enumeration (section 2.1.1.21).'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusMetafileDataType) -> None:
        '''Sets 32-bit unsigned integer that specifies the type of metafile that is embedded
        in the MetafileData field. This value MUST be defined in the MetafileDataType
        enumeration (section 2.1.1.21).'''
        raise NotImplementedError()
    
    @property
    def metafile_data_size(self) -> int:
        '''Gets 32-bit unsigned integer that specifies the size in bytes of the metafile
        data in the MetafileData field'''
        raise NotImplementedError()
    
    @metafile_data_size.setter
    def metafile_data_size(self, value : int) -> None:
        '''Sets 32-bit unsigned integer that specifies the size in bytes of the metafile
        data in the MetafileData field'''
        raise NotImplementedError()
    
    @property
    def metafile_data(self) -> List[int]:
        '''Gets variable-length data that specifies the embedded metafile. The content
        and format of the data can be different for each metafile type.'''
        raise NotImplementedError()
    
    @metafile_data.setter
    def metafile_data(self, value : List[int]) -> None:
        '''Sets variable-length data that specifies the embedded metafile. The content
        and format of the data can be different for each metafile type.'''
        raise NotImplementedError()
    

class EmfPlusObject(aspose.imaging.fileformats.emf.MetaObject):
    '''Base Emf+ object type.'''
    

class EmfPlusPalette(EmfPlusStructureObjectType):
    '''The EmfPlusPalette object specifies the colors that make up a palette.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def palette_style_flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPaletteStyleFlags:
        '''Gets the palette style flags.'''
        raise NotImplementedError()
    
    @palette_style_flags.setter
    def palette_style_flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPaletteStyleFlags) -> None:
        '''Sets the palette style flags.'''
        raise NotImplementedError()
    
    @property
    def argb_32_entries(self) -> List[int]:
        '''Gets the palette entries.'''
        raise NotImplementedError()
    
    @argb_32_entries.setter
    def argb_32_entries(self, value : List[int]) -> None:
        '''Sets the palette entries.'''
        raise NotImplementedError()
    

class EmfPlusPath(EmfPlusGraphicsObjectType):
    '''The EmfPlusPath object specifies a series of line and curve segments that form a graphics path. The
    order for Bezier data points is the start point, control point 1, control point 2, and end point.For
    more information see[MSDN - DrawBeziers].'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def path_point_flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPathPointFlags:
        '''Gets Path points count
        A 32-bit unsigned integer that specifies how to interpret the points and associated point types that are defined by this object'''
        raise NotImplementedError()
    
    @path_point_flags.setter
    def path_point_flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPathPointFlags) -> None:
        '''Sets Path points count
        A 32-bit unsigned integer that specifies how to interpret the points and associated point types that are defined by this object'''
        raise NotImplementedError()
    
    @property
    def path_points(self) -> List[aspose.imaging.PointF]:
        '''Gets array of path points
        An array of PathPointCount points that specify the path. The type of objects in this array are specified by the PathPointFlags field, as follows:
        If the P flag is set, the points are relative locations that are specified by EmfPlusPointR objects (section 2.2.2.37).
        If the P flag is clear and the C flag is set, the points are absolute locations that are specified by EmfPlusPoint objects (section 2.2.2.35).
        If the P flag is clear and the C flag is clear, the points are absolute locations that are specified by EmfPlusPointF objects (section 2.2.2.36).'''
        raise NotImplementedError()
    
    @path_points.setter
    def path_points(self, value : List[aspose.imaging.PointF]) -> None:
        '''Sets array of path points
        An array of PathPointCount points that specify the path. The type of objects in this array are specified by the PathPointFlags field, as follows:
        If the P flag is set, the points are relative locations that are specified by EmfPlusPointR objects (section 2.2.2.37).
        If the P flag is clear and the C flag is set, the points are absolute locations that are specified by EmfPlusPoint objects (section 2.2.2.35).
        If the P flag is clear and the C flag is clear, the points are absolute locations that are specified by EmfPlusPointF objects (section 2.2.2.36).'''
        raise NotImplementedError()
    
    @property
    def path_point_types(self) -> List[aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBasePointType]:
        '''Gets an array that specifies how the points in the PathPoints field are used to draw the path.
        The type of objects in this array is specified by the R flag in the PathPointFlags field'''
        raise NotImplementedError()
    
    @path_point_types.setter
    def path_point_types(self, value : List[aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBasePointType]) -> None:
        '''Sets an array that specifies how the points in the PathPoints field are used to draw the path.
        The type of objects in this array is specified by the R flag in the PathPointFlags field'''
        raise NotImplementedError()
    

class EmfPlusPathGradientBrushData(EmfPlusBaseBrushData):
    '''The EmfPlusPathGradientBrushData object specifies a path gradient for a graphics brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def brush_data_flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBrushDataFlags:
        '''Gets 32-bit unsigned integer that specifies the data in the OptionalData field.
        This value MUST be composed of BrushData flags (section 2.1.2.1). The following flags are relevant to a path gradient brush:'''
        raise NotImplementedError()
    
    @brush_data_flags.setter
    def brush_data_flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBrushDataFlags) -> None:
        '''Sets 32-bit unsigned integer that specifies the data in the OptionalData field.
        This value MUST be composed of BrushData flags (section 2.1.2.1). The following flags are relevant to a path gradient brush:'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusWrapMode:
        '''Gets 32-bit signed integer from the WrapMode enumeration (section 2.1.1.34) that specifies
        whether to paint the area outside the boundary of the brush. When painting
        outside the boundary, the wrap mode specifies how the color gradient is repeated'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusWrapMode) -> None:
        '''Sets 32-bit signed integer from the WrapMode enumeration (section 2.1.1.34) that specifies
        whether to paint the area outside the boundary of the brush. When painting
        outside the boundary, the wrap mode specifies how the color gradient is repeated'''
        raise NotImplementedError()
    
    @property
    def center_argb_32_color(self) -> int:
        '''Gets EmfPlusARGB object (section 2.2.2.1) that specifies the center color of
        the path gradient brush, which is the color that appears at the center point of the brush.
        The color of the brush changes gradually from the boundary
        color to the center color as it moves from the boundary to the center point.'''
        raise NotImplementedError()
    
    @center_argb_32_color.setter
    def center_argb_32_color(self, value : int) -> None:
        '''Sets EmfPlusARGB object (section 2.2.2.1) that specifies the center color of
        the path gradient brush, which is the color that appears at the center point of the brush.
        The color of the brush changes gradually from the boundary
        color to the center color as it moves from the boundary to the center point.'''
        raise NotImplementedError()
    
    @property
    def center_point_f(self) -> aspose.imaging.PointF:
        '''Gets EmfPlusARGB object (section 2.2.2.1) that specifies the center color of the path gradient brush,
        which is the color that appears at the center point of the brush. The color of the
        brush changes gradually from the boundary color to the center color as it moves
        from the boundary to the center point.'''
        raise NotImplementedError()
    
    @center_point_f.setter
    def center_point_f(self, value : aspose.imaging.PointF) -> None:
        '''Sets EmfPlusARGB object (section 2.2.2.1) that specifies the center color of the path gradient brush,
        which is the color that appears at the center point of the brush. The color of the
        brush changes gradually from the boundary color to the center color as it moves
        from the boundary to the center point.'''
        raise NotImplementedError()
    
    @property
    def surrounding_argb_32_colors(self) -> List[int]:
        '''Gets array of SurroundingColorCount EmfPlusARGB objects
        that specify the colors for discrete points on the boundary of the brush.'''
        raise NotImplementedError()
    
    @surrounding_argb_32_colors.setter
    def surrounding_argb_32_colors(self, value : List[int]) -> None:
        '''Sets array of SurroundingColorCount EmfPlusARGB objects
        that specify the colors for discrete points on the boundary of the brush.'''
        raise NotImplementedError()
    
    @property
    def boundary_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBoundaryBase:
        '''Gets the boundary of the path gradient brush, which is specified by either a path or a closed cardinal spline.
        If the BrushDataPath flag is set in the BrushDataFlags field, this field MUST contain an EmfPlusBoundaryPathData object (section 2.2.2.6);
        otherwise, this field MUST contain an EmfPlusBoundaryPointData object (section 2.2.2.7).'''
        raise NotImplementedError()
    
    @boundary_data.setter
    def boundary_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBoundaryBase) -> None:
        '''Sets the boundary of the path gradient brush, which is specified by either a path or a closed cardinal spline.
        If the BrushDataPath flag is set in the BrushDataFlags field, this field MUST contain an EmfPlusBoundaryPathData object (section 2.2.2.6);
        otherwise, this field MUST contain an EmfPlusBoundaryPointData object (section 2.2.2.7).'''
        raise NotImplementedError()
    
    @property
    def optional_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPathGradientBrushOptionalData:
        '''Gets an optional EmfPlusPathGradientBrushOptionalData object (section 2.2.2.30) that
        specifies additional data for the path gradient brush.
        The specific contents of this field are determined by the value of the BrushDataFlags field.'''
        raise NotImplementedError()
    
    @optional_data.setter
    def optional_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPathGradientBrushOptionalData) -> None:
        '''Sets an optional EmfPlusPathGradientBrushOptionalData object (section 2.2.2.30) that
        specifies additional data for the path gradient brush.
        The specific contents of this field are determined by the value of the BrushDataFlags field.'''
        raise NotImplementedError()
    

class EmfPlusPathGradientBrushOptionalData(EmfPlusStructureObjectType):
    '''The EmfPlusPathGradientBrushOptionalData object specifies optional data for a path gradient brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def transform_matrix(self) -> aspose.imaging.Matrix:
        '''Gets an optional EmfPlusTransformMatrix object (section 2.2.2.47) that specifies a world space to device space transform for the path gradient brush.
        This field MUST be present if the BrushDataTransform flag is set in the BrushDataFlags field of the EmfPlusPathGradientBrushData object.'''
        raise NotImplementedError()
    
    @transform_matrix.setter
    def transform_matrix(self, value : aspose.imaging.Matrix) -> None:
        '''Sets an optional EmfPlusTransformMatrix object (section 2.2.2.47) that specifies a world space to device space transform for the path gradient brush.
        This field MUST be present if the BrushDataTransform flag is set in the BrushDataFlags field of the EmfPlusPathGradientBrushData object.'''
        raise NotImplementedError()
    
    @property
    def blend_pattern(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBlendBase:
        '''Gets an optional blend pattern for the path gradient brush. If this field is
        present, it MUST contain either an EmfPlusBlendColors object (section 2.2.2.4),
        or an EmfPlusBlendFactors object (section 2.2.2.5), but it MUST NOT contain both.
        The table below shows the valid combinations of EmfPlusPathGradientBrushData
        BrushData flags and the corresponding blend patterns:'''
        raise NotImplementedError()
    
    @blend_pattern.setter
    def blend_pattern(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBlendBase) -> None:
        '''Sets an optional blend pattern for the path gradient brush. If this field is
        present, it MUST contain either an EmfPlusBlendColors object (section 2.2.2.4),
        or an EmfPlusBlendFactors object (section 2.2.2.5), but it MUST NOT contain both.
        The table below shows the valid combinations of EmfPlusPathGradientBrushData
        BrushData flags and the corresponding blend patterns:'''
        raise NotImplementedError()
    
    @property
    def focus_scale_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusFocusScaleData:
        '''Gets an optional EmfPlusFocusScaleData object (section 2.2.2.18) that specifies
        focus scales for the path gradient brush. This field MUST be present if the
        BrushDataFocusScales flag is set in the BrushDataFlags field of the
        EmfPlusPathGradientBrushData object.'''
        raise NotImplementedError()
    
    @focus_scale_data.setter
    def focus_scale_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusFocusScaleData) -> None:
        '''Sets an optional EmfPlusFocusScaleData object (section 2.2.2.18) that specifies
        focus scales for the path gradient brush. This field MUST be present if the
        BrushDataFocusScales flag is set in the BrushDataFlags field of the
        EmfPlusPathGradientBrushData object.'''
        raise NotImplementedError()
    

class EmfPlusPathPointType(EmfPlusBasePointType):
    '''The EmfPlusPathPointType object specifies a type value associated with a point on a graphics'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def data(self) -> int:
        '''Gets the data.'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : int) -> None:
        '''Sets the data.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPathPointTypeEnum:
        '''Gets 4-bit unsigned integer path point type. This value MUST be
        defined in the PathPointType enumeration (section 2.1.1.23).'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPathPointTypeEnum) -> None:
        '''Sets 4-bit unsigned integer path point type. This value MUST be
        defined in the PathPointType enumeration (section 2.1.1.23).'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPathPointTypeFlags:
        '''Gets 4-bit flag field that specifies properties of the path point.
        This value MUST be one or more of the PathPointType flags (section 2.1.2.6).'''
        raise NotImplementedError()
    
    @flags.setter
    def flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPathPointTypeFlags) -> None:
        '''Sets 4-bit flag field that specifies properties of the path point.
        This value MUST be one or more of the PathPointType flags (section 2.1.2.6).'''
        raise NotImplementedError()
    

class EmfPlusPathPointTypeRle(EmfPlusBasePointType):
    '''The EmfPlusPathPointTypeRle object specifies type values associated with points on a graphics path using RLE compression.
    0 1 2 3 4 5 6 7 8 9 1 0 1 2 3 4 5 6 7 8 9 2 0 1 2 3 4 5 6 7 8 9 3 0 1
    B|1|RunCount   | PointType       |
    B (1 bit): If set, the path points are on a Bezier curve.
    If clear, the path points are on a graphics line.
    RunCount (6 bits): The run count, which is the number of path points to be associated with the type in the PointType field.
    PointType (1 byte): An EmfPlusPathPointType object (section 2.2.2.31) that specifies the type to associate with the path points.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def data(self) -> int:
        '''Gets the data.'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : int) -> None:
        '''Sets the data.'''
        raise NotImplementedError()
    
    @property
    def bezier(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPathPointTypeRle` is bezier.
        If set, the path points are on a Bezier curve.
        If clear, the path points are on a graphics line.'''
        raise NotImplementedError()
    
    @bezier.setter
    def bezier(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPathPointTypeRle` is bezier.
        If set, the path points are on a Bezier curve.
        If clear, the path points are on a graphics line.'''
        raise NotImplementedError()
    
    @property
    def run_count(self) -> int:
        '''Gets the run count.
        RunCount (6 bits): The run count, which is the number of path
        points to be associated with the type in the PointType field'''
        raise NotImplementedError()
    
    @run_count.setter
    def run_count(self, value : int) -> None:
        '''Sets the run count.
        RunCount (6 bits): The run count, which is the number of path
        points to be associated with the type in the PointType field'''
        raise NotImplementedError()
    
    @property
    def point_type(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPathPointType:
        '''Gets the type of the point.
        PointType (1 byte): An EmfPlusPathPointType object
        (section 2.2.2.31) that specifies the type to associate with the path points.'''
        raise NotImplementedError()
    
    @point_type.setter
    def point_type(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPathPointType) -> None:
        '''Sets the type of the point.
        PointType (1 byte): An EmfPlusPathPointType object
        (section 2.2.2.31) that specifies the type to associate with the path points.'''
        raise NotImplementedError()
    

class EmfPlusPen(EmfPlusGraphicsObjectType):
    '''The EmfPlusPen object specifies a graphics pen for the drawing of lines.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> int:
        '''Gets This field MUST be set to zero'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : int) -> None:
        '''Sets This field MUST be set to zero'''
        raise NotImplementedError()
    
    @property
    def pen_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData:
        '''Gets an EmfPlusPenData object that specifies properties of the graphics pen'''
        raise NotImplementedError()
    
    @pen_data.setter
    def pen_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData) -> None:
        '''Sets an EmfPlusPenData object that specifies properties of the graphics pen'''
        raise NotImplementedError()
    
    @property
    def brush_object(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBrush:
        '''Gets an EmfPlusBrush object that specifies a graphics brush associated with the pen'''
        raise NotImplementedError()
    
    @brush_object.setter
    def brush_object(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBrush) -> None:
        '''Sets an EmfPlusBrush object that specifies a graphics brush associated with the pen'''
        raise NotImplementedError()
    

class EmfPlusPenData(EmfPlusStructureObjectType):
    '''The EmfPlusPenData object specifies properties of a graphics pen.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def pen_data_flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPenDataFlags:
        '''Gets 32-bit unsigned integer that specifies the data in the
        OptionalData field. This value MUST be composed of PenData
        flags (section 2.1.2.7).'''
        raise NotImplementedError()
    
    @pen_data_flags.setter
    def pen_data_flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPenDataFlags) -> None:
        '''Sets 32-bit unsigned integer that specifies the data in the
        OptionalData field. This value MUST be composed of PenData
        flags (section 2.1.2.7).'''
        raise NotImplementedError()
    
    @property
    def pen_unit(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusUnitType:
        '''Gets 32-bit unsigned integer that specifies the measuring units
        for the pen. The value MUST be from the UnitType enumeration
        (section 2.1.1.33).'''
        raise NotImplementedError()
    
    @pen_unit.setter
    def pen_unit(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusUnitType) -> None:
        '''Sets 32-bit unsigned integer that specifies the measuring units
        for the pen. The value MUST be from the UnitType enumeration
        (section 2.1.1.33).'''
        raise NotImplementedError()
    
    @property
    def pen_width(self) -> float:
        '''Gets 32-bit floating-point value that specifies the width of the
        line drawn by the pen in the units specified by the PenUnit
        field. If a zero width is specified, a minimum value is used,
        which is determined by the units'''
        raise NotImplementedError()
    
    @pen_width.setter
    def pen_width(self, value : float) -> None:
        '''Sets 32-bit floating-point value that specifies the width of the
        line drawn by the pen in the units specified by the PenUnit
        field. If a zero width is specified, a minimum value is used,
        which is determined by the units'''
        raise NotImplementedError()
    
    @property
    def optional_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenOptionalData:
        '''Gets optional EmfPlusPenOptionalData object (section 2.2.2.34)
        that specifies additional data for the pen object. The specific
        contents of this field are determined by the value of the
        PenDataFlags field.'''
        raise NotImplementedError()
    
    @optional_data.setter
    def optional_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenOptionalData) -> None:
        '''Sets optional EmfPlusPenOptionalData object (section 2.2.2.34)
        that specifies additional data for the pen object. The specific
        contents of this field are determined by the value of the
        PenDataFlags field.'''
        raise NotImplementedError()
    

class EmfPlusPenOptionalData(EmfPlusStructureObjectType):
    '''The EmfPlusPenOptionalData object specifies optional data for a graphics pen'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def transform_matrix(self) -> aspose.imaging.Matrix:
        '''Gets an optional EmfPlusTransformMatrix object (section 2.2.2.47)
        that specifies a world space to device space transform for
        the pen. This field MUST be present if the PenDataTransform
        flag is set in the PenDataFlags field of the EmfPlusPenData
        object.'''
        raise NotImplementedError()
    
    @transform_matrix.setter
    def transform_matrix(self, value : aspose.imaging.Matrix) -> None:
        '''Sets an optional EmfPlusTransformMatrix object (section 2.2.2.47)
        that specifies a world space to device space transform for
        the pen. This field MUST be present if the PenDataTransform
        flag is set in the PenDataFlags field of the EmfPlusPenData
        object.'''
        raise NotImplementedError()
    
    @property
    def start_cap(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType:
        '''Gets an optional 32-bit signed integer that specifies the shape for
        the start of a line in the CustomStartCapData field.
        This field MUST be present if the PenDataStartCap flag is set
        in the PenDataFlags field of the EmfPlusPenData object, and the
        value MUST be defined in the LineCapType enumeration
        (section 2.1.1.18).'''
        raise NotImplementedError()
    
    @start_cap.setter
    def start_cap(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType) -> None:
        '''Sets an optional 32-bit signed integer that specifies the shape for
        the start of a line in the CustomStartCapData field.
        This field MUST be present if the PenDataStartCap flag is set
        in the PenDataFlags field of the EmfPlusPenData object, and the
        value MUST be defined in the LineCapType enumeration
        (section 2.1.1.18).'''
        raise NotImplementedError()
    
    @property
    def end_cap(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType:
        '''Gets optional 32-bit signed integer that specifies the shape
        for the end of a line in the CustomEndCapData field. This
        field MUST be present if the PenDataEndCap flag is set in the
        PenDataFlags field of the EmfPlusPenData object, and the value
        MUST be defined in the LineCapType enumeration'''
        raise NotImplementedError()
    
    @end_cap.setter
    def end_cap(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineCapType) -> None:
        '''Sets optional 32-bit signed integer that specifies the shape
        for the end of a line in the CustomEndCapData field. This
        field MUST be present if the PenDataEndCap flag is set in the
        PenDataFlags field of the EmfPlusPenData object, and the value
        MUST be defined in the LineCapType enumeration'''
        raise NotImplementedError()
    
    @property
    def join(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineJoinType:
        '''Gets an optional 32-bit signed integer that specifies how to join
        two lines that are drawn by the same pen and whose ends meet.
        This field MUST be present if the PenDataJoin flag is set in
        the PenDataFlags field of the EmfPlusPenData object, and the
        value MUST be defined in the LineJoinType enumeration
        (section 2.1.1.19).'''
        raise NotImplementedError()
    
    @join.setter
    def join(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineJoinType) -> None:
        '''Sets an optional 32-bit signed integer that specifies how to join
        two lines that are drawn by the same pen and whose ends meet.
        This field MUST be present if the PenDataJoin flag is set in
        the PenDataFlags field of the EmfPlusPenData object, and the
        value MUST be defined in the LineJoinType enumeration
        (section 2.1.1.19).'''
        raise NotImplementedError()
    
    @property
    def miter_limit(self) -> float:
        '''Gets optional 32-bit floating-point value that specifies the miter
        limit, which is the maximum allowed ratio of miter length to
        line width. The miter length is the distance from the
        intersection of the line walls on the inside the join to
        the intersection of the line walls outside the join.
        The miter length can be large when the angle between two
        lines is small. This field MUST be present if the
        PenDataMiterLimit flag is set in the PenDataFlags field
        of the EmfPlusPenData object.'''
        raise NotImplementedError()
    
    @miter_limit.setter
    def miter_limit(self, value : float) -> None:
        '''Sets optional 32-bit floating-point value that specifies the miter
        limit, which is the maximum allowed ratio of miter length to
        line width. The miter length is the distance from the
        intersection of the line walls on the inside the join to
        the intersection of the line walls outside the join.
        The miter length can be large when the angle between two
        lines is small. This field MUST be present if the
        PenDataMiterLimit flag is set in the PenDataFlags field
        of the EmfPlusPenData object.'''
        raise NotImplementedError()
    
    @property
    def line_style(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineStyle:
        '''Gets optional 32-bit signed integer that specifies the style
        used for lines drawn with this pen object. This field MUST
        be present if the PenDataLineStyle flag is set in the
        PenDataFlags field of the EmfPlusPenData object, and the
        value MUST be defined in the LineStyle enumeration
        (section 2.1.1.20).'''
        raise NotImplementedError()
    
    @line_style.setter
    def line_style(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLineStyle) -> None:
        '''Sets optional 32-bit signed integer that specifies the style
        used for lines drawn with this pen object. This field MUST
        be present if the PenDataLineStyle flag is set in the
        PenDataFlags field of the EmfPlusPenData object, and the
        value MUST be defined in the LineStyle enumeration
        (section 2.1.1.20).'''
        raise NotImplementedError()
    
    @property
    def dashed_line_cap_type(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusDashedLineCapType:
        '''Gets optional 32-bit signed integer that specifies the shape for
        both ends of each dash in a dashed line. This field MUST be
        present if the PenDataDashedLineCap flag is set in the
        PenDataFlags field of the EmfPlusPenData object, and the
        value MUST be defined in the DashedLineCapType enumeration
        (section 2.1.1.10).'''
        raise NotImplementedError()
    
    @dashed_line_cap_type.setter
    def dashed_line_cap_type(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusDashedLineCapType) -> None:
        '''Sets optional 32-bit signed integer that specifies the shape for
        both ends of each dash in a dashed line. This field MUST be
        present if the PenDataDashedLineCap flag is set in the
        PenDataFlags field of the EmfPlusPenData object, and the
        value MUST be defined in the DashedLineCapType enumeration
        (section 2.1.1.10).'''
        raise NotImplementedError()
    
    @property
    def dash_offset(self) -> float:
        '''Gets optional 32-bit floating-point value that specifies the
        distance from the start of a line to the start of the
        first space in a dashed line pattern. This field MUST be
        present if the PenDataDashedLineOffset flag is set in the
        PenDataFlags field of the EmfPlusPenData object.'''
        raise NotImplementedError()
    
    @dash_offset.setter
    def dash_offset(self, value : float) -> None:
        '''Sets optional 32-bit floating-point value that specifies the
        distance from the start of a line to the start of the
        first space in a dashed line pattern. This field MUST be
        present if the PenDataDashedLineOffset flag is set in the
        PenDataFlags field of the EmfPlusPenData object.'''
        raise NotImplementedError()
    
    @property
    def dashed_line_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusDashedLineData:
        '''Gets optional EmfPlusDashedLineData object (section 2.2.2.16)
        that specifies the lengths of dashes and spaces in a custom
        dashed line. This field MUST be present if the PenDataDashedLine
        flag is set in the PenDataFlags field of the EmfPlusPenData
        object.'''
        raise NotImplementedError()
    
    @dashed_line_data.setter
    def dashed_line_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusDashedLineData) -> None:
        '''Sets optional EmfPlusDashedLineData object (section 2.2.2.16)
        that specifies the lengths of dashes and spaces in a custom
        dashed line. This field MUST be present if the PenDataDashedLine
        flag is set in the PenDataFlags field of the EmfPlusPenData
        object.'''
        raise NotImplementedError()
    
    @property
    def pen_alignment(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPenAlignment:
        '''Gets optional 32-bit signed integer that specifies the
        distribution of the pen width with respect to the
        coordinates of the line being drawn. This field MUST
        be present if the PenDataNonCenter flag is set in the
        PenDataFlags field of the EmfPlusPenData object, and
        the value MUST be defined in the PenAlignment
        enumeration (section 2.1.1.24).'''
        raise NotImplementedError()
    
    @pen_alignment.setter
    def pen_alignment(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusPenAlignment) -> None:
        '''Sets optional 32-bit signed integer that specifies the
        distribution of the pen width with respect to the
        coordinates of the line being drawn. This field MUST
        be present if the PenDataNonCenter flag is set in the
        PenDataFlags field of the EmfPlusPenData object, and
        the value MUST be defined in the PenAlignment
        enumeration (section 2.1.1.24).'''
        raise NotImplementedError()
    
    @property
    def compound_line_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCompoundLineData:
        '''Gets optional EmfPlusCompoundLineData object (section 2.2.2.9)
        that specifies an array of floating-point values that define
        the compound line of a pen, which is made up of parallel lines
        and spaces. This field MUST be present if the
        PenDataCompoundLine flag is set in the PenDataFlags field
        of the EmfPlusPenData object'''
        raise NotImplementedError()
    
    @compound_line_data.setter
    def compound_line_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCompoundLineData) -> None:
        '''Sets optional EmfPlusCompoundLineData object (section 2.2.2.9)
        that specifies an array of floating-point values that define
        the compound line of a pen, which is made up of parallel lines
        and spaces. This field MUST be present if the
        PenDataCompoundLine flag is set in the PenDataFlags field
        of the EmfPlusPenData object'''
        raise NotImplementedError()
    
    @property
    def custom_start_cap_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomStartCapData:
        '''Gets optional EmfPlusCustomStartCapData object (section 2.2.2.15)
        that defines the custom start-cap shape, which is the shape to
        use at the start of a line drawn with this pen. It can be any
        of various shapes, such as a square, circle, or diamond.
        This field MUST be present if the PenDataCustomStartCap flag
        is set in the PenDataFlags field of the EmfPlusPenData object'''
        raise NotImplementedError()
    
    @custom_start_cap_data.setter
    def custom_start_cap_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomStartCapData) -> None:
        '''Sets optional EmfPlusCustomStartCapData object (section 2.2.2.15)
        that defines the custom start-cap shape, which is the shape to
        use at the start of a line drawn with this pen. It can be any
        of various shapes, such as a square, circle, or diamond.
        This field MUST be present if the PenDataCustomStartCap flag
        is set in the PenDataFlags field of the EmfPlusPenData object'''
        raise NotImplementedError()
    
    @property
    def custom_end_cap_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomEndCapData:
        '''Gets optional EmfPlusCustomEndCapData object (section 2.2.2.11)
        that defines the custom end-cap shape, which is the shape to
        use at the end of a line drawn with this pen. It can be any of
        various shapes, such as a square, circle, or diamond. This
        field MUST be present if the PenDataCustomEndCap flag is
        set in the PenDataFlags field of the EmfPlusPenData object'''
        raise NotImplementedError()
    
    @custom_end_cap_data.setter
    def custom_end_cap_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomEndCapData) -> None:
        '''Sets optional EmfPlusCustomEndCapData object (section 2.2.2.11)
        that defines the custom end-cap shape, which is the shape to
        use at the end of a line drawn with this pen. It can be any of
        various shapes, such as a square, circle, or diamond. This
        field MUST be present if the PenDataCustomEndCap flag is
        set in the PenDataFlags field of the EmfPlusPenData object'''
        raise NotImplementedError()
    

class EmfPlusRectF(EmfPlusStructureObjectType):
    '''The EmfPlusRectF object specifies a rectangle\'s origin, height, and width as 32-bit floating-point values.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def rect(self) -> aspose.imaging.RectangleF:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rect.setter
    def rect(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class EmfPlusRedEyeCorrectionEffect(EmfPlusImageEffectsObjectType):
    '''The RedEyeCorrectionEffect object specifies areas of an image to which a red-eye correction is applied.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def number_of_areas(self) -> int:
        '''Gets the A 32-bit signed integer that specifies the number of rectangles in
        the Areas field.'''
        raise NotImplementedError()
    
    @number_of_areas.setter
    def number_of_areas(self, value : int) -> None:
        '''Sets the A 32-bit signed integer that specifies the number of rectangles in
        the Areas field.'''
        raise NotImplementedError()
    
    @property
    def areas(self) -> List[aspose.imaging.Rectangle]:
        '''Gets the An array of NumberOfAreas WMF RectL objects, specified in [MS-WMF]
        section 2.2.2.19. Each rectangle specifies an area of the bitmap image to which the red-eye
        correction effect SHOULD be applied.'''
        raise NotImplementedError()
    
    @areas.setter
    def areas(self, value : List[aspose.imaging.Rectangle]) -> None:
        '''Sets the An array of NumberOfAreas WMF RectL objects, specified in [MS-WMF]
        section 2.2.2.19. Each rectangle specifies an area of the bitmap image to which the red-eye
        correction effect SHOULD be applied.'''
        raise NotImplementedError()
    

class EmfPlusRegion(EmfPlusGraphicsObjectType):
    '''The EmfPlusRegion object specifies line and curve segments that define a non rectilinear shape'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def region_node(self) -> List[aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNode]:
        '''Gets an array of RegionNodeCount+1 EmfPlusRegionNode objects
        (section 2.2.2.40). Regions are specified as a binary tree
        of region nodes, and each node MUST either be a terminal
        node or specify one or two child nodes.
        RegionNode MUST contain at least one element'''
        raise NotImplementedError()
    
    @region_node.setter
    def region_node(self, value : List[aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNode]) -> None:
        '''Sets an array of RegionNodeCount+1 EmfPlusRegionNode objects
        (section 2.2.2.40). Regions are specified as a binary tree
        of region nodes, and each node MUST either be a terminal
        node or specify one or two child nodes.
        RegionNode MUST contain at least one element'''
        raise NotImplementedError()
    

class EmfPlusRegionNode(EmfPlusStructureObjectType):
    '''The EmfPlusRegionNode object specifies nodes of a graphics region.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def region_node_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusStructureObjectType:
        '''Gets an optional, variable-length data that defines the region node
        data object specified in the Type field. The content and
        format of the data can be different for every region
        node type. This field MUST NOT be present if the node
        type is RegionNodeDataTypeEmpty or RegionNodeDataTypeInfinite
        This object is generic and is used to specify different types of region node data, including:
        An EmfPlusRegionNodePath object (section 2.2.2.42), for a terminal node;
        An EmfPlusRectF object (section 2.2.2.39), for a terminal node; and
        An EmfPlusRegionNodeChildNodes object (section 2.2.2.41), for a non-terminal node.'''
        raise NotImplementedError()
    
    @region_node_data.setter
    def region_node_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusStructureObjectType) -> None:
        '''Sets an optional, variable-length data that defines the region node
        data object specified in the Type field. The content and
        format of the data can be different for every region
        node type. This field MUST NOT be present if the node
        type is RegionNodeDataTypeEmpty or RegionNodeDataTypeInfinite
        This object is generic and is used to specify different types of region node data, including:
        An EmfPlusRegionNodePath object (section 2.2.2.42), for a terminal node;
        An EmfPlusRectF object (section 2.2.2.39), for a terminal node; and
        An EmfPlusRegionNodeChildNodes object (section 2.2.2.41), for a non-terminal node.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusRegionNodeDataType:
        '''Gets 32-bit unsigned integer that specifies the type of
        data in the RegionNodeData field. This value MUST be defined in the
        RegionNodeDataType enumeration (section 2.1.1.27).'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusRegionNodeDataType) -> None:
        '''Sets 32-bit unsigned integer that specifies the type of
        data in the RegionNodeData field. This value MUST be defined in the
        RegionNodeDataType enumeration (section 2.1.1.27).'''
        raise NotImplementedError()
    

class EmfPlusRegionNodeChildNodes(EmfPlusStructureObjectType):
    '''The EmfPlusRegionNodeChildNodes object specifies child nodes of a graphics region node'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def operation(self) -> Aspose.Imaging.FileFormats.Emf.EmfPlus.Objects.EmfPlusRegionNodeChildNodes+NodesOperation:
        '''Gets the operation.'''
        raise NotImplementedError()
    
    @operation.setter
    def operation(self, value : Aspose.Imaging.FileFormats.Emf.EmfPlus.Objects.EmfPlusRegionNodeChildNodes+NodesOperation) -> None:
        '''Sets the operation.'''
        raise NotImplementedError()
    
    @property
    def left(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNode:
        '''Gets an EmfPlusRegionNode object that specifies the left child node of this region node.'''
        raise NotImplementedError()
    
    @left.setter
    def left(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNode) -> None:
        '''Sets an EmfPlusRegionNode object that specifies the left child node of this region node.'''
        raise NotImplementedError()
    
    @property
    def right(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNode:
        '''Gets an EmfPlusRegionNode object that defines the right child node of this region node.'''
        raise NotImplementedError()
    
    @right.setter
    def right(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNode) -> None:
        '''Sets an EmfPlusRegionNode object that defines the right child node of this region node.'''
        raise NotImplementedError()
    

class EmfPlusRegionNodePath(EmfPlusStructureObjectType):
    '''The EmfPlusRegionNodePath object specifies a graphics path for drawing the boundary of a region node.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def region_node_path(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath:
        '''Gets an EmfPlusPath object (section 2.2.1.6) that specifies
        the boundary of the region node.'''
        raise NotImplementedError()
    
    @region_node_path.setter
    def region_node_path(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath) -> None:
        '''Sets an EmfPlusPath object (section 2.2.1.6) that specifies
        the boundary of the region node.'''
        raise NotImplementedError()
    

class EmfPlusSharpenEffect(EmfPlusImageEffectsObjectType):
    '''The SharpenEffect object specifies an increase in the difference in intensity between pixels in an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def radius(self) -> float:
        '''Gets A 32-bit floating-point number that specifies the sharpening radius in pixels,
        which determines the number of pixels involved in calculating the new value of a given pixel.
        As this value increases, the number of pixels involved in the calculation increases, and the
        resulting bitmap SHOULD become sharper.'''
        raise NotImplementedError()
    
    @radius.setter
    def radius(self, value : float) -> None:
        '''Sets A 32-bit floating-point number that specifies the sharpening radius in pixels,
        which determines the number of pixels involved in calculating the new value of a given pixel.
        As this value increases, the number of pixels involved in the calculation increases, and the
        resulting bitmap SHOULD become sharper.'''
        raise NotImplementedError()
    
    @property
    def amount(self) -> float:
        '''Gets A 32-bit floating-point number that specifies the difference in intensity
        between a given pixel and the surrounding pixels.
        0 Specifies that sharpening MUST NOT be performed.
        0 < value ≤ 100
        As this value increases, the difference in intensity between pixels SHOULD
        increase.'''
        raise NotImplementedError()
    
    @amount.setter
    def amount(self, value : float) -> None:
        '''Sets A 32-bit floating-point number that specifies the difference in intensity
        between a given pixel and the surrounding pixels.
        0 Specifies that sharpening MUST NOT be performed.
        0 < value ≤ 100
        As this value increases, the difference in intensity between pixels SHOULD
        increase.'''
        raise NotImplementedError()
    

class EmfPlusSolidBrushData(EmfPlusBaseBrushData):
    '''The EmfPlusSolidBrushData object specifies a solid color for a graphics brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def solid_argb_32_color(self) -> int:
        '''Gets an EmfPlusARGB object (section 2.2.2.1) that specifies the color of the brush.'''
        raise NotImplementedError()
    
    @solid_argb_32_color.setter
    def solid_argb_32_color(self, value : int) -> None:
        '''Sets an EmfPlusARGB object (section 2.2.2.1) that specifies the color of the brush.'''
        raise NotImplementedError()
    

class EmfPlusStringFormat(EmfPlusGraphicsObjectType):
    '''The EmfPlusStringFormat object specifies text layout,
    display manipulations, and language identification'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusGraphicsVersion) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def digit_language(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLanguageIdentifierType:
        '''Gets an EmfPlusLanguageIdentifier object that specifies the
        language to use for numeric digits in the string.
        For example, if this string contains Arabic digits,
        this field MUST contain a language identifier that
        specifies an Arabic language'''
        raise NotImplementedError()
    
    @digit_language.setter
    def digit_language(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLanguageIdentifierType) -> None:
        '''Sets an EmfPlusLanguageIdentifier object that specifies the
        language to use for numeric digits in the string.
        For example, if this string contains Arabic digits,
        this field MUST contain a language identifier that
        specifies an Arabic language'''
        raise NotImplementedError()
    
    @property
    def digit_substitution(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringDigitSubstitution:
        '''Gets a 32-bit unsigned integer that specifies how to substitute
        numeric digits in the string according to a locale or language.
        This value MUST be defined in the StringDigitSubstitution
        enumeration (section 2.1.1.30).'''
        raise NotImplementedError()
    
    @digit_substitution.setter
    def digit_substitution(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringDigitSubstitution) -> None:
        '''Sets a 32-bit unsigned integer that specifies how to substitute
        numeric digits in the string according to a locale or language.
        This value MUST be defined in the StringDigitSubstitution
        enumeration (section 2.1.1.30).'''
        raise NotImplementedError()
    
    @property
    def first_tab_offset(self) -> float:
        '''Gets a 32-bit floating-point value that specifies the number
        of spaces between the beginning of a text line and
        the first tab stop'''
        raise NotImplementedError()
    
    @first_tab_offset.setter
    def first_tab_offset(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies the number
        of spaces between the beginning of a text line and
        the first tab stop'''
        raise NotImplementedError()
    
    @property
    def hotkey_prefix(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusHotkeyPrefix:
        '''Gets a 32-bit signed integer that specifies the type of
        processing that is performed on a string when a keyboard
        shortcut prefix (that is, an ampersand) is encountered.
        Basically, this field specifies whether to display
        keyboard shortcut prefixes that relate to text.
        The value MUST be defined in the HotkeyPrefix
        enumeration (section 2.1.1.14).'''
        raise NotImplementedError()
    
    @hotkey_prefix.setter
    def hotkey_prefix(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusHotkeyPrefix) -> None:
        '''Sets a 32-bit signed integer that specifies the type of
        processing that is performed on a string when a keyboard
        shortcut prefix (that is, an ampersand) is encountered.
        Basically, this field specifies whether to display
        keyboard shortcut prefixes that relate to text.
        The value MUST be defined in the HotkeyPrefix
        enumeration (section 2.1.1.14).'''
        raise NotImplementedError()
    
    @property
    def language(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLanguageIdentifierType:
        '''Gets an EmfPlusLanguageIdentifier object (section 2.2.2.23)
        that specifies the language to use for the string'''
        raise NotImplementedError()
    
    @language.setter
    def language(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusLanguageIdentifierType) -> None:
        '''Sets an EmfPlusLanguageIdentifier object (section 2.2.2.23)
        that specifies the language to use for the string'''
        raise NotImplementedError()
    
    @property
    def leading_margin(self) -> float:
        '''Gets a 32-bit floating-point value that specifies the length
        of the space to add to the starting position of a string.
        The default is 1/6 inch; for typographic fonts, the
        default value is 0.'''
        raise NotImplementedError()
    
    @leading_margin.setter
    def leading_margin(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies the length
        of the space to add to the starting position of a string.
        The default is 1/6 inch; for typographic fonts, the
        default value is 0.'''
        raise NotImplementedError()
    
    @property
    def line_align(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringAlignment:
        '''Gets a 32-bit unsigned integer that specifies how to
        align the string vertically in the layout rectangle.
        This value MUST be defined in the StringAlignment enumeration.'''
        raise NotImplementedError()
    
    @line_align.setter
    def line_align(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringAlignment) -> None:
        '''Sets a 32-bit unsigned integer that specifies how to
        align the string vertically in the layout rectangle.
        This value MUST be defined in the StringAlignment enumeration.'''
        raise NotImplementedError()
    
    @property
    def range_count(self) -> int:
        '''Gets a 32-bit signed integer that specifies the number of EmfPlusCharacterRange
        objects (section 2.2.2.8) defined in the StringFormatData field.'''
        raise NotImplementedError()
    
    @range_count.setter
    def range_count(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the number of EmfPlusCharacterRange
        objects (section 2.2.2.8) defined in the StringFormatData field.'''
        raise NotImplementedError()
    
    @property
    def string_alignment(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringAlignment:
        '''Gets a 32-bit unsigned integer that specifies how to
        align the string horizontally in the layout rectangle.
        This value MUST be defined in the StringAlignment
        enumeration (section 2.1.1.29).'''
        raise NotImplementedError()
    
    @string_alignment.setter
    def string_alignment(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringAlignment) -> None:
        '''Sets a 32-bit unsigned integer that specifies how to
        align the string horizontally in the layout rectangle.
        This value MUST be defined in the StringAlignment
        enumeration (section 2.1.1.29).'''
        raise NotImplementedError()
    
    @property
    def string_format_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusStringFormatData:
        '''Gets an EmfPlusStringFormatData object (section 2.2.2.44)
        that specifies optional text layout data.'''
        raise NotImplementedError()
    
    @string_format_data.setter
    def string_format_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusStringFormatData) -> None:
        '''Sets an EmfPlusStringFormatData object (section 2.2.2.44)
        that specifies optional text layout data.'''
        raise NotImplementedError()
    
    @property
    def string_format_flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringFormatFlags:
        '''Gets a 32-bit unsigned integer that specifies text layout
        options for formatting, clipping and font handling.
        This value MUST be composed of StringFormat flags
        (section 2.1.2.8).'''
        raise NotImplementedError()
    
    @string_format_flags.setter
    def string_format_flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringFormatFlags) -> None:
        '''Sets a 32-bit unsigned integer that specifies text layout
        options for formatting, clipping and font handling.
        This value MUST be composed of StringFormat flags
        (section 2.1.2.8).'''
        raise NotImplementedError()
    
    @property
    def tabstop_count(self) -> int:
        '''Gets a 32-bit signed integer that specifies the number of tab stops
        defined in the StringFormatData field.'''
        raise NotImplementedError()
    
    @tabstop_count.setter
    def tabstop_count(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the number of tab stops
        defined in the StringFormatData field.'''
        raise NotImplementedError()
    
    @property
    def tracking(self) -> float:
        '''Gets a 32-bit floating-point value that specifies the ratio
        of the horizontal space allotted to each character in
        a specified string to the font-defined width of the
        character. Large values for this property specify ample
        space between characters; values less than 1 can produce
        character overlap. The default is 1.03; for typographic
        fonts, the default value is 1.00.'''
        raise NotImplementedError()
    
    @tracking.setter
    def tracking(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies the ratio
        of the horizontal space allotted to each character in
        a specified string to the font-defined width of the
        character. Large values for this property specify ample
        space between characters; values less than 1 can produce
        character overlap. The default is 1.03; for typographic
        fonts, the default value is 1.00.'''
        raise NotImplementedError()
    
    @property
    def trailing_margin(self) -> float:
        '''Gets a 32-bit floating-point value that specifies the length
        of the space to leave following a string. The default
        is 1/6 inch; for typographic fonts, the default value is 0.'''
        raise NotImplementedError()
    
    @trailing_margin.setter
    def trailing_margin(self, value : float) -> None:
        '''Sets a 32-bit floating-point value that specifies the length
        of the space to leave following a string. The default
        is 1/6 inch; for typographic fonts, the default value is 0.'''
        raise NotImplementedError()
    
    @property
    def trimming(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringTrimming:
        '''Gets specifies how to trim characters from a string that is
        too large to fit into a layout rectangle. This value
        MUST be defined in the StringTrimming enumeration (section 2.1.1.31).'''
        raise NotImplementedError()
    
    @trimming.setter
    def trimming(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusStringTrimming) -> None:
        '''Sets specifies how to trim characters from a string that is
        too large to fit into a layout rectangle. This value
        MUST be defined in the StringTrimming enumeration (section 2.1.1.31).'''
        raise NotImplementedError()
    

class EmfPlusStringFormatData(EmfPlusStructureObjectType):
    '''The EmfPlusStringFormatData object specifies tab stops and character positions for a graphics string.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def tab_stops(self) -> List[float]:
        '''Gets an optional array of floating-point values that specify
        the optional tab stop locations for this object. Each tab
        stop value represents the number of spaces between tab
        stops or, for the first tab stop, the number of spaces
        between the beginning of a line of text and the first tab stop.
        This field MUST be present if the value of the TabStopCount
        field in the EmfPlusStringFormat object is greater than 0.'''
        raise NotImplementedError()
    
    @tab_stops.setter
    def tab_stops(self, value : List[float]) -> None:
        '''Sets an optional array of floating-point values that specify
        the optional tab stop locations for this object. Each tab
        stop value represents the number of spaces between tab
        stops or, for the first tab stop, the number of spaces
        between the beginning of a line of text and the first tab stop.
        This field MUST be present if the value of the TabStopCount
        field in the EmfPlusStringFormat object is greater than 0.'''
        raise NotImplementedError()
    
    @property
    def char_range(self) -> List[aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCharacterRange]:
        '''Gets an optional array of RangeCount EmfPlusCharacterRange
        objects that specify the range of character positions
        within a string of text. The bounding region is defined
        by the area of the display that is occupied by a group
        of characters specified by the character range.
        This field MUST be present if the value of the RangeCount
        field in the EmfPlusStringFormat object is greater than 0.'''
        raise NotImplementedError()
    
    @char_range.setter
    def char_range(self, value : List[aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCharacterRange]) -> None:
        '''Sets an optional array of RangeCount EmfPlusCharacterRange
        objects that specify the range of character positions
        within a string of text. The bounding region is defined
        by the area of the display that is occupied by a group
        of characters specified by the character range.
        This field MUST be present if the value of the RangeCount
        field in the EmfPlusStringFormat object is greater than 0.'''
        raise NotImplementedError()
    

class EmfPlusStructureObjectType(EmfPlusObject):
    '''The Structure Objects specify containers for data structures that are embedded in EMF+ metafile
    records.Structure objects, unlike graphics objects, are not explicitly created; they are components
    that make up more complex structures'''
    

class EmfPlusTextureBrushData(EmfPlusBaseBrushData):
    '''The EmfPlusTextureBrushData object specifies a texture image for a graphics brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def brush_data_flags(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBrushDataFlags:
        '''Gets a 32-bit unsigned integer that specifies the data in the OptionalData field.
        This value MUST be composed of BrushData flags (section 2.1.2.1).
        The following flags are relevant to a texture brush
        BrushDataTransform
        BrushDataIsGammaCorrected
        BrushDataDoNotTransform'''
        raise NotImplementedError()
    
    @brush_data_flags.setter
    def brush_data_flags(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusBrushDataFlags) -> None:
        '''Sets a 32-bit unsigned integer that specifies the data in the OptionalData field.
        This value MUST be composed of BrushData flags (section 2.1.2.1).
        The following flags are relevant to a texture brush
        BrushDataTransform
        BrushDataIsGammaCorrected
        BrushDataDoNotTransform'''
        raise NotImplementedError()
    
    @property
    def wrap_mode(self) -> aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusWrapMode:
        '''Gets a 32-bit signed integer from the WrapMode enumeration (section 2.1.1.34)
        that specifies how to repeat the texture image across a shape, when the
        image is smaller than the area being filled.'''
        raise NotImplementedError()
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusWrapMode) -> None:
        '''Sets a 32-bit signed integer from the WrapMode enumeration (section 2.1.1.34)
        that specifies how to repeat the texture image across a shape, when the
        image is smaller than the area being filled.'''
        raise NotImplementedError()
    
    @property
    def optional_data(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusTextureBrushOptionalData:
        '''Gets an optional EmfPlusTextureBrushOptionalData object (section 2.2.2.46) that
        specifies additional data for the texture brush. The specific contents of
        this field are determined by the value of the BrushDataFlags field'''
        raise NotImplementedError()
    
    @optional_data.setter
    def optional_data(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusTextureBrushOptionalData) -> None:
        '''Sets an optional EmfPlusTextureBrushOptionalData object (section 2.2.2.46) that
        specifies additional data for the texture brush. The specific contents of
        this field are determined by the value of the BrushDataFlags field'''
        raise NotImplementedError()
    

class EmfPlusTextureBrushOptionalData(EmfPlusStructureObjectType):
    '''he EmfPlusTextureBrushOptionalData object specifies optional data for a texture brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def transform_matrix(self) -> aspose.imaging.Matrix:
        '''Gets an optional EmfPlusTransformMatrix object (section 2.2.2.47)
        that specifies a world space to device space transform for the
        texture brush. This field MUST be present if the BrushDataTransform
        flag is set in the BrushDataFlags field of the EmfPlusTextureBrushData object.'''
        raise NotImplementedError()
    
    @transform_matrix.setter
    def transform_matrix(self, value : aspose.imaging.Matrix) -> None:
        '''Sets an optional EmfPlusTransformMatrix object (section 2.2.2.47)
        that specifies a world space to device space transform for the
        texture brush. This field MUST be present if the BrushDataTransform
        flag is set in the BrushDataFlags field of the EmfPlusTextureBrushData object.'''
        raise NotImplementedError()
    
    @property
    def image_object(self) -> aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusImage:
        '''Gets an optional EmfPlusImage object (section 2.2.1.4) that specifies the
        brush texture. This field MUST be present if the size of the
        EmfPlusObject record (section 2.3.5.1) that defines this texture
        brush is large enough to accommodate an EmfPlusImage object in
        addition to the required fields of the EmfPlusTextureBrushData object
        and optionally an EmfPlusTransformMatrix object.'''
        raise NotImplementedError()
    
    @image_object.setter
    def image_object(self, value : aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusImage) -> None:
        '''Sets an optional EmfPlusImage object (section 2.2.1.4) that specifies the
        brush texture. This field MUST be present if the size of the
        EmfPlusObject record (section 2.3.5.1) that defines this texture
        brush is large enough to accommodate an EmfPlusImage object in
        addition to the required fields of the EmfPlusTextureBrushData object
        and optionally an EmfPlusTransformMatrix object.'''
        raise NotImplementedError()
    

class EmfPlusTintEffect(EmfPlusImageEffectsObjectType):
    '''The TintEffect object specifies an addition of black or white to a specified hue in an image.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def hue(self) -> int:
        '''Gets a 32-bit signed integer that specifies the hue to which the tint effect is applied.
        -180 ≤ value < 0
        The color at a specified counter-clockwise rotation of the color wheel, starting
        from blue.
        0 A value of 0 specifies the color blue on the color wheel.
        0 < value ≤ 180
        The color at a specified clockwise rotation of the color wheel, starting from blue'''
        raise NotImplementedError()
    
    @hue.setter
    def hue(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the hue to which the tint effect is applied.
        -180 ≤ value < 0
        The color at a specified counter-clockwise rotation of the color wheel, starting
        from blue.
        0 A value of 0 specifies the color blue on the color wheel.
        0 < value ≤ 180
        The color at a specified clockwise rotation of the color wheel, starting from blue'''
        raise NotImplementedError()
    
    @property
    def amount(self) -> int:
        '''Gets A 32-bit signed integer that specifies how much the hue is strengthened or weakened.
        -100 ≤ value < 0
        Negative values specify how much the hue is weakened, which equates to the
        addition of black.
        0 A value of 0 specifies that the tint MUST NOT change.
        0 < value ≤ 100
        Positive values specify how much the hue is strengthened, which equates to the
        addition of white.'''
        raise NotImplementedError()
    
    @amount.setter
    def amount(self, value : int) -> None:
        '''Sets A 32-bit signed integer that specifies how much the hue is strengthened or weakened.
        -100 ≤ value < 0
        Negative values specify how much the hue is weakened, which equates to the
        addition of black.
        0 A value of 0 specifies that the tint MUST NOT change.
        0 < value ≤ 100
        Positive values specify how much the hue is strengthened, which equates to the
        addition of white.'''
        raise NotImplementedError()
    

