"""The namespace contains EXIF enumerations."""
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

class ExifColorSpace(enum.Enum):
    S_RGB = enum.auto()
    '''SRGB color space.'''
    ADOBE_RGB = enum.auto()
    '''Adobe rgb color space.'''
    UNCALIBRATED = enum.auto()
    '''Uncalibrated color space.'''

class ExifContrast(enum.Enum):
    NORMAL = enum.auto()
    '''Normal contrast.'''
    LOW = enum.auto()
    '''Low contrast.'''
    HIGH = enum.auto()
    '''High contrast.'''

class ExifCustomRendered(enum.Enum):
    NORMAL_PROCESS = enum.auto()
    '''Normal render process.'''
    CUSTOM_PROCESS = enum.auto()
    '''Custom render process.'''

class ExifExposureMode(enum.Enum):
    AUTO = enum.auto()
    '''Auto exposure.'''
    MANUAL = enum.auto()
    '''Manual exposure.'''
    AUTO_BRACKET = enum.auto()
    '''Auto bracket.'''

class ExifExposureProgram(enum.Enum):
    NOTDEFINED = enum.auto()
    '''Not defined.'''
    MANUAL = enum.auto()
    '''Manual program.'''
    AUTO = enum.auto()
    '''Auto exposure.'''
    APERTUREPRIORITY = enum.auto()
    '''Aperture priority.'''
    SHUTTERPRIORITY = enum.auto()
    '''Shutter priority.'''
    CREATIVEPROGRAM = enum.auto()
    '''Creative program.'''
    ACTIONPROGRAM = enum.auto()
    '''Action program.'''
    PORTRAITMODE = enum.auto()
    '''Portrait mode.'''
    LANDSCAPEMODE = enum.auto()
    '''Landscape mode.'''

class ExifFileSource(enum.Enum):
    OTHERS = enum.auto()
    '''The others.'''
    FILM_SCANNER = enum.auto()
    '''Film scanner.'''
    REFLEXION_PRINT_SCANNER = enum.auto()
    '''Reflexion print scanner.'''
    DIGITAL_STILL_CAMERA = enum.auto()
    '''Digital still camera.'''

class ExifFlash(enum.Enum):
    NOFLASH = enum.auto()
    '''No flash fired.'''
    FIRED = enum.auto()
    '''Flash fired.'''
    FIRED_RETURN_LIGHT_NOT_DETECTED = enum.auto()
    '''Flash fired, return light not detected.'''
    FIRED_RETURN_LIGHT_DETECTED = enum.auto()
    '''Flash fired, return light detected.'''
    YES_COMPULSORY = enum.auto()
    '''Flash fired, compulsory flash mode.'''
    YES_COMPULSORY_RETURN_LIGHT_NOT_DETECTED = enum.auto()
    '''Flash fired, compulsory mode, return light not detected.'''
    YES_COMPULSORY_RETURN_LIGHT_DETECTED = enum.auto()
    '''Flash fired, compulsory mode, return light detected.'''
    NO_COMPULSORY = enum.auto()
    '''Flash did not fire, compulsory flash mode.'''
    NO_DID_NOT_FIRE_RETURN_LIGHT_NOT_DETECTED = enum.auto()
    '''Flash did not fire, return light not detected.'''
    NO_AUTO = enum.auto()
    '''Flash did not fire, auto mode.'''
    YES_AUTO = enum.auto()
    '''Flash firedm auto mode.'''
    YES_AUTO_RETURN_LIGHT_NOT_DETECTED = enum.auto()
    '''Flash fired, auto mode, return light not detected.'''
    YES_AUTO_RETURN_LIGHT_DETECTED = enum.auto()
    '''Flash fired, auto mode, return light detected.'''
    NO_FLASH_FUNCTION = enum.auto()
    '''No flash function.'''

class ExifGPSAltitudeRef(enum.Enum):
    ABOVE_SEA_LEVEL = enum.auto()
    '''Above sea level.'''
    BELOW_SEA_LEVEL = enum.auto()
    '''Below sea level.'''

class ExifGainControl(enum.Enum):
    NONE = enum.auto()
    '''No gain control.'''
    LOW_GAIN_UP = enum.auto()
    '''Low gain up.'''
    HIGH_GAIN_UP = enum.auto()
    '''High gain up.'''
    LOW_GAIN_DOWN = enum.auto()
    '''Low gain down.'''
    HIGH_GAIN_DOWN = enum.auto()
    '''High gain down.'''

class ExifLightSource(enum.Enum):
    UNKNOWN = enum.auto()
    '''The unknown.'''
    DAYLIGHT = enum.auto()
    '''The daylight.'''
    FLUORESCENT = enum.auto()
    '''The fluorescent.'''
    TUNGSTEN = enum.auto()
    '''The tungsten.'''
    FLASH = enum.auto()
    '''The flash.'''
    FINEWEATHER = enum.auto()
    '''The fineweather.'''
    CLOUDYWEATHER = enum.auto()
    '''The cloudyweather.'''
    SHADE = enum.auto()
    '''The shade.'''
    DAYLIGHT_FLUORESCENT = enum.auto()
    '''The daylight fluorescent.'''
    DAY_WHITE_FLUORESCENT = enum.auto()
    '''The day white fluorescent.'''
    COOL_WHITE_FLUORESCENT = enum.auto()
    '''The cool white fluorescent.'''
    WHITE_FLUORESCENT = enum.auto()
    '''The white fluorescent.'''
    STANDARDLIGHT_A = enum.auto()
    '''The standardlight a.'''
    STANDARDLIGHT_B = enum.auto()
    '''The standardlight b.'''
    STANDARDLIGHT_C = enum.auto()
    '''The standardlight c.'''
    D55 = enum.auto()
    '''The d55 value(5500K).'''
    D65 = enum.auto()
    '''The d65 value(6500K).'''
    D75 = enum.auto()
    '''The d75 value(7500K).'''
    D50 = enum.auto()
    '''The d50 value(5000K).'''
    IS_OSTUDIOTUNGSTEN = enum.auto()
    '''The iso studio tungsten lightsource.'''
    OTHERLIGHTSOURCE = enum.auto()
    '''The otherlightsource.'''

class ExifMeteringMode(enum.Enum):
    UNKNOWN = enum.auto()
    '''Undefined mode'''
    AVERAGE = enum.auto()
    '''Average metering'''
    CENTERWEIGHTEDAVERAGE = enum.auto()
    '''Center weighted average.'''
    SPOT = enum.auto()
    '''Spot metering'''
    MULTI_SPOT = enum.auto()
    '''Multi spot metering'''
    MULTI_SEGMENT = enum.auto()
    '''Multi segment metering.'''
    PARTIAL = enum.auto()
    '''Partial metering.'''
    OTHER = enum.auto()
    '''For other modes.'''

class ExifOrientation(enum.Enum):
    TOP_LEFT = enum.auto()
    '''Top left. Default orientation.'''
    TOP_RIGHT = enum.auto()
    '''Top right. Horizontally reversed.'''
    BOTTOM_RIGHT = enum.auto()
    '''Bottom right. Rotated by 180 degrees.'''
    BOTTOM_LEFT = enum.auto()
    '''Bottom left. Rotated by 180 degrees and then horizontally reversed.'''
    LEFT_TOP = enum.auto()
    '''Left top. Rotated by 90 degrees counterclockwise and then horizontally reversed.'''
    RIGHT_TOP = enum.auto()
    '''Right top. Rotated by 90 degrees clockwise.'''
    RIGHT_BOTTOM = enum.auto()
    '''Right bottom. Rotated by 90 degrees clockwise and then horizontally reversed.'''
    LEFT_BOTTOM = enum.auto()
    '''Left bottom. Rotated by 90 degrees counterclockwise.'''

class ExifSaturation(enum.Enum):
    NORMAL = enum.auto()
    '''Normal saturation.'''
    LOW = enum.auto()
    '''Low saturation.'''
    HIGH = enum.auto()
    '''High saturation.'''

class ExifSceneCaptureType(enum.Enum):
    STANDARD = enum.auto()
    '''Standard scene.'''
    LANDSCAPE = enum.auto()
    '''Landscape scene.'''
    PORTRAIT = enum.auto()
    '''Portrait scene.'''
    NIGHT_SCENE = enum.auto()
    '''Night scene.'''

class ExifSensingMethod(enum.Enum):
    NOTDEFINED = enum.auto()
    '''Not defined.'''
    ONE_CHIP_COLOR_AREA = enum.auto()
    '''One chip color area.'''
    TWO_CHIP_COLOR_AREA = enum.auto()
    '''Two chip color area.'''
    THREE_CHIP_COLOR_AREA = enum.auto()
    '''Three chip color area.'''
    COLORSEQUENTIALAREA = enum.auto()
    '''Color Sequential area.'''
    TRILINEARSENSOR = enum.auto()
    '''Trilinear sensor.'''
    COLORSEQUENTIALLINEAR = enum.auto()
    '''Color sequential linear sensor.'''

class ExifSubjectDistanceRange(enum.Enum):
    UNKNOWN = enum.auto()
    '''Unknown subject distance range'''
    MACRO = enum.auto()
    '''Macro range'''
    CLOSE_VIEW = enum.auto()
    '''Close view.'''
    DISTANT_VIEW = enum.auto()
    '''Distant view.'''

class ExifUnit(enum.Enum):
    NONE = enum.auto()
    '''Undefined units'''
    INCH = enum.auto()
    '''Inch units'''
    CM = enum.auto()
    '''Metric centimeter units'''

class ExifWhiteBalance(enum.Enum):
    AUTO = enum.auto()
    '''Auto white balance'''
    MANUAL = enum.auto()
    '''Manual  white balance'''

class ExifYCbCrPositioning(enum.Enum):
    CENTERED = enum.auto()
    '''Centered YCbCr'''
    CO_SITED = enum.auto()
    '''Co-sited position'''

