"""The namespace contains Dicom metadata related helper classes, constants and methods."""
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

class DicomPackage(aspose.imaging.xmp.XmpPackage):
    '''The Dicom Xmp package.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.schemas.dicom.DicomPackage` class.'''
        raise NotImplementedError()
    
    @overload
    def add_value(self, key : str, value : str) -> None:
        '''Adds the value to the specified key.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The value to add to.'''
        raise NotImplementedError()
    
    @overload
    def add_value(self, key : str, value : Any) -> None:
        '''Adds the value to the specified key.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The value to add to.'''
        raise NotImplementedError()
    
    @overload
    def set_value(self, key : str, value : aspose.imaging.xmp.IXmlValue) -> None:
        '''Sets the value.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The value to add to.'''
        raise NotImplementedError()
    
    @overload
    def set_value(self, key : str, value : aspose.imaging.xmp.types.IXmpType) -> None:
        '''Sets the value.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The value to add to.'''
        raise NotImplementedError()
    
    def contains_key(self, key : str) -> bool:
        '''Determines whether this collection specified key.
        
        :param key: The key to be checked.
        :returns: if the :py:class:`dict` contains the specified key; otherwise, .'''
        raise NotImplementedError()
    
    def get_prop_value(self, key : str) -> Any:
        '''Gets the :py:class:`Any` with the specified key.
        
        :param key: The key that identifies value.
        :returns: Returns the :py:class:`Any` with the specified key.'''
        raise NotImplementedError()
    
    def set_prop_value(self, key : str, value : Any) -> None:
        '''Gets or sets the :py:class:`Any` with the specified key.
        
        :param key: The key that identifies value.
        :param value: The :py:class:`Any` with the specified key.'''
        raise NotImplementedError()
    
    def try_get_value(self, key : str, value : List[Any]) -> bool:
        '''Gets the value by the ``key``.
        
        :param key: The XMP element key.
        :param value: The XMP value.
        :returns: , if the :py:class:`dict` contains the ``key``; otherwise, .'''
        raise NotImplementedError()
    
    def remove(self, key : str) -> bool:
        '''Remove the value with the specified key.
        
        :param key: The string representation of key that is identified with removed value.
        :returns: Returns true if the value with the specified key was removed.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Clears this instance.'''
        raise NotImplementedError()
    
    def set_xmp_type_value(self, key : str, value : aspose.imaging.xmp.types.XmpTypeBase) -> None:
        '''Sets the XMP type value.
        
        :param key: The string representation of key that is identified with set value.
        :param value: The value to set to.'''
        raise NotImplementedError()
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        raise NotImplementedError()
    
    def set_equipment_institution(self, equipment_institution : str) -> None:
        '''Sets the equipment institution.
        
        :param equipment_institution: The equipment institution.'''
        raise NotImplementedError()
    
    def set_equipment_manufacturer(self, equipment_manufacturer : str) -> None:
        '''Sets the equipment manufacturer.
        
        :param equipment_manufacturer: The equipment manufacturer.'''
        raise NotImplementedError()
    
    def set_patient_birth_date(self, patient_birth_date : str) -> None:
        '''Sets the patient\'s birth date.
        
        :param patient_birth_date: The patient\'s birth date.'''
        raise NotImplementedError()
    
    def set_patient_id(self, patient_id : str) -> None:
        '''Sets the patient\'s ID.
        
        :param patient_id: The patient\'s ID.'''
        raise NotImplementedError()
    
    def set_patient_name(self, patient_name : str) -> None:
        '''Sets the color mode.
        
        :param patient_name: The patient\'s name.'''
        raise NotImplementedError()
    
    def set_patient_sex(self, patient_sex : str) -> None:
        '''Sets the patient\'s sex.
        
        :param patient_sex: The patient\'s sex.'''
        raise NotImplementedError()
    
    def set_series_date_time(self, series_date_time : str) -> None:
        '''Sets the series date time.
        
        :param series_date_time: The series date time.'''
        raise NotImplementedError()
    
    def set_series_description(self, series_description : str) -> None:
        '''Sets series description.
        
        :param series_description: The series description.'''
        raise NotImplementedError()
    
    def set_series_modality(self, series_modality : str) -> None:
        '''Sets the document series modality.
        
        :param series_modality: The series modality.'''
        raise NotImplementedError()
    
    def set_series_number(self, series_number : str) -> None:
        '''Sets the series number.
        
        :param series_number: The series number.'''
        raise NotImplementedError()
    
    def set_study_date_time(self, study_date_time : str) -> None:
        '''Sets the study DateTime.
        
        :param study_date_time: The studyDateTime.'''
        raise NotImplementedError()
    
    def set_study_description(self, study_description : str) -> None:
        '''Sets the study description.
        
        :param study_description: The study description.'''
        raise NotImplementedError()
    
    def set_study_id(self, study_id : str) -> None:
        '''Sets the study ID.
        
        :param study_id: The study ID.'''
        raise NotImplementedError()
    
    def set_study_physician(self, study_physician : str) -> None:
        '''Sets the study physician.
        
        :param study_physician: The study physician.'''
        raise NotImplementedError()
    
    @property
    def xml_namespace(self) -> str:
        '''Gets the XML namespace.'''
        raise NotImplementedError()
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        raise NotImplementedError()
    
    @property
    def namespace_uri(self) -> str:
        '''Gets the namespace URI.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the XMP key count.'''
        raise NotImplementedError()
    

