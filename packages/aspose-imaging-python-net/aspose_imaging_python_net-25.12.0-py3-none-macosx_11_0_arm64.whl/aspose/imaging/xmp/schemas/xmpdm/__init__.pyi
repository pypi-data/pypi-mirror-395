"""The namespace contains XMP related helper classes, constants and methods used by the Adobe dynamic media group."""
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

class AudioChannelType:
    '''Represents audio channel type.'''
    
    @staticmethod
    @property
    def mono() -> aspose.imaging.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the mono audio channel.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def stereo() -> aspose.imaging.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the stereo audio channel.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def audio51() -> aspose.imaging.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the 5.1 audio channel.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def audio71() -> aspose.imaging.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the 7.1 audio channel.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def audio_16_channel() -> aspose.imaging.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the 16 audio channel.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def other_channel() -> aspose.imaging.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the other channel.'''
        raise NotImplementedError()


class AudioSampleType:
    '''Represents Audio sample type in :py:class:`aspose.imaging.xmp.schemas.xmpdm.XmpDynamicMediaPackage`.'''
    
    @staticmethod
    @property
    def sample_8_int() -> aspose.imaging.xmp.schemas.xmpdm.AudioSampleType:
        '''Represents 8Int audio sample.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def sample_16_int() -> aspose.imaging.xmp.schemas.xmpdm.AudioSampleType:
        '''Represents 16Int audio sample.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def sample_24_int() -> aspose.imaging.xmp.schemas.xmpdm.AudioSampleType:
        '''Represents 24Int audio sample.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def sample_32_int() -> aspose.imaging.xmp.schemas.xmpdm.AudioSampleType:
        '''Represents 32Int audio sample.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def sample_32_float() -> aspose.imaging.xmp.schemas.xmpdm.AudioSampleType:
        '''Represents 32Float audio sample.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def compressed() -> aspose.imaging.xmp.schemas.xmpdm.AudioSampleType:
        '''Represents Compressed audio sample.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def packed() -> aspose.imaging.xmp.schemas.xmpdm.AudioSampleType:
        '''Represents Packed audio sample.'''
        raise NotImplementedError()


class ProjectLink(aspose.imaging.xmp.types.XmpTypeBase):
    '''Represents path of the project.'''
    
    def __init__(self) -> None:
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: Returns string containing xmp representation.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones this instance.
        
        :returns: A memberwise clone.'''
        raise NotImplementedError()
    
    @property
    def path(self) -> str:
        '''Gets full path to the project.'''
        raise NotImplementedError()
    
    @path.setter
    def path(self, value : str) -> None:
        '''Sets full path to the project.'''
        raise NotImplementedError()
    
    @property
    def type(self) -> aspose.imaging.xmp.schemas.xmpdm.ProjectType:
        '''Gets file type.'''
        raise NotImplementedError()
    
    @type.setter
    def type(self, value : aspose.imaging.xmp.schemas.xmpdm.ProjectType) -> None:
        '''Sets file type.'''
        raise NotImplementedError()
    

class Time(aspose.imaging.xmp.types.XmpTypeBase):
    '''Representation of a time value in seconds.'''
    
    def __init__(self, scale : aspose.imaging.xmp.types.derived.Rational, value : int) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.schemas.xmpdm.Time` class.
        
        :param scale: The scale.
        :param value: The value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones this instance.
        
        :returns: A memberwise clone.'''
        raise NotImplementedError()
    
    @property
    def scale(self) -> aspose.imaging.xmp.types.derived.Rational:
        '''Gets scale for the time value.'''
        raise NotImplementedError()
    
    @scale.setter
    def scale(self, value : aspose.imaging.xmp.types.derived.Rational) -> None:
        '''Sets scale for the time value.'''
        raise NotImplementedError()
    
    @property
    def value(self) -> int:
        '''Gets time value in the specified scale.'''
        raise NotImplementedError()
    
    @value.setter
    def value(self, value : int) -> None:
        '''Sets time value in the specified scale.'''
        raise NotImplementedError()
    

class TimeFormat:
    '''Represents time format in :py:class:`aspose.imaging.xmp.schemas.xmpdm.Timecode`.'''
    
    def equals(self, other : aspose.imaging.xmp.schemas.xmpdm.TimeFormat) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def timecode24() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode24.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def timecode25() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode25.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def drop_timecode2997() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the drop timecode2997.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def non_drop_timecode2997() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the non drop timecode2997.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def timecode30() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode30.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def timecode50() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode50.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def drop_timecode5994() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the drop timecode5994.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def non_drop_timecode5994() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the non drop timecode5994.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def timecode60() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode60.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def timecode23976() -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode23976.'''
        raise NotImplementedError()


class Timecode(aspose.imaging.xmp.types.XmpTypeBase):
    '''Represents timecode value in video.'''
    
    def __init__(self, format : aspose.imaging.xmp.schemas.xmpdm.TimeFormat, time_value : str) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.schemas.xmpdm.Timecode` class.
        
        :param format: The time format.
        :param time_value: The time value.'''
        raise NotImplementedError()
    
    def get_xmp_representation(self) -> str:
        '''Returns the string contained value in XMP format.
        
        :returns: Returns the string containing xmp representation.'''
        raise NotImplementedError()
    
    def clone(self) -> Any:
        '''Clones this instance.
        
        :returns: A memberwise clone.'''
        raise NotImplementedError()
    
    def equals(self, other : aspose.imaging.xmp.schemas.xmpdm.Timecode) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        raise NotImplementedError()
    
    @property
    def format(self) -> aspose.imaging.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the format used in the :py:attr:`aspose.imaging.xmp.schemas.xmpdm.Timecode.time_value`.'''
        raise NotImplementedError()
    
    @format.setter
    def format(self, value : aspose.imaging.xmp.schemas.xmpdm.TimeFormat) -> None:
        '''Sets the format used in the :py:attr:`aspose.imaging.xmp.schemas.xmpdm.Timecode.time_value`.'''
        raise NotImplementedError()
    
    @property
    def time_value(self) -> str:
        '''Gets the time value in the specified format.'''
        raise NotImplementedError()
    
    @time_value.setter
    def time_value(self, value : str) -> None:
        '''Sets the time value in the specified format.'''
        raise NotImplementedError()
    

class XmpDynamicMediaPackage(aspose.imaging.xmp.XmpPackage):
    '''Represents XMP Dynamic Media namespace.'''
    
    def __init__(self) -> None:
        '''Initializes a new instance of the :py:class:`aspose.imaging.xmp.schemas.xmpdm.XmpDynamicMediaPackage` class.'''
        raise NotImplementedError()
    
    @overload
    def add_value(self, key : str, value : str) -> None:
        '''Adds string property.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The string value.'''
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
    
    def set_abs_peak_audio_file_path(self, uri : str) -> None:
        '''Sets the absolute peak audio file path.
        
        :param uri: The absolute path to the file’s peak audio file.'''
        raise NotImplementedError()
    
    def set_alblum(self, album : str) -> None:
        '''Sets the alblum.
        
        :param album: The album.'''
        raise NotImplementedError()
    
    def set_alt_tape_name(self, alt_tape_name : str) -> None:
        '''Sets the alternative tape name.
        
        :param alt_tape_name: Alternative tape name.'''
        raise NotImplementedError()
    
    def set_alt_time_code(self, timecode : aspose.imaging.xmp.schemas.xmpdm.Timecode) -> None:
        '''Sets the alternative time code.
        
        :param timecode: Time code.'''
        raise NotImplementedError()
    
    def set_artist(self, artist : str) -> None:
        '''Sets the artist.
        
        :param artist: The artist.'''
        raise NotImplementedError()
    
    def set_audio_channel_type(self, audio_channel_type : aspose.imaging.xmp.schemas.xmpdm.AudioChannelType) -> None:
        '''Sets the audio channel type.
        
        :param audio_channel_type: Audio channel type.'''
        raise NotImplementedError()
    
    def set_audio_sample_rate(self, rate : int) -> None:
        '''Sets the audio sample rate.
        
        :param rate: The audio sample rate.'''
        raise NotImplementedError()
    
    def set_audio_sample_type(self, audio_sample_type : aspose.imaging.xmp.schemas.xmpdm.AudioSampleType) -> None:
        '''Sets the audio sample type.
        
        :param audio_sample_type: The audio sample type.'''
        raise NotImplementedError()
    
    def set_camera_angle(self, camera_angle : str) -> None:
        '''Sets the camera angle.
        
        :param camera_angle: The camera angle.'''
        raise NotImplementedError()
    
    def set_camera_label(self, camera_label : str) -> None:
        '''Sets the camera label.
        
        :param camera_label: The camera label.'''
        raise NotImplementedError()
    
    def set_camera_move(self, camera_move : str) -> None:
        '''Sets the camera move.
        
        :param camera_move: The camera move.'''
        raise NotImplementedError()
    
    def set_client(self, client : str) -> None:
        '''Sets the client.
        
        :param client: The client.'''
        raise NotImplementedError()
    
    def set_comment(self, comment : str) -> None:
        '''Sets the comment.
        
        :param comment: The comment.'''
        raise NotImplementedError()
    
    def set_composer(self, composer : str) -> None:
        '''Sets the composer.
        
        :param composer: The composer.'''
        raise NotImplementedError()
    
    def set_director(self, director : str) -> None:
        '''Sets the director.
        
        :param director: The director.'''
        raise NotImplementedError()
    
    def set_director_photography(self, director_photography : str) -> None:
        '''Sets the director of photography.
        
        :param director_photography: The director of photography.'''
        raise NotImplementedError()
    
    def set_duration(self, duration : aspose.imaging.xmp.schemas.xmpdm.Time) -> None:
        '''Sets the duration.
        
        :param duration: The duration.'''
        raise NotImplementedError()
    
    def set_engineer(self, engineer : str) -> None:
        '''Sets the engineer.
        
        :param engineer: The engineer.'''
        raise NotImplementedError()
    
    def set_file_data_rate(self, rate : aspose.imaging.xmp.types.derived.Rational) -> None:
        '''Sets the file data rate.
        
        :param rate: The file data rate in megabytes per second.'''
        raise NotImplementedError()
    
    def set_genre(self, genre : str) -> None:
        '''Sets the genre.
        
        :param genre: The genre.'''
        raise NotImplementedError()
    
    def set_good(self, good : bool) -> None:
        '''Sets the good.
        
        :param good: if set to ``true`` a shot is a keeper.'''
        raise NotImplementedError()
    
    def set_instrument(self, instrument : str) -> None:
        '''Sets the instrument.
        
        :param instrument: The instrument.'''
        raise NotImplementedError()
    
    def set_intro_time(self, intro_time : aspose.imaging.xmp.schemas.xmpdm.Time) -> None:
        '''Sets the intro time.
        
        :param intro_time: The intro time.'''
        raise NotImplementedError()
    
    def set_key(self, key : str) -> None:
        '''Sets the audio’s musical key.
        
        :param key: The audio’s musical key. One of: C, C#, D, D#, E, F, F#, G, G#, A, A#, and B.'''
        raise NotImplementedError()
    
    def set_log_comment(self, comment : str) -> None:
        '''Sets the user\'s log comment.
        
        :param comment: The comment.'''
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
    

class ProjectType(enum.Enum):
    MOVIE = enum.auto()
    '''The movie project type'''
    STILL = enum.auto()
    '''The still project type'''
    AUDIO = enum.auto()
    '''The audio project type'''
    CUSTOM = enum.auto()
    '''The custom project type'''

