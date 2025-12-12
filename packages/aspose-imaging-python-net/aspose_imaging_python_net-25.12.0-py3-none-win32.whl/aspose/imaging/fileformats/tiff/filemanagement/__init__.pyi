"""The namespace contains Tiff file format stream handling classes."""
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

class TiffBigEndianStreamReader(TiffStreamReader):
    '''The tiff stream for handling big endian tiff file format.'''
    
    @overload
    def __init__(self, data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffBigEndianStreamReader` class.
        
        :param data: The byte array data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data : List[int], start_index : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffBigEndianStreamReader` class.
        
        :param data: The byte array data.
        :param start_index: The start index into ``data``.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data : List[int], start_index : int, data_length : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffBigEndianStreamReader` class.
        
        :param data: The byte array data.
        :param start_index: The start index into ``data``.
        :param data_length: Length of the data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, stream_container : aspose.imaging.StreamContainer) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffBigEndianStreamReader` class.
        
        :param stream_container: The stream container.'''
        raise NotImplementedError()
    
    @overload
    def read_bytes(self, array : List[int], array_index : int, position : int, count : int) -> int:
        '''Reads an array of byte values from the stream.
        
        :param array: The array to fill.
        :param array_index: The array index to start putting values to.
        :param position: The stream position to read from.
        :param count: The elements count to read.
        :returns: The array of byte values.'''
        raise NotImplementedError()
    
    @overload
    def read_bytes(self, position : int, count : int) -> List[int]:
        '''Reads an array of unsigned byte values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of unsigned byte values.'''
        raise NotImplementedError()
    
    def read_double(self, position : int) -> float:
        '''Read a single double value from the stream.
        
        :param position: The position to read from.
        :returns: The single double value.'''
        raise NotImplementedError()
    
    def read_double_array(self, position : int, count : int) -> List[float]:
        '''Reads an array of double values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of double values.'''
        raise NotImplementedError()
    
    def read_float(self, position : int) -> float:
        '''Read a single float value from the stream.
        
        :param position: The position to read from.
        :returns: The single float value.'''
        raise NotImplementedError()
    
    def read_float_array(self, position : int, count : int) -> List[float]:
        '''Reads an array of float values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of float values.'''
        raise NotImplementedError()
    
    def read_rational(self, position : int) -> aspose.imaging.fileformats.tiff.TiffRational:
        '''Read a single rational number value from the stream.
        
        :param position: The position to read from.
        :returns: The rational number.'''
        raise NotImplementedError()
    
    def read_s_rational(self, position : int) -> aspose.imaging.fileformats.tiff.TiffSRational:
        '''Read a single signed rational number value from the stream.
        
        :param position: The position to read from.
        :returns: The signed rational number.'''
        raise NotImplementedError()
    
    def read_rational_array(self, position : int, count : int) -> List[aspose.imaging.fileformats.tiff.TiffRational]:
        '''Reads an array of rational values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of rational values.'''
        raise NotImplementedError()
    
    def read_s_rational_array(self, position : int, count : int) -> List[aspose.imaging.fileformats.tiff.TiffSRational]:
        '''Reads an array of signed rational values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed rational values.'''
        raise NotImplementedError()
    
    def read_s_byte(self, position : int) -> int:
        '''Reads signed byte data from the stream.
        
        :param position: The position to read from.
        :returns: The signed byte value.'''
        raise NotImplementedError()
    
    def read_s_byte_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of signed byte values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed byte values.'''
        raise NotImplementedError()
    
    def read_s_int(self, position : int) -> int:
        '''Read signed integer value from the stream.
        
        :param position: The position to read from.
        :returns: A signed integer value.'''
        raise NotImplementedError()
    
    def read_s_int_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of signed integer values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed integer values.'''
        raise NotImplementedError()
    
    def read_s_short(self, position : int) -> int:
        '''Read signed short value from the stream.
        
        :param position: The position to read from.
        :returns: A signed short value.'''
        raise NotImplementedError()
    
    def read_s_short_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of signed short values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed short values.'''
        raise NotImplementedError()
    
    def read_u_int(self, position : int) -> int:
        '''Read unsigned integer value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned integer value.'''
        raise NotImplementedError()
    
    def read_u_int_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of unsigned integer values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of unsigned integer values.'''
        raise NotImplementedError()
    
    def read_u_short(self, position : int) -> int:
        '''Read unsigned short value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned short value.'''
        raise NotImplementedError()
    
    def read_u_short_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of unsigned integer values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of unsigned integer values.'''
        raise NotImplementedError()
    
    def read_long(self, position : int) -> int:
        '''Read unsigned long value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned short value.'''
        raise NotImplementedError()
    
    def read_long_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of ulong values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The ulong array.'''
        raise NotImplementedError()
    
    def read_u_long(self, position : int) -> int:
        '''Read unsigned long value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned short value.'''
        raise NotImplementedError()
    
    def read_u_long_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of ulong values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The ulong array.'''
        raise NotImplementedError()
    
    def to_stream_container(self, start_position : int) -> aspose.imaging.StreamContainer:
        '''Converts the underlying data to the stream container.
        
        :param start_position: The start position to start conversion from.
        :returns: The :py:class:`aspose.imaging.StreamContainer` with converted data.'''
        raise NotImplementedError()
    
    @property
    def length(self) -> int:
        '''Gets the reader length.'''
        raise NotImplementedError()
    
    @property
    def throw_exceptions(self) -> bool:
        '''Gets a value indicating whether exceptions are thrown on incorrect data processing (reading or writing to stream).'''
        raise NotImplementedError()
    
    @throw_exceptions.setter
    def throw_exceptions(self, value : bool) -> None:
        '''Sets a value indicating whether exceptions are thrown on incorrect data processing (reading or writing to stream).'''
        raise NotImplementedError()
    

class TiffBigEndianStreamWriter(TiffStreamWriter):
    '''Tiff stream writer for big-endian streams.'''
    
    def __init__(self, writer : aspose.imaging.StreamContainer) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffBigEndianStreamWriter` class.
        
        :param writer: The stream writer.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int], offset : int, data_length : int) -> None:
        '''Writes the specified data.
        
        :param data: The data to write.
        :param offset: The data offset.
        :param data_length: Length of the data to writer.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes the specified data.
        
        :param data: The data to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : float) -> None:
        '''Writes a single double value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[float]) -> None:
        '''Writes an array of double values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : float) -> None:
        '''Writes a single float value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[float]) -> None:
        '''Writes an array of float values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : aspose.imaging.fileformats.tiff.TiffRational) -> None:
        '''Writes a single rational number value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : aspose.imaging.fileformats.tiff.TiffSRational) -> None:
        '''Writes a single signed rational number value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[aspose.imaging.fileformats.tiff.TiffRational]) -> None:
        '''Writes an array of unsigned rational values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[aspose.imaging.fileformats.tiff.TiffSRational]) -> None:
        '''Writes an array of signed rational values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single signed byte value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of signed byte values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of integer values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single short value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of short values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single integer value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single byte value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single unsigned integer value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of unsigned integer values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single unsigned short value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of unsigned short values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes an array of signed long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of signed long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes an array of unsigned long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of unsigned long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_bytes(self, data : List[int]) -> None:
        '''Writes the specified data.
        
        :param data: The data to write.'''
        raise NotImplementedError()
    
    def write_double(self, data : float) -> None:
        '''Writes a single double value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_doubles(self, data : List[float]) -> None:
        '''Writes an array of double values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_float(self, data : float) -> None:
        '''Writes a single float value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_floats(self, data : List[float]) -> None:
        '''Writes an array of float values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_rational(self, data : aspose.imaging.fileformats.tiff.TiffRational) -> None:
        '''Writes a single rational number value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_s_rational(self, data : aspose.imaging.fileformats.tiff.TiffSRational) -> None:
        '''Writes a single signed rational number value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_rationals(self, data : List[aspose.imaging.fileformats.tiff.TiffRational]) -> None:
        '''Writes an array of unsigned rational values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_s_rationals(self, data : List[aspose.imaging.fileformats.tiff.TiffSRational]) -> None:
        '''Writes an array of signed rational values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_s_byte(self, data : int) -> None:
        '''Writes a single signed byte value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_s_bytes(self, data : List[int]) -> None:
        '''Writes an array of signed byte values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_ints(self, data : List[int]) -> None:
        '''Writes an array of integer values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_short(self, data : int) -> None:
        '''Writes a single short value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_shorts(self, data : List[int]) -> None:
        '''Writes an array of short values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_int(self, data : int) -> None:
        '''Writes a single integer value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_byte(self, data : int) -> None:
        '''Writes a single byte value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_uint(self, data : int) -> None:
        '''Writes a single unsigned integer value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_uints(self, data : List[int]) -> None:
        '''Writes an array of unsigned integer values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_ushort(self, data : int) -> None:
        '''Writes a single unsigned short value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_ushorts(self, data : List[int]) -> None:
        '''Writes an array of unsigned short values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_long(self, data : int) -> None:
        '''Writes an array of signed long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_longs(self, data : List[int]) -> None:
        '''Writes an array of signed long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_ulong(self, data : int) -> None:
        '''Writes an array of unsigned long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_ulongs(self, data : List[int]) -> None:
        '''Writes an array of unsigned long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @property
    def sync_root(self) -> Any:
        '''Gets an object that can be used to synchronize access to the synchronized resource.'''
        raise NotImplementedError()
    
    @property
    def position(self) -> int:
        '''Gets the stream position.'''
        raise NotImplementedError()
    
    @position.setter
    def position(self, value : int) -> None:
        '''Sets the stream position.'''
        raise NotImplementedError()
    

class TiffStreamFactory:
    '''The Tiff stream factory based on byte endianness.'''
    
    @overload
    @staticmethod
    def get_tiff_reader(stream : aspose.imaging.StreamContainer, byte_order : aspose.imaging.fileformats.tiff.enums.TiffByteOrder, is_big_tiff : bool) -> aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader:
        '''Gets the tiff stream reader.
        
        :param stream: The stream container.
        :param byte_order: The byte order.
        :param is_big_tiff: Indicates TIFF type.
        :returns: Tiff stream suitable for reading.'''
        raise NotImplementedError()
    
    @overload
    @staticmethod
    def get_tiff_reader(bytes : List[int], bytes_offset : int, data_length : int, byte_order : aspose.imaging.fileformats.tiff.enums.TiffByteOrder, is_big_tiff : bool) -> aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader:
        '''Gets the tiff stream reader.
        
        :param bytes: The bytes.
        :param bytes_offset: The bytes offset.
        :param data_length: Length of the data.
        :param byte_order: The byte order.
        :param is_big_tiff: Indicates Tiff type: original or big.
        :returns: Tiff stream suitable for reading.'''
        raise NotImplementedError()
    
    @staticmethod
    def get_tiff_writer(stream : aspose.imaging.StreamContainer, byte_order : aspose.imaging.fileformats.tiff.enums.TiffByteOrder, is_big_tiff : bool) -> aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter:
        '''Gets the tiff stream writer.
        
        :param stream: The stream container.
        :param byte_order: The byte order.
        :param is_big_tiff: Indicates TIFF type.
        :returns: Tiff stream suitable for writing.'''
        raise NotImplementedError()
    

class TiffStreamReader:
    '''The tiff stream for handling little endian tiff file format.'''
    
    @overload
    def __init__(self, data : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader` class.
        
        :param data: The byte array data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data : List[int], start_index : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader` class.
        
        :param data: The byte array data.
        :param start_index: The start index into ``data``.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, data : List[int], start_index : int, data_length : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader` class.
        
        :param data: The byte array data.
        :param start_index: The start index into ``data``.
        :param data_length: Length of the data.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, stream_container : aspose.imaging.StreamContainer) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffStreamReader` class.
        
        :param stream_container: The stream container.'''
        raise NotImplementedError()
    
    @overload
    def read_bytes(self, array : List[int], array_index : int, position : int, count : int) -> int:
        '''Reads an array of byte values from the stream.
        
        :param array: The array to fill.
        :param array_index: The array index to start putting values to.
        :param position: The stream position to read from.
        :param count: The elements count to read.
        :returns: The array of byte values.'''
        raise NotImplementedError()
    
    @overload
    def read_bytes(self, position : int, count : int) -> List[int]:
        '''Reads an array of unsigned byte values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of unsigned byte values.'''
        raise NotImplementedError()
    
    def read_double(self, position : int) -> float:
        '''Read a single double value from the stream.
        
        :param position: The position to read from.
        :returns: The single double value.'''
        raise NotImplementedError()
    
    def read_double_array(self, position : int, count : int) -> List[float]:
        '''Reads an array of double values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of double values.'''
        raise NotImplementedError()
    
    def read_float(self, position : int) -> float:
        '''Read a single float value from the stream.
        
        :param position: The position to read from.
        :returns: The single float value.'''
        raise NotImplementedError()
    
    def read_float_array(self, position : int, count : int) -> List[float]:
        '''Reads an array of float values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of float values.'''
        raise NotImplementedError()
    
    def read_rational(self, position : int) -> aspose.imaging.fileformats.tiff.TiffRational:
        '''Read a single rational number value from the stream.
        
        :param position: The position to read from.
        :returns: The rational number.'''
        raise NotImplementedError()
    
    def read_s_rational(self, position : int) -> aspose.imaging.fileformats.tiff.TiffSRational:
        '''Read a single signed rational number value from the stream.
        
        :param position: The position to read from.
        :returns: The signed rational number.'''
        raise NotImplementedError()
    
    def read_rational_array(self, position : int, count : int) -> List[aspose.imaging.fileformats.tiff.TiffRational]:
        '''Reads an array of rational values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of rational values.'''
        raise NotImplementedError()
    
    def read_s_rational_array(self, position : int, count : int) -> List[aspose.imaging.fileformats.tiff.TiffSRational]:
        '''Reads an array of signed rational values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed rational values.'''
        raise NotImplementedError()
    
    def read_s_byte(self, position : int) -> int:
        '''Reads signed byte data from the stream.
        
        :param position: The position to read from.
        :returns: The signed byte value.'''
        raise NotImplementedError()
    
    def read_s_byte_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of signed byte values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed byte values.'''
        raise NotImplementedError()
    
    def read_s_int(self, position : int) -> int:
        '''Read signed integer value from the stream.
        
        :param position: The position to read from.
        :returns: A signed integer value.'''
        raise NotImplementedError()
    
    def read_s_int_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of signed integer values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed integer values.'''
        raise NotImplementedError()
    
    def read_s_short(self, position : int) -> int:
        '''Read signed short value from the stream.
        
        :param position: The position to read from.
        :returns: A signed short value.'''
        raise NotImplementedError()
    
    def read_s_short_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of signed short values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed short values.'''
        raise NotImplementedError()
    
    def read_u_int(self, position : int) -> int:
        '''Read unsigned integer value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned integer value.'''
        raise NotImplementedError()
    
    def read_u_int_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of unsigned integer values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of unsigned integer values.'''
        raise NotImplementedError()
    
    def read_u_short(self, position : int) -> int:
        '''Read unsigned short value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned short value.'''
        raise NotImplementedError()
    
    def read_u_short_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of unsigned integer values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of unsigned integer values.'''
        raise NotImplementedError()
    
    def read_long(self, position : int) -> int:
        '''Read unsigned long value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned short value.'''
        raise NotImplementedError()
    
    def read_long_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of ulong values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The ulong array.'''
        raise NotImplementedError()
    
    def read_u_long(self, position : int) -> int:
        '''Read unsigned long value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned short value.'''
        raise NotImplementedError()
    
    def read_u_long_array(self, position : int, count : int) -> List[int]:
        '''Reads an array of ulong values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The ulong array.'''
        raise NotImplementedError()
    
    def to_stream_container(self, start_position : int) -> aspose.imaging.StreamContainer:
        '''Converts the underlying data to the stream container.
        
        :param start_position: The start position to start conversion from.
        :returns: The :py:class:`aspose.imaging.StreamContainer` with converted data.'''
        raise NotImplementedError()
    
    @property
    def length(self) -> int:
        '''Gets the reader length.'''
        raise NotImplementedError()
    
    @property
    def throw_exceptions(self) -> bool:
        '''Gets a value indicating whether exceptions are thrown on incorrect data processing (reading or writing to stream).'''
        raise NotImplementedError()
    
    @throw_exceptions.setter
    def throw_exceptions(self, value : bool) -> None:
        '''Sets a value indicating whether exceptions are thrown on incorrect data processing (reading or writing to stream).'''
        raise NotImplementedError()
    

class TiffStreamWriter:
    '''The Tiff stream writer.'''
    
    def __init__(self, writer : aspose.imaging.StreamContainer) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.tiff.filemanagement.TiffStreamWriter` class.
        
        :param writer: The stream writer.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int], offset : int, data_length : int) -> None:
        '''Writes the specified data.
        
        :param data: The data to write.
        :param offset: The data offset.
        :param data_length: Length of the data to writer.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes the specified data.
        
        :param data: The data to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : float) -> None:
        '''Writes a single double value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[float]) -> None:
        '''Writes an array of double values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : float) -> None:
        '''Writes a single float value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[float]) -> None:
        '''Writes an array of float values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : aspose.imaging.fileformats.tiff.TiffRational) -> None:
        '''Writes a single rational number value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : aspose.imaging.fileformats.tiff.TiffSRational) -> None:
        '''Writes a single signed rational number value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[aspose.imaging.fileformats.tiff.TiffRational]) -> None:
        '''Writes an array of unsigned rational values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[aspose.imaging.fileformats.tiff.TiffSRational]) -> None:
        '''Writes an array of signed rational values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single signed byte value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of signed byte values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of integer values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single short value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of short values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single integer value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single byte value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single unsigned integer value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of unsigned integer values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes a single unsigned short value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of unsigned short values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes an array of signed long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of signed long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : int) -> None:
        '''Writes an array of unsigned long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @overload
    def write(self, data : List[int]) -> None:
        '''Writes an array of unsigned long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_bytes(self, data : List[int]) -> None:
        '''Writes the specified data.
        
        :param data: The data to write.'''
        raise NotImplementedError()
    
    def write_double(self, data : float) -> None:
        '''Writes a single double value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_doubles(self, data : List[float]) -> None:
        '''Writes an array of double values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_float(self, data : float) -> None:
        '''Writes a single float value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_floats(self, data : List[float]) -> None:
        '''Writes an array of float values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_rational(self, data : aspose.imaging.fileformats.tiff.TiffRational) -> None:
        '''Writes a single rational number value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_s_rational(self, data : aspose.imaging.fileformats.tiff.TiffSRational) -> None:
        '''Writes a single signed rational number value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_rationals(self, data : List[aspose.imaging.fileformats.tiff.TiffRational]) -> None:
        '''Writes an array of unsigned rational values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_s_rationals(self, data : List[aspose.imaging.fileformats.tiff.TiffSRational]) -> None:
        '''Writes an array of signed rational values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_s_byte(self, data : int) -> None:
        '''Writes a single signed byte value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_s_bytes(self, data : List[int]) -> None:
        '''Writes an array of signed byte values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_ints(self, data : List[int]) -> None:
        '''Writes an array of integer values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_short(self, data : int) -> None:
        '''Writes a single short value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_shorts(self, data : List[int]) -> None:
        '''Writes an array of short values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_int(self, data : int) -> None:
        '''Writes a single integer value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_byte(self, data : int) -> None:
        '''Writes a single byte value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_uint(self, data : int) -> None:
        '''Writes a single unsigned integer value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_uints(self, data : List[int]) -> None:
        '''Writes an array of unsigned integer values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_ushort(self, data : int) -> None:
        '''Writes a single unsigned short value to the stream.
        
        :param data: The value to write.'''
        raise NotImplementedError()
    
    def write_ushorts(self, data : List[int]) -> None:
        '''Writes an array of unsigned short values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_long(self, data : int) -> None:
        '''Writes an array of signed long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_longs(self, data : List[int]) -> None:
        '''Writes an array of signed long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_ulong(self, data : int) -> None:
        '''Writes an array of unsigned long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    def write_ulongs(self, data : List[int]) -> None:
        '''Writes an array of unsigned long values to the stream.
        
        :param data: The array to write.'''
        raise NotImplementedError()
    
    @property
    def sync_root(self) -> Any:
        '''Gets an object that can be used to synchronize access to the synchronized resource.'''
        raise NotImplementedError()
    
    @property
    def position(self) -> int:
        '''Gets the stream position.'''
        raise NotImplementedError()
    
    @position.setter
    def position(self, value : int) -> None:
        '''Sets the stream position.'''
        raise NotImplementedError()
    

