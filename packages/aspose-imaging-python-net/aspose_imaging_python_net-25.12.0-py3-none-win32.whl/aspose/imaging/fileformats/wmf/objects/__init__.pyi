"""The  contains types [MS-WMF]: Windows
                Metafile Format 2.2 WMF Objects"""
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

class WmfAnimatePalette(WmfObject):
    '''The META_ANIMATEPALETTE record redefines entries in the logical palette
    that is defined in the playback device context with the specified
    Palette object (section 2.2.1.3).'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def log_palette(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfLogPalette:
        '''Gets the log palette.'''
        raise NotImplementedError()
    
    @log_palette.setter
    def log_palette(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfLogPalette) -> None:
        '''Sets the log palette.'''
        raise NotImplementedError()
    
    @property
    def start(self) -> int:
        '''Gets the start.'''
        raise NotImplementedError()
    
    @start.setter
    def start(self, value : int) -> None:
        '''Sets the start.'''
        raise NotImplementedError()
    

class WmfArc(WmfRectangle):
    '''The META_ARC record draws an elliptical arc.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def end_arc(self) -> aspose.imaging.Point:
        '''Gets the end arc.'''
        raise NotImplementedError()
    
    @end_arc.setter
    def end_arc(self, value : aspose.imaging.Point) -> None:
        '''Sets the end arc.'''
        raise NotImplementedError()
    
    @property
    def start_arc(self) -> aspose.imaging.Point:
        '''Gets the start arc.'''
        raise NotImplementedError()
    
    @start_arc.setter
    def start_arc(self, value : aspose.imaging.Point) -> None:
        '''Sets the start arc.'''
        raise NotImplementedError()
    

class WmfBitBlt(WmfStretchBlt):
    '''The META_BITBLT record specifies the transfer of a block of pixels
    according to a raster operation. The destination of the transfer is the
    current output region in the playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def raster_operation(self) -> aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation:
        '''Gets the raster operation.'''
        raise NotImplementedError()
    
    @raster_operation.setter
    def raster_operation(self, value : aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation) -> None:
        '''Sets the raster operation.'''
        raise NotImplementedError()
    
    @property
    def src_height(self) -> int:
        '''Gets the height of the source.'''
        raise NotImplementedError()
    
    @src_height.setter
    def src_height(self, value : int) -> None:
        '''Sets the height of the source.'''
        raise NotImplementedError()
    
    @property
    def src_width(self) -> int:
        '''Gets the width of the source.'''
        raise NotImplementedError()
    
    @src_width.setter
    def src_width(self, value : int) -> None:
        '''Sets the width of the source.'''
        raise NotImplementedError()
    
    @property
    def src_position(self) -> aspose.imaging.Point:
        '''Gets the source position.'''
        raise NotImplementedError()
    
    @src_position.setter
    def src_position(self, value : aspose.imaging.Point) -> None:
        '''Sets the source position.'''
        raise NotImplementedError()
    
    @property
    def dest_height(self) -> int:
        '''Gets the height of the dest.'''
        raise NotImplementedError()
    
    @dest_height.setter
    def dest_height(self, value : int) -> None:
        '''Sets the height of the dest.'''
        raise NotImplementedError()
    
    @property
    def dest_width(self) -> int:
        '''Gets the width of the dest.'''
        raise NotImplementedError()
    
    @dest_width.setter
    def dest_width(self, value : int) -> None:
        '''Sets the width of the dest.'''
        raise NotImplementedError()
    
    @property
    def dst_position(self) -> aspose.imaging.Point:
        '''Gets the DST position.'''
        raise NotImplementedError()
    
    @dst_position.setter
    def dst_position(self, value : aspose.imaging.Point) -> None:
        '''Sets the DST position.'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets the reserved.'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets the reserved.'''
        raise NotImplementedError()
    
    @property
    def bitmap(self) -> aspose.imaging.fileformats.wmf.objects.WmfBitmap16:
        '''Gets the bitmap.'''
        raise NotImplementedError()
    
    @bitmap.setter
    def bitmap(self, value : aspose.imaging.fileformats.wmf.objects.WmfBitmap16) -> None:
        '''Sets the bitmap.'''
        raise NotImplementedError()
    

class WmfBitmap16(aspose.imaging.fileformats.emf.MetaObject):
    '''The Bitmap16 Object specifies information about the dimensions and color
    format of a bitmap.'''
    
    def __init__(self) -> None:
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
    def width(self) -> int:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    
    @property
    def width_bytes(self) -> int:
        '''Gets the width bytes.'''
        raise NotImplementedError()
    
    @width_bytes.setter
    def width_bytes(self, value : int) -> None:
        '''Sets the width bytes.'''
        raise NotImplementedError()
    
    @property
    def planes(self) -> int:
        '''Gets the planes.'''
        raise NotImplementedError()
    
    @planes.setter
    def planes(self, value : int) -> None:
        '''Sets the planes.'''
        raise NotImplementedError()
    
    @property
    def bits_pixel(self) -> int:
        '''Gets the bits pixel.'''
        raise NotImplementedError()
    
    @bits_pixel.setter
    def bits_pixel(self, value : int) -> None:
        '''Sets the bits pixel.'''
        raise NotImplementedError()
    
    @property
    def bits(self) -> List[int]:
        '''Gets the bits.'''
        raise NotImplementedError()
    
    @bits.setter
    def bits(self, value : List[int]) -> None:
        '''Sets the bits.'''
        raise NotImplementedError()
    

class WmfBitmapBaseHeader(aspose.imaging.fileformats.emf.MetaObject):
    '''The base bitmap header class.'''
    
    @property
    def header_size(self) -> int:
        '''Gets a 32-bit unsigned integer that defines the size of this
        object, in bytes.'''
        raise NotImplementedError()
    
    @header_size.setter
    def header_size(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that defines the size of this
        object, in bytes.'''
        raise NotImplementedError()
    
    @property
    def planes(self) -> int:
        '''Gets a 16-bit unsigned integer that defines the number of
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.planes` for the target device. This value MUST be
        0x0001.'''
        raise NotImplementedError()
    
    @planes.setter
    def planes(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that defines the number of
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.planes` for the target device. This value MUST be
        0x0001.'''
        raise NotImplementedError()
    
    @property
    def bit_count(self) -> aspose.imaging.apsbuilder.dib.DibBitCount:
        '''Gets a 16-bit unsigned integer that defines the format of
        each pixel, and the maximum number of colors in the DIB. This value
        MUST be in the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.bit_count` Enumeration (section 2.1.1.3).'''
        raise NotImplementedError()
    
    @bit_count.setter
    def bit_count(self, value : aspose.imaging.apsbuilder.dib.DibBitCount) -> None:
        '''Sets a 16-bit unsigned integer that defines the format of
        each pixel, and the maximum number of colors in the DIB. This value
        MUST be in the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.bit_count` Enumeration (section 2.1.1.3).'''
        raise NotImplementedError()
    

class WmfBitmapCoreHeader(WmfBitmapBaseHeader):
    '''The BitmapCoreHeader Object contains information about the dimensions
    and color format of a device-independent bitmap(DIB).'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def header_size(self) -> int:
        '''Gets a 32-bit unsigned integer that defines the size of this
        object, in bytes.'''
        raise NotImplementedError()
    
    @header_size.setter
    def header_size(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that defines the size of this
        object, in bytes.'''
        raise NotImplementedError()
    
    @property
    def planes(self) -> int:
        '''Gets a 16-bit unsigned integer that defines the number of
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.planes` for the target device. This value MUST be
        0x0001.'''
        raise NotImplementedError()
    
    @planes.setter
    def planes(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that defines the number of
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.planes` for the target device. This value MUST be
        0x0001.'''
        raise NotImplementedError()
    
    @property
    def bit_count(self) -> aspose.imaging.apsbuilder.dib.DibBitCount:
        '''Gets a 16-bit unsigned integer that defines the format of
        each pixel, and the maximum number of colors in the DIB. This value
        MUST be in the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.bit_count` Enumeration (section 2.1.1.3).'''
        raise NotImplementedError()
    
    @bit_count.setter
    def bit_count(self, value : aspose.imaging.apsbuilder.dib.DibBitCount) -> None:
        '''Sets a 16-bit unsigned integer that defines the format of
        each pixel, and the maximum number of colors in the DIB. This value
        MUST be in the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.bit_count` Enumeration (section 2.1.1.3).'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets a 16-bit unsigned integer that defines the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapCoreHeader.width` of the DIB, in pixels'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that defines the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapCoreHeader.width` of the DIB, in pixels'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets a 16-bit unsigned integer that defines the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapCoreHeader.height` of the DIB, in pixels'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that defines the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapCoreHeader.height` of the DIB, in pixels'''
        raise NotImplementedError()
    

class WmfBitmapInfoHeader(WmfBitmapBaseHeader):
    '''The BitmapInfoHeader Object contains information about the dimensions and color format of a device-independent
    bitmap (DIB).'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def header_size(self) -> int:
        '''Gets a 32-bit unsigned integer that defines the size of this
        object, in bytes.'''
        raise NotImplementedError()
    
    @header_size.setter
    def header_size(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that defines the size of this
        object, in bytes.'''
        raise NotImplementedError()
    
    @property
    def planes(self) -> int:
        '''Gets a 16-bit unsigned integer that defines the number of
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.planes` for the target device. This value MUST be
        0x0001.'''
        raise NotImplementedError()
    
    @planes.setter
    def planes(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that defines the number of
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.planes` for the target device. This value MUST be
        0x0001.'''
        raise NotImplementedError()
    
    @property
    def bit_count(self) -> aspose.imaging.apsbuilder.dib.DibBitCount:
        '''Gets a 16-bit unsigned integer that defines the format of
        each pixel, and the maximum number of colors in the DIB. This value
        MUST be in the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.bit_count` Enumeration (section 2.1.1.3).'''
        raise NotImplementedError()
    
    @bit_count.setter
    def bit_count(self, value : aspose.imaging.apsbuilder.dib.DibBitCount) -> None:
        '''Sets a 16-bit unsigned integer that defines the format of
        each pixel, and the maximum number of colors in the DIB. This value
        MUST be in the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader.bit_count` Enumeration (section 2.1.1.3).'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets a 32-bit signed integer that defines the width of the DIB, in pixels. This value MUST be positive.
        This field SHOULD specify the width of the decompressed image file, if the Compression value specifies JPEG or PNG
        format.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets a 32-bit signed integer that defines the width of the DIB, in pixels. This value MUST be positive.
        This field SHOULD specify the width of the decompressed image file, if the Compression value specifies JPEG or PNG
        format.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets  32-bit signed integer that defines the height of the DIB, in pixels. This value MUST NOT be zero.
        If this value is positive, the DIB is a bottom-up bitmap, and its origin is the lower-left corner.
        If this value is negative, the DIB is a top-down bitmap, and its origin is the upper-left corner. Top-down bitmaps
        do not support compression.
        This field SHOULD specify the height of the decompressed image file, if the Compression value specifies JPEG or PNG
        format.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets  32-bit signed integer that defines the height of the DIB, in pixels. This value MUST NOT be zero.
        If this value is positive, the DIB is a bottom-up bitmap, and its origin is the lower-left corner.
        If this value is negative, the DIB is a top-down bitmap, and its origin is the upper-left corner. Top-down bitmaps
        do not support compression.
        This field SHOULD specify the height of the decompressed image file, if the Compression value specifies JPEG or PNG
        format.'''
        raise NotImplementedError()
    
    @property
    def compression(self) -> aspose.imaging.fileformats.wmf.consts.WmfCompression:
        '''Gets a 32-bit unsigned integer that defines the compression mode of the DIB. This value MUST be in the
        Compression Enumeration (section 2.1.1.7).
        This value MUST NOT specify a compressed format if the DIB is a top-down bitmap, as indicated by the Height value.'''
        raise NotImplementedError()
    
    @compression.setter
    def compression(self, value : aspose.imaging.fileformats.wmf.consts.WmfCompression) -> None:
        '''Sets a 32-bit unsigned integer that defines the compression mode of the DIB. This value MUST be in the
        Compression Enumeration (section 2.1.1.7).
        This value MUST NOT specify a compressed format if the DIB is a top-down bitmap, as indicated by the Height value.'''
        raise NotImplementedError()
    
    @property
    def image_size(self) -> int:
        '''Gets a 32-bit unsigned integer that defines the size, in bytes, of the image.
        If the Compression value is BI_RGB, this value SHOULD be zero and MUST be ignored.
        If the Compression value is BI_JPEG or BI_PNG, this value MUST specify the size of the JPEG or PNG image buffer,
        respectively.'''
        raise NotImplementedError()
    
    @image_size.setter
    def image_size(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that defines the size, in bytes, of the image.
        If the Compression value is BI_RGB, this value SHOULD be zero and MUST be ignored.
        If the Compression value is BI_JPEG or BI_PNG, this value MUST specify the size of the JPEG or PNG image buffer,
        respectively.'''
        raise NotImplementedError()
    
    @property
    def x_pels_per_meter(self) -> int:
        '''Gets a 32-bit signed integer that defines the horizontal resolution, in pixels-per-meter, of the target
        device for the DIB'''
        raise NotImplementedError()
    
    @x_pels_per_meter.setter
    def x_pels_per_meter(self, value : int) -> None:
        '''Sets a 32-bit signed integer that defines the horizontal resolution, in pixels-per-meter, of the target
        device for the DIB'''
        raise NotImplementedError()
    
    @property
    def y_pels_per_meter(self) -> int:
        '''Gets a 32-bit signed integer that defines the vertical resolution, in pixels-per-meter, of the target
        device for the DIB'''
        raise NotImplementedError()
    
    @y_pels_per_meter.setter
    def y_pels_per_meter(self, value : int) -> None:
        '''Sets a 32-bit signed integer that defines the vertical resolution, in pixels-per-meter, of the target
        device for the DIB'''
        raise NotImplementedError()
    
    @property
    def color_used(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of indexes in the color table used by the DIB, as
        follows:
        If this value is zero, the DIB uses the maximum number of colors that correspond to the BitCount value.
        If this value is nonzero and the BitCount value is less than 16, this value specifies the number of colors used by
        the DIB.
        If this value is nonzero and the BitCount value is 16 or greater, this value specifies the size of the color table
        used to optimize performance of the system palette.
        Note If this value is nonzero and greater than the maximum possible size of the color table based on the BitCount
        value, the maximum color table size SHOULD be assumed.'''
        raise NotImplementedError()
    
    @color_used.setter
    def color_used(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of indexes in the color table used by the DIB, as
        follows:
        If this value is zero, the DIB uses the maximum number of colors that correspond to the BitCount value.
        If this value is nonzero and the BitCount value is less than 16, this value specifies the number of colors used by
        the DIB.
        If this value is nonzero and the BitCount value is 16 or greater, this value specifies the size of the color table
        used to optimize performance of the system palette.
        Note If this value is nonzero and greater than the maximum possible size of the color table based on the BitCount
        value, the maximum color table size SHOULD be assumed.'''
        raise NotImplementedError()
    
    @property
    def color_important(self) -> int:
        '''Gets a 32-bit unsigned integer that defines the number of color indexes that are required for displaying
        the DIB.
        If this value is zero, all color indexes are required'''
        raise NotImplementedError()
    
    @color_important.setter
    def color_important(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that defines the number of color indexes that are required for displaying
        the DIB.
        If this value is zero, all color indexes are required'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def STRUCTURE_SIZE() -> int:
        '''The structure size'''
        raise NotImplementedError()


class WmfChord(WmfRectangle):
    '''The META_CHORD record draws a chord, which is defined by a region
    bounded by the intersection of an ellipse with a line segment. The chord
    is outlined using the pen and filled using the brush that are defined in
    the playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def radial2(self) -> aspose.imaging.Point:
        '''Gets the radial2.'''
        raise NotImplementedError()
    
    @radial2.setter
    def radial2(self, value : aspose.imaging.Point) -> None:
        '''Sets the radial2.'''
        raise NotImplementedError()
    
    @property
    def radial1(self) -> aspose.imaging.Point:
        '''Gets the radial1.'''
        raise NotImplementedError()
    
    @radial1.setter
    def radial1(self, value : aspose.imaging.Point) -> None:
        '''Sets the radial1.'''
        raise NotImplementedError()
    

class WmfCieXyz:
    '''The CIEXYZ Object defines information about the CIEXYZ chromaticity
    object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def ciexyz_x(self) -> int:
        '''Gets a 32-bit 2.30 fixed point type that defines the x
        chromaticity value.'''
        raise NotImplementedError()
    
    @ciexyz_x.setter
    def ciexyz_x(self, value : int) -> None:
        '''Sets a 32-bit 2.30 fixed point type that defines the x
        chromaticity value.'''
        raise NotImplementedError()
    
    @property
    def ciexyz_y(self) -> int:
        '''Gets a 32-bit 2.30 fixed point type that defines the y
        chromaticity value.'''
        raise NotImplementedError()
    
    @ciexyz_y.setter
    def ciexyz_y(self, value : int) -> None:
        '''Sets a 32-bit 2.30 fixed point type that defines the y
        chromaticity value.'''
        raise NotImplementedError()
    
    @property
    def ciexyz_z(self) -> int:
        '''Gets a 32-bit 2.30 fixed point type that defines the z
        chromaticity value.'''
        raise NotImplementedError()
    
    @ciexyz_z.setter
    def ciexyz_z(self, value : int) -> None:
        '''Sets a 32-bit 2.30 fixed point type that defines the z
        chromaticity value.'''
        raise NotImplementedError()
    

class WmfCieXyzTriple:
    '''The CIEXYZTriple Object defines information about the CIEXYZTriple color
    object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def ciexyz_red(self) -> aspose.imaging.fileformats.wmf.objects.WmfCieXyz:
        '''Gets a 96-bit CIEXYZ Object that defines the red
        chromaticity values.'''
        raise NotImplementedError()
    
    @ciexyz_red.setter
    def ciexyz_red(self, value : aspose.imaging.fileformats.wmf.objects.WmfCieXyz) -> None:
        '''Sets a 96-bit CIEXYZ Object that defines the red
        chromaticity values.'''
        raise NotImplementedError()
    
    @property
    def ciexyz_green(self) -> aspose.imaging.fileformats.wmf.objects.WmfCieXyz:
        '''Gets a 96-bit CIEXYZ Object that defines the green
        chromaticity values.'''
        raise NotImplementedError()
    
    @ciexyz_green.setter
    def ciexyz_green(self, value : aspose.imaging.fileformats.wmf.objects.WmfCieXyz) -> None:
        '''Sets a 96-bit CIEXYZ Object that defines the green
        chromaticity values.'''
        raise NotImplementedError()
    
    @property
    def ciexyz_blue(self) -> aspose.imaging.fileformats.wmf.objects.WmfCieXyz:
        '''Gets a 96-bit CIEXYZ Object that defines the blue
        chromaticity values.'''
        raise NotImplementedError()
    
    @ciexyz_blue.setter
    def ciexyz_blue(self, value : aspose.imaging.fileformats.wmf.objects.WmfCieXyz) -> None:
        '''Sets a 96-bit CIEXYZ Object that defines the blue
        chromaticity values.'''
        raise NotImplementedError()
    

class WmfCreateBrushInDirect(WmfGraphicObject):
    '''The Create brush in direct'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfCreateBrushInDirect` class.'''
        raise NotImplementedError()
    
    @property
    def index(self) -> int:
        '''Gets the index.'''
        raise NotImplementedError()
    
    @index.setter
    def index(self, value : int) -> None:
        '''Sets the index.'''
        raise NotImplementedError()
    
    @property
    def log_brush(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfLogBrushEx:
        '''Gets the log brush.'''
        raise NotImplementedError()
    
    @log_brush.setter
    def log_brush(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfLogBrushEx) -> None:
        '''Sets the log brush.'''
        raise NotImplementedError()
    

class WmfCreateFontInDirect(WmfGraphicObject):
    '''The Create font'''
    
    def __init__(self) -> None:
        '''WMFs the record.'''
        raise NotImplementedError()
    
    @property
    def index(self) -> int:
        '''Gets the index.'''
        raise NotImplementedError()
    
    @index.setter
    def index(self, value : int) -> None:
        '''Sets the index.'''
        raise NotImplementedError()
    
    @property
    def log_font(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfLogFont:
        '''Gets the log font.'''
        raise NotImplementedError()
    
    @log_font.setter
    def log_font(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfLogFont) -> None:
        '''Sets the log font.'''
        raise NotImplementedError()
    
    @property
    def extended_bytes(self) -> List[int]:
        '''Gets the extended bytes.'''
        raise NotImplementedError()
    
    @extended_bytes.setter
    def extended_bytes(self, value : List[int]) -> None:
        '''Sets the extended bytes.'''
        raise NotImplementedError()
    

class WmfCreatePalette(WmfGraphicObject):
    '''The META_CREATEPALETTE record creates a Palette Object (section 2.2.1.3).'''
    
    def __init__(self) -> None:
        '''WMFs the record.'''
        raise NotImplementedError()
    
    @property
    def index(self) -> int:
        '''Gets the index.'''
        raise NotImplementedError()
    
    @index.setter
    def index(self, value : int) -> None:
        '''Sets the index.'''
        raise NotImplementedError()
    
    @property
    def log_palette(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfLogPalette:
        '''Gets the log palette.'''
        raise NotImplementedError()
    
    @log_palette.setter
    def log_palette(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfLogPalette) -> None:
        '''Sets the log palette.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def PALETTE_START() -> int:
        '''The palette start tag'''
        raise NotImplementedError()


class WmfCreatePatternBrush(WmfGraphicObject):
    '''The META_CREATEPATTERNBRUSH record creates a brush object with a pattern
    specified by a bitmap.'''
    
    def __init__(self) -> None:
        '''WMFs the record.'''
        raise NotImplementedError()
    
    @property
    def index(self) -> int:
        '''Gets the index.'''
        raise NotImplementedError()
    
    @index.setter
    def index(self, value : int) -> None:
        '''Sets the index.'''
        raise NotImplementedError()
    
    @property
    def bitmap(self) -> aspose.imaging.fileformats.wmf.objects.WmfBitmap16:
        '''Gets the bitmap.'''
        raise NotImplementedError()
    
    @bitmap.setter
    def bitmap(self, value : aspose.imaging.fileformats.wmf.objects.WmfBitmap16) -> None:
        '''Sets the bitmap.'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> List[int]:
        '''Gets the reserved.'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : List[int]) -> None:
        '''Sets the reserved.'''
        raise NotImplementedError()
    
    @property
    def pattern(self) -> List[int]:
        '''Gets the pattern.'''
        raise NotImplementedError()
    
    @pattern.setter
    def pattern(self, value : List[int]) -> None:
        '''Sets the pattern.'''
        raise NotImplementedError()
    

class WmfCreatePenInDirect(WmfGraphicObject):
    '''The create pen in direct'''
    
    def __init__(self) -> None:
        '''WMFs the record.'''
        raise NotImplementedError()
    
    @property
    def index(self) -> int:
        '''Gets the index.'''
        raise NotImplementedError()
    
    @index.setter
    def index(self, value : int) -> None:
        '''Sets the index.'''
        raise NotImplementedError()
    
    @property
    def log_pen(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfLogPen:
        '''Gets the log pen.'''
        raise NotImplementedError()
    
    @log_pen.setter
    def log_pen(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfLogPen) -> None:
        '''Sets the log pen.'''
        raise NotImplementedError()
    

class WmfCreateRegion(WmfGraphicObject):
    '''The META_CREATEREGION record creates a Region Object (section 2.2.1.5).'''
    
    def __init__(self) -> None:
        '''WMFs the record.'''
        raise NotImplementedError()
    
    @property
    def index(self) -> int:
        '''Gets the index.'''
        raise NotImplementedError()
    
    @index.setter
    def index(self, value : int) -> None:
        '''Sets the index.'''
        raise NotImplementedError()
    
    @property
    def region(self) -> aspose.imaging.fileformats.wmf.objects.WmfRegion:
        '''Gets the region.'''
        raise NotImplementedError()
    
    @region.setter
    def region(self, value : aspose.imaging.fileformats.wmf.objects.WmfRegion) -> None:
        '''Sets the region.'''
        raise NotImplementedError()
    

class WmfDeleteObject(WmfObject):
    '''The Delete object'''
    
    @overload
    def __init__(self, deleted_object : aspose.imaging.fileformats.wmf.objects.WmfGraphicObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfDeleteObject` class.
        
        :param deleted_object: The deleted object.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfDeleteObject` class.'''
        raise NotImplementedError()
    
    @property
    def object_index(self) -> int:
        '''Gets the index of the object.'''
        raise NotImplementedError()
    
    @object_index.setter
    def object_index(self, value : int) -> None:
        '''Sets the index of the object.'''
        raise NotImplementedError()
    

class WmfDeviceIndependentBitmap(aspose.imaging.fileformats.emf.MetaObject):
    '''The DeviceIndependentBitmap Object defines an image in
    device-independent bitmap (DIB) format'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def header(self) -> aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader:
        '''Gets either a BitmapCoreHeader Object (section 2.2.2.2) or a
        BitmapInfoHeader Object (section 2.2.2.3) that specifies information
        about the image'''
        raise NotImplementedError()
    
    @header.setter
    def header(self, value : aspose.imaging.fileformats.wmf.objects.WmfBitmapBaseHeader) -> None:
        '''Sets either a BitmapCoreHeader Object (section 2.2.2.2) or a
        BitmapInfoHeader Object (section 2.2.2.3) that specifies information
        about the image'''
        raise NotImplementedError()
    
    @property
    def colors_data(self) -> List[int]:
        '''Gets an optional array of either RGBQuad Objects (section
        2.2.2.20) or 16-bit unsigned integers that define a color table. The
        size and contents of this field SHOULD be determined from the
        metafile record or object that contains this DeviceIndependentBitmap
        and from information in the DIBHeaderInfo field. See ColorUsage
        Enumeration (section 2.1.1.6) and BitCount Enumeration (section
        2.1.1.3) for additional details'''
        raise NotImplementedError()
    
    @colors_data.setter
    def colors_data(self, value : List[int]) -> None:
        '''Sets an optional array of either RGBQuad Objects (section
        2.2.2.20) or 16-bit unsigned integers that define a color table. The
        size and contents of this field SHOULD be determined from the
        metafile record or object that contains this DeviceIndependentBitmap
        and from information in the DIBHeaderInfo field. See ColorUsage
        Enumeration (section 2.1.1.6) and BitCount Enumeration (section
        2.1.1.3) for additional details'''
        raise NotImplementedError()
    
    @property
    def a_data(self) -> List[int]:
        '''Gets an array of bytes that define the image. The size and
        format of this data is determined by information in the
        DIBHeaderInfo field.'''
        raise NotImplementedError()
    
    @a_data.setter
    def a_data(self, value : List[int]) -> None:
        '''Sets an array of bytes that define the image. The size and
        format of this data is determined by information in the
        DIBHeaderInfo field.'''
        raise NotImplementedError()
    
    @property
    def cached_image(self) -> List[int]:
        '''Gets the cached raster image.'''
        raise NotImplementedError()
    
    @cached_image.setter
    def cached_image(self, value : List[int]) -> None:
        '''Sets the cached raster image.'''
        raise NotImplementedError()
    

class WmfDibBitBlt(WmfObject):
    '''The META_DIBBITBLT record specifies the transfer of a block of pixels in
    device-independent format according to a raster operation.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def raster_operation(self) -> aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation:
        '''Gets the raster operation.'''
        raise NotImplementedError()
    
    @raster_operation.setter
    def raster_operation(self, value : aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation) -> None:
        '''Sets the raster operation.'''
        raise NotImplementedError()
    
    @property
    def src_pos(self) -> aspose.imaging.Point:
        '''Gets the source position.'''
        raise NotImplementedError()
    
    @src_pos.setter
    def src_pos(self, value : aspose.imaging.Point) -> None:
        '''Sets the source position.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    
    @property
    def dst_pos(self) -> aspose.imaging.Point:
        '''Gets the DST position.'''
        raise NotImplementedError()
    
    @dst_pos.setter
    def dst_pos(self, value : aspose.imaging.Point) -> None:
        '''Sets the DST position.'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets the reserved.'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets the reserved.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap:
        '''Gets the source.'''
        raise NotImplementedError()
    
    @source.setter
    def source(self, value : aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap) -> None:
        '''Sets the source.'''
        raise NotImplementedError()
    

class WmfDibCreatePatternBrush(WmfGraphicObject):
    '''The META_DIBCREATEPATTERNBRUSH record creates a Brush Object (section
    2.2.1.1) with a pattern specified by a DeviceIndependentBitmap (DIB)
    Object (section 2.2.2.9).'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def index(self) -> int:
        '''Gets the index.'''
        raise NotImplementedError()
    
    @index.setter
    def index(self, value : int) -> None:
        '''Sets the index.'''
        raise NotImplementedError()
    
    @property
    def style(self) -> aspose.imaging.fileformats.wmf.consts.WmfBrushStyle:
        '''Gets the style.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : aspose.imaging.fileformats.wmf.consts.WmfBrushStyle) -> None:
        '''Sets the style.'''
        raise NotImplementedError()
    
    @property
    def color_usage(self) -> aspose.imaging.fileformats.wmf.consts.WmfColorUsageEnum:
        '''Gets the color usage.'''
        raise NotImplementedError()
    
    @color_usage.setter
    def color_usage(self, value : aspose.imaging.fileformats.wmf.consts.WmfColorUsageEnum) -> None:
        '''Sets the color usage.'''
        raise NotImplementedError()
    
    @property
    def source_bitmap(self) -> aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap:
        '''Gets the source bitmap.'''
        raise NotImplementedError()
    
    @source_bitmap.setter
    def source_bitmap(self, value : aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap) -> None:
        '''Sets the source bitmap.'''
        raise NotImplementedError()
    

class WmfDibStrechBlt(WmfObject):
    '''The META_DIBSTRETCHBLT record specifies the transfer of a block of
    pixels in device-independent format according to a raster operation,
    with possible expansion or contraction.'''
    
    def __init__(self) -> None:
        '''WMFs the record.'''
        raise NotImplementedError()
    
    @property
    def raster_operation(self) -> aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation:
        '''Gets the raster operation.'''
        raise NotImplementedError()
    
    @raster_operation.setter
    def raster_operation(self, value : aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation) -> None:
        '''Sets the raster operation.'''
        raise NotImplementedError()
    
    @property
    def src_height(self) -> int:
        '''Gets the height of the source.'''
        raise NotImplementedError()
    
    @src_height.setter
    def src_height(self, value : int) -> None:
        '''Sets the height of the source.'''
        raise NotImplementedError()
    
    @property
    def src_width(self) -> int:
        '''Gets the width of the source.'''
        raise NotImplementedError()
    
    @src_width.setter
    def src_width(self, value : int) -> None:
        '''Sets the width of the source.'''
        raise NotImplementedError()
    
    @property
    def y_src(self) -> int:
        '''Gets the y source.'''
        raise NotImplementedError()
    
    @y_src.setter
    def y_src(self, value : int) -> None:
        '''Sets the y source.'''
        raise NotImplementedError()
    
    @property
    def x_src(self) -> int:
        '''Gets the x source.'''
        raise NotImplementedError()
    
    @x_src.setter
    def x_src(self, value : int) -> None:
        '''Sets the x source.'''
        raise NotImplementedError()
    
    @property
    def dest_height(self) -> int:
        '''Gets the height of the dest.'''
        raise NotImplementedError()
    
    @dest_height.setter
    def dest_height(self, value : int) -> None:
        '''Sets the height of the dest.'''
        raise NotImplementedError()
    
    @property
    def dest_width(self) -> int:
        '''Gets the width of the dest.'''
        raise NotImplementedError()
    
    @dest_width.setter
    def dest_width(self, value : int) -> None:
        '''Sets the width of the dest.'''
        raise NotImplementedError()
    
    @property
    def y_dest(self) -> int:
        '''Gets the y dest.'''
        raise NotImplementedError()
    
    @y_dest.setter
    def y_dest(self, value : int) -> None:
        '''Sets the y dest.'''
        raise NotImplementedError()
    
    @property
    def x_dest(self) -> int:
        '''Gets the x dest.'''
        raise NotImplementedError()
    
    @x_dest.setter
    def x_dest(self, value : int) -> None:
        '''Sets the x dest.'''
        raise NotImplementedError()
    
    @property
    def source_bitmap(self) -> aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap:
        '''Gets the source bitmap.'''
        raise NotImplementedError()
    
    @source_bitmap.setter
    def source_bitmap(self, value : aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap) -> None:
        '''Sets the source bitmap.'''
        raise NotImplementedError()
    

class WmfEllipse(WmfRectangle):
    '''The META_ELLIPSE record draws an ellipse. The center of the ellipse is
    the center of the specified bounding rectangle. The ellipse is outlined
    by using the pen and is filled by using the brush; these are defined in
    the playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class WmfEof(WmfObject):
    '''The Eof object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    

class WmfEscape(WmfObject):
    '''The wmf escape object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def escape_type(self) -> aspose.imaging.fileformats.wmf.consts.WmfMetafileEscapes:
        '''Gets the type of the escape.'''
        raise NotImplementedError()
    
    @escape_type.setter
    def escape_type(self, value : aspose.imaging.fileformats.wmf.consts.WmfMetafileEscapes) -> None:
        '''Sets the type of the escape.'''
        raise NotImplementedError()
    
    @property
    def escape_record(self) -> aspose.imaging.fileformats.wmf.objects.escaperecords.WmfEscapeRecordBase:
        '''Gets the escape record.'''
        raise NotImplementedError()
    
    @escape_record.setter
    def escape_record(self, value : aspose.imaging.fileformats.wmf.objects.escaperecords.WmfEscapeRecordBase) -> None:
        '''Sets the escape record.'''
        raise NotImplementedError()
    

class WmfExcludeClipRect(WmfRectangle):
    '''The META_EXCLUDECLIPRECT record sets the clipping region in the playback
    device context to the existing clipping region minus the specified
    rectangle.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class WmfExtFloodFill(WmfFloodFill):
    '''The META_EXTFLOODFILL record fills an area with the brush that is
    defined in the playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def color_ref(self) -> int:
        '''Gets the color reference.'''
        raise NotImplementedError()
    
    @color_ref.setter
    def color_ref(self, value : int) -> None:
        '''Sets the color reference.'''
        raise NotImplementedError()
    
    @property
    def y_start(self) -> int:
        '''Gets the y start.'''
        raise NotImplementedError()
    
    @y_start.setter
    def y_start(self, value : int) -> None:
        '''Sets the y start.'''
        raise NotImplementedError()
    
    @property
    def x_start(self) -> int:
        '''Gets the x start.'''
        raise NotImplementedError()
    
    @x_start.setter
    def x_start(self, value : int) -> None:
        '''Sets the x start.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> aspose.imaging.fileformats.wmf.consts.WmfFloodFillMode:
        '''Gets the mode.'''
        raise NotImplementedError()
    
    @mode.setter
    def mode(self, value : aspose.imaging.fileformats.wmf.consts.WmfFloodFillMode) -> None:
        '''Sets the mode.'''
        raise NotImplementedError()
    

class WmfExtTextOut(WmfPointObject):
    '''Wmf ext text out'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    
    @property
    def string_length(self) -> int:
        '''Gets the length of the string.'''
        raise NotImplementedError()
    
    @string_length.setter
    def string_length(self, value : int) -> None:
        '''Sets the length of the string.'''
        raise NotImplementedError()
    
    @property
    def fw_opts(self) -> int:
        '''Gets the fw opts.'''
        raise NotImplementedError()
    
    @fw_opts.setter
    def fw_opts(self, value : int) -> None:
        '''Sets the fw opts.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
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
    
    @property
    def dx(self) -> List[int]:
        '''Gets the dx.'''
        raise NotImplementedError()
    
    @dx.setter
    def dx(self, value : List[int]) -> None:
        '''Sets the dx.'''
        raise NotImplementedError()
    
    @property
    def extended_byte(self) -> int:
        '''Gets the extended byte.'''
        raise NotImplementedError()
    
    @extended_byte.setter
    def extended_byte(self, value : int) -> None:
        '''Sets the extended byte.'''
        raise NotImplementedError()
    

class WmfFillRegion(WmfObject):
    '''The META_FILLREGION record fills a region using a specified brush.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfFillRegion` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, region : aspose.imaging.fileformats.wmf.objects.WmfGraphicObject, brush : aspose.imaging.fileformats.wmf.objects.WmfGraphicObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfFillRegion` class.
        
        :param region: The region.
        :param brush: The brush.'''
        raise NotImplementedError()
    
    @property
    def region_index(self) -> int:
        '''Gets the index of the region.'''
        raise NotImplementedError()
    
    @region_index.setter
    def region_index(self, value : int) -> None:
        '''Sets the index of the region.'''
        raise NotImplementedError()
    
    @property
    def brush_index(self) -> int:
        '''Gets the index of the brush.'''
        raise NotImplementedError()
    
    @brush_index.setter
    def brush_index(self, value : int) -> None:
        '''Sets the index of the brush.'''
        raise NotImplementedError()
    

class WmfFloodFill(WmfObject):
    '''The META_FLOODFILL record fills an area of the output surface with the
    brush that is defined in the playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def color_ref(self) -> int:
        '''Gets the color reference.'''
        raise NotImplementedError()
    
    @color_ref.setter
    def color_ref(self, value : int) -> None:
        '''Sets the color reference.'''
        raise NotImplementedError()
    
    @property
    def y_start(self) -> int:
        '''Gets the y start.'''
        raise NotImplementedError()
    
    @y_start.setter
    def y_start(self, value : int) -> None:
        '''Sets the y start.'''
        raise NotImplementedError()
    
    @property
    def x_start(self) -> int:
        '''Gets the x start.'''
        raise NotImplementedError()
    
    @x_start.setter
    def x_start(self, value : int) -> None:
        '''Sets the x start.'''
        raise NotImplementedError()
    

class WmfFrameRegion(WmfObject):
    '''The wmf frame region object.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfFillRegion` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, region : aspose.imaging.fileformats.wmf.objects.WmfGraphicObject, brush : aspose.imaging.fileformats.wmf.objects.WmfGraphicObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfFillRegion` class.
        
        :param region: The region.
        :param brush: The brush.'''
        raise NotImplementedError()
    
    @property
    def region_index(self) -> int:
        '''Gets the index of the region.'''
        raise NotImplementedError()
    
    @region_index.setter
    def region_index(self, value : int) -> None:
        '''Sets the index of the region.'''
        raise NotImplementedError()
    
    @property
    def brush_index(self) -> int:
        '''Gets the index of the brush.'''
        raise NotImplementedError()
    
    @brush_index.setter
    def brush_index(self, value : int) -> None:
        '''Sets the index of the brush.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    

class WmfGraphicObject(WmfObject):
    '''The WMF Graphics Objects specify parameters for graphics output.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def index(self) -> int:
        '''Gets the index.'''
        raise NotImplementedError()
    
    @index.setter
    def index(self, value : int) -> None:
        '''Sets the index.'''
        raise NotImplementedError()
    

class WmfIntersectClipRect(WmfObject):
    '''The META_INTERSECTCLIPRECT record sets the clipping region in the
    playback device context to the intersection of the existing clipping
    region and the specified rectangle.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class WmfInvertRegion(WmfObject):
    '''The META_INVERTREGION record draws a region in which the colors are
    inverted.'''
    
    @overload
    def __init__(self, region : aspose.imaging.fileformats.wmf.objects.WmfGraphicObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfInvertRegion` class.
        
        :param region: The region.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfInvertRegion` class.'''
        raise NotImplementedError()
    
    @property
    def region_index(self) -> int:
        '''Gets the index of the region.'''
        raise NotImplementedError()
    
    @region_index.setter
    def region_index(self, value : int) -> None:
        '''Sets the index of the region.'''
        raise NotImplementedError()
    

class WmfLineTo(WmfPointObject):
    '''The META_LINETO record draws a line from the drawing position that is
    defined in the playback device context up to, but not including, the
    specified point.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfLogColorSpace(aspose.imaging.fileformats.emf.MetaObject):
    '''The LogColorSpace object specifies a logical color space for the
    playback device context, which can be the name of a color profile in
    ASCII characters.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def signature(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.signature` of color space objects; it MUST be set to
        the value 0x50534F43, which is the ASCII encoding of the string
        "PSOC".'''
        raise NotImplementedError()
    
    @signature.setter
    def signature(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.signature` of color space objects; it MUST be set to
        the value 0x50534F43, which is the ASCII encoding of the string
        "PSOC".'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets a 32-bit unsigned integer that defines a
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.version` number; it MUST be0x00000400.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that defines a
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.version` number; it MUST be0x00000400.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets a 32-bit unsigned integer that defines the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.size` of this object, in bytes.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that defines the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.size` of this object, in bytes.'''
        raise NotImplementedError()
    
    @property
    def color_space_type(self) -> aspose.imaging.fileformats.wmf.consts.WmfLogicalColorSpaceEnum:
        '''Gets a 32-bit signed integer that specifies the color space
        type. It MUST be defined in the LogicalColorSpace enumeration
        (section 2.1.1.14). If this value is LCS_sRGB or
        LCS_WINDOWS_COLOR_SPACE, the sRGB color space MUST be used.'''
        raise NotImplementedError()
    
    @color_space_type.setter
    def color_space_type(self, value : aspose.imaging.fileformats.wmf.consts.WmfLogicalColorSpaceEnum) -> None:
        '''Sets a 32-bit signed integer that specifies the color space
        type. It MUST be defined in the LogicalColorSpace enumeration
        (section 2.1.1.14). If this value is LCS_sRGB or
        LCS_WINDOWS_COLOR_SPACE, the sRGB color space MUST be used.'''
        raise NotImplementedError()
    
    @property
    def intent(self) -> aspose.imaging.fileformats.wmf.consts.WmfGamutMappingIntent:
        '''Gets a 32-bit signed integer that defines the gamut mapping
        intent. It MUST be defined in the GamutMappingIntent enumeration
        (section 2.1.1.11).'''
        raise NotImplementedError()
    
    @intent.setter
    def intent(self, value : aspose.imaging.fileformats.wmf.consts.WmfGamutMappingIntent) -> None:
        '''Sets a 32-bit signed integer that defines the gamut mapping
        intent. It MUST be defined in the GamutMappingIntent enumeration
        (section 2.1.1.11).'''
        raise NotImplementedError()
    
    @property
    def endpoints(self) -> aspose.imaging.fileformats.wmf.objects.WmfCieXyzTriple:
        '''Gets a CIEXYZTriple object (section 2.2.2.7) that defines
        the CIE chromaticity x, y, and z coordinates of the three colors
        that correspond to the RGB :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.endpoints` for the logical
        color space associated with the bitmap. If the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field does not specify
        LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @endpoints.setter
    def endpoints(self, value : aspose.imaging.fileformats.wmf.objects.WmfCieXyzTriple) -> None:
        '''Sets a CIEXYZTriple object (section 2.2.2.7) that defines
        the CIE chromaticity x, y, and z coordinates of the three colors
        that correspond to the RGB :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.endpoints` for the logical
        color space associated with the bitmap. If the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field does not specify
        LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def gamma_red(self) -> int:
        '''Gets a 32-bit fixed point value that defines the toned
        response curve for red. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @gamma_red.setter
    def gamma_red(self, value : int) -> None:
        '''Sets a 32-bit fixed point value that defines the toned
        response curve for red. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def gamma_green(self) -> int:
        '''Gets a 32-bit fixed point value that defines the toned
        response curve for green. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @gamma_green.setter
    def gamma_green(self, value : int) -> None:
        '''Sets a 32-bit fixed point value that defines the toned
        response curve for green. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def gamma_blue(self) -> int:
        '''Gets a 32-bit fixed point value that defines the toned
        response curve for blue. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @gamma_blue.setter
    def gamma_blue(self, value : int) -> None:
        '''Sets a 32-bit fixed point value that defines the toned
        response curve for blue. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def filename(self) -> str:
        '''Gets an optional, ASCII charactger string that specifies the
        name of a file that contains a color profile. If a file name is
        specified, and the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field is set to
        LCS_CALIBRATED_RGB, the other fields of this structure SHOULD be
        ignored.'''
        raise NotImplementedError()
    
    @filename.setter
    def filename(self, value : str) -> None:
        '''Sets an optional, ASCII charactger string that specifies the
        name of a file that contains a color profile. If a file name is
        specified, and the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpace.color_space_type` field is set to
        LCS_CALIBRATED_RGB, the other fields of this structure SHOULD be
        ignored.'''
        raise NotImplementedError()
    

class WmfLogColorSpaceW(aspose.imaging.fileformats.emf.MetaObject):
    '''The LogColorSpaceW object specifies a logical color space, which can be
    defined by a color profile file with a name consisting of Unicode 16-bit
    characters.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def signature(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.signature` of color space objects; it MUST be set to
        the value 0x50534F43, which is the ASCII encoding of the string
        "PSOC".'''
        raise NotImplementedError()
    
    @signature.setter
    def signature(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.signature` of color space objects; it MUST be set to
        the value 0x50534F43, which is the ASCII encoding of the string
        "PSOC".'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets a 32-bit unsigned integer that defines a
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.version` number; it MUST be0x00000400.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that defines a
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.version` number; it MUST be0x00000400.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets a 32-bit unsigned integer that defines the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.size` of this object, in bytes.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that defines the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.size` of this object, in bytes.'''
        raise NotImplementedError()
    
    @property
    def color_space_type(self) -> aspose.imaging.fileformats.wmf.consts.WmfLogicalColorSpaceEnum:
        '''Gets a 32-bit signed integer that specifies the color space
        type. It MUST be defined in the LogicalColorSpace enumeration
        (section 2.1.1.14). If this value is LCS_sRGB or
        LCS_WINDOWS_COLOR_SPACE, the sRGB color space MUST be used.'''
        raise NotImplementedError()
    
    @color_space_type.setter
    def color_space_type(self, value : aspose.imaging.fileformats.wmf.consts.WmfLogicalColorSpaceEnum) -> None:
        '''Sets a 32-bit signed integer that specifies the color space
        type. It MUST be defined in the LogicalColorSpace enumeration
        (section 2.1.1.14). If this value is LCS_sRGB or
        LCS_WINDOWS_COLOR_SPACE, the sRGB color space MUST be used.'''
        raise NotImplementedError()
    
    @property
    def intent(self) -> aspose.imaging.fileformats.wmf.consts.WmfGamutMappingIntent:
        '''Gets a 32-bit signed integer that defines the gamut mapping
        intent. It MUST be defined in the GamutMappingIntent enumeration
        (section 2.1.1.11).'''
        raise NotImplementedError()
    
    @intent.setter
    def intent(self, value : aspose.imaging.fileformats.wmf.consts.WmfGamutMappingIntent) -> None:
        '''Sets a 32-bit signed integer that defines the gamut mapping
        intent. It MUST be defined in the GamutMappingIntent enumeration
        (section 2.1.1.11).'''
        raise NotImplementedError()
    
    @property
    def endpoints(self) -> aspose.imaging.fileformats.wmf.objects.WmfCieXyzTriple:
        '''Gets a CIEXYZTriple object (section 2.2.2.7) that defines
        the CIE chromaticity x, y, and z coordinates of the three colors
        that correspond to the RGB :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.endpoints` for the logical
        color space associated with the bitmap. If the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field does not specify
        LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @endpoints.setter
    def endpoints(self, value : aspose.imaging.fileformats.wmf.objects.WmfCieXyzTriple) -> None:
        '''Sets a CIEXYZTriple object (section 2.2.2.7) that defines
        the CIE chromaticity x, y, and z coordinates of the three colors
        that correspond to the RGB :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.endpoints` for the logical
        color space associated with the bitmap. If the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field does not specify
        LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def gamma_red(self) -> int:
        '''Gets a 32-bit fixed point value that defines the toned
        response curve for red. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @gamma_red.setter
    def gamma_red(self, value : int) -> None:
        '''Sets a 32-bit fixed point value that defines the toned
        response curve for red. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def gamma_green(self) -> int:
        '''Gets a 32-bit fixed point value that defines the toned
        response curve for green. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @gamma_green.setter
    def gamma_green(self, value : int) -> None:
        '''Sets a 32-bit fixed point value that defines the toned
        response curve for green. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def gamma_blue(self) -> int:
        '''Gets a 32-bit fixed point value that defines the toned
        response curve for blue. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @gamma_blue.setter
    def gamma_blue(self, value : int) -> None:
        '''Sets a 32-bit fixed point value that defines the toned
        response curve for blue. If the :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field
        does not specify LCS_CALIBRATED_RGB, this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def filename(self) -> str:
        '''Gets an optional, null-terminated Unicode UTF16-LE character
        string, which specifies the name of a file that contains a color
        profile. If a file name is specified, and the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field is set to LCS_CALIBRATED_RGB, the
        other fields of this structure SHOULD be ignored.'''
        raise NotImplementedError()
    
    @filename.setter
    def filename(self, value : str) -> None:
        '''Sets an optional, null-terminated Unicode UTF16-LE character
        string, which specifies the name of a file that contains a color
        profile. If a file name is specified, and the
        :py:attr:`aspose.imaging.fileformats.wmf.objects.WmfLogColorSpaceW.color_space_type` field is set to LCS_CALIBRATED_RGB, the
        other fields of this structure SHOULD be ignored.'''
        raise NotImplementedError()
    

class WmfMoveTo(WmfPointObject):
    '''The META_MOVETO record sets the output position in the playback device
    context to a specified point.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfObject(aspose.imaging.fileformats.emf.MetaObject):
    '''The base wmf object.'''
    

class WmfOffsetClipRgn(WmfPointObject):
    '''The META_OFFSETCLIPRGN record moves the clipping region in the playback
    device context by the specified offsets.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfOffsetViewPortOrg(WmfPointObject):
    '''The META_OFFSETVIEWPORTORG record moves the viewport origin in the
    playback device context by specified horizontal and vertical offsets.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfOffsetWindowOrg(WmfPointObject):
    '''The META_OFFSETWINDOWORG record moves the output window origin in the
    playback device context by specified horizontal and vertical offsets.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfPaintRegion(WmfObject):
    '''The META_PAINTREGION record paints the specified region by using the
    brush that is defined in the playback device context.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfSelectClipRegion` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, region : aspose.imaging.fileformats.wmf.objects.WmfGraphicObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfSelectClipRegion` class.
        
        :param region: The region.'''
        raise NotImplementedError()
    
    @property
    def region_index(self) -> int:
        '''Gets the index of the region.'''
        raise NotImplementedError()
    
    @region_index.setter
    def region_index(self, value : int) -> None:
        '''Sets the index of the region.'''
        raise NotImplementedError()
    

class WmfPatBlt(WmfPointObject):
    '''The META_PATBLT record paints a specified rectangle using the brush that
    is defined in the playback device context. The brush color and the
    surface color or colors are combined using the specified raster
    operation.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    
    @property
    def raster_operation(self) -> aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation:
        '''Gets the raster operation.'''
        raise NotImplementedError()
    
    @raster_operation.setter
    def raster_operation(self, value : aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation) -> None:
        '''Sets the raster operation.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    

class WmfPie(WmfRectangle):
    '''The META_PIE record draws a pie-shaped wedge bounded by the intersection
    of an ellipse and two radials. The pie is outlined by using the pen and
    filled by using the brush that are defined in the playback device
    context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def radial2(self) -> aspose.imaging.Point:
        '''Gets the radial2.'''
        raise NotImplementedError()
    
    @radial2.setter
    def radial2(self, value : aspose.imaging.Point) -> None:
        '''Sets the radial2.'''
        raise NotImplementedError()
    
    @property
    def radial1(self) -> aspose.imaging.Point:
        '''Gets the radial1.'''
        raise NotImplementedError()
    
    @radial1.setter
    def radial1(self, value : aspose.imaging.Point) -> None:
        '''Sets the radial1.'''
        raise NotImplementedError()
    

class WmfPitchAndFamily:
    '''The PitchAndFamily object specifies the pitch and family properties of a
    Font object (section 2.2.1.2). Pitch refers to the width of the
    characters, and family refers to the general appearance of a font.'''
    
    @overload
    def __init__(self, byte_data : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily`
        struct.
        
        :param byte_data: The  data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, pitch : aspose.imaging.fileformats.wmf.consts.WmfPitchFont, family : aspose.imaging.fileformats.wmf.consts.WmfFamilyFont) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily`
        struct.
        
        :param pitch: The pitch.
        :param family: The family.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def to_byte(self) -> int:
        '''To the byte.
        
        :returns: The byte value.'''
        raise NotImplementedError()
    
    @property
    def family(self) -> aspose.imaging.fileformats.wmf.consts.WmfFamilyFont:
        '''Gets A property of a font that describes its general appearance.
        This MUST be a value in the FamilyFont enumeration'''
        raise NotImplementedError()
    
    @property
    def pitch(self) -> aspose.imaging.fileformats.wmf.consts.WmfPitchFont:
        '''Gets A property of a font that describes the pitch, of the
        characters. This MUST be a value in the PitchFont enumeration.'''
        raise NotImplementedError()
    
    @property
    def byte_data(self) -> int:
        '''Sets the  data.'''
        raise NotImplementedError()
    
    @byte_data.setter
    def byte_data(self, value : int) -> None:
        '''Sets the  data.'''
        raise NotImplementedError()
    

class WmfPointObject(WmfObject):
    '''The Point object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfPolyLine(WmfObject):
    '''The poly line object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def number_of_point(self) -> int:
        '''Gets the number of point. A 16-bit signed integer that
        defines the number of points in the array.'''
        raise NotImplementedError()
    
    @number_of_point.setter
    def number_of_point(self, value : int) -> None:
        '''Sets the number of point. A 16-bit signed integer that
        defines the number of points in the array.'''
        raise NotImplementedError()
    
    @property
    def a_points(self) -> List[aspose.imaging.Point]:
        '''Gets the points. A NumberOfPoints array of 32-bit PointS
        Objects, in logical units.'''
        raise NotImplementedError()
    
    @a_points.setter
    def a_points(self, value : List[aspose.imaging.Point]) -> None:
        '''Sets the points. A NumberOfPoints array of 32-bit PointS
        Objects, in logical units.'''
        raise NotImplementedError()
    

class WmfPolyPolygon(WmfObject):
    '''The PolyPolygon Object defines a series of closed polygons.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def number_of_polygons(self) -> int:
        '''Gets the number of polygons. The number of polygons in the
        object.'''
        raise NotImplementedError()
    
    @number_of_polygons.setter
    def number_of_polygons(self, value : int) -> None:
        '''Sets the number of polygons. The number of polygons in the
        object.'''
        raise NotImplementedError()
    
    @property
    def a_points_per_polygon(self) -> List[int]:
        '''Gets a points per polygon.'''
        raise NotImplementedError()
    
    @a_points_per_polygon.setter
    def a_points_per_polygon(self, value : List[int]) -> None:
        '''Sets a points per polygon.'''
        raise NotImplementedError()
    
    @property
    def a_points(self) -> List[List[aspose.imaging.Point]]:
        '''Gets a points.'''
        raise NotImplementedError()
    
    @a_points.setter
    def a_points(self, value : List[List[aspose.imaging.Point]]) -> None:
        '''Sets a points.'''
        raise NotImplementedError()
    

class WmfPolygon(WmfObject):
    '''The polygon object'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def number_of_point(self) -> int:
        '''Gets the number of point. A 16-bit signed integer that
        defines the number of points in the array.'''
        raise NotImplementedError()
    
    @number_of_point.setter
    def number_of_point(self, value : int) -> None:
        '''Sets the number of point. A 16-bit signed integer that
        defines the number of points in the array.'''
        raise NotImplementedError()
    
    @property
    def a_points(self) -> List[aspose.imaging.Point]:
        '''Gets the points. A NumberOfPoints array of 32-bit PointS
        Objects (section 2.2.2.16), in logical units.'''
        raise NotImplementedError()
    
    @a_points.setter
    def a_points(self, value : List[aspose.imaging.Point]) -> None:
        '''Sets the points. A NumberOfPoints array of 32-bit PointS
        Objects (section 2.2.2.16), in logical units.'''
        raise NotImplementedError()
    

class WmfRealizePalette(WmfObject):
    '''The META_REALIZEPALETTE record maps entries from the logical palette
    that is defined in the playback device context to the system palette.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    

class WmfRecord(aspose.imaging.fileformats.emf.MetaObject):
    '''The Wmf Record'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the size.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Sets the size.'''
        raise NotImplementedError()
    
    @property
    def record_type(self) -> aspose.imaging.fileformats.wmf.consts.WmfRecordType:
        ''':py:attr:`aspose.imaging.fileformats.wmf.objects.WmfRecord.record_type` number (defined in WINDOWS.H)'''
        raise NotImplementedError()
    
    @record_type.setter
    def record_type(self, value : aspose.imaging.fileformats.wmf.consts.WmfRecordType) -> None:
        ''':py:attr:`aspose.imaging.fileformats.wmf.objects.WmfRecord.record_type` number (defined in WINDOWS.H)'''
        raise NotImplementedError()
    

class WmfRectangle(WmfObject):
    '''The META_RECTANGLE record paints a rectangle. The rectangle is outlined
    by using the pen and filled by using the brush that are defined in the
    playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    

class WmfRegion(aspose.imaging.fileformats.emf.MetaObject):
    '''The Region Object defines a potentially non-rectilinear shape defined by
    an array of scanlines.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def next_in_chain(self) -> int:
        '''Gets the next in chain.'''
        raise NotImplementedError()
    
    @next_in_chain.setter
    def next_in_chain(self, value : int) -> None:
        '''Sets the next in chain.'''
        raise NotImplementedError()
    
    @property
    def object_type(self) -> int:
        '''Gets the type of the object.'''
        raise NotImplementedError()
    
    @object_type.setter
    def object_type(self, value : int) -> None:
        '''Sets the type of the object.'''
        raise NotImplementedError()
    
    @property
    def object_count(self) -> int:
        '''Gets the object count.'''
        raise NotImplementedError()
    
    @object_count.setter
    def object_count(self, value : int) -> None:
        '''Sets the object count.'''
        raise NotImplementedError()
    
    @property
    def region_size(self) -> int:
        '''Gets the size of the region.'''
        raise NotImplementedError()
    
    @region_size.setter
    def region_size(self, value : int) -> None:
        '''Sets the size of the region.'''
        raise NotImplementedError()
    
    @property
    def scan_count(self) -> int:
        '''Gets the scan count.'''
        raise NotImplementedError()
    
    @scan_count.setter
    def scan_count(self, value : int) -> None:
        '''Sets the scan count.'''
        raise NotImplementedError()
    
    @property
    def max_scan(self) -> int:
        '''Gets the maximum scan.'''
        raise NotImplementedError()
    
    @max_scan.setter
    def max_scan(self, value : int) -> None:
        '''Sets the maximum scan.'''
        raise NotImplementedError()
    
    @property
    def bounding_rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the bounding rectangle.'''
        raise NotImplementedError()
    
    @bounding_rectangle.setter
    def bounding_rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the bounding rectangle.'''
        raise NotImplementedError()
    
    @property
    def a_scans(self) -> List[aspose.imaging.fileformats.wmf.objects.WmfScanObject]:
        '''Gets a scans.'''
        raise NotImplementedError()
    
    @a_scans.setter
    def a_scans(self, value : List[aspose.imaging.fileformats.wmf.objects.WmfScanObject]) -> None:
        '''Sets a scans.'''
        raise NotImplementedError()
    

class WmfResizePalette(WmfObject):
    '''The META_RESIZEPALETTE record redefines the size of the logical palette
    that is defined in the playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def number_of_entries(self) -> int:
        '''Gets the number of entries.'''
        raise NotImplementedError()
    
    @number_of_entries.setter
    def number_of_entries(self, value : int) -> None:
        '''Sets the number of entries.'''
        raise NotImplementedError()
    

class WmfRestoreDc(WmfObject):
    '''The restore DC object'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def n_saved_dc(self) -> int:
        '''Gets the n saved dc.'''
        raise NotImplementedError()
    
    @n_saved_dc.setter
    def n_saved_dc(self, value : int) -> None:
        '''Sets the n saved dc.'''
        raise NotImplementedError()
    

class WmfRoundRect(WmfRectangle):
    '''The rectangle object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the rectangle.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    

class WmfSaveDc(WmfObject):
    '''The META_SAVEDC record saves the playback device context for later
    retrieval.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    

class WmfScaleViewportExt(WmfScaleWindowExt):
    '''The META_SCALEVIEWPORTEXT record scales the horizontal and vertical
    extents of the viewport that is defined in the playback device context
    by using the ratios formed by the specified multiplicands and divisors.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def y_denom(self) -> int:
        '''Gets the y denom.'''
        raise NotImplementedError()
    
    @y_denom.setter
    def y_denom(self, value : int) -> None:
        '''Sets the y denom.'''
        raise NotImplementedError()
    
    @property
    def y_num(self) -> int:
        '''Gets the y num.'''
        raise NotImplementedError()
    
    @y_num.setter
    def y_num(self, value : int) -> None:
        '''Sets the y num.'''
        raise NotImplementedError()
    
    @property
    def x_denom(self) -> int:
        '''Gets the x denom.'''
        raise NotImplementedError()
    
    @x_denom.setter
    def x_denom(self, value : int) -> None:
        '''Sets the x denom.'''
        raise NotImplementedError()
    
    @property
    def x_num(self) -> int:
        '''Gets the x number.'''
        raise NotImplementedError()
    
    @x_num.setter
    def x_num(self, value : int) -> None:
        '''Sets the x number.'''
        raise NotImplementedError()
    

class WmfScaleWindowExt(WmfObject):
    '''The META_SCALEWINDOWEXT record scales the horizontal and vertical
    extents of the output window that is defined in the playback device
    context by using the ratios formed by specified multiplicands and
    divisors.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def y_denom(self) -> int:
        '''Gets the y denom.'''
        raise NotImplementedError()
    
    @y_denom.setter
    def y_denom(self, value : int) -> None:
        '''Sets the y denom.'''
        raise NotImplementedError()
    
    @property
    def y_num(self) -> int:
        '''Gets the y num.'''
        raise NotImplementedError()
    
    @y_num.setter
    def y_num(self, value : int) -> None:
        '''Sets the y num.'''
        raise NotImplementedError()
    
    @property
    def x_denom(self) -> int:
        '''Gets the x denom.'''
        raise NotImplementedError()
    
    @x_denom.setter
    def x_denom(self, value : int) -> None:
        '''Sets the x denom.'''
        raise NotImplementedError()
    
    @property
    def x_num(self) -> int:
        '''Gets the x number.'''
        raise NotImplementedError()
    
    @x_num.setter
    def x_num(self, value : int) -> None:
        '''Sets the x number.'''
        raise NotImplementedError()
    

class WmfScanObject(aspose.imaging.fileformats.emf.MetaObject):
    '''The Scan Object specifies a collection of scanlines.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count.'''
        raise NotImplementedError()
    
    @count.setter
    def count(self, value : int) -> None:
        '''Sets the count.'''
        raise NotImplementedError()
    
    @property
    def top(self) -> int:
        '''Gets the top.'''
        raise NotImplementedError()
    
    @top.setter
    def top(self, value : int) -> None:
        '''Sets the top.'''
        raise NotImplementedError()
    
    @property
    def bottom(self) -> int:
        '''Gets the bottom.'''
        raise NotImplementedError()
    
    @bottom.setter
    def bottom(self, value : int) -> None:
        '''Sets the bottom.'''
        raise NotImplementedError()
    
    @property
    def scan_lines(self) -> List[aspose.imaging.Point]:
        '''Gets the scan lines.'''
        raise NotImplementedError()
    
    @scan_lines.setter
    def scan_lines(self, value : List[aspose.imaging.Point]) -> None:
        '''Sets the scan lines.'''
        raise NotImplementedError()
    
    @property
    def count2(self) -> int:
        '''Gets the count2.'''
        raise NotImplementedError()
    
    @count2.setter
    def count2(self, value : int) -> None:
        '''Sets the count2.'''
        raise NotImplementedError()
    

class WmfSelectClipRegion(WmfObject):
    '''The META_SELECTCLIPREGION record specifies a Region Object (section 2.2.1.5) to be the current clipping region.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfSelectClipRegion` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, region : aspose.imaging.fileformats.wmf.objects.WmfGraphicObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfSelectClipRegion` class.
        
        :param region: The region.'''
        raise NotImplementedError()
    
    @property
    def object_index(self) -> int:
        '''Gets the index of the object.'''
        raise NotImplementedError()
    
    @object_index.setter
    def object_index(self, value : int) -> None:
        '''Sets the index of the object.'''
        raise NotImplementedError()
    

class WmfSelectObject(WmfObject):
    '''The select object.'''
    
    @overload
    def __init__(self, wmf_object : aspose.imaging.fileformats.wmf.objects.WmfGraphicObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfSelectObject` class.
        
        :param wmf_object: The WMF object.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.wmf.objects.WmfSelectObject` class.'''
        raise NotImplementedError()
    
    @property
    def object_index(self) -> int:
        '''Gets the index of the object.'''
        raise NotImplementedError()
    
    @object_index.setter
    def object_index(self, value : int) -> None:
        '''Sets the index of the object.'''
        raise NotImplementedError()
    

class WmfSelectPalette(WmfObject):
    '''The META_SELECTPALETTE record defines the current logical palette with a
    specified Palette Object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def object_index(self) -> int:
        '''Gets the index of the object.'''
        raise NotImplementedError()
    
    @object_index.setter
    def object_index(self, value : int) -> None:
        '''Sets the index of the object.'''
        raise NotImplementedError()
    

class WmfSetBkColor(WmfObject):
    '''The META_SETBKCOLOR record sets the background color in the playback
    device context to a specified color, or to the nearest physical color if
    the device cannot represent the specified color.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def color_ref(self) -> int:
        '''Gets the color reference.'''
        raise NotImplementedError()
    
    @color_ref.setter
    def color_ref(self, value : int) -> None:
        '''Sets the color reference.'''
        raise NotImplementedError()
    

class WmfSetBkMode(WmfObject):
    '''The set bk mode.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def bk_mode(self) -> aspose.imaging.fileformats.wmf.consts.WmfMixMode:
        '''Gets the bk mode.'''
        raise NotImplementedError()
    
    @bk_mode.setter
    def bk_mode(self, value : aspose.imaging.fileformats.wmf.consts.WmfMixMode) -> None:
        '''Sets the bk mode.'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets the reserved.'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets the reserved.'''
        raise NotImplementedError()
    

class WmfSetDibToDev(WmfObject):
    '''The META_SETDIBTODEV record sets a block of pixels in the playback
    device context using device-independent color data. The source of the
    color data is a DIB.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def color_usage(self) -> aspose.imaging.fileformats.wmf.consts.WmfColorUsageEnum:
        '''Gets the color usage.'''
        raise NotImplementedError()
    
    @color_usage.setter
    def color_usage(self, value : aspose.imaging.fileformats.wmf.consts.WmfColorUsageEnum) -> None:
        '''Sets the color usage.'''
        raise NotImplementedError()
    
    @property
    def scan_count(self) -> int:
        '''Gets the scan count.'''
        raise NotImplementedError()
    
    @scan_count.setter
    def scan_count(self, value : int) -> None:
        '''Sets the scan count.'''
        raise NotImplementedError()
    
    @property
    def start_scan(self) -> int:
        '''Gets the start scan.'''
        raise NotImplementedError()
    
    @start_scan.setter
    def start_scan(self, value : int) -> None:
        '''Sets the start scan.'''
        raise NotImplementedError()
    
    @property
    def dib_pos(self) -> aspose.imaging.Point:
        '''Gets the dib position.'''
        raise NotImplementedError()
    
    @dib_pos.setter
    def dib_pos(self, value : aspose.imaging.Point) -> None:
        '''Sets the dib position.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    
    @property
    def dest_pos(self) -> aspose.imaging.Point:
        '''Gets the dest position.'''
        raise NotImplementedError()
    
    @dest_pos.setter
    def dest_pos(self, value : aspose.imaging.Point) -> None:
        '''Sets the dest position.'''
        raise NotImplementedError()
    
    @property
    def dib(self) -> aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap:
        '''Gets the dib.'''
        raise NotImplementedError()
    
    @dib.setter
    def dib(self, value : aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap) -> None:
        '''Sets the dib.'''
        raise NotImplementedError()
    

class WmfSetLayout(WmfObject):
    '''The META_SETLAYOUT record defines the layout orientation in the playback
    device context. The layout orientation determines the direction in which
    text and graphics are drawn'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def layout_mode(self) -> Aspose.Imaging.FileFormats.Emf.Emf.Records.EmfSetLayout+LayoutModeEnum:
        '''Gets the LayoutMode.'''
        raise NotImplementedError()
    
    @layout_mode.setter
    def layout_mode(self, value : Aspose.Imaging.FileFormats.Emf.Emf.Records.EmfSetLayout+LayoutModeEnum) -> None:
        '''Sets the LayoutMode.'''
        raise NotImplementedError()
    

class WmfSetMapMode(WmfObject):
    '''The set map mode.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def map_mode(self) -> aspose.imaging.fileformats.wmf.consts.WmfMapMode:
        '''Gets the map mode.'''
        raise NotImplementedError()
    
    @map_mode.setter
    def map_mode(self, value : aspose.imaging.fileformats.wmf.consts.WmfMapMode) -> None:
        '''Sets the map mode.'''
        raise NotImplementedError()
    

class WmfSetMapperFlags(WmfObject):
    '''The META_SETMAPPERFLAGS record defines the algorithm that the font
    mapper uses when it maps logical fonts to physical fonts.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def mapper_values(self) -> int:
        '''Gets the mapper values.'''
        raise NotImplementedError()
    
    @mapper_values.setter
    def mapper_values(self, value : int) -> None:
        '''Sets the mapper values.'''
        raise NotImplementedError()
    

class WmfSetPalentries(WmfObject):
    '''The META_SETPALENTRIES record defines RGB color values in a range of
    entries in the logical palette that is defined in the playback device
    context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def log_palette(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfLogPalette:
        '''Gets the log palette.'''
        raise NotImplementedError()
    
    @log_palette.setter
    def log_palette(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfLogPalette) -> None:
        '''Sets the log palette.'''
        raise NotImplementedError()
    
    @property
    def start(self) -> int:
        '''Gets the start.'''
        raise NotImplementedError()
    
    @start.setter
    def start(self, value : int) -> None:
        '''Sets the start.'''
        raise NotImplementedError()
    

class WmfSetPixel(WmfPointObject):
    '''The META_SETPIXEL record sets the pixel at the specified coordinates to
    the specified color.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    
    @property
    def color_ref(self) -> int:
        '''Gets the color reference.'''
        raise NotImplementedError()
    
    @color_ref.setter
    def color_ref(self, value : int) -> None:
        '''Sets the color reference.'''
        raise NotImplementedError()
    

class WmfSetPolyFillMode(WmfObject):
    '''The set poly fill mode.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def poly_fill_mode(self) -> aspose.imaging.fileformats.wmf.consts.WmfPolyFillMode:
        '''Gets the poly fill mode.'''
        raise NotImplementedError()
    
    @poly_fill_mode.setter
    def poly_fill_mode(self, value : aspose.imaging.fileformats.wmf.consts.WmfPolyFillMode) -> None:
        '''Sets the poly fill mode.'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets the reserved.'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets the reserved.'''
        raise NotImplementedError()
    

class WmfSetRelabs(WmfObject):
    '''The META_SETRELABS record is reserved and not supported.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def parameters(self) -> List[int]:
        '''Gets the parameter.'''
        raise NotImplementedError()
    
    @parameters.setter
    def parameters(self, value : List[int]) -> None:
        '''Sets the parameter.'''
        raise NotImplementedError()
    

class WmfSetRop2(WmfObject):
    '''The set rop2'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def draw_mode(self) -> aspose.imaging.fileformats.wmf.consts.WmfBinaryRasterOperation:
        '''Gets the draw mode.'''
        raise NotImplementedError()
    
    @draw_mode.setter
    def draw_mode(self, value : aspose.imaging.fileformats.wmf.consts.WmfBinaryRasterOperation) -> None:
        '''Sets the draw mode.'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets the reserved.'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets the reserved.'''
        raise NotImplementedError()
    

class WmfSetStretchbltMode(WmfObject):
    '''The META_SETSTRETCHBLTMODE record defines the bitmap stretching mode in
    the playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def stretch_mode(self) -> aspose.imaging.fileformats.wmf.consts.StretchMode:
        '''Gets the stretch mode.'''
        raise NotImplementedError()
    
    @stretch_mode.setter
    def stretch_mode(self, value : aspose.imaging.fileformats.wmf.consts.StretchMode) -> None:
        '''Sets the stretch mode.'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets the reserved.'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets the reserved.'''
        raise NotImplementedError()
    

class WmfSetTextAlign(WmfObject):
    '''The Set text align'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def text_align(self) -> aspose.imaging.fileformats.wmf.consts.WmfTextAlignmentModeFlags:
        '''Gets the text align.'''
        raise NotImplementedError()
    
    @text_align.setter
    def text_align(self, value : aspose.imaging.fileformats.wmf.consts.WmfTextAlignmentModeFlags) -> None:
        '''Sets the text align.'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets the reserved.'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets the reserved.'''
        raise NotImplementedError()
    

class WmfSetTextCharExtra(WmfObject):
    '''The META_SETTEXTCHAREXTRA record defines inter-character spacing for
    text justification in the playback device context. Spacing is added to
    the white space between each character, including
    characters, when a line of justified text is
    output.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def char_extra(self) -> int:
        '''Gets the character extra.'''
        raise NotImplementedError()
    
    @char_extra.setter
    def char_extra(self, value : int) -> None:
        '''Sets the character extra.'''
        raise NotImplementedError()
    

class WmfSetTextColor(WmfObject):
    '''The Set text color.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def color_ref(self) -> int:
        '''Gets the color reference.'''
        raise NotImplementedError()
    
    @color_ref.setter
    def color_ref(self, value : int) -> None:
        '''Sets the color reference.'''
        raise NotImplementedError()
    
    @property
    def extended_byte(self) -> int:
        '''Gets the extended byte.'''
        raise NotImplementedError()
    
    @extended_byte.setter
    def extended_byte(self, value : int) -> None:
        '''Sets the extended byte.'''
        raise NotImplementedError()
    

class WmfSetTextJustification(WmfObject):
    '''The META_SETTEXTJUSTIFICATION record defines the amount of space to add
    to  characters in a string of justified text.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def break_count(self) -> int:
        '''Gets the  count.'''
        raise NotImplementedError()
    
    @break_count.setter
    def break_count(self, value : int) -> None:
        '''Sets the  count.'''
        raise NotImplementedError()
    
    @property
    def break_extra(self) -> int:
        '''Gets the  extra.'''
        raise NotImplementedError()
    
    @break_extra.setter
    def break_extra(self, value : int) -> None:
        '''Sets the  extra.'''
        raise NotImplementedError()
    

class WmfSetViewportExt(WmfPointObject):
    '''The META_SETVIEWPORTEXT record sets the horizontal and vertical extents
    of the viewport in the playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfSetViewportOrg(WmfPointObject):
    '''The META_SETVIEWPORTORG record defines the viewport origin in the
    playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfSetWindowExt(WmfPointObject):
    '''The set window object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfSetWindowOrg(WmfPointObject):
    '''The set window org object'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    

class WmfStretchBlt(WmfObject):
    '''The META_STRETCHBLT record specifies the transfer of a block of pixels
    according to a raster operation, with possible expansion or contraction.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def raster_operation(self) -> aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation:
        '''Gets the raster operation.'''
        raise NotImplementedError()
    
    @raster_operation.setter
    def raster_operation(self, value : aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation) -> None:
        '''Sets the raster operation.'''
        raise NotImplementedError()
    
    @property
    def src_height(self) -> int:
        '''Gets the height of the source.'''
        raise NotImplementedError()
    
    @src_height.setter
    def src_height(self, value : int) -> None:
        '''Sets the height of the source.'''
        raise NotImplementedError()
    
    @property
    def src_width(self) -> int:
        '''Gets the width of the source.'''
        raise NotImplementedError()
    
    @src_width.setter
    def src_width(self, value : int) -> None:
        '''Sets the width of the source.'''
        raise NotImplementedError()
    
    @property
    def src_position(self) -> aspose.imaging.Point:
        '''Gets the source position.'''
        raise NotImplementedError()
    
    @src_position.setter
    def src_position(self, value : aspose.imaging.Point) -> None:
        '''Sets the source position.'''
        raise NotImplementedError()
    
    @property
    def dest_height(self) -> int:
        '''Gets the height of the dest.'''
        raise NotImplementedError()
    
    @dest_height.setter
    def dest_height(self, value : int) -> None:
        '''Sets the height of the dest.'''
        raise NotImplementedError()
    
    @property
    def dest_width(self) -> int:
        '''Gets the width of the dest.'''
        raise NotImplementedError()
    
    @dest_width.setter
    def dest_width(self, value : int) -> None:
        '''Sets the width of the dest.'''
        raise NotImplementedError()
    
    @property
    def dst_position(self) -> aspose.imaging.Point:
        '''Gets the DST position.'''
        raise NotImplementedError()
    
    @dst_position.setter
    def dst_position(self, value : aspose.imaging.Point) -> None:
        '''Sets the DST position.'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets the reserved.'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets the reserved.'''
        raise NotImplementedError()
    
    @property
    def bitmap(self) -> aspose.imaging.fileformats.wmf.objects.WmfBitmap16:
        '''Gets the bitmap.'''
        raise NotImplementedError()
    
    @bitmap.setter
    def bitmap(self, value : aspose.imaging.fileformats.wmf.objects.WmfBitmap16) -> None:
        '''Sets the bitmap.'''
        raise NotImplementedError()
    

class WmfStretchDib(WmfObject):
    '''The wmf Stretch DIB objetc.'''
    
    def __init__(self) -> None:
        '''WMFs the record.'''
        raise NotImplementedError()
    
    @property
    def raster_operation(self) -> aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation:
        '''Gets the raster operation.'''
        raise NotImplementedError()
    
    @raster_operation.setter
    def raster_operation(self, value : aspose.imaging.fileformats.wmf.consts.WmfTernaryRasterOperation) -> None:
        '''Sets the raster operation.'''
        raise NotImplementedError()
    
    @property
    def color_usage(self) -> aspose.imaging.fileformats.wmf.consts.WmfColorUsageEnum:
        '''Gets the color usage.'''
        raise NotImplementedError()
    
    @color_usage.setter
    def color_usage(self, value : aspose.imaging.fileformats.wmf.consts.WmfColorUsageEnum) -> None:
        '''Sets the color usage.'''
        raise NotImplementedError()
    
    @property
    def src_height(self) -> int:
        '''Gets the height of the source.'''
        raise NotImplementedError()
    
    @src_height.setter
    def src_height(self, value : int) -> None:
        '''Sets the height of the source.'''
        raise NotImplementedError()
    
    @property
    def src_width(self) -> int:
        '''Gets the width of the source.'''
        raise NotImplementedError()
    
    @src_width.setter
    def src_width(self, value : int) -> None:
        '''Sets the width of the source.'''
        raise NotImplementedError()
    
    @property
    def y_src(self) -> int:
        '''Gets the y source.'''
        raise NotImplementedError()
    
    @y_src.setter
    def y_src(self, value : int) -> None:
        '''Sets the y source.'''
        raise NotImplementedError()
    
    @property
    def x_src(self) -> int:
        '''Gets the x source.'''
        raise NotImplementedError()
    
    @x_src.setter
    def x_src(self, value : int) -> None:
        '''Sets the x source.'''
        raise NotImplementedError()
    
    @property
    def dest_height(self) -> int:
        '''Gets the height of the dest.'''
        raise NotImplementedError()
    
    @dest_height.setter
    def dest_height(self, value : int) -> None:
        '''Sets the height of the dest.'''
        raise NotImplementedError()
    
    @property
    def dest_width(self) -> int:
        '''Gets the width of the dest.'''
        raise NotImplementedError()
    
    @dest_width.setter
    def dest_width(self, value : int) -> None:
        '''Sets the width of the dest.'''
        raise NotImplementedError()
    
    @property
    def y_dest(self) -> int:
        '''Gets the y dest.'''
        raise NotImplementedError()
    
    @y_dest.setter
    def y_dest(self, value : int) -> None:
        '''Sets the y dest.'''
        raise NotImplementedError()
    
    @property
    def x_dest(self) -> int:
        '''Gets the x dest.'''
        raise NotImplementedError()
    
    @x_dest.setter
    def x_dest(self, value : int) -> None:
        '''Sets the x dest.'''
        raise NotImplementedError()
    
    @property
    def source_bitmap(self) -> aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap:
        '''Gets the source bitmap.'''
        raise NotImplementedError()
    
    @source_bitmap.setter
    def source_bitmap(self, value : aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap) -> None:
        '''Sets the source bitmap.'''
        raise NotImplementedError()
    

class WmfTextOut(WmfExtTextOut):
    '''The META_EXTTEXTOUT record outputs text by using the font, background
    color, and text color that are defined in the playback device context.
    Optionally, dimensions can be provided for clipping, opaquing, or both.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def point(self) -> aspose.imaging.Point:
        '''Gets the point.'''
        raise NotImplementedError()
    
    @point.setter
    def point(self, value : aspose.imaging.Point) -> None:
        '''Sets the point.'''
        raise NotImplementedError()
    
    @property
    def string_length(self) -> int:
        '''Gets the length of the string.'''
        raise NotImplementedError()
    
    @string_length.setter
    def string_length(self, value : int) -> None:
        '''Sets the length of the string.'''
        raise NotImplementedError()
    
    @property
    def fw_opts(self) -> int:
        '''Gets the fw opts.'''
        raise NotImplementedError()
    
    @fw_opts.setter
    def fw_opts(self, value : int) -> None:
        '''Sets the fw opts.'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets the rectangle.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
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
    
    @property
    def dx(self) -> List[int]:
        '''Gets the dx.'''
        raise NotImplementedError()
    
    @dx.setter
    def dx(self, value : List[int]) -> None:
        '''Sets the dx.'''
        raise NotImplementedError()
    
    @property
    def extended_byte(self) -> int:
        '''Gets the extended byte.'''
        raise NotImplementedError()
    
    @extended_byte.setter
    def extended_byte(self, value : int) -> None:
        '''Sets the extended byte.'''
        raise NotImplementedError()
    

class WmfUntyped(WmfObject):
    '''The wmf untyped object'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def parameters(self) -> List[int]:
        '''Gets the parameters.'''
        raise NotImplementedError()
    
    @parameters.setter
    def parameters(self, value : List[int]) -> None:
        '''Sets the parameters.'''
        raise NotImplementedError()
    

