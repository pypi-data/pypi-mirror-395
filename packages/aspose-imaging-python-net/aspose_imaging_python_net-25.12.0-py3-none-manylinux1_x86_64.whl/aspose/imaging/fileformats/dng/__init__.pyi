"""The namespace contains DNG file format types"""
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

class DngImage(aspose.imaging.RasterCachedImage):
    '''The API for processing DNG (Digital Negative) image file format used for digital
    photography needs by providing comprehensive support for raw files and metadata.
    Designed for use with digital cameras across various manufacturers, it enables
    developers to manipulate aspects like bits per pixel, extract internal data,
    and adjust image balance efficiently. With capabilities to update and save image
    data seamlessly, this API empowers developers to work with DNG files,
    ensuring high-quality results and versatile processing options.'''
    
    @overload
    def save(self, stream : io._IOBase, options_base : aspose.imaging.ImageOptionsBase, bounds_rectangle : aspose.imaging.Rectangle) -> None:
        '''Saves the image\'s data to the specified stream in the specified file format according to save options.
        
        :param stream: The stream to save the image\'s data to.
        :param options_base: The save options.
        :param bounds_rectangle: The destination image bounds rectangle. Set the empty rectangle for use source bounds.'''
        raise NotImplementedError()
    
    @overload
    def save(self) -> None:
        '''Saves the image data to the underlying stream.'''
        raise NotImplementedError()
    
    @overload
    def save(self, file_path : str) -> None:
        '''Saves the image to the specified file location.
        
        :param file_path: The file path to save the image to.'''
        raise NotImplementedError()
    
    @overload
    def save(self, file_path : str, options : aspose.imaging.ImageOptionsBase) -> None:
        '''Saves the object\'s data to the specified file location in the specified file format according to save options.
        
        :param file_path: The file path.
        :param options: The options.'''
        raise NotImplementedError()
    
    @overload
    def save(self, file_path : str, options : aspose.imaging.ImageOptionsBase, bounds_rectangle : aspose.imaging.Rectangle) -> None:
        '''Saves the object\'s data to the specified file location in the specified file format according to save options.
        
        :param file_path: The file path.
        :param options: The options.
        :param bounds_rectangle: The destination image bounds rectangle. Set the empty rectangle for use sourse bounds.'''
        raise NotImplementedError()
    
    @overload
    def save(self, stream : io._IOBase, options_base : aspose.imaging.ImageOptionsBase) -> None:
        '''Saves the image\'s data to the specified stream in the specified file format according to save options.
        
        :param stream: The stream to save the image\'s data to.
        :param options_base: The save options.'''
        raise NotImplementedError()
    
    @overload
    def save(self, stream : io._IOBase) -> None:
        '''Saves the object\'s data to the specified stream.
        
        :param stream: The stream to save the object\'s data to.'''
        raise NotImplementedError()
    
    @overload
    def save(self, file_path : str, over_write : bool) -> None:
        '''Saves the object\'s data to the specified file location.
        
        :param file_path: The file path to save the object\'s data to.
        :param over_write: if set to ``true`` over write the file contents, otherwise append will occur.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def can_load(file_path : str) -> bool:
        '''Determines whether image can be loaded from the specified file path.
        
        :param file_path: The file path.
        :returns: ``true`` if image can be loaded from the specified file; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def can_load(file_path : str, load_options : aspose.imaging.LoadOptions) -> bool:
        '''Determines whether image can be loaded from the specified file path and optionally using the specified open options.
        
        :param file_path: The file path.
        :param load_options: The load options.
        :returns: ``true`` if image can be loaded from the specified file; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def can_load(stream : io._IOBase) -> bool:
        '''Determines whether image can be loaded from the specified stream.
        
        :param stream: The stream to load from.
        :returns: ``true`` if image can be loaded from the specified stream; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def can_load(stream : io._IOBase, load_options : aspose.imaging.LoadOptions) -> bool:
        '''Determines whether image can be loaded from the specified stream and optionally using the specified ``loadOptions``.
        
        :param stream: The stream to load from.
        :param load_options: The load options.
        :returns: ``true`` if image can be loaded from the specified stream; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create(image_options : aspose.imaging.ImageOptionsBase, width : int, height : int) -> aspose.imaging.Image:
        '''Creates a new image using the specified create options.
        
        :param image_options: The image options.
        :param width: The width.
        :param height: The height.
        :returns: The newly created image.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create(image_options : aspose.imaging.ImageOptionsBase, width : int, height : int, pixels : List[int]) -> aspose.imaging.Image:
        '''Creates a :py:class:`aspose.imaging.RasterImage` instance from the provided pixel array.
        
        Validates that the specified width and height match the dimensions of the pixel data.
        This method can only be used when the library is in Licensed mode.
        
        :param image_options: The options used to create the :py:class:`aspose.imaging.RasterImage`.
        :param width: The width of the :py:class:`aspose.imaging.RasterImage`.
        :param height: The height of the :py:class:`aspose.imaging.RasterImage`.
        :param pixels: The array of pixel values used to populate the image.
        :returns: A :py:class:`aspose.imaging.RasterImage` populated with the provided pixel data.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create(images : List[aspose.imaging.Image]) -> aspose.imaging.Image:
        '''Creates a new image using the specified images as pages
        
        :param images: The images.
        :returns: The Image as IMultipageImage'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create(multipage_create_options : aspose.imaging.imageoptions.MultipageCreateOptions) -> aspose.imaging.Image:
        '''Creates the specified multipage create options.
        
        :param multipage_create_options: The multipage create options.
        :returns: The multipage image'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create(files : List[str], throw_exception_on_load_error : bool) -> aspose.imaging.Image:
        '''Creates the multipage image containing the specified files.
        
        :param files: The files.
        :param throw_exception_on_load_error: if set to ``true`` [throw exception on load error].
        :returns: The multipage image'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create(files : List[str]) -> aspose.imaging.Image:
        '''Creates the multipage image containing the specified files.
        
        :param files: The files.
        :returns: The multipage image'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create(images : List[aspose.imaging.Image], dispose_images : bool) -> aspose.imaging.Image:
        '''Creates a new image the specified images as pages.
        
        :param images: The images.
        :param dispose_images: if set to ``true`` [dispose images].
        :returns: The Image as IMultipageImage'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create_from_images(images : List[aspose.imaging.Image]) -> aspose.imaging.Image:
        '''Creates a new image using the specified images as pages
        
        :param images: The images.
        :returns: The Image as IMultipageImage'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create_from_images(images : List[aspose.imaging.Image], dispose_images : bool) -> aspose.imaging.Image:
        '''Creates a new image the specified images as pages.
        
        :param images: The images.
        :param dispose_images: if set to ``true`` [dispose images].
        :returns: The Image as IMultipageImage'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create_from_files(files : List[str], throw_exception_on_load_error : bool) -> aspose.imaging.Image:
        '''Creates the multipage image containing the specified files as lazy loading pages.
        
        :param files: The files.
        :param throw_exception_on_load_error: if set to ``true`` throw exception on load error.
        :returns: The multipage image'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def create_from_files(files : List[str]) -> aspose.imaging.Image:
        '''Creates the multipage image containing the specified files as lazy loading pages.
        
        :param files: The files.
        :returns: The multipage image'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def get_file_format(file_path : str) -> aspose.imaging.FileFormat:
        '''Gets the file format.
        
        :param file_path: The file path.
        :returns: The determined file format.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def get_file_format(stream : io._IOBase) -> aspose.imaging.FileFormat:
        '''Gets the file format.
        
        :param stream: The stream.
        :returns: The determined file format.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def get_fitting_rectangle(rectangle : aspose.imaging.Rectangle, width : int, height : int) -> aspose.imaging.Rectangle:
        '''Gets rectangle which fits the current image.
        
        :param rectangle: The rectangle to get fitting rectangle for.
        :param width: The object width.
        :param height: The object height.
        :returns: The fitting rectangle or exception if no fitting rectangle can be found.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def get_fitting_rectangle(rectangle : aspose.imaging.Rectangle, pixels : List[int], width : int, height : int) -> aspose.imaging.Rectangle:
        '''Gets rectangle which fits the current image.
        
        :param rectangle: The rectangle to get fitting rectangle for.
        :param pixels: The 32-bit ARGB pixels.
        :param width: The object width.
        :param height: The object height.
        :returns: The fitting rectangle or exception if no fitting rectangle can be found.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def load(file_path : str, load_options : aspose.imaging.LoadOptions) -> aspose.imaging.Image:
        '''Loads a new image from the specified file path or URL.
        If ``filePath`` is a file path the method just opens the file.
        If ``filePath`` is an URL, the method downloads the file, stores it as a temporary one, and opens it.
        
        :param file_path: The file path or URL to load image from.
        :param load_options: The load options.
        :returns: The loaded image.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def load(file_path : str) -> aspose.imaging.Image:
        '''Loads a new image from the specified file path or URL.
        If ``filePath`` is a file path the method just opens the file.
        If ``filePath`` is an URL, the method downloads the file, stores it as a temporary one, and opens it.
        
        :param file_path: The file path or URL to load image from.
        :returns: The loaded image.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def load(stream : io._IOBase, load_options : aspose.imaging.LoadOptions) -> aspose.imaging.Image:
        '''Loads a new image from the specified stream.
        
        :param stream: The stream to load image from.
        :param load_options: The load options.
        :returns: The loaded image.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def load(stream : io._IOBase) -> aspose.imaging.Image:
        '''Loads a new image from the specified stream.
        
        :param stream: The stream to load image from.
        :returns: The loaded image.'''
        raise NotImplementedError()
    
    @overload
    def resize(self, new_width : int, new_height : int, resize_type : aspose.imaging.ResizeType) -> None:
        '''Resizes the image.
        
        :param new_width: The new width.
        :param new_height: The new height.
        :param resize_type: The resize type.'''
        raise NotImplementedError()
    
    @overload
    def resize(self, new_width : int, new_height : int, settings : aspose.imaging.ImageResizeSettings) -> None:
        '''Resizes the image.
        
        :param new_width: The new width.
        :param new_height: The new height.
        :param settings: The resize settings.'''
        raise NotImplementedError()
    
    @overload
    def resize(self, new_width : int, new_height : int) -> None:
        '''Resizes the image. The default :py:attr:`aspose.imaging.ResizeType.NEAREST_NEIGHBOUR_RESAMPLE` is used.
        
        :param new_width: The new width.
        :param new_height: The new height.'''
        raise NotImplementedError()
    
    @overload
    def resize_width_proportionally(self, new_width : int) -> None:
        '''Resizes the width proportionally. The default :py:attr:`aspose.imaging.ResizeType.NEAREST_NEIGHBOUR_RESAMPLE` is used.
        
        :param new_width: The new width.'''
        raise NotImplementedError()
    
    @overload
    def resize_width_proportionally(self, new_width : int, resize_type : aspose.imaging.ResizeType) -> None:
        '''Resizes the width proportionally.
        
        :param new_width: The new width.
        :param resize_type: Type of the resize.'''
        raise NotImplementedError()
    
    @overload
    def resize_width_proportionally(self, new_width : int, settings : aspose.imaging.ImageResizeSettings) -> None:
        '''Resizes the width proportionally.
        
        :param new_width: The new width.
        :param settings: The image resize settings.'''
        raise NotImplementedError()
    
    @overload
    def resize_height_proportionally(self, new_height : int) -> None:
        '''Resizes the height proportionally. The default :py:attr:`aspose.imaging.ResizeType.NEAREST_NEIGHBOUR_RESAMPLE` is used.
        
        :param new_height: The new height.'''
        raise NotImplementedError()
    
    @overload
    def resize_height_proportionally(self, new_height : int, resize_type : aspose.imaging.ResizeType) -> None:
        '''Resizes the height proportionally.
        
        :param new_height: The new height.
        :param resize_type: Type of the resize.'''
        raise NotImplementedError()
    
    @overload
    def resize_height_proportionally(self, new_height : int, settings : aspose.imaging.ImageResizeSettings) -> None:
        '''Resizes the height proportionally.
        
        :param new_height: The new height.
        :param settings: The image resize settings.'''
        raise NotImplementedError()
    
    @overload
    def rotate(self, angle : float, resize_proportionally : bool, background_color : aspose.imaging.Color) -> None:
        '''Rotate image around the center.
        
        :param angle: The rotate angle in degrees. Positive values will rotate clockwise.
        :param resize_proportionally: if set to ``true`` you will have your image size changed according to rotated rectangle (corner points) projections in other case that leaves dimensions untouched and only internal image contents are rotated.
        :param background_color: Color of the background.'''
        raise NotImplementedError()
    
    @overload
    def rotate(self, angle : float) -> None:
        '''Rotate image around the center.
        
        :param angle: The rotate angle in degrees. Positive values will rotate clockwise.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, rectangle : aspose.imaging.Rectangle) -> None:
        '''Cropping the image.
        
        :param rectangle: The rectangle.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, left_shift : int, right_shift : int, top_shift : int, bottom_shift : int) -> None:
        '''Crop image with shifts.
        
        :param left_shift: The left shift.
        :param right_shift: The right shift.
        :param top_shift: The top shift.
        :param bottom_shift: The bottom shift.'''
        raise NotImplementedError()
    
    @overload
    def dither(self, dithering_method : aspose.imaging.DitheringMethod, bits_count : int, custom_palette : aspose.imaging.IColorPalette) -> None:
        '''Performs dithering on the current image.
        
        :param dithering_method: The dithering method.
        :param bits_count: The final bits count for dithering.
        :param custom_palette: The custom palette for dithering.'''
        raise NotImplementedError()
    
    @overload
    def dither(self, dithering_method : aspose.imaging.DitheringMethod, bits_count : int) -> None:
        '''Performs dithering on the current image.
        
        :param dithering_method: The dithering method.
        :param bits_count: The final bits count for dithering.'''
        raise NotImplementedError()
    
    @overload
    def get_default_raw_data(self, rectangle : aspose.imaging.Rectangle, partial_raw_data_loader : aspose.imaging.IPartialRawDataLoader, raw_data_settings : aspose.imaging.RawDataSettings) -> None:
        '''Gets the default raw data array using partial pixel loader.
        
        :param rectangle: The rectangle to get pixels for.
        :param partial_raw_data_loader: The partial raw data loader.
        :param raw_data_settings: The raw data settings.'''
        raise NotImplementedError()
    
    @overload
    def get_default_raw_data(self, rectangle : aspose.imaging.Rectangle, raw_data_settings : aspose.imaging.RawDataSettings) -> List[int]:
        '''Gets the default raw data array.
        
        :param rectangle: The rectangle to get raw data for.
        :param raw_data_settings: The raw data settings.
        :returns: The default raw data array.'''
        raise NotImplementedError()
    
    @overload
    def load_raw_data(self, rectangle : aspose.imaging.Rectangle, raw_data_settings : aspose.imaging.RawDataSettings, raw_data_loader : aspose.imaging.IPartialRawDataLoader) -> None:
        '''Loads raw data.
        
        :param rectangle: The rectangle to load raw data from.
        :param raw_data_settings: The raw data settings to use for loaded data. Note if data is not in the format specified then data conversion will be performed.
        :param raw_data_loader: The raw data loader.'''
        raise NotImplementedError()
    
    @overload
    def load_raw_data(self, rectangle : aspose.imaging.Rectangle, dest_image_bounds : aspose.imaging.Rectangle, raw_data_settings : aspose.imaging.RawDataSettings, raw_data_loader : aspose.imaging.IPartialRawDataLoader) -> None:
        '''Loads raw data.
        
        :param rectangle: The rectangle to load raw data from.
        :param dest_image_bounds: The dest image bounds.
        :param raw_data_settings: The raw data settings to use for loaded data. Note if data is not in the format specified then data conversion will be performed.
        :param raw_data_loader: The raw data loader.'''
        raise NotImplementedError()
    
    @overload
    def binarize_bradley(self, brightness_difference : float, window_size : int) -> None:
        '''Binarization of an image using Bradley\'s adaptive thresholding algorithm using the integral image thresholding
        
        :param brightness_difference: The brightness difference between pixel and the average of an s x s window of pixels centered around this pixel.
        :param window_size: The size of s x s window of pixels centered around this pixel'''
        raise NotImplementedError()
    
    @overload
    def binarize_bradley(self, brightness_difference : float) -> None:
        '''Binarization of an image using Bradley\'s adaptive thresholding algorithm using the integral image thresholding
        
        :param brightness_difference: The brightness difference between pixel and the average of an s x s window of pixels centered around this pixel.'''
        raise NotImplementedError()
    
    @overload
    def blend(self, origin : aspose.imaging.Point, overlay : aspose.imaging.RasterImage, overlay_area : aspose.imaging.Rectangle, overlay_alpha : int) -> None:
        '''Blends this image instance with the ``overlay`` image.
        
        :param origin: The background image blending origin.
        :param overlay: The overlay image.
        :param overlay_area: The overlay area.
        :param overlay_alpha: The overlay alpha.'''
        raise NotImplementedError()
    
    @overload
    def blend(self, origin : aspose.imaging.Point, overlay : aspose.imaging.RasterImage, overlay_alpha : int) -> None:
        '''Blends this image instance with the ``overlay`` image.
        
        :param origin: The background image blending origin.
        :param overlay: The overlay image.
        :param overlay_alpha: The overlay alpha.'''
        raise NotImplementedError()
    
    @overload
    def adjust_gamma(self, gamma_red : float, gamma_green : float, gamma_blue : float) -> None:
        '''Gamma-correction of an image.
        
        :param gamma_red: Gamma for red channel coefficient
        :param gamma_green: Gamma for green channel coefficient
        :param gamma_blue: Gamma for blue channel coefficient'''
        raise NotImplementedError()
    
    @overload
    def adjust_gamma(self, gamma : float) -> None:
        '''Gamma-correction of an image.
        
        :param gamma: Gamma for red, green and blue channels coefficient'''
        raise NotImplementedError()
    
    @overload
    def normalize_angle(self) -> None:
        '''Normalizes the angle.
        This method is applicable to scanned text documents to get rid of the skewed scan.
        This method uses :py:func:`aspose.imaging.RasterImage.get_skew_angle` and :py:func:`aspose.imaging.RasterImage.rotate` methods.'''
        raise NotImplementedError()
    
    @overload
    def normalize_angle(self, resize_proportionally : bool, background_color : aspose.imaging.Color) -> None:
        '''Normalizes the angle.
        This method is applicable to scanned text documents to get rid of the skewed scan.
        This method uses :py:func:`aspose.imaging.RasterImage.get_skew_angle` and :py:func:`aspose.imaging.RasterImage.rotate` methods.
        
        :param resize_proportionally: if set to ``true`` you will have your image size changed according to rotated rectangle (corner points) projections in other case that leaves dimensions untouched and only internal image contents are rotated.
        :param background_color: Color of the background.'''
        raise NotImplementedError()
    
    @overload
    def replace_color(self, old_color : aspose.imaging.Color, old_color_diff : int, new_color : aspose.imaging.Color) -> None:
        '''Replaces one color to another with allowed difference and preserves original alpha value to save smooth edges.
        
        :param old_color: Old color to be replaced.
        :param old_color_diff: Allowed difference in old color to be able to widen replaced color tone.
        :param new_color: New color to replace old color with.'''
        raise NotImplementedError()
    
    @overload
    def replace_color(self, old_color_argb : int, old_color_diff : int, new_color_argb : int) -> None:
        '''Replaces one color to another with allowed difference and preserves original alpha value to save smooth edges.
        
        :param old_color_argb: Old color ARGB value to be replaced.
        :param old_color_diff: Allowed difference in old color to be able to widen replaced color tone.
        :param new_color_argb: New color ARGB value to replace old color with.'''
        raise NotImplementedError()
    
    @overload
    def replace_non_transparent_colors(self, new_color : aspose.imaging.Color) -> None:
        '''Replaces all non-transparent colors with new color and preserves original alpha value to save smooth edges.
        Note: if you use it on images without transparency, all colors will be replaced with a single one.
        
        :param new_color: New color to replace non transparent colors with.'''
        raise NotImplementedError()
    
    @overload
    def replace_non_transparent_colors(self, new_color_argb : int) -> None:
        '''Replaces all non-transparent colors with new color and preserves original alpha value to save smooth edges.
        Note: if you use it on images without transparency, all colors will be replaced with a single one.
        
        :param new_color_argb: New color ARGB value to replace non transparent colors with.'''
        raise NotImplementedError()
    
    def cache_data(self) -> None:
        '''Caches the data and ensures no additional data loading will be performed from the underlying :py:attr:`aspose.imaging.DataStreamSupporter.data_stream_container`.'''
        raise NotImplementedError()
    
    def save_to_stream(self, stream : io._IOBase) -> None:
        '''Saves the object\'s data to the specified stream.
        
        :param stream: The stream to save the object\'s data to.'''
        raise NotImplementedError()
    
    @staticmethod
    def can_load_with_options(file_path : str, load_options : aspose.imaging.LoadOptions) -> bool:
        '''Determines whether image can be loaded from the specified file path and optionally using the specified open options.
        
        :param file_path: The file path.
        :param load_options: The load options.
        :returns: ``true`` if image can be loaded from the specified file; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @staticmethod
    def can_load_stream(stream : io._IOBase) -> bool:
        '''Determines whether image can be loaded from the specified stream.
        
        :param stream: The stream to load from.
        :returns: ``true`` if image can be loaded from the specified stream; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @staticmethod
    def can_load_stream_with_options(stream : io._IOBase, load_options : aspose.imaging.LoadOptions) -> bool:
        '''Determines whether image can be loaded from the specified stream and optionally using the specified ``loadOptions``.
        
        :param stream: The stream to load from.
        :param load_options: The load options.
        :returns: ``true`` if image can be loaded from the specified stream; otherwise, ``false``.'''
        raise NotImplementedError()
    
    @staticmethod
    def get_file_format_of_stream(stream : io._IOBase) -> aspose.imaging.FileFormat:
        '''Gets the file format.
        
        :param stream: The stream.
        :returns: The determined file format.'''
        raise NotImplementedError()
    
    @staticmethod
    def load_with_options(file_path : str, load_options : aspose.imaging.LoadOptions) -> aspose.imaging.Image:
        '''Loads a new image from the specified file path or URL.
        If ``filePath`` is a file path the method just opens the file.
        If ``filePath`` is an URL, the method downloads the file, stores it as a temporary one, and opens it.
        
        :param file_path: The file path or URL to load image from.
        :param load_options: The load options.
        :returns: The loaded image.'''
        raise NotImplementedError()
    
    @staticmethod
    def load_stream_with_options(stream : io._IOBase, load_options : aspose.imaging.LoadOptions) -> aspose.imaging.Image:
        '''Loads a new image from the specified stream.
        
        :param stream: The stream to load image from.
        :param load_options: The load options.
        :returns: The loaded image.'''
        raise NotImplementedError()
    
    @staticmethod
    def load_stream(stream : io._IOBase) -> aspose.imaging.Image:
        '''Loads a new image from the specified stream.
        
        :param stream: The stream to load image from.
        :returns: The loaded image.'''
        raise NotImplementedError()
    
    @staticmethod
    def get_proportional_width(width : int, height : int, new_height : int) -> int:
        '''Gets a proportional width.
        
        :param width: The width.
        :param height: The height.
        :param new_height: The new height.
        :returns: The proportional width.'''
        raise NotImplementedError()
    
    @staticmethod
    def get_proportional_height(width : int, height : int, new_width : int) -> int:
        '''Gets a proportional height.
        
        :param width: The width.
        :param height: The height.
        :param new_width: The new width.
        :returns: The proportional height.'''
        raise NotImplementedError()
    
    def remove_metadata(self) -> None:
        '''Removes this image instance metadata by setting this :py:attr:`aspose.imaging.xmp.IHasXmpData.xmp_data` value to .'''
        raise NotImplementedError()
    
    def try_set_metadata(self, metadata : aspose.imaging.metadata.IImageMetadataFormat) -> bool:
        '''Tries to set a ``metadata`` instance, if this :py:class:`aspose.imaging.Image` instance supports and implements :py:class:`aspose.imaging.metadata.IImageMetadataFormat` type.
        
        :param metadata: The metadata.
        :returns: True, if the :py:class:`aspose.imaging.Image` instance supports and implements :py:class:`aspose.imaging.metadata.IImageMetadataFormat` type; otherwise, false.'''
        raise NotImplementedError()
    
    def can_save(self, options : aspose.imaging.ImageOptionsBase) -> bool:
        '''Determines whether image can be saved to the specified file format represented by the passed save options.
        
        :param options: The save options to use.
        :returns: ``true`` if image can be saved to the specified file format represented by the passed save options; otherwise, ``false``.'''
        raise NotImplementedError()
    
    def resize_by_type(self, new_width : int, new_height : int, resize_type : aspose.imaging.ResizeType) -> None:
        '''Resizes the image.
        
        :param new_width: The new width.
        :param new_height: The new height.
        :param resize_type: The resize type.'''
        raise NotImplementedError()
    
    def resize_by_settings(self, new_width : int, new_height : int, settings : aspose.imaging.ImageResizeSettings) -> None:
        '''Resizes the image.
        
        :param new_width: The new width.
        :param new_height: The new height.
        :param settings: The resize settings.'''
        raise NotImplementedError()
    
    def get_default_options(self, args : List[Any]) -> aspose.imaging.ImageOptionsBase:
        '''Gets the default options.
        
        :param args: The arguments.
        :returns: Default options'''
        raise NotImplementedError()
    
    def get_original_options(self) -> aspose.imaging.ImageOptionsBase:
        '''Gets the options based on the original file settings.
        This can be helpful to keep bit-depth and other parameters of the original image unchanged.
        For example, if we load a black-white PNG image with 1 bit per pixel and then save it using the
        :py:func:`aspose.imaging.DataStreamSupporter.save` method, the output PNG image with 8-bit per pixel will be produced.
        To avoid it and save PNG image with 1-bit per pixel, use this method to get corresponding saving options and pass them
        to the :py:func:`aspose.imaging.Image.save` method as the second parameter.
        
        :returns: The options based on the original file settings.'''
        raise NotImplementedError()
    
    def resize_width_proportionally_settings(self, new_width : int, settings : aspose.imaging.ImageResizeSettings) -> None:
        '''Resizes the width proportionally.
        
        :param new_width: The new width.
        :param settings: The image resize settings.'''
        raise NotImplementedError()
    
    def resize_height_proportionally_settings(self, new_height : int, settings : aspose.imaging.ImageResizeSettings) -> None:
        '''Resizes the height proportionally.
        
        :param new_height: The new height.
        :param settings: The image resize settings.'''
        raise NotImplementedError()
    
    def rotate_flip(self, rotate_flip_type : aspose.imaging.RotateFlipType) -> None:
        '''Rotates, flips, or rotates and flips the image.
        
        :param rotate_flip_type: The rotate flip type.'''
        raise NotImplementedError()
    
    def save_with_options(self, file_path : str, options : aspose.imaging.ImageOptionsBase) -> None:
        '''Saves the object\'s data to the specified file location in the specified file format according to save options.
        
        :param file_path: The file path.
        :param options: The options.'''
        raise NotImplementedError()
    
    def save_with_options_rect(self, file_path : str, options : aspose.imaging.ImageOptionsBase, bounds_rectangle : aspose.imaging.Rectangle) -> None:
        '''Saves the object\'s data to the specified file location in the specified file format according to save options.
        
        :param file_path: The file path.
        :param options: The options.
        :param bounds_rectangle: The destination image bounds rectangle. Set the empty rectangle for use sourse bounds.'''
        raise NotImplementedError()
    
    def save_to_stream_with_options(self, stream : io._IOBase, options_base : aspose.imaging.ImageOptionsBase) -> None:
        '''Saves the image\'s data to the specified stream in the specified file format according to save options.
        
        :param stream: The stream to save the image\'s data to.
        :param options_base: The save options.'''
        raise NotImplementedError()
    
    def save_to_stream_with_options_rect(self, stream : io._IOBase, options_base : aspose.imaging.ImageOptionsBase, bounds_rectangle : aspose.imaging.Rectangle) -> None:
        '''Saves the image\'s data to the specified stream in the specified file format according to save options.
        
        :param stream: The stream to save the image\'s data to.
        :param options_base: The save options.
        :param bounds_rectangle: The destination image bounds rectangle. Set the empty rectangle for use source bounds.'''
        raise NotImplementedError()
    
    def get_serialized_stream(self, image_options : aspose.imaging.ImageOptionsBase, clipping_rectangle : aspose.imaging.Rectangle, page_number : List[int]) -> io._IOBase:
        '''Converts to aps.
        
        :param image_options: The image options.
        :param clipping_rectangle: The clipping rectangle.
        :param page_number: The page number.
        :returns: The serialized stream'''
        raise NotImplementedError()
    
    def set_palette(self, palette : aspose.imaging.IColorPalette, update_colors : bool) -> None:
        '''Sets the image palette.
        
        :param palette: The palette to set.
        :param update_colors: if set to ``true`` colors will be updated according to the new palette; otherwise color indexes remain unchanged. Note that unchanged indexes may crash the image on loading if some indexes have no corresponding palette entries.'''
        raise NotImplementedError()
    
    def get_modify_date(self, use_default : bool) -> datetime:
        '''Gets the date and time the resource image was last modified.
        
        :param use_default: if set to ``true`` uses the information from FileInfo as default value.
        :returns: The date and time the resource image was last modified.'''
        raise NotImplementedError()
    
    def get_default_pixels(self, rectangle : aspose.imaging.Rectangle, partial_pixel_loader : aspose.imaging.IPartialArgb32PixelLoader) -> None:
        '''Gets the default pixels array using partial pixel loader.
        
        :param rectangle: The rectangle to get pixels for.
        :param partial_pixel_loader: The partial pixel loader.'''
        raise NotImplementedError()
    
    def get_default_argb_32_pixels(self, rectangle : aspose.imaging.Rectangle) -> List[int]:
        '''Gets the default 32-bit ARGB pixels array.
        
        :param rectangle: The rectangle to get pixels for.
        :returns: The default pixels array.'''
        raise NotImplementedError()
    
    def get_argb_32_pixel(self, x : int, y : int) -> int:
        '''Gets an image 32-bit ARGB pixel.
        
        :param x: The pixel x location.
        :param y: The pixel y location.
        :returns: The 32-bit ARGB pixel for the specified location.'''
        raise NotImplementedError()
    
    def get_pixel(self, x : int, y : int) -> aspose.imaging.Color:
        '''Gets an image pixel.
        
        :param x: The pixel x location.
        :param y: The pixel y location.
        :returns: The pixel color for the specified location.'''
        raise NotImplementedError()
    
    def set_argb_32_pixel(self, x : int, y : int, argb_32_color : int) -> None:
        '''Sets an image 32-bit ARGB pixel for the specified position.
        
        :param x: The pixel x location.
        :param y: The pixel y location.
        :param argb_32_color: The 32-bit ARGB pixel for the specified position.'''
        raise NotImplementedError()
    
    def set_pixel(self, x : int, y : int, color : aspose.imaging.Color) -> None:
        '''Sets an image pixel for the specified position.
        
        :param x: The pixel x location.
        :param y: The pixel y location.
        :param color: The pixel color for the specified position.'''
        raise NotImplementedError()
    
    def read_scan_line(self, scan_line_index : int) -> List[aspose.imaging.Color]:
        '''Reads the whole scan line by the specified scan line index.
        
        :param scan_line_index: Zero based index of the scan line.
        :returns: The scan line pixel color values array.'''
        raise NotImplementedError()
    
    def read_argb_32_scan_line(self, scan_line_index : int) -> List[int]:
        '''Reads the whole scan line by the specified scan line index.
        
        :param scan_line_index: Zero based index of the scan line.
        :returns: The scan line 32-bit ARGB color values array.'''
        raise NotImplementedError()
    
    def write_scan_line(self, scan_line_index : int, pixels : List[aspose.imaging.Color]) -> None:
        '''Writes the whole scan line to the specified scan line index.
        
        :param scan_line_index: Zero based index of the scan line.
        :param pixels: The pixel colors array to write.'''
        raise NotImplementedError()
    
    def write_argb_32_scan_line(self, scan_line_index : int, argb_32_pixels : List[int]) -> None:
        '''Writes the whole scan line to the specified scan line index.
        
        :param scan_line_index: Zero based index of the scan line.
        :param argb_32_pixels: The 32-bit ARGB colors array to write.'''
        raise NotImplementedError()
    
    def load_partial_argb_32_pixels(self, rectangle : aspose.imaging.Rectangle, partial_pixel_loader : aspose.imaging.IPartialArgb32PixelLoader) -> None:
        '''Loads 32-bit ARGB pixels partially by packs.
        
        :param rectangle: The desired rectangle.
        :param partial_pixel_loader: The 32-bit ARGB pixel loader.'''
        raise NotImplementedError()
    
    def load_partial_pixels(self, desired_rectangle : aspose.imaging.Rectangle, pixel_loader : aspose.imaging.IPartialPixelLoader) -> None:
        '''Loads pixels partially by packs.
        
        :param desired_rectangle: The desired rectangle.
        :param pixel_loader: The pixel loader.'''
        raise NotImplementedError()
    
    def load_argb_32_pixels(self, rectangle : aspose.imaging.Rectangle) -> List[int]:
        '''Loads 32-bit ARGB pixels.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded 32-bit ARGB pixels array.'''
        raise NotImplementedError()
    
    def load_argb_64_pixels(self, rectangle : aspose.imaging.Rectangle) -> List[int]:
        '''Loads 64-bit ARGB pixels.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded 64-bit ARGB pixels array.'''
        raise NotImplementedError()
    
    def load_partial_argb_64_pixels(self, rectangle : aspose.imaging.Rectangle, partial_pixel_loader : aspose.imaging.IPartialArgb64PixelLoader) -> None:
        '''Loads 64-bit ARGB pixels partially by packs.
        
        :param rectangle: The desired rectangle.
        :param partial_pixel_loader: The 64-bit ARGB pixel loader.'''
        raise NotImplementedError()
    
    def load_pixels(self, rectangle : aspose.imaging.Rectangle) -> List[aspose.imaging.Color]:
        '''Loads pixels.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded pixels array.'''
        raise NotImplementedError()
    
    def load_cmyk_pixels(self, rectangle : aspose.imaging.Rectangle) -> List[aspose.imaging.CmykColor]:
        '''Loads pixels in CMYK format.
        This method is deprecated. Please use more effective the :py:func:`aspose.imaging.RasterImage.load_cmyk_32_pixels` method.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded CMYK pixels array.'''
        raise NotImplementedError()
    
    def load_cmyk_32_pixels(self, rectangle : aspose.imaging.Rectangle) -> List[int]:
        '''Loads pixels in CMYK format.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded CMYK pixels presentes as 32-bit inateger values.'''
        raise NotImplementedError()
    
    def save_raw_data(self, data : List[int], data_offset : int, rectangle : aspose.imaging.Rectangle, raw_data_settings : aspose.imaging.RawDataSettings) -> None:
        '''Saves the raw data.
        
        :param data: The raw data.
        :param data_offset: The starting raw data offset.
        :param rectangle: The raw data rectangle.
        :param raw_data_settings: The raw data settings the data is in.'''
        raise NotImplementedError()
    
    def save_argb_32_pixels(self, rectangle : aspose.imaging.Rectangle, pixels : List[int]) -> None:
        '''Saves the 32-bit ARGB pixels.
        
        :param rectangle: The rectangle to save pixels to.
        :param pixels: The 32-bit ARGB pixels array.'''
        raise NotImplementedError()
    
    def save_pixels(self, rectangle : aspose.imaging.Rectangle, pixels : List[aspose.imaging.Color]) -> None:
        '''Saves the pixels.
        
        :param rectangle: The rectangle to save pixels to.
        :param pixels: The pixels array.'''
        raise NotImplementedError()
    
    def save_cmyk_pixels(self, rectangle : aspose.imaging.Rectangle, pixels : List[aspose.imaging.CmykColor]) -> None:
        '''Saves the pixels.
        This method is deprecated. Please use more effective the :py:func:`aspose.imaging.RasterImage.save_cmyk_32_pixels` method.
        
        :param rectangle: The rectangle to save pixels to.
        :param pixels: The CMYK pixels array.'''
        raise NotImplementedError()
    
    def save_cmyk_32_pixels(self, rectangle : aspose.imaging.Rectangle, pixels : List[int]) -> None:
        '''Saves the pixels.
        
        :param rectangle: The rectangle to save pixels to.
        :param pixels: The CMYK pixels presented as the 32-bit integer values.'''
        raise NotImplementedError()
    
    def set_resolution(self, dpi_x : float, dpi_y : float) -> None:
        '''Sets the resolution for this :py:class:`aspose.imaging.RasterImage`.
        
        :param dpi_x: The horizontal resolution, in dots per inch, of the :py:class:`aspose.imaging.RasterImage`.
        :param dpi_y: The vertical resolution, in dots per inch, of the :py:class:`aspose.imaging.RasterImage`.'''
        raise NotImplementedError()
    
    def auto_rotate(self) -> None:
        '''Automatically rotates the image based on orientation data extracted from Exif
        metadata. This method ensures that images are displayed in the correct orientation,
        enhancing user experience and eliminating the need for manual adjustments. By
        analyzing Exif information, the image is rotated accordingly, providing a seamless
        viewing experience across different platforms and devices. This automated rotation
        process simplifies image handling and improves overall usability, especially when
        dealing with large batches of images with varying orientations.'''
        raise NotImplementedError()
    
    def binarize_fixed(self, threshold : int) -> None:
        '''Binarization of an image with predefined threshold
        
        :param threshold: Threshold value. If corresponding gray value of a pixel is greater than threshold, a value of 255 will be assigned to it, 0 otherwise.'''
        raise NotImplementedError()
    
    def binarize_otsu(self) -> None:
        '''Binarization of an image with Otsu thresholding'''
        raise NotImplementedError()
    
    def grayscale(self) -> None:
        '''Transformation of an image to its grayscale representation'''
        raise NotImplementedError()
    
    def normalize_histogram(self) -> None:
        '''Normalizes the image histogram — adjust pixel values to use all available range.'''
        raise NotImplementedError()
    
    def auto_brightness_contrast(self) -> None:
        '''Performs automatic adaptive brightness and contrast normalization for the entire image.'''
        raise NotImplementedError()
    
    def adjust_brightness(self, brightness : int) -> None:
        '''Adjust of a brightness for image.
        
        :param brightness: Brightness value.'''
        raise NotImplementedError()
    
    def adjust_contrast(self, contrast : float) -> None:
        '''Image contrasting
        
        :param contrast: Contrast value (in range [-100; 100])'''
        raise NotImplementedError()
    
    def embed_digital_signature(self, password : str) -> None:
        '''Embed digital sign based on provided password into the image using steganography.
        
        :param password: The password used for generate digital sign data'''
        raise NotImplementedError()
    
    def analyze_percentage_digital_signature(self, password : str) -> int:
        '''Calculates the percentage similarity between the extracted data and the original password.
        
        :param password: The password used to extract the embedded data.
        :returns: The percentage similarity value.'''
        raise NotImplementedError()
    
    def is_digital_signed(self, password : str, percentage_threshold : int) -> bool:
        '''Performs a fast check to determine if the image is digitally signed, using the provided password and threshold.
        
        :param password: The password to check the signing.
        :param percentage_threshold: The threshold (in percentage)[0-100] that determines if the image is considered signed.
        If not specified, a default threshold (``75``) will be applied.
        :returns: True if the image is signed, otherwise false.'''
        raise NotImplementedError()
    
    def get_skew_angle(self) -> float:
        '''Gets the skew angle.
        This method is applicable to scanned text documents, to determine the skew angle when scanning.
        
        :returns: The skew angle, in degrees.'''
        raise NotImplementedError()
    
    def filter(self, rectangle : aspose.imaging.Rectangle, options : aspose.imaging.imagefilters.filteroptions.FilterOptionsBase) -> None:
        '''Filters the specified rectangle.
        
        :param rectangle: The rectangle.
        :param options: The options.'''
        raise NotImplementedError()
    
    def replace_argb(self, old_color_argb : int, old_color_diff : int, new_color_argb : int) -> None:
        '''Replaces one color to another with allowed difference and preserves original alpha value to save smooth edges.
        
        :param old_color_argb: Old color ARGB value to be replaced.
        :param old_color_diff: Allowed difference in old color to be able to widen replaced color tone.
        :param new_color_argb: New color ARGB value to replace old color with.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def data_stream_container(self) -> aspose.imaging.StreamContainer:
        '''Gets the object\'s data stream.'''
        raise NotImplementedError()
    
    @property
    def is_cached(self) -> bool:
        '''Gets a value indicating whether image data is cached currently.'''
        raise NotImplementedError()
    
    @property
    def bits_per_pixel(self) -> int:
        '''Discover the number of bits per pixel in the image effortlessly with this
        property. Ideal for understanding the image\'s pixel depth quickly and accurately.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the image bounds.'''
        raise NotImplementedError()
    
    @property
    def container(self) -> aspose.imaging.Image:
        '''Gets the :py:class:`aspose.imaging.Image` container.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Retrieve the height of the image with this property. Perfect for determining the
        vertical size of the image without hassle.'''
        raise NotImplementedError()
    
    @property
    def palette(self) -> aspose.imaging.IColorPalette:
        '''Gets the color palette. The color palette is not used when pixels are represented directly.'''
        raise NotImplementedError()
    
    @palette.setter
    def palette(self, value : aspose.imaging.IColorPalette) -> None:
        '''Sets the color palette. The color palette is not used when pixels are represented directly.'''
        raise NotImplementedError()
    
    @property
    def use_palette(self) -> bool:
        '''Gets a value indicating whether the image palette is used.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> aspose.imaging.Size:
        '''Gets the image size.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Access the width of the image with this property. Ideal for obtaining the
        horizontal size of the image quickly and efficiently.'''
        raise NotImplementedError()
    
    @property
    def interrupt_monitor(self) -> aspose.imaging.multithreading.InterruptMonitor:
        '''Gets the interrupt monitor.'''
        raise NotImplementedError()
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.imaging.multithreading.InterruptMonitor) -> None:
        '''Sets the interrupt monitor.'''
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
    def auto_adjust_palette(self) -> bool:
        '''Gets a value indicating whether automatic adjust palette.'''
        raise NotImplementedError()
    
    @auto_adjust_palette.setter
    def auto_adjust_palette(self, value : bool) -> None:
        '''Sets a value indicating whether automatic adjust palette.'''
        raise NotImplementedError()
    
    @property
    def has_background_color(self) -> bool:
        '''Gets a value indicating whether image has background color.'''
        raise NotImplementedError()
    
    @has_background_color.setter
    def has_background_color(self, value : bool) -> None:
        '''Sets a value indicating whether image has background color.'''
        raise NotImplementedError()
    
    @property
    def file_format(self) -> aspose.imaging.FileFormat:
        '''Identify the file format of your image with this property. Perfect for
        understanding the format - just straightforward details.'''
        raise NotImplementedError()
    
    @property
    def background_color(self) -> aspose.imaging.Color:
        '''Gets a value for the background color.'''
        raise NotImplementedError()
    
    @background_color.setter
    def background_color(self, value : aspose.imaging.Color) -> None:
        '''Sets a value for the background color.'''
        raise NotImplementedError()
    
    @property
    def metadata(self) -> aspose.imaging.metadata.ImageMetadata:
        '''Gets the image metadata.'''
        raise NotImplementedError()
    
    @property
    def exif_data(self) -> aspose.imaging.exif.ExifData:
        '''Gets the Exif data.'''
        raise NotImplementedError()
    
    @exif_data.setter
    def exif_data(self, value : aspose.imaging.exif.ExifData) -> None:
        '''Sets the Exif data.'''
        raise NotImplementedError()
    
    @property
    def xmp_data(self) -> aspose.imaging.xmp.XmpPacketWrapper:
        '''Gets the Xmp data.'''
        raise NotImplementedError()
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.imaging.xmp.XmpPacketWrapper) -> None:
        '''Sets the Xmp data.'''
        raise NotImplementedError()
    
    @property
    def premultiply_components(self) -> bool:
        '''Gets a value indicating whether the image components must be premultiplied.'''
        raise NotImplementedError()
    
    @premultiply_components.setter
    def premultiply_components(self, value : bool) -> None:
        '''Sets a value indicating whether the image components must be premultiplied.'''
        raise NotImplementedError()
    
    @property
    def use_raw_data(self) -> bool:
        '''Gets a value indicating whether to use raw data loading when the raw data loading is available.'''
        raise NotImplementedError()
    
    @use_raw_data.setter
    def use_raw_data(self, value : bool) -> None:
        '''Sets a value indicating whether to use raw data loading when the raw data loading is available.'''
        raise NotImplementedError()
    
    @property
    def update_xmp_data(self) -> bool:
        '''Gets a value indicating whether to update the XMP metadata.'''
        raise NotImplementedError()
    
    @update_xmp_data.setter
    def update_xmp_data(self, value : bool) -> None:
        '''Sets a value indicating whether to update the XMP metadata.'''
        raise NotImplementedError()
    
    @property
    def raw_indexed_color_converter(self) -> aspose.imaging.IIndexedColorConverter:
        '''Gets the indexed color converter'''
        raise NotImplementedError()
    
    @raw_indexed_color_converter.setter
    def raw_indexed_color_converter(self, value : aspose.imaging.IIndexedColorConverter) -> None:
        '''Sets the indexed color converter'''
        raise NotImplementedError()
    
    @property
    def raw_custom_color_converter(self) -> aspose.imaging.IColorConverter:
        '''Gets the custom color converter'''
        raise NotImplementedError()
    
    @raw_custom_color_converter.setter
    def raw_custom_color_converter(self, value : aspose.imaging.IColorConverter) -> None:
        '''Sets the custom color converter'''
        raise NotImplementedError()
    
    @property
    def raw_fallback_index(self) -> int:
        '''Gets the fallback index to use when palette index is out of bounds'''
        raise NotImplementedError()
    
    @raw_fallback_index.setter
    def raw_fallback_index(self, value : int) -> None:
        '''Sets the fallback index to use when palette index is out of bounds'''
        raise NotImplementedError()
    
    @property
    def raw_data_settings(self) -> aspose.imaging.RawDataSettings:
        '''Gets the current raw data settings. Note when using these settings the data loads without conversion.'''
        raise NotImplementedError()
    
    @property
    def raw_data_format(self) -> aspose.imaging.PixelDataFormat:
        '''Gets the raw data format.'''
        raise NotImplementedError()
    
    @property
    def raw_line_size(self) -> int:
        '''Gets the raw line size in bytes.'''
        raise NotImplementedError()
    
    @property
    def is_raw_data_available(self) -> bool:
        '''Gets a value indicating whether raw data loading is available.'''
        raise NotImplementedError()
    
    @property
    def horizontal_resolution(self) -> float:
        '''Gets the horizontal resolution, in pixels per inch, of this :py:class:`aspose.imaging.RasterImage`.'''
        raise NotImplementedError()
    
    @horizontal_resolution.setter
    def horizontal_resolution(self, value : float) -> None:
        '''Sets the horizontal resolution, in pixels per inch, of this :py:class:`aspose.imaging.RasterImage`.'''
        raise NotImplementedError()
    
    @property
    def vertical_resolution(self) -> float:
        '''Gets the vertical resolution, in pixels per inch, of this :py:class:`aspose.imaging.RasterImage`.'''
        raise NotImplementedError()
    
    @vertical_resolution.setter
    def vertical_resolution(self, value : float) -> None:
        '''Sets the vertical resolution, in pixels per inch, of this :py:class:`aspose.imaging.RasterImage`.'''
        raise NotImplementedError()
    
    @property
    def has_transparent_color(self) -> bool:
        '''Gets a value indicating whether image has transparent color.'''
        raise NotImplementedError()
    
    @has_transparent_color.setter
    def has_transparent_color(self, value : bool) -> None:
        '''Gets a value indicating whether image has transparent color.'''
        raise NotImplementedError()
    
    @property
    def has_alpha(self) -> bool:
        '''Gets a value indicating whether this instance has alpha.'''
        raise NotImplementedError()
    
    @property
    def transparent_color(self) -> aspose.imaging.Color:
        '''Gets the image transparent color.'''
        raise NotImplementedError()
    
    @transparent_color.setter
    def transparent_color(self, value : aspose.imaging.Color) -> None:
        '''Gets the image transparent color.'''
        raise NotImplementedError()
    
    @property
    def image_opacity(self) -> float:
        '''Gets opacity of this image.'''
        raise NotImplementedError()
    
    @property
    def img_data(self) -> aspose.imaging.fileformats.dng.decoder.RawData:
        '''Manage the image data with this property. Whether you\'re retrieving or updating,
        this property provides seamless access to the image data for efficient
        manipulation.'''
        raise NotImplementedError()
    
    @img_data.setter
    def img_data(self, value : aspose.imaging.fileformats.dng.decoder.RawData) -> None:
        '''Manage the image data with this property. Whether you\'re retrieving or updating,
        this property provides seamless access to the image data for efficient
        manipulation.'''
        raise NotImplementedError()
    

