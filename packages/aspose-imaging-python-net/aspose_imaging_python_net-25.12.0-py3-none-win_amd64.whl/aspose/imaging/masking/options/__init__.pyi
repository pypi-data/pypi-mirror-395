"""The namespace handles ImageMasking.Options processing."""
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

class AssumedObjectData:
    '''The assumed object\'s data. Includes object\'s type and area.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.masking.options.AssumedObjectData` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, type : aspose.imaging.masking.options.DetectedObjectType, bounds : aspose.imaging.Rectangle) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.masking.options.AssumedObjectData` class.
        
        :param type: The object\'s type.
        :param bounds: The object\'s bounds.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, type : str, bounds : aspose.imaging.Rectangle) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.masking.options.AssumedObjectData` class.
        
        :param type: The object\'s type.
        :param bounds: The object\'s bounds.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.masking.options.DetectedObjectType:
        '''Gets the object\'s type.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.masking.options.DetectedObjectType) -> None:
        '''Sets the object\'s type.'''
        raise NotImplementedError()
    
    @property
    def bounds(self) -> aspose.imaging.Rectangle:
        '''Gets the object\'s bounds.'''
        raise NotImplementedError()
    
    @bounds.setter
    def bounds(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the object\'s bounds.'''
        raise NotImplementedError()
    

class AutoMaskingArgs(IMaskingArgs):
    '''Represents the arguments that are specified for automated masking methods'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def number_of_objects(self) -> int:
        '''Gets the number of objects
        to separate initial image to (optional), default value is 2 (object and background).'''
        raise NotImplementedError()
    
    @number_of_objects.setter
    def number_of_objects(self, value : int) -> None:
        '''Sets the number of objects
        to separate initial image to (optional), default value is 2 (object and background).'''
        raise NotImplementedError()
    
    @property
    def objects_rectangles(self) -> List[aspose.imaging.Rectangle]:
        '''Gets the objects rectangles that belong to separated objects (optional).
        This parameter is used to increase segmentation method precision.'''
        raise NotImplementedError()
    
    @objects_rectangles.setter
    def objects_rectangles(self, value : List[aspose.imaging.Rectangle]) -> None:
        '''Sets the objects rectangles that belong to separated objects (optional).
        This parameter is used to increase segmentation method precision.'''
        raise NotImplementedError()
    
    @property
    def objects_points(self) -> List[List[aspose.imaging.Point]]:
        '''Gets the points that belong to separated objects (optional)
        NumberOfObjects coordinates that belong to NumberOfObjects objects of initial image.
        This parameter is used to increase segmentation method precision.'''
        raise NotImplementedError()
    
    @objects_points.setter
    def objects_points(self, value : List[List[aspose.imaging.Point]]) -> None:
        '''Sets the points that belong to separated objects (optional)
        NumberOfObjects coordinates that belong to NumberOfObjects objects of initial image.
        This parameter is used to increase segmentation method precision.'''
        raise NotImplementedError()
    
    @property
    def orphaned_points(self) -> List[aspose.imaging.Point]:
        '''Gets the points that no longer belong to any object (optional).
        This parameter is used only in case of re-segmentation.'''
        raise NotImplementedError()
    
    @orphaned_points.setter
    def orphaned_points(self, value : List[aspose.imaging.Point]) -> None:
        '''Sets the points that no longer belong to any object (optional).
        This parameter is used only in case of re-segmentation.'''
        raise NotImplementedError()
    
    @property
    def precision(self) -> float:
        '''Gets the precision of segmentation method (optional).'''
        raise NotImplementedError()
    
    @precision.setter
    def precision(self, value : float) -> None:
        '''Sets the precision of segmentation method (optional).'''
        raise NotImplementedError()
    
    @property
    def max_iteration_number(self) -> int:
        '''Gets the maximum number of iterations.'''
        raise NotImplementedError()
    
    @max_iteration_number.setter
    def max_iteration_number(self, value : int) -> None:
        '''Sets the maximum number of iterations.'''
        raise NotImplementedError()
    

class AutoMaskingGraphCutOptions(GraphCutMaskingOptions):
    '''The GraphCut auto masking options.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.masking.options.AutoMaskingGraphCutOptions` class.'''
        raise NotImplementedError()
    
    @property
    def method(self) -> aspose.imaging.masking.options.SegmentationMethod:
        '''Gets the segmentation method.'''
        raise NotImplementedError()
    
    @method.setter
    def method(self, value : aspose.imaging.masking.options.SegmentationMethod) -> None:
        '''Sets the segmentation method.'''
        raise NotImplementedError()
    
    @property
    def args(self) -> aspose.imaging.masking.options.IMaskingArgs:
        '''Gets the arguments for segmentation algorithm.'''
        raise NotImplementedError()
    
    @args.setter
    def args(self, value : aspose.imaging.masking.options.IMaskingArgs) -> None:
        '''Sets the arguments for segmentation algorithm.'''
        raise NotImplementedError()
    
    @property
    def export_options(self) -> aspose.imaging.ImageOptionsBase:
        '''Gets the image export options.'''
        raise NotImplementedError()
    
    @export_options.setter
    def export_options(self, value : aspose.imaging.ImageOptionsBase) -> None:
        '''Sets the image export options.'''
        raise NotImplementedError()
    
    @property
    def masking_area(self) -> aspose.imaging.Rectangle:
        '''Gets the masking area.'''
        raise NotImplementedError()
    
    @masking_area.setter
    def masking_area(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the masking area.'''
        raise NotImplementedError()
    
    @property
    def decompose(self) -> bool:
        '''Gets a value indicating whether
        needless to separate each Shape from mask as individual object or as united object from mask separated from background.'''
        raise NotImplementedError()
    
    @decompose.setter
    def decompose(self, value : bool) -> None:
        '''Sets a value indicating whether
        needless to separate each Shape from mask as individual object or as united object from mask separated from background.'''
        raise NotImplementedError()
    
    @property
    def background_replacement_color(self) -> aspose.imaging.Color:
        '''Gets the background replacement color.'''
        raise NotImplementedError()
    
    @background_replacement_color.setter
    def background_replacement_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the background replacement color.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def BACKGROUND_OBJECT_NUMBER() -> int:
        '''The background object number'''
        raise NotImplementedError()

    @property
    def feathering_radius(self) -> int:
        '''Gets the feathering radius.'''
        raise NotImplementedError()
    
    @feathering_radius.setter
    def feathering_radius(self, value : int) -> None:
        '''Sets the feathering radius.'''
        raise NotImplementedError()
    
    @property
    def default_foreground_strokes(self) -> List[aspose.imaging.Point]:
        '''Gets the pre-calculated default foreground strokes.'''
        raise NotImplementedError()
    
    @property
    def default_background_strokes(self) -> List[aspose.imaging.Point]:
        '''Gets the default background strokes.'''
        raise NotImplementedError()
    
    @property
    def default_objects_rectangles(self) -> List[aspose.imaging.Rectangle]:
        '''Gets the default objects rectangles.'''
        raise NotImplementedError()
    
    @property
    def assumed_objects(self) -> List[aspose.imaging.masking.options.AssumedObjectData]:
        '''Gets the assumed objects.'''
        raise NotImplementedError()
    
    @assumed_objects.setter
    def assumed_objects(self, value : List[aspose.imaging.masking.options.AssumedObjectData]) -> None:
        '''Sets the assumed objects.'''
        raise NotImplementedError()
    
    @property
    def calculate_default_strokes(self) -> bool:
        '''Gets a value indicating whether default strokes should be calculated.'''
        raise NotImplementedError()
    
    @calculate_default_strokes.setter
    def calculate_default_strokes(self, value : bool) -> None:
        '''Sets a value indicating whether default strokes should be calculated.'''
        raise NotImplementedError()
    

class GraphCutMaskingOptions(MaskingOptions):
    '''The GraphCut auto masking options.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def method(self) -> aspose.imaging.masking.options.SegmentationMethod:
        '''Gets the segmentation method.'''
        raise NotImplementedError()
    
    @method.setter
    def method(self, value : aspose.imaging.masking.options.SegmentationMethod) -> None:
        '''Sets the segmentation method.'''
        raise NotImplementedError()
    
    @property
    def args(self) -> aspose.imaging.masking.options.IMaskingArgs:
        '''Gets the arguments for segmentation algorithm.'''
        raise NotImplementedError()
    
    @args.setter
    def args(self, value : aspose.imaging.masking.options.IMaskingArgs) -> None:
        '''Sets the arguments for segmentation algorithm.'''
        raise NotImplementedError()
    
    @property
    def export_options(self) -> aspose.imaging.ImageOptionsBase:
        '''Gets the image export options.'''
        raise NotImplementedError()
    
    @export_options.setter
    def export_options(self, value : aspose.imaging.ImageOptionsBase) -> None:
        '''Sets the image export options.'''
        raise NotImplementedError()
    
    @property
    def masking_area(self) -> aspose.imaging.Rectangle:
        '''Gets the masking area.'''
        raise NotImplementedError()
    
    @masking_area.setter
    def masking_area(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the masking area.'''
        raise NotImplementedError()
    
    @property
    def decompose(self) -> bool:
        '''Gets a value indicating whether
        needless to separate each Shape from mask as individual object or as united object from mask separated from background.'''
        raise NotImplementedError()
    
    @decompose.setter
    def decompose(self, value : bool) -> None:
        '''Sets a value indicating whether
        needless to separate each Shape from mask as individual object or as united object from mask separated from background.'''
        raise NotImplementedError()
    
    @property
    def background_replacement_color(self) -> aspose.imaging.Color:
        '''Gets the background replacement color.'''
        raise NotImplementedError()
    
    @background_replacement_color.setter
    def background_replacement_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the background replacement color.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def BACKGROUND_OBJECT_NUMBER() -> int:
        '''The background object number'''
        raise NotImplementedError()

    @property
    def feathering_radius(self) -> int:
        '''Gets the feathering radius.'''
        raise NotImplementedError()
    
    @feathering_radius.setter
    def feathering_radius(self, value : int) -> None:
        '''Sets the feathering radius.'''
        raise NotImplementedError()
    

class IMaskingArgs:
    '''The masking arguments'''
    

class ManualMaskingArgs(IMaskingArgs):
    '''Represents the arguments that are specified for manual masking method'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def mask(self) -> aspose.imaging.GraphicsPath:
        '''Gets the set of graphic shapes that form mask.'''
        raise NotImplementedError()
    
    @mask.setter
    def mask(self, value : aspose.imaging.GraphicsPath) -> None:
        '''Sets the set of graphic shapes that form mask.'''
        raise NotImplementedError()
    

class MaskingOptions:
    '''Represents the common image masking options.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def method(self) -> aspose.imaging.masking.options.SegmentationMethod:
        '''Gets the segmentation method.'''
        raise NotImplementedError()
    
    @method.setter
    def method(self, value : aspose.imaging.masking.options.SegmentationMethod) -> None:
        '''Sets the segmentation method.'''
        raise NotImplementedError()
    
    @property
    def args(self) -> aspose.imaging.masking.options.IMaskingArgs:
        '''Gets the arguments for segmentation algorithm.'''
        raise NotImplementedError()
    
    @args.setter
    def args(self, value : aspose.imaging.masking.options.IMaskingArgs) -> None:
        '''Sets the arguments for segmentation algorithm.'''
        raise NotImplementedError()
    
    @property
    def export_options(self) -> aspose.imaging.ImageOptionsBase:
        '''Gets the image export options.'''
        raise NotImplementedError()
    
    @export_options.setter
    def export_options(self, value : aspose.imaging.ImageOptionsBase) -> None:
        '''Sets the image export options.'''
        raise NotImplementedError()
    
    @property
    def masking_area(self) -> aspose.imaging.Rectangle:
        '''Gets the masking area.'''
        raise NotImplementedError()
    
    @masking_area.setter
    def masking_area(self, value : aspose.imaging.Rectangle) -> None:
        '''Sets the masking area.'''
        raise NotImplementedError()
    
    @property
    def decompose(self) -> bool:
        '''Gets a value indicating whether
        needless to separate each Shape from mask as individual object or as united object from mask separated from background.'''
        raise NotImplementedError()
    
    @decompose.setter
    def decompose(self, value : bool) -> None:
        '''Sets a value indicating whether
        needless to separate each Shape from mask as individual object or as united object from mask separated from background.'''
        raise NotImplementedError()
    
    @property
    def background_replacement_color(self) -> aspose.imaging.Color:
        '''Gets the background replacement color.'''
        raise NotImplementedError()
    
    @background_replacement_color.setter
    def background_replacement_color(self, value : aspose.imaging.Color) -> None:
        '''Sets the background replacement color.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def BACKGROUND_OBJECT_NUMBER() -> int:
        '''The background object number'''
        raise NotImplementedError()


class DetectedObjectType(enum.Enum):
    HUMAN = enum.auto()
    '''The human object type.'''
    OTHER = enum.auto()
    '''Other object type.'''

class SegmentationMethod(enum.Enum):
    MANUAL = enum.auto()
    '''The manual segmentation algorithm'''
    K_MEANS = enum.auto()
    '''The K-means segmentation algorithm.'''
    FUZZY_C_MEANS = enum.auto()
    '''The Fuzzy C-means segmentation algorithm.'''
    WATERSHED = enum.auto()
    '''The Watershed segmentation algorithm.'''
    GRAPH_CUT = enum.auto()
    '''The Graph Cut segmentation algorithm'''

