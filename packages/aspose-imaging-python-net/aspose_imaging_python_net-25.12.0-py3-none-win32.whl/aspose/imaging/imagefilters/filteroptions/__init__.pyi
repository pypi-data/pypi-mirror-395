"""The namespace handles Filter options."""
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

class AdaptiveWhiteStretchFilterOptions(FilterOptionsBase):
    '''Provides options for configuring the Adaptive White Stretch filter.
    Allows customization of histogram stretch parameters to enhance the white level
    and improve the readability of faint-text or low-contrast document images.'''
    
    def __init__(self, is_grayscale : bool, low_percentile : int, high_percentile : int, target_white : int, max_scale : float) -> None:
        '''Initializes a new instance of the :py:class:`Aspose.Imaging.ImageFilters.AdaptiveWhiteStretchFilter` class.
        
        :param is_grayscale: Indicates whether the filter should operate in grayscale mode.
        :param low_percentile: Lower percentile for black point (e.g. 10).
        :param high_percentile: Upper percentile for white point (e.g. 90).
        :param target_white: Target white value (e.g. 240).
        :param max_scale: Maximum allowed brightness scale (e.g. 1.7).'''
        raise NotImplementedError()
    
    @property
    def is_grayscale(self) -> bool:
        '''Gets a value indicating whether the filter operates in grayscale mode.'''
        raise NotImplementedError()
    
    @property
    def low_percentile(self) -> int:
        '''Gets the lower percentile for black point calculation.
        Pixel values below this percentile are considered as black during stretching.'''
        raise NotImplementedError()
    
    @property
    def high_percentile(self) -> int:
        '''Gets the upper percentile for white point calculation.
        Pixel values above this percentile are considered as white during stretching.'''
        raise NotImplementedError()
    
    @property
    def target_white(self) -> int:
        '''Gets the target white value the stretch aims to achieve.'''
        raise NotImplementedError()
    
    @property
    def max_scale(self) -> float:
        '''Gets the maximum allowed brightness scale.
        The actual stretching will not exceed this factor, to avoid over-brightening.'''
        raise NotImplementedError()
    

class AutoWhiteBalanceFilterOptions(FilterOptionsBase):
    '''Provides configuration options for the Auto White Balance filter.
    Allows tuning of contrast stretching parameters and channel scaling
    to improve the appearance of digital images.'''
    
    def __init__(self, low_percentile : int, target_high_percentile : int, target_value : int, max_scale : float, protected_dark_offset : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.AutoWhiteBalanceFilterOptions` class.
        
        :param low_percentile: The low percentile for black point, used for darks protection (default: 3).
        :param target_high_percentile: The target high percentile for contrast stretching (default 97).
        :param target_value: The target value for the high percentile (default 255).
        :param max_scale: The maximum scaling factor for each channel (default 1.4f).
        :param protected_dark_offset: Offset from low percentile below which dark pixels are not stretched (protection).'''
        raise NotImplementedError()
    
    @property
    def target_high_percentile(self) -> int:
        '''Gets the target high percentile for contrast stretching.
        Determines which brightness percentile will be mapped to the target value.'''
        raise NotImplementedError()
    
    @property
    def target_value(self) -> int:
        '''Gets the target value for the high percentile.
        This value will be used as the white reference for contrast stretching.'''
        raise NotImplementedError()
    
    @property
    def max_scale(self) -> float:
        '''Gets the maximum scaling factor for each channel.
        Restricts the amplification of any channel to avoid excessive color shifts.'''
        raise NotImplementedError()
    
    @property
    def low_percentile(self) -> int:
        '''The low percentile for black point, used for darks protection (default: 3).'''
        raise NotImplementedError()
    
    @property
    def protected_dark_offset(self) -> int:
        '''Offset from low percentile below which dark pixels are not stretched (protection).'''
        raise NotImplementedError()
    

class BigRectangularFilterOptions(FilterOptionsBase):
    '''Big Rectangular Filter Options'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    

class BilateralSmoothingFilterOptions(FilterOptionsBase):
    '''The Bilateral Smoothing Filter Options.'''
    
    @overload
    def __init__(self, size : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.BilateralSmoothingFilterOptions` class.
        
        :param size: Size of the kernal.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.BilateralSmoothingFilterOptions` class.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the size of the kernel.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Sets the size of the kernel.'''
        raise NotImplementedError()
    
    @property
    def spatial_factor(self) -> float:
        '''Gets the spatial factor.'''
        raise NotImplementedError()
    
    @spatial_factor.setter
    def spatial_factor(self, value : float) -> None:
        '''Sets the spatial factor.'''
        raise NotImplementedError()
    
    @property
    def spatial_power(self) -> float:
        '''Gets the spatial power.'''
        raise NotImplementedError()
    
    @spatial_power.setter
    def spatial_power(self, value : float) -> None:
        '''Sets the spatial power.'''
        raise NotImplementedError()
    
    @property
    def color_factor(self) -> float:
        '''Gets the color factor.'''
        raise NotImplementedError()
    
    @color_factor.setter
    def color_factor(self, value : float) -> None:
        '''Sets the color factor.'''
        raise NotImplementedError()
    
    @property
    def color_power(self) -> float:
        '''Gets the color power.'''
        raise NotImplementedError()
    
    @color_power.setter
    def color_power(self, value : float) -> None:
        '''Sets the color power.'''
        raise NotImplementedError()
    

class ClaheFilterOptions(FilterOptionsBase):
    '''Provides options for configuring the Contrast-Limited Adaptive Histogram Equalization (CLAHE) filter.'''
    
    def __init__(self, is_grayscale : bool, tiles_number_horizontal : int, tiles_number_vertical : int, clip_limit : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.ClaheFilterOptions` class
        with the specified parameters.
        
        :param is_grayscale: Indicates whether the filter should operate in grayscale mode.
        :param tiles_number_horizontal: Number of tiles horizontally. Default is 8.
        :param tiles_number_vertical: Number of tiles vertically. Default is 8.
        :param clip_limit: Contrast limiting threshold. Default is 4.0.'''
        raise NotImplementedError()
    
    @property
    def is_grayscale(self) -> bool:
        '''Gets a value indicating whether the filter operates in grayscale mode.'''
        raise NotImplementedError()
    
    @property
    def tiles_number_horizontal(self) -> int:
        '''Gets the number of tiles in the horizontal direction.
        Determines how many regions the image is divided into horizontally for local contrast equalization.'''
        raise NotImplementedError()
    
    @property
    def tiles_number_vertical(self) -> int:
        '''Gets the number of tiles in the vertical direction.
        Determines how many regions the image is divided into vertically for local contrast equalization.'''
        raise NotImplementedError()
    
    @property
    def clip_limit(self) -> float:
        '''Gets the contrast limiting threshold.
        Higher values allow more contrast; lower values limit the enhancement to prevent noise amplification.'''
        raise NotImplementedError()
    

class ConvolutionFilterOptions(FilterOptionsBase):
    '''The convolution filter options.'''
    
    @overload
    def __init__(self, kernel : List[float]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.ConvolutionFilterOptions` class with factor = 1, and bias = 0.
        
        :param kernel: The convolution kernel for X-axis direction.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, kernel : List[float], factor : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.ConvolutionFilterOptions` class with bias = 0.
        
        :param kernel: The convolution kernel for X-axis direction.
        :param factor: The factor.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, kernel : List[float], factor : float, bias : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.ConvolutionFilterOptions` class.
        
        :param kernel: The convolution kernel for X-axis direction.
        :param factor: The factor.
        :param bias: The bias value.'''
        raise NotImplementedError()
    
    @property
    def kernel_data(self) -> List[float]:
        '''Gets the kernel.'''
        raise NotImplementedError()
    
    @property
    def factor(self) -> float:
        '''Gets the factor.'''
        raise NotImplementedError()
    
    @factor.setter
    def factor(self, value : float) -> None:
        '''Sets the factor.'''
        raise NotImplementedError()
    
    @property
    def bias(self) -> int:
        '''Gets the bias.'''
        raise NotImplementedError()
    
    @bias.setter
    def bias(self, value : int) -> None:
        '''Sets the bias.'''
        raise NotImplementedError()
    
    @property
    def ignore_alpha(self) -> bool:
        '''Gets a value indicating whether [ignore alpha].'''
        raise NotImplementedError()
    
    @ignore_alpha.setter
    def ignore_alpha(self, value : bool) -> None:
        '''Sets a value indicating whether [ignore alpha].'''
        raise NotImplementedError()
    
    @property
    def borders_processing(self) -> bool:
        '''Gets a value indicating whether [borders processing].'''
        raise NotImplementedError()
    
    @borders_processing.setter
    def borders_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [borders processing].'''
        raise NotImplementedError()
    

class DeconvolutionFilterOptions(FilterOptionsBase):
    '''Deconvolution Filter Options, abstract class'''
    
    @overload
    def __init__(self, kernel : List[float]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The kernel.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, kernel : List[aspose.imaging.imagefilters.complexutils.Complex]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The kernel.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_double(kernel : List[float]) -> aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The double[] kernel.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_complex(kernel : List[aspose.imaging.imagefilters.complexutils.Complex]) -> aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The Complex[] kernel.'''
        raise NotImplementedError()
    
    @property
    def kernel_data(self) -> List[aspose.imaging.imagefilters.complexutils.Complex]:
        '''Gets the kernel.'''
        raise NotImplementedError()
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        raise NotImplementedError()
    
    @snr.setter
    def snr(self, value : float) -> None:
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        raise NotImplementedError()
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        raise NotImplementedError()
    
    @brightness.setter
    def brightness(self, value : float) -> None:
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        raise NotImplementedError()
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        raise NotImplementedError()
    
    @grayscale.setter
    def grayscale(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        raise NotImplementedError()
    
    @property
    def is_partial_loaded(self) -> bool:
        '''Gets a value indicating whether this instance is partial loaded.'''
        raise NotImplementedError()
    

class FilterOptionsBase:
    '''Base filter options class.'''
    

class GaussWienerFilterOptions(GaussianDeconvolutionFilterOptions):
    '''Gauss Wiener filter options for image debluring.'''
    
    @overload
    def __init__(self, size : int, sigma : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.GaussWienerFilterOptions` class.
        
        :param size: The Gaussian kernel size.
        :param sigma: The Gaussian kernel sigma.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.GaussWienerFilterOptions` class.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_double(kernel : List[float]) -> aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The double[] kernel.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_complex(kernel : List[aspose.imaging.imagefilters.complexutils.Complex]) -> aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The Complex[] kernel.'''
        raise NotImplementedError()
    
    @property
    def kernel_data(self) -> List[aspose.imaging.imagefilters.complexutils.Complex]:
        '''Gets the kernel.'''
        raise NotImplementedError()
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        raise NotImplementedError()
    
    @snr.setter
    def snr(self, value : float) -> None:
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        raise NotImplementedError()
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        raise NotImplementedError()
    
    @brightness.setter
    def brightness(self, value : float) -> None:
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        raise NotImplementedError()
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        raise NotImplementedError()
    
    @grayscale.setter
    def grayscale(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        raise NotImplementedError()
    
    @property
    def is_partial_loaded(self) -> bool:
        '''Gets a value indicating whether this instance is partial loaded.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @property
    def sigma(self) -> float:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @sigma.setter
    def sigma(self, value : float) -> None:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @property
    def radius(self) -> int:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    
    @radius.setter
    def radius(self, value : int) -> None:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    

class GaussianBlurFilterOptions(ConvolutionFilterOptions):
    '''The Gaussian blur filter options.'''
    
    @overload
    def __init__(self, size : int, sigma : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.GaussianBlurFilterOptions` class.
        
        :param size: The Gaussian kernel size..
        :param sigma: The Gaussian kernel sigma.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.GaussianBlurFilterOptions` class.'''
        raise NotImplementedError()
    
    @property
    def kernel_data(self) -> List[float]:
        '''Gets the Gaussian kernel.'''
        raise NotImplementedError()
    
    @property
    def factor(self) -> float:
        '''Gets the factor.'''
        raise NotImplementedError()
    
    @factor.setter
    def factor(self, value : float) -> None:
        '''Sets the factor.'''
        raise NotImplementedError()
    
    @property
    def bias(self) -> int:
        '''Gets the bias.'''
        raise NotImplementedError()
    
    @bias.setter
    def bias(self, value : int) -> None:
        '''Sets the bias.'''
        raise NotImplementedError()
    
    @property
    def ignore_alpha(self) -> bool:
        '''Gets a value indicating whether [ignore alpha].'''
        raise NotImplementedError()
    
    @ignore_alpha.setter
    def ignore_alpha(self, value : bool) -> None:
        '''Sets a value indicating whether [ignore alpha].'''
        raise NotImplementedError()
    
    @property
    def borders_processing(self) -> bool:
        '''Gets a value indicating whether [borders processing].'''
        raise NotImplementedError()
    
    @borders_processing.setter
    def borders_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [borders processing].'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @property
    def sigma(self) -> float:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @sigma.setter
    def sigma(self, value : float) -> None:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @property
    def radius(self) -> int:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    
    @radius.setter
    def radius(self, value : int) -> None:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    

class GaussianDeconvolutionFilterOptions(DeconvolutionFilterOptions):
    '''The deconvolution filter options using Gaussian bluring.'''
    
    @staticmethod
    def create_with_double(kernel : List[float]) -> aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The double[] kernel.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_complex(kernel : List[aspose.imaging.imagefilters.complexutils.Complex]) -> aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The Complex[] kernel.'''
        raise NotImplementedError()
    
    @property
    def kernel_data(self) -> List[aspose.imaging.imagefilters.complexutils.Complex]:
        '''Gets the kernel.'''
        raise NotImplementedError()
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        raise NotImplementedError()
    
    @snr.setter
    def snr(self, value : float) -> None:
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        raise NotImplementedError()
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        raise NotImplementedError()
    
    @brightness.setter
    def brightness(self, value : float) -> None:
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        raise NotImplementedError()
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        raise NotImplementedError()
    
    @grayscale.setter
    def grayscale(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        raise NotImplementedError()
    
    @property
    def is_partial_loaded(self) -> bool:
        '''Gets a value indicating whether this instance is partial loaded.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @property
    def sigma(self) -> float:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @sigma.setter
    def sigma(self, value : float) -> None:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @property
    def radius(self) -> int:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    
    @radius.setter
    def radius(self, value : int) -> None:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    

class ImageBlendingFilterOptions(FilterOptionsBase):
    '''The image blending filter options'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def image(self) -> aspose.imaging.RasterImage:
        '''Gets the image.'''
        raise NotImplementedError()
    
    @image.setter
    def image(self, value : aspose.imaging.RasterImage) -> None:
        '''Sets the image.'''
        raise NotImplementedError()
    
    @property
    def position(self) -> aspose.imaging.Point:
        '''Gets the position.'''
        raise NotImplementedError()
    
    @position.setter
    def position(self, value : aspose.imaging.Point) -> None:
        '''Sets the position.'''
        raise NotImplementedError()
    
    @property
    def blending_mode(self) -> aspose.imaging.imagefilters.filteroptions.BlendingMode:
        '''Gets the blending mode.'''
        raise NotImplementedError()
    
    @blending_mode.setter
    def blending_mode(self, value : aspose.imaging.imagefilters.filteroptions.BlendingMode) -> None:
        '''Sets the blending mode.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the opacity.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the opacity.'''
        raise NotImplementedError()
    

class MedianFilterOptions(FilterOptionsBase):
    '''Median filter'''
    
    def __init__(self, size : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.MedianFilterOptions` class.
        
        :param size: The size of filter rectangle.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the size.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Sets the size.'''
        raise NotImplementedError()
    

class MotionWienerFilterOptions(GaussianDeconvolutionFilterOptions):
    '''The motion debluring filter options.'''
    
    def __init__(self, size : int, sigma : float, angle : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.MotionWienerFilterOptions` class.
        
        :param size: The Gaussian kernel size.
        :param sigma: The Gaussian kernel sigma.
        :param angle: The angle in degrees.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_double(kernel : List[float]) -> aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The double[] kernel.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_complex(kernel : List[aspose.imaging.imagefilters.complexutils.Complex]) -> aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` class.
        
        :param kernel: The Complex[] kernel.'''
        raise NotImplementedError()
    
    @property
    def kernel_data(self) -> List[aspose.imaging.imagefilters.complexutils.Complex]:
        '''Gets the kernel.'''
        raise NotImplementedError()
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        raise NotImplementedError()
    
    @snr.setter
    def snr(self, value : float) -> None:
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        raise NotImplementedError()
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        raise NotImplementedError()
    
    @brightness.setter
    def brightness(self, value : float) -> None:
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        raise NotImplementedError()
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        raise NotImplementedError()
    
    @grayscale.setter
    def grayscale(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        raise NotImplementedError()
    
    @property
    def is_partial_loaded(self) -> bool:
        '''Gets a value indicating whether this instance is partial loaded.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @property
    def sigma(self) -> float:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @sigma.setter
    def sigma(self, value : float) -> None:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @property
    def radius(self) -> int:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    
    @radius.setter
    def radius(self, value : int) -> None:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets the angle in degrees.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets the angle in degrees.'''
        raise NotImplementedError()
    

class SharpenFilterOptions(GaussianBlurFilterOptions):
    '''The sharpen filter options.'''
    
    @overload
    def __init__(self, size : int, sigma : float) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.SharpenFilterOptions` class.
        
        :param size: The size of the kernel.
        :param sigma: The sigma.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.imagefilters.filteroptions.SharpenFilterOptions` class.'''
        raise NotImplementedError()
    
    @property
    def kernel_data(self) -> List[float]:
        '''Gets the kernel.'''
        raise NotImplementedError()
    
    @property
    def factor(self) -> float:
        '''Gets the factor.'''
        raise NotImplementedError()
    
    @factor.setter
    def factor(self, value : float) -> None:
        '''Sets the factor.'''
        raise NotImplementedError()
    
    @property
    def bias(self) -> int:
        '''Gets the bias.'''
        raise NotImplementedError()
    
    @bias.setter
    def bias(self, value : int) -> None:
        '''Sets the bias.'''
        raise NotImplementedError()
    
    @property
    def ignore_alpha(self) -> bool:
        '''Gets a value indicating whether [ignore alpha].'''
        raise NotImplementedError()
    
    @ignore_alpha.setter
    def ignore_alpha(self, value : bool) -> None:
        '''Sets a value indicating whether [ignore alpha].'''
        raise NotImplementedError()
    
    @property
    def borders_processing(self) -> bool:
        '''Gets a value indicating whether [borders processing].'''
        raise NotImplementedError()
    
    @borders_processing.setter
    def borders_processing(self, value : bool) -> None:
        '''Sets a value indicating whether [borders processing].'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Gets the Gaussian kernel size. Must be a positive non-zero odd value.'''
        raise NotImplementedError()
    
    @property
    def sigma(self) -> float:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @sigma.setter
    def sigma(self, value : float) -> None:
        '''Gets the Gaussian kernel sigma (smoothing). Must be a positive non-zero value.'''
        raise NotImplementedError()
    
    @property
    def radius(self) -> int:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    
    @radius.setter
    def radius(self, value : int) -> None:
        '''Gets the radius of Gausseian :py:class:`Aspose.Imaging.ImageFilters.Convolution.ISquareConvolutionKernel`.'''
        raise NotImplementedError()
    

class SmallRectangularFilterOptions(FilterOptionsBase):
    '''Small rectangular filter options'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    

class BlendingMode(enum.Enum):
    NORMAL = enum.auto()
    '''The normal'''
    MULTIPLY = enum.auto()
    '''The multiply'''
    SCREEN = enum.auto()
    '''The screen'''
    OVERLAY = enum.auto()
    '''The overlay'''
    DARKEN = enum.auto()
    '''The darken'''
    LIGHTEN = enum.auto()
    '''The lighten'''
    COLOR_DODGE = enum.auto()
    '''The color dodge'''
    COLOR_BURN = enum.auto()
    '''The color burn'''
    HARD_LIGHT = enum.auto()
    '''The hard light'''
    SOFT_LIGHT = enum.auto()
    '''The soft light'''
    DIFFERENCE = enum.auto()
    '''The difference'''
    EXCLUSION = enum.auto()
    '''The exclusion'''
    HUE = enum.auto()
    '''The hue mode'''
    SATURATION = enum.auto()
    '''The saturation'''
    COLOR = enum.auto()
    '''The color mode'''
    LUMINOSITY = enum.auto()
    '''The luminosity'''

