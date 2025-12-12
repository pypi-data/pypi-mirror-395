"""The namespace handles Tiff file format processing."""
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

class CmxColor:
    '''Represents a color value.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def color_model(self) -> aspose.imaging.fileformats.cmx.objectmodel.enums.ColorModels:
        '''Gets the color model.'''
        raise NotImplementedError()
    
    @color_model.setter
    def color_model(self, value : aspose.imaging.fileformats.cmx.objectmodel.enums.ColorModels) -> None:
        '''Sets the color model.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> int:
        '''Gets the color value.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : int) -> None:
        '''Sets the color value.'''
        raise NotImplementedError()
    

class CmxFillStyle:
    '''Fill style for shapes.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def fill_type(self) -> aspose.imaging.fileformats.cmx.objectmodel.enums.FillTypes:
        '''Gets the type of the fill.'''
        raise NotImplementedError()
    
    @fill_type.setter
    def fill_type(self, value : aspose.imaging.fileformats.cmx.objectmodel.enums.FillTypes) -> None:
        '''Sets the type of the fill.'''
        raise NotImplementedError()
    
    @property
    def color1(self) -> aspose.imaging.fileformats.cmx.objectmodel.styles.CmxColor:
        '''Gets the primary color.'''
        raise NotImplementedError()
    
    @color1.setter
    def color1(self, value : aspose.imaging.fileformats.cmx.objectmodel.styles.CmxColor) -> None:
        '''Sets the primary color.'''
        raise NotImplementedError()
    
    @property
    def color2(self) -> aspose.imaging.fileformats.cmx.objectmodel.styles.CmxColor:
        '''Gets the secondary color.'''
        raise NotImplementedError()
    
    @color2.setter
    def color2(self, value : aspose.imaging.fileformats.cmx.objectmodel.styles.CmxColor) -> None:
        '''Sets the secondary color.'''
        raise NotImplementedError()
    
    @property
    def gradient(self) -> aspose.imaging.fileformats.cmx.objectmodel.styles.CmxGradient:
        '''Gets the gradient info.'''
        raise NotImplementedError()
    
    @gradient.setter
    def gradient(self, value : aspose.imaging.fileformats.cmx.objectmodel.styles.CmxGradient) -> None:
        '''Sets the gradient info.'''
        raise NotImplementedError()
    
    @property
    def image_fill(self) -> aspose.imaging.fileformats.cmx.objectmodel.styles.CmxImageFill:
        '''Gets the image fill info.'''
        raise NotImplementedError()
    
    @image_fill.setter
    def image_fill(self, value : aspose.imaging.fileformats.cmx.objectmodel.styles.CmxImageFill) -> None:
        '''Sets the image fill info.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets the fill transform.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets the fill transform.'''
        raise NotImplementedError()
    

class CmxGradient:
    '''Represents a gradient info.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets the angle.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets the angle.'''
        raise NotImplementedError()
    
    @property
    def center_x_offset(self) -> int:
        '''Gets the center x offset.'''
        raise NotImplementedError()
    
    @center_x_offset.setter
    def center_x_offset(self, value : int) -> None:
        '''Sets the center x offset.'''
        raise NotImplementedError()
    
    @property
    def center_y_offset(self) -> int:
        '''Gets the center y offset.'''
        raise NotImplementedError()
    
    @center_y_offset.setter
    def center_y_offset(self, value : int) -> None:
        '''Sets the center y offset.'''
        raise NotImplementedError()
    
    @property
    def colors(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.styles.CmxColor]:
        '''Gets the colors.'''
        raise NotImplementedError()
    
    @colors.setter
    def colors(self, value : List[aspose.imaging.fileformats.cmx.objectmodel.styles.CmxColor]) -> None:
        '''Sets the colors.'''
        raise NotImplementedError()
    
    @property
    def edge_offset(self) -> int:
        '''Gets the edge offset.'''
        raise NotImplementedError()
    
    @edge_offset.setter
    def edge_offset(self, value : int) -> None:
        '''Sets the edge offset.'''
        raise NotImplementedError()
    
    @property
    def mode(self) -> int:
        '''Gets the mode.'''
        raise NotImplementedError()
    
    @mode.setter
    def mode(self, value : int) -> None:
        '''Sets the mode.'''
        raise NotImplementedError()
    
    @property
    def offsets(self) -> List[float]:
        '''Gets the offsets.'''
        raise NotImplementedError()
    
    @offsets.setter
    def offsets(self, value : List[float]) -> None:
        '''Sets the offsets.'''
        raise NotImplementedError()
    
    @property
    def rate_method(self) -> int:
        '''Gets the rate method.'''
        raise NotImplementedError()
    
    @rate_method.setter
    def rate_method(self, value : int) -> None:
        '''Sets the rate method.'''
        raise NotImplementedError()
    
    @property
    def rate_value(self) -> int:
        '''Gets the rate value.'''
        raise NotImplementedError()
    
    @rate_value.setter
    def rate_value(self, value : int) -> None:
        '''Sets the rate value.'''
        raise NotImplementedError()
    
    @property
    def screen(self) -> int:
        '''Gets the screen.'''
        raise NotImplementedError()
    
    @screen.setter
    def screen(self, value : int) -> None:
        '''Sets the screen.'''
        raise NotImplementedError()
    
    @property
    def steps(self) -> int:
        '''Gets the steps.'''
        raise NotImplementedError()
    
    @steps.setter
    def steps(self, value : int) -> None:
        '''Sets the steps.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.cmx.objectmodel.enums.GradientTypes:
        '''Gets the type.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.fileformats.cmx.objectmodel.enums.GradientTypes) -> None:
        '''Sets the type.'''
        raise NotImplementedError()
    

class CmxImageFill:
    '''Image fill info'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def images(self) -> List[aspose.imaging.fileformats.cmx.objectmodel.specs.CmxRasterImage]:
        '''Gets the images.'''
        raise NotImplementedError()
    
    @images.setter
    def images(self, value : List[aspose.imaging.fileformats.cmx.objectmodel.specs.CmxRasterImage]) -> None:
        '''Sets the images.'''
        raise NotImplementedError()
    
    @property
    def procedure(self) -> aspose.imaging.fileformats.cmx.objectmodel.CmxProcedure:
        '''Gets the procedure.'''
        raise NotImplementedError()
    
    @procedure.setter
    def procedure(self, value : aspose.imaging.fileformats.cmx.objectmodel.CmxProcedure) -> None:
        '''Sets the procedure.'''
        raise NotImplementedError()
    
    @property
    def tile_offset_x(self) -> float:
        '''Gets the tile offset X.'''
        raise NotImplementedError()
    
    @tile_offset_x.setter
    def tile_offset_x(self, value : float) -> None:
        '''Sets the tile offset X.'''
        raise NotImplementedError()
    
    @property
    def tile_offset_y(self) -> float:
        '''Gets the tile offset Y.'''
        raise NotImplementedError()
    
    @tile_offset_y.setter
    def tile_offset_y(self, value : float) -> None:
        '''Sets the tile offset Y.'''
        raise NotImplementedError()
    
    @property
    def rcp_offset(self) -> float:
        '''Gets the relative offset between tile rows or columns (depends on :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.styles.CmxImageFill.offset_type`).
        Dimension is fractions of height of width.'''
        raise NotImplementedError()
    
    @rcp_offset.setter
    def rcp_offset(self, value : float) -> None:
        '''Sets the relative offset between tile rows or columns (depends on :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.styles.CmxImageFill.offset_type`).
        Dimension is fractions of height of width.'''
        raise NotImplementedError()
    
    @property
    def offset_type(self) -> aspose.imaging.fileformats.cmx.objectmodel.enums.TileOffsetTypes:
        '''Gets the type of the offset between adjacent tiles.'''
        raise NotImplementedError()
    
    @offset_type.setter
    def offset_type(self, value : aspose.imaging.fileformats.cmx.objectmodel.enums.TileOffsetTypes) -> None:
        '''Sets the type of the offset between adjacent tiles.'''
        raise NotImplementedError()
    
    @property
    def pattern_width(self) -> float:
        '''Gets the width of the pattern.
        Uses common document distance measure unit in case if :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.styles.CmxImageFill.is_relative` is ``false``,
        otherwise has the dimension of the image pixel width fraction.'''
        raise NotImplementedError()
    
    @pattern_width.setter
    def pattern_width(self, value : float) -> None:
        '''Sets the width of the pattern.
        Uses common document distance measure unit in case if :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.styles.CmxImageFill.is_relative` is ``false``,
        otherwise has the dimension of the image pixel width fraction.'''
        raise NotImplementedError()
    
    @property
    def pattern_height(self) -> float:
        '''Gets the height of the pattern.
        Uses common document distance measure unit in case if :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.styles.CmxImageFill.is_relative` is ``false``,
        otherwise has the dimension of the image pixel height fraction.'''
        raise NotImplementedError()
    
    @pattern_height.setter
    def pattern_height(self, value : float) -> None:
        '''Sets the height of the pattern.
        Uses common document distance measure unit in case if :py:attr:`aspose.imaging.fileformats.cmx.objectmodel.styles.CmxImageFill.is_relative` is ``false``,
        otherwise has the dimension of the image pixel height fraction.'''
        raise NotImplementedError()
    
    @property
    def is_relative(self) -> bool:
        '''Gets a value indicating whether patterns size values is relative.'''
        raise NotImplementedError()
    
    @is_relative.setter
    def is_relative(self, value : bool) -> None:
        '''Sets a value indicating whether patterns size values is relative.'''
        raise NotImplementedError()
    
    @property
    def rotate180(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cmx.objectmodel.specs.CmxImageSpec` is upside down.'''
        raise NotImplementedError()
    
    @rotate180.setter
    def rotate180(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cmx.objectmodel.specs.CmxImageSpec` is upside down.'''
        raise NotImplementedError()
    

class CmxOutline:
    '''Represents an outline style.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def line_type(self) -> aspose.imaging.fileformats.cmx.objectmodel.enums.LineTypes:
        '''Gets the type of the line.'''
        raise NotImplementedError()
    
    @line_type.setter
    def line_type(self, value : aspose.imaging.fileformats.cmx.objectmodel.enums.LineTypes) -> None:
        '''Sets the type of the line.'''
        raise NotImplementedError()
    
    @property
    def caps_type(self) -> aspose.imaging.fileformats.cmx.objectmodel.enums.CapsTypes:
        '''Gets the type of the line caps.'''
        raise NotImplementedError()
    
    @caps_type.setter
    def caps_type(self, value : aspose.imaging.fileformats.cmx.objectmodel.enums.CapsTypes) -> None:
        '''Sets the type of the line caps.'''
        raise NotImplementedError()
    
    @property
    def join_type(self) -> aspose.imaging.fileformats.cmx.objectmodel.enums.JoinTypes:
        '''Gets the type of the line join.'''
        raise NotImplementedError()
    
    @join_type.setter
    def join_type(self, value : aspose.imaging.fileformats.cmx.objectmodel.enums.JoinTypes) -> None:
        '''Sets the type of the line join.'''
        raise NotImplementedError()
    
    @property
    def line_width(self) -> float:
        '''Gets the width of the line.
        Uses common document distance measure unit.'''
        raise NotImplementedError()
    
    @line_width.setter
    def line_width(self, value : float) -> None:
        '''Sets the width of the line.
        Uses common document distance measure unit.'''
        raise NotImplementedError()
    
    @property
    def stretch(self) -> float:
        '''Gets the stretch value.'''
        raise NotImplementedError()
    
    @stretch.setter
    def stretch(self, value : float) -> None:
        '''Sets the stretch value.'''
        raise NotImplementedError()
    
    @property
    def angle(self) -> float:
        '''Gets the angle.'''
        raise NotImplementedError()
    
    @angle.setter
    def angle(self, value : float) -> None:
        '''Sets the angle.'''
        raise NotImplementedError()
    
    @property
    def color(self) -> aspose.imaging.fileformats.cmx.objectmodel.styles.CmxColor:
        '''Gets the outline color.'''
        raise NotImplementedError()
    
    @color.setter
    def color(self, value : aspose.imaging.fileformats.cmx.objectmodel.styles.CmxColor) -> None:
        '''Sets the outline color.'''
        raise NotImplementedError()
    
    @property
    def stroke(self) -> List[int]:
        '''Gets the stroke pattern.'''
        raise NotImplementedError()
    
    @stroke.setter
    def stroke(self, value : List[int]) -> None:
        '''Sets the stroke pattern.'''
        raise NotImplementedError()
    
    @property
    def start_arrowhead(self) -> aspose.imaging.fileformats.cmx.objectmodel.specs.CmxArrowSpec:
        '''Gets the shape for the start of the line'''
        raise NotImplementedError()
    
    @start_arrowhead.setter
    def start_arrowhead(self, value : aspose.imaging.fileformats.cmx.objectmodel.specs.CmxArrowSpec) -> None:
        '''Sets the shape for the start of the line'''
        raise NotImplementedError()
    
    @property
    def end_arrowhead(self) -> aspose.imaging.fileformats.cmx.objectmodel.specs.CmxArrowSpec:
        '''Gets the shape for the end of the line'''
        raise NotImplementedError()
    
    @end_arrowhead.setter
    def end_arrowhead(self, value : aspose.imaging.fileformats.cmx.objectmodel.specs.CmxArrowSpec) -> None:
        '''Sets the shape for the end of the line'''
        raise NotImplementedError()
    

class CmxParagraphStyle:
    '''The paragraph style.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def character_spacing(self) -> float:
        '''Gets the character spacing.'''
        raise NotImplementedError()
    
    @character_spacing.setter
    def character_spacing(self, value : float) -> None:
        '''Sets the character spacing.'''
        raise NotImplementedError()
    
    @property
    def language_spacing(self) -> float:
        '''Gets the language spacing.'''
        raise NotImplementedError()
    
    @language_spacing.setter
    def language_spacing(self, value : float) -> None:
        '''Sets the language spacing.'''
        raise NotImplementedError()
    
    @property
    def word_spacing(self) -> float:
        '''Gets the word spacing.'''
        raise NotImplementedError()
    
    @word_spacing.setter
    def word_spacing(self, value : float) -> None:
        '''Sets the word spacing.'''
        raise NotImplementedError()
    
    @property
    def line_spacing(self) -> float:
        '''Gets the line spacing.'''
        raise NotImplementedError()
    
    @line_spacing.setter
    def line_spacing(self, value : float) -> None:
        '''Sets the line spacing.'''
        raise NotImplementedError()
    
    @property
    def horizontal_alignment(self) -> aspose.imaging.fileformats.cmx.objectmodel.enums.ParagraphHorizontalAlignment:
        '''Gets the horizontal alignment.'''
        raise NotImplementedError()
    
    @horizontal_alignment.setter
    def horizontal_alignment(self, value : aspose.imaging.fileformats.cmx.objectmodel.enums.ParagraphHorizontalAlignment) -> None:
        '''Sets the horizontal alignment.'''
        raise NotImplementedError()
    

