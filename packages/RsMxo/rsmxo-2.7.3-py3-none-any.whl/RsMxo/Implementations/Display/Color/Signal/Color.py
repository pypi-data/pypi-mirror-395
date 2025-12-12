from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ColorCls:
	"""Color commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("color", core, parent)

	def set(self, signal: enums.SignalSource, value: int) -> None:
		"""DISPlay:COLor:SIGNal:COLor \n
		Snippet: driver.display.color.signal.color.set(signal = enums.SignalSource.C1, value = 1) \n
		Sets the color of the selected waveform. \n
			:param signal: Signal name as returned by method RsMxo.Display.Color.Signal.catalog.
			:param value: Decimal value of the ARGB color. Use the color dialog box on the instrument to get the hex value of the color, and convert the hex value to a decimal value. 0 is fully transparent black. 4278190080 (dec) = FF000000 (hex) is opaque black. 4294967295 (dec) = FFFFFFFF (hex) is opaque white. To reset the color to its default, use DISPlay:COLor:SIGNal:COLor Signal,DEF.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('signal', signal, DataType.Enum, enums.SignalSource), ArgSingle('value', value, DataType.Integer))
		self._core.io.write(f'DISPlay:COLor:SIGNal:COLor {param}'.rstrip())

	def get(self) -> int:
		"""DISPlay:COLor:SIGNal:COLor \n
		Snippet: value: int = driver.display.color.signal.color.get() \n
		Sets the color of the selected waveform. \n
			:return: value: Decimal value of the ARGB color. Use the color dialog box on the instrument to get the hex value of the color, and convert the hex value to a decimal value. 0 is fully transparent black. 4278190080 (dec) = FF000000 (hex) is opaque black. 4294967295 (dec) = FFFFFFFF (hex) is opaque white. To reset the color to its default, use DISPlay:COLor:SIGNal:COLor Signal,DEF."""
		response = self._core.io.query_str(f'DISPlay:COLor:SIGNal:COLor?')
		return Conversions.str_to_int(response)
