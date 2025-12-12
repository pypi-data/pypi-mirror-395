"""The namespace handles WMF file format processing."""
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

class WmfImage(aspose.imaging.fileformats.emf.MetaImage):
    '''Manipulate Microsoft Windows Metafile (WMF) images with our API, seamlessly
    handling both vector and bitmap data stored within variable-length records.
    Resize, rotate, and flip images with ease while setting custom image palettes.
    Convert WMF files to compressed WMZ formats or save them in raster image formats
    for versatile usage across platforms and applications.'''
    
    @overload
    def __init__(self) -> None:
        '''Create a new instance of the :py:class:`aspose.imaging.fileformats.wmf.WmfImage` class, initializing it for
        further manipulation and processing of Windows Metafile (WMF) image data. This
        constructor provides a foundational object for working with WMF images, enabling
        seamless integration of WMF image handling capabilities into your application\'s
        functionality.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, width : int, height : int) -> None:
        '''Instantiate a new instance of the :py:class:`aspose.imaging.fileformats.wmf.WmfImage` class with customizable
        width and height parameters, facilitating the creation of blank WMF images
        tailored to specific dimensions. Utilize this constructor to dynamically generate
        WMF images with precise dimensions, enabling flexible image creation and
        manipulation within your application.
        
        :param width: The width.
        :param height: The height.'''
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
    def save(self, stream : io._IOBase, options_base : aspose.imaging.ImageOptionsBase, bounds_rectangle : aspose.imaging.Rectangle) -> None:
        '''Saves the image\'s data to the specified stream in the specified file format according to save options.
        
        :param stream: The stream to save the image\'s data to.
        :param options_base: The save options.
        :param bounds_rectangle: The destination image bounds rectangle. Set the empty rectangle for use source bounds.'''
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
        '''Resizes the specified new width.
        
        :param new_width: The new width.
        :param new_height: The new height.
        :param resize_type: Type of the resize.'''
        raise NotImplementedError()
    
    @overload
    def resize(self, new_width : int, new_height : int, settings : aspose.imaging.ImageResizeSettings) -> None:
        '''Resizes the image with extended options.
        
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
    def crop(self, rectangle : aspose.imaging.Rectangle) -> None:
        '''Crops the specified rectangle.
        
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
    def remove_background(self) -> None:
        '''Removes the background.'''
        raise NotImplementedError()
    
    @overload
    def remove_background(self, settings : aspose.imaging.RemoveBackgroundSettings) -> None:
        '''Removes the background.
        
        :param settings: The settings.'''
        raise NotImplementedError()
    
    def cache_data(self) -> None:
        '''Efficiently cache the data, eliminating the need for additional loading from the
        underlying :py:attr:`aspose.imaging.DataStreamSupporter.data_stream_container`. Utilize this
        method to optimize performance and minimize resource usage within your application
        by storing and accessing local data cache.'''
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
        '''Removes metadata.'''
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
        '''Gets the default image options.
        
        :param args: The arguments.
        :returns: The default image options.'''
        raise NotImplementedError()
    
    def get_original_options(self) -> aspose.imaging.ImageOptionsBase:
        '''Gets the original image options.
        
        :returns: The original image options.'''
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
        
        :param rotate_flip_type: Type of the rotate flip.'''
        raise NotImplementedError()
    
    def rotate(self, angle : float) -> None:
        '''Rotate image around the center.
        
        :param angle: The rotate angle in degrees. Positive values will rotate clockwise.'''
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
        '''Apply a specified palette to the image, enabling customization of color
        representation. Utilize this method to enhance visual rendering and achieve
        specific color effects within your application.
        
        :param palette: The palette to set.
        :param update_colors: if set to ``true`` colors will be updated according to the new palette; otherwise color
        indexes remain unchanged. Note that unchanged indexes may crash the image on loading if some indexes have no
        corresponding palette entries.'''
        raise NotImplementedError()
    
    def get_embedded_images(self) -> List[aspose.imaging.EmbeddedImage]:
        '''Gets the embedded images.
        
        :returns: Array of images'''
        raise NotImplementedError()
    
    def get_used_fonts(self) -> List[str]:
        '''Retrieve the list of fonts used within the metafile, providing insight into the
        font resources utilized in the image. Utilize this method to analyze font usage
        and ensure font availability for rendering or further processing within your application.
        
        :returns: The font list'''
        raise NotImplementedError()
    
    def get_missed_fonts(self) -> List[str]:
        '''Returns the list of fonts which used inside metafile but not found.
        
        :returns: The font list'''
        raise NotImplementedError()
    
    def resize_canvas(self, new_rectangle : aspose.imaging.Rectangle) -> None:
        '''Resize the canvas of the image, adjusting its dimensions while retaining the image
        content. Utilize this method to modify the size of the canvas without altering the
        content, facilitating layout adjustments and composition changes within your
        application.
        
        :param new_rectangle: The new rectangle.'''
        raise NotImplementedError()
    
    def add_record(self, record : aspose.imaging.fileformats.wmf.objects.WmfObject) -> int:
        '''Incorporate the specified record object into the image, enriching its content with
        additional data or metadata. Utilize this method to seamlessly integrate record
        objects into the image, facilitating comprehensive data storage and organization
        within your application.
        
        :param record: The record.
        :returns: Number of record.'''
        raise NotImplementedError()
    
    def get_post_script(self) -> str:
        '''Access the PostScript data associated with the image, providing detailed
        information about its structure or content. Utilize this method to retrieve
        PostScript data for further analysis or processing within your application,
        enabling advanced functionality related to PostScript rendering or manipulation.
        
        :returns: The post script'''
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
        '''Retrieve a boolean value indicating whether the object\'s data is currently cached,
        eliminating the need for additional data reading operations. Utilize this property
        to optimize performance by determining if the object\'s data is readily available
        without the need for costly data retrieval processes within your application.'''
        raise NotImplementedError()
    
    @property
    def bits_per_pixel(self) -> int:
        '''Retrieve the count of bits per pixel for the image, indicating the level of color
        depth or granularity. Utilize this property to determine the image\'s color
        representation and precision, facilitating compatibility checks and color-related
        processing within your application.'''
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
        '''Gets the image height.'''
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
        '''Gets the image width.'''
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
        '''Access the file format value associated with the image, providing information
        about the format in which the image is stored. Utilize this property to determine
        the file format of the image, facilitating compatibility checks and
        format-specific processing within your application.'''
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
    def size_f(self) -> aspose.imaging.SizeF:
        '''Gets the object size, in inches.'''
        raise NotImplementedError()
    
    @property
    def width_f(self) -> float:
        '''Access the width of the image, indicating the number of pixels along its
        horizontal axis. Utilize this property to determine the image\'s spatial dimensions
        and aspect ratio, enabling precise layout and rendering adjustments within your
        application.'''
        raise NotImplementedError()
    
    @property
    def height_f(self) -> float:
        '''Access the image\'s height, representing the number of pixels along its vertical
        axis. Utilize this property to ascertain the image\'s spatial dimensions and aspect
        ratio, enabling accurate layout and rendering adjustments within your application.'''
        raise NotImplementedError()
    
    @property
    def records(self) -> aspose.imaging.fileformats.emf.MetaObjectList:
        '''Gets the records.'''
        raise NotImplementedError()
    
    @records.setter
    def records(self, value : aspose.imaging.fileformats.emf.MetaObjectList) -> None:
        '''Sets the records.'''
        raise NotImplementedError()
    
    @property
    def inch(self) -> int:
        '''Access or modify the inch property, representing a unit of measurement typically
        used for specifying physical dimensions in print or display contexts. Utilize this
        property to establish or retrieve inch values associated with the image,
        facilitating accurate representation of physical dimensions within your application.'''
        raise NotImplementedError()
    
    @inch.setter
    def inch(self, value : int) -> None:
        '''Access or modify the inch property, representing a unit of measurement typically
        used for specifying physical dimensions in print or display contexts. Utilize this
        property to establish or retrieve inch values associated with the image,
        facilitating accurate representation of physical dimensions within your application.'''
        raise NotImplementedError()
    
    @property
    def frame_bounds(self) -> aspose.imaging.Rectangle:
        '''Access the bounds of the frame, indicating its position and dimensions within the
        image. Utilize this property to retrieve detailed information about the frame\'s
        spatial location, enabling precise manipulation and rendering within your application.'''
        raise NotImplementedError()
    

class WmfRenderMode(enum.Enum):
    WMF_RECORDS_ONLY = enum.auto()
    '''The render wmf records only without ebedded emf.'''
    EMBEDDED_EMF_ONLY = enum.auto()
    '''The render embedded emf only.'''
    BOTH = enum.auto()
    '''The render both in order.'''
    AUTO = enum.auto()
    '''The auto render. If exists embedded emf, then render emf else render wmf.'''

