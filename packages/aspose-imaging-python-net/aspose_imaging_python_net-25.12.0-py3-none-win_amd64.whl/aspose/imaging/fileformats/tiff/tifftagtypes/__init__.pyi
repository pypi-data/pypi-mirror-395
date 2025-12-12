"""The namespace contains Tiff file format tag classes."""
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

class TiffASCIIType(aspose.imaging.fileformats.tiff.TiffDataType):
    '''The tiff ascii type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffASCIIType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffASCIIType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffASCIIType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffASCIIType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffASCIIType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffASCIIType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the text.'''
        raise NotImplementedError()
    
    @text.setter
    def text(self, value : str) -> None:
        '''Sets the text.'''
        raise NotImplementedError()
    

class TiffByteType(TiffCommonArrayType):
    '''The tiff byte type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffByteType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffByteType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffByteType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffByteType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffByteType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffByteType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffCommonArrayType(aspose.imaging.fileformats.tiff.TiffDataType):
    '''The tiff common array type.'''
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    

class TiffDoubleType(TiffCommonArrayType):
    '''The tiff double type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffDoubleType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffDoubleType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffDoubleType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffDoubleType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffDoubleType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffDoubleType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[float]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[float]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffFloatType(TiffCommonArrayType):
    '''The tiff float type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffFloatType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffFloatType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffFloatType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffFloatType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffFloatType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffFloatType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[float]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[float]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffIfd8Type(TiffLong8Type):
    '''The Tiff unsigned 64-bit Image File Directory type.'''
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfd8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfd8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfd8Type:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfd8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfd8Type:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfd8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets size of element.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffIfdType(TiffCommonArrayType):
    '''Represents the TIFF Exif image file directory type class.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfdType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfdType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfdType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfdType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfdType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffIfdType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffLong8Type(TiffCommonArrayType):
    '''The Tiff unsigned 64-bit type.'''
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffLong8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffLong8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffLong8Type:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffLong8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffLong8Type:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffLong8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets size of element.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffLongType(TiffCommonArrayType):
    '''The tiff long type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffLongType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffLongType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffLongType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffLongType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffLongType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffLongType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffRationalType(TiffCommonArrayType):
    '''The tiff rational type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffRationalType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffRationalType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffRationalType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffRationalType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffRationalType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffRationalType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[aspose.imaging.fileformats.tiff.TiffRational]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[aspose.imaging.fileformats.tiff.TiffRational]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffSByteType(TiffCommonArrayType):
    '''The tiff signed byte type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSByteType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSByteType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSByteType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSByteType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSByteType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSByteType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffSLong8Type(TiffCommonArrayType):
    '''The Tiff unsigned 64-bit type.'''
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLong8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLong8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLong8Type:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLong8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLong8Type:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLong8Type` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets size of element.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffSLongType(TiffCommonArrayType):
    '''The tiff signed long type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLongType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLongType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLongType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLongType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLongType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSLongType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffSRationalType(TiffCommonArrayType):
    '''The tiff signed rational type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSRationalType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSRationalType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSRationalType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSRationalType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSRationalType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSRationalType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[aspose.imaging.fileformats.tiff.TiffSRational]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[aspose.imaging.fileformats.tiff.TiffSRational]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffSShortType(TiffCommonArrayType):
    '''The tiff signed short type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSShortType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSShortType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSShortType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSShortType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffSShortType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffSShortType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the values.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the values.'''
        raise NotImplementedError()
    

class TiffShortType(TiffCommonArrayType):
    '''The tiff short type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffShortType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffShortType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffShortType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffShortType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffShortType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffShortType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def values_container(self) -> List[Any]:
        '''Gets the values container.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[int]:
        '''Gets the data.'''
        raise NotImplementedError()
    
    @values.setter
    def values(self, value : List[int]) -> None:
        '''Sets the data.'''
        raise NotImplementedError()
    

class TiffUndefinedType(aspose.imaging.fileformats.tiff.TiffDataType):
    '''The tiff undefined type.'''
    
    @overload
    def __init__(self, tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffUndefinedType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, tag_id : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffUndefinedType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag(tag_id : aspose.imaging.fileformats.tiff.enums.TiffTags) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffUndefinedType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffUndefinedType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @staticmethod
    def create_with_tag_id(tag_id : int) -> aspose.imaging.fileformats.tiff.tifftagtypes.TiffUndefinedType:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffUndefinedType` class.
        
        :param tag_id: The tag id.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the data.'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : List[int]) -> None:
        '''Sets the data.'''
        raise NotImplementedError()
    

class TiffUnknownType(aspose.imaging.fileformats.tiff.TiffDataType):
    '''The unknown tiff type. In case the tiff tag cannot be recognized this type is instantinated.'''
    
    def __init__(self, stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, tag_type : int, tag_id : int, count : int, offset_or_value : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.tifftagtypes.TiffUnknownType` class.
        
        :param stream: The stream to read from.
        :param tag_type: Type of the tag.
        :param tag_id: The tag id.
        :param count: The count value.
        :param offset_or_value: The offset or value.'''
        raise NotImplementedError()
    
    @staticmethod
    def read_tag(data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader, position : int) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        raise NotImplementedError()
    
    def compare_to(self, obj : Any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        raise NotImplementedError()
    
    def get_aligned_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the data size aligned in 4-byte (int) or 8-byte (long) boundary.
        
        :param size_of_tag_value: Size of tag value.
        :returns: The aligned data size in bytes.'''
        raise NotImplementedError()
    
    def get_additional_data_size(self, size_of_tag_value : int) -> int:
        '''Gets the additional tag value size in bytes (in case the tag can not fit the whole tag value).
        
        :param size_of_tag_value: Size of tag value: 4 or 8 for BigTiff.
        :returns: The additional data size in bytes.'''
        raise NotImplementedError()
    
    def deep_clone(self) -> aspose.imaging.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        raise NotImplementedError()
    
    def write_tag(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int) -> None:
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        raise NotImplementedError()
    
    def write_additional_data(self, data_stream : aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        raise NotImplementedError()
    
    @property
    def element_size(self) -> int:
        '''Gets the element size in bytes.'''
        raise NotImplementedError()
    
    @property
    def data_size(self) -> int:
        '''Gets the tag value size.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets tag id as number.'''
        raise NotImplementedError()
    
    @property
    def tag_id(self) -> aspose.imaging.fileformats.tiff.enums.TiffTags:
        '''Gets the tag id.'''
        raise NotImplementedError()
    
    @property
    def tag_type(self) -> aspose.imaging.fileformats.tiff.enums.TiffDataTypes:
        '''Gets the tag type.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> Any:
        '''Gets the value this data type contains.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : Any) -> None:
        '''Sets the value this data type contains.'''
        raise NotImplementedError()
    
    @property
    def is_valid(self) -> bool:
        '''Gets a value indicating whether tag data is valid. The valid tag contains data which may be preserved. The invalid tag cannot be stored.'''
        raise NotImplementedError()
    
    @property
    def offset_or_value(self) -> int:
        '''Gets the offset value for an additional data or value itself in case count is 1.'''
        raise NotImplementedError()
    
    @property
    def stream(self) -> aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader:
        '''Gets the stream to read additional data from.'''
        raise NotImplementedError()
    

