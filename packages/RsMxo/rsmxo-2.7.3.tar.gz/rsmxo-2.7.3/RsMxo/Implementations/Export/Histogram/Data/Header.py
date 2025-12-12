from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HeaderCls:
	"""Header commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("header", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- 1 Start: float: 1. header value: start value, for vertical histogram in the waveform unit, for horizontal histogram in s.
			- 2 End: float: 2. header value: end value, for vertical histogram in the waveform unit, for horizontal histogram in s.
			- 3 Histogram_Length: int: 3. header value: number of histogram bins"""
		__meta_args_list = [
			ArgStruct.scalar_float('Start'),
			ArgStruct.scalar_float('End'),
			ArgStruct.scalar_int('Histogram_Length')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Start: float = None
			self.End: float = None
			self.Histogram_Length: int = None

	def get(self, histogram=repcap.Histogram.Default) -> GetStruct:
		"""EXPort:HISTogram<*>:DATA:HEADer \n
		Snippet: value: GetStruct = driver.export.histogram.data.header.get(histogram = repcap.Histogram.Default) \n
		Returns the header of the histogram data, the attributes of the waveform histogram. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		return self._core.io.query_struct(f'EXPort:HISTogram{histogram_cmd_val}:DATA:HEADer?', self.__class__.GetStruct())
