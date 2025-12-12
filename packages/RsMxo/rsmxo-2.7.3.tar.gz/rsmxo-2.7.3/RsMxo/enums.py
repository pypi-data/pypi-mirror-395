from enum import Enum


# noinspection SpellCheckingInspection
class AbsRel(Enum):
	"""2 Members, ABS ... REL"""
	ABS = 0
	REL = 1


# noinspection SpellCheckingInspection
class AcqMd(Enum):
	"""4 Members, AVERage ... SAMPle"""
	AVERage = 0
	ENVelope = 1
	PDETect = 2
	SAMPle = 3


# noinspection SpellCheckingInspection
class AdLogic(Enum):
	"""4 Members, AND ... OR"""
	AND = 0
	NAND = 1
	NOR = 2
	OR = 3


# noinspection SpellCheckingInspection
class Algorithm(Enum):
	"""4 Members, CFRequency ... PLLRlock"""
	CFRequency = 0
	FF = 1
	PLL = 2
	PLLRlock = 3


# noinspection SpellCheckingInspection
class AmplitudeMode(Enum):
	"""2 Members, CONStant ... PROFile"""
	CONStant = 0
	PROFile = 1


# noinspection SpellCheckingInspection
class AmplitudeProfileVoltageChange(Enum):
	"""2 Members, RAMP ... SINGle"""
	RAMP = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class AnalogChannels(Enum):
	"""8 Members, C1 ... C8"""
	C1 = 0
	C2 = 1
	C3 = 2
	C4 = 3
	C5 = 4
	C6 = 5
	C7 = 6
	C8 = 7


# noinspection SpellCheckingInspection
class AnalogCutoffFreq(Enum):
	"""3 Members, KHZ5 ... MHZ50"""
	KHZ5 = 0
	KHZ50 = 1
	MHZ50 = 2


# noinspection SpellCheckingInspection
class AreaCombination(Enum):
	"""55 Members, ABS ... XOR"""
	ABS = 0
	ACORrrelat = 1
	ACOS = 2
	ADD = 3
	AND = 4
	ASIN = 5
	ATAN = 6
	BWC = 7
	CDR = 8
	CORRelation = 9
	COS = 10
	COSH = 11
	DERivation = 12
	DIV = 13
	ELECPOWER = 14
	EQUal = 15
	EXP = 16
	FIR = 17
	GDELay = 18
	GEQual = 19
	GREater = 20
	IFFT = 21
	IMG = 22
	INTegral = 23
	INVert = 24
	LD = 25
	LEQual = 26
	LESS = 27
	LN = 28
	LOG = 29
	MA = 30
	MAG = 31
	MUL = 32
	NAND = 33
	NOR = 34
	NOT = 35
	NXOR = 36
	OR = 37
	PHI = 38
	POW = 39
	POWRational = 40
	POWZ = 41
	RE = 42
	RECiprocal = 43
	RESCale = 44
	SIN = 45
	SINC = 46
	SINH = 47
	SQRT = 48
	SUB = 49
	TAN = 50
	TANH = 51
	TOBit = 52
	UNEQual = 53
	XOR = 54


# noinspection SpellCheckingInspection
class AutoManualMode(Enum):
	"""2 Members, AUTO ... MANual"""
	AUTO = 0
	MANual = 1


# noinspection SpellCheckingInspection
class AutoUser(Enum):
	"""2 Members, AUTO ... USER"""
	AUTO = 0
	USER = 1


# noinspection SpellCheckingInspection
class AxisMode(Enum):
	"""2 Members, LIN ... LOG"""
	LIN = 0
	LOG = 1


# noinspection SpellCheckingInspection
class BitOrder(Enum):
	"""2 Members, LSBF ... MSBF"""
	LSBF = 0
	MSBF = 1


# noinspection SpellCheckingInspection
class ByteOrder(Enum):
	"""2 Members, LSBFirst ... MSBFirst"""
	LSBFirst = 0
	MSBFirst = 1


# noinspection SpellCheckingInspection
class ClockSource(Enum):
	"""16 Members, D0 ... D9"""
	D0 = 0
	D1 = 1
	D10 = 2
	D11 = 3
	D12 = 4
	D13 = 5
	D14 = 6
	D15 = 7
	D2 = 8
	D3 = 9
	D4 = 10
	D5 = 11
	D6 = 12
	D7 = 13
	D8 = 14
	D9 = 15


# noinspection SpellCheckingInspection
class Color(Enum):
	"""20 Members, BLUE ... YELLow"""
	BLUE = 0
	DAGReen = 1
	DGRay = 2
	DORange = 3
	GRAY = 4
	GREen = 5
	LBLue = 6
	LGRay = 7
	LIGReen = 8
	LORange = 9
	LPINk = 10
	LPURple = 11
	MGRay = 12
	ORANge = 13
	PINK = 14
	PURPle = 15
	RED = 16
	TURQuoise = 17
	WHITe = 18
	YELLow = 19


# noinspection SpellCheckingInspection
class ColorTable(Enum):
	"""4 Members, FalseColors ... Temperature"""
	FalseColors = "'FalseColors'"
	SingleEvent = "'SingleEvent'"
	Spectrum = "'Spectrum'"
	Temperature = "'Temperature'"


# noinspection SpellCheckingInspection
class Column(Enum):
	"""4 Members, COL1 ... NONE"""
	COL1 = 0
	COL2 = 1
	COL3 = 2
	NONE = 3


# noinspection SpellCheckingInspection
class ContentType(Enum):
	"""4 Members, DIAG ... RES"""
	DIAG = 0
	NODE = 1
	NONE = 2
	RES = 3


# noinspection SpellCheckingInspection
class Coupling(Enum):
	"""3 Members, AC ... DCLimit"""
	AC = 0
	DC = 1
	DCLimit = 2


# noinspection SpellCheckingInspection
class CouplingMode(Enum):
	"""4 Members, CURSor ... ZOOM"""
	CURSor = 0
	MANual = 1
	SPECtrum = 2
	ZOOM = 3


# noinspection SpellCheckingInspection
class CrcCalculation(Enum):
	"""2 Members, SAEJ ... TLE"""
	SAEJ = 0
	TLE = 1


# noinspection SpellCheckingInspection
class CrcVersion(Enum):
	"""2 Members, LEGA ... V2010"""
	LEGA = 0
	V2010 = 1


# noinspection SpellCheckingInspection
class Cursor(Enum):
	"""4 Members, CURSOR1 ... CURSOR4"""
	CURSOR1 = 0
	CURSOR2 = 1
	CURSOR3 = 2
	CURSOR4 = 3


# noinspection SpellCheckingInspection
class CursorStyle(Enum):
	"""4 Members, LINes ... VLRHombus"""
	LINes = 0
	LRHombus = 1
	RHOMbus = 2
	VLRHombus = 3


# noinspection SpellCheckingInspection
class CursorType(Enum):
	"""3 Members, HORizontal ... VERTical"""
	HORizontal = 0
	PAIRed = 1
	VERTical = 2


# noinspection SpellCheckingInspection
class DataAlignment(Enum):
	"""2 Members, BIT ... WORD"""
	BIT = 0
	WORD = 1


# noinspection SpellCheckingInspection
class DataFormat(Enum):
	"""3 Members, ASCii ... REAL"""
	ASCii = 0
	INT = 1
	REAL = 2


# noinspection SpellCheckingInspection
class Detection(Enum):
	"""2 Members, DETected ... NDETected"""
	DETected = 0
	NDETected = 1


# noinspection SpellCheckingInspection
class DiagramStyle(Enum):
	"""2 Members, DOTS ... VECTors"""
	DOTS = 0
	VECTors = 1


# noinspection SpellCheckingInspection
class DispedHarmonics(Enum):
	"""4 Members, ALL ... STANdard"""
	ALL = 0
	EVEN = 1
	ODD = 2
	STANdard = 3


# noinspection SpellCheckingInspection
class DisplayDiff(Enum):
	"""2 Members, DIFFerential ... SINGleended"""
	DIFFerential = 0
	SINGleended = 1


# noinspection SpellCheckingInspection
class Edge(Enum):
	"""3 Members, BOTH ... RISE"""
	BOTH = 0
	FALL = 1
	RISE = 2


# noinspection SpellCheckingInspection
class EdgeCntDirct(Enum):
	"""2 Members, FRFI ... FRLA"""
	FRFI = 0
	FRLA = 1


# noinspection SpellCheckingInspection
class Endianness(Enum):
	"""2 Members, BENDian ... LENDian"""
	BENDian = 0
	LENDian = 1


# noinspection SpellCheckingInspection
class EnvelopeCurve(Enum):
	"""3 Members, BOTH ... MIN"""
	BOTH = 0
	MAX = 1
	MIN = 2


# noinspection SpellCheckingInspection
class EventsMode(Enum):
	"""2 Members, SEQuence ... SINGle"""
	SEQuence = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class ExportScope(Enum):
	"""5 Members, ALL ... MANual"""
	ALL = 0
	CURSor = 1
	DISPlay = 2
	GATE = 3
	MANual = 4


# noinspection SpellCheckingInspection
class FileExtension(Enum):
	"""19 Members, BIN ... ZIP"""
	BIN = 0
	CMD = 1
	CSV = 2
	DMO = 3
	EXE = 4
	GEN = 5
	H5 = 6
	JPG = 7
	PNG = 8
	PTT = 9
	PY = 10
	REF = 11
	RSI = 12
	S2P = 13
	S4P = 14
	SET = 15
	SVG = 16
	XML = 17
	ZIP = 18


# noinspection SpellCheckingInspection
class FormErrorCause(Enum):
	"""5 Members, ACKDerror ... RESerror"""
	ACKDerror = 0
	CRCDerror = 1
	FSBE = 2
	NONE = 3
	RESerror = 4


# noinspection SpellCheckingInspection
class FrameType(Enum):
	"""7 Members, BADX ... TCOD"""
	BADX = 0
	DATA = 1
	EEP = 2
	EOP = 3
	FCT = 4
	NULL = 5
	TCOD = 6


# noinspection SpellCheckingInspection
class FrAnalysisCalStates(Enum):
	"""4 Members, FAIL ... RUN"""
	FAIL = 0
	NOAL = 1
	PASS = 2
	RUN = 3


# noinspection SpellCheckingInspection
class FundamentalFreqEn61000(Enum):
	"""3 Members, AUTO ... F60"""
	AUTO = 0
	F50 = 1
	F60 = 2


# noinspection SpellCheckingInspection
class FundamentalFreqMil(Enum):
	"""2 Members, F400 ... F60"""
	F400 = 0
	F60 = 1


# noinspection SpellCheckingInspection
class FundamentalFreqRtca(Enum):
	"""3 Members, F400 ... WVF"""
	F400 = 0
	NVF = 1
	WVF = 2


# noinspection SpellCheckingInspection
class GeneratorChannel(Enum):
	"""2 Members, GEN1 ... GEN2"""
	GEN1 = 0
	GEN2 = 1


# noinspection SpellCheckingInspection
class GenSyncCombination(Enum):
	"""2 Members, GEN12 ... NONE"""
	GEN12 = 0
	NONE = 1


# noinspection SpellCheckingInspection
class HiLowMode(Enum):
	"""3 Members, EITHer ... LOW"""
	EITHer = 0
	HIGH = 1
	LOW = 2


# noinspection SpellCheckingInspection
class HistMode(Enum):
	"""2 Members, HORizontal ... VERTical"""
	HORizontal = 0
	VERTical = 1


# noinspection SpellCheckingInspection
class Hlx(Enum):
	"""3 Members, DONTcare ... LOW"""
	DONTcare = 0
	HIGH = 1
	LOW = 2


# noinspection SpellCheckingInspection
class HorizontalMode(Enum):
	"""2 Members, COUPled ... ORIGinal"""
	COUPled = 0
	ORIGinal = 1


# noinspection SpellCheckingInspection
class HorizontalUnit(Enum):
	"""2 Members, ATIMe ... UI"""
	ATIMe = 0
	UI = 1


# noinspection SpellCheckingInspection
class Hysteresis(Enum):
	"""3 Members, MAXimum ... ROBust"""
	MAXimum = 0
	NORMal = 1
	ROBust = 2


# noinspection SpellCheckingInspection
class InitialPhase(Enum):
	"""2 Members, DATaedge ... SAMPle"""
	DATaedge = 0
	SAMPle = 1


# noinspection SpellCheckingInspection
class Intersection(Enum):
	"""2 Members, MUST ... NOT"""
	MUST = 0
	NOT = 1


# noinspection SpellCheckingInspection
class IntpolMd(Enum):
	"""3 Members, LINear ... SMHD"""
	LINear = 0
	SINX = 1
	SMHD = 2


# noinspection SpellCheckingInspection
class LabelBorder(Enum):
	"""2 Members, FULL ... NOBorder"""
	FULL = 0
	NOBorder = 1


# noinspection SpellCheckingInspection
class LayoutSplitType(Enum):
	"""6 Members, BODE ... ZOOM"""
	BODE = 0
	HOR = 1
	NONE = 2
	SPEC = 3
	VERT = 4
	ZOOM = 5


# noinspection SpellCheckingInspection
class LowHigh(Enum):
	"""2 Members, HIGH ... LOW"""
	HIGH = 0
	LOW = 1


# noinspection SpellCheckingInspection
class MagnitudeUnit(Enum):
	"""7 Members, DB ... LINear"""
	DB = 0
	DBHZ = 1
	DBM = 2
	DBS = 3
	DBUV = 4
	DBV = 5
	LINear = 6


# noinspection SpellCheckingInspection
class MeasDelayMode(Enum):
	"""2 Members, PERiod ... TIME"""
	PERiod = 0
	TIME = 1


# noinspection SpellCheckingInspection
class MeasRbw(Enum):
	"""3 Members, HIGH ... MID"""
	HIGH = 0
	LOW = 1
	MID = 2


# noinspection SpellCheckingInspection
class MeasType(Enum):
	"""127 Members, ACPower ... WSAMples"""
	ACPower = 0
	ACTivepower = 1
	AMMod = 2
	AMPLitude = 3
	APOWer = 4
	AREA = 5
	BIDLe = 6
	BWIDth = 7
	CAMPlitude = 8
	CCDutycycle = 9
	CCJitter = 10
	CCWidth = 11
	CFER = 12
	CMAXimum = 13
	CMINimum = 14
	CPDelta = 15
	CPOWer = 16
	CPPercent = 17
	CRESt = 18
	CYCarea = 19
	CYCCrest = 20
	CYCMean = 21
	CYCRms = 22
	CYCStddev = 23
	DCDistortion = 24
	DELay = 25
	DRATe = 26
	DTOTrigger = 27
	EAMPlitude = 28
	EBASe = 29
	EBRate = 30
	EDGecount = 31
	EFTime = 32
	EHEight = 33
	ERDB = 34
	ERPercent = 35
	ERTime = 36
	ETOP = 37
	EWIDth = 38
	F2F = 39
	F2T = 40
	FCNT = 41
	FEC = 42
	FER = 43
	FLDValue = 44
	FREQuency = 45
	FTIMe = 46
	GAP = 47
	HAR = 48
	HIGH = 49
	HMAXimum = 50
	HMEan = 51
	HMINimum = 52
	HOLD = 53
	HPEak = 54
	HSAMples = 55
	HSTDdev = 56
	LOW = 57
	LPEakvalue = 58
	M1STddev = 59
	M2STddev = 60
	M3STddev = 61
	MAXimum = 62
	MAXMin = 63
	MBITrate = 64
	MEAN = 65
	MEDian = 66
	MINimum = 67
	MKNegative = 68
	MKPositive = 69
	NCJitter = 70
	NDCYcle = 71
	NOVershoot = 72
	NPULse = 73
	NSWitching = 74
	OBWidth = 75
	PDCYcle = 76
	PDELta = 77
	PEAK = 78
	PERiod = 79
	PHASe = 80
	PLISt = 81
	POVershoot = 82
	POWerfactor = 83
	PPHase = 84
	PPJitter = 85
	PPULse = 86
	PROBemeter = 87
	PSWitching = 88
	PULCnt = 89
	PULSetrain = 90
	QFACtor = 91
	REACpower = 92
	RMS = 93
	RMSJitter = 94
	RMSNoise = 95
	RSERr = 96
	RTIMe = 97
	SBITrate = 98
	SBWidth = 99
	SETup = 100
	SHR = 101
	SHT = 102
	SKWDelay = 103
	SKWPhase = 104
	SLEFalling = 105
	SLERising = 106
	SNRatio = 107
	STDDev = 108
	STDJitter = 109
	T2F = 110
	THD = 111
	THDA = 112
	THDF = 113
	THDPCT = 114
	THDR = 115
	THDU = 116
	TIE = 117
	TMAX = 118
	TMIN = 119
	TOI = 120
	UINTerval = 121
	UPEakvalue = 122
	VNOVershoot = 123
	VPOVershoot = 124
	WCOunt = 125
	WSAMples = 126


# noinspection SpellCheckingInspection
class MeterBandwidth(Enum):
	"""8 Members, B100 ... B5M"""
	B100 = 0
	B10M = 1
	B1M = 2
	B200 = 3
	B20M = 4
	B2M = 5
	B500 = 6
	B5M = 7


# noinspection SpellCheckingInspection
class ModulationType(Enum):
	"""6 Members, AM ... PWM"""
	AM = 0
	ASK = 1
	FM = 2
	FSK = 3
	NONE = 4
	PWM = 5


# noinspection SpellCheckingInspection
class NormalInverted(Enum):
	"""2 Members, INVerted ... NORMal"""
	INVerted = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class OnOffType(Enum):
	"""2 Members, TOFF ... TON"""
	TOFF = 0
	TON = 1


# noinspection SpellCheckingInspection
class OperatorA(Enum):
	"""8 Members, ANY ... NEQual"""
	ANY = 0
	EQUal = 1
	GETHan = 2
	GTHan = 3
	INRange = 4
	LETHan = 5
	LTHan = 6
	NEQual = 7


# noinspection SpellCheckingInspection
class OperatorB(Enum):
	"""9 Members, EQUal ... OORange"""
	EQUal = 0
	GETHan = 1
	GTHan = 2
	INRange = 3
	LETHan = 4
	LTHan = 5
	NEQual = 6
	OFF = 7
	OORange = 8


# noinspection SpellCheckingInspection
class PeriodSlope(Enum):
	"""4 Members, EITHer ... POSitive"""
	EITHer = 0
	FIRSt = 1
	NEGative = 2
	POSitive = 3


# noinspection SpellCheckingInspection
class PhaseMode(Enum):
	"""2 Members, DEGRees ... RADians"""
	DEGRees = 0
	RADians = 1


# noinspection SpellCheckingInspection
class PictureFileFormat(Enum):
	"""5 Members, BMP ... TIFF"""
	BMP = 0
	JPG = 1
	PDF = 2
	PNG = 3
	TIFF = 4


# noinspection SpellCheckingInspection
class PllOrder(Enum):
	"""2 Members, FIRSt ... SECond"""
	FIRSt = 0
	SECond = 1


# noinspection SpellCheckingInspection
class PointsMode(Enum):
	"""2 Members, DECade ... TOTal"""
	DECade = 0
	TOTal = 1


# noinspection SpellCheckingInspection
class PowerCoupling(Enum):
	"""2 Members, AC ... DC"""
	AC = 0
	DC = 1


# noinspection SpellCheckingInspection
class PowerType(Enum):
	"""6 Members, EFFiciency ... SWITching"""
	EFFiciency = 0
	HARMonics = 1
	ONOFf = 2
	QUALity = 3
	SOA = 4
	SWITching = 5


# noinspection SpellCheckingInspection
class PowerUnit(Enum):
	"""2 Members, ENERgy ... POWer"""
	ENERgy = 0
	POWer = 1


# noinspection SpellCheckingInspection
class PqualFundamentalFreq(Enum):
	"""5 Members, AUTO ... USER"""
	AUTO = 0
	F400 = 1
	F50 = 2
	F60 = 3
	USER = 4


# noinspection SpellCheckingInspection
class PrintTarget(Enum):
	"""3 Members, CLIPBOARD ... PRINTER"""
	CLIPBOARD = 0
	MMEM = 1
	PRINTER = 2


# noinspection SpellCheckingInspection
class ProbeAdapterType(Enum):
	"""2 Members, NONE ... Z2T"""
	NONE = 0
	Z2T = 1


# noinspection SpellCheckingInspection
class ProbeAttUnits(Enum):
	"""3 Members, A ... W"""
	A = 0
	V = 1
	W = 2


# noinspection SpellCheckingInspection
class ProbeMeasMode(Enum):
	"""4 Members, CMODe ... PMODe"""
	CMODe = 0
	DMODe = 1
	NMODe = 2
	PMODe = 3


# noinspection SpellCheckingInspection
class ProbeRange(Enum):
	"""3 Members, AUTO ... MLOW"""
	AUTO = 0
	MHIGh = 1
	MLOW = 2


# noinspection SpellCheckingInspection
class ProbeSetupMode(Enum):
	"""12 Members, AUToset ... SITFile"""
	AUToset = 0
	AZERo = 1
	FTRiglevel = 2
	NOACtion = 3
	OTMean = 4
	PRINt = 5
	PROBemode = 6
	PRSetup = 7
	RCONtinuous = 8
	REPort = 9
	RSINgle = 10
	SITFile = 11


# noinspection SpellCheckingInspection
class ProbeTipModel(Enum):
	"""8 Members, NONE ... Z302"""
	NONE = 0
	UNKNOWN = 1
	Z101 = 2
	Z201 = 3
	Z202 = 4
	Z203 = 5
	Z301 = 6
	Z302 = 7


# noinspection SpellCheckingInspection
class ProcessState(Enum):
	"""3 Members, OFF ... STOP"""
	OFF = 0
	RUN = 1
	STOP = 2


# noinspection SpellCheckingInspection
class ProtocolType(Enum):
	"""20 Members, ARIN429 ... UART"""
	ARIN429 = 0
	CAN = 1
	EBTB = 2
	HBTO = 3
	I2C = 4
	I3C = 5
	LIN = 6
	MANC = 7
	MILS1553 = 8
	NRZC = 9
	NRZU = 10
	QSPI = 11
	RFFE = 12
	SENT = 13
	SPI = 14
	SPMI = 15
	SWIR = 16
	TBTO = 17
	TNOS = 18
	UART = 19


# noinspection SpellCheckingInspection
class PulseSlope(Enum):
	"""3 Members, EITHer ... POSitive"""
	EITHer = 0
	NEGative = 1
	POSitive = 2


# noinspection SpellCheckingInspection
class PwrHarmonicsRevision(Enum):
	"""2 Members, REV2011 ... REV2019"""
	REV2011 = 0
	REV2019 = 1


# noinspection SpellCheckingInspection
class PwrHarmonicsStandard(Enum):
	"""6 Members, ENA ... RTCA"""
	ENA = 0
	ENB = 1
	ENC = 2
	END = 3
	MIL = 4
	RTCA = 5


# noinspection SpellCheckingInspection
class RangeMode(Enum):
	"""4 Members, LONGer ... WITHin"""
	LONGer = 0
	OUTSide = 1
	SHORter = 2
	WITHin = 3


# noinspection SpellCheckingInspection
class ReferenceLevel(Enum):
	"""3 Members, LOWer ... UPPer"""
	LOWer = 0
	MIDDle = 1
	UPPer = 2


# noinspection SpellCheckingInspection
class RelativeLevels(Enum):
	"""4 Members, FIVE ... USER"""
	FIVE = 0
	TEN = 1
	TWENty = 2
	USER = 3


# noinspection SpellCheckingInspection
class RelativePolarity(Enum):
	"""2 Members, INVerse ... MATChing"""
	INVerse = 0
	MATChing = 1


# noinspection SpellCheckingInspection
class Result(Enum):
	"""2 Members, FAIL ... PASS"""
	FAIL = 0
	PASS = 1


# noinspection SpellCheckingInspection
class ResultColumn(Enum):
	"""2 Members, FREQ ... VAL"""
	FREQ = 0
	VAL = 1


# noinspection SpellCheckingInspection
class ResultFileType(Enum):
	"""4 Members, CSV ... XML"""
	CSV = 0
	HTML = 1
	PY = 2
	XML = 3


# noinspection SpellCheckingInspection
class ResultOrder(Enum):
	"""2 Members, ASC ... DESC"""
	ASC = 0
	DESC = 1


# noinspection SpellCheckingInspection
class ResultState(Enum):
	"""3 Members, FAILed ... PASSed"""
	FAILed = 0
	NOALigndata = 1
	PASSed = 2


# noinspection SpellCheckingInspection
class SbusAckBit(Enum):
	"""3 Members, ACK ... NACK"""
	ACK = 0
	EITHer = 1
	NACK = 2


# noinspection SpellCheckingInspection
class SbusArincFrameState(Enum):
	"""6 Members, CODE ... UNKN"""
	CODE = 0
	GAP = 1
	INC = 2
	OK = 3
	PAR = 4
	UNKN = 5


# noinspection SpellCheckingInspection
class SbusArincPolarity(Enum):
	"""2 Members, ALEG ... BLEG"""
	ALEG = 0
	BLEG = 1


# noinspection SpellCheckingInspection
class SbusBitState(Enum):
	"""3 Members, DC ... ZERO"""
	DC = 0
	ONE = 1
	ZERO = 2


# noinspection SpellCheckingInspection
class SbusCanFrameOverallState(Enum):
	"""3 Members, ERRor ... UNDF"""
	ERRor = 0
	OK = 1
	UNDF = 2


# noinspection SpellCheckingInspection
class SbusCanFrameState(Enum):
	"""11 Members, ACKD ... UNKNown"""
	ACKD = 0
	BTST = 1
	CRC = 2
	CRCD = 3
	EOFD = 4
	FORM = 5
	INComplete = 6
	NOACk = 7
	OK = 8
	SERRror = 9
	UNKNown = 10


# noinspection SpellCheckingInspection
class SbusCanFrameType(Enum):
	"""10 Members, CBFF ... XLFF"""
	CBFF = 0
	CBFR = 1
	CEFF = 2
	CEFR = 3
	ERRor = 4
	FBFF = 5
	FEFF = 6
	OVERload = 7
	UNDefined = 8
	XLFF = 9


# noinspection SpellCheckingInspection
class SbusCanIdentifierType(Enum):
	"""2 Members, B11 ... B29"""
	B11 = 0
	B29 = 1


# noinspection SpellCheckingInspection
class SbusCanSignalType(Enum):
	"""2 Members, CANH ... CANL"""
	CANH = 0
	CANL = 1


# noinspection SpellCheckingInspection
class SbusCanTransceiverMode(Enum):
	"""2 Members, FAST ... SIC"""
	FAST = 0
	SIC = 1


# noinspection SpellCheckingInspection
class SbusCanTriggerType(Enum):
	"""7 Members, EDOF ... SYMB"""
	EDOF = 0
	ERRC = 1
	FTYP = 2
	ID = 3
	IDDT = 4
	STOF = 5
	SYMB = 6


# noinspection SpellCheckingInspection
class SbusDataFormat(Enum):
	"""10 Members, ASCII ... USIG"""
	ASCII = 0
	AUTO = 1
	BIN = 2
	DEC = 3
	HEX = 4
	OCT = 5
	SIGN = 6
	STRG = 7
	SYMB = 8
	USIG = 9


# noinspection SpellCheckingInspection
class SbusFrameCondition(Enum):
	"""2 Members, CLKTimeout ... CS"""
	CLKTimeout = 0
	CS = 1


# noinspection SpellCheckingInspection
class SbusHbtoFrameState(Enum):
	"""7 Members, ECRC ... UNCorrelated"""
	ECRC = 0
	ELENgth = 1
	EPRMble = 2
	ESFD = 3
	INComplete = 4
	OK = 5
	UNCorrelated = 6


# noinspection SpellCheckingInspection
class SbusHbtoFrameType(Enum):
	"""4 Members, FILLer ... UNKNown"""
	FILLer = 0
	IDLE = 1
	MAC = 2
	UNKNown = 3


# noinspection SpellCheckingInspection
class SbusHbtoMode(Enum):
	"""3 Members, AUTO ... SUB"""
	AUTO = 0
	MAIN = 1
	SUB = 2


# noinspection SpellCheckingInspection
class SBusI2cAddressType(Enum):
	"""5 Members, ANY ... BIT7RW"""
	ANY = 0
	AUTO = 1
	BIT10 = 2
	BIT7 = 3
	BIT7RW = 4


# noinspection SpellCheckingInspection
class SbusI2cFrameState(Enum):
	"""5 Members, ADDifferent ... UNKNown"""
	ADDifferent = 0
	INComplete = 1
	NOSTop = 2
	OK = 3
	UNKNown = 4


# noinspection SpellCheckingInspection
class SbusI2cTriggerType(Enum):
	"""7 Members, ADAT ... STOP"""
	ADAT = 0
	ADDRess = 1
	DATA = 2
	NACK = 3
	REPStart = 4
	STARt = 5
	STOP = 6


# noinspection SpellCheckingInspection
class SbusI3cFrameState(Enum):
	"""7 Members, ACK ... UNKNown"""
	ACK = 0
	CRC = 1
	INComplete = 2
	LENGth = 3
	OK = 4
	PAR = 5
	UNKNown = 6


# noinspection SpellCheckingInspection
class SbusI3cFrameType(Enum):
	"""8 Members, BRDC ... WRIT"""
	BRDC = 0
	DRCT = 1
	HDDR = 2
	HTSX = 3
	PROB = 4
	READ = 5
	UNKNown = 6
	WRIT = 7


# noinspection SpellCheckingInspection
class SbusIxcReadWriteBit(Enum):
	"""4 Members, EITHer ... WRITe"""
	EITHer = 0
	READ = 1
	UNDefined = 2
	WRITe = 3


# noinspection SpellCheckingInspection
class SbusLinFrameState(Enum):
	"""9 Members, CHCKsum ... WAKeup"""
	CHCKsum = 0
	INComplete = 1
	LNERror = 2
	OK = 3
	PRERror = 4
	STERror = 5
	SYERror = 6
	UNK = 7
	WAKeup = 8


# noinspection SpellCheckingInspection
class SBusLinStandard(Enum):
	"""4 Members, AUTO ... V2X"""
	AUTO = 0
	J2602 = 1
	V1X = 2
	V2X = 3


# noinspection SpellCheckingInspection
class SbusLinTriggerType(Enum):
	"""5 Members, ERRC ... WKFR"""
	ERRC = 0
	ID = 1
	IDDT = 2
	STARtframe = 3
	WKFR = 4


# noinspection SpellCheckingInspection
class SbusLinUartPolarity(Enum):
	"""2 Members, IDLHigh ... IDLLow"""
	IDLHigh = 0
	IDLLow = 1


# noinspection SpellCheckingInspection
class SbusManchDataPhase(Enum):
	"""2 Members, FEDGe ... SEDGe"""
	FEDGe = 0
	SEDGe = 1


# noinspection SpellCheckingInspection
class SbusManchDataPolarity(Enum):
	"""2 Members, MANC ... MANT"""
	MANC = 0
	MANT = 1


# noinspection SpellCheckingInspection
class SbusMilstdFrameState(Enum):
	"""8 Members, GAP ... UNKNown"""
	GAP = 0
	INComplete = 1
	MANC = 2
	OK = 3
	PAR = 4
	RT = 5
	SYNC = 6
	UNKNown = 7


# noinspection SpellCheckingInspection
class SbusMilstdFrameType(Enum):
	"""6 Members, CMD ... UNKNown"""
	CMD = 0
	CMST = 1
	DATA = 2
	IM = 3
	STAT = 4
	UNKNown = 5


# noinspection SpellCheckingInspection
class SbusNrzcFrameState(Enum):
	"""5 Members, CRC ... PARity"""
	CRC = 0
	INComplete = 1
	LENGth = 2
	OK = 3
	PARity = 4


# noinspection SpellCheckingInspection
class SbusQspiFrameState(Enum):
	"""4 Members, INComplete ... OPCode"""
	INComplete = 0
	LENGth = 1
	OK = 2
	OPCode = 3


# noinspection SpellCheckingInspection
class SbusQspiInstruction(Enum):
	"""3 Members, DUAL ... SINGle"""
	DUAL = 0
	QUAD = 1
	SINGle = 2


# noinspection SpellCheckingInspection
class SbusQspiSclkPolarity(Enum):
	"""2 Members, FALLing ... RISing"""
	FALLing = 0
	RISing = 1


# noinspection SpellCheckingInspection
class SbusRffeReadMode(Enum):
	"""2 Members, SREAD ... STRD"""
	SREAD = 0
	STRD = 1


# noinspection SpellCheckingInspection
class SbusRffeSeqType(Enum):
	"""17 Members, ERRD ... UNKN"""
	ERRD = 0
	ERRL = 1
	ERRor = 2
	ERWL = 3
	ERWR = 4
	IRSUM = 5
	MCTR = 6
	MCTW = 7
	MOHO = 8
	MRD = 9
	MSKW = 10
	MWR = 11
	RRD = 12
	RWR = 13
	RZWR = 14
	UNDEF = 15
	UNKN = 16


# noinspection SpellCheckingInspection
class SbusRffeState(Enum):
	"""9 Members, BPERR ... VERSion"""
	BPERR = 0
	GAP = 1
	INComplete = 2
	LENGth = 3
	NORESPONSE = 4
	OK = 5
	PARity = 6
	SSC = 7
	VERSion = 8


# noinspection SpellCheckingInspection
class SbusSentFrameState(Enum):
	"""8 Members, CRC ... SYNC"""
	CRC = 0
	FORM = 1
	INComplete = 2
	LENGth = 3
	OK = 4
	PAUSe = 5
	PULSe = 6
	SYNC = 7


# noinspection SpellCheckingInspection
class SbusSentFrameType(Enum):
	"""6 Members, ELSM ... UNKNown"""
	ELSM = 0
	ESSM = 1
	PAUSe = 2
	SMSG = 3
	TRSQ = 4
	UNKNown = 5


# noinspection SpellCheckingInspection
class SbusSentIdentifierType(Enum):
	"""2 Members, B4 ... B8"""
	B4 = 0
	B8 = 1


# noinspection SpellCheckingInspection
class SbusSentMode(Enum):
	"""2 Members, LEGacy ... SPC"""
	LEGacy = 0
	SPC = 1


# noinspection SpellCheckingInspection
class SbusSentPausePulse(Enum):
	"""3 Members, NPP ... PPFL"""
	NPP = 0
	PP = 1
	PPFL = 2


# noinspection SpellCheckingInspection
class SbusSentResultDisplay(Enum):
	"""3 Members, ALL ... TRSQ"""
	ALL = 0
	SMSG = 1
	TRSQ = 2


# noinspection SpellCheckingInspection
class SbusSentSerialMessages(Enum):
	"""2 Members, DISabled ... ENABled"""
	DISabled = 0
	ENABled = 1


# noinspection SpellCheckingInspection
class SbusSpiCsPolarity(Enum):
	"""2 Members, ACTHigh ... ACTLow"""
	ACTHigh = 0
	ACTLow = 1


# noinspection SpellCheckingInspection
class SbusSpiFrameState(Enum):
	"""4 Members, INComplete ... VOID"""
	INComplete = 0
	LENGth = 1
	OK = 2
	VOID = 3


# noinspection SpellCheckingInspection
class SbusSpiTriggerType(Enum):
	"""4 Members, FRENd ... MOSI"""
	FRENd = 0
	FRSTart = 1
	MISO = 2
	MOSI = 3


# noinspection SpellCheckingInspection
class SbusSpmiFrameState(Enum):
	"""11 Members, ACKerror ... SSCerror"""
	ACKerror = 0
	ARBerror = 1
	BPERror = 2
	CMDerror = 3
	CODerror = 4
	INComplete = 5
	LENerror = 6
	NOReponse = 7
	OK = 8
	PARerror = 9
	SSCerror = 10


# noinspection SpellCheckingInspection
class SbusSpmiFrameType(Enum):
	"""20 Members, ARB ... WAK"""
	ARB = 0
	AUTH = 1
	BMRD = 2
	BSRD = 3
	ERRD = 4
	ERRL = 5
	ERWL = 6
	ERWR = 7
	INV = 8
	MARD = 9
	MAWR = 10
	REST = 11
	RRD = 12
	RWR = 13
	RZWR = 14
	SHUT = 15
	SLEP = 16
	TBOW = 17
	UNKN = 18
	WAK = 19


# noinspection SpellCheckingInspection
class SbusSwireFrameState(Enum):
	"""5 Members, AMBiguous ... PARity"""
	AMBiguous = 0
	INComplete = 1
	LENGth = 2
	OK = 3
	PARity = 4


# noinspection SpellCheckingInspection
class SbusTbtoFrameState(Enum):
	"""6 Members, ERRCRC ... OK"""
	ERRCRC = 0
	ERRFEC = 1
	ERROOR = 2
	ERRZERO = 3
	INComplete = 4
	OK = 5


# noinspection SpellCheckingInspection
class SbusTbtoFrameType(Enum):
	"""9 Members, BH ... ZEROTSYM"""
	BH = 0
	CTLADDR = 1
	CTLCODE = 2
	IDLE = 3
	MAC = 4
	OAM = 5
	RSFEC = 6
	UNKNown = 7
	ZEROTSYM = 8


# noinspection SpellCheckingInspection
class SbusTnosFrameState(Enum):
	"""7 Members, ECRC ... OK"""
	ECRC = 0
	EESD = 1
	ELEN = 2
	EPRMble = 3
	ESFD = 4
	INComplete = 5
	OK = 6


# noinspection SpellCheckingInspection
class SbusTnosFrameType(Enum):
	"""4 Members, BEACon ... UNKN"""
	BEACon = 0
	COMMit = 1
	MAC = 2
	UNKN = 3


# noinspection SpellCheckingInspection
class SbusUartFrameSeparation(Enum):
	"""2 Members, NONE ... TOUT"""
	NONE = 0
	TOUT = 1


# noinspection SpellCheckingInspection
class SbusUartParity(Enum):
	"""6 Members, DC ... SPC"""
	DC = 0
	EVEN = 1
	MARK = 2
	NONE = 3
	ODD = 4
	SPC = 5


# noinspection SpellCheckingInspection
class SbusUartTriggerType(Enum):
	"""6 Members, BRKC ... STPerror"""
	BRKC = 0
	DATA = 1
	PCKS = 2
	PRER = 3
	STBT = 4
	STPerror = 5


# noinspection SpellCheckingInspection
class SbusUartWordState(Enum):
	"""6 Members, BREak ... STERror"""
	BREak = 0
	INComplete = 1
	OK = 2
	PRERror = 3
	SPERror = 4
	STERror = 5


# noinspection SpellCheckingInspection
class SelectProbe(Enum):
	"""23 Members, NONE ... ZZ80"""
	NONE = 0
	USER = 1
	ZC02100 = 2
	ZC021000 = 3
	ZC03 = 4
	ZC10 = 5
	ZC20 = 6
	ZC30 = 7
	ZC3101 = 8
	ZC311 = 9
	ZC3110 = 10
	ZD002A10 = 11
	ZD002A100 = 12
	ZD003A20 = 13
	ZD003A200 = 14
	ZD01A100 = 15
	ZD01A1000 = 16
	ZD02 = 17
	ZD08 = 18
	ZH03 = 19
	ZP1X = 20
	ZS10L = 21
	ZZ80 = 22


# noinspection SpellCheckingInspection
class SelResults(Enum):
	"""2 Members, ALL ... LOCKed"""
	ALL = 0
	LOCKed = 1


# noinspection SpellCheckingInspection
class SignalSource(Enum):
	"""362 Members, C1 ... XY4"""
	C1 = 0
	C2 = 1
	C3 = 2
	C4 = 3
	C5 = 4
	C6 = 5
	C7 = 6
	C8 = 7
	D0 = 8
	D1 = 9
	D10 = 10
	D11 = 11
	D12 = 12
	D13 = 13
	D14 = 14
	D15 = 15
	D2 = 16
	D3 = 17
	D4 = 18
	D5 = 19
	D6 = 20
	D7 = 21
	D8 = 22
	D9 = 23
	DREF0 = 24
	DREF1 = 25
	DREF10 = 26
	DREF11 = 27
	DREF12 = 28
	DREF13 = 29
	DREF14 = 30
	DREF15 = 31
	DREF2 = 32
	DREF3 = 33
	DREF4 = 34
	DREF5 = 35
	DREF6 = 36
	DREF7 = 37
	DREF8 = 38
	DREF9 = 39
	EYE1 = 40
	EYE2 = 41
	EYE3 = 42
	EYE4 = 43
	EYE5 = 44
	EYE6 = 45
	EYE7 = 46
	EYE8 = 47
	FAMPlitude = 48
	FGAin = 49
	FPHase = 50
	FREF1 = 51
	FREF2 = 52
	FREF3 = 53
	FREF4 = 54
	HISMeas1 = 55
	HISMeas2 = 56
	HISMeas3 = 57
	HISMeas4 = 58
	HISMeas5 = 59
	HISMeas6 = 60
	HISMeas7 = 61
	HISMeas8 = 62
	HISWaveform1 = 63
	HISWaveform2 = 64
	HISWaveform3 = 65
	HISWaveform4 = 66
	HISWaveform5 = 67
	HISWaveform6 = 68
	HISWaveform7 = 69
	HISWaveform8 = 70
	M1 = 71
	M2 = 72
	M3 = 73
	M4 = 74
	M5 = 75
	M6 = 76
	M7 = 77
	M8 = 78
	NONE = 79
	O10C1 = 80
	O10C2 = 81
	O10C3 = 82
	O10C4 = 83
	O10C5 = 84
	O10C6 = 85
	O10C7 = 86
	O10C8 = 87
	O10R1 = 88
	O10R2 = 89
	O10R3 = 90
	O10R4 = 91
	O10R5 = 92
	O10R6 = 93
	O10R7 = 94
	O10R8 = 95
	O11C1 = 96
	O11C2 = 97
	O11C3 = 98
	O11C4 = 99
	O11C5 = 100
	O11C6 = 101
	O11C7 = 102
	O11C8 = 103
	O11R1 = 104
	O11R2 = 105
	O11R3 = 106
	O11R4 = 107
	O11R5 = 108
	O11R6 = 109
	O11R7 = 110
	O11R8 = 111
	O2C1 = 112
	O2C2 = 113
	O2C3 = 114
	O2C4 = 115
	O2C5 = 116
	O2C6 = 117
	O2C7 = 118
	O2C8 = 119
	O2R1 = 120
	O2R2 = 121
	O2R3 = 122
	O2R4 = 123
	O2R5 = 124
	O2R6 = 125
	O2R7 = 126
	O2R8 = 127
	O3C1 = 128
	O3C2 = 129
	O3C3 = 130
	O3C4 = 131
	O3C5 = 132
	O3C6 = 133
	O3C7 = 134
	O3C8 = 135
	O3R1 = 136
	O3R2 = 137
	O3R3 = 138
	O3R4 = 139
	O3R5 = 140
	O3R6 = 141
	O3R7 = 142
	O3R8 = 143
	O4C1 = 144
	O4C2 = 145
	O4C3 = 146
	O4C4 = 147
	O4C5 = 148
	O4C6 = 149
	O4C7 = 150
	O4C8 = 151
	O4R1 = 152
	O4R2 = 153
	O4R3 = 154
	O4R4 = 155
	O4R5 = 156
	O4R6 = 157
	O4R7 = 158
	O4R8 = 159
	O5C1 = 160
	O5C2 = 161
	O5C3 = 162
	O5C4 = 163
	O5C5 = 164
	O5C6 = 165
	O5C7 = 166
	O5C8 = 167
	O5R1 = 168
	O5R2 = 169
	O5R3 = 170
	O5R4 = 171
	O5R5 = 172
	O5R6 = 173
	O5R7 = 174
	O5R8 = 175
	O6C1 = 176
	O6C2 = 177
	O6C3 = 178
	O6C4 = 179
	O6C5 = 180
	O6C6 = 181
	O6C7 = 182
	O6C8 = 183
	O6R1 = 184
	O6R2 = 185
	O6R3 = 186
	O6R4 = 187
	O6R5 = 188
	O6R6 = 189
	O6R7 = 190
	O6R8 = 191
	O7C1 = 192
	O7C2 = 193
	O7C3 = 194
	O7C4 = 195
	O7C5 = 196
	O7C6 = 197
	O7C7 = 198
	O7C8 = 199
	O7R1 = 200
	O7R2 = 201
	O7R3 = 202
	O7R4 = 203
	O7R5 = 204
	O7R6 = 205
	O7R7 = 206
	O7R8 = 207
	O8C1 = 208
	O8C2 = 209
	O8C3 = 210
	O8C4 = 211
	O8C5 = 212
	O8C6 = 213
	O8C7 = 214
	O8C8 = 215
	O8R1 = 216
	O8R2 = 217
	O8R3 = 218
	O8R4 = 219
	O8R5 = 220
	O8R6 = 221
	O8R7 = 222
	O8R8 = 223
	O9C1 = 224
	O9C2 = 225
	O9C3 = 226
	O9C4 = 227
	O9C5 = 228
	O9C6 = 229
	O9C7 = 230
	O9C8 = 231
	O9R1 = 232
	O9R2 = 233
	O9R3 = 234
	O9R4 = 235
	O9R5 = 236
	O9R6 = 237
	O9R7 = 238
	O9R8 = 239
	PA1HPOWER1 = 240
	PA1IPOWER = 241
	PA1OPOWER1 = 242
	PA1OPOWER2 = 243
	PA1OPOWER3 = 244
	PA1QPOWER1 = 245
	PA1SOA = 246
	PA1SPOWER1 = 247
	PA1TOPOWER = 248
	PA2HPOWER1 = 249
	PA2IPOWER = 250
	PA2OPOWER1 = 251
	PA2OPOWER2 = 252
	PA2OPOWER3 = 253
	PA2QPOWER1 = 254
	PA2SOA = 255
	PA2SPOWER1 = 256
	PA2TOPOWER = 257
	PA3HPOWER1 = 258
	PA3IPOWER = 259
	PA3OPOWER1 = 260
	PA3OPOWER2 = 261
	PA3OPOWER3 = 262
	PA3QPOWER1 = 263
	PA3SOA = 264
	PA3SPOWER1 = 265
	PA3TOPOWER = 266
	PA4HPOWER1 = 267
	PA4IPOWER = 268
	PA4OPOWER1 = 269
	PA4OPOWER2 = 270
	PA4OPOWER3 = 271
	PA4QPOWER1 = 272
	PA4SOA = 273
	PA4SPOWER1 = 274
	PA4TOPOWER = 275
	PA5HPOWER1 = 276
	PA5IPOWER = 277
	PA5OPOWER1 = 278
	PA5OPOWER2 = 279
	PA5OPOWER3 = 280
	PA5QPOWER1 = 281
	PA5SOA = 282
	PA5SPOWER1 = 283
	PA5TOPOWER = 284
	PA6HPOWER1 = 285
	PA6IPOWER = 286
	PA6OPOWER1 = 287
	PA6OPOWER2 = 288
	PA6OPOWER3 = 289
	PA6QPOWER1 = 290
	PA6SOA = 291
	PA6SPOWER1 = 292
	PA6TOPOWER = 293
	PBUS1 = 294
	PBUS2 = 295
	PBUS3 = 296
	PBUS4 = 297
	R1 = 298
	R2 = 299
	R3 = 300
	R4 = 301
	R5 = 302
	R6 = 303
	R7 = 304
	R8 = 305
	SBUS1 = 306
	SBUS2 = 307
	SBUS3 = 308
	SBUS4 = 309
	SPECAVER1 = 310
	SPECAVER2 = 311
	SPECAVER3 = 312
	SPECAVER4 = 313
	SPECMAXH1 = 314
	SPECMAXH2 = 315
	SPECMAXH3 = 316
	SPECMAXH4 = 317
	SPECMINH1 = 318
	SPECMINH2 = 319
	SPECMINH3 = 320
	SPECMINH4 = 321
	SPECNORM1 = 322
	SPECNORM2 = 323
	SPECNORM3 = 324
	SPECNORM4 = 325
	TREF1 = 326
	TREF2 = 327
	TREF3 = 328
	TREF4 = 329
	TREF5 = 330
	TREF6 = 331
	TREF7 = 332
	TREF8 = 333
	TRK1 = 334
	TRK10 = 335
	TRK11 = 336
	TRK12 = 337
	TRK13 = 338
	TRK14 = 339
	TRK15 = 340
	TRK16 = 341
	TRK17 = 342
	TRK18 = 343
	TRK19 = 344
	TRK2 = 345
	TRK20 = 346
	TRK21 = 347
	TRK22 = 348
	TRK23 = 349
	TRK24 = 350
	TRK3 = 351
	TRK4 = 352
	TRK5 = 353
	TRK6 = 354
	TRK7 = 355
	TRK8 = 356
	TRK9 = 357
	XY1 = 358
	XY2 = 359
	XY3 = 360
	XY4 = 361


# noinspection SpellCheckingInspection
class SignalType(Enum):
	"""31 Members, CHANNEL ... ZUI_VOLT"""
	CHANNEL = 0
	DIFFERENTIAL = 1
	DIGITAL = 2
	DIGITAL_REFERENCE = 3
	EYE = 4
	FRA_GEN = 5
	FRA_IMP = 6
	FRA_REF = 7
	GAIN = 8
	GENERATOR = 9
	HARMONICS = 10
	HISTOGRAM = 11
	IQ = 12
	IQ_CH_I = 13
	IQ_CH_Q = 14
	LONGTERM = 15
	MATH = 16
	MSO = 17
	NONE = 18
	PHASE = 19
	REFERENCE = 20
	SERIAL = 21
	SPECTROGRAM = 22
	SPECTRUM = 23
	TIMELINE = 24
	TRACK = 25
	TREF = 26
	XY = 27
	ZUI = 28
	ZUI_CURRENT = 29
	ZUI_VOLT = 30


# noinspection SpellCheckingInspection
class SlopeType(Enum):
	"""2 Members, NEGative ... POSitive"""
	NEGative = 0
	POSitive = 1


# noinspection SpellCheckingInspection
class SourceInt(Enum):
	"""2 Members, EXTernal ... INTernal"""
	EXTernal = 0
	INTernal = 1


# noinspection SpellCheckingInspection
class SourceMode(Enum):
	"""3 Members, MSOurce ... SINGle"""
	MSOurce = 0
	SECond = 1
	SINGle = 2


# noinspection SpellCheckingInspection
class StatusQuestionAdcState(Enum):
	"""32 Members, CNCHannel1 ... CPPRobe8"""
	CNCHannel1 = 0
	CNCHannel2 = 1
	CNCHannel3 = 2
	CNCHannel4 = 3
	CNCHannel5 = 4
	CNCHannel6 = 5
	CNCHannel7 = 6
	CNCHannel8 = 7
	CNPRobe1 = 8
	CNPRobe2 = 9
	CNPRobe3 = 10
	CNPRobe4 = 11
	CNPRobe5 = 12
	CNPRobe6 = 13
	CNPRobe7 = 14
	CNPRobe8 = 15
	CPCHannel1 = 16
	CPCHannel2 = 17
	CPCHannel3 = 18
	CPCHannel4 = 19
	CPCHannel5 = 20
	CPCHannel6 = 21
	CPCHannel7 = 22
	CPCHannel8 = 23
	CPPRobe1 = 24
	CPPRobe2 = 25
	CPPRobe3 = 26
	CPPRobe4 = 27
	CPPRobe5 = 28
	CPPRobe6 = 29
	CPPRobe7 = 30
	CPPRobe8 = 31


# noinspection SpellCheckingInspection
class StatusQuestionCoverload(Enum):
	"""18 Members, CHANnel1 ... WCHannel8"""
	CHANnel1 = 0
	CHANnel2 = 1
	CHANnel3 = 2
	CHANnel4 = 3
	CHANnel5 = 4
	CHANnel6 = 5
	CHANnel7 = 6
	CHANnel8 = 7
	EXTTRIGGERIN = 8
	TRIGGEROUT = 9
	WCHannel1 = 10
	WCHannel2 = 11
	WCHannel3 = 12
	WCHannel4 = 13
	WCHannel5 = 14
	WCHannel6 = 15
	WCHannel7 = 16
	WCHannel8 = 17


# noinspection SpellCheckingInspection
class StatusQuestionGenerator(Enum):
	"""8 Members, WGENerator1 ... WGENerator8"""
	WGENerator1 = 0
	WGENerator2 = 1
	WGENerator3 = 2
	WGENerator4 = 3
	WGENerator5 = 4
	WGENerator6 = 5
	WGENerator7 = 6
	WGENerator8 = 7


# noinspection SpellCheckingInspection
class StatusQuestionLimit(Enum):
	"""8 Members, MEASurement1 ... MEASurement8"""
	MEASurement1 = 0
	MEASurement2 = 1
	MEASurement3 = 2
	MEASurement4 = 3
	MEASurement5 = 4
	MEASurement6 = 5
	MEASurement7 = 6
	MEASurement8 = 7


# noinspection SpellCheckingInspection
class StatusQuestionMask(Enum):
	"""8 Members, MASK1 ... MASK8"""
	MASK1 = 0
	MASK2 = 1
	MASK3 = 2
	MASK4 = 3
	MASK5 = 4
	MASK6 = 5
	MASK7 = 6
	MASK8 = 7


# noinspection SpellCheckingInspection
class StatusQuestionPll(Enum):
	"""8 Members, PLL100 ... PLLLO10G"""
	PLL100 = 0
	PLL250 = 1
	PLL312 = 2
	PLL500 = 3
	PLL800 = 4
	PLLCAL = 5
	PLLGBSYNC = 6
	PLLLO10G = 7


# noinspection SpellCheckingInspection
class StatusQuestionPsupply(Enum):
	"""8 Members, PROBe1 ... PROBe8"""
	PROBe1 = 0
	PROBe2 = 1
	PROBe3 = 2
	PROBe4 = 3
	PROBe5 = 4
	PROBe6 = 5
	PROBe7 = 6
	PROBe8 = 7


# noinspection SpellCheckingInspection
class StopBits(Enum):
	"""3 Members, B1 ... B2"""
	B1 = 0
	B15 = 1
	B2 = 2


# noinspection SpellCheckingInspection
class Technology(Enum):
	"""11 Members, CUSTom ... VM13"""
	CUSTom = 0
	MANual = 1
	V0 = 2
	V09 = 3
	V125 = 4
	V15 = 5
	V165 = 6
	V20 = 7
	V25 = 8
	V38 = 9
	VM13 = 10


# noinspection SpellCheckingInspection
class TekPredefProbe(Enum):
	"""25 Members, NONE ... TCP202"""
	NONE = 0
	P5205A50 = 1
	P5205A500 = 2
	P5210A100 = 3
	P5210A1000 = 4
	P6205 = 5
	P6241 = 6
	P6243 = 7
	P6245 = 8
	P6246A1 = 9
	P6246A10 = 10
	P6247A1 = 11
	P6247A10 = 12
	P6248A1 = 13
	P6248A10 = 14
	P6249 = 15
	P6250A5 = 16
	P6250A50 = 17
	P6251A5 = 18
	P6251A50 = 19
	P6701B = 20
	P6703B = 21
	P6711 = 22
	P6713 = 23
	TCP202 = 24


# noinspection SpellCheckingInspection
class TimebaseRollMode(Enum):
	"""2 Members, AUTO ... OFF"""
	AUTO = 0
	OFF = 1


# noinspection SpellCheckingInspection
class TreferenceType(Enum):
	"""4 Members, CLOCk ... SCDR"""
	CLOCk = 0
	HCDR = 1
	RCDR = 2
	SCDR = 3


# noinspection SpellCheckingInspection
class TrigFilterMode(Enum):
	"""3 Members, LFReject ... RFReject"""
	LFReject = 0
	OFF = 1
	RFReject = 2


# noinspection SpellCheckingInspection
class TriggerAction(Enum):
	"""4 Members, NOACtion ... VIOLation"""
	NOACtion = 0
	SUCCess = 1
	TRIGger = 2
	VIOLation = 3


# noinspection SpellCheckingInspection
class TriggerEventType(Enum):
	"""18 Members, ANEDge ... WINDow"""
	ANEDge = 0
	ANTV = 1
	CDR = 2
	EDGE = 3
	GLITch = 4
	INTerval = 5
	IQMagnitude = 6
	NFC = 7
	PATTern = 8
	RUNT = 9
	SERPattern = 10
	SETHold = 11
	SLEWrate = 12
	STATe = 13
	TIMeout = 14
	TV = 15
	WIDTh = 16
	WINDow = 17


# noinspection SpellCheckingInspection
class TriggerGlitchMode(Enum):
	"""2 Members, LONGer ... SHORter"""
	LONGer = 0
	SHORter = 1


# noinspection SpellCheckingInspection
class TriggerHoldoffMode(Enum):
	"""5 Members, AUTO ... TIME"""
	AUTO = 0
	EVENts = 1
	OFF = 2
	RANDom = 3
	TIME = 4


# noinspection SpellCheckingInspection
class TriggerMode(Enum):
	"""3 Members, AUTO ... NORMal"""
	AUTO = 0
	FREerun = 1
	NORMal = 2


# noinspection SpellCheckingInspection
class TriggerMultiEventsType(Enum):
	"""9 Members, AB ... AZ"""
	AB = 0
	ABR = 1
	ABRZ = 2
	ABZ = 3
	AONLy = 4
	AORB = 5
	AORBZ = 6
	ASB = 7
	AZ = 8


# noinspection SpellCheckingInspection
class TriggerOutSource(Enum):
	"""3 Members, POST ... WAIT"""
	POST = 0
	TRIG = 1
	WAIT = 2


# noinspection SpellCheckingInspection
class TriggerPatternSource(Enum):
	"""3 Members, AAD ... DIGital"""
	AAD = 0
	ANALog = 1
	DIGital = 2


# noinspection SpellCheckingInspection
class TriggerRuntRangeMode(Enum):
	"""5 Members, ANY ... WITHin"""
	ANY = 0
	LONGer = 1
	OUTSide = 2
	SHORter = 3
	WITHin = 4


# noinspection SpellCheckingInspection
class TriggerSlewRangeMode(Enum):
	"""4 Members, GTHan ... OUTRange"""
	GTHan = 0
	INSRange = 1
	LTHan = 2
	OUTRange = 3


# noinspection SpellCheckingInspection
class TriggerSource(Enum):
	"""47 Members, C1 ... Z2V4"""
	C1 = 0
	C2 = 1
	C3 = 2
	C4 = 3
	C5 = 4
	C6 = 5
	C7 = 6
	C8 = 7
	D0 = 8
	D1 = 9
	D10 = 10
	D11 = 11
	D12 = 12
	D13 = 13
	D14 = 14
	D15 = 15
	D2 = 16
	D3 = 17
	D4 = 18
	D5 = 19
	D6 = 20
	D7 = 21
	D8 = 22
	D9 = 23
	EXTernanalog = 24
	GENerator = 25
	LINE = 26
	SBUS1 = 27
	SBUS2 = 28
	SBUS3 = 29
	SBUS4 = 30
	Z1I1 = 31
	Z1I2 = 32
	Z1I3 = 33
	Z1I4 = 34
	Z1V1 = 35
	Z1V2 = 36
	Z1V3 = 37
	Z1V4 = 38
	Z2I1 = 39
	Z2I2 = 40
	Z2I3 = 41
	Z2I4 = 42
	Z2V1 = 43
	Z2V2 = 44
	Z2V3 = 45
	Z2V4 = 46


# noinspection SpellCheckingInspection
class TriggerWinRangeMode(Enum):
	"""4 Members, ENTer ... WITHin"""
	ENTer = 0
	EXIT = 1
	OUTSide = 2
	WITHin = 3


# noinspection SpellCheckingInspection
class TxRx(Enum):
	"""2 Members, RX ... TX"""
	RX = 0
	TX = 1


# noinspection SpellCheckingInspection
class TypePy(Enum):
	"""4 Members, BLEFt ... TRIGht"""
	BLEFt = 0
	BRIGht = 1
	TLEFt = 2
	TRIGht = 3


# noinspection SpellCheckingInspection
class Unit(Enum):
	"""115 Members, A ... WS"""
	A = 0
	A_DIV = 1
	A_S = 2
	A_SQRT_HZ = 3
	A_V = 4
	AS = 5
	BAUD = 6
	BER = 7
	BIT = 8
	BIT_S = 9
	BYTS = 10
	C = 11
	DB = 12
	DB_DIV = 13
	DB_GHZ = 14
	DB_HZ = 15
	DBA = 16
	DBA_DIV = 17
	DBA_HZ = 18
	DBC = 19
	DBC_HZ = 20
	DBHZ = 21
	DBM = 22
	DBM_DIV = 23
	DBM_HZ = 24
	DBMA = 25
	DBMV = 26
	DBMV_HZ = 27
	DBMV_M_HZ = 28
	DBMV_MHZ = 29
	DBMW = 30
	DBPT = 31
	DBPT_HZ = 32
	DBPW = 33
	DBPW_HZ = 34
	DBS = 35
	DBUA = 36
	DBUA_HZ = 37
	DBUA_M = 38
	DBUA_M_HZ = 39
	DBUA_M_MHZ = 40
	DBUA_MHZ = 41
	DBUA_SQRT_HZ = 42
	DBUV = 43
	DBUV_DIV = 44
	DBUV_HZ = 45
	DBUV_M = 46
	DBUV_M_MHZ = 47
	DBUV_MHZ = 48
	DBUV_SQRT_HZ = 49
	DBV = 50
	DBV_DIV = 51
	DBV_HZ = 52
	DBW = 53
	DEG = 54
	DEG_DIV = 55
	DIV = 56
	F = 57
	FF_GHZ = 58
	H = 59
	HZ = 60
	HZ_DIV = 61
	HZ_S = 62
	IRE = 63
	J = 64
	K = 65
	M = 66
	MBIT_S = 67
	MSYMB_S = 68
	MV = 69
	MW = 70
	NONE = 71
	OHM = 72
	PCT = 73
	PER_DIV = 74
	PER_SEC = 75
	PH_GHZ = 76
	PPM = 77
	PX = 78
	RAD = 79
	S = 80
	S_DIV = 81
	S_S = 82
	SIEMENS = 83
	SYMB = 84
	SYMB_S = 85
	UA_HZ = 86
	UA_M_HZ = 87
	UI = 88
	USER = 89
	UV = 90
	UV_HZ = 91
	UV_M_HZ = 92
	V = 93
	V_A = 94
	V_DIV = 95
	V_S = 96
	V_SQRT_HZ = 97
	V_V = 98
	V_W = 99
	VA = 100
	VA_LIN = 101
	VA_LOG = 102
	VAR = 103
	VPP = 104
	VPP_DIV = 105
	VS = 106
	VV = 107
	W = 108
	W_DIV = 109
	W_HZ = 110
	W_S = 111
	W_V = 112
	WORD = 113
	WS = 114


# noinspection SpellCheckingInspection
class UserActivityTout(Enum):
	"""15 Members, OFF ... T5Minutes"""
	OFF = 0
	T10Minutes = 1
	T15Minutes = 2
	T1Hour = 3
	T1Minute = 4
	T20Minutes = 5
	T25Minutes = 6
	T2Hours = 7
	T2Minutes = 8
	T30Minutes = 9
	T3Hours = 10
	T3Minutes = 11
	T45Minutes = 12
	T4Hours = 13
	T5Minutes = 14


# noinspection SpellCheckingInspection
class VerticalMode(Enum):
	"""2 Members, COUPled ... INDependent"""
	COUPled = 0
	INDependent = 1


# noinspection SpellCheckingInspection
class WgenFunctionType(Enum):
	"""14 Members, ARBitrary ... SQUare"""
	ARBitrary = 0
	CARDiac = 1
	DC = 2
	EXPFall = 3
	EXPRise = 4
	GAUSs = 5
	HAVer = 6
	LORNtz = 7
	PULSe = 8
	PWM = 9
	RAMP = 10
	SINC = 11
	SINusoid = 12
	SQUare = 13


# noinspection SpellCheckingInspection
class WgenLoad(Enum):
	"""2 Members, FIFTy ... HIZ"""
	FIFTy = 0
	HIZ = 1


# noinspection SpellCheckingInspection
class WgenOperationMode(Enum):
	"""4 Members, ARBGenerator ... SWEep"""
	ARBGenerator = 0
	FUNCgen = 1
	MODulation = 2
	SWEep = 3


# noinspection SpellCheckingInspection
class WgenRunMode(Enum):
	"""2 Members, REPetitive ... SINGle"""
	REPetitive = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class WgenSignalType(Enum):
	"""4 Members, RAMP ... SQUare"""
	RAMP = 0
	SAWTooth = 1
	SINusoid = 2
	SQUare = 3


# noinspection SpellCheckingInspection
class WgenWaveformSource(Enum):
	"""3 Members, ARBitrary ... SCOPe"""
	ARBitrary = 0
	ERINjection = 1
	SCOPe = 2


# noinspection SpellCheckingInspection
class WindowFunction(Enum):
	"""7 Members, BLACkharris ... RECTangular"""
	BLACkharris = 0
	FLATTOP2 = 1
	GAUSsian = 2
	HAMMing = 3
	HANN = 4
	KAISerbessel = 5
	RECTangular = 6


# noinspection SpellCheckingInspection
class WindowPosition(Enum):
	"""6 Members, BOTT ... TOP"""
	BOTT = 0
	FREE = 1
	LEFT = 2
	NONE = 3
	RIGH = 4
	TOP = 5
