"""The namespace handles AsyncTask processing."""
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

class AsyncTask:
    '''The static factory class for creating the asynchronous tasks'''
    

class AsyncTaskProgress:
    '''Provides progress info for the asynchronous task.'''
    
    def __init__(self, progress_percentage : int, duration : timedelta) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.asynctask.AsyncTaskProgress` class.
        
        :param progress_percentage: The progress percentage.
        :param duration: The duration.'''
        raise NotImplementedError()
    
    @property
    def DURATION(self) -> timedelta:
        '''The duration of the asynchronous task.'''
        raise NotImplementedError()
    
    @property
    def PROGRESS_PERCENTAGE(self) -> int:
        '''The progress of the asynchronous task, in percent.'''
        raise NotImplementedError()
    

class IAsyncTask:
    '''The asynchronous task.'''
    
    def run_async(self) -> None:
        '''Runs this task.'''
        raise NotImplementedError()
    
    def cancel(self) -> None:
        '''Cancels this task.
        The task is completed safely by the controlled stopping of the algorithm.'''
        raise NotImplementedError()
    
    def abort(self) -> None:
        '''Aborts this task.
        The task is completed immediately, with the risk of not freeing internal unmanaged resources.'''
        raise NotImplementedError()
    
    def wait_on_done(self) -> None:
        '''Waits until task is finished.'''
        raise NotImplementedError()
    
    @property
    def is_busy(self) -> bool:
        '''Gets a value indicating whether this task is currently running.'''
        raise NotImplementedError()
    
    @property
    def is_canceled(self) -> bool:
        '''Gets a value indicating whether this task was canceled.'''
        raise NotImplementedError()
    
    @property
    def is_faulted(self) -> bool:
        '''Gets a value indicating whether this task was faulted.'''
        raise NotImplementedError()
    
    @property
    def result(self) -> Any:
        '''Gets the result of this task.'''
        raise NotImplementedError()
    

class IAsyncTaskState:
    '''Provides access to the state of the asynchronous task.'''
    
    def indicate_progress(self, event_type : aspose.imaging.progressmanagement.EventType) -> None:
        '''Sets the progress of the asynchronous task.
        
        :param event_type: The progress state.'''
        raise NotImplementedError()
    
    def increment_progress_max_value(self, value : int) -> None:
        '''Increments the progress maximum value.
        
        :param value: The increase value.'''
        raise NotImplementedError()
    
    @property
    def is_canceled(self) -> bool:
        '''Gets a value indicating whether the asynchronous task is canceled.'''
        raise NotImplementedError()
    
    @property
    def progress(self) -> aspose.imaging.progressmanagement.EventType:
        '''Gets the progress of the asynchronous task.'''
        raise NotImplementedError()
    

