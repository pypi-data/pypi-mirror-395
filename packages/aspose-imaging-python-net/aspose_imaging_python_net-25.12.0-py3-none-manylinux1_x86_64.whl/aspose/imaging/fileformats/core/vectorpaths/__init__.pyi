"""The namespace contains PSD Vector Paths."""
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

class BezierKnotRecord(VectorPathRecord):
    '''Bezier Knot Record Class'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.BezierKnotRecord` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.BezierKnotRecord` class.
        
        :param data: The record data.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        raise NotImplementedError()
    
    @property
    def path_points(self) -> List[aspose.imaging.PointF]:
        '''Gets the path points.'''
        raise NotImplementedError()
    
    @path_points.setter
    def path_points(self, value : List[aspose.imaging.PointF]) -> None:
        '''Sets the path points.'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.Point]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.Point]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    
    @property
    def is_closed(self) -> bool:
        '''Gets a value indicating whether this instance is closed.'''
        raise NotImplementedError()
    
    @is_closed.setter
    def is_closed(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is closed.'''
        raise NotImplementedError()
    
    @property
    def is_linked(self) -> bool:
        '''Gets a value indicating whether this instance is linked.'''
        raise NotImplementedError()
    
    @is_linked.setter
    def is_linked(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is linked.'''
        raise NotImplementedError()
    
    @property
    def is_open(self) -> bool:
        '''Gets a value indicating whether this instance is open.'''
        raise NotImplementedError()
    
    @is_open.setter
    def is_open(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is open.'''
        raise NotImplementedError()
    

class ClipboardRecord(VectorPathRecord):
    '''Clipboard Record Class'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.ClipboardRecord` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.ClipboardRecord` class.
        
        :param data: The record data.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        raise NotImplementedError()
    
    @property
    def bounding_rect(self) -> aspose.imaging.RectangleF:
        '''Gets the bounding rect.'''
        raise NotImplementedError()
    
    @bounding_rect.setter
    def bounding_rect(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounding rect.'''
        raise NotImplementedError()
    
    @property
    def resolution(self) -> float:
        '''Gets the resolution.'''
        raise NotImplementedError()
    
    @resolution.setter
    def resolution(self, value : float) -> None:
        '''Sets the resolution.'''
        raise NotImplementedError()
    

class IVectorPathData:
    '''The interface for access to the vector path data.'''
    
    @property
    def paths(self) -> List[aspose.imaging.fileformats.core.vectorpaths.VectorPathRecord]:
        '''Gets the path records.'''
        raise NotImplementedError()
    
    @paths.setter
    def paths(self, value : List[aspose.imaging.fileformats.core.vectorpaths.VectorPathRecord]) -> None:
        '''Sets the path records.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    
    @property
    def is_disabled(self) -> bool:
        '''Gets a value indicating whether this instance is disabled.'''
        raise NotImplementedError()
    
    @is_disabled.setter
    def is_disabled(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is disabled.'''
        raise NotImplementedError()
    
    @property
    def is_not_linked(self) -> bool:
        '''Gets a value indicating whether this instance is not linked.'''
        raise NotImplementedError()
    
    @is_not_linked.setter
    def is_not_linked(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is not linked.'''
        raise NotImplementedError()
    
    @property
    def is_inverted(self) -> bool:
        '''Gets a value indicating whether this instance is inverted.'''
        raise NotImplementedError()
    
    @is_inverted.setter
    def is_inverted(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is inverted.'''
        raise NotImplementedError()
    

class InitialFillRuleRecord(VectorPathRecord):
    '''Initial Fill Rule Record Class'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.InitialFillRuleRecord` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, is_fill_starts_with_all_pixels : bool) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.InitialFillRuleRecord` class.
        
        :param is_fill_starts_with_all_pixels: The is fill starts with all pixels.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.InitialFillRuleRecord` class.
        
        :param data: The record data.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_filled_with_pixels(is_fill_starts_with_all_pixels : bool) -> aspose.imaging.fileformats.core.vectorpaths.InitialFillRuleRecord:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.InitialFillRuleRecord` class.
        
        :param is_fill_starts_with_all_pixels: The is fill starts with all pixels.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_from_bytes(data : List[int]) -> aspose.imaging.fileformats.core.vectorpaths.InitialFillRuleRecord:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.InitialFillRuleRecord` class.
        
        :param data: The record data.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        raise NotImplementedError()
    
    @property
    def is_fill_starts_with_all_pixels(self) -> bool:
        '''Gets a value indicating whether is fill starts with all pixels.'''
        raise NotImplementedError()
    
    @is_fill_starts_with_all_pixels.setter
    def is_fill_starts_with_all_pixels(self, value : bool) -> None:
        '''Sets a value indicating whether is fill starts with all pixels.'''
        raise NotImplementedError()
    

class LengthRecord(VectorPathRecord):
    '''Subpath Length Record Class'''
    
    @overload
    def __init__(self, data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.LengthRecord` class.
        
        :param data: The record data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.LengthRecord` class.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        raise NotImplementedError()
    
    @property
    def is_closed(self) -> bool:
        '''Gets a value indicating whether this instance is closed.'''
        raise NotImplementedError()
    
    @is_closed.setter
    def is_closed(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is closed.'''
        raise NotImplementedError()
    
    @property
    def is_open(self) -> bool:
        '''Gets a value indicating whether this instance is open.'''
        raise NotImplementedError()
    
    @is_open.setter
    def is_open(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is open.'''
        raise NotImplementedError()
    
    @property
    def record_count(self) -> int:
        '''Gets the record count.'''
        raise NotImplementedError()
    
    @record_count.setter
    def record_count(self, value : int) -> None:
        '''Sets the record count.'''
        raise NotImplementedError()
    
    @property
    def bezier_knot_records_count(self) -> int:
        '''Gets the bezier knot records count.'''
        raise NotImplementedError()
    
    @bezier_knot_records_count.setter
    def bezier_knot_records_count(self, value : int) -> None:
        '''Sets the bezier knot records count.'''
        raise NotImplementedError()
    
    @property
    def path_operations(self) -> aspose.imaging.fileformats.core.vectorpaths.PathOperations:
        '''Gets the path operations.'''
        raise NotImplementedError()
    
    @path_operations.setter
    def path_operations(self, value : aspose.imaging.fileformats.core.vectorpaths.PathOperations) -> None:
        '''Sets the path operations.'''
        raise NotImplementedError()
    
    @property
    def shape_index(self) -> int:
        '''Gets the index of current path shape in layer.'''
        raise NotImplementedError()
    
    @shape_index.setter
    def shape_index(self, value : int) -> None:
        '''Sets the index of current path shape in layer.'''
        raise NotImplementedError()
    

class PathFillRuleRecord(VectorPathRecord):
    '''Path Fill Rule Record Class'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.PathFillRuleRecord` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.core.vectorpaths.PathFillRuleRecord` class.
        
        :param data: The record data.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        raise NotImplementedError()
    

class VectorPathRecord:
    '''Vector Path Record Class'''
    
    @property
    def type(self) -> aspose.imaging.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        raise NotImplementedError()
    

class VectorPathRecordFactory:
    '''Vector Path Record Factory Class'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def produce_path_record(self, data : List[int]) -> aspose.imaging.fileformats.core.vectorpaths.VectorPathRecord:
        '''Produces the path record.
        
        :param data: The record data.
        :returns: Created :py:class:`aspose.imaging.fileformats.core.vectorpaths.VectorPathRecord`'''
        raise NotImplementedError()
    

class PathOperations(enum.Enum):
    EXCLUDE_OVERLAPPING_SHAPES = enum.auto()
    '''Exclude Overlapping Shapes (XOR operation).'''
    COMBINE_SHAPES = enum.auto()
    '''Combine Shapes (OR operation). This is default value in Photoshop.'''
    SUBTRACT_FRONT_SHAPE = enum.auto()
    '''Subtract Front Shape (NOT operation).'''
    INTERSECT_SHAPE_AREAS = enum.auto()
    '''Intersect Shape Areas (AND operation).'''

class VectorPathType(enum.Enum):
    CLOSED_SUBPATH_LENGTH_RECORD = enum.auto()
    '''The closed subpath length record'''
    CLOSED_SUBPATH_BEZIER_KNOT_LINKED = enum.auto()
    '''The closed subpath bezier knot linked'''
    CLOSED_SUBPATH_BEZIER_KNOT_UNLINKED = enum.auto()
    '''The closed subpath bezier knot unlinked'''
    OPEN_SUBPATH_LENGTH_RECORD = enum.auto()
    '''The open subpath length record'''
    OPEN_SUBPATH_BEZIER_KNOT_LINKED = enum.auto()
    '''The open subpath bezier knot linked'''
    OPEN_SUBPATH_BEZIER_KNOT_UNLINKED = enum.auto()
    '''The open subpath bezier knot unlinked'''
    PATH_FILL_RULE_RECORD = enum.auto()
    '''The path fill rule record'''
    CLIPBOARD_RECORD = enum.auto()
    '''The clipboard record'''
    INITIAL_FILL_RULE_RECORD = enum.auto()
    '''The initial fill rule record'''

