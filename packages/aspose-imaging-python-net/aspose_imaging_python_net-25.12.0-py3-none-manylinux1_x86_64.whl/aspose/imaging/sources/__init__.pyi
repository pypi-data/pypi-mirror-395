"""Namespace contains different stream sources which are suitable for input or output data flow."""
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

class FileCreateSource(FileSource):
    '''Represents a file source for creation.'''
    
    @overload
    def __init__(self, file_path : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.sources.FileCreateSource` class.
        
        :param file_path: The file path to create.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, file_path : str, is_temporal : bool) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.sources.FileCreateSource` class.
        
        :param file_path: The file path to create.
        :param is_temporal: If set to ``true`` the created file will be temporal.'''
        raise NotImplementedError()
    
    def get_stream_container(self) -> aspose.imaging.StreamContainer:
        '''Gets the stream container.
        
        :returns: the stream container.'''
        raise NotImplementedError()
    
    @property
    def is_temporal(self) -> bool:
        '''Gets a value indicating whether file will be temporal.'''
        raise NotImplementedError()
    
    @property
    def file_path(self) -> str:
        '''Gets the file path to create.'''
        raise NotImplementedError()
    

class FileOpenSource(FileSource):
    '''Represents a file source for opening.'''
    
    def __init__(self, file_path : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.sources.FileOpenSource` class.
        
        :param file_path: The file path to open.'''
        raise NotImplementedError()
    
    def get_stream_container(self) -> aspose.imaging.StreamContainer:
        '''Gets the stream container.
        
        :returns: the stream container.'''
        raise NotImplementedError()
    
    @property
    def is_temporal(self) -> bool:
        '''Gets a value indicating whether file will be temporal.'''
        raise NotImplementedError()
    
    @property
    def file_path(self) -> str:
        '''Gets the file path to open.'''
        raise NotImplementedError()
    

class FileSource(aspose.imaging.Source):
    '''Represents a file source which is capable of files manipulation.'''
    
    def get_stream_container(self) -> aspose.imaging.StreamContainer:
        '''Gets the stream container.
        
        :returns: the stream container.'''
        raise NotImplementedError()
    
    @property
    def is_temporal(self) -> bool:
        '''Gets a value indicating whether file will be temporal.'''
        raise NotImplementedError()
    

class StreamSource(aspose.imaging.Source):
    '''Represents a stream source.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.sources.StreamSource` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, stream : io._IOBase) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.sources.StreamSource` class.
        
        :param stream: The stream to open.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, stream : io._IOBase, dispose_stream : bool) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.sources.StreamSource` class.
        
        :param stream: The stream to open.
        :param dispose_stream: if set to ``true`` the stream will be disposed.'''
        raise NotImplementedError()
    
    def get_stream_container(self) -> aspose.imaging.StreamContainer:
        '''Gets the stream container.
        
        :returns: the stream container.'''
        raise NotImplementedError()
    
    @property
    def stream(self) -> io._IOBase:
        '''Gets the stream.'''
        raise NotImplementedError()
    
    @property
    def dispose_stream(self) -> bool:
        '''Gets a value indicating whether stream should be disposed whenever container gets disposed.'''
        raise NotImplementedError()
    

