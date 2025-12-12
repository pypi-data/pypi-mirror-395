"""The namespace contains types [MS-EMF]: Enhanced Metafile Format.
            2.2 EMF Objects"""
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

class EmfBasePen(EmfObject):
    '''The base pen object'''
    
    @property
    def pen_style(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfPenStyle:
        '''Gets the pen style.'''
        raise NotImplementedError()
    
    @pen_style.setter
    def pen_style(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfPenStyle) -> None:
        '''Sets the pen style.'''
        raise NotImplementedError()
    
    @property
    def argb_32_color_ref(self) -> int:
        '''Gets the 32-bit ARGB color reference.'''
        raise NotImplementedError()
    
    @argb_32_color_ref.setter
    def argb_32_color_ref(self, value : int) -> None:
        '''Sets the 32-bit ARGB color reference.'''
        raise NotImplementedError()
    

class EmfBitFix28To4(EmfObject):
    '''The BitFIX28_4 object defines a numeric value in 28.4 bit FIX notation.'''
    
    def __init__(self, dword_data : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfBitFix28To4` class.
        
        :param dword_data: The dword data.'''
        raise NotImplementedError()
    
    @property
    def int_val(self) -> int:
        '''Gets the integer value value'''
        raise NotImplementedError()
    
    @int_val.setter
    def int_val(self, value : int) -> None:
        '''Sets the integer value value'''
        raise NotImplementedError()
    
    @property
    def frac_value(self) -> int:
        '''Gets the fraction value'''
        raise NotImplementedError()
    
    @frac_value.setter
    def frac_value(self, value : int) -> None:
        '''Sets the fraction value'''
        raise NotImplementedError()
    
    @property
    def value(self) -> float:
        '''Gets the resulting float value;'''
        raise NotImplementedError()
    

class EmfColorAdjustment(EmfObject):
    '''The ColorAdjustment object defines values for adjusting the colors in source bitmaps in bit-block transfers.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the size in bytes of this object. This MUST be 0x0018.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the size in bytes of this object. This MUST be 0x0018.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfColorAdjustmentEnum:
        '''Gets a 16-bit unsigned integer that specifies how to prepare the output image. This field can be
        set to NULL or to any combination of values in the ColorAdjustment enumeration (section 2.1.5).'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfColorAdjustmentEnum) -> None:
        '''Sets a 16-bit unsigned integer that specifies how to prepare the output image. This field can be
        set to NULL or to any combination of values in the ColorAdjustment enumeration (section 2.1.5).'''
        raise NotImplementedError()
    
    @property
    def illuminant_index(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfIlluminant:
        '''Gets a 16-bit unsigned integer that specifies the type of standard light source under which the
        image is viewed, from the Illuminant enumeration (section 2.1.19).'''
        raise NotImplementedError()
    
    @illuminant_index.setter
    def illuminant_index(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfIlluminant) -> None:
        '''Sets a 16-bit unsigned integer that specifies the type of standard light source under which the
        image is viewed, from the Illuminant enumeration (section 2.1.19).'''
        raise NotImplementedError()
    
    @property
    def red_gamma(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the nth power gamma correction value for the red
        primary of the source colors. This value SHOULD be in the range from 2,500 to 65,000.
        A value of 10,000 means gamma correction MUST NOT be performed.'''
        raise NotImplementedError()
    
    @red_gamma.setter
    def red_gamma(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the nth power gamma correction value for the red
        primary of the source colors. This value SHOULD be in the range from 2,500 to 65,000.
        A value of 10,000 means gamma correction MUST NOT be performed.'''
        raise NotImplementedError()
    
    @property
    def green_gamma(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the nth power gamma correction value for the green
        primary of the source colors. This value SHOULD be in the range from 2,500 to 65,000.
        A value of 10,000 means gamma correction MUST NOT be performed.'''
        raise NotImplementedError()
    
    @green_gamma.setter
    def green_gamma(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the nth power gamma correction value for the green
        primary of the source colors. This value SHOULD be in the range from 2,500 to 65,000.
        A value of 10,000 means gamma correction MUST NOT be performed.'''
        raise NotImplementedError()
    
    @property
    def blue_gamma(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the nth power gamma correction value for the
        blue primary of the source colors. This value SHOULD be in the range from 2,500 to 65,000.
        A value of 10,000 means gamma correction MUST NOT be performed.'''
        raise NotImplementedError()
    
    @blue_gamma.setter
    def blue_gamma(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the nth power gamma correction value for the
        blue primary of the source colors. This value SHOULD be in the range from 2,500 to 65,000.
        A value of 10,000 means gamma correction MUST NOT be performed.'''
        raise NotImplementedError()
    
    @property
    def reference_black(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the black reference for the source colors.
        Any colors that are darker than this are treated as black.
        This value SHOULD be in the range from zero to 4,000'''
        raise NotImplementedError()
    
    @reference_black.setter
    def reference_black(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the black reference for the source colors.
        Any colors that are darker than this are treated as black.
        This value SHOULD be in the range from zero to 4,000'''
        raise NotImplementedError()
    
    @property
    def reference_white(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the white reference for the source colors.
        Any colors that are lighter than this are treated as white.
        This value SHOULD be in the range from 6,000 to 10,000.'''
        raise NotImplementedError()
    
    @reference_white.setter
    def reference_white(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the white reference for the source colors.
        Any colors that are lighter than this are treated as white.
        This value SHOULD be in the range from 6,000 to 10,000.'''
        raise NotImplementedError()
    
    @property
    def contrast(self) -> int:
        '''Gets a 16-bit signed integer that specifies the amount of contrast to be applied to the source object.
        This value SHOULD be in the range from –100 to 100. A value of zero means contrast adjustment MUST NOT be performed.'''
        raise NotImplementedError()
    
    @contrast.setter
    def contrast(self, value : int) -> None:
        '''Sets a 16-bit signed integer that specifies the amount of contrast to be applied to the source object.
        This value SHOULD be in the range from –100 to 100. A value of zero means contrast adjustment MUST NOT be performed.'''
        raise NotImplementedError()
    
    @property
    def brightness(self) -> int:
        '''Gets a 16-bit signed integer that specifies the amount of brightness to be applied to the source object.
        This value SHOULD be in the range from –100 to 100.
        A value of zero means brightness adjustment MUST NOT be performed.'''
        raise NotImplementedError()
    
    @brightness.setter
    def brightness(self, value : int) -> None:
        '''Sets a 16-bit signed integer that specifies the amount of brightness to be applied to the source object.
        This value SHOULD be in the range from –100 to 100.
        A value of zero means brightness adjustment MUST NOT be performed.'''
        raise NotImplementedError()
    
    @property
    def colorfullness(self) -> int:
        '''Gets a 16-bit signed integer that specifies the amount of colorfulness to be applied to the source object.
        This value SHOULD be in the range from –100 to 100.
        A value of zero means colorfulness adjustment MUST NOT be performed'''
        raise NotImplementedError()
    
    @colorfullness.setter
    def colorfullness(self, value : int) -> None:
        '''Sets a 16-bit signed integer that specifies the amount of colorfulness to be applied to the source object.
        This value SHOULD be in the range from –100 to 100.
        A value of zero means colorfulness adjustment MUST NOT be performed'''
        raise NotImplementedError()
    
    @property
    def red_green_tint(self) -> int:
        '''Gets 16-bit signed integer that specifies the amount of red or green tint adjustment to be applied
        to the source object. This value SHOULD be in the range from –100 to 100.
        Positive numbers adjust towards red and negative numbers adjust towards green.
        A value of zero means tint adjustment MUST NOT be performed'''
        raise NotImplementedError()
    
    @red_green_tint.setter
    def red_green_tint(self, value : int) -> None:
        '''Sets 16-bit signed integer that specifies the amount of red or green tint adjustment to be applied
        to the source object. This value SHOULD be in the range from –100 to 100.
        Positive numbers adjust towards red and negative numbers adjust towards green.
        A value of zero means tint adjustment MUST NOT be performed'''
        raise NotImplementedError()
    

class EmfDesignVector(EmfObject):
    '''The DesignVector (section 2.2.3) object defines the design vector, which specifies values for the font axes of a multiple master font.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def signature(self) -> int:
        '''Gets a 32-bit unsigned integer that MUST be set to the value 0x08007664.'''
        raise NotImplementedError()
    
    @signature.setter
    def signature(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that MUST be set to the value 0x08007664.'''
        raise NotImplementedError()
    
    @property
    def num_axes(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of elements in
        the Values array. It MUST be in the range 0 to 16, inclusive'''
        raise NotImplementedError()
    
    @num_axes.setter
    def num_axes(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of elements in
        the Values array. It MUST be in the range 0 to 16, inclusive'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets an optional array of 32-bit signed integers that specify the values
        of the font axes of a multiple master, OpenType font. The maximum number of values in the array is 16.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets an optional array of 32-bit signed integers that specify the values
        of the font axes of a multiple master, OpenType font. The maximum number of values in the array is 16.'''
        raise NotImplementedError()
    

class EmfEpsData(EmfObject):
    '''The EpsData object is a container for EPS data'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def size_data(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the total size of this object, in bytes'''
        raise NotImplementedError()
    
    @size_data.setter
    def size_data(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the total size of this object, in bytes'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the PostScript language level. This
        value MUST be 0x00000001'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the PostScript language level. This
        value MUST be 0x00000001'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.fileformats.emf.emf.objects.EmfPoint28To4]:
        '''Gets an array of three Point28_4 objects (section 2.2.23) that defines the
        coordinates of the output parallelogram using 28.4 bit FIX notation'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.fileformats.emf.emf.objects.EmfPoint28To4]) -> None:
        '''Sets an array of three Point28_4 objects (section 2.2.23) that defines the
        coordinates of the output parallelogram using 28.4 bit FIX notation'''
        raise NotImplementedError()
    
    @property
    def post_script_data(self) -> List[int]:
        '''Gets an array of bytes of PostScript data. The length of this array can
        be computed from the SizeData field. This data MAY be used to render an image.'''
        raise NotImplementedError()
    
    @post_script_data.setter
    def post_script_data(self, value : List[int]) -> None:
        '''Sets an array of bytes of PostScript data. The length of this array can
        be computed from the SizeData field. This data MAY be used to render an image.'''
        raise NotImplementedError()
    

class EmfFormat(EmfObject):
    '''The EmrFormat object contains information that identifies the format of image data in an
    EMR_COMMENT_MULTIFORMATS record(section 2.3.3.4.3).'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def signature(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfFormatSignature:
        '''Gets a 32-bit unsigned integer that specifies the format of the image data.
        This value MUST be in the FormatSignature enumeration (section 2.1.14).'''
        raise NotImplementedError()
    
    @signature.setter
    def signature(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfFormatSignature) -> None:
        '''Sets a 32-bit unsigned integer that specifies the format of the image data.
        This value MUST be in the FormatSignature enumeration (section 2.1.14).'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the format version number.
        If the Signature field specifies encapsulated PostScript (EPS),
        this value MUST be 0x00000001; otherwise, this value MUST be ignored'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the format version number.
        If the Signature field specifies encapsulated PostScript (EPS),
        this value MUST be 0x00000001; otherwise, this value MUST be ignored'''
        raise NotImplementedError()
    
    @property
    def size_data(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the size of the data in bytes'''
        raise NotImplementedError()
    
    @size_data.setter
    def size_data(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the size of the data in bytes'''
        raise NotImplementedError()
    
    @property
    def off_data(self) -> int:
        '''Gets 32-bit unsigned integer that specifies the offset to the data from the
        start of the identifier field in an EMR_COMMENT_PUBLIC record (section 2.3.3.4).
        The offset MUST be 32-bit aligned.'''
        raise NotImplementedError()
    
    @off_data.setter
    def off_data(self, value : int) -> None:
        '''Sets 32-bit unsigned integer that specifies the offset to the data from the
        start of the identifier field in an EMR_COMMENT_PUBLIC record (section 2.3.3.4).
        The offset MUST be 32-bit aligned.'''
        raise NotImplementedError()
    

class EmfGradientRectangle(EmfObject):
    '''The GradientRectangle object defines a rectangle using TriVertex objects (section 2.2.26) in an
    EMR_GRADIENTFILL record (section 2.3.5.12).'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def upper_left(self) -> int:
        '''Gets an index into an array of TriVertex objects that specifies the upper-left
        vertex of a rectangle. The index MUST be smaller than the size of the array, as defined by the
        nVer field of the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    
    @upper_left.setter
    def upper_left(self, value : int) -> None:
        '''Sets an index into an array of TriVertex objects that specifies the upper-left
        vertex of a rectangle. The index MUST be smaller than the size of the array, as defined by the
        nVer field of the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    
    @property
    def lower_right(self) -> int:
        '''Gets an index into an array of TriVertex objects that specifies the lower-right
        vertex of a rectangle. The index MUST be smaller than the size of the array, as defined by the
        nVer field of the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    
    @lower_right.setter
    def lower_right(self, value : int) -> None:
        '''Sets an index into an array of TriVertex objects that specifies the lower-right
        vertex of a rectangle. The index MUST be smaller than the size of the array, as defined by the
        nVer field of the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    

class EmfGradientTriangle(EmfObject):
    '''The GradientTriangle object defines a triangle using TriVertex objects (section 2.2.26) in an
    EMR_GRADIENTFILL record (section 2.3.5.12)'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def vertex1(self) -> int:
        '''Gets an index into an array of TriVertex objects that specifies a vertex of a
        triangle. The index MUST be smaller than the size of the array, as defined by the nVer field of
        the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    
    @vertex1.setter
    def vertex1(self, value : int) -> None:
        '''Sets an index into an array of TriVertex objects that specifies a vertex of a
        triangle. The index MUST be smaller than the size of the array, as defined by the nVer field of
        the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    
    @property
    def vertex2(self) -> int:
        '''Gets an index into an array of TriVertex objects that specifies a vertex of a
        triangle. The index MUST be smaller than the size of the array, as defined by the nVer field of
        the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    
    @vertex2.setter
    def vertex2(self, value : int) -> None:
        '''Sets an index into an array of TriVertex objects that specifies a vertex of a
        triangle. The index MUST be smaller than the size of the array, as defined by the nVer field of
        the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    
    @property
    def vertex3(self) -> int:
        '''Gets an index into an array of TriVertex objects that specifies a vertex of a
        triangle. The index MUST be smaller than the size of the array, as defined by the nVer field of
        the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    
    @vertex3.setter
    def vertex3(self, value : int) -> None:
        '''Sets an index into an array of TriVertex objects that specifies a vertex of a
        triangle. The index MUST be smaller than the size of the array, as defined by the nVer field of
        the EMR_GRADIENTFILL record.'''
        raise NotImplementedError()
    

class EmfHeaderExtension1(EmfHeaderObject):
    '''The HeaderExtension1 object defines the first extension to the EMF metafile header.
    It adds support for a PixelFormatDescriptor object (section 2.2.22) and OpenGL
    [OPENGL] records (section 2.3.9).'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfHeaderObject` class.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets a WMF RectL object ([MS-WMF] section 2.2.2.19) that specifies the rectangular inclusive-inclusive
        bounds in device units of the smallest rectangle that can be drawn around the image stored in
        the metafile'''
        raise NotImplementedError()
    
    @bounds.setter
    def bounds(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets a WMF RectL object ([MS-WMF] section 2.2.2.19) that specifies the rectangular inclusive-inclusive
        bounds in device units of the smallest rectangle that can be drawn around the image stored in
        the metafile'''
        raise NotImplementedError()
    
    @property
    def frame(self) -> aspose.imaging.Rectangle:
        '''Gets a WMF RectL object that specifies the rectangular inclusive-inclusive dimensions, in .01 millimeter
        units, of a rectangle that surrounds the image stored in the metafile'''
        raise NotImplementedError()
    
    @frame.setter
    def frame(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets a WMF RectL object that specifies the rectangular inclusive-inclusive dimensions, in .01 millimeter
        units, of a rectangle that surrounds the image stored in the metafile'''
        raise NotImplementedError()
    
    @property
    def record_signature(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfFormatSignature:
        '''Gets a 32-bit unsigned integer that specifies the record signature. This MUST be ENHMETA_SIGNATURE,
        from the FormatSignature enumeration (section 2.1.14).'''
        raise NotImplementedError()
    
    @record_signature.setter
    def record_signature(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfFormatSignature) -> None:
        '''Sets a 32-bit unsigned integer that specifies the record signature. This MUST be ENHMETA_SIGNATURE,
        from the FormatSignature enumeration (section 2.1.14).'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets Version (4 bytes): A 32-bit unsigned integer that specifies EMF metafile interoperability. This SHOULD be 0x00010000'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets Version (4 bytes): A 32-bit unsigned integer that specifies EMF metafile interoperability. This SHOULD be 0x00010000'''
        raise NotImplementedError()
    
    @property
    def bytes(self) -> int:
        '''Gets  32-bit unsigned integer that specifies the size of the metafile, in bytes.'''
        raise NotImplementedError()
    
    @bytes.setter
    def bytes(self, value : int) -> None:
        '''Sets  32-bit unsigned integer that specifies the size of the metafile, in bytes.'''
        raise NotImplementedError()
    
    @property
    def records(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of records in the metafile'''
        raise NotImplementedError()
    
    @records.setter
    def records(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of records in the metafile'''
        raise NotImplementedError()
    
    @property
    def handles(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the number of graphics objects that will be used during the processing of the metafile'''
        raise NotImplementedError()
    
    @handles.setter
    def handles(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the number of graphics objects that will be used during the processing of the metafile'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets a 16-bit unsigned integer that MUST be 0x0000 and MUST be ignored'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that MUST be 0x0000 and MUST be ignored'''
        raise NotImplementedError()
    
    @property
    def n_desription(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of characters in the array
        that contains the description of the metafile\'s contents. This is zero if there is no description string.'''
        raise NotImplementedError()
    
    @n_desription.setter
    def n_desription(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of characters in the array
        that contains the description of the metafile\'s contents. This is zero if there is no description string.'''
        raise NotImplementedError()
    
    @property
    def off_description(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the offset from the beginning of this
        record to the array that contains the description of the metafile\'s contents'''
        raise NotImplementedError()
    
    @off_description.setter
    def off_description(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the offset from the beginning of this
        record to the array that contains the description of the metafile\'s contents'''
        raise NotImplementedError()
    
    @property
    def n_pal_entries(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of entries in the metafile
        palette. The palette is located in the EMR_EOF record'''
        raise NotImplementedError()
    
    @n_pal_entries.setter
    def n_pal_entries(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of entries in the metafile
        palette. The palette is located in the EMR_EOF record'''
        raise NotImplementedError()
    
    @property
    def device(self) -> aspose.imaging.Size:
        '''Gets a WMF SizeL object ([MS-WMF] section 2.2.2.22) that specifies the size of the reference device, in pixels'''
        raise NotImplementedError()
    
    @device.setter
    def device(self, value : aspose.imaging.Size) -> None:
        '''Sets a WMF SizeL object ([MS-WMF] section 2.2.2.22) that specifies the size of the reference device, in pixels'''
        raise NotImplementedError()
    
    @property
    def millimeters(self) -> aspose.imaging.Size:
        '''Gets a WMF SizeL object that specifies the size of the reference device, in millimeters'''
        raise NotImplementedError()
    
    @millimeters.setter
    def millimeters(self, value : aspose.imaging.Size) -> None:
        '''Sets a WMF SizeL object that specifies the size of the reference device, in millimeters'''
        raise NotImplementedError()
    
    @property
    def valid(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfHeaderObject` is valid.'''
        raise NotImplementedError()
    
    @property
    def cb_pixel_format(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the size of the PixelFormatDescriptor object.
        This MUST be 0x00000000 if no pixel format is set'''
        raise NotImplementedError()
    
    @cb_pixel_format.setter
    def cb_pixel_format(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the size of the PixelFormatDescriptor object.
        This MUST be 0x00000000 if no pixel format is set'''
        raise NotImplementedError()
    
    @property
    def off_pixel_format(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the offset to the PixelFormatDescriptor object.
        This MUST be 0x00000000 if no pixel format is set.'''
        raise NotImplementedError()
    
    @off_pixel_format.setter
    def off_pixel_format(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the offset to the PixelFormatDescriptor object.
        This MUST be 0x00000000 if no pixel format is set.'''
        raise NotImplementedError()
    
    @property
    def b_open_gl(self) -> int:
        '''Gets a 32-bit unsigned integer that indicates whether OpenGL commands are present in the metafile.
        0x00000000 OpenGL records are not present in the metafile.
        0x00000001 OpenGL records are present in the metafile.'''
        raise NotImplementedError()
    
    @b_open_gl.setter
    def b_open_gl(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that indicates whether OpenGL commands are present in the metafile.
        0x00000000 OpenGL records are not present in the metafile.
        0x00000001 OpenGL records are present in the metafile.'''
        raise NotImplementedError()
    

class EmfHeaderExtension2(EmfHeaderObject):
    '''The HeaderExtension2 object defines the second extension to the EMF metafile header. It adds the
    ability to measure device surfaces in micrometers, which enhances the resolution and scalability of EMF metafiles.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfHeaderObject` class.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets a WMF RectL object ([MS-WMF] section 2.2.2.19) that specifies the rectangular inclusive-inclusive
        bounds in device units of the smallest rectangle that can be drawn around the image stored in
        the metafile'''
        raise NotImplementedError()
    
    @bounds.setter
    def bounds(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets a WMF RectL object ([MS-WMF] section 2.2.2.19) that specifies the rectangular inclusive-inclusive
        bounds in device units of the smallest rectangle that can be drawn around the image stored in
        the metafile'''
        raise NotImplementedError()
    
    @property
    def frame(self) -> aspose.imaging.Rectangle:
        '''Gets a WMF RectL object that specifies the rectangular inclusive-inclusive dimensions, in .01 millimeter
        units, of a rectangle that surrounds the image stored in the metafile'''
        raise NotImplementedError()
    
    @frame.setter
    def frame(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets a WMF RectL object that specifies the rectangular inclusive-inclusive dimensions, in .01 millimeter
        units, of a rectangle that surrounds the image stored in the metafile'''
        raise NotImplementedError()
    
    @property
    def record_signature(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfFormatSignature:
        '''Gets a 32-bit unsigned integer that specifies the record signature. This MUST be ENHMETA_SIGNATURE,
        from the FormatSignature enumeration (section 2.1.14).'''
        raise NotImplementedError()
    
    @record_signature.setter
    def record_signature(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfFormatSignature) -> None:
        '''Sets a 32-bit unsigned integer that specifies the record signature. This MUST be ENHMETA_SIGNATURE,
        from the FormatSignature enumeration (section 2.1.14).'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets Version (4 bytes): A 32-bit unsigned integer that specifies EMF metafile interoperability. This SHOULD be 0x00010000'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets Version (4 bytes): A 32-bit unsigned integer that specifies EMF metafile interoperability. This SHOULD be 0x00010000'''
        raise NotImplementedError()
    
    @property
    def bytes(self) -> int:
        '''Gets  32-bit unsigned integer that specifies the size of the metafile, in bytes.'''
        raise NotImplementedError()
    
    @bytes.setter
    def bytes(self, value : int) -> None:
        '''Sets  32-bit unsigned integer that specifies the size of the metafile, in bytes.'''
        raise NotImplementedError()
    
    @property
    def records(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of records in the metafile'''
        raise NotImplementedError()
    
    @records.setter
    def records(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of records in the metafile'''
        raise NotImplementedError()
    
    @property
    def handles(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the number of graphics objects that will be used during the processing of the metafile'''
        raise NotImplementedError()
    
    @handles.setter
    def handles(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the number of graphics objects that will be used during the processing of the metafile'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets a 16-bit unsigned integer that MUST be 0x0000 and MUST be ignored'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that MUST be 0x0000 and MUST be ignored'''
        raise NotImplementedError()
    
    @property
    def n_desription(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of characters in the array
        that contains the description of the metafile\'s contents. This is zero if there is no description string.'''
        raise NotImplementedError()
    
    @n_desription.setter
    def n_desription(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of characters in the array
        that contains the description of the metafile\'s contents. This is zero if there is no description string.'''
        raise NotImplementedError()
    
    @property
    def off_description(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the offset from the beginning of this
        record to the array that contains the description of the metafile\'s contents'''
        raise NotImplementedError()
    
    @off_description.setter
    def off_description(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the offset from the beginning of this
        record to the array that contains the description of the metafile\'s contents'''
        raise NotImplementedError()
    
    @property
    def n_pal_entries(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of entries in the metafile
        palette. The palette is located in the EMR_EOF record'''
        raise NotImplementedError()
    
    @n_pal_entries.setter
    def n_pal_entries(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of entries in the metafile
        palette. The palette is located in the EMR_EOF record'''
        raise NotImplementedError()
    
    @property
    def device(self) -> aspose.imaging.Size:
        '''Gets a WMF SizeL object ([MS-WMF] section 2.2.2.22) that specifies the size of the reference device, in pixels'''
        raise NotImplementedError()
    
    @device.setter
    def device(self, value : aspose.imaging.Size) -> None:
        '''Sets a WMF SizeL object ([MS-WMF] section 2.2.2.22) that specifies the size of the reference device, in pixels'''
        raise NotImplementedError()
    
    @property
    def millimeters(self) -> aspose.imaging.Size:
        '''Gets a WMF SizeL object that specifies the size of the reference device, in millimeters'''
        raise NotImplementedError()
    
    @millimeters.setter
    def millimeters(self, value : aspose.imaging.Size) -> None:
        '''Sets a WMF SizeL object that specifies the size of the reference device, in millimeters'''
        raise NotImplementedError()
    
    @property
    def valid(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfHeaderObject` is valid.'''
        raise NotImplementedError()
    
    @property
    def micrometers_x(self) -> int:
        '''Gets the 32-bit horizontal size of the display device for which the metafile image was generated, in micrometers'''
        raise NotImplementedError()
    
    @micrometers_x.setter
    def micrometers_x(self, value : int) -> None:
        '''Sets the 32-bit horizontal size of the display device for which the metafile image was generated, in micrometers'''
        raise NotImplementedError()
    
    @property
    def micrometers_y(self) -> int:
        '''Gets the 32-bit vertical size of the display device for which the metafile image was generated, in micrometers.'''
        raise NotImplementedError()
    
    @micrometers_y.setter
    def micrometers_y(self, value : int) -> None:
        '''Sets the 32-bit vertical size of the display device for which the metafile image was generated, in micrometers.'''
        raise NotImplementedError()
    

class EmfHeaderObject(EmfObject):
    '''The Header object defines the EMF metafile header. It specifies properties of the device on which the image in the metafile was created.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfHeaderObject` class.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets a WMF RectL object ([MS-WMF] section 2.2.2.19) that specifies the rectangular inclusive-inclusive
        bounds in device units of the smallest rectangle that can be drawn around the image stored in
        the metafile'''
        raise NotImplementedError()
    
    @bounds.setter
    def bounds(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets a WMF RectL object ([MS-WMF] section 2.2.2.19) that specifies the rectangular inclusive-inclusive
        bounds in device units of the smallest rectangle that can be drawn around the image stored in
        the metafile'''
        raise NotImplementedError()
    
    @property
    def frame(self) -> aspose.imaging.Rectangle:
        '''Gets a WMF RectL object that specifies the rectangular inclusive-inclusive dimensions, in .01 millimeter
        units, of a rectangle that surrounds the image stored in the metafile'''
        raise NotImplementedError()
    
    @frame.setter
    def frame(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets a WMF RectL object that specifies the rectangular inclusive-inclusive dimensions, in .01 millimeter
        units, of a rectangle that surrounds the image stored in the metafile'''
        raise NotImplementedError()
    
    @property
    def record_signature(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfFormatSignature:
        '''Gets a 32-bit unsigned integer that specifies the record signature. This MUST be ENHMETA_SIGNATURE,
        from the FormatSignature enumeration (section 2.1.14).'''
        raise NotImplementedError()
    
    @record_signature.setter
    def record_signature(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfFormatSignature) -> None:
        '''Sets a 32-bit unsigned integer that specifies the record signature. This MUST be ENHMETA_SIGNATURE,
        from the FormatSignature enumeration (section 2.1.14).'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets Version (4 bytes): A 32-bit unsigned integer that specifies EMF metafile interoperability. This SHOULD be 0x00010000'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets Version (4 bytes): A 32-bit unsigned integer that specifies EMF metafile interoperability. This SHOULD be 0x00010000'''
        raise NotImplementedError()
    
    @property
    def bytes(self) -> int:
        '''Gets  32-bit unsigned integer that specifies the size of the metafile, in bytes.'''
        raise NotImplementedError()
    
    @bytes.setter
    def bytes(self, value : int) -> None:
        '''Sets  32-bit unsigned integer that specifies the size of the metafile, in bytes.'''
        raise NotImplementedError()
    
    @property
    def records(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of records in the metafile'''
        raise NotImplementedError()
    
    @records.setter
    def records(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of records in the metafile'''
        raise NotImplementedError()
    
    @property
    def handles(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the number of graphics objects that will be used during the processing of the metafile'''
        raise NotImplementedError()
    
    @handles.setter
    def handles(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the number of graphics objects that will be used during the processing of the metafile'''
        raise NotImplementedError()
    
    @property
    def reserved(self) -> int:
        '''Gets a 16-bit unsigned integer that MUST be 0x0000 and MUST be ignored'''
        raise NotImplementedError()
    
    @reserved.setter
    def reserved(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that MUST be 0x0000 and MUST be ignored'''
        raise NotImplementedError()
    
    @property
    def n_desription(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of characters in the array
        that contains the description of the metafile\'s contents. This is zero if there is no description string.'''
        raise NotImplementedError()
    
    @n_desription.setter
    def n_desription(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of characters in the array
        that contains the description of the metafile\'s contents. This is zero if there is no description string.'''
        raise NotImplementedError()
    
    @property
    def off_description(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the offset from the beginning of this
        record to the array that contains the description of the metafile\'s contents'''
        raise NotImplementedError()
    
    @off_description.setter
    def off_description(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the offset from the beginning of this
        record to the array that contains the description of the metafile\'s contents'''
        raise NotImplementedError()
    
    @property
    def n_pal_entries(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of entries in the metafile
        palette. The palette is located in the EMR_EOF record'''
        raise NotImplementedError()
    
    @n_pal_entries.setter
    def n_pal_entries(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of entries in the metafile
        palette. The palette is located in the EMR_EOF record'''
        raise NotImplementedError()
    
    @property
    def device(self) -> aspose.imaging.Size:
        '''Gets a WMF SizeL object ([MS-WMF] section 2.2.2.22) that specifies the size of the reference device, in pixels'''
        raise NotImplementedError()
    
    @device.setter
    def device(self, value : aspose.imaging.Size) -> None:
        '''Sets a WMF SizeL object ([MS-WMF] section 2.2.2.22) that specifies the size of the reference device, in pixels'''
        raise NotImplementedError()
    
    @property
    def millimeters(self) -> aspose.imaging.Size:
        '''Gets a WMF SizeL object that specifies the size of the reference device, in millimeters'''
        raise NotImplementedError()
    
    @millimeters.setter
    def millimeters(self, value : aspose.imaging.Size) -> None:
        '''Sets a WMF SizeL object that specifies the size of the reference device, in millimeters'''
        raise NotImplementedError()
    
    @property
    def valid(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfHeaderObject` is valid.'''
        raise NotImplementedError()
    

class EmfLogBrushEx(EmfObject):
    '''The LogBrushEx object defines the style, color, and pattern of a device-independent brush.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def brush_style(self) -> aspose.imaging.fileformats.wmf.consts.WmfBrushStyle:
        '''Gets a 32-bit unsigned integer that specifies the brush style. The value MUST
        be an enumeration from WMF BrushStyle enumeration ([MS-WMF] section 2.1.1.4). The style
        values that are supported in this structure are listed later in this section. The BS_NULL style
        SHOULD be used to specify a brush that has no effect.'''
        raise NotImplementedError()
    
    @brush_style.setter
    def brush_style(self, value : aspose.imaging.fileformats.wmf.consts.WmfBrushStyle) -> None:
        '''Sets a 32-bit unsigned integer that specifies the brush style. The value MUST
        be an enumeration from WMF BrushStyle enumeration ([MS-WMF] section 2.1.1.4). The style
        values that are supported in this structure are listed later in this section. The BS_NULL style
        SHOULD be used to specify a brush that has no effect.'''
        raise NotImplementedError()
    
    @property
    def argb_32_color_ref(self) -> int:
        '''Gets a 32-bit WMF ColorRef object ([MS-WMF] section 2.2.2.8) that specifies a
        color. The interpretation of this field depends on the value of BrushStyle, as explained in the
        following table.'''
        raise NotImplementedError()
    
    @argb_32_color_ref.setter
    def argb_32_color_ref(self, value : int) -> None:
        '''Sets a 32-bit WMF ColorRef object ([MS-WMF] section 2.2.2.8) that specifies a
        color. The interpretation of this field depends on the value of BrushStyle, as explained in the
        following table.'''
        raise NotImplementedError()
    
    @property
    def brush_hatch(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfHatchStyle:
        '''Gets a 32-bit unsigned field that contains the brush hatch data. Its
        interpretation depends on the value of BrushStyle,'''
        raise NotImplementedError()
    
    @brush_hatch.setter
    def brush_hatch(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfHatchStyle) -> None:
        '''Sets a 32-bit unsigned field that contains the brush hatch data. Its
        interpretation depends on the value of BrushStyle,'''
        raise NotImplementedError()
    

class EmfLogFont(EmfObject):
    '''The LogFont object specifies the basic attributes of a logical font.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets a 32-bit signed integer that specifies the height, in logical units, of the font\'s
        character cell or character. The character height value, also known as the em size, is the
        character cell height value minus the internal leading value. The font mapper SHOULD
        interpret the value specified in the Height field in the following manner.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the height, in logical units, of the font\'s
        character cell or character. The character height value, also known as the em size, is the
        character cell height value minus the internal leading value. The font mapper SHOULD
        interpret the value specified in the Height field in the following manner.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets a 32-bit signed integer that specifies the average width, in logical units, of
        characters in the font. If the Width field value is zero, an appropriate value SHOULD be
        calculated from other LogFont values to find a font that has the typographer\'s intended
        aspect ratio'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the average width, in logical units, of
        characters in the font. If the Width field value is zero, an appropriate value SHOULD be
        calculated from other LogFont values to find a font that has the typographer\'s intended
        aspect ratio'''
        raise NotImplementedError()
    
    @property
    def escapement(self) -> int:
        '''Gets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between the escapement vector and the x-axis of the device. The escapement vector is
        parallel to the baseline of a row of text.'''
        raise NotImplementedError()
    
    @escapement.setter
    def escapement(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between the escapement vector and the x-axis of the device. The escapement vector is
        parallel to the baseline of a row of text.'''
        raise NotImplementedError()
    
    @property
    def orientation(self) -> int:
        '''Gets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between each character\'s baseline and the x-axis of the device.'''
        raise NotImplementedError()
    
    @orientation.setter
    def orientation(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between each character\'s baseline and the x-axis of the device.'''
        raise NotImplementedError()
    
    @property
    def weight(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfLogFontWeight:
        '''Gets a 32-bit signed integer that specifies the weight of the font in the range
        zero through 1000. For example, 400 is normal and 700 is bold. If this value is zero, a default
        weight can be used.'''
        raise NotImplementedError()
    
    @weight.setter
    def weight(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfLogFontWeight) -> None:
        '''Sets a 32-bit signed integer that specifies the weight of the font in the range
        zero through 1000. For example, 400 is normal and 700 is bold. If this value is zero, a default
        weight can be used.'''
        raise NotImplementedError()
    
    @property
    def italic(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies an italic font if set to 0x01; otherwise,
        it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @italic.setter
    def italic(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies an italic font if set to 0x01; otherwise,
        it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def underline(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies an underlined font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @underline.setter
    def underline(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies an underlined font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def strikeout(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies a strikeout font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @strikeout.setter
    def strikeout(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies a strikeout font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def char_set(self) -> aspose.imaging.fileformats.wmf.consts.WmfCharacterSet:
        '''Gets an 8-bit unsigned integer that specifies the set of character glyphs. It MUST
        be a value in the WMF CharacterSet enumeration ([MS-WMF] section 2.1.1.5). If the
        character set is unknown, metafile processing SHOULD NOT attempt to translate or interpret
        strings that are rendered with that font.'''
        raise NotImplementedError()
    
    @char_set.setter
    def char_set(self, value : aspose.imaging.fileformats.wmf.consts.WmfCharacterSet) -> None:
        '''Sets an 8-bit unsigned integer that specifies the set of character glyphs. It MUST
        be a value in the WMF CharacterSet enumeration ([MS-WMF] section 2.1.1.5). If the
        character set is unknown, metafile processing SHOULD NOT attempt to translate or interpret
        strings that are rendered with that font.'''
        raise NotImplementedError()
    
    @property
    def out_precision(self) -> aspose.imaging.fileformats.wmf.consts.WmfOutPrecision:
        '''Gets an 8-bit unsigned integer that specifies the output precision. The
        output precision defines how closely the font is required to match the requested height, width,
        character orientation, escapement, pitch, and font type. It MUST be a value from the WMF
        OutPrecision enumeration'''
        raise NotImplementedError()
    
    @out_precision.setter
    def out_precision(self, value : aspose.imaging.fileformats.wmf.consts.WmfOutPrecision) -> None:
        '''Sets an 8-bit unsigned integer that specifies the output precision. The
        output precision defines how closely the font is required to match the requested height, width,
        character orientation, escapement, pitch, and font type. It MUST be a value from the WMF
        OutPrecision enumeration'''
        raise NotImplementedError()
    
    @property
    def clip_precision(self) -> aspose.imaging.fileformats.wmf.consts.WmfClipPrecisionFlags:
        '''Gets an 8-bit unsigned integer that specifies the clipping precision. The
        clipping precision defines how to clip characters that are partially outside the clipping region.
        It can be one or more of the WMF ClipPrecision Flags'''
        raise NotImplementedError()
    
    @clip_precision.setter
    def clip_precision(self, value : aspose.imaging.fileformats.wmf.consts.WmfClipPrecisionFlags) -> None:
        '''Sets an 8-bit unsigned integer that specifies the clipping precision. The
        clipping precision defines how to clip characters that are partially outside the clipping region.
        It can be one or more of the WMF ClipPrecision Flags'''
        raise NotImplementedError()
    
    @property
    def quality(self) -> aspose.imaging.fileformats.wmf.consts.WmfFontQuality:
        '''Gets an 8-bit unsigned integer that specifies the output quality. The output quality
        defines how closely to attempt to match the logical-font attributes to those of an actual
        physical font. It MUST be one of the values in the WMF FontQuality enumeration ([MS-WMF]
        section 2.1.1.10).'''
        raise NotImplementedError()
    
    @quality.setter
    def quality(self, value : aspose.imaging.fileformats.wmf.consts.WmfFontQuality) -> None:
        '''Sets an 8-bit unsigned integer that specifies the output quality. The output quality
        defines how closely to attempt to match the logical-font attributes to those of an actual
        physical font. It MUST be one of the values in the WMF FontQuality enumeration ([MS-WMF]
        section 2.1.1.10).'''
        raise NotImplementedError()
    
    @property
    def pitch_and_family(self) -> aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily:
        '''Gets a WMF PitchAndFamily object ([MS-WMF] section 2.2.2.14) that
        specifies the pitch and family of the font. Font families describe the look of a font in a general
        way. They are intended for specifying a font when the specified typeface is not available.'''
        raise NotImplementedError()
    
    @pitch_and_family.setter
    def pitch_and_family(self, value : aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily) -> None:
        '''Sets a WMF PitchAndFamily object ([MS-WMF] section 2.2.2.14) that
        specifies the pitch and family of the font. Font families describe the look of a font in a general
        way. They are intended for specifying a font when the specified typeface is not available.'''
        raise NotImplementedError()
    
    @property
    def facename(self) -> str:
        '''Gets a Facename (64 bytes):  A string of no more than 32 Unicode characters that specifies the
        typeface name of the font. If the length of this string is less than 32 characters, a terminating
        NULL MUST be present, after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @facename.setter
    def facename(self, value : str) -> None:
        '''Sets a Facename (64 bytes):  A string of no more than 32 Unicode characters that specifies the
        typeface name of the font. If the length of this string is less than 32 characters, a terminating
        NULL MUST be present, after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    

class EmfLogFontEx(EmfLogFont):
    '''The LogFontEx object specifies the extended attributes of a logical font.'''
    
    def __init__(self, emf_log_font : aspose.imaging.fileformats.emf.emf.objects.EmfLogFont) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfLogFontEx` class.
        
        :param emf_log_font: The EMF log font.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets a 32-bit signed integer that specifies the height, in logical units, of the font\'s
        character cell or character. The character height value, also known as the em size, is the
        character cell height value minus the internal leading value. The font mapper SHOULD
        interpret the value specified in the Height field in the following manner.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the height, in logical units, of the font\'s
        character cell or character. The character height value, also known as the em size, is the
        character cell height value minus the internal leading value. The font mapper SHOULD
        interpret the value specified in the Height field in the following manner.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets a 32-bit signed integer that specifies the average width, in logical units, of
        characters in the font. If the Width field value is zero, an appropriate value SHOULD be
        calculated from other LogFont values to find a font that has the typographer\'s intended
        aspect ratio'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the average width, in logical units, of
        characters in the font. If the Width field value is zero, an appropriate value SHOULD be
        calculated from other LogFont values to find a font that has the typographer\'s intended
        aspect ratio'''
        raise NotImplementedError()
    
    @property
    def escapement(self) -> int:
        '''Gets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between the escapement vector and the x-axis of the device. The escapement vector is
        parallel to the baseline of a row of text.'''
        raise NotImplementedError()
    
    @escapement.setter
    def escapement(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between the escapement vector and the x-axis of the device. The escapement vector is
        parallel to the baseline of a row of text.'''
        raise NotImplementedError()
    
    @property
    def orientation(self) -> int:
        '''Gets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between each character\'s baseline and the x-axis of the device.'''
        raise NotImplementedError()
    
    @orientation.setter
    def orientation(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between each character\'s baseline and the x-axis of the device.'''
        raise NotImplementedError()
    
    @property
    def weight(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfLogFontWeight:
        '''Gets a 32-bit signed integer that specifies the weight of the font in the range
        zero through 1000. For example, 400 is normal and 700 is bold. If this value is zero, a default
        weight can be used.'''
        raise NotImplementedError()
    
    @weight.setter
    def weight(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfLogFontWeight) -> None:
        '''Sets a 32-bit signed integer that specifies the weight of the font in the range
        zero through 1000. For example, 400 is normal and 700 is bold. If this value is zero, a default
        weight can be used.'''
        raise NotImplementedError()
    
    @property
    def italic(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies an italic font if set to 0x01; otherwise,
        it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @italic.setter
    def italic(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies an italic font if set to 0x01; otherwise,
        it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def underline(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies an underlined font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @underline.setter
    def underline(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies an underlined font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def strikeout(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies a strikeout font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @strikeout.setter
    def strikeout(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies a strikeout font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def char_set(self) -> aspose.imaging.fileformats.wmf.consts.WmfCharacterSet:
        '''Gets an 8-bit unsigned integer that specifies the set of character glyphs. It MUST
        be a value in the WMF CharacterSet enumeration ([MS-WMF] section 2.1.1.5). If the
        character set is unknown, metafile processing SHOULD NOT attempt to translate or interpret
        strings that are rendered with that font.'''
        raise NotImplementedError()
    
    @char_set.setter
    def char_set(self, value : aspose.imaging.fileformats.wmf.consts.WmfCharacterSet) -> None:
        '''Sets an 8-bit unsigned integer that specifies the set of character glyphs. It MUST
        be a value in the WMF CharacterSet enumeration ([MS-WMF] section 2.1.1.5). If the
        character set is unknown, metafile processing SHOULD NOT attempt to translate or interpret
        strings that are rendered with that font.'''
        raise NotImplementedError()
    
    @property
    def out_precision(self) -> aspose.imaging.fileformats.wmf.consts.WmfOutPrecision:
        '''Gets an 8-bit unsigned integer that specifies the output precision. The
        output precision defines how closely the font is required to match the requested height, width,
        character orientation, escapement, pitch, and font type. It MUST be a value from the WMF
        OutPrecision enumeration'''
        raise NotImplementedError()
    
    @out_precision.setter
    def out_precision(self, value : aspose.imaging.fileformats.wmf.consts.WmfOutPrecision) -> None:
        '''Sets an 8-bit unsigned integer that specifies the output precision. The
        output precision defines how closely the font is required to match the requested height, width,
        character orientation, escapement, pitch, and font type. It MUST be a value from the WMF
        OutPrecision enumeration'''
        raise NotImplementedError()
    
    @property
    def clip_precision(self) -> aspose.imaging.fileformats.wmf.consts.WmfClipPrecisionFlags:
        '''Gets an 8-bit unsigned integer that specifies the clipping precision. The
        clipping precision defines how to clip characters that are partially outside the clipping region.
        It can be one or more of the WMF ClipPrecision Flags'''
        raise NotImplementedError()
    
    @clip_precision.setter
    def clip_precision(self, value : aspose.imaging.fileformats.wmf.consts.WmfClipPrecisionFlags) -> None:
        '''Sets an 8-bit unsigned integer that specifies the clipping precision. The
        clipping precision defines how to clip characters that are partially outside the clipping region.
        It can be one or more of the WMF ClipPrecision Flags'''
        raise NotImplementedError()
    
    @property
    def quality(self) -> aspose.imaging.fileformats.wmf.consts.WmfFontQuality:
        '''Gets an 8-bit unsigned integer that specifies the output quality. The output quality
        defines how closely to attempt to match the logical-font attributes to those of an actual
        physical font. It MUST be one of the values in the WMF FontQuality enumeration ([MS-WMF]
        section 2.1.1.10).'''
        raise NotImplementedError()
    
    @quality.setter
    def quality(self, value : aspose.imaging.fileformats.wmf.consts.WmfFontQuality) -> None:
        '''Sets an 8-bit unsigned integer that specifies the output quality. The output quality
        defines how closely to attempt to match the logical-font attributes to those of an actual
        physical font. It MUST be one of the values in the WMF FontQuality enumeration ([MS-WMF]
        section 2.1.1.10).'''
        raise NotImplementedError()
    
    @property
    def pitch_and_family(self) -> aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily:
        '''Gets a WMF PitchAndFamily object ([MS-WMF] section 2.2.2.14) that
        specifies the pitch and family of the font. Font families describe the look of a font in a general
        way. They are intended for specifying a font when the specified typeface is not available.'''
        raise NotImplementedError()
    
    @pitch_and_family.setter
    def pitch_and_family(self, value : aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily) -> None:
        '''Sets a WMF PitchAndFamily object ([MS-WMF] section 2.2.2.14) that
        specifies the pitch and family of the font. Font families describe the look of a font in a general
        way. They are intended for specifying a font when the specified typeface is not available.'''
        raise NotImplementedError()
    
    @property
    def facename(self) -> str:
        '''Gets a Facename (64 bytes):  A string of no more than 32 Unicode characters that specifies the
        typeface name of the font. If the length of this string is less than 32 characters, a terminating
        NULL MUST be present, after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @facename.setter
    def facename(self, value : str) -> None:
        '''Sets a Facename (64 bytes):  A string of no more than 32 Unicode characters that specifies the
        typeface name of the font. If the length of this string is less than 32 characters, a terminating
        NULL MUST be present, after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def full_name(self) -> str:
        '''Gets a string of 64 Unicode characters that contains the font\'s full name. If
        the length of this string is less than 64 characters, a terminating NULL MUST be present, after
        which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @full_name.setter
    def full_name(self, value : str) -> None:
        '''Sets a string of 64 Unicode characters that contains the font\'s full name. If
        the length of this string is less than 64 characters, a terminating NULL MUST be present, after
        which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def style(self) -> str:
        '''Gets a string of 32 Unicode characters that defines the font\'s style. If the length of
        this string is less than 32 characters, a terminating NULL MUST be present, after which the
        remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : str) -> None:
        '''Sets a string of 32 Unicode characters that defines the font\'s style. If the length of
        this string is less than 32 characters, a terminating NULL MUST be present, after which the
        remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def script(self) -> str:
        '''Gets a string of 32 Unicode characters that defines the character set of the font.
        If the length of this string is less than 32 characters, a terminating NULL MUST be present,
        after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @script.setter
    def script(self, value : str) -> None:
        '''Sets a string of 32 Unicode characters that defines the character set of the font.
        If the length of this string is less than 32 characters, a terminating NULL MUST be present,
        after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    

class EmfLogFontExDv(EmfLogFontEx):
    '''The LogFontExDv object specifies the design vector for an extended logical font.'''
    
    def __init__(self, emf_log_font_ex : aspose.imaging.fileformats.emf.emf.objects.EmfLogFontEx) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfLogFontExDv` class.
        
        :param emf_log_font_ex: The EMF log font ex.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets a 32-bit signed integer that specifies the height, in logical units, of the font\'s
        character cell or character. The character height value, also known as the em size, is the
        character cell height value minus the internal leading value. The font mapper SHOULD
        interpret the value specified in the Height field in the following manner.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the height, in logical units, of the font\'s
        character cell or character. The character height value, also known as the em size, is the
        character cell height value minus the internal leading value. The font mapper SHOULD
        interpret the value specified in the Height field in the following manner.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets a 32-bit signed integer that specifies the average width, in logical units, of
        characters in the font. If the Width field value is zero, an appropriate value SHOULD be
        calculated from other LogFont values to find a font that has the typographer\'s intended
        aspect ratio'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the average width, in logical units, of
        characters in the font. If the Width field value is zero, an appropriate value SHOULD be
        calculated from other LogFont values to find a font that has the typographer\'s intended
        aspect ratio'''
        raise NotImplementedError()
    
    @property
    def escapement(self) -> int:
        '''Gets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between the escapement vector and the x-axis of the device. The escapement vector is
        parallel to the baseline of a row of text.'''
        raise NotImplementedError()
    
    @escapement.setter
    def escapement(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between the escapement vector and the x-axis of the device. The escapement vector is
        parallel to the baseline of a row of text.'''
        raise NotImplementedError()
    
    @property
    def orientation(self) -> int:
        '''Gets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between each character\'s baseline and the x-axis of the device.'''
        raise NotImplementedError()
    
    @orientation.setter
    def orientation(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between each character\'s baseline and the x-axis of the device.'''
        raise NotImplementedError()
    
    @property
    def weight(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfLogFontWeight:
        '''Gets a 32-bit signed integer that specifies the weight of the font in the range
        zero through 1000. For example, 400 is normal and 700 is bold. If this value is zero, a default
        weight can be used.'''
        raise NotImplementedError()
    
    @weight.setter
    def weight(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfLogFontWeight) -> None:
        '''Sets a 32-bit signed integer that specifies the weight of the font in the range
        zero through 1000. For example, 400 is normal and 700 is bold. If this value is zero, a default
        weight can be used.'''
        raise NotImplementedError()
    
    @property
    def italic(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies an italic font if set to 0x01; otherwise,
        it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @italic.setter
    def italic(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies an italic font if set to 0x01; otherwise,
        it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def underline(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies an underlined font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @underline.setter
    def underline(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies an underlined font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def strikeout(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies a strikeout font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @strikeout.setter
    def strikeout(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies a strikeout font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def char_set(self) -> aspose.imaging.fileformats.wmf.consts.WmfCharacterSet:
        '''Gets an 8-bit unsigned integer that specifies the set of character glyphs. It MUST
        be a value in the WMF CharacterSet enumeration ([MS-WMF] section 2.1.1.5). If the
        character set is unknown, metafile processing SHOULD NOT attempt to translate or interpret
        strings that are rendered with that font.'''
        raise NotImplementedError()
    
    @char_set.setter
    def char_set(self, value : aspose.imaging.fileformats.wmf.consts.WmfCharacterSet) -> None:
        '''Sets an 8-bit unsigned integer that specifies the set of character glyphs. It MUST
        be a value in the WMF CharacterSet enumeration ([MS-WMF] section 2.1.1.5). If the
        character set is unknown, metafile processing SHOULD NOT attempt to translate or interpret
        strings that are rendered with that font.'''
        raise NotImplementedError()
    
    @property
    def out_precision(self) -> aspose.imaging.fileformats.wmf.consts.WmfOutPrecision:
        '''Gets an 8-bit unsigned integer that specifies the output precision. The
        output precision defines how closely the font is required to match the requested height, width,
        character orientation, escapement, pitch, and font type. It MUST be a value from the WMF
        OutPrecision enumeration'''
        raise NotImplementedError()
    
    @out_precision.setter
    def out_precision(self, value : aspose.imaging.fileformats.wmf.consts.WmfOutPrecision) -> None:
        '''Sets an 8-bit unsigned integer that specifies the output precision. The
        output precision defines how closely the font is required to match the requested height, width,
        character orientation, escapement, pitch, and font type. It MUST be a value from the WMF
        OutPrecision enumeration'''
        raise NotImplementedError()
    
    @property
    def clip_precision(self) -> aspose.imaging.fileformats.wmf.consts.WmfClipPrecisionFlags:
        '''Gets an 8-bit unsigned integer that specifies the clipping precision. The
        clipping precision defines how to clip characters that are partially outside the clipping region.
        It can be one or more of the WMF ClipPrecision Flags'''
        raise NotImplementedError()
    
    @clip_precision.setter
    def clip_precision(self, value : aspose.imaging.fileformats.wmf.consts.WmfClipPrecisionFlags) -> None:
        '''Sets an 8-bit unsigned integer that specifies the clipping precision. The
        clipping precision defines how to clip characters that are partially outside the clipping region.
        It can be one or more of the WMF ClipPrecision Flags'''
        raise NotImplementedError()
    
    @property
    def quality(self) -> aspose.imaging.fileformats.wmf.consts.WmfFontQuality:
        '''Gets an 8-bit unsigned integer that specifies the output quality. The output quality
        defines how closely to attempt to match the logical-font attributes to those of an actual
        physical font. It MUST be one of the values in the WMF FontQuality enumeration ([MS-WMF]
        section 2.1.1.10).'''
        raise NotImplementedError()
    
    @quality.setter
    def quality(self, value : aspose.imaging.fileformats.wmf.consts.WmfFontQuality) -> None:
        '''Sets an 8-bit unsigned integer that specifies the output quality. The output quality
        defines how closely to attempt to match the logical-font attributes to those of an actual
        physical font. It MUST be one of the values in the WMF FontQuality enumeration ([MS-WMF]
        section 2.1.1.10).'''
        raise NotImplementedError()
    
    @property
    def pitch_and_family(self) -> aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily:
        '''Gets a WMF PitchAndFamily object ([MS-WMF] section 2.2.2.14) that
        specifies the pitch and family of the font. Font families describe the look of a font in a general
        way. They are intended for specifying a font when the specified typeface is not available.'''
        raise NotImplementedError()
    
    @pitch_and_family.setter
    def pitch_and_family(self, value : aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily) -> None:
        '''Sets a WMF PitchAndFamily object ([MS-WMF] section 2.2.2.14) that
        specifies the pitch and family of the font. Font families describe the look of a font in a general
        way. They are intended for specifying a font when the specified typeface is not available.'''
        raise NotImplementedError()
    
    @property
    def facename(self) -> str:
        '''Gets a Facename (64 bytes):  A string of no more than 32 Unicode characters that specifies the
        typeface name of the font. If the length of this string is less than 32 characters, a terminating
        NULL MUST be present, after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @facename.setter
    def facename(self, value : str) -> None:
        '''Sets a Facename (64 bytes):  A string of no more than 32 Unicode characters that specifies the
        typeface name of the font. If the length of this string is less than 32 characters, a terminating
        NULL MUST be present, after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def full_name(self) -> str:
        '''Gets a string of 64 Unicode characters that contains the font\'s full name. If
        the length of this string is less than 64 characters, a terminating NULL MUST be present, after
        which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @full_name.setter
    def full_name(self, value : str) -> None:
        '''Sets a string of 64 Unicode characters that contains the font\'s full name. If
        the length of this string is less than 64 characters, a terminating NULL MUST be present, after
        which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def style(self) -> str:
        '''Gets a string of 32 Unicode characters that defines the font\'s style. If the length of
        this string is less than 32 characters, a terminating NULL MUST be present, after which the
        remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : str) -> None:
        '''Sets a string of 32 Unicode characters that defines the font\'s style. If the length of
        this string is less than 32 characters, a terminating NULL MUST be present, after which the
        remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def script(self) -> str:
        '''Gets a string of 32 Unicode characters that defines the character set of the font.
        If the length of this string is less than 32 characters, a terminating NULL MUST be present,
        after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @script.setter
    def script(self, value : str) -> None:
        '''Sets a string of 32 Unicode characters that defines the character set of the font.
        If the length of this string is less than 32 characters, a terminating NULL MUST be present,
        after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def design_vector(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfDesignVector:
        '''Gets a DesignVector object (section 2.2.3). This field MUST NOT be longer than 72 bytes.'''
        raise NotImplementedError()
    
    @design_vector.setter
    def design_vector(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfDesignVector) -> None:
        '''Sets a DesignVector object (section 2.2.3). This field MUST NOT be longer than 72 bytes.'''
        raise NotImplementedError()
    

class EmfLogFontPanose(EmfLogFont):
    '''The LogFontPanose object specifies the PANOSE characteristics of a logical font.'''
    
    def __init__(self, emf_log_font : aspose.imaging.fileformats.emf.emf.objects.EmfLogFont) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfLogFontPanose` class.
        
        :param emf_log_font: The base log font.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets a 32-bit signed integer that specifies the height, in logical units, of the font\'s
        character cell or character. The character height value, also known as the em size, is the
        character cell height value minus the internal leading value. The font mapper SHOULD
        interpret the value specified in the Height field in the following manner.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the height, in logical units, of the font\'s
        character cell or character. The character height value, also known as the em size, is the
        character cell height value minus the internal leading value. The font mapper SHOULD
        interpret the value specified in the Height field in the following manner.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets a 32-bit signed integer that specifies the average width, in logical units, of
        characters in the font. If the Width field value is zero, an appropriate value SHOULD be
        calculated from other LogFont values to find a font that has the typographer\'s intended
        aspect ratio'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the average width, in logical units, of
        characters in the font. If the Width field value is zero, an appropriate value SHOULD be
        calculated from other LogFont values to find a font that has the typographer\'s intended
        aspect ratio'''
        raise NotImplementedError()
    
    @property
    def escapement(self) -> int:
        '''Gets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between the escapement vector and the x-axis of the device. The escapement vector is
        parallel to the baseline of a row of text.'''
        raise NotImplementedError()
    
    @escapement.setter
    def escapement(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between the escapement vector and the x-axis of the device. The escapement vector is
        parallel to the baseline of a row of text.'''
        raise NotImplementedError()
    
    @property
    def orientation(self) -> int:
        '''Gets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between each character\'s baseline and the x-axis of the device.'''
        raise NotImplementedError()
    
    @orientation.setter
    def orientation(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the angle, in tenths of degrees,
        between each character\'s baseline and the x-axis of the device.'''
        raise NotImplementedError()
    
    @property
    def weight(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfLogFontWeight:
        '''Gets a 32-bit signed integer that specifies the weight of the font in the range
        zero through 1000. For example, 400 is normal and 700 is bold. If this value is zero, a default
        weight can be used.'''
        raise NotImplementedError()
    
    @weight.setter
    def weight(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfLogFontWeight) -> None:
        '''Sets a 32-bit signed integer that specifies the weight of the font in the range
        zero through 1000. For example, 400 is normal and 700 is bold. If this value is zero, a default
        weight can be used.'''
        raise NotImplementedError()
    
    @property
    def italic(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies an italic font if set to 0x01; otherwise,
        it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @italic.setter
    def italic(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies an italic font if set to 0x01; otherwise,
        it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def underline(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies an underlined font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @underline.setter
    def underline(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies an underlined font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def strikeout(self) -> int:
        '''Gets an 8-bit unsigned integer that specifies a strikeout font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @strikeout.setter
    def strikeout(self, value : int) -> None:
        '''Sets an 8-bit unsigned integer that specifies a strikeout font if set to 0x01;
        otherwise, it MUST be set to 0x00.'''
        raise NotImplementedError()
    
    @property
    def char_set(self) -> aspose.imaging.fileformats.wmf.consts.WmfCharacterSet:
        '''Gets an 8-bit unsigned integer that specifies the set of character glyphs. It MUST
        be a value in the WMF CharacterSet enumeration ([MS-WMF] section 2.1.1.5). If the
        character set is unknown, metafile processing SHOULD NOT attempt to translate or interpret
        strings that are rendered with that font.'''
        raise NotImplementedError()
    
    @char_set.setter
    def char_set(self, value : aspose.imaging.fileformats.wmf.consts.WmfCharacterSet) -> None:
        '''Sets an 8-bit unsigned integer that specifies the set of character glyphs. It MUST
        be a value in the WMF CharacterSet enumeration ([MS-WMF] section 2.1.1.5). If the
        character set is unknown, metafile processing SHOULD NOT attempt to translate or interpret
        strings that are rendered with that font.'''
        raise NotImplementedError()
    
    @property
    def out_precision(self) -> aspose.imaging.fileformats.wmf.consts.WmfOutPrecision:
        '''Gets an 8-bit unsigned integer that specifies the output precision. The
        output precision defines how closely the font is required to match the requested height, width,
        character orientation, escapement, pitch, and font type. It MUST be a value from the WMF
        OutPrecision enumeration'''
        raise NotImplementedError()
    
    @out_precision.setter
    def out_precision(self, value : aspose.imaging.fileformats.wmf.consts.WmfOutPrecision) -> None:
        '''Sets an 8-bit unsigned integer that specifies the output precision. The
        output precision defines how closely the font is required to match the requested height, width,
        character orientation, escapement, pitch, and font type. It MUST be a value from the WMF
        OutPrecision enumeration'''
        raise NotImplementedError()
    
    @property
    def clip_precision(self) -> aspose.imaging.fileformats.wmf.consts.WmfClipPrecisionFlags:
        '''Gets an 8-bit unsigned integer that specifies the clipping precision. The
        clipping precision defines how to clip characters that are partially outside the clipping region.
        It can be one or more of the WMF ClipPrecision Flags'''
        raise NotImplementedError()
    
    @clip_precision.setter
    def clip_precision(self, value : aspose.imaging.fileformats.wmf.consts.WmfClipPrecisionFlags) -> None:
        '''Sets an 8-bit unsigned integer that specifies the clipping precision. The
        clipping precision defines how to clip characters that are partially outside the clipping region.
        It can be one or more of the WMF ClipPrecision Flags'''
        raise NotImplementedError()
    
    @property
    def quality(self) -> aspose.imaging.fileformats.wmf.consts.WmfFontQuality:
        '''Gets an 8-bit unsigned integer that specifies the output quality. The output quality
        defines how closely to attempt to match the logical-font attributes to those of an actual
        physical font. It MUST be one of the values in the WMF FontQuality enumeration ([MS-WMF]
        section 2.1.1.10).'''
        raise NotImplementedError()
    
    @quality.setter
    def quality(self, value : aspose.imaging.fileformats.wmf.consts.WmfFontQuality) -> None:
        '''Sets an 8-bit unsigned integer that specifies the output quality. The output quality
        defines how closely to attempt to match the logical-font attributes to those of an actual
        physical font. It MUST be one of the values in the WMF FontQuality enumeration ([MS-WMF]
        section 2.1.1.10).'''
        raise NotImplementedError()
    
    @property
    def pitch_and_family(self) -> aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily:
        '''Gets a WMF PitchAndFamily object ([MS-WMF] section 2.2.2.14) that
        specifies the pitch and family of the font. Font families describe the look of a font in a general
        way. They are intended for specifying a font when the specified typeface is not available.'''
        raise NotImplementedError()
    
    @pitch_and_family.setter
    def pitch_and_family(self, value : aspose.imaging.fileformats.wmf.objects.WmfPitchAndFamily) -> None:
        '''Sets a WMF PitchAndFamily object ([MS-WMF] section 2.2.2.14) that
        specifies the pitch and family of the font. Font families describe the look of a font in a general
        way. They are intended for specifying a font when the specified typeface is not available.'''
        raise NotImplementedError()
    
    @property
    def facename(self) -> str:
        '''Gets a Facename (64 bytes):  A string of no more than 32 Unicode characters that specifies the
        typeface name of the font. If the length of this string is less than 32 characters, a terminating
        NULL MUST be present, after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @facename.setter
    def facename(self, value : str) -> None:
        '''Sets a Facename (64 bytes):  A string of no more than 32 Unicode characters that specifies the
        typeface name of the font. If the length of this string is less than 32 characters, a terminating
        NULL MUST be present, after which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def full_name(self) -> str:
        '''Gets a string of 64 Unicode characters that defines the font\'s full name. If
        the length of this string is less than 64 characters, a terminating NULL MUST be present, after
        which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @full_name.setter
    def full_name(self, value : str) -> None:
        '''Sets a string of 64 Unicode characters that defines the font\'s full name. If
        the length of this string is less than 64 characters, a terminating NULL MUST be present, after
        which the remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def style(self) -> str:
        '''Gets a string of 32 Unicode characters that defines the font\'s style. If the length of
        this string is less than 32 characters, a terminating NULL MUST be present, after which the
        remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @style.setter
    def style(self, value : str) -> None:
        '''Sets a string of 32 Unicode characters that defines the font\'s style. If the length of
        this string is less than 32 characters, a terminating NULL MUST be present, after which the
        remainder of this field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets This field MUST be ignored.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets This field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def style_size(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the point size at which font
        hinting is performed. If set to zero, font hinting is performed at the point size corresponding
        to the Height field in the LogFont object in the LogFont field'''
        raise NotImplementedError()
    
    @style_size.setter
    def style_size(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the point size at which font
        hinting is performed. If set to zero, font hinting is performed at the point size corresponding
        to the Height field in the LogFont object in the LogFont field'''
        raise NotImplementedError()
    
    @property
    def match(self) -> int:
        '''Gets This field MUST be ignored.'''
        raise NotImplementedError()
    
    @match.setter
    def match(self, value : int) -> None:
        '''Sets This field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def vendor_id(self) -> int:
        '''Gets This field MUST be ignored.'''
        raise NotImplementedError()
    
    @vendor_id.setter
    def vendor_id(self, value : int) -> None:
        '''Sets This field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def culture(self) -> int:
        '''Gets a 32-bit unsigned integer that MUST be set to zero and MUST be ignored.'''
        raise NotImplementedError()
    
    @culture.setter
    def culture(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that MUST be set to zero and MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def panose(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfPanose:
        '''Gets a Panose object (section 2.2.21) that specifies the PANOSE characteristics
        of the logical font. If all fields of this object are zero, it MUST be ignored.'''
        raise NotImplementedError()
    
    @panose.setter
    def panose(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfPanose) -> None:
        '''Sets a Panose object (section 2.2.21) that specifies the PANOSE characteristics
        of the logical font. If all fields of this object are zero, it MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def padding(self) -> int:
        '''Gets a field that exists only to ensure 32-bit alignment of this structure. It MUST be ignored'''
        raise NotImplementedError()
    
    @padding.setter
    def padding(self, value : int) -> None:
        '''Sets a field that exists only to ensure 32-bit alignment of this structure. It MUST be ignored'''
        raise NotImplementedError()
    

class EmfLogPalette(EmfObject):
    '''The LogPalette object specifies a logical_palette that contains device-independent color definitions.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the version number of the system.
        This MUST be 0x0300.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the version number of the system.
        This MUST be 0x0300.'''
        raise NotImplementedError()
    
    @property
    def palette_argb_32_entries(self) -> List[int]:
        '''Gets an array of 32-bit ARGB colors.'''
        raise NotImplementedError()
    
    @palette_argb_32_entries.setter
    def palette_argb_32_entries(self, value : List[int]) -> None:
        '''Sets an array of 32-bit ARGB colors.'''
        raise NotImplementedError()
    

class EmfLogPen(EmfBasePen):
    '''The LogPen object defines the style, width, and color of a logical pen.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def pen_style(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfPenStyle:
        '''Gets a 32-bit unsigned integer that specifies the PenStyle. The value MUST be
        defined from the PenStyle enumeration table, specified in section 2.1.25.'''
        raise NotImplementedError()
    
    @pen_style.setter
    def pen_style(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfPenStyle) -> None:
        '''Sets a 32-bit unsigned integer that specifies the PenStyle. The value MUST be
        defined from the PenStyle enumeration table, specified in section 2.1.25.'''
        raise NotImplementedError()
    
    @property
    def argb_32_color_ref(self) -> int:
        '''Gets a WMF ColorRef object ([MS-WMF] section 2.2.2.8) that specifies the pen color value.'''
        raise NotImplementedError()
    
    @argb_32_color_ref.setter
    def argb_32_color_ref(self, value : int) -> None:
        '''Sets a WMF ColorRef object ([MS-WMF] section 2.2.2.8) that specifies the pen color value.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> aspose.imaging.Point:
        '''Gets a WMF PointL object ([MS-WMF] section 2.2.2.15) that specifies the width of
        the pen by the value of its x field. The value of its y field MUST be ignored.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : aspose.imaging.Point) -> None:
        '''Sets a WMF PointL object ([MS-WMF] section 2.2.2.15) that specifies the width of
        the pen by the value of its x field. The value of its y field MUST be ignored.'''
        raise NotImplementedError()
    
    @property
    def affect_width(self) -> int:
        '''Gets the width of the affect.'''
        raise NotImplementedError()
    
    @affect_width.setter
    def affect_width(self, value : int) -> None:
        '''Sets the width of the affect.'''
        raise NotImplementedError()
    

class EmfLogPenEx(EmfBasePen):
    '''The LogPenEx object specifies the style, width, and color of an extended logical pen.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def pen_style(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfPenStyle:
        '''Gets the pen style'''
        raise NotImplementedError()
    
    @pen_style.setter
    def pen_style(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfPenStyle) -> None:
        '''Sets the pen style'''
        raise NotImplementedError()
    
    @property
    def argb_32_color_ref(self) -> int:
        '''Gets a WMF ColorRef object ([MS-WMF] section 2.2.2.8). The interpretation of this
        field depends on the BrushStyle value, as shown in the table later in this section.'''
        raise NotImplementedError()
    
    @argb_32_color_ref.setter
    def argb_32_color_ref(self, value : int) -> None:
        '''Sets a WMF ColorRef object ([MS-WMF] section 2.2.2.8). The interpretation of this
        field depends on the BrushStyle value, as shown in the table later in this section.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the width of the line drawn by the pen.
        If the pen type in the PenStyle field is PS_GEOMETRIC, this value is the width in
        logical units; otherwise, the width is specified in device units.
        If the pen type in the PenStyle field is PS_COSMETIC, this value MUST be 0x00000001.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the width of the line drawn by the pen.
        If the pen type in the PenStyle field is PS_GEOMETRIC, this value is the width in
        logical units; otherwise, the width is specified in device units.
        If the pen type in the PenStyle field is PS_COSMETIC, this value MUST be 0x00000001.'''
        raise NotImplementedError()
    
    @property
    def brush_style(self) -> aspose.imaging.fileformats.wmf.consts.WmfBrushStyle:
        '''Gets a 32-bit unsigned integer that specifies a brush style for the pen from the
        WMF BrushStyle enumeration ([MS-WMF] section 2.1.1.4).
        If the pen type in the PenStyle field is PS_GEOMETRIC, this value MUST be either
        BS_SOLID or BS_HATCHED. The value of this field can be BS_NULL, but only if the
        line style specified in PenStyle is PS_NULL. The BS_NULL style SHOULD be used
        to specify a brush that has no effect.'''
        raise NotImplementedError()
    
    @brush_style.setter
    def brush_style(self, value : aspose.imaging.fileformats.wmf.consts.WmfBrushStyle) -> None:
        '''Sets a 32-bit unsigned integer that specifies a brush style for the pen from the
        WMF BrushStyle enumeration ([MS-WMF] section 2.1.1.4).
        If the pen type in the PenStyle field is PS_GEOMETRIC, this value MUST be either
        BS_SOLID or BS_HATCHED. The value of this field can be BS_NULL, but only if the
        line style specified in PenStyle is PS_NULL. The BS_NULL style SHOULD be used
        to specify a brush that has no effect.'''
        raise NotImplementedError()
    
    @property
    def brush_hatch(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfHatchStyle:
        '''Gets the brush hatch pattern. The definition of this field depends on the
        BrushStyle value, as shown in the table later in this section.'''
        raise NotImplementedError()
    
    @brush_hatch.setter
    def brush_hatch(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfHatchStyle) -> None:
        '''Sets the brush hatch pattern. The definition of this field depends on the
        BrushStyle value, as shown in the table later in this section.'''
        raise NotImplementedError()
    
    @property
    def num_style_entities(self) -> int:
        '''Gets the number of elements in the array specified in the StyleEntry field.
        This value SHOULD be zero if PenStyle does not specify PS_USERSTYLE.'''
        raise NotImplementedError()
    
    @property
    def style_entry(self) -> List[int]:
        '''Gets an optional array of 32-bit unsigned integers that defines the lengths of
        dashes and gaps in the line drawn by this pen, when the value of PenStyle
        is PS_USERSTYLE line style for the pen. The array contains a number of
        entries specified by NumStyleEntries, but it is used as if it repeated indefinitely
        The first entry in the array specifies the length of the first dash. The second
        entry specifies the length of the first gap. Thereafter, lengths of dashes and gaps alternate.
        If the pen type in the PenStyle field is PS_GEOMETRIC, the lengths are specified in
        logical units; otherwise, the lengths are specified in device units.'''
        raise NotImplementedError()
    
    @style_entry.setter
    def style_entry(self, value : List[int]) -> None:
        '''Sets an optional array of 32-bit unsigned integers that defines the lengths of
        dashes and gaps in the line drawn by this pen, when the value of PenStyle
        is PS_USERSTYLE line style for the pen. The array contains a number of
        entries specified by NumStyleEntries, but it is used as if it repeated indefinitely
        The first entry in the array specifies the length of the first dash. The second
        entry specifies the length of the first gap. Thereafter, lengths of dashes and gaps alternate.
        If the pen type in the PenStyle field is PS_GEOMETRIC, the lengths are specified in
        logical units; otherwise, the lengths are specified in device units.'''
        raise NotImplementedError()
    
    @property
    def brush_dib_pattern(self) -> aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap:
        '''Gets the brush dib pattern.'''
        raise NotImplementedError()
    
    @brush_dib_pattern.setter
    def brush_dib_pattern(self, value : aspose.imaging.fileformats.wmf.objects.WmfDeviceIndependentBitmap) -> None:
        '''Sets the brush dib pattern.'''
        raise NotImplementedError()
    

class EmfObject(aspose.imaging.fileformats.emf.MetaObject):
    '''Base class for Emf objects'''
    

class EmfPanose(EmfObject):
    '''The Panose object describes the PANOSE font-classification values for a TrueType font. These
    characteristics are used to associate the font with other fonts of similar appearance but different names.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def family_type(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfFamilyType:
        '''Gets an 8-bit unsigned integer that specifies the family type. The value MUST
        be in the FamilyType (section 2.1.12) enumeration table.'''
        raise NotImplementedError()
    
    @family_type.setter
    def family_type(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfFamilyType) -> None:
        '''Sets an 8-bit unsigned integer that specifies the family type. The value MUST
        be in the FamilyType (section 2.1.12) enumeration table.'''
        raise NotImplementedError()
    
    @property
    def serif_style(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfSerifStyle:
        '''Gets an 8-bit unsigned integer that specifies the serif style. The value MUST be
        in the SerifType (section 2.1.30) enumeration table.'''
        raise NotImplementedError()
    
    @serif_style.setter
    def serif_style(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfSerifStyle) -> None:
        '''Sets an 8-bit unsigned integer that specifies the serif style. The value MUST be
        in the SerifType (section 2.1.30) enumeration table.'''
        raise NotImplementedError()
    
    @property
    def weight(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfWeight:
        '''Gets an 8-bit unsigned integer that specifies the weight of the font. The value
        MUST be in the Weight (section 2.1.34) enumeration table.'''
        raise NotImplementedError()
    
    @weight.setter
    def weight(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfWeight) -> None:
        '''Sets an 8-bit unsigned integer that specifies the weight of the font. The value
        MUST be in the Weight (section 2.1.34) enumeration table.'''
        raise NotImplementedError()
    
    @property
    def proportion(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfProportion:
        '''Gets an 8-bit unsigned integer that specifies the proportion of the font. The
        value MUST be in the Proportion (section 2.1.28) enumeration table.'''
        raise NotImplementedError()
    
    @proportion.setter
    def proportion(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfProportion) -> None:
        '''Sets an 8-bit unsigned integer that specifies the proportion of the font. The
        value MUST be in the Proportion (section 2.1.28) enumeration table.'''
        raise NotImplementedError()
    
    @property
    def contrast(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfContrast:
        '''Gets an 8-bit unsigned integer that specifies the contrast of the font. The value
        MUST be in the Contrast (section 2.1.8) enumeration table.'''
        raise NotImplementedError()
    
    @contrast.setter
    def contrast(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfContrast) -> None:
        '''Sets an 8-bit unsigned integer that specifies the contrast of the font. The value
        MUST be in the Contrast (section 2.1.8) enumeration table.'''
        raise NotImplementedError()
    
    @property
    def stroke_variation(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfStrokeVariation:
        '''Gets an 8-bit unsigned integer that specifies the stroke variation for the
        font. The value MUST be in the StrokeVariation (section 2.1.33) enumeration table.'''
        raise NotImplementedError()
    
    @stroke_variation.setter
    def stroke_variation(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfStrokeVariation) -> None:
        '''Sets an 8-bit unsigned integer that specifies the stroke variation for the
        font. The value MUST be in the StrokeVariation (section 2.1.33) enumeration table.'''
        raise NotImplementedError()
    
    @property
    def arm_style(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfArmStyle:
        '''Gets an 8-bit unsigned integer that specifies the arm style of the font. The value
        MUST be in the ArmStyle (section 2.1.3) enumeration table.'''
        raise NotImplementedError()
    
    @arm_style.setter
    def arm_style(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfArmStyle) -> None:
        '''Sets an 8-bit unsigned integer that specifies the arm style of the font. The value
        MUST be in the ArmStyle (section 2.1.3) enumeration table.'''
        raise NotImplementedError()
    
    @property
    def letterform(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfLetterform:
        '''Gets an 8-bit unsigned integer that specifies the letterform of the font. The
        value MUST be in the Letterform (section 2.1.20) enumeration table'''
        raise NotImplementedError()
    
    @letterform.setter
    def letterform(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfLetterform) -> None:
        '''Sets an 8-bit unsigned integer that specifies the letterform of the font. The
        value MUST be in the Letterform (section 2.1.20) enumeration table'''
        raise NotImplementedError()
    
    @property
    def midline(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfMidLine:
        '''Gets an 8-bit unsigned integer that specifies the midline of the font. The value
        MUST be in the MidLine (section 2.1.23) enumeration table.'''
        raise NotImplementedError()
    
    @midline.setter
    def midline(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfMidLine) -> None:
        '''Sets an 8-bit unsigned integer that specifies the midline of the font. The value
        MUST be in the MidLine (section 2.1.23) enumeration table.'''
        raise NotImplementedError()
    
    @property
    def x_height(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfXHeight:
        '''Gets an 8-bit unsigned integer that specifies the x height of the font. The value
        MUST be in the XHeight (section 2.1.35) enumeration table.'''
        raise NotImplementedError()
    
    @x_height.setter
    def x_height(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfXHeight) -> None:
        '''Sets an 8-bit unsigned integer that specifies the x height of the font. The value
        MUST be in the XHeight (section 2.1.35) enumeration table.'''
        raise NotImplementedError()
    

class EmfPixelFormatDescriptor(EmfObject):
    '''The PixelFormatDescriptor object can be used in EMR_HEADER records (section 2.3.4.2) to specify the pixel format of the output surface for the playback device context.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def n_size(self) -> int:
        '''Gets a 16-bit integer that specifies the size, in bytes, of this data structure.'''
        raise NotImplementedError()
    
    @n_size.setter
    def n_size(self, value : int) -> None:
        '''Sets a 16-bit integer that specifies the size, in bytes, of this data structure.'''
        raise NotImplementedError()
    
    @property
    def n_version(self) -> int:
        '''Gets a 16-bit integer that MUST be set to 0x0001.'''
        raise NotImplementedError()
    
    @n_version.setter
    def n_version(self, value : int) -> None:
        '''Sets a 16-bit integer that MUST be set to 0x0001.'''
        raise NotImplementedError()
    
    @property
    def dw_flags(self) -> int:
        '''Gets bit flags that specify properties of the pixel buffer that is used
        for output to the drawing surface. These properties are not all mutually
        exclusive; combinations of flags are allowed, except where noted otherwise.'''
        raise NotImplementedError()
    
    @dw_flags.setter
    def dw_flags(self, value : int) -> None:
        '''Sets bit flags that specify properties of the pixel buffer that is used
        for output to the drawing surface. These properties are not all mutually
        exclusive; combinations of flags are allowed, except where noted otherwise.'''
        raise NotImplementedError()
    
    @property
    def pixel_type(self) -> int:
        '''Gets the type of pixel data
        PFD_TYPE_RGBA       0x00 The pixel format is RGBA.
        PFD_TYPE_COLORINDEX 0x01 Each pixel is an index in a color table.'''
        raise NotImplementedError()
    
    @pixel_type.setter
    def pixel_type(self, value : int) -> None:
        '''Sets the type of pixel data
        PFD_TYPE_RGBA       0x00 The pixel format is RGBA.
        PFD_TYPE_COLORINDEX 0x01 Each pixel is an index in a color table.'''
        raise NotImplementedError()
    
    @property
    def c_color_bits(self) -> int:
        '''Gets the number of bits per pixel for RGBA pixel types, excluding the alpha bitplanes. For color table pixels, it is the size of each color table index'''
        raise NotImplementedError()
    
    @c_color_bits.setter
    def c_color_bits(self, value : int) -> None:
        '''Sets the number of bits per pixel for RGBA pixel types, excluding the alpha bitplanes. For color table pixels, it is the size of each color table index'''
        raise NotImplementedError()
    
    @property
    def c_red_bits(self) -> int:
        '''Gets  Specifies the number of red bitplanes in each RGBA color buffer'''
        raise NotImplementedError()
    
    @c_red_bits.setter
    def c_red_bits(self, value : int) -> None:
        '''Sets  Specifies the number of red bitplanes in each RGBA color buffer'''
        raise NotImplementedError()
    
    @property
    def c_red_shift(self) -> int:
        '''Gets  Specifies the shift count in bits for red bitplanes in each RGBA color buffer.'''
        raise NotImplementedError()
    
    @c_red_shift.setter
    def c_red_shift(self, value : int) -> None:
        '''Sets  Specifies the shift count in bits for red bitplanes in each RGBA color buffer.'''
        raise NotImplementedError()
    
    @property
    def c_green_bits(self) -> int:
        '''Gets  Specifies the number of green bitplanes in each RGBA color buffer'''
        raise NotImplementedError()
    
    @c_green_bits.setter
    def c_green_bits(self, value : int) -> None:
        '''Sets  Specifies the number of green bitplanes in each RGBA color buffer'''
        raise NotImplementedError()
    
    @property
    def c_green_shift(self) -> int:
        '''Gets  Specifies the shift count for green bitplanes in each RGBA color buffer.'''
        raise NotImplementedError()
    
    @c_green_shift.setter
    def c_green_shift(self, value : int) -> None:
        '''Sets  Specifies the shift count for green bitplanes in each RGBA color buffer.'''
        raise NotImplementedError()
    
    @property
    def c_blue_bits(self) -> int:
        '''Gets  Specifies the number of blue bitplanes in each RGBA color buffer.'''
        raise NotImplementedError()
    
    @c_blue_bits.setter
    def c_blue_bits(self, value : int) -> None:
        '''Sets  Specifies the number of blue bitplanes in each RGBA color buffer.'''
        raise NotImplementedError()
    
    @property
    def c_blue_shift(self) -> int:
        '''Gets  Specifies the shift count for blue bitplanes in each RGBA color buffer.'''
        raise NotImplementedError()
    
    @c_blue_shift.setter
    def c_blue_shift(self, value : int) -> None:
        '''Sets  Specifies the shift count for blue bitplanes in each RGBA color buffer.'''
        raise NotImplementedError()
    
    @property
    def c_alpha_bits(self) -> int:
        '''Gets  Specifies the number of alpha bitplanes in each RGBA color buffer'''
        raise NotImplementedError()
    
    @c_alpha_bits.setter
    def c_alpha_bits(self, value : int) -> None:
        '''Sets  Specifies the number of alpha bitplanes in each RGBA color buffer'''
        raise NotImplementedError()
    
    @property
    def c_alpha_shift(self) -> int:
        '''Gets Specifies the shift count for alpha bitplanes in each RGBA color buffer'''
        raise NotImplementedError()
    
    @c_alpha_shift.setter
    def c_alpha_shift(self, value : int) -> None:
        '''Sets Specifies the shift count for alpha bitplanes in each RGBA color buffer'''
        raise NotImplementedError()
    
    @property
    def c_accum_bits(self) -> int:
        '''Gets specifies the total number of bitplanes in the accumulation buffer.'''
        raise NotImplementedError()
    
    @c_accum_bits.setter
    def c_accum_bits(self, value : int) -> None:
        '''Sets specifies the total number of bitplanes in the accumulation buffer.'''
        raise NotImplementedError()
    
    @property
    def c_accum_red_bits(self) -> int:
        '''Gets specifies the number of red bitplanes in the accumulation buffer'''
        raise NotImplementedError()
    
    @c_accum_red_bits.setter
    def c_accum_red_bits(self, value : int) -> None:
        '''Sets specifies the number of red bitplanes in the accumulation buffer'''
        raise NotImplementedError()
    
    @property
    def c_accum_green_bits(self) -> int:
        '''Gets specifies the number of green bitplanes in the accumulation'''
        raise NotImplementedError()
    
    @c_accum_green_bits.setter
    def c_accum_green_bits(self, value : int) -> None:
        '''Sets specifies the number of green bitplanes in the accumulation'''
        raise NotImplementedError()
    
    @property
    def c_accum_blue_bits(self) -> int:
        '''Gets specifies the number of blue bitplanes in the accumulation buffer.'''
        raise NotImplementedError()
    
    @c_accum_blue_bits.setter
    def c_accum_blue_bits(self, value : int) -> None:
        '''Sets specifies the number of blue bitplanes in the accumulation buffer.'''
        raise NotImplementedError()
    
    @property
    def c_accum_alpha_bits(self) -> int:
        '''Gets specifies the number of alpha bitplanes in the accumulation buffer'''
        raise NotImplementedError()
    
    @c_accum_alpha_bits.setter
    def c_accum_alpha_bits(self, value : int) -> None:
        '''Sets specifies the number of alpha bitplanes in the accumulation buffer'''
        raise NotImplementedError()
    
    @property
    def c_depth_bits(self) -> int:
        '''Gets specifies the depth of the depth (z-axis) buffer.'''
        raise NotImplementedError()
    
    @c_depth_bits.setter
    def c_depth_bits(self, value : int) -> None:
        '''Sets specifies the depth of the depth (z-axis) buffer.'''
        raise NotImplementedError()
    
    @property
    def c_stencil_bits(self) -> int:
        '''Gets specifies the depth of the stencil buffer.'''
        raise NotImplementedError()
    
    @c_stencil_bits.setter
    def c_stencil_bits(self, value : int) -> None:
        '''Sets specifies the depth of the stencil buffer.'''
        raise NotImplementedError()
    
    @property
    def c_aux_buffers(self) -> int:
        '''Gets specifies the number of auxiliary buffers. Auxiliary buffers are not supported'''
        raise NotImplementedError()
    
    @c_aux_buffers.setter
    def c_aux_buffers(self, value : int) -> None:
        '''Sets specifies the number of auxiliary buffers. Auxiliary buffers are not supported'''
        raise NotImplementedError()
    
    @property
    def layer_type(self) -> int:
        '''Gets This field MAY be ignored'''
        raise NotImplementedError()
    
    @layer_type.setter
    def layer_type(self, value : int) -> None:
        '''Sets This field MAY be ignored'''
        raise NotImplementedError()
    
    @property
    def b_reserved(self) -> int:
        '''Gets specifies the number of overlay and underlay planes. Bits 0 through 3 specify
        up to 15 overlay planes and bits 4 through 7 specify up to 15 underlay planes'''
        raise NotImplementedError()
    
    @b_reserved.setter
    def b_reserved(self, value : int) -> None:
        '''Sets specifies the number of overlay and underlay planes. Bits 0 through 3 specify
        up to 15 overlay planes and bits 4 through 7 specify up to 15 underlay planes'''
        raise NotImplementedError()
    
    @property
    def dw_layer_mask(self) -> int:
        '''Gets This field MAY be ignored.'''
        raise NotImplementedError()
    
    @dw_layer_mask.setter
    def dw_layer_mask(self, value : int) -> None:
        '''Sets This field MAY be ignored.'''
        raise NotImplementedError()
    
    @property
    def dw_visible_mask(self) -> int:
        '''Gets specifies the transparent color or index of an underlay plane. When the pixel
        type is RGBA, dwVisibleMask is a transparent RGB color value. When the pixel
        type is color index, it is a transparent index value.'''
        raise NotImplementedError()
    
    @dw_visible_mask.setter
    def dw_visible_mask(self, value : int) -> None:
        '''Sets specifies the transparent color or index of an underlay plane. When the pixel
        type is RGBA, dwVisibleMask is a transparent RGB color value. When the pixel
        type is color index, it is a transparent index value.'''
        raise NotImplementedError()
    
    @property
    def dw_damage_mask(self) -> int:
        '''Gets This field MAY be ignored'''
        raise NotImplementedError()
    
    @dw_damage_mask.setter
    def dw_damage_mask(self, value : int) -> None:
        '''Sets This field MAY be ignored'''
        raise NotImplementedError()
    

class EmfPoint28To4(EmfObject):
    '''The Point28_4 object represents the location of a point on a device surface with coordinates in 28.4 bit FIX notation.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def x(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfBitFix28To4:
        '''Gets a BitFIX28_4 object (section 2.2.1) that represents the horizontal coordinate of the point.'''
        raise NotImplementedError()
    
    @x.setter
    def x(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfBitFix28To4) -> None:
        '''Sets a BitFIX28_4 object (section 2.2.1) that represents the horizontal coordinate of the point.'''
        raise NotImplementedError()
    
    @property
    def y(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfBitFix28To4:
        '''Gets a BitFIX28_4 object that represents the vertical coordinate of the point.'''
        raise NotImplementedError()
    
    @y.setter
    def y(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfBitFix28To4) -> None:
        '''Sets a BitFIX28_4 object that represents the vertical coordinate of the point.'''
        raise NotImplementedError()
    

class EmfRegionData(EmfObject):
    '''The RegionData object specifies data that defines a region, which is made of non-overlapping rectangles.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfRegionData` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, rectangle : aspose.imaging.Rectangle) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.emf.emf.objects.EmfRegionData` class.
        
        :param rectangle: The rectangle.'''
        raise NotImplementedError()
    
    @property
    def region_data_header(self) -> aspose.imaging.fileformats.emf.emf.objects.EmfRegionDataHeader:
        '''Gets a 256-bit RegionDataHeader object that describes the following data.'''
        raise NotImplementedError()
    
    @region_data_header.setter
    def region_data_header(self, value : aspose.imaging.fileformats.emf.emf.objects.EmfRegionDataHeader) -> None:
        '''Sets a 256-bit RegionDataHeader object that describes the following data.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[aspose.imaging.Rectangle]:
        '''Gets an array of WMF RectL objects ([MS-WMF] section 2.2.2.19); the objects are
        merged to create the region'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : List[aspose.imaging.Rectangle]) -> None:
        '''Sets an array of WMF RectL objects ([MS-WMF] section 2.2.2.19); the objects are
        merged to create the region'''
        raise NotImplementedError()
    

class EmfRegionDataHeader(EmfObject):
    '''The RegionDataHeader object describes the properties of a RegionData object.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the size of this object in bytes. This MUST be 0x00000020.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the size of this object in bytes. This MUST be 0x00000020.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the region type. This SHOULD be
        RDH_RECTANGLES (0x00000001).'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the region type. This SHOULD be
        RDH_RECTANGLES (0x00000001).'''
        raise NotImplementedError()
    
    @property
    def count_rects(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of rectangles in this region.'''
        raise NotImplementedError()
    
    @count_rects.setter
    def count_rects(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of rectangles in this region.'''
        raise NotImplementedError()
    
    @property
    def rgn_size(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the size of the buffer of rectangles in bytes.'''
        raise NotImplementedError()
    
    @rgn_size.setter
    def rgn_size(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the size of the buffer of rectangles in bytes.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets a 128-bit WMF RectL object ([MS-WMF] section 2.2.2.19), which specifies
        the bounds of the region.'''
        raise NotImplementedError()
    
    @bounds.setter
    def bounds(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets a 128-bit WMF RectL object ([MS-WMF] section 2.2.2.19), which specifies
        the bounds of the region.'''
        raise NotImplementedError()
    

class EmfText(EmfObject):
    '''The EmrText object contains values for text output.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def reference(self) -> aspose.imaging.Point:
        '''Gets a WMF PointL object ([MS-WMF] section 2.2.2.15) that specifies the coordinates of the
        reference point used to position the string. The reference point is defined by the last
        EMR_SETTEXTALIGN record (section 2.3.11.25). If no such record has been set,
        the default alignment is TA_LEFT,TA_TOP.'''
        raise NotImplementedError()
    
    @reference.setter
    def reference(self, value : aspose.imaging.Point) -> None:
        '''Sets a WMF PointL object ([MS-WMF] section 2.2.2.15) that specifies the coordinates of the
        reference point used to position the string. The reference point is defined by the last
        EMR_SETTEXTALIGN record (section 2.3.11.25). If no such record has been set,
        the default alignment is TA_LEFT,TA_TOP.'''
        raise NotImplementedError()
    
    @property
    def chars(self) -> int:
        '''Gets a 32-bit unsigned integer that specifies the number of characters in the string'''
        raise NotImplementedError()
    
    @chars.setter
    def chars(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that specifies the number of characters in the string'''
        raise NotImplementedError()
    
    @property
    def options(self) -> aspose.imaging.fileformats.emf.emf.consts.EmfExtTextOutOptions:
        '''Gets a 32-bit unsigned integer that specifies how to use the rectangle specified in the
        Rectangle field. This field can be a combination of more than one ExtTextOutOptions
        enumeration (section 2.1.11) values'''
        raise NotImplementedError()
    
    @options.setter
    def options(self, value : aspose.imaging.fileformats.emf.emf.consts.EmfExtTextOutOptions) -> None:
        '''Sets a 32-bit unsigned integer that specifies how to use the rectangle specified in the
        Rectangle field. This field can be a combination of more than one ExtTextOutOptions
        enumeration (section 2.1.11) values'''
        raise NotImplementedError()
    
    @property
    def rectangle(self) -> aspose.imaging.Rectangle:
        '''Gets an optional WMF RectL object ([MS-WMF] section 2.2.2.19) that defines a clipping
        and/or opaquing rectangle in logical units. This rectangle is applied to the text
        output performed by the containing record.'''
        raise NotImplementedError()
    
    @rectangle.setter
    def rectangle(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets an optional WMF RectL object ([MS-WMF] section 2.2.2.19) that defines a clipping
        and/or opaquing rectangle in logical units. This rectangle is applied to the text
        output performed by the containing record.'''
        raise NotImplementedError()
    
    @property
    def string_buffer(self) -> str:
        '''Gets the character string buffer
        UndefinedSpace1 (variable): An optional number of unused bytes.
        The OutputString field is not required to follow immediately the preceding portion of this structure.
        OutputString (variable): An array of characters that specify the string to output.
        The location of this field is specified by the value of offString in bytes from the start of this record.
        The number of characters is specified by the value of Chars.'''
        raise NotImplementedError()
    
    @string_buffer.setter
    def string_buffer(self, value : str) -> None:
        '''Sets the character string buffer
        UndefinedSpace1 (variable): An optional number of unused bytes.
        The OutputString field is not required to follow immediately the preceding portion of this structure.
        OutputString (variable): An array of characters that specify the string to output.
        The location of this field is specified by the value of offString in bytes from the start of this record.
        The number of characters is specified by the value of Chars.'''
        raise NotImplementedError()
    
    @property
    def glyph_index_buffer(self) -> List[int]:
        '''Gets the optional glyph index buffer.
        If options has ETO_GLYPH_INDEX flag then the codes for characters in an output text string are actually indexes
        of the character glyphs in a TrueType font (2.1.11 ExtTextOutOptions enumeration). Glyph indexes are font-specific,
        so to display the correct characters on playback, the font that is used MUST be identical to the font used to
        generate the indexes.'''
        raise NotImplementedError()
    
    @glyph_index_buffer.setter
    def glyph_index_buffer(self, value : List[int]) -> None:
        '''Sets the optional glyph index buffer.
        If options has ETO_GLYPH_INDEX flag then the codes for characters in an output text string are actually indexes
        of the character glyphs in a TrueType font (2.1.11 ExtTextOutOptions enumeration). Glyph indexes are font-specific,
        so to display the correct characters on playback, the font that is used MUST be identical to the font used to
        generate the indexes.'''
        raise NotImplementedError()
    
    @property
    def dx_buffer(self) -> List[int]:
        '''Gets the optional character spacing buffer
        UndefinedSpace2 (variable): An optional number of unused bytes. The OutputDx field is not required to
        follow immediately the preceding portion of this structure.
        OutputDx (variable): An array of 32-bit unsigned integers that specify the output spacing between
        the origins of adjacent character cells in logical units. The location of this field is specified by
        the value of offDx in bytes from the start of this record. If spacing is defined, this field contains
        the same number of values as characters in the output string. If the Options field of the EmrText object
        contains the ETO_PDY flag, then this buffer contains twice as many values as there are characters in
        the output string, one horizontal and one vertical offset for each, in that order. If ETO_RTLREADING is specified,
        characters are laid right to left instead of left to right. No other options affect the interpretation of this field.'''
        raise NotImplementedError()
    
    @dx_buffer.setter
    def dx_buffer(self, value : List[int]) -> None:
        '''Sets the optional character spacing buffer
        UndefinedSpace2 (variable): An optional number of unused bytes. The OutputDx field is not required to
        follow immediately the preceding portion of this structure.
        OutputDx (variable): An array of 32-bit unsigned integers that specify the output spacing between
        the origins of adjacent character cells in logical units. The location of this field is specified by
        the value of offDx in bytes from the start of this record. If spacing is defined, this field contains
        the same number of values as characters in the output string. If the Options field of the EmrText object
        contains the ETO_PDY flag, then this buffer contains twice as many values as there are characters in
        the output string, one horizontal and one vertical offset for each, in that order. If ETO_RTLREADING is specified,
        characters are laid right to left instead of left to right. No other options affect the interpretation of this field.'''
        raise NotImplementedError()
    

class EmfTriVertex(EmfObject):
    '''The TriVertex object specifies color and position information for the definition of a rectangle or
    triangle vertex.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def x(self) -> int:
        '''Gets a 32-bit signed integer that specifies the horizontal position, in logical units.'''
        raise NotImplementedError()
    
    @x.setter
    def x(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the horizontal position, in logical units.'''
        raise NotImplementedError()
    
    @property
    def y(self) -> int:
        '''Gets a 32-bit signed integer that specifies the vertical position, in logical units.'''
        raise NotImplementedError()
    
    @y.setter
    def y(self, value : int) -> None:
        '''Sets a 32-bit signed integer that specifies the vertical position, in logical units.'''
        raise NotImplementedError()
    
    @property
    def red(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the red color value for the point.'''
        raise NotImplementedError()
    
    @red.setter
    def red(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the red color value for the point.'''
        raise NotImplementedError()
    
    @property
    def green(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the green color value for the point.'''
        raise NotImplementedError()
    
    @green.setter
    def green(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the green color value for the point.'''
        raise NotImplementedError()
    
    @property
    def blue(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the blue color value for the point.'''
        raise NotImplementedError()
    
    @blue.setter
    def blue(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the blue color value for the point.'''
        raise NotImplementedError()
    
    @property
    def alpha(self) -> int:
        '''Gets a 16-bit unsigned integer that specifies the alpha transparency value for the point.'''
        raise NotImplementedError()
    
    @alpha.setter
    def alpha(self, value : int) -> None:
        '''Sets a 16-bit unsigned integer that specifies the alpha transparency value for the point.'''
        raise NotImplementedError()
    

class EmfUniversalFontId(EmfObject):
    '''The UniversalFontId object defines a mechanism for identifying fonts in EMF metafiles.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def checksum(self) -> int:
        '''Gets a 32-bit unsigned integer that is the checksum of the font.
        The checksum value has the following meanings.
        0x00000000  The object is a device font.
        0x00000001  The object is a Type 1 font that has been installed on the client machine and is
        enumerated by the PostScript printer driver as a device font.
        0x00000002  The object is not a font but is a Type 1 rasterizer.
        3 ≤ value   The object is a bitmap, vector, or TrueType font, or a Type 1 rasterized font that
        was created by a Type 1 rasterizer.'''
        raise NotImplementedError()
    
    @checksum.setter
    def checksum(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that is the checksum of the font.
        The checksum value has the following meanings.
        0x00000000  The object is a device font.
        0x00000001  The object is a Type 1 font that has been installed on the client machine and is
        enumerated by the PostScript printer driver as a device font.
        0x00000002  The object is not a font but is a Type 1 rasterizer.
        3 ≤ value   The object is a bitmap, vector, or TrueType font, or a Type 1 rasterized font that
        was created by a Type 1 rasterizer.'''
        raise NotImplementedError()
    
    @property
    def index(self) -> int:
        '''Gets a 32-bit unsigned integer that is an index associated with the font object. The
        meaning of this field is determined by the type of font.'''
        raise NotImplementedError()
    
    @index.setter
    def index(self, value : int) -> None:
        '''Sets a 32-bit unsigned integer that is an index associated with the font object. The
        meaning of this field is determined by the type of font.'''
        raise NotImplementedError()
    

