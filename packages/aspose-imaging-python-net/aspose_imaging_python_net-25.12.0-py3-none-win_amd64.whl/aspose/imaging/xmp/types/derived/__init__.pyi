"""The namespace contains classes that represent the derived type values of XMP properties."""
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

class Rational(aspose.imaging.xmp.types.XmpTypeBase):
    '''Represents XMP Rational.'''
    
    def __init__(self, numerator : int, denominator : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.derived.Rational` class.
        
        :param numerator: The numerator.
        :param denominator: The denominator.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Gets thestring contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones this instance.
        
        :returns: A memberwise clone.'''
        raise NotImplementedError()
    
    @property
    def numerator(self) -> int:
        '''Gets the numerator.'''
        raise NotImplementedError()
    
    @property
    def denominator(self) -> int:
        '''Gets the denominator.'''
        raise NotImplementedError()
    
    @denominator.setter
    def denominator(self, value : int) -> None:
        '''Sets the denominator.'''
        raise NotImplementedError()
    
    @property
    def float_value(self) -> float:
        '''Gets the float value.'''
        raise NotImplementedError()
    

class RenditionClass(aspose.imaging.xmp.types.XmpTypeBase):
    '''Represents the XMP Rendition.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.derived.RenditionClass` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, token : str, value : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.derived.RenditionClass` class.
        
        :param token: The token.
        :param value: The value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones this instance.
        
        :returns: A memberwise clone.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def defined_values() -> List[str]:
        '''The defined values'''
        raise NotImplementedError()

    @property
    def token(self) -> str:
        '''Gets the token.'''
        raise NotImplementedError()
    
    @token.setter
    def token(self, value : str) -> None:
        '''Sets the token.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> str:
        '''Gets the value.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : str) -> None:
        '''Sets the value.'''
        raise NotImplementedError()
    

class XmpAgentName(aspose.imaging.xmp.types.basic.XmpText):
    '''Represents Agent name, Software organization etc.'''
    
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.derived.XmpAgentName` class.
        
        :param value: The value.'''
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
    def value(self) -> str:
        '''Gets the text value.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : str) -> None:
        '''Sets the text value.'''
        raise NotImplementedError()
    

class XmpGuid(aspose.imaging.xmp.types.XmpTypeBase):
    '''Represents XMP global unique identifier.'''
    
    @overload
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.derived.XmpGuid` class.
        
        :param value: The value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, guid : UUID) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.derived.XmpGuid` class.
        
        :param guid: The unique identifier.'''
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
        '''Gets the prefix like uuid.'''
        raise NotImplementedError()
    
    @prefix.setter
    def prefix(self, value : str) -> None:
        '''Sets the prefix like uuid.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> UUID:
        '''Gets the value.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : UUID) -> None:
        '''Sets the value.'''
        raise NotImplementedError()
    

class XmpLocale(aspose.imaging.xmp.types.basic.XmpText):
    '''Represents language code.'''
    
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.derived.XmpLocale` class.
        
        :param value: The value.'''
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
    def value(self) -> str:
        '''Gets the text value.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : str) -> None:
        '''Sets the text value.'''
        raise NotImplementedError()
    

class XmpMimeType(aspose.imaging.xmp.types.basic.XmpText):
    '''Represents MIME type.'''
    
    def __init__(self, value : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.types.derived.XmpMimeType` class.
        
        :param value: The value.'''
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
    def value(self) -> str:
        '''Gets the text value.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : str) -> None:
        '''Sets the text value.'''
        raise NotImplementedError()
    

