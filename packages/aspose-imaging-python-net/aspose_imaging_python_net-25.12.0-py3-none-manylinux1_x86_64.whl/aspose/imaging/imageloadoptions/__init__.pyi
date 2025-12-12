"""The namespace contains different file format load options."""
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

class CdrLoadOptions(aspose.imaging.LoadOptions):
    '''The Cdr load options'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imageloadoptions.CdrLoadOptions` class.'''
        raise NotImplementedError()
    
    @property
    def data_recovery_mode(self) -> aspose.imaging.DataRecoveryMode:
        '''Gets the data recovery mode.'''
        raise NotImplementedError()
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.imaging.DataRecoveryMode) -> None:
        '''Sets the data recovery mode.'''
        raise NotImplementedError()
    
    @property
    def data_background_color(self) -> aspose.imaging.Color:
        '''Gets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        '''Gets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool) -> None:
        '''Sets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @property
    def buffer_size_hint(self) -> int:
        '''Gets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int) -> None:
        '''Sets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @property
    def concurrent_image_processing(self) -> bool:
        '''Gets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @concurrent_image_processing.setter
    def concurrent_image_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @property
    def default_font(self) -> aspose.imaging.Font:
        '''Gets the default font.'''
        raise NotImplementedError()
    
    @default_font.setter
    def default_font(self, value : aspose.imaging.Font) -> None:
        '''Sets the default font.'''
        raise NotImplementedError()
    
    @property
    def optimal_memory_usage(self) -> bool:
        '''Gets a value indicating whether [optimal memory usage].'''
        raise NotImplementedError()
    
    @optimal_memory_usage.setter
    def optimal_memory_usage(self, value : bool) -> None:
        '''Sets a value indicating whether [optimal memory usage].'''
        raise NotImplementedError()
    

class CmxLoadOptions(aspose.imaging.LoadOptions):
    '''The CMX load options'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.LoadOptions`.'''
        raise NotImplementedError()
    
    @property
    def data_recovery_mode(self) -> aspose.imaging.DataRecoveryMode:
        '''Gets the data recovery mode.'''
        raise NotImplementedError()
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.imaging.DataRecoveryMode) -> None:
        '''Sets the data recovery mode.'''
        raise NotImplementedError()
    
    @property
    def data_background_color(self) -> aspose.imaging.Color:
        '''Gets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        '''Gets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool) -> None:
        '''Sets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @property
    def buffer_size_hint(self) -> int:
        '''Gets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int) -> None:
        '''Sets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @property
    def concurrent_image_processing(self) -> bool:
        '''Gets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @concurrent_image_processing.setter
    def concurrent_image_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @property
    def optimal_memory_usage(self) -> bool:
        '''Gets a value indicating whether [optimal memory usage].'''
        raise NotImplementedError()
    
    @optimal_memory_usage.setter
    def optimal_memory_usage(self, value : bool) -> None:
        '''Sets a value indicating whether [optimal memory usage].'''
        raise NotImplementedError()
    

class DngLoadOptions(aspose.imaging.LoadOptions):
    '''The DNG load options'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.LoadOptions`.'''
        raise NotImplementedError()
    
    @property
    def data_recovery_mode(self) -> aspose.imaging.DataRecoveryMode:
        '''Gets the data recovery mode.'''
        raise NotImplementedError()
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.imaging.DataRecoveryMode) -> None:
        '''Sets the data recovery mode.'''
        raise NotImplementedError()
    
    @property
    def data_background_color(self) -> aspose.imaging.Color:
        '''Gets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        '''Gets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool) -> None:
        '''Sets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @property
    def buffer_size_hint(self) -> int:
        '''Gets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int) -> None:
        '''Sets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @property
    def concurrent_image_processing(self) -> bool:
        '''Gets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @concurrent_image_processing.setter
    def concurrent_image_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @property
    def fbdd(self) -> aspose.imaging.imageloadoptions.NoiseReductionType:
        '''Gets the FBDD.'''
        raise NotImplementedError()
    
    @fbdd.setter
    def fbdd(self, value : aspose.imaging.imageloadoptions.NoiseReductionType) -> None:
        '''Sets the FBDD.'''
        raise NotImplementedError()
    
    @property
    def adjust_white_balance(self) -> bool:
        '''Gets the flag indicating that the white balance of the loaded DNG image should be adjusted.'''
        raise NotImplementedError()
    
    @adjust_white_balance.setter
    def adjust_white_balance(self, value : bool) -> None:
        '''Sets the flag indicating that the white balance of the loaded DNG image should be adjusted.'''
        raise NotImplementedError()
    

class Jpeg2000LoadOptions(aspose.imaging.LoadOptions):
    '''JPEG2000 load options'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imageloadoptions.Jpeg2000LoadOptions` class.'''
        raise NotImplementedError()
    
    @property
    def data_recovery_mode(self) -> aspose.imaging.DataRecoveryMode:
        '''Gets the data recovery mode.'''
        raise NotImplementedError()
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.imaging.DataRecoveryMode) -> None:
        '''Sets the data recovery mode.'''
        raise NotImplementedError()
    
    @property
    def data_background_color(self) -> aspose.imaging.Color:
        '''Gets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        '''Gets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool) -> None:
        '''Sets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @property
    def buffer_size_hint(self) -> int:
        '''Gets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int) -> None:
        '''Sets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @property
    def concurrent_image_processing(self) -> bool:
        '''Gets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @concurrent_image_processing.setter
    def concurrent_image_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @property
    def maximum_decoding_time(self) -> int:
        '''Gets the maximum decoding time in seconds (this option can be used on very slow on memory machines to prevent hanging on process on very big images - resolution more than 5500x6500 pixels).'''
        raise NotImplementedError()
    
    @maximum_decoding_time.setter
    def maximum_decoding_time(self, value : int) -> None:
        '''Sets the maximum decoding time in seconds (this option can be used on very slow on memory machines to prevent hanging on process on very big images - resolution more than 5500x6500 pixels).'''
        raise NotImplementedError()
    
    @property
    def maximum_decoding_time_for_tile(self) -> int:
        '''Gets the maximum decoding time for tile.'''
        raise NotImplementedError()
    
    @maximum_decoding_time_for_tile.setter
    def maximum_decoding_time_for_tile(self, value : int) -> None:
        '''Sets the maximum decoding time for tile.'''
        raise NotImplementedError()
    

class OdLoadOptions(aspose.imaging.LoadOptions):
    '''The Open Dcocument Load Options'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.LoadOptions`.'''
        raise NotImplementedError()
    
    @property
    def data_recovery_mode(self) -> aspose.imaging.DataRecoveryMode:
        '''Gets the data recovery mode.'''
        raise NotImplementedError()
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.imaging.DataRecoveryMode) -> None:
        '''Sets the data recovery mode.'''
        raise NotImplementedError()
    
    @property
    def data_background_color(self) -> aspose.imaging.Color:
        '''Gets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        '''Gets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool) -> None:
        '''Sets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @property
    def buffer_size_hint(self) -> int:
        '''Gets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int) -> None:
        '''Sets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @property
    def concurrent_image_processing(self) -> bool:
        '''Gets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @concurrent_image_processing.setter
    def concurrent_image_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @property
    def password(self) -> str:
        '''Gets the password.'''
        raise NotImplementedError()
    
    @password.setter
    def password(self, value : str) -> None:
        '''Sets the password.'''
        raise NotImplementedError()
    

class PngLoadOptions(aspose.imaging.LoadOptions):
    '''The png load options.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imageloadoptions.PngLoadOptions` class.'''
        raise NotImplementedError()
    
    @property
    def data_recovery_mode(self) -> aspose.imaging.DataRecoveryMode:
        '''Gets the data recovery mode.'''
        raise NotImplementedError()
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.imaging.DataRecoveryMode) -> None:
        '''Sets the data recovery mode.'''
        raise NotImplementedError()
    
    @property
    def data_background_color(self) -> aspose.imaging.Color:
        '''Gets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        '''Gets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool) -> None:
        '''Sets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @property
    def buffer_size_hint(self) -> int:
        '''Gets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int) -> None:
        '''Sets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @property
    def concurrent_image_processing(self) -> bool:
        '''Gets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @concurrent_image_processing.setter
    def concurrent_image_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @property
    def strict_mode(self) -> bool:
        '''Gets a value indicating whether [strict mode].'''
        raise NotImplementedError()
    
    @strict_mode.setter
    def strict_mode(self, value : bool) -> None:
        '''Sets a value indicating whether [strict mode].'''
        raise NotImplementedError()
    

class SvgLoadOptions(aspose.imaging.LoadOptions):
    '''The Svg load options.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.LoadOptions`.'''
        raise NotImplementedError()
    
    @property
    def data_recovery_mode(self) -> aspose.imaging.DataRecoveryMode:
        '''Gets the data recovery mode.'''
        raise NotImplementedError()
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.imaging.DataRecoveryMode) -> None:
        '''Sets the data recovery mode.'''
        raise NotImplementedError()
    
    @property
    def data_background_color(self) -> aspose.imaging.Color:
        '''Gets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the :py:class:`aspose.imaging.Image` background :py:class:`aspose.imaging.Color`.'''
        raise NotImplementedError()
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        '''Gets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool) -> None:
        '''Sets a value indicating whether ICC profile conversion should be applied.'''
        raise NotImplementedError()
    
    @property
    def buffer_size_hint(self) -> int:
        '''Gets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int) -> None:
        '''Sets the buffer size hint which is defined max allowed size for all internal buffers.'''
        raise NotImplementedError()
    
    @property
    def concurrent_image_processing(self) -> bool:
        '''Gets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @concurrent_image_processing.setter
    def concurrent_image_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [concurrent image processing].'''
        raise NotImplementedError()
    
    @property
    def default_width(self) -> int:
        '''Gets the default width.
        Property DefaultWidth use with only case, when width not set in file.'''
        raise NotImplementedError()
    
    @default_width.setter
    def default_width(self, value : int) -> None:
        '''Sets the default width.
        Property DefaultWidth use with only case, when width not set in file.'''
        raise NotImplementedError()
    
    @property
    def default_height(self) -> int:
        '''Gets the default height.
        Property DefaultHeight use with only case, when height not set in file.'''
        raise NotImplementedError()
    
    @default_height.setter
    def default_height(self, value : int) -> None:
        '''Sets the default height.
        Property DefaultHeight use with only case, when height not set in file.'''
        raise NotImplementedError()
    

class NoiseReductionType(enum.Enum):
    NONE = enum.auto()
    '''The None, do not use FBDD noise reduction'''
    LIGHT = enum.auto()
    '''The light, light FBDD reduction'''
    FULL = enum.auto()
    '''The full, full FBDD reduction'''

