"""The namespace handles Cdr file format processing."""
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

class CdrArrow(CdrDictionaryItem):
    '''The cdr arrow'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.fileformats.cdr.types.PointD]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.fileformats.cdr.types.PointD]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    
    @property
    def point_types(self) -> List[int]:
        '''Gets the point types.'''
        raise NotImplementedError()
    
    @point_types.setter
    def point_types(self, value : List[int]) -> None:
        '''Sets the point types.'''
        raise NotImplementedError()
    

class CdrArtisticText(CdrGraphicObject):
    '''The cdr Artistic text'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    
    @property
    def bounds_in_pixels(self) -> aspose.imaging.RectangleF:
        '''Gets the bounds in pixels.'''
        raise NotImplementedError()
    
    @bounds_in_pixels.setter
    def bounds_in_pixels(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounds in pixels.'''
        raise NotImplementedError()
    
    @property
    def clip_id(self) -> int:
        '''Gets the clip identifier.'''
        raise NotImplementedError()
    
    @clip_id.setter
    def clip_id(self, value : int) -> None:
        '''Sets the clip identifier.'''
        raise NotImplementedError()
    
    @property
    def origin(self) -> aspose.imaging.fileformats.cdr.types.PointD:
        '''Gets the origin.'''
        raise NotImplementedError()
    
    @origin.setter
    def origin(self, value : aspose.imaging.fileformats.cdr.types.PointD) -> None:
        '''Sets the origin.'''
        raise NotImplementedError()
    
    @property
    def text_index(self) -> int:
        '''Gets the index of the text.'''
        raise NotImplementedError()
    
    @text_index.setter
    def text_index(self, value : int) -> None:
        '''Sets the index of the text.'''
        raise NotImplementedError()
    

class CdrBbox(CdrObjectContainer):
    '''The cdr box'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @property
    def x0(self) -> float:
        '''Gets the x0.'''
        raise NotImplementedError()
    
    @x0.setter
    def x0(self, value : float) -> None:
        '''Sets the x0.'''
        raise NotImplementedError()
    
    @property
    def y0(self) -> float:
        '''Gets the y0.'''
        raise NotImplementedError()
    
    @y0.setter
    def y0(self, value : float) -> None:
        '''Sets the y0.'''
        raise NotImplementedError()
    
    @property
    def x1(self) -> float:
        '''Gets the x1.'''
        raise NotImplementedError()
    
    @x1.setter
    def x1(self, value : float) -> None:
        '''Sets the x1.'''
        raise NotImplementedError()
    
    @property
    def y1(self) -> float:
        '''Gets the y1.'''
        raise NotImplementedError()
    
    @y1.setter
    def y1(self, value : float) -> None:
        '''Sets the y1.'''
        raise NotImplementedError()
    
    @property
    def x(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @property
    def y(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the height.'''
        raise NotImplementedError()
    

class CdrBmp(CdrDictionaryItem):
    '''he cdr bmp'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def color_model(self) -> int:
        '''Gets the color model.'''
        raise NotImplementedError()
    
    @color_model.setter
    def color_model(self, value : int) -> None:
        '''Sets the color model.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    
    @property
    def bpp(self) -> int:
        '''Gets the BPP.'''
        raise NotImplementedError()
    
    @bpp.setter
    def bpp(self, value : int) -> None:
        '''Sets the BPP.'''
        raise NotImplementedError()
    
    @property
    def bytes_per_line(self) -> int:
        '''Gets the bytes per line.'''
        raise NotImplementedError()
    
    @bytes_per_line.setter
    def bytes_per_line(self, value : int) -> None:
        '''Sets the bytes per line.'''
        raise NotImplementedError()
    
    @property
    def palette(self) -> List[int]:
        '''Gets the palette.'''
        raise NotImplementedError()
    
    @palette.setter
    def palette(self, value : List[int]) -> None:
        '''Sets the palette.'''
        raise NotImplementedError()
    

class CdrCurve(CdrGraphicObject):
    '''The cdr curve'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    
    @property
    def bounds_in_pixels(self) -> aspose.imaging.RectangleF:
        '''Gets the bounds in pixels.'''
        raise NotImplementedError()
    
    @bounds_in_pixels.setter
    def bounds_in_pixels(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounds in pixels.'''
        raise NotImplementedError()
    
    @property
    def clip_id(self) -> int:
        '''Gets the clip identifier.'''
        raise NotImplementedError()
    
    @clip_id.setter
    def clip_id(self, value : int) -> None:
        '''Sets the clip identifier.'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.fileformats.cdr.types.PointD]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.fileformats.cdr.types.PointD]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    
    @property
    def point_types(self) -> List[int]:
        '''Gets the point types.'''
        raise NotImplementedError()
    
    @point_types.setter
    def point_types(self, value : List[int]) -> None:
        '''Sets the point types.'''
        raise NotImplementedError()
    

class CdrDictionaryItem(CdrObject):
    '''The cdr dictionary item'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    

class CdrDisp(CdrObjectContainer):
    '''The cdr Disp'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    

class CdrDocument(CdrObjectContainer):
    '''The cdr root object'''
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @property
    def texts(self) -> aspose.imaging.fileformats.cdr.types.CdrTextCollection:
        '''Gets the texts.'''
        raise NotImplementedError()
    
    @property
    def clip_ids(self) -> List[int]:
        '''Gets the clip ids.'''
        raise NotImplementedError()
    
    @clip_ids.setter
    def clip_ids(self, value : List[int]) -> None:
        '''Sets the clip ids.'''
        raise NotImplementedError()
    
    @property
    def last_text_index(self) -> int:
        '''Gets the text indexes.'''
        raise NotImplementedError()
    
    @last_text_index.setter
    def last_text_index(self, value : int) -> None:
        '''Gets the text indexes.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    

class CdrEllipse(CdrGraphicObject):
    '''The cdr Ellipse'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    
    @property
    def bounds_in_pixels(self) -> aspose.imaging.RectangleF:
        '''Gets the bounds in pixels.'''
        raise NotImplementedError()
    
    @bounds_in_pixels.setter
    def bounds_in_pixels(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounds in pixels.'''
        raise NotImplementedError()
    
    @property
    def clip_id(self) -> int:
        '''Gets the clip identifier.'''
        raise NotImplementedError()
    
    @clip_id.setter
    def clip_id(self, value : int) -> None:
        '''Sets the clip identifier.'''
        raise NotImplementedError()
    
    @property
    def angle1(self) -> float:
        '''Gets the angle1.'''
        raise NotImplementedError()
    
    @angle1.setter
    def angle1(self, value : float) -> None:
        '''Sets the angle1.'''
        raise NotImplementedError()
    
    @property
    def angle2(self) -> float:
        '''Gets the angle2.'''
        raise NotImplementedError()
    
    @angle2.setter
    def angle2(self, value : float) -> None:
        '''Sets the angle2.'''
        raise NotImplementedError()
    
    @property
    def pie(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrEllipse` is pie.'''
        raise NotImplementedError()
    
    @pie.setter
    def pie(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrEllipse` is pie.'''
        raise NotImplementedError()
    

class CdrFill(CdrDictionaryItem):
    '''The cdr fill'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def fill_type(self) -> aspose.imaging.fileformats.cdr.enum.CdrFillType:
        '''Gets the type of the fill.'''
        raise NotImplementedError()
    
    @fill_type.setter
    def fill_type(self, value : aspose.imaging.fileformats.cdr.enum.CdrFillType) -> None:
        '''Sets the type of the fill.'''
        raise NotImplementedError()
    
    @property
    def color1(self) -> aspose.imaging.fileformats.cdr.types.CdrColor:
        '''Gets the color1.'''
        raise NotImplementedError()
    
    @color1.setter
    def color1(self, value : aspose.imaging.fileformats.cdr.types.CdrColor) -> None:
        '''Sets the color1.'''
        raise NotImplementedError()
    
    @property
    def color2(self) -> aspose.imaging.fileformats.cdr.types.CdrColor:
        '''Gets the color2.'''
        raise NotImplementedError()
    
    @color2.setter
    def color2(self, value : aspose.imaging.fileformats.cdr.types.CdrColor) -> None:
        '''Sets the color2.'''
        raise NotImplementedError()
    
    @property
    def gradient(self) -> aspose.imaging.fileformats.cdr.types.CdrGradient:
        '''Gets the gradient.'''
        raise NotImplementedError()
    
    @gradient.setter
    def gradient(self, value : aspose.imaging.fileformats.cdr.types.CdrGradient) -> None:
        '''Sets the gradient.'''
        raise NotImplementedError()
    
    @property
    def image_fill(self) -> aspose.imaging.fileformats.cdr.types.CdrImageFill:
        '''Gets the image fill.'''
        raise NotImplementedError()
    
    @image_fill.setter
    def image_fill(self, value : aspose.imaging.fileformats.cdr.types.CdrImageFill) -> None:
        '''Sets the image fill.'''
        raise NotImplementedError()
    

class CdrFillTransform(CdrObjectContainer):
    '''the cdr fill transform'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @property
    def transform(self) -> aspose.imaging.Matrix:
        '''Gets the transform.'''
        raise NotImplementedError()
    
    @transform.setter
    def transform(self, value : aspose.imaging.Matrix) -> None:
        '''Sets the transform.'''
        raise NotImplementedError()
    

class CdrFlgs(CdrObject):
    '''The cdr flags'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> int:
        '''Gets the value.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : int) -> None:
        '''Sets the value.'''
        raise NotImplementedError()
    

class CdrFont(CdrDictionaryItem):
    '''the cdr Font'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def font_name(self) -> str:
        '''Gets the name of the font.'''
        raise NotImplementedError()
    
    @font_name.setter
    def font_name(self, value : str) -> None:
        '''Sets the name of the font.'''
        raise NotImplementedError()
    
    @property
    def encoding(self) -> int:
        '''Gets the encoding.'''
        raise NotImplementedError()
    
    @encoding.setter
    def encoding(self, value : int) -> None:
        '''Sets the encoding.'''
        raise NotImplementedError()
    

class CdrGraphicObject(CdrObject):
    '''The cdr graphic object'''
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    
    @property
    def bounds_in_pixels(self) -> aspose.imaging.RectangleF:
        '''Gets the bounds in pixels.'''
        raise NotImplementedError()
    
    @bounds_in_pixels.setter
    def bounds_in_pixels(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounds in pixels.'''
        raise NotImplementedError()
    
    @property
    def clip_id(self) -> int:
        '''Gets the clip identifier.'''
        raise NotImplementedError()
    
    @clip_id.setter
    def clip_id(self, value : int) -> None:
        '''Sets the clip identifier.'''
        raise NotImplementedError()
    

class CdrIcc(CdrObjectContainer):
    '''The cdr Icc profile'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    

class CdrListObjects(CdrObjectContainer):
    '''The cdr list objects'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.cdr.objects.CdrListObjects` class.'''
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @property
    def page_width(self) -> float:
        '''Gets the width of the page.'''
        raise NotImplementedError()
    
    @page_width.setter
    def page_width(self, value : float) -> None:
        '''Sets the width of the page.'''
        raise NotImplementedError()
    
    @property
    def page_height(self) -> float:
        '''Gets the height of the page.'''
        raise NotImplementedError()
    
    @page_height.setter
    def page_height(self, value : float) -> None:
        '''Sets the height of the page.'''
        raise NotImplementedError()
    
    @property
    def fill_id(self) -> int:
        '''Gets the fill identifier.'''
        raise NotImplementedError()
    
    @fill_id.setter
    def fill_id(self, value : int) -> None:
        '''Sets the fill identifier.'''
        raise NotImplementedError()
    
    @property
    def opacity_fill_id(self) -> int:
        '''Gets the opacity fill identifier.'''
        raise NotImplementedError()
    
    @opacity_fill_id.setter
    def opacity_fill_id(self, value : int) -> None:
        '''Sets the opacity fill identifier.'''
        raise NotImplementedError()
    
    @property
    def out_line_id(self) -> int:
        '''Gets the out line identifier.'''
        raise NotImplementedError()
    
    @out_line_id.setter
    def out_line_id(self, value : int) -> None:
        '''Sets the out line identifier.'''
        raise NotImplementedError()
    
    @property
    def style_id(self) -> int:
        '''Gets the style identifier.'''
        raise NotImplementedError()
    
    @style_id.setter
    def style_id(self, value : int) -> None:
        '''Sets the style identifier.'''
        raise NotImplementedError()
    
    @property
    def opacity(self) -> float:
        '''Gets the opacity.'''
        raise NotImplementedError()
    
    @opacity.setter
    def opacity(self, value : float) -> None:
        '''Sets the opacity.'''
        raise NotImplementedError()
    

class CdrMcfg(CdrObject):
    '''The cdr configuration object'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    

class CdrObject(aspose.imaging.DisposableObject):
    '''The cdr object'''
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    

class CdrObjectContainer(CdrObject):
    '''The cdr object container'''
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    

class CdrOutline(CdrDictionaryItem):
    '''The cdr out line'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def line_type(self) -> int:
        '''Gets the type of the line.'''
        raise NotImplementedError()
    
    @line_type.setter
    def line_type(self, value : int) -> None:
        '''Sets the type of the line.'''
        raise NotImplementedError()
    
    @property
    def caps_type(self) -> int:
        '''Gets the type of the caps.'''
        raise NotImplementedError()
    
    @caps_type.setter
    def caps_type(self, value : int) -> None:
        '''Sets the type of the caps.'''
        raise NotImplementedError()
    
    @property
    def join_type(self) -> int:
        '''Gets the type of the join.'''
        raise NotImplementedError()
    
    @join_type.setter
    def join_type(self, value : int) -> None:
        '''Sets the type of the join.'''
        raise NotImplementedError()
    
    @property
    def line_width(self) -> float:
        '''Gets the width of the line.'''
        raise NotImplementedError()
    
    @line_width.setter
    def line_width(self, value : float) -> None:
        '''Sets the width of the line.'''
        raise NotImplementedError()
    
    @property
    def stretch(self) -> float:
        '''Gets the stretch.'''
        raise NotImplementedError()
    
    @stretch.setter
    def stretch(self, value : float) -> None:
        '''Sets the stretch.'''
        raise NotImplementedError()
    
    @property
    def aangle(self) -> float:
        '''Gets the angle.'''
        raise NotImplementedError()
    
    @aangle.setter
    def aangle(self, value : float) -> None:
        '''Sets the angle.'''
        raise NotImplementedError()
    
    @property
    def color(self) -> aspose.imaging.fileformats.cdr.types.CdrColor:
        '''Gets the color.'''
        raise NotImplementedError()
    
    @color.setter
    def color(self, value : aspose.imaging.fileformats.cdr.types.CdrColor) -> None:
        '''Sets the color.'''
        raise NotImplementedError()
    
    @property
    def dash_array(self) -> List[int]:
        '''Gets the dash array.'''
        raise NotImplementedError()
    
    @dash_array.setter
    def dash_array(self, value : List[int]) -> None:
        '''Sets the dash array.'''
        raise NotImplementedError()
    
    @property
    def start_marker_id(self) -> int:
        '''Gets the start marker identifier.'''
        raise NotImplementedError()
    
    @start_marker_id.setter
    def start_marker_id(self, value : int) -> None:
        '''Sets the start marker identifier.'''
        raise NotImplementedError()
    
    @property
    def end_marker_id(self) -> int:
        '''Gets the end marker identifier.'''
        raise NotImplementedError()
    
    @end_marker_id.setter
    def end_marker_id(self, value : int) -> None:
        '''Sets the end marker identifier.'''
        raise NotImplementedError()
    

class CdrPage(CdrObjectContainer):
    '''The cdr page'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    

class CdrParagraph(CdrGraphicObject):
    '''The cdr Paragraph'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    
    @property
    def bounds_in_pixels(self) -> aspose.imaging.RectangleF:
        '''Gets the bounds in pixels.'''
        raise NotImplementedError()
    
    @bounds_in_pixels.setter
    def bounds_in_pixels(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounds in pixels.'''
        raise NotImplementedError()
    
    @property
    def clip_id(self) -> int:
        '''Gets the clip identifier.'''
        raise NotImplementedError()
    
    @clip_id.setter
    def clip_id(self, value : int) -> None:
        '''Sets the clip identifier.'''
        raise NotImplementedError()
    
    @property
    def text_index(self) -> int:
        '''Gets the index of the text.'''
        raise NotImplementedError()
    
    @text_index.setter
    def text_index(self, value : int) -> None:
        '''Sets the index of the text.'''
        raise NotImplementedError()
    

class CdrPathObject(CdrGraphicObject):
    '''The Cdr path'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    
    @property
    def bounds_in_pixels(self) -> aspose.imaging.RectangleF:
        '''Gets the bounds in pixels.'''
        raise NotImplementedError()
    
    @bounds_in_pixels.setter
    def bounds_in_pixels(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounds in pixels.'''
        raise NotImplementedError()
    
    @property
    def clip_id(self) -> int:
        '''Gets the clip identifier.'''
        raise NotImplementedError()
    
    @clip_id.setter
    def clip_id(self, value : int) -> None:
        '''Sets the clip identifier.'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.fileformats.cdr.types.PointD]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.fileformats.cdr.types.PointD]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    
    @property
    def point_types(self) -> List[int]:
        '''Gets the point types.'''
        raise NotImplementedError()
    
    @point_types.setter
    def point_types(self, value : List[int]) -> None:
        '''Sets the point types.'''
        raise NotImplementedError()
    

class CdrPattern(CdrDictionaryItem):
    '''The cdr bitmap'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> int:
        '''Gets the width.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : int) -> None:
        '''Sets the width.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> int:
        '''Gets the height.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : int) -> None:
        '''Sets the height.'''
        raise NotImplementedError()
    

class CdrPolygon(CdrGraphicObject):
    '''The cdr polygon'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    
    @property
    def bounds_in_pixels(self) -> aspose.imaging.RectangleF:
        '''Gets the bounds in pixels.'''
        raise NotImplementedError()
    
    @bounds_in_pixels.setter
    def bounds_in_pixels(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounds in pixels.'''
        raise NotImplementedError()
    
    @property
    def clip_id(self) -> int:
        '''Gets the clip identifier.'''
        raise NotImplementedError()
    
    @clip_id.setter
    def clip_id(self, value : int) -> None:
        '''Sets the clip identifier.'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.fileformats.cdr.types.PointD]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.fileformats.cdr.types.PointD]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    
    @property
    def point_types(self) -> List[int]:
        '''Gets the point types.'''
        raise NotImplementedError()
    
    @point_types.setter
    def point_types(self, value : List[int]) -> None:
        '''Sets the point types.'''
        raise NotImplementedError()
    

class CdrPolygonTransform(CdrObjectContainer):
    '''The polygon transform'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @property
    def x_radius(self) -> float:
        '''Gets the x radius.'''
        raise NotImplementedError()
    
    @x_radius.setter
    def x_radius(self, value : float) -> None:
        '''Sets the x radius.'''
        raise NotImplementedError()
    
    @property
    def y_radius(self) -> float:
        '''Gets the y radius.'''
        raise NotImplementedError()
    
    @y_radius.setter
    def y_radius(self, value : float) -> None:
        '''Sets the y radius.'''
        raise NotImplementedError()
    
    @property
    def position(self) -> aspose.imaging.fileformats.cdr.types.PointD:
        '''Gets the position.'''
        raise NotImplementedError()
    
    @position.setter
    def position(self, value : aspose.imaging.fileformats.cdr.types.PointD) -> None:
        '''Sets the position.'''
        raise NotImplementedError()
    
    @property
    def num_angles(self) -> int:
        '''Gets the number angles.'''
        raise NotImplementedError()
    
    @num_angles.setter
    def num_angles(self, value : int) -> None:
        '''Sets the number angles.'''
        raise NotImplementedError()
    
    @property
    def next_point(self) -> int:
        '''Gets the next point.'''
        raise NotImplementedError()
    
    @next_point.setter
    def next_point(self, value : int) -> None:
        '''Sets the next point.'''
        raise NotImplementedError()
    

class CdrPpdt(CdrGraphicObject):
    '''The cdr knot vector object'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    
    @property
    def bounds_in_pixels(self) -> aspose.imaging.RectangleF:
        '''Gets the bounds in pixels.'''
        raise NotImplementedError()
    
    @bounds_in_pixels.setter
    def bounds_in_pixels(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounds in pixels.'''
        raise NotImplementedError()
    
    @property
    def clip_id(self) -> int:
        '''Gets the clip identifier.'''
        raise NotImplementedError()
    
    @clip_id.setter
    def clip_id(self, value : int) -> None:
        '''Sets the clip identifier.'''
        raise NotImplementedError()
    
    @property
    def points(self) -> List[aspose.imaging.fileformats.cdr.types.PointD]:
        '''Gets the points.'''
        raise NotImplementedError()
    
    @points.setter
    def points(self, value : List[aspose.imaging.fileformats.cdr.types.PointD]) -> None:
        '''Sets the points.'''
        raise NotImplementedError()
    
    @property
    def knot_vecor(self) -> List[int]:
        '''Gets the knot vecors.'''
        raise NotImplementedError()
    
    @knot_vecor.setter
    def knot_vecor(self, value : List[int]) -> None:
        '''Sets the knot vecors.'''
        raise NotImplementedError()
    

class CdrRectangle(CdrGraphicObject):
    '''The cdr rectangle'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def width(self) -> float:
        '''Gets the x.'''
        raise NotImplementedError()
    
    @width.setter
    def width(self, value : float) -> None:
        '''Sets the x.'''
        raise NotImplementedError()
    
    @property
    def height(self) -> float:
        '''Gets the y.'''
        raise NotImplementedError()
    
    @height.setter
    def height(self, value : float) -> None:
        '''Sets the y.'''
        raise NotImplementedError()
    
    @property
    def bounds_in_pixels(self) -> aspose.imaging.RectangleF:
        '''Gets the bounds in pixels.'''
        raise NotImplementedError()
    
    @bounds_in_pixels.setter
    def bounds_in_pixels(self, value : aspose.imaging.RectangleF) -> None:
        '''Sets the bounds in pixels.'''
        raise NotImplementedError()
    
    @property
    def clip_id(self) -> int:
        '''Gets the clip identifier.'''
        raise NotImplementedError()
    
    @clip_id.setter
    def clip_id(self, value : int) -> None:
        '''Sets the clip identifier.'''
        raise NotImplementedError()
    
    @property
    def r3(self) -> float:
        '''Gets the r3.'''
        raise NotImplementedError()
    
    @r3.setter
    def r3(self, value : float) -> None:
        '''Sets the r3.'''
        raise NotImplementedError()
    
    @property
    def r2(self) -> float:
        '''Gets the r2.'''
        raise NotImplementedError()
    
    @r2.setter
    def r2(self, value : float) -> None:
        '''Sets the r2.'''
        raise NotImplementedError()
    
    @property
    def r1(self) -> float:
        '''Gets the r1.'''
        raise NotImplementedError()
    
    @r1.setter
    def r1(self, value : float) -> None:
        '''Sets the r1.'''
        raise NotImplementedError()
    
    @property
    def r0(self) -> float:
        '''Gets the r0.'''
        raise NotImplementedError()
    
    @r0.setter
    def r0(self, value : float) -> None:
        '''Sets the r0.'''
        raise NotImplementedError()
    
    @property
    def corner_type(self) -> int:
        '''Gets the type of the corner.'''
        raise NotImplementedError()
    
    @corner_type.setter
    def corner_type(self, value : int) -> None:
        '''Sets the type of the corner.'''
        raise NotImplementedError()
    
    @property
    def scale_x(self) -> float:
        '''Gets the scale x.'''
        raise NotImplementedError()
    
    @scale_x.setter
    def scale_x(self, value : float) -> None:
        '''Sets the scale x.'''
        raise NotImplementedError()
    
    @property
    def scale_y(self) -> float:
        '''Gets the scale y.'''
        raise NotImplementedError()
    
    @scale_y.setter
    def scale_y(self, value : float) -> None:
        '''Sets the scale y.'''
        raise NotImplementedError()
    

class CdrSpnd(CdrDictionaryItem):
    '''The cdr span'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> int:
        '''Gets the value.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : int) -> None:
        '''Sets the value.'''
        raise NotImplementedError()
    

class CdrStyd(CdrObjectContainer):
    '''The cdr style'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    

class CdrStyle(CdrDictionaryItem):
    '''The cdr style'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def copy(self) -> aspose.imaging.fileformats.cdr.objects.CdrStyle:
        '''Copies this instance.
        
        :returns: The current style copy'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def font_name(self) -> str:
        '''Gets the name of the font.'''
        raise NotImplementedError()
    
    @font_name.setter
    def font_name(self, value : str) -> None:
        '''Sets the name of the font.'''
        raise NotImplementedError()
    
    @property
    def charset(self) -> int:
        '''Gets the character set.'''
        raise NotImplementedError()
    
    @charset.setter
    def charset(self, value : int) -> None:
        '''Sets the character set.'''
        raise NotImplementedError()
    
    @property
    def font_size(self) -> float:
        '''Gets the size of the font.'''
        raise NotImplementedError()
    
    @font_size.setter
    def font_size(self, value : float) -> None:
        '''Sets the size of the font.'''
        raise NotImplementedError()
    
    @property
    def font_weight(self) -> int:
        '''Gets the font weight.'''
        raise NotImplementedError()
    
    @font_weight.setter
    def font_weight(self, value : int) -> None:
        '''Sets the font weight.'''
        raise NotImplementedError()
    
    @property
    def fill(self) -> aspose.imaging.fileformats.cdr.objects.CdrFill:
        '''Gets the fill.'''
        raise NotImplementedError()
    
    @fill.setter
    def fill(self, value : aspose.imaging.fileformats.cdr.objects.CdrFill) -> None:
        '''Sets the fill.'''
        raise NotImplementedError()
    
    @property
    def out_line(self) -> aspose.imaging.fileformats.cdr.objects.CdrOutline:
        '''Gets the out line.'''
        raise NotImplementedError()
    
    @out_line.setter
    def out_line(self, value : aspose.imaging.fileformats.cdr.objects.CdrOutline) -> None:
        '''Sets the out line.'''
        raise NotImplementedError()
    
    @property
    def align(self) -> int:
        '''Gets the align.'''
        raise NotImplementedError()
    
    @align.setter
    def align(self, value : int) -> None:
        '''Sets the align.'''
        raise NotImplementedError()
    
    @property
    def right_indent(self) -> float:
        '''Gets the right indent.'''
        raise NotImplementedError()
    
    @right_indent.setter
    def right_indent(self, value : float) -> None:
        '''Sets the right indent.'''
        raise NotImplementedError()
    
    @property
    def first_indent(self) -> float:
        '''Gets the first indent.'''
        raise NotImplementedError()
    
    @first_indent.setter
    def first_indent(self, value : float) -> None:
        '''Sets the first indent.'''
        raise NotImplementedError()
    
    @property
    def left_indent(self) -> float:
        '''Gets the left indent.'''
        raise NotImplementedError()
    
    @left_indent.setter
    def left_indent(self, value : float) -> None:
        '''Sets the left indent.'''
        raise NotImplementedError()
    
    @property
    def parent_id(self) -> int:
        '''Gets the parent identifier.'''
        raise NotImplementedError()
    
    @parent_id.setter
    def parent_id(self, value : int) -> None:
        '''Sets the parent identifier.'''
        raise NotImplementedError()
    

class CdrText(CdrDictionaryItem):
    '''The cdr text'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.cdr.objects.CdrText` class.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.
        For legacy compatibility'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.
        For legacy compatibility'''
        raise NotImplementedError()
    
    @property
    def text(self) -> str:
        '''Gets the CDR text boxes.'''
        raise NotImplementedError()
    
    @text.setter
    def text(self, value : str) -> None:
        '''Sets the CDR text boxes.'''
        raise NotImplementedError()
    
    @property
    def char_descriptors(self) -> List[int]:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.cdr.objects.CdrText` class.'''
        raise NotImplementedError()
    
    @char_descriptors.setter
    def char_descriptors(self, value : List[int]) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.fileformats.cdr.objects.CdrText` class.'''
        raise NotImplementedError()
    
    @property
    def styles(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrStyle]:
        '''Adds the text box.'''
        raise NotImplementedError()
    
    @styles.setter
    def styles(self, value : List[aspose.imaging.fileformats.cdr.objects.CdrStyle]) -> None:
        '''Adds the text box.'''
        raise NotImplementedError()
    
    @property
    def style_id(self) -> int:
        '''Gets the style identifier.'''
        raise NotImplementedError()
    
    @style_id.setter
    def style_id(self, value : int) -> None:
        '''Sets the style identifier.'''
        raise NotImplementedError()
    

class CdrTransforms(CdrObject):
    '''The cdr transforms object'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def transforms(self) -> List[aspose.imaging.Matrix]:
        '''Gets the transforms.'''
        raise NotImplementedError()
    
    @transforms.setter
    def transforms(self, value : List[aspose.imaging.Matrix]) -> None:
        '''Sets the transforms.'''
        raise NotImplementedError()
    

class CdrUdta(CdrObjectContainer):
    '''The cdr udta'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    

class CdrUserPalette(CdrObjectContainer):
    '''The cdr user palette'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    

class CdrVectorPattern(CdrDictionaryItem):
    '''The cdr vector pattern'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        raise NotImplementedError()
    
    @id.setter
    def id(self, value : int) -> None:
        '''Sets the identifier.'''
        raise NotImplementedError()
    
    @property
    def data(self) -> List[int]:
        '''Gets the data.'''
        raise NotImplementedError()
    
    @data.setter
    def data(self, value : List[int]) -> None:
        '''Sets the data.'''
        raise NotImplementedError()
    

class CdrVersion(CdrObjectContainer):
    '''The cdr Version'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def add_child_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Adds the child object.
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    def insert_object(self, cdr_object : aspose.imaging.fileformats.cdr.objects.CdrObject) -> None:
        '''Inserts the object
        
        :param cdr_object: The CDR object.'''
        raise NotImplementedError()
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        raise NotImplementedError()
    
    @property
    def parent(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the parent.'''
        raise NotImplementedError()
    
    @parent.setter
    def parent(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the parent.'''
        raise NotImplementedError()
    
    @property
    def document(self) -> aspose.imaging.fileformats.cdr.objects.CdrDocument:
        '''Gets the document.'''
        raise NotImplementedError()
    
    @document.setter
    def document(self, value : aspose.imaging.fileformats.cdr.objects.CdrDocument) -> None:
        '''Sets the document.'''
        raise NotImplementedError()
    
    @property
    def childs(self) -> List[aspose.imaging.fileformats.cdr.objects.CdrObject]:
        '''Gets the objects.'''
        raise NotImplementedError()
    
    @property
    def load_to_last_child(self) -> bool:
        '''Gets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @load_to_last_child.setter
    def load_to_last_child(self, value : bool) -> None:
        '''Sets a value indicating whether [load to last child].'''
        raise NotImplementedError()
    
    @property
    def last_child(self) -> aspose.imaging.fileformats.cdr.objects.CdrObjectContainer:
        '''Gets the last child.'''
        raise NotImplementedError()
    
    @last_child.setter
    def last_child(self, value : aspose.imaging.fileformats.cdr.objects.CdrObjectContainer) -> None:
        '''Sets the last child.'''
        raise NotImplementedError()
    
    @property
    def hidden(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @hidden.setter
    def hidden(self, value : bool) -> None:
        '''Sets a value indicating whether this :py:class:`aspose.imaging.fileformats.cdr.objects.CdrObjectContainer` is visible.'''
        raise NotImplementedError()
    
    @property
    def version(self) -> int:
        '''Gets the version.'''
        raise NotImplementedError()
    
    @version.setter
    def version(self, value : int) -> None:
        '''Sets the version.'''
        raise NotImplementedError()
    

