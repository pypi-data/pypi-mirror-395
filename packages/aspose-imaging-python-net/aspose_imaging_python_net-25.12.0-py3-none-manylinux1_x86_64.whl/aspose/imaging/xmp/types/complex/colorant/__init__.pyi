"""The namespace contains classes that represent the structures containing the characteristics of a colorant (swatch) used in a document."""
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

class ColorantBase(aspose.imaging.xmp.types.complex.ComplexTypeBase):
    '''Represents XMP Colorant type.'''
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones this instance.
        
        :returns: A memberwise clone.'''
        raise NotImplementedError()
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        raise NotImplementedError()
    
    @property
    def namespace_uri(self) -> str:
        '''Gets the default namespace URI.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> aspose.imaging.xmp.types.complex.colorant.ColorMode:
        '''Gets :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorMode`.'''
        raise NotImplementedError()
    
    @property
    def swatch_name(self) -> str:
        '''Gets the name of the swatch.'''
        raise NotImplementedError()
    
    @swatch_name.setter
    def swatch_name(self, value : str) -> None:
        '''Sets the name of the swatch.'''
        raise NotImplementedError()
    
    @property
    def color_type(self) -> aspose.imaging.xmp.types.complex.colorant.ColorType:
        '''Gets the type of the color.'''
        raise NotImplementedError()
    
    @color_type.setter
    def color_type(self, value : aspose.imaging.xmp.types.complex.colorant.ColorType) -> None:
        '''Sets the type of the color.'''
        raise NotImplementedError()
    

class ColorantCmyk(ColorantBase):
    '''Represents CMYK Colorant.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorantCmyk` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, black : float, cyan : float, magenta : float, yellow : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorantCmyk` class.
        
        :param black: The black component value.
        :param cyan: The cyan color component value.
        :param magenta: The magenta component value.
        :param yellow: The yellow component value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones this instance.
        
        :returns: A memberwise clone.'''
        raise NotImplementedError()
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        raise NotImplementedError()
    
    @property
    def namespace_uri(self) -> str:
        '''Gets the default namespace URI.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> aspose.imaging.xmp.types.complex.colorant.ColorMode:
        '''Gets :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorMode`.'''
        raise NotImplementedError()
    
    @property
    def swatch_name(self) -> str:
        '''Gets the name of the swatch.'''
        raise NotImplementedError()
    
    @swatch_name.setter
    def swatch_name(self, value : str) -> None:
        '''Sets the name of the swatch.'''
        raise NotImplementedError()
    
    @property
    def color_type(self) -> aspose.imaging.xmp.types.complex.colorant.ColorType:
        '''Gets the type of the color.'''
        raise NotImplementedError()
    
    @color_type.setter
    def color_type(self, value : aspose.imaging.xmp.types.complex.colorant.ColorType) -> None:
        '''Sets the type of the color.'''
        raise NotImplementedError()
    
    @property
    def black(self) -> float:
        '''Gets the black component value.'''
        raise NotImplementedError()
    
    @black.setter
    def black(self, value : float) -> None:
        '''Sets the black component value.'''
        raise NotImplementedError()
    
    @property
    def cyan(self) -> float:
        '''Gets the cyan component value.'''
        raise NotImplementedError()
    
    @cyan.setter
    def cyan(self, value : float) -> None:
        '''Sets the cyan component value.'''
        raise NotImplementedError()
    
    @property
    def magenta(self) -> float:
        '''Gets the magenta component value.'''
        raise NotImplementedError()
    
    @magenta.setter
    def magenta(self, value : float) -> None:
        '''Sets the magenta component value.'''
        raise NotImplementedError()
    
    @property
    def yellow(self) -> float:
        '''Gets the yellow component value.'''
        raise NotImplementedError()
    
    @yellow.setter
    def yellow(self, value : float) -> None:
        '''Sets the yellow component value.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def COLOR_VALUE_MAX() -> float:
        '''Color max value in CMYK colorant.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def COLOR_VALUE_MIN() -> float:
        '''Color min value in CMYK colorant.'''
        raise NotImplementedError()


class ColorantLab(ColorantBase):
    '''Represents LAB Colorant.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorantLab` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, a : int, b : int, l : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorantLab` class.
        
        :param a: A component.
        :param b: B component.
        :param l: L component.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones this instance.
        
        :returns: A memberwise clone.'''
        raise NotImplementedError()
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        raise NotImplementedError()
    
    @property
    def namespace_uri(self) -> str:
        '''Gets the default namespace URI.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> aspose.imaging.xmp.types.complex.colorant.ColorMode:
        '''Gets :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorMode`.'''
        raise NotImplementedError()
    
    @property
    def swatch_name(self) -> str:
        '''Gets the name of the swatch.'''
        raise NotImplementedError()
    
    @swatch_name.setter
    def swatch_name(self, value : str) -> None:
        '''Sets the name of the swatch.'''
        raise NotImplementedError()
    
    @property
    def color_type(self) -> aspose.imaging.xmp.types.complex.colorant.ColorType:
        '''Gets the type of the color.'''
        raise NotImplementedError()
    
    @color_type.setter
    def color_type(self, value : aspose.imaging.xmp.types.complex.colorant.ColorType) -> None:
        '''Sets the type of the color.'''
        raise NotImplementedError()
    
    @property
    def a(self) -> int:
        '''Gets the A component.'''
        raise NotImplementedError()
    
    @a.setter
    def a(self, value : int) -> None:
        '''Sets the A component.'''
        raise NotImplementedError()
    
    @property
    def b(self) -> int:
        '''Gets the B component.'''
        raise NotImplementedError()
    
    @b.setter
    def b(self, value : int) -> None:
        '''Sets the B component.'''
        raise NotImplementedError()
    
    @property
    def l(self) -> float:
        '''Gets the L component.'''
        raise NotImplementedError()
    
    @l.setter
    def l(self, value : float) -> None:
        '''Sets the L component.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def MIN_A() -> int:
        '''The minimum A component value'''
        raise NotImplementedError()

    @staticmethod
    @property
    def MAX_A() -> int:
        '''The maximum A component value'''
        raise NotImplementedError()

    @staticmethod
    @property
    def MIN_B() -> int:
        '''The minimum B component value'''
        raise NotImplementedError()

    @staticmethod
    @property
    def MAX_B() -> int:
        '''The maximum A component value'''
        raise NotImplementedError()

    @staticmethod
    @property
    def MIN_L() -> float:
        '''The minimum L component value'''
        raise NotImplementedError()

    @staticmethod
    @property
    def MAX_L() -> float:
        '''The maximum A component value'''
        raise NotImplementedError()


class ColorantRgb(ColorantBase):
    '''Represents RGB Colorant.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorantRgb` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, red : int, green : int, blue : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorantRgb` class.
        
        :param red: The red component value.
        :param green: The green component value.
        :param blue: The blue component value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones this instance.
        
        :returns: A memberwise clone.'''
        raise NotImplementedError()
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        raise NotImplementedError()
    
    @property
    def namespace_uri(self) -> str:
        '''Gets the default namespace URI.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> aspose.imaging.xmp.types.complex.colorant.ColorMode:
        '''Gets :py:class:`aspose.imaging.xmp.types.complex.colorant.ColorMode`.'''
        raise NotImplementedError()
    
    @property
    def swatch_name(self) -> str:
        '''Gets the name of the swatch.'''
        raise NotImplementedError()
    
    @swatch_name.setter
    def swatch_name(self, value : str) -> None:
        '''Sets the name of the swatch.'''
        raise NotImplementedError()
    
    @property
    def color_type(self) -> aspose.imaging.xmp.types.complex.colorant.ColorType:
        '''Gets the type of the color.'''
        raise NotImplementedError()
    
    @color_type.setter
    def color_type(self, value : aspose.imaging.xmp.types.complex.colorant.ColorType) -> None:
        '''Sets the type of the color.'''
        raise NotImplementedError()
    
    @property
    def red(self) -> int:
        '''Gets the red component value.'''
        raise NotImplementedError()
    
    @red.setter
    def red(self, value : int) -> None:
        '''Sets the red component value.'''
        raise NotImplementedError()
    
    @property
    def green(self) -> int:
        '''Gets the green component value.'''
        raise NotImplementedError()
    
    @green.setter
    def green(self, value : int) -> None:
        '''Sets the green component value.'''
        raise NotImplementedError()
    
    @property
    def blue(self) -> int:
        '''Gets the blue component value.'''
        raise NotImplementedError()
    
    @blue.setter
    def blue(self, value : int) -> None:
        '''Sets the blue component value.'''
        raise NotImplementedError()
    

class ColorMode(enum.Enum):
    CMYK = enum.auto()
    '''CMYK color mode.'''
    RGB = enum.auto()
    '''RGB color mode.'''
    LAB = enum.auto()
    '''LAB color mode.'''

class ColorType(enum.Enum):
    PROCESS = enum.auto()
    '''Process color type.'''
    SPOT = enum.auto()
    '''Spot color type.'''

