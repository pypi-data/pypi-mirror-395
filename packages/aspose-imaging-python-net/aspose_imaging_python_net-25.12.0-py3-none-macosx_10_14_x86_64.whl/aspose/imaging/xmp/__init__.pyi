"""The namespace contains XMP related helper classes and methods."""
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

class IHasXmpData:
    ''':py:class:`aspose.imaging.xmp.XmpPacketWrapper` instance container interface.'''
    
    @property
    def xmp_data(self) -> aspose.imaging.xmp.XmpPacketWrapper:
        '''Gets Xmp data.'''
        raise NotImplementedError()
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.imaging.xmp.XmpPacketWrapper) -> None:
        '''Sets Xmp data.'''
        raise NotImplementedError()
    

class IXmlValue:
    '''Converts xmp values to the XML string representation.'''
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        raise NotImplementedError()
    

class LangAlt(IXmlValue):
    '''Represents XMP Language Alternative.'''
    
    @overload
    def __init__(self, default_value : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.LangAlt` class.
        
        :param default_value: The default value.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.LangAlt` class.'''
        raise NotImplementedError()
    
    def add_language(self, language : str, value : str) -> None:
        '''Adds the language.
        
        :param language: The language.
        :param value: The language value.'''
        raise NotImplementedError()
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        raise NotImplementedError()
    

class Namespaces:
    '''Contains namespaces used in RDF document.'''
    
    @staticmethod
    @property
    def XMP_GRAPHICS() -> str:
        '''XMP graphics namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_GRAPHICS_THUMBNAIL() -> str:
        '''XMP graphics namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_TYPE_FONT() -> str:
        '''XMP Font type.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_TYPE_DIMENSIONS() -> str:
        '''XMP Dimensions type.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_TYPE_RESOURCE_REF() -> str:
        '''XMP ResourceRef URI.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_TYPE_RESOURCE_EVENT() -> str:
        '''XMP ResourceEvent URI.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_TYPE_VERSION() -> str:
        '''XMP Version.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XML() -> str:
        '''Xml namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def RDF() -> str:
        '''Resource definition framework namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def DUBLIN_CORE() -> str:
        '''Dublic Core namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_BASIC() -> str:
        '''XMP Basic namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_RIGHTS() -> str:
        '''XMP Rights Management namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_MM() -> str:
        '''XMP digital asset management namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def XMP_DM() -> str:
        '''XMP Dynamic Media namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def PDF() -> str:
        '''Adobe PDF namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def PHOTOSHOP() -> str:
        '''Adobe Photoshop namespace.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def DICOM() -> str:
        '''Dicom namespace.'''
        raise NotImplementedError()


class XmpArray(XmpCollection):
    '''Represents Xmp Array in :py:class:`aspose.imaging.xmp.XmpPackage`.'''
    
    def __init__(self, type : aspose.imaging.xmp.XmpArrayType, items : List[str]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpArray` class.
        
        :param type: The type of array.
        :param items: The items list.'''
        raise NotImplementedError()
    
    def add_item(self, item : str) -> None:
        '''Adds new item.
        
        :param item: The item to be added to list of items.'''
        raise NotImplementedError()
    
    def add(self, item : Any) -> None:
        '''Adds an XMP data item.
        
        :param item: An XMP item.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Gets the XMP string value of this.
        
        :returns: Returns the string contained value in XMP format.'''
        raise NotImplementedError()
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        raise NotImplementedError()
    
    @property
    def values(self) -> List[str]:
        '''Gets array of values inside :py:class:`aspose.imaging.xmp.XmpArray`.'''
        raise NotImplementedError()
    

class XmpArrayHelper:
    '''The helper class for processing RDF logic'''
    
    @staticmethod
    def get_rdf_code(xmp_array_type : aspose.imaging.xmp.XmpArrayType) -> str:
        '''Gets the RDF code for specific :py:class:`aspose.imaging.xmp.XmpArrayType`.
        
        :param xmp_array_type: Type of the XMP array.
        :returns: Returns the RDF code for specific :py:class:`aspose.imaging.xmp.XmpArrayType`.'''
        raise NotImplementedError()
    

class XmpCollection(aspose.imaging.xmp.types.IXmpType):
    '''An XMP element collection.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpCollection` class.'''
        raise NotImplementedError()
    
    def add_item(self, item : str) -> None:
        '''Adds new item.
        
        :param item: The item to be added to list of items.'''
        raise NotImplementedError()
    
    def add(self, item : Any) -> None:
        '''Adds an XMP data item.
        
        :param item: An XMP item.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Gets the XMP string value of this.
        
        :returns: Returns the string contained value in XMP format.'''
        raise NotImplementedError()
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        raise NotImplementedError()
    

class XmpElementBase:
    '''Represents base xmp element contains attributes.'''
    
    def add_attribute(self, attribute : str, value : str) -> None:
        '''Adds the attribute.
        
        :param attribute: The attribute.
        :param value: The value.'''
        raise NotImplementedError()
    
    def get_attribute(self, attribute : str) -> str:
        '''Gets the attribute.
        
        :param attribute: The attribute.
        :returns: Returns the attribute for specified attribute name.'''
        raise NotImplementedError()
    
    def clear_attributes(self) -> None:
        '''Removes all attributes.'''
        raise NotImplementedError()
    
    def equals(self, other : aspose.imaging.xmp.XmpElementBase) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    

class XmpHeaderPi(IXmlValue):
    '''Represents XMP header processing instruction.'''
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpHeaderPi` class.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self, guid : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpHeaderPi` class.
        
        :param guid: The unique identifier.'''
        raise NotImplementedError()
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        raise NotImplementedError()
    
    def equals(self, other : aspose.imaging.xmp.XmpHeaderPi) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    
    @property
    def guid(self) -> str:
        '''Represents Header Guid.'''
        raise NotImplementedError()
    
    @guid.setter
    def guid(self, value : str) -> None:
        '''Represents Header Guid.'''
        raise NotImplementedError()
    

class XmpMeta(XmpElementBase):
    '''Represents xmpmeta. Optional.
    The purpose of this element is to identify XMP metadata within general XML text that might contain other non-XMP uses of RDF.'''
    
    @overload
    def __init__(self, toolkit_version : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpMeta` class.
        
        :param toolkit_version: Adobe XMP toolkit version.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpMeta` class.'''
        raise NotImplementedError()
    
    @overload
    def equals(self, other : aspose.imaging.xmp.XmpMeta) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    
    @overload
    def equals(self, other : aspose.imaging.xmp.XmpElementBase) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    
    def add_attribute(self, attribute : str, value : str) -> None:
        '''Adds the attribute.
        
        :param attribute: The attribute.
        :param value: The value.'''
        raise NotImplementedError()
    
    def get_attribute(self, attribute : str) -> str:
        '''Gets the attribute.
        
        :param attribute: The attribute.
        :returns: Returns the attribute for specified attribute name.'''
        raise NotImplementedError()
    
    def clear_attributes(self) -> None:
        '''Removes all attributes.'''
        raise NotImplementedError()
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        raise NotImplementedError()
    
    @property
    def adobe_xmp_toolkit(self) -> str:
        '''Gets or set Adobe Xmp toolkit version.'''
        raise NotImplementedError()
    
    @adobe_xmp_toolkit.setter
    def adobe_xmp_toolkit(self, value : str) -> None:
        '''Set Adobe Xmp toolkit version.'''
        raise NotImplementedError()
    

class XmpPackage(IXmlValue):
    '''Represents base abstraction for XMP package.'''
    
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
    

class XmpPackageBaseCollection:
    '''Represents collection of :py:class:`aspose.imaging.xmp.XmpPackage`.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpPackageBaseCollection` class.'''
        raise NotImplementedError()
    
    def add(self, package : aspose.imaging.xmp.XmpPackage) -> None:
        '''Adds new instance of :py:class:`aspose.imaging.xmp.XmpPackage`.
        
        :param package: The XMP package to add.'''
        raise NotImplementedError()
    
    def remove(self, package : aspose.imaging.xmp.XmpPackage) -> None:
        '''Removes the specified XMP package.
        
        :param package: The XMP package to remove.'''
        raise NotImplementedError()
    
    def get_packages(self) -> List[aspose.imaging.xmp.XmpPackage]:
        '''Get array of :py:class:`aspose.imaging.xmp.XmpPackage`.
        
        :returns: Returns an array of XMP packages.'''
        raise NotImplementedError()
    
    def get_package(self, namespace_uri : str) -> aspose.imaging.xmp.XmpPackage:
        '''Gets :py:class:`aspose.imaging.xmp.XmpPackage` by it\'s namespaceURI.
        
        :param namespace_uri: The namespace URI to get package for.
        :returns: Returns XMP package for specified namespace Uri.'''
        raise NotImplementedError()
    
    def clear(self) -> None:
        '''Clear all :py:class:`aspose.imaging.xmp.XmpPackage` inside collection.'''
        raise NotImplementedError()
    
    @property
    def count(self) -> int:
        '''Gets the number of elements in the collection.'''
        raise NotImplementedError()
    

class XmpPacketWrapper(IXmlValue):
    '''Contains serialized xmp package including header and trailer.'''
    
    @overload
    def __init__(self, header : aspose.imaging.xmp.XmpHeaderPi, trailer : aspose.imaging.xmp.XmpTrailerPi, xmp_meta : aspose.imaging.xmp.XmpMeta) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpPacketWrapper` class.
        
        :param header: The XMP header of processing instruction.
        :param trailer: The XMP trailer of processing instruction.
        :param xmp_meta: The XMP metadata.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpPacketWrapper` class.'''
        raise NotImplementedError()
    
    def add_package(self, package : aspose.imaging.xmp.XmpPackage) -> None:
        '''Adds the package.
        
        :param package: The package.'''
        raise NotImplementedError()
    
    def get_package(self, namespace_uri : str) -> aspose.imaging.xmp.XmpPackage:
        '''Gets package by namespace URI.
        
        :param namespace_uri: The package schema URI.
        :returns: Returns the XMP package for specified namespace URI.'''
        raise NotImplementedError()
    
    def contains_package(self, namespace_uri : str) -> bool:
        '''Determines whethere package is exist in xmp wrapper.
        
        :param namespace_uri: Package schema uri.
        :returns: Returns true if package with specified namespace Uri exist in XMP wrapper.'''
        raise NotImplementedError()
    
    def remove_package(self, package : aspose.imaging.xmp.XmpPackage) -> None:
        '''Removes the XMP package.
        
        :param package: The package.'''
        raise NotImplementedError()
    
    def clear_packages(self) -> None:
        '''Removes all :py:class:`aspose.imaging.xmp.XmpPackage` inside XMP.'''
        raise NotImplementedError()
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns converted XMP value to XML.'''
        raise NotImplementedError()
    
    @property
    def header_pi(self) -> aspose.imaging.xmp.XmpHeaderPi:
        '''Gets the header processing instruction.'''
        raise NotImplementedError()
    
    @property
    def meta(self) -> aspose.imaging.xmp.XmpMeta:
        '''Gets the XMP meta. Optional.'''
        raise NotImplementedError()
    
    @meta.setter
    def meta(self, value : aspose.imaging.xmp.XmpMeta) -> None:
        '''Gets the XMP meta. Optional.'''
        raise NotImplementedError()
    
    @property
    def trailer_pi(self) -> aspose.imaging.xmp.XmpTrailerPi:
        '''Gets the trailer processing instruction.'''
        raise NotImplementedError()
    
    @property
    def packages(self) -> List[aspose.imaging.xmp.XmpPackage]:
        '''Gets array of :py:class:`aspose.imaging.xmp.XmpPackage` inside XMP.'''
        raise NotImplementedError()
    
    @property
    def packages_count(self) -> int:
        '''Gets amount of packages inside XMP structure.'''
        raise NotImplementedError()
    

class XmpRdfRoot(XmpElementBase):
    '''Represents rdf:RDF element.
    A single XMP packet shall be serialized using a single rdf:RDF XML element. The rdf:RDF element content shall consist of only zero or more rdf:Description elements.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpRdfRoot` class.'''
        raise NotImplementedError()
    
    def add_attribute(self, attribute : str, value : str) -> None:
        '''Adds the attribute.
        
        :param attribute: The attribute.
        :param value: The value.'''
        raise NotImplementedError()
    
    def get_attribute(self, attribute : str) -> str:
        '''Gets the attribute.
        
        :param attribute: The attribute.
        :returns: Returns the attribute for specified attribute name.'''
        raise NotImplementedError()
    
    def clear_attributes(self) -> None:
        '''Removes all attributes.'''
        raise NotImplementedError()
    
    def equals(self, other : aspose.imaging.xmp.XmpElementBase) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    
    def register_namespace_uri(self, prefix : str, namespace_uri : str) -> None:
        '''Adds namespace uri by prefix. Prefix may start without xmlns.
        
        :param prefix: The prefix.
        :param namespace_uri: Package schema uri.'''
        raise NotImplementedError()
    
    def get_namespace_uri(self, prefix : str) -> str:
        '''Gets namespace URI by specific prefix. Prefix may start without xmlns.
        
        :param prefix: The prefix.
        :returns: Returns a package schema URI.'''
        raise NotImplementedError()
    
    def get_xml_value(self) -> str:
        '''Converts xmp value to the xml representation.
        
        :returns: Returns XMP value converted to XML string.'''
        raise NotImplementedError()
    

class XmpTrailerPi(IXmlValue):
    '''Represents XMP trailer processing instruction.'''
    
    @overload
    def __init__(self, is_writable : bool) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpTrailerPi` class.
        
        :param is_writable: Inditacates whether trailer is writable.'''
        raise NotImplementedError()
    
    @overload
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.XmpTrailerPi` class.'''
        raise NotImplementedError()
    
    def get_xml_value(self) -> str:
        '''Converts xmp value to the xml representation.
        
        :returns: Returns XML representation of XMP.'''
        raise NotImplementedError()
    
    def equals(self, other : aspose.imaging.xmp.XmpTrailerPi) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    
    @property
    def is_writable(self) -> bool:
        '''Gets a value indicating whether this instance is writable.'''
        raise NotImplementedError()
    
    @is_writable.setter
    def is_writable(self, value : bool) -> None:
        '''Sets a value indicating whether this instance is writable.'''
        raise NotImplementedError()
    

class XmpArrayType(enum.Enum):
    UNORDERED = enum.auto()
    '''The unordered array.'''
    ORDERED = enum.auto()
    '''The ordered array.'''
    ALTERNATIVE = enum.auto()
    '''The alternative array.'''

