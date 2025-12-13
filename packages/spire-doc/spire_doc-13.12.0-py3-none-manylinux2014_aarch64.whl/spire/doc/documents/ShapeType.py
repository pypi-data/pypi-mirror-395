from enum import Enum
from plum import dispatch
from typing import TypeVar, Union, Generic, List, Tuple
from spire.doc.common import *
from spire.doc import *
from ctypes import *
import abc

class ShapeType(Enum):
    """
    Specifies type of the Shape.
    """

    # the shape is a group shape
    Group = -1
    # The shape is an image.
    Image = 75
    # The shape is a textbox. Note that shapes of many other types can also have text inside them too.
    # A shape does not have to have this type to contain text.
    # The shape is a textbox.
    TextBox = 202
    # The shape is an OLE object.
    # <p>You cannot create shapes of this type in the document.</p>
    # In Microsoft Word, shapes that represent OLE objects have shape type picture,
    # but in our model, they are distinguished into their own shape type.
    # The shape is an OLE object.
    OleObject = -2
    # The shape is an ActiveX control.
    # <p>You cannot create shapes of this type in the document.</p>
    # In DOC and RTF, shapes that represent ActiveX controls have shape type picture.
    # In WordML, ActiveX controls have their own shape type and so is in the model.
    # The shape is an ActiveX control.
    OleControl = 201
    # A shape Psawn by user and consisting of multiple segments and/or vertices (curve, freeform or scribble).
    # <p>You cannot create shapes of this type in the document.</p>
    NonPrimitive = 0
    Rectangle = 1
    RoundRectangle = 2
    Ellipse = 3
    Diamond = 4
    Triangle = 5
    RightTriangle = 6
    Parallelogram = 7
    Trapezoid = 8
    Hexagon = 9
    Octagon = 10
    Plus = 11
    Star = 12
    Arrow = 13
    ThickArrow = 14
    HomePlate = 15
    Cube = 16
    Balloon = 17
    Seal = 18
    Arc = 19
    Line = 20
    Plaque = 21
    Can = 22
    Donut = 23
    TextSimple = 24
    TextOctagon = 25
    TextHexagon = 26
    TextCurve = 27
    TextWave = 28
    TextRing = 29
    TextOnCurve = 30
    TextOnRing = 31
    StraightConnector1 = 32
    BentConnector2 = 33
    BentConnector3 = 34
    BentConnector4 = 35
    BentConnector5 = 36
    CurvedConnector2 = 37
    CurvedConnector3 = 38
    CurvedConnector4 = 39
    CurvedConnector5 = 40
    Callout1 = 41
    Callout2 = 42
    Callout3 = 43
    AccentCallout1 = 44
    AccentCallout2 = 45
    AccentCallout3 = 46
    BorderCallout1 = 47
    BorderCallout2 = 48
    BorderCallout3 = 49
    AccentBorderCallout1 = 50
    AccentBorderCallout2 = 51
    AccentBorderCallout3 = 52
    AccentBorderCallout90 = 181
    Ribbon = 53
    Ribbon2 = 54
    Chevron = 55
    Pentagon = 56
    NoSmoking = 57
    Seal8 = 58
    Seal16 = 59
    Seal32 = 60
    WedgeRectCallout = 61
    WedgeRRectCallout = 62
    WedgeEllipseCallout = 63
    Wave = 64
    FoldedCorner = 65
    LeftArrow = 66
    DownArrow = 67
    UpArrow = 68
    LeftRightArrow = 69
    UpDownArrow = 70
    IrregularSeal1 = 71
    IrregularSeal2 = 72
    LightningBolt = 73
    Heart = 74
    QuadArrow = 76
    LeftArrowCallout = 77
    RightArrowCallout = 78
    UpArrowCallout = 79
    DownArrowCallout = 80
    LeftRightArrowCallout = 81
    UpDownArrowCallout = 82
    QuadArrowCallout = 83
    Bevel = 84
    LeftBracket = 85
    RightBracket = 86
    LeftBrace = 87
    RightBrace = 88
    LeftUpArrow = 89
    BentUpArrow = 90
    BentArrow = 91
    Seal24 = 92
    StripedRightArrow = 93
    NotchedRightArrow = 94
    BlockArc = 95
    SmileyFace = 96
    VerticalScroll = 97
    HorizontalScroll = 98
    CircularArrow = 99
    # This shape type seems to be set for shapes that are not part of the standard set of the
    # auto shapes in Microsoft Word. For example, if you insert a new auto shape from ClipArt.
    # <p>You cannot create shapes of this type in the document.</p>
    CustomShape = 100
    UturnArrow = 101
    CurvedRightArrow = 102
    CurvedLeftArrow = 103
    CurvedUpArrow = 104
    CurvedDownArrow = 105
    CloudCallout = 106
    EllipseRibbon = 107
    EllipseRibbon2 = 108
    FlowChartProcess = 109
    FlowChartDecision = 110
    FlowChartInputOutput = 111
    FlowChartPredefinedProcess = 112
    FlowChartInternalStorage = 113
    FlowChartDocument = 114
    FlowChartMultidocument = 115
    FlowChartTerminator = 116
    FlowChartPreparation = 117
    FlowChartManualInput = 118
    FlowChartManualOperation = 119
    FlowChartConnector = 120
    FlowChartPunchedCard = 121
    FlowChartPunchedTape = 122
    FlowChartSummingJunction = 123
    FlowChartOr = 124
    FlowChartCollate = 125
    FlowChartSort = 126
    FlowChartExtract = 127
    FlowChartMerge = 128
    FlowChartOfflineStorage = 129
    FlowChartOnlineStorage = 130
    FlowChartMagneticTape = 131
    FlowChartMagneticDisk = 132
    FlowChartMagneticDrum = 133
    FlowChartDisplay = 134
    FlowChartDelay = 135
    TextPlainText = 136
    TextStop = 137
    TextTriangle = 138
    TextTriangleInverted = 139
    TextChevron = 140
    TextChevronInverted = 141
    TextRingInside = 142
    TextRingOutside = 143
    TextArchUpCurve = 144
    TextArchDownCurve = 145
    TextCircleCurve = 146
    TextButtonCurve = 147
    TextArchUpPour = 148
    TextArchDownPour = 149
    TextCirclePour = 150
    TextButtonPour = 151
    TextCurveUp = 152
    TextCurveDown = 153
    TextCascadeUp = 154
    TextCascadeDown = 155
    TextWave1 = 156
    TextWave2 = 157
    TextWave3 = 158
    TextWave4 = 159
    TextInflate = 160
    TextDeflate = 161
    TextInflateBottom = 162
    TextDeflateBottom = 163
    TextInflateTop = 164
    TextDeflateTop = 165
    TextDeflateInflate = 166
    TextDeflateInflateDeflate = 167
    TextFadeRight = 168
    TextFadeLeft = 169
    TextFadeUp = 170
    TextFadeDown = 171
    TextSlantUp = 172
    TextSlantDown = 173
    TextCanUp = 174
    TextCanDown = 175
    FlowChartAlternateProcess = 176
    FlowChartOffpageConnector = 177
    Callout90 = 178
    AccentCallout90 = 179
    BorderCallout90 = 180
    LeftRightUpArrow = 182
    Sun = 183
    Moon = 184
    BracketPair = 185
    BracePair = 186
    Seal4 = 187
    DoubleWave = 188
    ActionButtonBlank = 189
    ActionButtonHome = 190
    ActionButtonHelp = 191
    ActionButtonInformation = 192
    ActionButtonForwardNext = 193
    ActionButtonBackPrevious = 194
    ActionButtonEnd = 195
    ActionButtonBeginning = 196
    ActionButtonReturn = 197
    ActionButtonDocument = 198
    ActionButtonSound = 199
    ActionButtonMovie = 200
    # Snip single corner rectangle object.
    # Applicable only for DML shapes.
    SingleCornerSnipped = 203
    # Snip same side corner rectangle. 
    # Applicable only for DML shapes.
    TopCornersSnipped = 204
    # Snip diagonal corner rectangle.
    # Applicable only for DML shapes.
    DiagonalCornersSnipped = 205
    # Snip and round single corner rectangle.
    # Applicable only for DML shapes.
    TopCornersOneRoundedOneSnipped = 206
    # Round single corner rectangle. 
    # Applicable only for DML shapes.
    SingleCornerRounded = 207
    # Round same side corner rectangle.
    # Applicable only for DML shapes.
    TopCornersRounded = 208
    # Round diagonal corner rectangle.
    # Applicable only for DML shapes.
    DiagonalCornersRounded = 209
    # Heptagon.
    # Applicable only for DML shapes.
    Heptagon = 210
    # Cloud.
    # Applicable only for DML shapes.
    Cloud = 211
    # Six-pointed star.
    # Applicable only for DML shapes.
    Seal6 = 212
    # Seven-pointed star.
    # Applicable only for DML shapes.
    Seal7 = 213
    # Ten-pointed star.
    # Applicable only for DML shapes.
    Seal10 = 214
    # Twelve-pointed star.
    # Applicable only for DML shapes.
    Seal12 = 215
    # Swoosh arrow.
    # Applicable only for DML shapes.
    SwooshArrow = 216
    # Teardrop.
    # Applicable only for DML shapes.
    Teardrop = 217
    # Square tabs.
    # Applicable only for DML shapes.
    SquareTabs = 218
    # Plaque tabs.
    # Applicable only for DML shapes.
    PlaqueTabs = 219
    # Pie. 
    # Applicable only for DML shapes.
    Pie = 220
    # Wedge pie. 
    # Applicable only for DML shapes.
    WedgePie = 221
    # Inverse line.
    # Applicable only for DML shapes.
    InverseLine = 222
    # Math plus. 
    # Applicable only for DML shapes.
    MathPlus = 223
    # Math minus.
    # Applicable only for DML shapes.
    MathMinus = 224
    # Math multiply. 
    # Applicable only for DML shapes.
    MathMultiply = 225
    # Math divide. 
    # Applicable only for DML shapes.
    MathDivide = 226
    # Math equal. 
    # Applicable only for DML shapes.
    MathEqual = 227
    # Math not equal. 
    # Applicable only for DML shapes.
    MathNotEqual = 228
    # Non-isosceles trapezoid. 
    # Applicable only for DML shapes.
    NonIsoscelesTrapezoid = 229
    # Left-right circular arrow. 
    # Applicable only for DML shapes.
    LeftRightCircularArrow = 230
    # Left-right ribbon.
    # Applicable only for DML shapes.
    LeftRightRibbon = 231
    # Left circular arrow.
    # Applicable only for DML shapes.
    LeftCircularArrow = 232
    # Frame.
    # Applicable only for DML shapes.
    Frame = 233
    # Half frame. Applicable only for DML shapes.
    # Applicable only for DML shapes.
    HalfFrame = 234
    # Funnel.
    # Applicable only for DML shapes.
    Funnel = 235
    # Six-tooth gear.
    # Applicable only for DML shapes.
    Gear6 = 236
    # Nine-tooth gear.
    # Applicable only for DML shapes.
    Gear9 = 237
    # Decagon.
    # Applicable only for DML shapes.
    Decagon = 238
    # Dodecagon.
    # Applicable only for DML shapes.
    Dodecagon = 239
    # Diagonal stripe.
    # Applicable only for DML shapes.
    DiagonalStripe = 240
    # Corner.
    # Applicable only for DML shapes.
    Corner = 241
    # Corner tabs.
    # Applicable only for DML shapes.
    CornerTabs = 242
    # Chord.
    # Applicable only for DML shapes.
    Chord = 243
    # Chart plus.
    # Applicable only for DML shapes.
    ChartPlus = 244
    # Chart star.
    # Applicable only for DML shapes.
    ChartStar = 245
    # Chart X.
    # Applicable only for DML shapes.
    ChartX = 246
    # Reserved for the system use.
    MinValue = -2

