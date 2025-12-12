"""The namespace contains DNG decoder types"""
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

class ImageOtherParameters:
    '''Other image parameters'''
    
    @property
    def description(self) -> str:
        '''Gets the image description.'''
        raise NotImplementedError()
    
    @property
    def artist(self) -> str:
        '''Gets the author of image.'''
        raise NotImplementedError()
    
    @property
    def timestamp(self) -> int:
        '''Gets the date of shooting.'''
        raise NotImplementedError()
    
    @property
    def shot_order(self) -> int:
        '''Gets serial number of image.'''
        raise NotImplementedError()
    
    @property
    def aperture(self) -> float:
        '''Gets the aperture.'''
        raise NotImplementedError()
    
    @property
    def shutter_speed(self) -> float:
        '''Gets the shutter speed.'''
        raise NotImplementedError()
    
    @property
    def gps_data(self) -> List[int]:
        '''Gets the GPS data.'''
        raise NotImplementedError()
    
    @property
    def focal_length(self) -> float:
        '''Gets the length of the focal.'''
        raise NotImplementedError()
    
    @property
    def iso_speed(self) -> float:
        '''Gets the ISO sensitivity.'''
        raise NotImplementedError()
    

class ImageParameters:
    '''Dng image parameters'''
    
    @property
    def dng_version(self) -> int:
        '''Gets the DNG version.'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Gets the description of colors (RGBG,RGBE,GMCY, or GBTG).'''
        raise NotImplementedError()
    
    @property
    def model(self) -> str:
        '''Gets the camera model.'''
        raise NotImplementedError()
    
    @property
    def camera_manufacturer(self) -> str:
        '''Gets the camera manufacturer.'''
        raise NotImplementedError()
    
    @property
    def is_foveon(self) -> int:
        '''Gets the is foveon matrix.'''
        raise NotImplementedError()
    
    @property
    def software(self) -> str:
        '''Gets the software.'''
        raise NotImplementedError()
    
    @property
    def raw_count(self) -> int:
        '''Gets the number of RAW images in file (0 means that the file has not been recognized).'''
        raise NotImplementedError()
    
    @property
    def filters(self) -> int:
        '''Gets the Bit mask describing the order of color pixels in the matrix.'''
        raise NotImplementedError()
    
    @property
    def colors_count(self) -> int:
        '''Gets the colors.'''
        raise NotImplementedError()
    
    @property
    def xmp_data(self) -> str:
        '''Gets the XMP data.'''
        raise NotImplementedError()
    
    @property
    def translation_cfa_dng(self) -> List[str]:
        '''Gets the translation array for CFA mosaic DNG format.'''
        raise NotImplementedError()
    

class RawData:
    '''The raw data in DNG format'''
    
    @property
    def image_data_parameters(self) -> aspose.imaging.fileformats.dng.decoder.ImageParameters:
        '''Gets the image data parameters.'''
        raise NotImplementedError()
    
    @image_data_parameters.setter
    def image_data_parameters(self, value : aspose.imaging.fileformats.dng.decoder.ImageParameters) -> None:
        '''Sets the image data parameters.'''
        raise NotImplementedError()
    
    @property
    def image_other_parameters(self) -> aspose.imaging.fileformats.dng.decoder.ImageOtherParameters:
        '''Gets the other image parameters.'''
        raise NotImplementedError()
    
    @image_other_parameters.setter
    def image_other_parameters(self, value : aspose.imaging.fileformats.dng.decoder.ImageOtherParameters) -> None:
        '''Sets the other image parameters.'''
        raise NotImplementedError()
    

