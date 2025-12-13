class MwPyMSLVersion():
    Default = "" #MWorks.Sysplorer使用的最新Modelica标准库。
    V2_2_2 = "2.2.2" #Modelica标准库版本 2.2.2。
    V3_0 = "3.0" #Modelica标准库版本 3.0。
    V3_2 = "3.2" #Modelica标准库版本 3.2。
    V3_2_1 = "3.2.1" #Modelica标准库版本 3.2.1。
    V3_2_2 = "3.2.2" #Modelica标准库版本 3.2.2。
    V3_2_3 = "3.2.3" #Modelica标准库版本 3.2.3。
    V4_0 = "4.0.0" #Modelica标准库版本 4.0.0。

class MwPyFMIType():
    ModelExchange = "me" #模型交换类型的FMI。
    CoSimulation = "cs" #联合仿真类型的FMI。

class MwPyFMIVersion():
    V1 = "1" #FMI 1.0 .
    V2 = "2" #FMI 2.0 .
    V3 = "3" #FMI 3.0 .

class MwPyFMIPlatform():
    x86 = "x86" #32位FMI。
    x64 = "x64" #64位FMI。

class MwPyFMI():
    Type = MwPyFMIType()
    Version = MwPyFMIVersion()
    Platform = MwPyFMIPlatform()

class MwPyModelView():
    Icon = "icon" #图标视图。
    Diagram = "diagram" #组件视图。
    Text="text" #文本视图。
    Documentation="info" #文档视图。

class MwPyIntegration():
    Dassl = "Dassl" #积分算法: Dassl。
    Ida = "Ida" #积分算法: Ida。
    Mebdfi = "Mebdfi" #积分算法: Mebdfi。
    Lsodar = "Lsodar" #积分算法: Lsodar。
    Lsode = "Lsode" #积分算法: Lsode。
    Cvode = "Cvode" #积分算法: Cvode。
    Mebdf = "Mebdf" #积分算法: Mebdf。
    Radau5 = "Radau5" #积分算法: Radau5。
    Sdirk34 = "Sdirk34" #积分算法: Sdirk34。
    Esdirk23 = "Esdirk23" #积分算法: Esdirk23。
    Esdirk34 = "Esdirk34" #积分算法: Esdirk34。
    Esdirk45 = "Esdirk45" #积分算法: Esdirk45。
    Dopri5 = "Dopri5" #积分算法: Dopri5。
    Dop853 = "Dop853" #积分算法: Dop853。
    Euler = "Euler" #积分算法: Euler。
    Rkfix2 = "Rkfix2" #积分算法: Rkfix2。
    Rkfix3 = "Rkfix3" #积分算法: Rkfix3。
    Rkfix4 = "Rkfix4" #积分算法: Rkfix4。
    Rkfix6 = "Rkfix6" #积分算法: Rkfix6。
    Rkfix8 = "Rkfix8" #积分算法: Rkfix8。
    ImplicitEuler = "ImplicitEuler" #积分算法: ImplicitEuler。
    ImplicitTrapezoid = "ImplicitTrapezoid" #积分算法: ImplicitTrapezoid。
    InlineImplicitEuler = "InlineImplicitEuler" #积分算法: InlineImplicitEuler。
    InlineImplicitTrapezoid = "InlineImplicitTrapezoid" #积分算法: InlineImplicitTrapezoid。

class MwPyResultFormat():
    Default = "msr" #默认的结果文件格式。
    Mat = "mat" #Matlab的".mat"文件格式。
    Csv = "csv" #csv(逗号分隔)文件格式。

class MwPyLegendLayout():
    EmbeddedTop = 1 #图例布局：嵌入上边。
    EmbeddedBottom = 2 #图例布局：嵌入下边。
    EmbeddedLeft = 3 #图例布局：嵌入左边。
    EmbeddedRight = 4 #图例布局：嵌入右边。
    FloatingTopLeft = 5 #图例布局：浮动位于左上。
    FloatingTopCenter = 6 #图例布局：浮动位于正上。
    FloatingTopRight = 7 #图例布局：浮动位于右上。
    FloatingCenterLeft = 8 #图例布局：浮动位于左边。
    FloatingCenterRight = 9 #图例布局：浮动位于右边。
    FloatingBottomLeft = 10 #图例布局：浮动位于左下。
    FloatingBottomCenter = 11 #图例布局：浮动位于正下。
    FloatingBottomRight = 12 #图例布局：浮动位于右下。
    Hide = 13 #图例布局：隐藏。

class MwPyAxisTitleType():
    None_ = 0 #无轴标题。
    Default = 1 #使用默认的轴标题。
    Custom = 2 #自定义的轴标题。

class MwPyLineStyle():
    Solid = 1 #实线。
    Dashed = 2 #虚线。
    Dotted = 3 #点线。
    DashDot = 4 #点划线。
    DashDotDot = 5 #双点划线。
LineStyle = MwPyLineStyle()

class MwPyLineColor():
    Blue = 0x0000ff #蓝色。
    Red  = 0xff0000 #红色。
    Green = 0x008000 #绿色。
    Magenta = 0xff00ff #洋红。
    Black = 0x000000 #黑色。
    Yellow = 0xffff00 #黄色。
    Purple = 0xA020F0 #紫色。
    Brown = 0x802A2A #棕色。

class MwPyLineThickness():
    Single = 1 #单倍线宽。
    Double = 2 #双倍线宽。
    Quad = 4 #四倍线宽。

class MwPyMarkerStyle():
    None_ = 0 #不显示数据点。
    Cross = 1 #交叉形。
    Circle = 2 #圆形。
    Square = 3 #正方形。
    FilledCircle = 4 #实心圆。
    FilledSquare = 5 #实心正方形。
    TriangleDown = 6 #倒三角形。
    TriangleUp = 7 #正三角形。
    Diamond = 8 #菱形。

class MwPyVerticalAxis():
    Left = 1 #左纵轴。
    Right = -1 #右纵轴。

class MwPyPlotFileFormat():
    Image = 1 #曲线导出为图片。
    Csv = 2 #曲线导出为csv文件。
    Mat = 3 #曲线导出为".mat"文件。
    Text = 4 #曲线导出为文本文件。

class MwPyExperiment():
    startTime = "startTime" #起始时刻
    stopTime = "stopTime" #结束时刻
    intervalLength = "intervalLength" #输出区间长度
    numberOfIntervals = "numberOfIntervals" #输出区间个数
    useIntervalLength = "useIntervalLength" #使用输出区间长度
    algorithm = "algorithm" #仿真算法
    tolerance = "tolerance" #仿真容差
    fixedOrInitStepSize = "fixedOrInitStepSize" #仿真积分步长
    saveEvent = "saveEvent" #是否存储事件时刻变量值
    saveAsDouble = "saveAsDouble" #是否以double格式存储变量值

class MwPySimulationTime():
    Begin = "begin" #仿真起始时刻。
    End = "end" #仿真结束时刻。

class MwTreeViewLabels():
    MwTreeViewLabName = "Name" #模型名
    MwTreeViewLabComment = "Comment" #模型描述
    MwTreeViewLabNameComment = "NameComment" #模型名（描述）

class MwCompilerType():
    MwCcmplBuiltInGcc = 'Built-in-gcc' #内置 gcc
    MwCcmplCustomGcc = 'CustomGcc' #自定义 gcc
    MwCcmplAutoCheckVc = 'AutoDetect' #自动检测的 vc
    MwCcmplCustomVc = 'CustomVc' #自定义 vc

class MwShapeType():
    Line = 'Line' #线段
    Lines = 'Lines' #多段线
    Polygon = 'Polygon' #多边形
    Triangle = 'Triangle' #三角形
    Rectangle = 'Rectangle' #矩形
    Ellipse = 'Ellipse' #椭圆
    Text = 'Text' #文字
    Bitmap = 'Bitmap' #图片

class MwTextAlignment():
    Left = 'Left' #左对齐
    Center = 'Center' #居中
    Right = 'Right' #右对齐

class MwFillPattern():
    Solid = 'Solid' #实心
    Horizontal = 'Horizontal' #水平线
    Vertical = 'Vertical' #垂直线
    Cross = 'Cross' #纵横交叉线
    Forward = 'Forward' #-45度斜线
    Backward = 'Backward' #45度斜线
    CrossDiag = 'CrossDiag' #45度斜交叉线
    HorizontalCylinder = 'HorizontalCylinder' #水平圆柱面
    VerticalCylinder = 'VerticalCylinder' #垂直圆柱面

class MwLinePattern():
    Solid = 'Solid' #实线
    Dash = 'Dash' #虚线
    Dot = 'Dot' #点线
    DashDot = 'DashDot' #点划线
    DashDotDot = 'DashDotDot' #双点划线

class MwBorderPattern():
    Raised = 'Raised' #凸起
    Sunken = 'Sunken' #凹陷
    Engraved = 'Engraved' #雕刻

class MwArrowPattern():
    Open = 'Open' #空心
    Filled = 'Filled' #实心
    Half = 'Half' #半空心

class MwSmooth():
    none = 'None' #不光滑
    Bezier = 'Bezier' #光滑

class MwShapeStyle():
    textColor = [0,0,0] #文字颜色
    textSize = 0 #文字字号
    textFont = '' #文字字体
    fillColor = [255,255,255] #填充颜色
    fillPattern = None #填充样式
    lineColor = [0,0,0] #边框颜色
    linePattern = MwLinePattern.Solid #边框样式
    lineWidth = 0.25 #边框粗细
    radius = 0 #圆角
    borderPattern = None #效果
    arrowStart = None #箭头起点
    arrowEnd = None #箭头终点
    arrowSize = 3 #箭头大小
    textBold = False #文字加粗
    textItalic = False #文字斜体
    textUnderLine = False #文字下划线
    horizontalAlignment = MwTextAlignment.Left #文字对齐
    smooth = MwSmooth.none #光滑
    manhattanize = False #保持横平竖直

class MwEncryptLevel():
    packageDuplicate = "Access.packageDuplicate" 
    nonPackageDuplicate = "Access.nonPackageDuplicate"
    packageText = "Access.packageText"
    nonPackageText = "Access.nonPackageText"
    diagram = "Access.diagram"
    documentation = "Access.documentation"
    icon = "Access.icon"
    hide = "Access.hide"
    default = "Default"