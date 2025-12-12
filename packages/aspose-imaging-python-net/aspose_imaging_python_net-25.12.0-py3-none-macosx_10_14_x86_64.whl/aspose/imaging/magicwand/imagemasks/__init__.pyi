"""The namespace handles image masks processing."""
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

class CircleMask(ImageMask):
    '''Describes a circle mask.'''
    
    @overload
    def __init__(self, x : int, y : int, radius : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.imagemasks.CircleMask` class with the specified center point and radius.
        
        :param x: The x-coordinate of the center point of the selected area.
        :param y: The y-coordinate of the center point of the selected area.
        :param radius: Radius of the selected area.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, center : aspose.imaging.Point, radius : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.imagemasks.CircleMask` class with the specified center point and radius.
        
        :param center: The center point of the selected area.
        :param radius: Radius of the selected area.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, rectangle : aspose.imaging.Rectangle) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified rectangle.
        
        :param rectangle: The specified rectangle.
        :returns: A cropped CircleMask or ImageBitMask as ImageMask.
        As ImageBitMask may be returned, fluent call is recommended.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, size : aspose.imaging.Size) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified size.
        
        :param size: The specified size.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, width : int, height : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified width and height.
        
        :param width: The specified width.
        :param height: The specified height.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def union(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the subtraction of the provided mask from current.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the source of the current mask subtracted from the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the provided image subtracted from the current mask.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    def get(self, x : int, y : int) -> bool:
        '''Gets the opacity of the specified pixel.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def inflate(self, size : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Inflates this mask by the specified amount.
        
        :param size: The amount to inflate this mask.
        :returns: An inflated CircleMask as ImageMask.'''
        raise NotImplementedError()
    
    def is_opaque(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is opaque.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def is_transparent(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is transparent.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is transparent; otherwise, false.'''
        raise NotImplementedError()
    
    def get_byte_opacity(self, x : int, y : int) -> int:
        '''Gets the opacity of the specified pixel with byte precision.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: Byte value, representing the opacity of the specified pixel.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Creates a new object that is a copy of the current instance.
        
        :returns: A new object that is a copy of this instance.'''
        raise NotImplementedError()
    
    def get_feathered(self, settings : aspose.imaging.magicwand.imagemasks.FeatheringSettings) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Gets grayscale mask with the border feathered with the specified settings.
        
        :param settings: Feathering settings.
        :returns: :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask` with feathered border.'''
        raise NotImplementedError()
    
    def apply(self) -> None:
        '''Applies current mask to the :py:class:`aspose.imaging.RasterImage` source, if exists.'''
        raise NotImplementedError()
    
    def apply_to(self, image : aspose.imaging.RasterImage) -> None:
        '''Applies current mask to the specified :py:class:`aspose.imaging.RasterImage`.
        
        :param image: Image to apply mask to.'''
        raise NotImplementedError()
    
    def invert(self) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the inversion of the current mask.
        
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> aspose.imaging.RasterImage:
        '''Gets the source image used to create this mask, if exists.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def selection_bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds, in pixels, of this mask.'''
        raise NotImplementedError()
    

class EmptyImageMask(ImageMask):
    '''Describes an empty non-abstract mask.'''
    
    def __init__(self, width : int, height : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.imagemasks.EmptyImageMask` class with the specified width and height.
        
        :param width: Width of the mask.
        :param height: Height of the mask.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, rectangle : aspose.imaging.Rectangle) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified rectangle.
        
        :param rectangle: The specified rectangle.
        :returns: A cropped EmptyImageMask as ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, size : aspose.imaging.Size) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified size.
        
        :param size: The specified size.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, width : int, height : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified width and height.
        
        :param width: The specified width.
        :param height: The specified height.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def union(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the subtraction of the provided mask from current.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the source of the current mask subtracted from the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the provided image subtracted from the current mask.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    def get(self, x : int, y : int) -> bool:
        '''Gets the opacity of the specified pixel.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def inflate(self, size : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Inflates this mask by the specified amount.
        
        :param size: The amount to inflate this mask.
        :returns: An inflated EmptyImageMask as ImageMask.'''
        raise NotImplementedError()
    
    def is_opaque(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is opaque.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def is_transparent(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is transparent.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is transparent; otherwise, false.'''
        raise NotImplementedError()
    
    def get_byte_opacity(self, x : int, y : int) -> int:
        '''Gets the opacity of the specified pixel with byte precision.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: Byte value, representing the opacity of the specified pixel.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Creates a new object that is a copy of the current instance.
        
        :returns: A new object that is a copy of this instance.'''
        raise NotImplementedError()
    
    def get_feathered(self, settings : aspose.imaging.magicwand.imagemasks.FeatheringSettings) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Gets grayscale mask with the border feathered with the specified settings.
        
        :param settings: Feathering settings.
        :returns: :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask` with feathered border.'''
        raise NotImplementedError()
    
    def apply(self) -> None:
        '''Applies current mask to the :py:class:`aspose.imaging.RasterImage` source, if exists.'''
        raise NotImplementedError()
    
    def apply_to(self, image : aspose.imaging.RasterImage) -> None:
        '''Applies current mask to the specified :py:class:`aspose.imaging.RasterImage`.
        
        :param image: Image to apply mask to.'''
        raise NotImplementedError()
    
    def invert(self) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the inversion of the current mask.
        
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> aspose.imaging.RasterImage:
        '''Gets the source image used to create this mask, if exists.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def selection_bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds of the selected part of the mask, in pixels.'''
        raise NotImplementedError()
    

class FeatheringSettings:
    '''A feathering settings class.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.MagicWandSettings` class.'''
        raise NotImplementedError()
    
    @property
    def size(self) -> int:
        '''Gets the feathering size.'''
        raise NotImplementedError()
    
    @size.setter
    def size(self, value : int) -> None:
        '''Sets the feathering size.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> aspose.imaging.magicwand.imagemasks.FeatheringMode:
        '''Gets the feathering algorithm mode.'''
        raise NotImplementedError()
    
    @mode.setter
    def mode(self, value : aspose.imaging.magicwand.imagemasks.FeatheringMode) -> None:
        '''Sets the feathering algorithm mode.'''
        raise NotImplementedError()
    

class IImageMask:
    '''Describes a mask.'''
    
    def is_opaque(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is opaque.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def is_transparent(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is transparent.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is transparent; otherwise, false.'''
        raise NotImplementedError()
    
    def get_byte_opacity(self, x : int, y : int) -> int:
        '''Gets the opacity of the specified pixel with byte precision.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: Byte value, representing the opacity of the specified pixel.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        raise NotImplementedError()
    
    @property
    def source(self) -> aspose.imaging.RasterImage:
        '''Gets the source image used to create this mask, if exists.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def selection_bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds of the selected part of the mask, in pixels.'''
        raise NotImplementedError()
    

class ImageBitMask(ImageMask):
    '''Describes a binary image mask.'''
    
    @overload
    def __init__(self, width : int, height : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask` class with the specified width and height.
        
        :param width: Width of the mask.
        :param height: Height of the mask.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.RasterImage) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask` class with the size of the specified existing :py:class:`aspose.imaging.RasterImage`.
        Specified :py:class:`aspose.imaging.RasterImage` will be stored as source image.
        
        :param image: Source image.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, rectangle : aspose.imaging.Rectangle) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified rectangle.
        
        :param rectangle: The specified rectangle.
        :returns: A cropped :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask` as :py:class:`aspose.imaging.magicwand.imagemasks.ImageMask`.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, size : aspose.imaging.Size) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified size.
        
        :param size: The specified size.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, width : int, height : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified width and height.
        
        :param width: The specified width.
        :param height: The specified height.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def union(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the subtraction of the provided mask from current.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the source of the current mask subtracted from the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the provided image subtracted from the current mask.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    def get(self, x : int, y : int) -> bool:
        '''Gets the opacity of the specified pixel.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def inflate(self, size : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Inflates this mask by the specified amount.
        
        :param size: The amount to inflate this mask.
        :returns: An inflated :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask` as :py:class:`aspose.imaging.magicwand.imagemasks.ImageMask`.'''
        raise NotImplementedError()
    
    def is_opaque(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is opaque.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def is_transparent(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is transparent.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is transparent; otherwise, false.'''
        raise NotImplementedError()
    
    def get_byte_opacity(self, x : int, y : int) -> int:
        '''Gets the opacity of the specified pixel with byte precision.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: Byte value, representing the opacity of the specified pixel.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Creates a new object that is a copy of the current instance.
        
        :returns: A new object that is a copy of this instance.'''
        raise NotImplementedError()
    
    def get_feathered(self, settings : aspose.imaging.magicwand.imagemasks.FeatheringSettings) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Gets grayscale mask with the border feathered with the specified settings.
        
        :param settings: Feathering settings.
        :returns: :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask` with feathered border.'''
        raise NotImplementedError()
    
    def apply(self) -> None:
        '''Applies current mask to the :py:class:`aspose.imaging.RasterImage` source, if exists.'''
        raise NotImplementedError()
    
    def apply_to(self, image : aspose.imaging.RasterImage) -> None:
        '''Applies current mask to the specified :py:class:`aspose.imaging.RasterImage`.
        
        :param image: Image to apply mask to.'''
        raise NotImplementedError()
    
    def invert(self) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the inversion of the current mask.
        
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    def set_mask_pixel(self, x : int, y : int, value : bool) -> None:
        '''Sets the opacity to the specified pixel.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :param value: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> aspose.imaging.RasterImage:
        '''Gets the source image used to create this mask, if exists.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def selection_bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds of the selected part of the mask, in pixels.'''
        raise NotImplementedError()
    

class ImageGrayscaleMask(IImageMask):
    '''Describes a grayscale image mask.'''
    
    @overload
    def __init__(self, width : int, height : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask` class with the specified width and height.
        
        :param width: Width of the mask.
        :param height: Height of the mask.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, image : aspose.imaging.RasterImage) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask` class with the size of the specified existing :py:class:`aspose.imaging.RasterImage`.
        Specified :py:class:`aspose.imaging.RasterImage` will be stored as source image.
        
        :param image: Source image.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, size : aspose.imaging.Size) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Crops mask with the specified size.
        
        :param size: The specified size.
        :returns: An cropped :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask`.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, width : int, height : int) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Crops mask with the specified width and height.
        
        :param width: The specified width.
        :param height: The specified height.
        :returns: An cropped :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask`.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, rectangle : aspose.imaging.Rectangle) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Crops mask with the specified rectangle.
        
        :param rectangle: The specified rectangle.
        :returns: A cropped :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask`.'''
        raise NotImplementedError()
    
    def get(self, x : int, y : int) -> int:
        '''Gets or sets the opacity of the specified pixel.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: Byte value; 0 if transparent; 255 if opaque.'''
        raise NotImplementedError()
    
    def set(self, x : int, y : int, value : int) -> None:
        '''Sets the opacity of the specified pixel.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :param value: Byte value; 0 if transparent; 255 if opaque.'''
        raise NotImplementedError()
    
    def is_opaque(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is opaque.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def is_transparent(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is transparent.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is transparent; otherwise, false.'''
        raise NotImplementedError()
    
    def get_byte_opacity(self, x : int, y : int) -> int:
        '''Gets the opacity of the specified pixel with byte precision.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: Byte value, representing the opacity of the specified pixel.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Creates a new object that is a copy of the current instance.
        
        :returns: A new object that is a copy of this instance.'''
        raise NotImplementedError()
    
    def apply(self) -> None:
        '''Applies current mask to the :py:class:`aspose.imaging.RasterImage` source, if exists.'''
        raise NotImplementedError()
    
    def apply_to(self, image : aspose.imaging.RasterImage) -> None:
        '''Applies current mask to the specified :py:class:`aspose.imaging.RasterImage`.
        
        :param image: Image to apply mask to.'''
        raise NotImplementedError()
    
    def invert(self) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Gets the inversion of the current mask.
        
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask`.'''
        raise NotImplementedError()
    
    def union(self, mask : aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Union of two masks.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask`.'''
        raise NotImplementedError()
    
    def subtract(self, mask : aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Gets the subtraction of the provided mask from current.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask`.'''
        raise NotImplementedError()
    
    def intersect(self, mask : aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Gets the intersection of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask`.'''
        raise NotImplementedError()
    
    def exclusive_disjunction(self, mask : aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Gets the exclusive disjunction of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask`.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> aspose.imaging.RasterImage:
        '''Gets the source image used to create this mask, if exists.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def selection_bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds of the selected part of the mask, in pixels.'''
        raise NotImplementedError()
    

class ImageMask(IImageMask):
    '''Describes a binary image mask.'''
    
    @overload
    def crop(self, size : aspose.imaging.Size) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified size.
        
        :param size: The specified size.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, width : int, height : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified width and height.
        
        :param width: The specified width.
        :param height: The specified height.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, rectangle : aspose.imaging.Rectangle) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified rectangle.
        
        :param rectangle: The specified rectangle.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def union(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the subtraction of the provided mask from current.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the source of the current mask subtracted from the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the provided image subtracted from the current mask.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    def get(self, x : int, y : int) -> bool:
        '''Gets the opacity of the specified pixel.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def inflate(self, size : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Inflates this mask by the specified amount.
        
        :param size: The amount to inflate this mask.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    def is_opaque(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is opaque.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def is_transparent(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is transparent.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is transparent; otherwise, false.'''
        raise NotImplementedError()
    
    def get_byte_opacity(self, x : int, y : int) -> int:
        '''Gets the opacity of the specified pixel with byte precision.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: Byte value, representing the opacity of the specified pixel.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Creates a new object that is a copy of the current instance.
        
        :returns: A new object that is a copy of this instance.'''
        raise NotImplementedError()
    
    def get_feathered(self, settings : aspose.imaging.magicwand.imagemasks.FeatheringSettings) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Gets grayscale mask with the border feathered with the specified settings.
        
        :param settings: Feathering settings.
        :returns: :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask` with feathered border.'''
        raise NotImplementedError()
    
    def apply(self) -> None:
        '''Applies current mask to the :py:class:`aspose.imaging.RasterImage` source, if exists.'''
        raise NotImplementedError()
    
    def apply_to(self, image : aspose.imaging.RasterImage) -> None:
        '''Applies current mask to the specified :py:class:`aspose.imaging.RasterImage`.
        
        :param image: Image to apply mask to.'''
        raise NotImplementedError()
    
    def invert(self) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the inversion of the current mask.
        
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> aspose.imaging.RasterImage:
        '''Gets the source image used to create this mask, if exists.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def selection_bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds of the selected part of the mask, in pixels.'''
        raise NotImplementedError()
    

class RectangleMask(ImageMask):
    '''Describes a rectangle mask.'''
    
    @overload
    def __init__(self, x : int, y : int, width : int, height : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.imagemasks.RectangleMask` class with the specified left-top point, width and height.
        
        :param x: The x-coordinate of the left-top point of the selected area.
        :param y: The y-coordinate of the left-top point of the selected area.
        :param width: Width of the selected area.
        :param height: Height of the selected area.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, selected_area : aspose.imaging.Rectangle) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.magicwand.imagemasks.RectangleMask` class with the specified rectangle.
        
        :param selected_area: Selected area specified as a rectangle.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, rectangle : aspose.imaging.Rectangle) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified rectangle.
        
        :param rectangle: The specified rectangle.
        :returns: A cropped RectangleMask as ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, size : aspose.imaging.Size) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified size.
        
        :param size: The specified size.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def crop(self, width : int, height : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Crops mask with the specified width and height.
        
        :param width: The specified width.
        :param height: The specified height.
        :returns: An ImageMask.'''
        raise NotImplementedError()
    
    @overload
    def union(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def union(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the union of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the subtraction of the provided mask from current.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the source of the current mask subtracted from the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def subtract(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the result of magic wand selection applied to the provided image subtracted from the current mask.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def intersect(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the intersection of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, mask : aspose.imaging.magicwand.imagemasks.ImageMask) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of current mask with provided.
        
        :param mask: Provided mask
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the source of the mask.
        
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @overload
    def exclusive_disjunction(self, image : aspose.imaging.RasterImage, settings : aspose.imaging.magicwand.MagicWandSettings) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the exclusive disjunction of the current mask with the result of magic wand selection applied to the provided image.
        
        :param image: Image for magic wand.
        :param settings: Magic wand settings.
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    def get(self, x : int, y : int) -> bool:
        '''Gets the opacity of the specified pixel.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def inflate(self, size : int) -> aspose.imaging.magicwand.imagemasks.ImageMask:
        '''Inflates this mask by the specified amount.
        
        :param size: The amount to inflate this mask.
        :returns: An inflated RectangleMask as ImageMask.'''
        raise NotImplementedError()
    
    def is_opaque(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is opaque.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is opaque; otherwise, false.'''
        raise NotImplementedError()
    
    def is_transparent(self, x : int, y : int) -> bool:
        '''Checks if the specified pixel is transparent.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: true if the specified pixel is transparent; otherwise, false.'''
        raise NotImplementedError()
    
    def get_byte_opacity(self, x : int, y : int) -> int:
        '''Gets the opacity of the specified pixel with byte precision.
        
        :param x: The x-coordinate of the pixel.
        :param y: The y-coordinate of the pixel.
        :returns: Byte value, representing the opacity of the specified pixel.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Creates a new object that is a copy of the current instance.
        
        :returns: A new object that is a copy of this instance.'''
        raise NotImplementedError()
    
    def get_feathered(self, settings : aspose.imaging.magicwand.imagemasks.FeatheringSettings) -> aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask:
        '''Gets grayscale mask with the border feathered with the specified settings.
        
        :param settings: Feathering settings.
        :returns: :py:class:`aspose.imaging.magicwand.imagemasks.ImageGrayscaleMask` with feathered border.'''
        raise NotImplementedError()
    
    def apply(self) -> None:
        '''Applies current mask to the :py:class:`aspose.imaging.RasterImage` source, if exists.'''
        raise NotImplementedError()
    
    def apply_to(self, image : aspose.imaging.RasterImage) -> None:
        '''Applies current mask to the specified :py:class:`aspose.imaging.RasterImage`.
        
        :param image: Image to apply mask to.'''
        raise NotImplementedError()
    
    def invert(self) -> aspose.imaging.magicwand.imagemasks.ImageBitMask:
        '''Gets the inversion of the current mask.
        
        :returns: New :py:class:`aspose.imaging.magicwand.imagemasks.ImageBitMask`.'''
        raise NotImplementedError()
    
    @property
    def source(self) -> aspose.imaging.RasterImage:
        '''Gets the source image used to create this mask, if exists.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds, in pixels, of this mask.'''
        raise NotImplementedError()
    
    @property
    def selection_bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the bounds of the selected part of the mask, in pixels.'''
        raise NotImplementedError()
    

class FeatheringMode(enum.Enum):
    NONE = enum.auto()
    '''No feathering'''
    MATHEMATICALLY_CORRECT = enum.auto()
    '''Mathematically correct algorithm that will most likely result with a well distinguishable line on the border of the selected area'''
    ADJUSTED = enum.auto()
    '''Adjusted algorithm that will create a smooth border of the selected area'''

