"""The namespace contains classes for PDF file format integration."""
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

class PdfCoreOptions:
    '''The common options for convertion to PDF'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def headings_outline_levels(self) -> int:
        '''Specifies how many levels of outline items to include in the document outline.
        0 - no outline, 1 - one outline level and so on.
        Default is 0.'''
        raise NotImplementedError()
    
    @headings_outline_levels.setter
    def headings_outline_levels(self, value : int) -> None:
        '''Specifies how many levels of outline items to include in the document outline.
        0 - no outline, 1 - one outline level and so on.
        Default is 0.'''
        raise NotImplementedError()
    
    @property
    def expanded_outline_levels(self) -> int:
        '''Specifies how many levels in the document outline to show expanded when the PDF file is viewed.
        0 - the document outline is not expanded.
        1 - first level items in the document are expanded and so on.
        Default is 0.'''
        raise NotImplementedError()
    
    @expanded_outline_levels.setter
    def expanded_outline_levels(self, value : int) -> None:
        '''Specifies how many levels in the document outline to show expanded when the PDF file is viewed.
        0 - the document outline is not expanded.
        1 - first level items in the document are expanded and so on.
        Default is 0.'''
        raise NotImplementedError()
    
    @property
    def bookmarks_outline_level(self) -> int:
        '''Specifies at which level in the document outline to display bookmark objects.
        0 - not displayed.
        1 at first level and so on.
        Default is 0.'''
        raise NotImplementedError()
    
    @bookmarks_outline_level.setter
    def bookmarks_outline_level(self, value : int) -> None:
        '''Specifies at which level in the document outline to display bookmark objects.
        0 - not displayed.
        1 at first level and so on.
        Default is 0.'''
        raise NotImplementedError()
    
    @property
    def jpeg_quality(self) -> int:
        '''Specifies the quality of JPEG compression for images (if JPEG compression is used).
        Default is 95.'''
        raise NotImplementedError()
    
    @jpeg_quality.setter
    def jpeg_quality(self, value : int) -> None:
        '''Specifies the quality of JPEG compression for images (if JPEG compression is used).
        Default is 95.'''
        raise NotImplementedError()
    
    @property
    def pdf_compliance(self) -> aspose.imaging.PdfComplianceVersion:
        '''Gets the PDF compliance.'''
        raise NotImplementedError()
    
    @pdf_compliance.setter
    def pdf_compliance(self, value : aspose.imaging.PdfComplianceVersion) -> None:
        '''Sets the PDF compliance.'''
        raise NotImplementedError()
    
    @property
    def compression(self) -> aspose.imaging.imageoptions.PdfImageCompressionOptions:
        '''Gets the compression.'''
        raise NotImplementedError()
    
    @compression.setter
    def compression(self, value : aspose.imaging.imageoptions.PdfImageCompressionOptions) -> None:
        '''Sets the compression.'''
        raise NotImplementedError()
    

class PdfDocumentInfo:
    '''This class represents set of metadata for document description.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def keywords(self) -> str:
        '''Gets keywords of the document.'''
        raise NotImplementedError()
    
    @keywords.setter
    def keywords(self, value : str) -> None:
        '''Sets keywords of the document.'''
        raise NotImplementedError()
    
    @property
    def title(self) -> str:
        '''Gets title of the document.'''
        raise NotImplementedError()
    
    @title.setter
    def title(self, value : str) -> None:
        '''Sets title of the document.'''
        raise NotImplementedError()
    
    @property
    def author(self) -> str:
        '''Gets author of the document.'''
        raise NotImplementedError()
    
    @author.setter
    def author(self, value : str) -> None:
        '''Sets author of the document.'''
        raise NotImplementedError()
    
    @property
    def subject(self) -> str:
        '''Gets subject of the document.'''
        raise NotImplementedError()
    
    @subject.setter
    def subject(self, value : str) -> None:
        '''Sets subject of the document.'''
        raise NotImplementedError()
    

