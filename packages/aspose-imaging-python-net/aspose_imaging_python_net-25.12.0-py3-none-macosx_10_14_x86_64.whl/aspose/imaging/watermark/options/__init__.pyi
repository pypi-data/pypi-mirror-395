"""The namespace handles Watermark options processing."""
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

class ContentAwareFillWatermarkOptions(WatermarkOptions):
    '''The common Content Aware Fill Algorithm options.'''
    
    @overload
    def __init__(self, mask : List[aspose.imaging.Point]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.watermark.options.ContentAwareFillWatermarkOptions` class.
        
        :param mask: The mask for the unknown area.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, mask : aspose.imaging.GraphicsPath) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.watermark.options.ContentAwareFillWatermarkOptions` class.
        
        :param mask: The mask for the unknown area.'''
        raise NotImplementedError()
    
    @property
    def mask(self) -> Iterable[aspose.imaging.Point]:
        '''Gets the mask.'''
        raise NotImplementedError()
    
    @mask.setter
    def mask(self, value : Iterable[aspose.imaging.Point]) -> None:
        '''Sets the mask.'''
        raise NotImplementedError()
    
    @property
    def graphics_path_mask(self) -> aspose.imaging.GraphicsPath:
        '''Gets the mask.'''
        raise NotImplementedError()
    
    @graphics_path_mask.setter
    def graphics_path_mask(self, value : aspose.imaging.GraphicsPath) -> None:
        '''Sets the mask.'''
        raise NotImplementedError()
    
    @property
    def patch_size(self) -> int:
        '''Gets the patch size (should be odd).'''
        raise NotImplementedError()
    
    @patch_size.setter
    def patch_size(self, value : int) -> None:
        '''Sets the patch size (should be odd).'''
        raise NotImplementedError()
    
    @property
    def max_painting_attempts(self) -> int:
        '''Gets the maximum number of painting attempts.
        The algorithm will chose the best variant.'''
        raise NotImplementedError()
    
    @max_painting_attempts.setter
    def max_painting_attempts(self, value : int) -> None:
        '''Sets the maximum number of painting attempts.
        The algorithm will chose the best variant.'''
        raise NotImplementedError()
    
    @property
    def interest_area(self) -> aspose.imaging.Rectangle:
        '''Gets the area to take patches.'''
        raise NotImplementedError()
    
    @interest_area.setter
    def interest_area(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the area to take patches.'''
        raise NotImplementedError()
    

class TeleaWatermarkOptions(WatermarkOptions):
    '''The common Telea Algorithm options.'''
    
    @overload
    def __init__(self, mask : List[aspose.imaging.Point]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.watermark.options.TeleaWatermarkOptions` class.
        
        :param mask: The mask for the unknown area.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, mask : aspose.imaging.GraphicsPath) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.watermark.options.TeleaWatermarkOptions` class.
        
        :param mask: The mask for the unknown area.'''
        raise NotImplementedError()
    
    @property
    def mask(self) -> Iterable[aspose.imaging.Point]:
        '''Gets the mask.'''
        raise NotImplementedError()
    
    @mask.setter
    def mask(self, value : Iterable[aspose.imaging.Point]) -> None:
        '''Sets the mask.'''
        raise NotImplementedError()
    
    @property
    def graphics_path_mask(self) -> aspose.imaging.GraphicsPath:
        '''Gets the mask.'''
        raise NotImplementedError()
    
    @graphics_path_mask.setter
    def graphics_path_mask(self, value : aspose.imaging.GraphicsPath) -> None:
        '''Sets the mask.'''
        raise NotImplementedError()
    
    @property
    def half_patch_size(self) -> int:
        '''Gets the half patch size.'''
        raise NotImplementedError()
    
    @half_patch_size.setter
    def half_patch_size(self, value : int) -> None:
        '''Sets the half patch size.'''
        raise NotImplementedError()
    

class WatermarkOptions:
    '''The common watermark remover algorithm options.'''
    
    @property
    def mask(self) -> Iterable[aspose.imaging.Point]:
        '''Gets the mask.'''
        raise NotImplementedError()
    
    @mask.setter
    def mask(self, value : Iterable[aspose.imaging.Point]) -> None:
        '''Sets the mask.'''
        raise NotImplementedError()
    
    @property
    def graphics_path_mask(self) -> aspose.imaging.GraphicsPath:
        '''Gets the mask.'''
        raise NotImplementedError()
    
    @graphics_path_mask.setter
    def graphics_path_mask(self, value : aspose.imaging.GraphicsPath) -> None:
        '''Sets the mask.'''
        raise NotImplementedError()
    

