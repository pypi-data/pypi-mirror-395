"""The namespace contains the Complex class."""
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

class Complex:
    '''The complex number structure.'''
    
    @overload
    def __init__(self, real : float, imaginary : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.complexutils.Complex` struct.
        
        :param real: The real part.
        :param imaginary: The imaginary part.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, c : aspose.imaging.imagefilters.complexutils.Complex) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.complexutils.Complex` struct.
        
        :param c: The complex number.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def add(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Adds ``a`` and ``b``.
        
        :param a: The a complex.
        :param b: The b complex.
        :returns: The sum complex.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def add(a : aspose.imaging.imagefilters.complexutils.Complex, s : float) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Adds ``a`` and ``s``.
        
        :param a: The a complex.
        :param s: The s value.
        :returns: The complex with its Re increased by ``s``.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def add(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Adds ``a`` and ``b``.
        
        :param a: The a complex.
        :param b: The b complex.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def add(a : aspose.imaging.imagefilters.complexutils.Complex, s : float, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Adds ``a`` and ``s``.
        
        :param a: The a complex.
        :param s: The s value.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def subtract(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Subtracts ``b`` from ``a``.
        
        :param a: The a complex.
        :param b: The b complex.
        :returns: The result of subtraction.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def subtract(a : aspose.imaging.imagefilters.complexutils.Complex, s : float) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Subtracts ``s`` from ``a``.
        
        :param a: The a complex.
        :param s: The s value.
        :returns: The result of subtraction.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def subtract(s : float, a : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Subtracts ``s`` from ``a``.
        
        :param s: The s value.
        :param a: The a complex.
        :returns: The result of subtraction.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def subtract(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Subtracts ``b`` from ``a``.
        
        :param a: The a complex.
        :param b: The b complex.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def subtract(a : aspose.imaging.imagefilters.complexutils.Complex, s : float, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Subtracts ``s`` from ``a``.
        
        :param a: The a complex.
        :param s: The s value.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def subtract(s : float, a : aspose.imaging.imagefilters.complexutils.Complex, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Subtracts ``a`` from ``s``.
        
        :param s: The s value.
        :param a: The a complex.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def multiply(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Multiplies ``a`` by ``b``.
        
        :param a: The a complex.
        :param b: The b complex.
        :returns: The result of multiplication.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def multiply(a : aspose.imaging.imagefilters.complexutils.Complex, s : float) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Multiplies ``a`` by ``s``.
        
        :param a: The a complex.
        :param s: The s value.
        :returns: The result of multiplication.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def multiply(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Multiplies ``a`` by ``b``.
        
        :param a: The a complex.
        :param b: The b complex.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def multiply(a : aspose.imaging.imagefilters.complexutils.Complex, s : float, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Multiplies ``a`` by ``s``.
        
        :param a: The a complex.
        :param s: The s value.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def divide(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Divides ``a`` by ``b``.
        
        :param a: The a complex.
        :param b: The b complex.
        :returns: The result of division.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def divide(a : aspose.imaging.imagefilters.complexutils.Complex, s : float) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Divides ``a`` by ``s``.
        
        :param a: The a complex.
        :param s: The s value.
        :returns: The result of division.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def divide(s : float, a : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Divides ``a`` by ``s``.
        
        :param s: The s value.
        :param a: The a complex.
        :returns: The result of division.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def divide(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Divides ``a`` by ``b``.
        
        :param a: The a complex.
        :param b: The b complex.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def divide(a : aspose.imaging.imagefilters.complexutils.Complex, s : float, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Divides ``a`` by ``s``.
        
        :param a: The a complex.
        :param s: The s value.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def divide(s : float, a : aspose.imaging.imagefilters.complexutils.Complex, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Divides ``s`` by ``a``.
        
        :param s: The s value.
        :param a: The a complex.
        :param result: The result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def approx_equal(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex) -> bool:
        '''Checks approximate equality.
        
        :param a: The a complex.
        :param b: The b complex.
        :returns: The approximate equality result.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def approx_equal(a : aspose.imaging.imagefilters.complexutils.Complex, b : aspose.imaging.imagefilters.complexutils.Complex, tolerance : float) -> bool:
        '''Checks approximate equality.
        
        :param a: The a complex.
        :param b: The b complex.
        :param tolerance: The tolerance.
        :returns: The approximate equality result.'''
        raise NotImplementedError()
    
    @staticmethod
    def negate(a : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Negates ``a``.
        
        :param a: The a complex.
        :returns: The result of negation.'''
        raise NotImplementedError()
    
    @staticmethod
    def parse(s : str) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Parses the specified ``s`` into a :py:class:`aspose.imaging.imagefilters.complexutils.Complex`.
        
        :param s: The s value.
        :returns: The complex number.'''
        raise NotImplementedError()
    
    @staticmethod
    def try_parse(s : str, result : List[aspose.imaging.imagefilters.complexutils.Complex]) -> bool:
        '''Tries to parse the specified ``s`` into a :py:class:`aspose.imaging.imagefilters.complexutils.Complex`.
        
        :param s: The s value.
        :param result: The result.
        :returns: True, if the complex number is parsed.'''
        raise NotImplementedError()
    
    @staticmethod
    def sqrt(a : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Gets square root of ``a``.
        
        :param a: The a complex.
        :returns: The square root.'''
        raise NotImplementedError()
    
    @staticmethod
    def log(a : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Gets log of ``a``.
        
        :param a: The a complex.
        :returns: The log of ``a``.'''
        raise NotImplementedError()
    
    @staticmethod
    def exp(a : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Raises e by ``a``.
        
        :param a: The a complex.
        :returns: e raised by ``a``.'''
        raise NotImplementedError()
    
    @staticmethod
    def sin(a : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Gets Sin of ``a``.
        
        :param a: The a complex.
        :returns: Sin of ``a``.'''
        raise NotImplementedError()
    
    @staticmethod
    def cos(a : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Gets Cos of ``a``.
        
        :param a: The a complex.
        :returns: Cos of ``a``.'''
        raise NotImplementedError()
    
    @staticmethod
    def tan(a : aspose.imaging.imagefilters.complexutils.Complex) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Gets Tan of ``a``.
        
        :param a: The a complex.
        :returns: Tan of ``a``.'''
        raise NotImplementedError()
    
    def equals(self, other : aspose.imaging.imagefilters.complexutils.Complex) -> bool:
        '''Determines whether the specified :py:class:`Any`, is equal to this instance.
        
        :param other: The :py:class:`Any` to compare with this instance.
        :returns: ``true`` if the specified :py:class:`Any` is equal to this instance; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def clone(self) -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Clones this instance.
        
        :returns: A clone of this complex.'''
        raise NotImplementedError()
    
    @property
    def re(self) -> float:
        '''Gets the real part.'''
        raise NotImplementedError()
    
    @re.setter
    def re(self, value : float) -> None:
        '''Sets the real part.'''
        raise NotImplementedError()
    
    @property
    def im(self) -> float:
        '''Gets the imaginary part.'''
        raise NotImplementedError()
    
    @im.setter
    def im(self, value : float) -> None:
        '''Sets the imaginary part.'''
        raise NotImplementedError()
    
    @property
    def magnitude(self) -> float:
        '''Gets the magnitude.'''
        raise NotImplementedError()
    
    @property
    def phase(self) -> float:
        '''Gets the phase.'''
        raise NotImplementedError()
    
    @property
    def squared_magnitude(self) -> float:
        '''Gets the squared magnitude.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def SIZE_OF_DOUBLE() -> int:
        '''The size of :py:class:`float`.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def SIZE_OF_COMPLEX() -> int:
        '''The size of complex.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def ZERO() -> aspose.imaging.imagefilters.complexutils.Complex:
        '''Zero complex.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def ONE() -> aspose.imaging.imagefilters.complexutils.Complex:
        '''One complex having :py:attr:`aspose.imaging.imagefilters.complexutils.Complex.re` and :py:attr:`aspose.imaging.imagefilters.complexutils.Complex.im` equal to 1.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def I() -> aspose.imaging.imagefilters.complexutils.Complex:
        '''I complex having :py:attr:`aspose.imaging.imagefilters.complexutils.Complex.im` equal to 1.'''
        raise NotImplementedError()


