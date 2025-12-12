from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StopCls:
	"""Stop commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stop", core, parent)

	def set(self, relative_stop: float, histogram=repcap.Histogram.Default) -> None:
		"""HISTogram<*>:WINDow:HORizontal:RELative:STOP \n
		Snippet: driver.histogram.window.horizontal.relative.stop.set(relative_stop = 1.0, histogram = repcap.Histogram.Default) \n
		Set the horizontal window limits as relative values in % of the diagram width. \n
			:param relative_stop: No help available
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		param = Conversions.decimal_value_to_str(relative_stop)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'HISTogram{histogram_cmd_val}:WINDow:HORizontal:RELative:STOP {param}')

	def get(self, histogram=repcap.Histogram.Default) -> float:
		"""HISTogram<*>:WINDow:HORizontal:RELative:STOP \n
		Snippet: value: float = driver.histogram.window.horizontal.relative.stop.get(histogram = repcap.Histogram.Default) \n
		Set the horizontal window limits as relative values in % of the diagram width. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: relative_stop: No help available"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'HISTogram{histogram_cmd_val}:WINDow:HORizontal:RELative:STOP?')
		return Conversions.str_to_float(response)
