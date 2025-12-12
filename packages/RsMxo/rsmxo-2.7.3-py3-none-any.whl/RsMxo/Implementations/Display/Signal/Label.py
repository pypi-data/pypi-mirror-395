from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LabelCls:
	"""Label commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("label", core, parent)

	def set(self, signal: enums.SignalSource, label: str) -> None:
		"""DISPlay:SIGNal:LABel \n
		Snippet: driver.display.signal.label.set(signal = enums.SignalSource.C1, label = 'abc') \n
		Defines and assigns a label to the specified channel waveform. \n
			:param signal: No help available
			:param label: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('signal', signal, DataType.Enum, enums.SignalSource), ArgSingle('label', label, DataType.String))
		self._core.io.write(f'DISPlay:SIGNal:LABel {param}'.rstrip())

	def get(self) -> str:
		"""DISPlay:SIGNal:LABel \n
		Snippet: value: str = driver.display.signal.label.get() \n
		Defines and assigns a label to the specified channel waveform. \n
			:return: label: No help available"""
		response = self._core.io.query_str(f'DISPlay:SIGNal:LABel?')
		return trim_str_response(response)
