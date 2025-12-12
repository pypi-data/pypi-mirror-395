"""The Open document objects"""
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

class OdGraphicStyle:
    '''The open document graphic style.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def copy(self) -> aspose.imaging.fileformats.opendocument.objects.OdGraphicStyle:
        '''Copies this instance.
        
        :returns: Gets the copy of this instance.'''
        raise NotImplementedError()
    
    @property
    def brush(self) -> aspose.imaging.fileformats.opendocument.objects.brush.OdBrush:
        '''Gets the brush.'''
        raise NotImplementedError()
    
    @brush.setter
    def brush(self, value : aspose.imaging.fileformats.opendocument.objects.brush.OdBrush) -> None:
        '''Gets the brush.'''
        raise NotImplementedError()
    
    @property
    def pen(self) -> aspose.imaging.fileformats.opendocument.objects.pen.OdPen:
        '''Gets the pen.'''
        raise NotImplementedError()
    
    @property
    def font(self) -> aspose.imaging.fileformats.opendocument.objects.font.OdFont:
        '''Gets the font.'''
        raise NotImplementedError()
    
    @property
    def text_color(self) -> int:
        '''Gets the color of the text.'''
        raise NotImplementedError()
    
    @text_color.setter
    def text_color(self, value : int) -> None:
        '''Sets the color of the text.'''
        raise NotImplementedError()
    
    @property
    def text_align(self) -> aspose.imaging.fileformats.opendocument.enums.OdTextAlignModeFlags:
        '''Gets the text align.'''
        raise NotImplementedError()
    
    @text_align.setter
    def text_align(self, value : aspose.imaging.fileformats.opendocument.enums.OdTextAlignModeFlags) -> None:
        '''Sets the text align.'''
        raise NotImplementedError()
    
    @property
    def line_height(self) -> int:
        '''Gets the height of the line.'''
        raise NotImplementedError()
    
    @line_height.setter
    def line_height(self, value : int) -> None:
        '''Sets the height of the line.'''
        raise NotImplementedError()
    
    @property
    def transform_info(self) -> aspose.imaging.fileformats.opendocument.objects.OdTransformInfo:
        '''Gets the transform information.'''
        raise NotImplementedError()
    
    @property
    def start_marker(self) -> aspose.imaging.fileformats.opendocument.objects.graphic.OdMarker:
        '''Gets the start marker.'''
        raise NotImplementedError()
    
    @start_marker.setter
    def start_marker(self, value : aspose.imaging.fileformats.opendocument.objects.graphic.OdMarker) -> None:
        '''Sets the start marker.'''
        raise NotImplementedError()
    
    @property
    def end_marker(self) -> aspose.imaging.fileformats.opendocument.objects.graphic.OdMarker:
        '''Gets the end marker.'''
        raise NotImplementedError()
    
    @end_marker.setter
    def end_marker(self, value : aspose.imaging.fileformats.opendocument.objects.graphic.OdMarker) -> None:
        '''Sets the end marker.'''
        raise NotImplementedError()
    
    @property
    def start_marker_width(self) -> float:
        '''Gets the start width of the marker.'''
        raise NotImplementedError()
    
    @start_marker_width.setter
    def start_marker_width(self, value : float) -> None:
        '''Sets the start width of the marker.'''
        raise NotImplementedError()
    
    @property
    def end_marker_width(self) -> float:
        '''Gets the end width of the marker.'''
        raise NotImplementedError()
    
    @end_marker_width.setter
    def end_marker_width(self, value : float) -> None:
        '''Sets the end width of the marker.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> int:
        '''Gets the opacity.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : int) -> None:
        '''Sets the opacity.'''
        raise NotImplementedError()
    
    @property
    def space_before(self) -> float:
        '''Gets the space before.'''
        raise NotImplementedError()
    
    @space_before.setter
    def space_before(self, value : float) -> None:
        '''Sets the space before.'''
        raise NotImplementedError()
    
    @property
    def padding_top(self) -> float:
        '''Gets the padding top.'''
        raise NotImplementedError()
    
    @padding_top.setter
    def padding_top(self, value : float) -> None:
        '''Sets the padding top.'''
        raise NotImplementedError()
    
    @property
    def padding_left(self) -> float:
        '''Gets the padding left.'''
        raise NotImplementedError()
    
    @padding_left.setter
    def padding_left(self, value : float) -> None:
        '''Sets the padding left.'''
        raise NotImplementedError()
    
    @property
    def padding_right(self) -> float:
        '''Gets the padding right.'''
        raise NotImplementedError()
    
    @padding_right.setter
    def padding_right(self, value : float) -> None:
        '''Sets the padding right.'''
        raise NotImplementedError()
    
    @property
    def padding_bottom(self) -> float:
        '''Gets the padding bottom.'''
        raise NotImplementedError()
    
    @padding_bottom.setter
    def padding_bottom(self, value : float) -> None:
        '''Sets the padding bottom.'''
        raise NotImplementedError()
    
    @property
    def margin_bottom(self) -> float:
        '''Gets the margin bottom.'''
        raise NotImplementedError()
    
    @margin_bottom.setter
    def margin_bottom(self, value : float) -> None:
        '''Sets the margin bottom.'''
        raise NotImplementedError()
    
    @property
    def margin_top(self) -> float:
        '''Gets the margin top.'''
        raise NotImplementedError()
    
    @margin_top.setter
    def margin_top(self, value : float) -> None:
        '''Sets the margin top.'''
        raise NotImplementedError()
    
    @property
    def start_guide(self) -> float:
        '''Gets the start guide.'''
        raise NotImplementedError()
    
    @start_guide.setter
    def start_guide(self, value : float) -> None:
        '''Sets the start guide.'''
        raise NotImplementedError()
    
    @property
    def end_guide(self) -> float:
        '''Gets the end guide.'''
        raise NotImplementedError()
    
    @end_guide.setter
    def end_guide(self, value : float) -> None:
        '''Sets the end guide.'''
        raise NotImplementedError()
    
    @property
    def measure_line_distance(self) -> float:
        '''Gets the measure line distance.'''
        raise NotImplementedError()
    
    @measure_line_distance.setter
    def measure_line_distance(self, value : float) -> None:
        '''Sets the measure line distance.'''
        raise NotImplementedError()
    
    @property
    def style_position(self) -> float:
        '''Gets the style position.'''
        raise NotImplementedError()
    
    @style_position.setter
    def style_position(self, value : float) -> None:
        '''Sets the style position.'''
        raise NotImplementedError()
    

class OdMetadata(aspose.imaging.fileformats.opendocument.OdObject):
    '''The Metadata of open document'''
    
    def __init__(self, parent : aspose.imaging.fileformats.opendocument.OdObject) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.opendocument.objects.OdMetadata` class.
        
        :param parent: The parent.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.opendocument.OdObject:
        '''Gets the parent object.'''
        raise NotImplementedError()
    
    @property
    def items(self) -> List[aspose.imaging.fileformats.opendocument.OdObject]:
        '''Gets the items.'''
        raise NotImplementedError()
    
    @property
    def generator(self) -> str:
        '''Gets the generator.'''
        raise NotImplementedError()
    
    @generator.setter
    def generator(self, value : str) -> None:
        '''Sets the generator.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''Gets the title.'''
        raise NotImplementedError()
    
    @title.setter
    def title(self, value : str) -> None:
        '''Sets the title.'''
        raise NotImplementedError()
    
    @property
    def description(self) -> str:
        '''Gets the description.'''
        raise NotImplementedError()
    
    @description.setter
    def description(self, value : str) -> None:
        '''Sets the description.'''
        raise NotImplementedError()
    
    @property
    def subject(self) -> str:
        '''Gets the subject.'''
        raise NotImplementedError()
    
    @subject.setter
    def subject(self, value : str) -> None:
        '''Sets the subject.'''
        raise NotImplementedError()
    
    @property
    def keywords(self) -> str:
        '''Gets the keywords.'''
        raise NotImplementedError()
    
    @keywords.setter
    def keywords(self, value : str) -> None:
        '''Sets the keywords.'''
        raise NotImplementedError()
    
    @property
    def initial_creator(self) -> str:
        '''Gets the initial creator.'''
        raise NotImplementedError()
    
    @initial_creator.setter
    def initial_creator(self, value : str) -> None:
        '''Sets the initial creator.'''
        raise NotImplementedError()
    
    @property
    def creator(self) -> str:
        '''Gets the creator.'''
        raise NotImplementedError()
    
    @creator.setter
    def creator(self, value : str) -> None:
        '''Sets the creator.'''
        raise NotImplementedError()
    
    @property
    def printed_by(self) -> str:
        '''Gets the printed by.'''
        raise NotImplementedError()
    
    @printed_by.setter
    def printed_by(self, value : str) -> None:
        '''Sets the printed by.'''
        raise NotImplementedError()
    
    @property
    def creation_date_time(self) -> str:
        '''Gets the creation date time.'''
        raise NotImplementedError()
    
    @creation_date_time.setter
    def creation_date_time(self, value : str) -> None:
        '''Sets the creation date time.'''
        raise NotImplementedError()
    
    @property
    def modification_date_time(self) -> str:
        '''Gets the modification date time.'''
        raise NotImplementedError()
    
    @modification_date_time.setter
    def modification_date_time(self, value : str) -> None:
        '''Sets the modification date time.'''
        raise NotImplementedError()
    
    @property
    def print_date_time(self) -> str:
        '''Gets the print date time.'''
        raise NotImplementedError()
    
    @print_date_time.setter
    def print_date_time(self, value : str) -> None:
        '''Sets the print date time.'''
        raise NotImplementedError()
    
    @property
    def document_template(self) -> str:
        '''Gets the document template.'''
        raise NotImplementedError()
    
    @document_template.setter
    def document_template(self, value : str) -> None:
        '''Sets the document template.'''
        raise NotImplementedError()
    
    @property
    def automatic_reload(self) -> str:
        '''Gets the automatic reload.'''
        raise NotImplementedError()
    
    @automatic_reload.setter
    def automatic_reload(self, value : str) -> None:
        '''Sets the automatic reload.'''
        raise NotImplementedError()
    
    @property
    def hyperlink_behavior(self) -> str:
        '''Gets the hyperlink behavior.'''
        raise NotImplementedError()
    
    @hyperlink_behavior.setter
    def hyperlink_behavior(self, value : str) -> None:
        '''Sets the hyperlink behavior.'''
        raise NotImplementedError()
    
    @property
    def language(self) -> str:
        '''Gets the language.'''
        raise NotImplementedError()
    
    @language.setter
    def language(self, value : str) -> None:
        '''Sets the language.'''
        raise NotImplementedError()
    
    @property
    def editing_cycles(self) -> str:
        '''Gets the editing cycles.'''
        raise NotImplementedError()
    
    @editing_cycles.setter
    def editing_cycles(self, value : str) -> None:
        '''Sets the editing cycles.'''
        raise NotImplementedError()
    
    @property
    def editing_duration(self) -> str:
        '''Gets the duration of the editing.'''
        raise NotImplementedError()
    
    @editing_duration.setter
    def editing_duration(self, value : str) -> None:
        '''Sets the duration of the editing.'''
        raise NotImplementedError()
    
    @property
    def document_statistics(self) -> str:
        '''Gets the document statistics.'''
        raise NotImplementedError()
    
    @document_statistics.setter
    def document_statistics(self, value : str) -> None:
        '''Sets the document statistics.'''
        raise NotImplementedError()
    

class OdTransformInfo:
    '''The open document translate info'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def copy(self) -> aspose.imaging.fileformats.opendocument.objects.OdTransformInfo:
        '''Copies this instance.
        
        :returns: Get the instance of OdTransformInfo'''
        raise NotImplementedError()
    
    @property
    def rotate_angle(self) -> float:
        '''Gets the rotate angle.'''
        raise NotImplementedError()
    
    @rotate_angle.setter
    def rotate_angle(self, value : float) -> None:
        '''Sets the rotate angle.'''
        raise NotImplementedError()
    
    @property
    def translate_x(self) -> float:
        '''Gets the translate x.'''
        raise NotImplementedError()
    
    @translate_x.setter
    def translate_x(self, value : float) -> None:
        '''Sets the translate x.'''
        raise NotImplementedError()
    
    @property
    def translate_y(self) -> float:
        '''Gets the translate y.'''
        raise NotImplementedError()
    
    @translate_y.setter
    def translate_y(self, value : float) -> None:
        '''Sets the translate y.'''
        raise NotImplementedError()
    
    @property
    def skew_x(self) -> float:
        '''Gets the skew x.'''
        raise NotImplementedError()
    
    @skew_x.setter
    def skew_x(self, value : float) -> None:
        '''Sets the skew x.'''
        raise NotImplementedError()
    
    @property
    def skew_y(self) -> float:
        '''Gets the skew y.'''
        raise NotImplementedError()
    
    @skew_y.setter
    def skew_y(self, value : float) -> None:
        '''Sets the skew y.'''
        raise NotImplementedError()
    

