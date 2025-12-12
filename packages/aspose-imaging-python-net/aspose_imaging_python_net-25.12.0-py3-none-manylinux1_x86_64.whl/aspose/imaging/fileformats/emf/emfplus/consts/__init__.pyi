"""The namespace contains types [MS-EMFPLUS]: Enhanced Metafile Format Plus Extensions
            2.1 EMF+ Constants"""
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

class EmfPlusImageEffectsIdentifiers:
    '''The ImageEffects identifiers define standard GUIDs for specifying graphics image effects. These identifiers are used by device drivers to publish their levels of support for these effects. The identifier constants are defined using the GUID curly-braced string representation ([MS-DTYP] section 2.3.4.3).'''
    
    @staticmethod
    def contain(object_guid : str) -> bool:
        '''Contains the specified object unique identifier.
        
        :param object_guid: The object unique identifier.
        :returns: True if contain.'''
        raise NotImplementedError()
    
    @staticmethod
    @property
    def BLUR_EFFECT_GUID() -> str:
        '''Specifies the blur effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def BRIGHTNESS_CONTRAST_EFFECT_GUID() -> str:
        '''Specifies the brightness contrast effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def COLOR_BALANCE_EFFECT_GUID() -> str:
        '''Specifies the color balance effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def COLOR_CURVE_EFFECT_GUID() -> str:
        '''Specifies the color curve effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def COLOR_LOOKUP_TABLE_EFFECT_GUID() -> str:
        '''Specifies the color lookup table effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def COLOR_MATRIX_EFFECT_GUID() -> str:
        '''Specifies the color matrix effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def HUE_SATURATION_LIGHTNESS_EFFECT_GUID() -> str:
        '''Specifies the hue saturation lightness effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def LEVELS_EFFECT_GUID() -> str:
        '''Specifies the levels effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def RED_EYE_CORRECTION_EFFECT_GUID() -> str:
        '''Specifies the red-eye correction effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def SHARPEN_EFFECT_GUID() -> str:
        '''Specifies the sharpen effect.'''
        raise NotImplementedError()

    @staticmethod
    @property
    def TINT_EFFECT_GUID() -> str:
        '''Specifies the tint effect.'''
        raise NotImplementedError()


class EmfPlusBitmapDataType(enum.Enum):
    BITMAP_DATA_TYPE_PIXEL = enum.auto()
    '''Specifies a bitmap image with pixel data.'''
    BITMAP_DATA_TYPE_COMPRESSED = enum.auto()
    '''Specifies an image with compressed data.'''

class EmfPlusBrushDataFlags(enum.Enum):
    BRUSH_DATA_PATH = enum.auto()
    '''This flag is meaningful in :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPathGradientBrushData` objects (section 2.2.2.29).
    If set, an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBoundaryPathData` object (section 2.2.2.6) MUST be specified in the BoundaryData field of the brush data object.
    If clear, an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBoundaryPointData` object (section 2.2.2.7) MUST be specified in the BoundaryData field of the brush data object.'''
    BRUSH_DATA_TRANSFORM = enum.auto()
    '''This flag is meaningful in :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusLinearGradientBrushData` objects (section 2.2.2.24), :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPathGradientBrushData` objects, and :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusTextureBrushData` objects (section 2.2.2.45).
    If set, a 2x3 world space to device space transform matrix MUST be specified in the OptionalData field of the brush data object.'''
    BRUSH_DATA_PRESET_COLORS = enum.auto()
    '''This flag is meaningful in EmfPlusLinearGradientBrushData and EmfPlusPathGradientBrushData objects.
    If set, an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBlendColors` object (section 2.2.2.4) MUST be specified in the OptionalData field of the brush data object.'''
    BRUSH_DATA_BLEND_FACTORS_H = enum.auto()
    '''This flag is meaningful in EmfPlusLinearGradientBrushData and EmfPlusPathGradientBrushData objects.
    If set, an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBlendFactors` object (section 2.2.2.5) that specifies a blend pattern along a horizontal gradient MUST be specified in the OptionalData field of the brush data object.'''
    BRUSH_DATA_BLEND_FACTORS_V = enum.auto()
    '''This flag is meaningful in EmfPlusLinearGradientBrushData objects.
    If set, an EmfPlusBlendFactors object that specifies a blend pattern along a vertical gradient MUST be specified in the OptionalData field of the brush data object.'''
    BRUSH_DATA_FOCUS_SCALES = enum.auto()
    '''This flag is meaningful in EmfPlusPathGradientBrushData objects.
    If set, an:py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusFocusScaleData` object (section 2.2.2.18) MUST be specified in the OptionalData field of the brush data object.'''
    BRUSH_DATA_IS_GAMMA_CORRECTED = enum.auto()
    '''This flag is meaningful in EmfPlusLinearGradientBrushData, EmfPlusPathGradientBrushData, and EmfPlusTextureBrushData objects.
    If set, the brush MUST already be gamma corrected; that is, output brightness and intensity have been corrected to match the input image.'''
    BRUSH_DATA_DO_NOT_TRANSFORM = enum.auto()
    '''This flag is meaningful in EmfPlusTextureBrushData objects.
    If set, a world space to device space transform SHOULD NOT be applied to the texture brush.'''

class EmfPlusBrushType(enum.Enum):
    BRUSH_TYPE_SOLID_COLOR = enum.auto()
    '''Specifies a solid-color brush, which is characterized by an EmfPlusArgb value.'''
    BRUSH_TYPE_HATCH_FILL = enum.auto()
    '''Specifies a hatch brush, which is characterized by a predefined pattern.'''
    BRUSH_TYPE_TEXTURE_FILL = enum.auto()
    '''Specifies a texture brush, which is characterized by an image.'''
    BRUSH_TYPE_PATH_GRADIENT = enum.auto()
    '''Specifies a path gradient brush, which is characterized by a color gradient path gradient brush data.'''
    BRUSH_TYPE_LINEAR_GRADIENT = enum.auto()
    '''contains linear gradient brush data.'''

class EmfPlusCombineMode(enum.Enum):
    COMBINE_MODE_REPLACE = enum.auto()
    '''Replaces the existing region with the new region.'''
    COMBINE_MODE_INTERSECT = enum.auto()
    '''Replaces the existing region with the intersection of the existing region and the new region.'''
    COMBINE_MODE_UNION = enum.auto()
    '''Replaces the existing region with the union of the existing and new regions.'''
    COMBINE_MODE_XOR = enum.auto()
    '''Replaces the existing region with the XOR of the existing and new regions.'''
    COMBINE_MODE_EXCLUDE = enum.auto()
    '''Replaces the existing region with the part of itself that is not in the new region.'''
    COMBINE_MODE_COMPLEMENT = enum.auto()
    '''Replaces the existing region with the part of the new region that is not in the existing region.'''

class EmfPlusCompositingMode(enum.Enum):
    COMPOSITING_MODE_SOURCE_OVER = enum.auto()
    '''Enables alpha blending, which specifies that when a color is rendered, it is blended with the background color. The extent of blending is determined by the value of the alpha component of the color being rendered.'''
    COMPOSITING_MODE_SOURCE_COPY = enum.auto()
    '''Disables alpha blending, which means that when a source color is rendered, it overwrites the background color.'''

class EmfPlusCompositingQuality(enum.Enum):
    COMPOSITING_QUALITY_DEFAULT = enum.auto()
    '''No gamma correction is performed. Gamma correction controls the overall brightness and contrast of an image. Without gamma correction, composited images can appear too light or too dark.'''
    COMPOSITING_QUALITY_HIGH_SPEED = enum.auto()
    '''No gamma correction is performed. Compositing speed is favored at the expense of quality. In terms of the result, there is no difference between this value and CompositingQualityDefault.'''
    COMPOSITING_QUALITY_HIGH_QUALITY = enum.auto()
    '''Gamma correction is performed. Compositing quality is favored at the expense of speed.'''
    COMPOSITING_QUALITY_GAMMA_CORRECTED = enum.auto()
    '''Enable gamma correction for higher-quality compositing with lower speed. In terms of the result, there is no difference between this value and CompositingQualityHighQuality.'''
    COMPOSITING_QUALITY_ASSUME_LINEAR = enum.auto()
    '''No gamma correction is performed; however, using linear values results in better quality than the default at a slightly lower speed.'''

class EmfPlusCurveAdjustments(enum.Enum):
    ADJUST_EXPOSURE = enum.auto()
    '''Specifies the simulation of increasing or decreasing the exposure of an image.'''
    ADJUST_DENSITY = enum.auto()
    '''Specifies the simulation of increasing or decreasing the density of an image.'''
    ADJUST_CONTRAST = enum.auto()
    '''Specifies an increase or decrease of the contrast of an image.'''
    ADJUST_HIGHLIGHT = enum.auto()
    '''Specifies an increase or decrease of the value of a color channel of an image, if that channel already has a value that is above half intensity. This adjustment can be used to increase definition in the light areas of an image without affecting the dark areas.'''
    ADJUST_SHADOW = enum.auto()
    '''Specifies an increase or decrease of the value of a color channel of an image, if that channel already has a value that is below half intensity. This adjustment can be used to increase definition in the dark areas of an image without affecting the light areas.'''
    ADJUST_MIDTONE = enum.auto()
    '''Specifies an adjustment that lightens or darkens an image. Color channel values in the middle of the intensity range are altered more than color channel values near the minimum or maximum extremes of intensity. This adjustment can be used to lighten or darken an image without losing the contrast between the darkest and lightest parts of the image.'''
    ADJUST_WHITE_SATURATION = enum.auto()
    '''Specifies an adjustment to the white saturation of an image, defined as the maximum value in the range of intensities for a given color channel, whose range is typically 0 to 255.'''
    ADJUST_BLACK_SATURATION = enum.auto()
    '''Specifies an adjustment to the black saturation of an image, which is the minimum value in the range of intensities for a given color channel, which is typically 0 to 255.'''

class EmfPlusCurveChannel(enum.Enum):
    CURVE_CHANNEL_ALL = enum.auto()
    '''Specifies that a color curve adjustment applies to all color channels.'''
    CURVE_CHANNEL_RED = enum.auto()
    '''Specifies that a color curve adjustment applies only to the red color channel.'''
    CURVE_CHANNEL_GREEN = enum.auto()
    '''Specifies that a color curve adjustment applies only to the green color channel.'''
    CURVE_CHANNEL_BLUE = enum.auto()
    '''Specifies that a color curve adjustment applies only to the blue color channel.'''

class EmfPlusCustomLineCapDataFlags(enum.Enum):
    CUSTOM_LINE_CAP_DATA_FILL_PATH = enum.auto()
    '''If set, an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusFillPath` object MUST be specified in the OptionalData field of the :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomLineCapData` object for filling the custom line cap.'''
    CUSTOM_LINE_CAP_DATA_LINE_PATH = enum.auto()
    '''If set, an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusLinePath` object MUST be specified in the OptionalData field of the EmfPlusCustomLineCapData object for outlining the custom line cap.'''

class EmfPlusCustomLineCapDataType(enum.Enum):
    CUSTOM_LINE_CAP_DATA_TYPE_DEFAULT = enum.auto()
    '''Specifies a default custom line cap.'''
    CUSTOM_LINE_CAP_DATA_TYPE_ADJUSTABLE_ARROW = enum.auto()
    '''Specifies an adjustable arrow custom line cap.'''

class EmfPlusDashedLineCapType(enum.Enum):
    DASHED_LINE_CAP_TYPE_FLAT = enum.auto()
    '''Specifies a flat dashed line cap.'''
    DASHED_LINE_CAP_TYPE_ROUND = enum.auto()
    '''Specifies a round dashed line cap.'''
    DASHED_LINE_CAP_TYPE_TRIANGLE = enum.auto()
    '''Specifies a triangular dashed line cap.'''

class EmfPlusDriverStringOptionsFlags(enum.Enum):
    DRIVER_STRING_OPTIONS_CMAP_LOOKUP = enum.auto()
    '''If set, the positions of character glyphs SHOULD be specified in a character map lookup table.
    If clear, the glyph positions SHOULD be obtained from an array of coordinates.'''
    DRIVER_STRING_OPTIONS_VERTICAL = enum.auto()
    '''If set, the string SHOULD be rendered vertically.
    If clear, the string SHOULD be rendered horizontally.'''
    DRIVER_STRING_OPTIONS_REALIZED_ADVANCE = enum.auto()
    '''If set, character glyph positions SHOULD be calculated relative to the position of the first glyph.
    If clear, the glyph positions SHOULD be obtained from an array of coordinates.'''
    DRIVER_STRING_OPTIONS_LIMIT_SUBPIXEL = enum.auto()
    '''If set, less memory SHOULD be used to cache anti-aliased glyphs, which produces lower quality text rendering.
    If clear, more memory SHOULD be used, which produces higher quality text rendering.'''

class EmfPlusFilterType(enum.Enum):
    FILTER_TYPE_NONE = enum.auto()
    '''Specifies that filtering is not performed.'''
    FILTER_TYPE_POINT = enum.auto()
    '''Specifies that each destination pixel is computed by sampling the nearest pixel from the source image.'''
    FILTER_TYPE_LINEAR = enum.auto()
    '''Specifies that linear interpolation is performed using the weighted average of a 2x2 area of pixels surrounding the source pixel.'''
    FILTER_TYPE_TRIANGLE = enum.auto()
    '''Specifies that each pixel in the source image contributes equally to the destination image. This is the slowest of filtering algorithms.'''
    FILTER_TYPE_BOX = enum.auto()
    '''Specifies a box filter algorithm, in which each destination pixel is computed by averaging a rectangle of source pixels. This algorithm is useful only when reducing the size of an image.'''
    FILTER_TYPE_PYRAMIDAL_QUAD = enum.auto()
    '''Specifies that a 4-sample tent filter is used.'''
    FILTER_TYPE_GAUSSIAN_QUAD = enum.auto()
    '''Specifies that a 4-sample Gaussian filter is used, which creates a blur effect on an image.'''

class EmfPlusFontStyleFlags(enum.Enum):
    FONT_STYLE_BOLD = enum.auto()
    '''If set, the font typeface MUST be rendered with a heavier weight or thickness.
    If clear, the font typeface MUST be rendered with a normal thickness.'''
    FONT_STYLE_ITALIC = enum.auto()
    '''If set, the font typeface MUST be rendered with the vertical stems of the characters at an increased angle or slant relative to the baseline.
    If clear, the font typeface MUST be rendered with the vertical stems of the characters at a normal angle.'''
    FONT_STYLE_UNDERLINE = enum.auto()
    '''If set, the font typeface MUST be rendered with a line underneath the baseline of the characters.
    If clear, the font typeface MUST be rendered without a line underneath the baseline.'''
    FONT_STYLE_STRIKEOUT = enum.auto()
    '''If set, the font typeface MUST be rendered with a line parallel to the baseline drawn through the middle of the characters.
    If clear, the font typeface MUST be rendered without a line through the characters.'''

class EmfPlusGraphicsVersionEnum(enum.Enum):
    GRAPHICS_VERSION1 = enum.auto()
    '''Specifies GDI+ version 1.0'''
    GRAPHICS_VERSION_1_1 = enum.auto()
    '''Specifies GDI+ version 1.1'''

class EmfPlusHatchStyle(enum.Enum):
    HATCH_STYLE_HORIZONTAL = enum.auto()
    '''Specifies equally spaced horizontal lines.'''
    HATCH_STYLE_VERTICAL = enum.auto()
    '''Specifies equally spaced vertical lines.'''
    HATCH_STYLE_FORWARD_DIAGONAL = enum.auto()
    '''Specifies lines on a diagonal from upper left to lower right.'''
    HATCH_STYLE_BACKWARD_DIAGONAL = enum.auto()
    '''Specifies lines on a diagonal from upper right to lower left.'''
    HATCH_STYLE_LARGE_GRID = enum.auto()
    '''Specifies crossing horizontal and vertical lines.'''
    HATCH_STYLE_DIAGONAL_CROSS = enum.auto()
    '''Specifies crossing forward diagonal and backward diagonal lines with anti-aliasing.'''
    HATCH_STYLE_05_PERCENT = enum.auto()
    '''Specifies a 5-percent hatch, which is the ratio of foreground color to background color equal to 5:100.'''
    HATCH_STYLE_10_PERCENT = enum.auto()
    '''Specifies a 10-percent hatch, which is the ratio of foreground color to background color equal to 10:100.'''
    HATCH_STYLE_20_PERCENT = enum.auto()
    '''Specifies a 20-percent hatch, which is the ratio of foreground color to background color equal to 20:100.'''
    HATCH_STYLE_25_PERCENT = enum.auto()
    '''Specifies a 20-percent hatch, which is the ratio of foreground color to background color equal to 20:100.'''
    HATCH_STYLE_30_PERCENT = enum.auto()
    '''Specifies a 30-percent hatch, which is the ratio of foreground color to background color equal to 30:100.'''
    HATCH_STYLE_40_PERCENT = enum.auto()
    '''Specifies a 40-percent hatch, which is the ratio of foreground color to background color equal to 40:100.'''
    HATCH_STYLE_50_PERCENT = enum.auto()
    '''Specifies a 50-percent hatch, which is the ratio of foreground color to background color equal to 50:100.'''
    HATCH_STYLE_60_PERCENT = enum.auto()
    '''Specifies a 60-percent hatch, which is the ratio of foreground color to background color equal to 60:100.'''
    HATCH_STYLE_70_PERCENT = enum.auto()
    '''Specifies a 70-percent hatch, which is the ratio of foreground color to background color equal to 70:100.'''
    HATCH_STYLE_75_PERCENT = enum.auto()
    '''Specifies a 75-percent hatch, which is the ratio of foreground color to background color equal to 75:100.'''
    HATCH_STYLE_80_PERCENT = enum.auto()
    '''Specifies an 80-percent hatch, which is the ratio of foreground color to background color equal to 80:100.'''
    HATCH_STYLE_90_PERCENT = enum.auto()
    '''Specifies a 90-percent hatch, which is the ratio of foreground color to background color equal to 90:100.'''
    HATCH_STYLE_LIGHT_DOWNWARD_DIAGONAL = enum.auto()
    '''Specifies diagonal lines that slant to the right from top to bottom points with no anti-aliasing. They are spaced 50 percent further apart than lines in the HatchStyleForwardDiagonal pattern'''
    HATCH_STYLE_LIGHT_UPWARD_DIAGONAL = enum.auto()
    '''Specifies diagonal lines that slant to the left from top to bottom points with no anti-aliasing. They are spaced 50 percent further apart than lines in the HatchStyleBackwardDiagonal pattern.'''
    HATCH_STYLE_DARK_DOWNWARD_DIAGONAL = enum.auto()
    '''Specifies diagonal lines that slant to the right from top to bottom points with no anti-aliasing. They are spaced 50 percent closer and are twice the width of lines in the HatchStyleForwardDiagonal pattern.'''
    HATCH_STYLE_DARK_UPWARD_DIAGONAL = enum.auto()
    '''Specifies diagonal lines that slant to the left from top to bottom points with no anti-aliasing. They are spaced 50 percent closer and are twice the width of lines in the HatchStyleBackwardDiagonal pattern.'''
    HATCH_STYLE_WIDE_DOWNWARD_DIAGONAL = enum.auto()
    '''Specifies diagonal lines that slant to the right from top to bottom points with no anti-aliasing. They have the same spacing between lines in HatchStyleWideDownwardDiagonal pattern and HatchStyleForwardDiagonal pattern, but HatchStyleWideDownwardDiagonal has the triple line width of HatchStyleForwardDiagonal.'''
    HATCH_STYLE_WIDE_UPWARD_DIAGONAL = enum.auto()
    '''Specifies diagonal lines that slant to the left from top to bottom points with no anti-aliasing. They have the same spacing between lines in HatchStyleWideUpwardDiagonal pattern and HatchStyleBackwardDiagonal pattern, but HatchStyleWideUpwardDiagonal has the triple line width of HatchStyleWideUpwardDiagonal.'''
    HATCH_STYLE_LIGHT_VERTICAL = enum.auto()
    '''Specifies vertical lines that are spaced 50 percent closer together than lines in the HatchStyleVertical pattern.'''
    HATCH_STYLE_LIGHT_HORIZONTAL = enum.auto()
    '''Specifies horizontal lines that are spaced 50 percent closer than lines in the HatchStyleHorizontal pattern.'''
    HATCH_STYLE_NARROW_VERTICAL = enum.auto()
    '''Specifies vertical lines that are spaced 75 percent closer than lines in the HatchStyleVertical pattern; or 25 percent closer than lines in the HatchStyleLightVertical pattern.'''
    HATCH_STYLE_NARROW_HORIZONTAL = enum.auto()
    '''Specifies horizontal lines that are spaced 75 percent closer than lines in the HatchStyleHorizontal pattern; or 25 percent closer than lines in the HatchStyleLightHorizontal pattern.'''
    HATCH_STYLE_DARK_VERTICAL = enum.auto()
    '''Specifies lines that are spaced 50 percent closer than lines in the HatchStyleVertical pattern.'''
    HATCH_STYLE_DARK_HORIZONTAL = enum.auto()
    '''Specifies lines that are spaced 50 percent closer than lines in the HatchStyleHorizontal pattern.'''
    HATCH_STYLE_DASHED_DOWNWARD_DIAGONAL = enum.auto()
    '''Specifies dashed diagonal lines that slant to the right from top to bottom points.'''
    HATCH_STYLE_DASHED_UPWARD_DIAGONAL = enum.auto()
    '''Specifies dashed diagonal lines that slant to the left from top to bottom points.'''
    HATCH_STYLE_DASHED_HORIZONTAL = enum.auto()
    '''Specifies dashed horizontal lines.'''
    HATCH_STYLE_DASHED_VERTICAL = enum.auto()
    '''Specifies dashed vertical lines.'''
    HATCH_STYLE_SMALL_CONFETTI = enum.auto()
    '''Specifies a pattern of lines that has the appearance of confetti.'''
    HATCH_STYLE_LARGE_CONFETTI = enum.auto()
    '''Specifies a pattern of lines that has the appearance of confetti, and is composed of larger pieces than the HatchStyleSmallConfetti pattern.'''
    HATCH_STYLE_ZIG_ZAG = enum.auto()
    '''Specifies horizontal lines that are composed of zigzags.'''
    HATCH_STYLE_WAVE = enum.auto()
    '''Specifies horizontal lines that are composed of tildes.'''
    HATCH_STYLE_DIAGONAL_BRICK = enum.auto()
    '''Specifies a pattern of lines that has the appearance of layered bricks that slant to the left from top to bottom points.'''
    HATCH_STYLE_HORIZONTAL_BRICK = enum.auto()
    '''Specifies a pattern of lines that has the appearance of horizontally layered bricks.'''
    HATCH_STYLE_WEAVE = enum.auto()
    '''Specifies a pattern of lines that has the appearance of a woven material.'''
    HATCH_STYLE_PLAID = enum.auto()
    '''Specifies a pattern of lines that has the appearance of a plaid material.'''
    HATCH_STYLE_DIVOT = enum.auto()
    '''Specifies a pattern of lines that has the appearance of divots.'''
    HATCH_STYLE_DOTTED_GRID = enum.auto()
    '''Specifies crossing horizontal and vertical lines, each of which is composed of dots.'''
    HATCH_STYLE_DOTTED_DIAMOND = enum.auto()
    '''Specifies crossing forward and backward diagonal lines, each of which is composed of dots.'''
    HATCH_STYLE_SHINGLE = enum.auto()
    '''Specifies a pattern of lines that has the appearance of diagonally layered shingles that slant to the right from top to bottom points.'''
    HATCH_STYLE_TRELLIS = enum.auto()
    '''Specifies a pattern of lines that has the appearance of a trellis.'''
    HATCH_STYLE_SPHERE = enum.auto()
    '''Specifies a pattern of lines that has the appearance of spheres laid adjacent to each other.'''
    HATCH_STYLE_SMALL_GRID = enum.auto()
    '''Specifies crossing horizontal and vertical lines that are spaced 50 percent closer together than HatchStyleLargeGrid.'''
    HATCH_STYLE_SMALL_CHECKER_BOARD = enum.auto()
    '''Specifies a pattern of lines that has the appearance of a checkerboard.'''
    HATCH_STYLE_LARGE_CHECKER_BOARD = enum.auto()
    '''Specifies a pattern of lines that has the appearance of a checkerboard, with squares that are twice the size of the squares in the :py:attr:`aspose.imaging.fileformats.emf.emfplus.consts.EmfPlusHatchStyle.HATCH_STYLE_SMALL_CHECKER_BOARD` pattern.'''
    HATCH_STYLE_OUTLINED_DIAMOND = enum.auto()
    '''Specifies crossing forward and backward diagonal lines; the lines are not anti-aliased.'''
    HATCH_STYLE_SOLID_DIAMOND = enum.auto()
    '''Specifies a pattern of lines that has the appearance of a checkerboard placed diagonally.'''

class EmfPlusHotkeyPrefix(enum.Enum):
    HOTKEY_PREFIX_NONE = enum.auto()
    '''Specifies that the hotkey prefix SHOULD NOT be displayed.'''
    HOTKEY_PREFIX_SHOW = enum.auto()
    '''Specifies that no hotkey prefix is defined.'''
    HOTKEY_PREFIX_HIDE = enum.auto()
    '''Specifies that the hotkey prefix SHOULD be displayed.'''

class EmfPlusImageDataType(enum.Enum):
    IMAGE_DATA_TYPE_UNKNOWN = enum.auto()
    '''The type of image is not known.'''
    IMAGE_DATA_TYPE_BITMAP = enum.auto()
    '''Specifies a bitmap image.'''
    IMAGE_DATA_TYPE_METAFILE = enum.auto()
    '''Specifies a metafile image.'''

class EmfPlusInterpolationMode(enum.Enum):
    INTERPOLATION_MODE_DEFAULT = enum.auto()
    '''Specifies the default interpolation mode, which is defined as InterpolationModeBilinear.'''
    INTERPOLATION_MODE_LOW_QUALITY = enum.auto()
    '''Specifies a low-quality interpolation mode, which is defined as InterpolationModeNearestNeighbor.'''
    INTERPOLATION_MODE_HIGH_QUALITY = enum.auto()
    '''Specifies a high-quality interpolation mode, which is defined as InterpolationModeHighQualityBicubic.'''
    INTERPOLATION_MODE_BILINEAR = enum.auto()
    '''Specifies bilinear interpolation, which uses the closest 2x2 neighborhood of known pixels surrounding the interpolated pixel. The weighted average of these 4 known pixel values determines the value to assign to the interpolated pixel. The result is smoother looking than InterpolationModeNearestNeighbor.'''
    INTERPOLATION_MODE_BICUBIC = enum.auto()
    '''Specifies bicubic interpolation, which uses the closest 4x4 neighborhood of known pixels surrounding the interpolated pixel. The weighted average of these 16 known pixel values determines the value to assign to the interpolated pixel. Because the known pixels are likely to be at varying distances from the interpolated pixel, closer pixels are given a higher weight in the calculation. The result is smoother looking than InterpolationModeBilinear.'''
    INTERPOLATION_MODE_NEAREST_NEIGHBOR = enum.auto()
    '''Specifies nearest-neighbor interpolation, which uses only the value of the pixel that is closest to the interpolated pixel. This mode simply duplicates or removes pixels, producing the lowest-quality result among these options.'''
    INTERPOLATION_MODE_HIGH_QUALITY_BILINEAR = enum.auto()
    '''Specifies bilinear interpolation with prefiltering.'''
    INTERPOLATION_MODE_HIGH_QUALITY_BICUBIC = enum.auto()
    '''Specifies bicubic interpolation with prefiltering, which produces the highest-quality result among these options.'''

class EmfPlusLanguageIdentifierType(enum.Enum):
    LANG_NEUTRAL = enum.auto()
    '''Neutral locale language.'''
    ZH_CHS = enum.auto()
    '''Chinese, Simplified (China).'''
    LANG_INVARIANT = enum.auto()
    '''Invariant language.'''
    LANG_NEUTRAL_USER_DEFAULT = enum.auto()
    '''User default locale language.'''
    AR_SA = enum.auto()
    '''Arabic (Saudi Arabia).'''
    BG_BG = enum.auto()
    '''Bulgarian (Bulgaria).'''
    CA_ES = enum.auto()
    '''Catalan (Spain).'''
    ZH_CHT = enum.auto()
    '''Chinese, Traditional (Taiwan).'''
    CS_CZ = enum.auto()
    '''Czech (Czech Republic).'''
    DA_DK = enum.auto()
    '''Danish (Denmark).'''
    DE_DE = enum.auto()
    '''German (Germany).'''
    EL_GR = enum.auto()
    '''Greek (Greece).'''
    EN_US = enum.auto()
    '''English (United States).'''
    ES_TRADNL_ES = enum.auto()
    '''Spanish, Traditional (Spain).'''
    FI_FI = enum.auto()
    '''Finnish (Finland).'''
    FR_FR = enum.auto()
    '''French (France).'''
    HE_IL = enum.auto()
    '''Hebrew (Israel).'''
    HU_HU = enum.auto()
    '''Hungarian (Hungary).'''
    IS_IS = enum.auto()
    '''Icelandic (Iceland).'''
    IT_IT = enum.auto()
    '''Italian (Italy).'''
    JA_JA = enum.auto()
    '''Japanese (Japan).'''
    KO_KR = enum.auto()
    '''Korean (Korea).'''
    NL_NL = enum.auto()
    '''Dutch (Netherlands).'''
    NB_NO = enum.auto()
    '''Bokmal (Norway).'''
    PL_PL = enum.auto()
    '''Polish (Poland).'''
    BR = enum.auto()
    '''Portuguese (Brazil).'''
    RM_CH = enum.auto()
    '''Romansh (Switzerland).'''
    RO_RO = enum.auto()
    '''Romanian (Romania).'''
    RU_RU = enum.auto()
    '''Russian (Russia).'''
    HR_HR = enum.auto()
    '''Croatian (Croatia).'''
    SK_SK = enum.auto()
    '''Slovak (Slovakia).'''
    SQ_AL = enum.auto()
    '''Albanian (Albania).'''
    SV_SE = enum.auto()
    '''Swedish (Sweden).'''
    TH_TH = enum.auto()
    '''Thai (Thailand).'''
    TR_TR = enum.auto()
    '''Turkish (Turkey).'''
    UR_PK = enum.auto()
    '''Urdu (Pakistan).'''
    ID_ID = enum.auto()
    '''Indonesian (Indonesia).'''
    UK_UA = enum.auto()
    '''Ukranian (Ukraine).'''
    BE_BY = enum.auto()
    '''Belarusian (Belarus).'''
    SL_SI = enum.auto()
    '''Slovenian (Slovenia).'''
    ET_EE = enum.auto()
    '''Estonian (Estonia).'''
    LV_LV = enum.auto()
    '''Latvian (Latvia).'''
    LT_LT = enum.auto()
    '''Lithuanian (Lithuania).'''
    TG_TJ = enum.auto()
    '''Tajik (Tajikistan).'''
    FA_IR = enum.auto()
    '''Persian (Iran).'''
    VI_VN = enum.auto()
    '''Vietnamese (Vietnam).'''
    HY_AM = enum.auto()
    '''Armenian (Armenia).'''
    AZ_LATN_AZ = enum.auto()
    '''Azeri, Latin alphabet (Azerbaijan).'''
    EU_ES = enum.auto()
    '''Basque (Spain).'''
    WEN_DE = enum.auto()
    '''Sorbian, Upper (Germany).'''
    MK_MK = enum.auto()
    '''Macedonian (Macedonia).'''
    ST_ZA = enum.auto()
    '''Sutu (South Africa).'''
    TN_ZA = enum.auto()
    '''Setswana (Botswana).'''
    XH_ZA = enum.auto()
    '''isiXhosa (South Africa).'''
    ZU_ZA = enum.auto()
    '''isiZulu (South Africa).'''
    AF_ZA = enum.auto()
    '''Afrikaans (South Africa).'''
    KA_GE = enum.auto()
    '''Georgian (Georgia).'''
    FA_FA = enum.auto()
    '''Faeroese (Faroe Islands).'''
    HI_IN = enum.auto()
    '''Hindi (India).'''
    MT_MT = enum.auto()
    '''Maltese (Malta).'''
    SE_NO = enum.auto()
    '''Sami, Northern (Norway).'''
    GA_GB = enum.auto()
    '''Gaelic (United Kingdom).'''
    MS_MY = enum.auto()
    '''Malay (Malaysia).'''
    KK_KZ = enum.auto()
    '''Kazakh (Kazakhstan).'''
    KY_KG = enum.auto()
    '''Kyrgyz (Kyrgyzstan).'''
    SW_KE = enum.auto()
    '''Kiswahili (Kenya, Tanzania, and other Eastern African nations; and it is the official language of the African Union).'''
    TK_TM = enum.auto()
    '''Turkmen (Turkmenistan).'''
    UZ_LATN_UZ = enum.auto()
    '''Uzbek, Latin alphabet (Uzbekistan).'''
    TT_RU = enum.auto()
    '''Tatar (Belarus, Russia, Ukraine, and other eastern European nations; and Kazakhstan, and Uzbekistan in central Asia).'''
    BN_IN = enum.auto()
    '''Bengali, Bengali script (India).'''
    PA_IN = enum.auto()
    '''Punjabi (India).'''
    GU_IN = enum.auto()
    '''Gujarati (India).'''
    OR_IN = enum.auto()
    '''Oriya (India).'''
    TA_IN = enum.auto()
    '''Tamil (India, Sri Lanka).'''
    TE_IN = enum.auto()
    '''Telugu (India).'''
    KN_IN = enum.auto()
    '''Kannada (India).'''
    ML_IN = enum.auto()
    '''Malayalam (India).'''
    AS_IN = enum.auto()
    '''Assamese (India).'''
    MR_IN = enum.auto()
    '''Marathi (India).'''
    SA_IN = enum.auto()
    '''Sanskrit (India).'''
    MN_MN = enum.auto()
    '''Mongolian, Cyrillic alphabet (Mongolia).'''
    BO_CN = enum.auto()
    '''Tibetan (China).'''
    CY_GB = enum.auto()
    '''Welsh (United Kingdom).'''
    KM_KH = enum.auto()
    '''Khmer (Cambodia).'''
    LO_LA = enum.auto()
    '''Lao (Laos).'''
    GL_ES = enum.auto()
    '''Galician (Spain).'''
    KOK_IN = enum.auto()
    '''Konkani (India).'''
    SD_IN = enum.auto()
    '''Sindhi (India).'''
    SYR_SY = enum.auto()
    '''Syriac (Syria).'''
    SI_LK = enum.auto()
    '''Sinhalese (Sri Lanka).'''
    IU_CANS_CA = enum.auto()
    '''Inuktitut, Syllabics (Canada).'''
    AM_ET = enum.auto()
    '''Amharic (Ethiopia).'''
    NE_NP = enum.auto()
    '''Nepali (Nepal).'''
    FY_NL = enum.auto()
    '''Frisian (Netherlands).'''
    PS_AF = enum.auto()
    '''Pashto (Afghanistan, Pakistan).'''
    FIL_PH = enum.auto()
    '''Filipino (Philippines).'''
    DIV_MV = enum.auto()
    '''Divehi (Maldives, India).'''
    HA_LATN_NG = enum.auto()
    '''Hausa, Latin alphabet (Benin, Nigeria, Togo, and other western African nations).'''
    YO_NG = enum.auto()
    '''Yoruba (Benin, Ghana, Nigeria, Togo, and other western African nations).'''
    QUZ_BO = enum.auto()
    '''Quechua (Bolivia).'''
    NZO_ZA = enum.auto()
    '''Sesotho sa Leboa (South Africa).'''
    BA_RU = enum.auto()
    '''Bashkir (Russia).'''
    LB_LU = enum.auto()
    '''Luxembourgish (Luxembourg).'''
    KL_GL = enum.auto()
    '''Greenlandic (Greenland).'''
    IG_NG = enum.auto()
    '''Igbo (Nigeria).'''
    SO_SO = enum.auto()
    '''Somali (Somalia).'''
    II_CN = enum.auto()
    '''Yi (China).'''
    ARN_CL = enum.auto()
    '''Mapudungun (Chile).'''
    MOH_CA = enum.auto()
    '''Mohawk (Canada).'''
    BR_FR = enum.auto()
    '''Breton (France).'''
    UG_CN = enum.auto()
    '''Uighur (China).'''
    MI_NZ = enum.auto()
    '''Maori (New Zealand).'''
    OC_FR = enum.auto()
    '''Occitan (France).'''
    CO_FR = enum.auto()
    '''Corsican (France).'''
    GSW_FR = enum.auto()
    '''Alsatian (France).'''
    SAH_RU = enum.auto()
    '''Yakut (Russia).'''
    QUT_GT = enum.auto()
    '''K\'iche (Guatemala).'''
    RW_RW = enum.auto()
    '''Kinyarwanda (Rwanda).'''
    WO_SN = enum.auto()
    '''Wolof (Gambia, Mauritania, Senegal, and other western African nations).'''
    GBZ_AF = enum.auto()
    '''Dari (Afghanistan).'''
    LANG_NEUTRAL_SYS_DEFAULT = enum.auto()
    '''System default locale language.'''
    AR_IQ = enum.auto()
    '''Arabic (Iraq).'''
    ZH_CN = enum.auto()
    '''Chinese (China).'''
    DE_CH = enum.auto()
    '''German (Switzerland).'''
    EN_GB = enum.auto()
    '''English (United Kingdom).'''
    ES_MX = enum.auto()
    '''Spanish (Mexico).'''
    FR_BE = enum.auto()
    '''French (Belgium).'''
    IT_CH = enum.auto()
    '''Italian (Switzerland).'''
    KO_JOHAB_KR = enum.auto()
    '''Korean, Johab (Korea).'''
    NL_BE = enum.auto()
    '''Dutch (Belgium).'''
    NN_NO = enum.auto()
    '''Nyorsk (Norway).'''
    PT = enum.auto()
    '''Portuguese (Portugal).'''
    SR_LATN_SP = enum.auto()
    '''Serbian, Latin alphabet (Serbia).'''
    SV_FI = enum.auto()
    '''Swedish (Finland).'''
    UR_IN = enum.auto()
    '''Urdu (India).'''
    LT_C_LT = enum.auto()
    '''Lithuanian, Classic (Lithuania).'''
    AZ_CYRL_AZ = enum.auto()
    '''Azeri, Cyrillic alphabet (Azerbaijan).'''
    WEE_DE = enum.auto()
    '''Sorbian, Lower (Germany).'''
    SE_SE = enum.auto()
    '''Sami, Northern (Sweden).'''
    GA_IE = enum.auto()
    '''Irish (Ireland).'''
    MS_BN = enum.auto()
    '''Malay (Brunei).'''
    UZ_CYRL_UZ = enum.auto()
    '''Uzbek, Cyrillic alphabet (Uzbekistan).'''
    BN_BD = enum.auto()
    '''Bengali (Bangladesh).'''
    MN_MONG_CN = enum.auto()
    '''Mongolian, Traditional (China).'''
    SD_PK = enum.auto()
    '''Sindhi (Pakistan).'''
    IU_LATN_CA = enum.auto()
    '''Inuktitut, Latin alphabet (Canada).'''
    TZM_LATN_DZ = enum.auto()
    '''Tamazight, Latin alphabet (Algeria).'''
    QUZ_EC = enum.auto()
    '''Quechua (Ecuador).'''
    LANG_NEUTRAL_CUSTOM_DEFAULT = enum.auto()
    '''Default custom locale language.'''
    AR_EG = enum.auto()
    '''Arabic (Egypt).'''
    ZH_HK = enum.auto()
    '''Chinese (Hong Kong Special Administrative Region, China).'''
    DE_AT = enum.auto()
    '''German (Austria).'''
    EN_AU = enum.auto()
    '''English (Australia).'''
    ES_ES = enum.auto()
    '''Spanish, Modern (Spain).'''
    FR_CA = enum.auto()
    '''French (Canada).'''
    SR_CYRL_CS = enum.auto()
    '''Serbian, Cyrillic alphabet (Serbia).'''
    SE_FI = enum.auto()
    '''Sami, Northern (Finland).'''
    QUZ_PE = enum.auto()
    '''Quechua (Peru).'''
    LANG_NEUTRAL_CUSTOM = enum.auto()
    '''Unspecified custom locale language.'''
    AR_LY = enum.auto()
    '''Arabic (Libya).'''
    ZH_SG = enum.auto()
    '''Chinese (Singapore).'''
    DE_LU = enum.auto()
    '''German (Luxembourg).'''
    EN_CA = enum.auto()
    '''English (Canada).'''
    ES_GT = enum.auto()
    '''Spanish (Guatemala).'''
    FR_CH = enum.auto()
    '''French (Switzerland).'''
    HR_BA = enum.auto()
    '''Croatian (Bosnia and Herzegovina).'''
    SMJ_NO = enum.auto()
    '''Sami, Luli (Norway).'''
    LANG_NEUTRAL_CUSTOM_DEFAULT_MUI = enum.auto()
    '''Default custom multi-user interface locale language.'''
    AR_DZ = enum.auto()
    '''Arabic (Algeria).'''
    ZH_MO = enum.auto()
    '''Chinese (Macao Special Administrative Region, China).'''
    DE_LI = enum.auto()
    '''German (Liechtenstein).'''
    EN_NZ = enum.auto()
    '''English (New Zealand).'''
    ES_CR = enum.auto()
    '''Spanish (Costa Rica).'''
    FR_LU = enum.auto()
    '''French (Luxembourg).'''
    BS_LATN_BA = enum.auto()
    '''Bosnian, Latin alphabet (Bosnia and Herzegovina).'''
    SMJ_SE = enum.auto()
    '''Sami, Lule (Sweden).'''
    AR_MA = enum.auto()
    '''Arabic (Morocco).'''
    EN_IE = enum.auto()
    '''English (Ireland).'''
    ES_PA = enum.auto()
    '''Spanish (Panama).'''
    AR_MC = enum.auto()
    '''French (Monaco).'''
    SR_LATN_BA = enum.auto()
    '''Serbian, Latin alphabet (Bosnia and Herzegovina).'''
    SMA_NO = enum.auto()
    '''Sami, Southern (Norway).'''
    AR_TN = enum.auto()
    '''Arabic (Tunisia).'''
    EN_ZA = enum.auto()
    '''English (South Africa).'''
    ES_DO = enum.auto()
    '''Spanish (Dominican Republic).'''
    SR_CYRL_BA = enum.auto()
    '''Serbian, Cyrillic alphabet (Bosnia and Herzegovina).'''
    SMA_SE = enum.auto()
    '''Sami, Southern (Sweden).'''
    AR_OM = enum.auto()
    '''Arabic (Oman).'''
    EL_2_GR = enum.auto()
    '''Greek 2 (Greece).'''
    EN_JM = enum.auto()
    '''English (Jamaica).'''
    ES_VE = enum.auto()
    '''Spanish (Venezuela).'''
    BS_CYRL_BA = enum.auto()
    '''Bosnian, Cyrillic alphabet (Bosnia and Herzegovina).'''
    SMS_FI = enum.auto()
    '''Sami, Skolt (Finland).'''
    AR_YE = enum.auto()
    '''Arabic (Yemen).'''
    AR_029 = enum.auto()
    '''English (Nations of the Caribbean).'''
    ES_CO = enum.auto()
    '''Spanish (Colombia).'''
    SMN_FI = enum.auto()
    '''Sami, Inari (Finland).'''
    AR_SY = enum.auto()
    '''Arabic (Syria).'''
    EN_BZ = enum.auto()
    '''English (Belize).'''
    ES_PE = enum.auto()
    '''Spanish (Peru).'''
    AR_JO = enum.auto()
    '''Arabic (Jordan).'''
    EN_TT = enum.auto()
    '''English (Trinidad and Tobago).'''
    ES_AR = enum.auto()
    '''Spanish (Argentina).'''
    AR_LB = enum.auto()
    '''Arabic (Lebanon).'''
    EN_ZW = enum.auto()
    '''English (Zimbabwe).'''
    ES_EC = enum.auto()
    '''Spanish (Ecuador).'''
    AR_KW = enum.auto()
    '''Arabic (Kuwait).'''
    EN_PH = enum.auto()
    '''English (Phillippines).'''
    ES_CL = enum.auto()
    '''Spanish (Chile).'''
    AR_AE = enum.auto()
    '''Arabic (United Arab Emirates).'''
    ES_UY = enum.auto()
    '''Spanish (Uruguay).'''
    AR_BH = enum.auto()
    '''Arabic (Bahrain).'''
    ES_PY = enum.auto()
    '''Spanish (Paraguay).'''
    AR_QA = enum.auto()
    '''Arabic (Qatar).'''
    EN_IN = enum.auto()
    '''English (India).'''
    ES_BO = enum.auto()
    '''Spanish (Bolivia).'''
    EN_MY = enum.auto()
    '''English (Malaysia).'''
    ES_SV = enum.auto()
    '''Spanish (El Salvador).'''
    EN_SG = enum.auto()
    '''English (Singapore).'''
    ES_HN = enum.auto()
    '''Spanish (Honduras).'''
    ES_NI = enum.auto()
    '''Spanish (Nicaragua).'''
    ES_PR = enum.auto()
    '''Spanish (Puerto Rico).'''
    ES_US = enum.auto()
    '''Spanish (United States).'''
    ZH_HANT = enum.auto()
    '''Chinese, Traditional (China).'''

class EmfPlusLineCapType(enum.Enum):
    LINE_CAP_TYPE_FLAT = enum.auto()
    '''Specifies a squared-off line cap. The end of the line MUST be the last point in the line.'''
    LINE_CAP_TYPE_SQUARE = enum.auto()
    '''Specifies a square line cap. The center of the square MUST be located at the last point in the line. The width of the square is the line width.'''
    LINE_CAP_TYPE_ROUND = enum.auto()
    '''Specifies a circular line cap. The center of the circle MUST be located at the last point in the line. The diameter of the circle is the line width.'''
    LINE_CAP_TYPE_TRIANGLE = enum.auto()
    '''Specifies a triangular line cap. The base of the triangle MUST be located at the last point in the line. The base of the triangle is the line width.'''
    LINE_CAP_TYPE_NO_ANCHOR = enum.auto()
    '''Specifies that the line end is not anchored.'''
    LINE_CAP_TYPE_SQUARE_ANCHOR = enum.auto()
    '''Specifies that the line end is anchored with a square line cap. The center of the square MUST be located at the last point in the line. The height and width of the square are the line width.'''
    LINE_CAP_TYPE_ROUND_ANCHOR = enum.auto()
    '''Specifies that the line end is anchored with a circular line cap. The center of the circle MUST be located at the last point in the line. The circle SHOULD be wider than the line.'''
    LINE_CAP_TYPE_DIAMOND_ANCHOR = enum.auto()
    '''Specifies that the line end is anchored with a diamond-shaped line cap, which is a square turned at 45 degrees. The center of the diamond MUST be located at the last point in the line. The diamond SHOULD be wider than the line.'''
    LINE_CAP_TYPE_ARROW_ANCHOR = enum.auto()
    '''Specifies that the line end is anchored with an arrowhead shape. The arrowhead point MUST be located at the last point in the line. The arrowhead SHOULD be wider than the line.'''
    LINE_CAP_TYPE_ANCHOR_MASK = enum.auto()
    '''Mask used to check whether a line cap is an anchor cap.'''
    LINE_CAP_TYPE_CUSTOM = enum.auto()
    '''Specifies a custom line cap.'''

class EmfPlusLineJoinType(enum.Enum):
    LINE_JOIN_TYPE_MITER = enum.auto()
    '''Specifies a mitered line join.'''
    LINE_JOIN_TYPE_BEVEL = enum.auto()
    '''Specifies a beveled line join.'''
    LINE_JOIN_TYPE_ROUND = enum.auto()
    '''Specifies a rounded line join.'''
    LINE_JOIN_TYPE_MITER_CLIPPED = enum.auto()
    '''Specifies a clipped mitered line join.'''

class EmfPlusLineStyle(enum.Enum):
    LINE_STYLE_SOLID = enum.auto()
    '''Specifies a solid line.'''
    LINE_STYLE_DASH = enum.auto()
    '''Specifies a dashed line.'''
    LINE_STYLE_DOT = enum.auto()
    '''Specifies a dotted line.'''
    LINE_STYLE_DASH_DOT = enum.auto()
    '''Specifies an alternating dash-dot line.'''
    LINE_STYLE_DASH_DOT_DOT = enum.auto()
    '''Specifies an alternating dash-dot-dot line.'''
    LINE_STYLE_CUSTOM = enum.auto()
    '''Specifies a user-defined, custom dashed line.'''

class EmfPlusMetafileDataType(enum.Enum):
    METAFILE_DATA_TYPE_WMF = enum.auto()
    '''Specifies that the metafile is a WMF metafile that specifies graphics operations with WMF records, as specified in [MS-WMF].'''
    METAFILE_DATA_TYPE_WMF_PLACEABLE = enum.auto()
    '''Specifies that the metafile is a WMF metafile that specifies graphics operations with WMF records, and which contains additional header information that makes the WMF metafile device-independent, as specified in [MS-WMF].'''
    METAFILE_DATA_TYPE_EMF = enum.auto()
    '''Specifies that the metafile is an EMF metafile that specifies graphics operations with EMF records, as specified in [MS-EMF].'''
    METAFILE_DATA_TYPE_EMF_PLUS_ONLY = enum.auto()
    '''Specifies that the metafile is an EMF+ metafile that specifies graphics operations with EMF+ records only.'''
    METAFILE_DATA_TYPE_EMF_PLUS_DUAL = enum.auto()
    '''Specifies that the metafile is an EMF+ metafile that specifies graphics operations with both EMF and EMF+ records.'''

class EmfPlusObjectClamp(enum.Enum):
    RECT_CLAMP = enum.auto()
    '''The rectangle clamp'''
    BITMAP_CLAMP = enum.auto()
    '''The bitmap clamp'''

class EmfPlusObjectType(enum.Enum):
    OBJECT_TYPE_INVALID = enum.auto()
    '''The object is not a valid object.'''
    OBJECT_TYPE_BRUSH = enum.auto()
    '''Specifies an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusBrush` object (section 2.2.1.1). Brush objects fill graphics regions.'''
    OBJECT_TYPE_PEN = enum.auto()
    '''Specifies an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPen` object (section 2.2.1.7). Pen objects draw graphics lines.'''
    OBJECT_TYPE_PATH = enum.auto()
    '''Specifies an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPath` object (section 2.2.1.6). Path objects specify sequences of lines, curves, and shapes.'''
    OBJECT_TYPE_REGION = enum.auto()
    '''Specifies an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegion` object (section 2.2.1.8). Region objects specify areas of the output surface.'''
    OBJECT_TYPE_IMAGE = enum.auto()
    '''Specifies an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusImage` object (section 2.2.1.4). Image objects encapsulate bitmaps and metafiles.'''
    OBJECT_TYPE_FONT = enum.auto()
    '''Specifies an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusFont` object (section 2.2.1.3). Font objects specify font properties, including typeface style, EM size, and font family.'''
    OBJECT_TYPE_STRING_FORMAT = enum.auto()
    '''Specifies an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusStringFormat` object (section 2.2.1.9). String format objects specify text layout, including alignment, orientation, tab stops, clipping, and digit substitution for languages that do not use Western European digits.'''
    OBJECT_TYPE_IMAGE_ATTRIBUTES = enum.auto()
    '''Specifies an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusImageAttributes` object (section 2.2.1.5). Image attribute objects specify operations on pixels during image rendering, including color adjustment, grayscale adjustment, gamma correction, and color mapping.'''
    OBJECT_TYPE_CUSTOM_LINE_CAP = enum.auto()
    '''Specifies an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomLineCap` object (section 2.2.1.2). Custom line cap objects specify shapes to draw at the ends of a graphics line, including squares, circles, and diamonds.'''

class EmfPlusPaletteStyleFlags(enum.Enum):
    PALETTE_STYLE_HAS_ALPHA = enum.auto()
    '''If set, one or more of the palette entries MUST contain alpha transparency information.'''
    PALETTE_STYLE_GRAY_SCALE = enum.auto()
    '''If set, the palette MUST contain only grayscale entries.'''
    PALETTE_STYLE_HALFTONE = enum.auto()
    '''If set, the palette MUST contain discrete color values that can be used for halftoning.'''

class EmfPlusPathPointFlags(enum.Enum):
    C = enum.auto()
    '''The c flag'''
    R = enum.auto()
    '''The r flag'''
    P = enum.auto()
    '''The p flag'''

class EmfPlusPathPointTypeEnum(enum.Enum):
    PATH_POINT_TYPE_START = enum.auto()
    '''Specifies that the point is the starting point of a path.'''
    PATH_POINT_TYPE_LINE = enum.auto()
    '''Specifies that the point is one of the two endpoints of a line.'''
    PATH_POINT_TYPE_BEZIER = enum.auto()
    '''Specifies that the point is an endpoint or control point of a cubic Bezier curve.'''

class EmfPlusPathPointTypeFlags(enum.Enum):
    PATH_POINT_TYPE_DASH_MODE = enum.auto()
    '''Specifies that a line segment that passes through the point is dashed.'''
    PATH_POINT_TYPE_PATH_MARKER = enum.auto()
    '''Specifies that the point is a position marker.'''
    PATH_POINT_TYPE_CLOSE_SUBPATH = enum.auto()
    '''Specifies that the point is the endpoint of a subpath.'''

class EmfPlusPenAlignment(enum.Enum):
    PEN_ALIGNMENT_CENTER = enum.auto()
    '''Specifies that the EmfPlusPen object is centered over the theoretical line.'''
    PEN_ALIGNMENT_INSET = enum.auto()
    '''Specifies that the pen is positioned on the inside of the theoretical line.'''
    PEN_ALIGNMENT_LEFT = enum.auto()
    '''Specifies that the pen is positioned to the left of the theoretical line.'''
    PEN_ALIGNMENT_OUTSET = enum.auto()
    '''Specifies that the pen is positioned on the outside of the theoretical line.'''
    PEN_ALIGNMENT_RIGHT = enum.auto()
    '''Specifies that the pen is positioned to the right of the theoretical line.'''

class EmfPlusPenDataFlags(enum.Enum):
    PEN_DATA_TRANSFORM = enum.auto()
    '''If set, a 2x3 transform matrix MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_START_CAP = enum.auto()
    '''If set, the style of a starting line cap MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_END_CAP = enum.auto()
    '''Indicates whether the style of an ending line cap MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_JOIN = enum.auto()
    '''Indicates whether a line join type MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_MITER_LIMIT = enum.auto()
    '''Indicates whether a miter limit MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_LINE_STYLE = enum.auto()
    '''Indicates whether a line style MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_DASHED_LINE_CAP = enum.auto()
    '''Indicates whether a dashed line cap MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_DASHED_LINE_OFFSET = enum.auto()
    '''Indicates whether a dashed line offset MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_DASHED_LINE = enum.auto()
    '''Indicates whether an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusDashedLineData` object MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_NON_CENTER = enum.auto()
    '''Indicates whether a pen alignment MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_COMPOUND_LINE = enum.auto()
    '''Indicates whether the length and content of a :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCompoundLineData` object are present in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_CUSTOM_START_CAP = enum.auto()
    '''Indicates whether an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomStartCapData` object MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''
    PEN_DATA_CUSTOM_END_CAP = enum.auto()
    '''Indicates whether an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusCustomEndCapData` object MUST be specified in the OptionalData field of an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusPenData` object.'''

class EmfPlusPixelFormat(enum.Enum):
    PIXEL_FORMAT_UNDEFINED = enum.auto()
    '''The format is not specified.'''
    PIXEL_FORMAT_1BPP_INDEXED = enum.auto()
    '''The format is monochrome, and a color palette lookup table is used.'''
    PIXEL_FORMAT_4BPP_INDEXED = enum.auto()
    '''The format is 16-color, and a color palette lookup table is used.'''
    PIXEL_FORMAT_8BPP_INDEXED = enum.auto()
    '''The format is 256-color, and a color palette lookup table is used.'''
    PIXEL_FORMAT_16BPP_GRAY_SCALE = enum.auto()
    '''The format is 16 bits per pixel, grayscale.'''
    PIXEL_FORMAT_16BPP_RGB555 = enum.auto()
    '''The format is 16 bits per pixel; 5 bits each are used for the red, green, and blue components. The remaining bit is not used.'''
    PIXEL_FORMAT_16BPP_RGB565 = enum.auto()
    '''The format is 16 bits per pixel; 5 bits are used for the red component, 6 bits for the green component, and 5 bits for the blue component.'''
    PIXEL_FORMAT_16BPP_ARGB1555 = enum.auto()
    '''The format is 16 bits per pixel; 1 bit is used for the alpha component, and 5 bits each are used for the red, green, and blue components.'''
    PIXEL_FORMAT_24BPP_RGB = enum.auto()
    '''The format is 24 bits per pixel; 8 bits each are used for the red, green, and blue components.'''
    PIXEL_FORMAT_32BPP_RGB = enum.auto()
    '''The format is 32 bits per pixel; 8 bits each are used for the red, green, and blue components. The remaining 8 bits are not used.'''
    PIXEL_FORMAT_32BPP_ARGB = enum.auto()
    '''The format is 32 bits per pixel; 8 bits each are used for the alpha, red, green, and blue components.'''
    PIXEL_FORMAT_32BPP_PARGB = enum.auto()
    '''The format is 32 bits per pixel; 8 bits each are used for the alpha, red, green, and blue components. The red, green, and blue components are premultiplied according to the alpha component.'''
    PIXEL_FORMAT_48BPP_RGB = enum.auto()
    '''The format is 48 bits per pixel; 16 bits each are used for the red, green, and blue components.'''
    PIXEL_FORMAT_64BPP_ARGB = enum.auto()
    '''The format is 64 bits per pixel; 16 bits each are used for the alpha, red, green, and blue components.'''
    PIXEL_FORMAT_64BPP_PARGB = enum.auto()
    '''The format is 64 bits per pixel; 16 bits each are used for the alpha, red, green, and blue components. The red, green, and blue components are premultiplied according to the alpha component.'''

class EmfPlusPixelOffsetMode(enum.Enum):
    PIXEL_OFFSET_MODE_DEFAULT = enum.auto()
    '''Pixels are centered on integer coordinates, specifying speed over quality.'''
    PIXEL_OFFSET_MODE_HIGH_SPEED = enum.auto()
    '''Pixels are centered on integer coordinates, as with PixelOffsetModeNone. Higher speed at the expense of quality is specified.'''
    PIXEL_OFFSET_MODE_HIGH_QUALITY = enum.auto()
    '''Pixels are centered on half-integer coordinates, as with PixelOffsetModeHalf. Higher quality at the expense of speed is specified.'''
    PIXEL_OFFSET_MODE_NONE = enum.auto()
    '''Pixels are centered on the origin, which means that the pixel covers the area from -0.5 to 0.5 on both the x and y axes and its center is at (0,0).'''
    PIXEL_OFFSET_MODE_HALF = enum.auto()
    '''Pixels are centered on half-integer coordinates, which means that the pixel covers the area from 0 to 1 on both the x and y axes and its center is at (0.5,0.5). By offsetting pixels during rendering, the render quality can be improved at the cost of render speed.'''

class EmfPlusRecordType(enum.Enum):
    EMF_PLUS_HEADER = enum.auto()
    '''This record specifies the start of EMF+ data in the metafile. It MUST be embedded in the first EMF record after the :py:class:`aspose.imaging.fileformats.emf.emf.records.EmfMetafileHeader` record ([MS-EMF] section 2.3.4.2 record).'''
    EMF_PLUS_END_OF_FILE = enum.auto()
    '''This record specifies the end of EMF+ data in the metafile.'''
    EMF_PLUS_COMMENT = enum.auto()
    '''This record specifies arbitrary private data.'''
    EMF_PLUS_GET_DC = enum.auto()
    '''This record specifies that subsequent EMF records encountered in the metafile SHOULD be processed. EMF records cease being processed when the next EMF+ record is encountered.'''
    EMF_PLUS_MULTI_FORMAT_START = enum.auto()
    '''This record is reserved and MUST NOT be used.'''
    EMF_PLUS_MULTI_FORMAT_SECTION = enum.auto()
    '''This record is reserved and MUST NOT be used.'''
    EMF_PLUS_MULTI_FORMAT_END = enum.auto()
    '''This record is reserved and MUST NOT be used.'''
    EMF_PLUS_OBJECT = enum.auto()
    '''This record specifies an object for use in graphics operations.'''
    EMF_PLUS_CLEAR = enum.auto()
    '''This record clears the output ``coordinate space`` and initializes it with a specified background color and transparency.'''
    EMF_PLUS_FILL_RECTS = enum.auto()
    '''This record defines how to fill the interiors of a series of rectangles, using a specified brush.'''
    EMF_PLUS_DRAW_RECTS = enum.auto()
    '''This record defines the pen strokes for drawing a series of rectangles.'''
    EMF_PLUS_FILL_POLYGON = enum.auto()
    '''This record defines the data to fill the interior of a polygon, using a specified brush.'''
    EMF_PLUS_DRAW_LINES = enum.auto()
    '''This record defines the pen strokes for drawing a series of connected lines.'''
    EMF_PLUS_FILL_ELLIPSE = enum.auto()
    '''This record defines how to fill the interiors of an ellipse, using a specified brush.'''
    EMF_PLUS_DRAW_ELLIPSE = enum.auto()
    '''This record defines the pen strokes for drawing an ellipse.'''
    EMF_PLUS_FILL_PIE = enum.auto()
    '''This record defines how to fill a section of an interior section of an ellipse using a specified brush.'''
    EMF_PLUS_DRAW_PIE = enum.auto()
    '''This record defines pen strokes for drawing a section of an ellipse.'''
    EMF_PLUS_DRAW_ARC = enum.auto()
    '''The record defines pen strokes for drawing an arc of an ellipse.'''
    EMF_PLUS_FILL_REGION = enum.auto()
    '''This record defines how to fill the interior of a region using a specified brush.'''
    EMF_PLUS_FILL_PATH = enum.auto()
    '''The record defines how to fill the interiors of the figures defined in a graphics path with a specified brush. A path is an object that defines an arbitrary sequence of lines, curves, and shapes.'''
    EMF_PLUS_DRAW_PATH = enum.auto()
    '''The record defines the pen strokes to draw the figures in a graphics path. A path is an object that defines an arbitrary sequence of lines, curves, and shapes.'''
    EMF_PLUS_FILL_CLOSED_CURVE = enum.auto()
    '''This record defines how to fill the interior of a closed cardinal spline using a specified brush.'''
    EMF_PLUS_DRAW_CLOSED_CURVE = enum.auto()
    '''This record defines the pen and strokes for drawing a closed cardinal spline.'''
    EMF_PLUS_DRAW_CURVE = enum.auto()
    '''This record defines the pen strokes for drawing a cardinal spline.'''
    EMF_PLUS_DRAW_BEZIERS = enum.auto()
    '''This record defines the pen strokes for drawing a Bezier spline.'''
    EMF_PLUS_DRAW_IMAGE = enum.auto()
    '''This record defines a scaled :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusImage` object (section 2.2.1.4). An image can consist of either bitmap or metafile data.'''
    EMF_PLUS_DRAW_IMAGE_POINTS = enum.auto()
    '''This record defines a scaled EmfPlusImage object inside a parallelogram. An image can consist of either bitmap or metafile data.'''
    EMF_PLUS_DRAW_STRING = enum.auto()
    '''This record defines a text string based on a font, a layout rectangle, and a format.'''
    EMF_PLUS_SET_RENDERING_ORIGIN = enum.auto()
    '''This record defines the origin of rendering to the specified horizontal and vertical coordinates. This applies to hatch brushes and to 8 and 16 bits per pixel dither patterns.'''
    EMF_PLUS_SET_ANTI_ALIAS_MODE = enum.auto()
    '''This record defines whether to enable or disable text anti-aliasing. Text anti-aliasing is a method of making lines and edges of character glyphs appear smoother when drawn on an output surface.'''
    EMF_PLUS_SET_TEXT_RENDERING_HINT = enum.auto()
    '''This record defines the process used for rendering text.'''
    EMF_PLUS_SET_TEXT_CONTRAST = enum.auto()
    '''This record sets text contrast according to the specified text gamma value.'''
    EMF_PLUS_SET_INTERPOLATION_MODE = enum.auto()
    '''This record defines the interpolation mode of an object according to the specified type of image filtering. The interpolation mode influences how scaling (stretching and shrinking) is performed.'''
    EMF_PLUS_SET_PIXEL_OFFSET_MODE = enum.auto()
    '''This record defines the pixel offset mode according to the specified pixel centering value.'''
    EMF_PLUS_SET_COMPOSITING_MODE = enum.auto()
    '''This record defines the compositing mode according to the state of alpha blending, which specifies how source colors are combined with background colors.'''
    EMF_PLUS_SET_COMPOSITING_QUALITY = enum.auto()
    '''This record defines the compositing quality, which describes the desired level of quality for creating composite images from multiple objects.'''
    EMF_PLUS_SAVE = enum.auto()
    '''This record saves the graphics state, identified by a specified index, on a stack of saved graphics states. Each stack index is associated with a particular saved state, and the index is used by an :py:class:`aspose.imaging.fileformats.emf.emfplus.records.EmfPlusRestore` record (section 2.3.7.4) to restore the state.'''
    EMF_PLUS_RESTORE = enum.auto()
    '''This record restores the graphics state, identified by a specified index, from a stack of saved graphics states. Each stack index is associated with a particular saved state, and the index is defined by an :py:class:`aspose.imaging.fileformats.emf.emfplus.records.EmfPlusSave` record (section 2.3.7.5) to save the state.'''
    EMF_PLUS_BEGIN_CONTAINER = enum.auto()
    '''This record opens a new graphics state container and specifies a transform for it. Graphics containers are used to retain elements of the graphics state.'''
    EMF_PLUS_BEGIN_CONTAINER_NO_PARAMS = enum.auto()
    '''This record opens a new graphics state container.'''
    EMF_PLUS_END_CONTAINER = enum.auto()
    '''This record closes a graphics state container that was previously opened by a begin container operation.'''
    EMF_PLUS_SET_WORLD_TRANSFORM = enum.auto()
    '''This record defines the current world space transform in the playback device_context, according to a specified transform matrix.'''
    EMF_PLUS_RESET_WORLD_TRANSFORM = enum.auto()
    '''This record resets the current world space transform to the identify matrix.'''
    EMF_PLUS_MULTIPLY_WORLD_TRANSFORM = enum.auto()
    '''This record multiplies the current world space by a specified transform matrix.'''
    EMF_PLUS_TRANSLATE_WORLD_TRANSFORM = enum.auto()
    '''This record applies a translation transform to the current world space by specified horizontal and vertical distances.'''
    EMF_PLUS_SCALE_WORLD_TRANSFORM = enum.auto()
    '''This record applies a scaling transform to the current world space by specified horizontal and vertical scale factors.'''
    EMF_PLUS_ROTATE_WORLD_TRANSFORM = enum.auto()
    '''This record rotates the current world space by a specified angle.'''
    EMF_PLUS_SET_PAGE_TRANSFORM = enum.auto()
    '''This record specifies extra scaling factors for the current world space transform.'''
    EMF_PLUS_RESET_CLIP = enum.auto()
    '''This record resets the current clipping region for the world space to infinity.'''
    EMF_PLUS_SET_CLIP_RECT = enum.auto()
    '''This record combines the current clipping region with a rectangle.'''
    EMF_PLUS_SET_CLIP_PATH = enum.auto()
    '''This record combines the current clipping region with a graphics path.'''
    EMF_PLUS_SET_CLIP_REGION = enum.auto()
    '''This record combines the current clipping region with another graphics region.'''
    EMF_PLUS_OFFSET_CLIP = enum.auto()
    '''This record applies a translation transform on the current clipping region of the world space.'''
    EMF_PLUS_DRAW_DRIVER_STRING = enum.auto()
    '''This record specifies text output with character positions.'''
    EMF_PLUS_STROKE_FILL_PATH = enum.auto()
    '''This record closes any open figures in a path, strokes the outline of the path by using the current pen, and fills its interior by using the current brush.'''
    EMF_PLUS_SERIALIZABLE_OBJECT = enum.auto()
    '''This record defines an image effects parameter block that has been serialized into a data buffer.'''
    EMF_PLUS_SET_TS_GRAPHICS = enum.auto()
    '''This record specifies the state of a graphics device context for a terminal server.'''
    EMF_PLUS_SET_TS_CLIP = enum.auto()
    '''This record specifies clipping areas in the graphics device context for a terminal server.'''

class EmfPlusRegionNodeDataType(enum.Enum):
    REGION_NODE_DATA_TYPE_AND = enum.auto()
    '''Specifies a region node with child nodes. A Boolean AND operation SHOULD be applied to the left and right child nodes specified by an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNodeChildNodes` object (section 2.2.2.41).'''
    REGION_NODE_DATA_TYPE_OR = enum.auto()
    '''Specifies a region node with child nodes. A Boolean OR operation SHOULD be applied to the left and right child nodes specified by an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNodeChildNodes` object.'''
    REGION_NODE_DATA_TYPE_XOR = enum.auto()
    '''Specifies a region node with child nodes. A Boolean XOR operation SHOULD be applied to the left and right child nodes specified by an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNodeChildNodes` object.'''
    REGION_NODE_DATA_TYPE_EXCLUDE = enum.auto()
    '''Specifies a region node with child nodes. A Boolean operation, defined as "the part of region 1 that is excluded from region 2", SHOULD be applied to the left and right child nodes specified by an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNodeChildNodes` object.'''
    REGION_NODE_DATA_TYPE_COMPLEMENT = enum.auto()
    '''Specifies a region node with child nodes. A Boolean operation, defined as "the part of region 2 that is excluded from region 1", SHOULD be applied to the left and right child nodes specified by an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNodeChildNodes` object.'''
    REGION_NODE_DATA_TYPE_RECT = enum.auto()
    '''Specifies a region node with no child nodes. The RegionNodeData field SHOULD specify a boundary with an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRectF` object (section 2.2.2.39).'''
    REGION_NODE_DATA_TYPE_PATH = enum.auto()
    '''Specifies a region node with no child nodes. The RegionNodeData field SHOULD specify a boundary with an :py:class:`aspose.imaging.fileformats.emf.emfplus.objects.EmfPlusRegionNodePath` object (section 2.2.2.42).'''
    REGION_NODE_DATA_TYPE_EMPTY = enum.auto()
    '''Specifies a region node with no child nodes. The RegionNodeData field SHOULD NOT be present'''
    REGION_NODE_DATA_TYPE_INFINITE = enum.auto()
    '''Specifies a region node with no child nodes, and its bounds are not defined.'''

class EmfPlusSmoothingMode(enum.Enum):
    SMOOTHING_MODE_DEFAULT = enum.auto()
    '''Specifies default curve smoothing with no anti-aliasing.'''
    SMOOTHING_MODE_HIGH_SPEED = enum.auto()
    '''Specifies best performance with no anti-aliasing.'''
    SMOOTHING_MODE_HIGH_QUALITY = enum.auto()
    '''Specifies best quality with anti-aliasing.'''
    SMOOTHING_MODE_NONE = enum.auto()
    '''Performs no curve smoothing and no anti-aliasing.'''
    SMOOTHING_MODE_ANTI_ALIAS_8X4 = enum.auto()
    '''Specifies good quality using an 8x4 box filter.'''
    SMOOTHING_MODE_ANTI_ALIAS_8X8 = enum.auto()
    '''Specifies better quality using an 8x8 box filter.'''

class EmfPlusStringAlignment(enum.Enum):
    STRING_ALIGNMENT_NEAR = enum.auto()
    '''Specifies that string alignment is toward the origin of the layout rectangle. This can be used to align characters along a line or to align text within a rectangle. For a right-to-left layout rectangle, the origin SHOULD be at the upper right.'''
    STRING_ALIGNMENT_CENTER = enum.auto()
    '''Specifies that alignment is centered between the origin and extent of the layout rectangle.'''
    STRING_ALIGNMENT_FAR = enum.auto()
    '''Specifies that alignment is to the right side of the layout rectangle.'''

class EmfPlusStringDigitSubstitution(enum.Enum):
    STRING_DIGIT_SUBSTITUTION_USER = enum.auto()
    '''Specifies an implementation-defined substitution scheme.'''
    STRING_DIGIT_SUBSTITUTION_NONE = enum.auto()
    '''Specifies to disable substitutions.'''
    STRING_DIGIT_SUBSTITUTION_NATIONAL = enum.auto()
    '''Specifies substitution digits that correspond with the official national language of the user\'s locale.'''
    STRING_DIGIT_SUBSTITUTION_TRADITIONAL = enum.auto()
    '''Specifies substitution digits that correspond to the user\'s native script or language, which can be different from the official national language of the user\'s locale.'''

class EmfPlusStringFormatFlags(enum.Enum):
    STRING_FORMAT_DIRECTION_RIGHT_TO_LEFT = enum.auto()
    '''If set, the reading order of the string SHOULD be right to left. For horizontal text, this means that characters are read from right to left. For vertical text, this means that columns are read from right to left.
    If clear, horizontal or vertical text SHOULD be read from left to right.'''
    STRING_FORMAT_DIRECTION_VERTICAL = enum.auto()
    '''If set, individual lines of text SHOULD be drawn vertically on the display device.
    If clear, individual lines of text SHOULD be drawn horizontally, with each new line below the previous line.'''
    STRING_FORMAT_NO_FIT_BLACK_BOX = enum.auto()
    '''If set, parts of characters MUST be allowed to overhang the text layout rectangle.
    If clear, characters that overhang the boundaries of the text layout rectangle MUST be repositioned to avoid overhang.
    An italic, "f" is an example of a character that can have overhanging parts.'''
    STRING_FORMAT_DISPLAY_FORMAT_CONTROL = enum.auto()
    '''If set, control characters SHOULD appear in the output as representative Unicode glyphs.'''
    STRING_FORMAT_NO_FONT_FALLBACK = enum.auto()
    '''If set, an alternate font SHOULD be used for characters that are not supported in the requested font.
    If clear, a character missing from the requested font SHOULD appear as a "font missing" character, which MAY be an open square.'''
    STRING_FORMAT_MEASURE_TRAILING_SPACES = enum.auto()
    '''If set, the space at the end of each line MUST be included in measurements of string length.
    If clear, the space at the end of each line MUST be excluded from measurements of string length.'''
    STRING_FORMAT_NO_WRAP = enum.auto()
    '''If set, a string that extends past the end of the text layout rectangle MUST NOT be wrapped to the next line.
    If clear, a string that extends past the end of the text layout rectangle MUST be broken at the last word boundary within the bounding rectangle, and the remainder of the string MUST be wrapped to the next line.'''
    STRING_FORMAT_LINE_LIMIT = enum.auto()
    '''If set, whole lines of text SHOULD be output and SHOULD NOT be clipped by the string\'s layout rectangle.
    If clear, text layout SHOULD continue until all lines are output, or until additional lines would not be visible as a result of clipping.
    This flag can be used either to deny or allow a line of text to be partially obscured by a layout rectangle that is not a multiple of line height. For all text to be visible, a layout rectangle at least as tall as the height of one line.'''
    STRING_FORMAT_NO_CLIP = enum.auto()
    '''If set, text extending outside the string layout rectangle SHOULD be allowed to show.
    If clear, all text that extends outside the layout rectangle SHOULD be clipped.'''
    STRING_FORMAT_BYPASS_GDI = enum.auto()
    '''This flag MAY be used to specify an implementation-specific process for rendering text.'''

class EmfPlusStringTrimming(enum.Enum):
    STRING_TRIMMING_NONE = enum.auto()
    '''Specifies that no trimming is done.'''
    STRING_TRIMMING_CHARACTER = enum.auto()
    '''Specifies that the string is broken at the boundary of the last character that is inside the layout rectangle. This is the default.'''
    STRING_TRIMMING_WORD = enum.auto()
    '''Specifies that the string is broken at the boundary of the last word that is inside the layout rectangle.'''
    STRING_TRIMMING_ELLIPSIS_CHARACTER = enum.auto()
    '''Specifies that the string is broken at the boundary of the last character that is inside the layout rectangle, and an ellipsis (...) is inserted after the character.'''
    STRING_TRIMMING_ELLIPSIS_WORD = enum.auto()
    '''Specifies that the string is broken at the boundary of the last word that is inside the layout rectangle, and an ellipsis (...) is inserted after the word.'''
    STRING_TRIMMING_ELLIPSIS_PATH = enum.auto()
    '''Specifies that the center is removed from the string and replaced by an ellipsis. The algorithm keeps as much of the last portion of the string as possible.'''

class EmfPlusTextRenderingHint(enum.Enum):
    TEXT_RENDERING_HINT_SYSTEM_DEFAULT = enum.auto()
    '''Specifies that each text character SHOULD be drawn using whatever font-smoothing settings have been configured on the operating system.'''
    TEXT_RENDERING_HINT_SINGLE_BIT_PER_PIXEL_GRID_FIT = enum.auto()
    '''Specifies that each text character SHOULD be drawn using its glyph bitmap. Smoothing MAY be used to improve the appearance of character glyph stems and curvature.'''
    TEXT_RENDERING_HINT_SINGLE_BIT_PER_PIXEL = enum.auto()
    '''Specifies that each text character SHOULD be drawn using its glyph bitmap. Smoothing is not used.'''
    TEXT_RENDERING_HINT_ANTIALIAS_GRID_FIT = enum.auto()
    '''Specifies that each text character SHOULD be drawn using its anti-aliased glyph bitmap with smoothing. The rendering is high quality because of anti-aliasing, but at a higher performance cost.'''
    TEXT_RENDERING_HINT_ANTIALIAS = enum.auto()
    '''Specifies that each text character is drawn using its anti-aliased glyph bitmap without hinting. Better quality results from anti-aliasing, but stem width differences MAY be noticeable because hinting is turned off.'''
    TEXT_RENDERING_HINT_CLEAR_TYPE_GRID_FIT = enum.auto()
    '''Specifies that each text character SHOULD be drawn using its ClearType glyph bitmap with smoothing. This is the highest-quality text hinting setting, which is used to take advantage of ClearType font features.'''

class EmfPlusUnitType(enum.Enum):
    UNIT_TYPE_WORLD = enum.auto()
    '''Specifies a unit of logical distance within the world space.'''
    UNIT_TYPE_DISPLAY = enum.auto()
    '''Specifies a unit of distance based on the characteristics of the physical display.
    For example, if the display device is a monitor, then the unit is 1 pixel.'''
    UNIT_TYPE_PIXEL = enum.auto()
    '''Specifies a unit of 1 pixel.'''
    UNIT_TYPE_POINT = enum.auto()
    '''Specifies a unit of 1 printer\'s point, or 1/72 inch.'''
    UNIT_TYPE_INCH = enum.auto()
    '''Specifies a unit of 1 inch.'''
    UNIT_TYPE_DOCUMENT = enum.auto()
    '''Specifies a unit of 1/300 inch.'''
    UNIT_TYPE_MILLIMETER = enum.auto()
    '''Specifies a unit of 1 millimeter.'''

class EmfPlusWrapMode(enum.Enum):
    WRAP_MODE_TILE = enum.auto()
    '''Tiles the gradient or texture.'''
    WRAP_MODE_TILE_FLIP_X = enum.auto()
    '''Reverses the texture or gradient horizontally, and then tiles the texture or gradient.'''
    WRAP_MODE_TILE_FLIP_Y = enum.auto()
    '''Reverses the texture or gradient vertically, and then tiles the texture or gradient.'''
    WRAP_MODE_TILE_FLIP_XY = enum.auto()
    '''Reverses the texture or gradient horizontally and vertically, and then tiles the texture or gradient.'''
    WRAP_MODE_CLAMP = enum.auto()
    '''Fixes the texture or gradient to the object boundary.'''

