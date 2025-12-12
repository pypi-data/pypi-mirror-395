from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class EnableCls:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, state: bool, histogram=repcap.Histogram.Default) -> None:
		"""HISTogram<*>:WINDow:ENABle \n
		Snippet: driver.histogram.window.enable.set(state = False, histogram = repcap.Histogram.Default) \n
		When you use a histogram window, the analyzed part of the source waveform is limited vertically and horizontally. \n
			:param state: No help available
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		param = Conversions.bool_to_str(state)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'HISTogram{histogram_cmd_val}:WINDow:ENABle {param}')

	def get(self, histogram=repcap.Histogram.Default) -> bool:
		"""HISTogram<*>:WINDow:ENABle \n
		Snippet: value: bool = driver.histogram.window.enable.get(histogram = repcap.Histogram.Default) \n
		When you use a histogram window, the analyzed part of the source waveform is limited vertically and horizontally. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: state: No help available"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'HISTogram{histogram_cmd_val}:WINDow:ENABle?')
		return Conversions.str_to_bool(response)
