"""The  contains escape types [MS-WMF]: Windows"""
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

class WmfEscapeEnhancedMetafile(WmfEscapeRecordBase):
    '''The Escape Enhanced Meta file record.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def byte_count(self) -> int:
        '''Gets the byte count.'''
        raise NotImplementedError()
    
    @byte_count.setter
    def byte_count(self, value : int) -> None:
        '''Sets the byte count.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the data.'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : List[int]) -> None:
        '''Sets the data.'''
        raise NotImplementedError()
    
    @property
    def checked(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.wmf.objects.escaperecords.WmfEscapeRecordBase` is checked.'''
        raise NotImplementedError()
    
    @checked.setter
    def checked(self, value : bool) -> None:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.wmf.objects.escaperecords.WmfEscapeRecordBase` is checked.'''
        raise NotImplementedError()
    
    @property
    def comment_identifier(self) -> int:
        '''Gets the comment identifier.'''
        raise NotImplementedError()
    
    @comment_identifier.setter
    def comment_identifier(self, value : int) -> None:
        '''Sets the comment identifier.'''
        raise NotImplementedError()
    
    @property
    def comment_type(self) -> int:
        '''Gets the type of the comment.'''
        raise NotImplementedError()
    
    @comment_type.setter
    def comment_type(self, value : int) -> None:
        '''Sets the type of the comment.'''
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
    def checksum(self) -> int:
        '''Gets the checksum.'''
        raise NotImplementedError()
    
    @checksum.setter
    def checksum(self, value : int) -> None:
        '''Sets the checksum.'''
        raise NotImplementedError()
    
    @property
    def flags(self) -> int:
        '''Gets the flags.'''
        raise NotImplementedError()
    
    @flags.setter
    def flags(self, value : int) -> None:
        '''Sets the flags.'''
        raise NotImplementedError()
    
    @property
    def comment_record_count(self) -> int:
        '''Gets the comment record count.'''
        raise NotImplementedError()
    
    @comment_record_count.setter
    def comment_record_count(self, value : int) -> None:
        '''Sets the comment record count.'''
        raise NotImplementedError()
    
    @property
    def current_record_size(self) -> int:
        '''Gets the size of the current record.'''
        raise NotImplementedError()
    
    @current_record_size.setter
    def current_record_size(self, value : int) -> None:
        '''Sets the size of the current record.'''
        raise NotImplementedError()
    
    @property
    def remaining_bytes(self) -> int:
        '''Gets the remaining bytes.'''
        raise NotImplementedError()
    
    @remaining_bytes.setter
    def remaining_bytes(self, value : int) -> None:
        '''Sets the remaining bytes.'''
        raise NotImplementedError()
    
    @property
    def enhanced_metafile_data_size(self) -> int:
        '''Gets the size of the enhanced metafile data.'''
        raise NotImplementedError()
    
    @enhanced_metafile_data_size.setter
    def enhanced_metafile_data_size(self, value : int) -> None:
        '''Sets the size of the enhanced metafile data.'''
        raise NotImplementedError()
    
    @property
    def enhanced_metafile_data(self) -> List[int]:
        '''Gets the enhanced metafile data.'''
        raise NotImplementedError()
    
    @enhanced_metafile_data.setter
    def enhanced_metafile_data(self, value : List[int]) -> None:
        '''Sets the enhanced metafile data.'''
        raise NotImplementedError()
    

class WmfEscapePostScript(WmfEscapeRecordBase):
    '''The Escape PostScript data record.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def byte_count(self) -> int:
        '''Gets the byte count.'''
        raise NotImplementedError()
    
    @byte_count.setter
    def byte_count(self, value : int) -> None:
        '''Sets the byte count.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the data.'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : List[int]) -> None:
        '''Sets the data.'''
        raise NotImplementedError()
    
    @property
    def checked(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.wmf.objects.escaperecords.WmfEscapeRecordBase` is checked.'''
        raise NotImplementedError()
    
    @checked.setter
    def checked(self, value : bool) -> None:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.wmf.objects.escaperecords.WmfEscapeRecordBase` is checked.'''
        raise NotImplementedError()
    
    @property
    def post_script_part(self) -> str:
        '''Gets the post script part.'''
        raise NotImplementedError()
    
    @post_script_part.setter
    def post_script_part(self, value : str) -> None:
        '''Sets the post script part.'''
        raise NotImplementedError()
    

class WmfEscapeRecordBase(aspose.imaging.fileformats.wmf.objects.WmfObject):
    '''The escape record base.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def byte_count(self) -> int:
        '''Gets the byte count.'''
        raise NotImplementedError()
    
    @byte_count.setter
    def byte_count(self, value : int) -> None:
        '''Sets the byte count.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the data.'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : List[int]) -> None:
        '''Sets the data.'''
        raise NotImplementedError()
    
    @property
    def checked(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.wmf.objects.escaperecords.WmfEscapeRecordBase` is checked.'''
        raise NotImplementedError()
    
    @checked.setter
    def checked(self, value : bool) -> None:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.wmf.objects.escaperecords.WmfEscapeRecordBase` is checked.'''
        raise NotImplementedError()
    

