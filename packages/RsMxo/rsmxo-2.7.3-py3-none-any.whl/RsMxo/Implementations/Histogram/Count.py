from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CountCls:
	"""Count commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("count", core, parent)

	def set(self, count: int, histogram=repcap.Histogram.Default) -> None:
		"""HISTogram<*>:COUNt \n
		Snippet: driver.histogram.count.set(count = 1, histogram = repcap.Histogram.Default) \n
		Returns the number of created histograms. You can query the minimum and maximum values with <command>? MIN and <command>?
		MAX. \n
			:param count: Counted number of histograms
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		param = Conversions.decimal_value_to_str(count)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'HISTogram{histogram_cmd_val}:COUNt {param}')

	def get(self, histogram=repcap.Histogram.Default) -> int:
		"""HISTogram<*>:COUNt \n
		Snippet: value: int = driver.histogram.count.get(histogram = repcap.Histogram.Default) \n
		Returns the number of created histograms. You can query the minimum and maximum values with <command>? MIN and <command>?
		MAX. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: count: Counted number of histograms"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'HISTogram{histogram_cmd_val}:COUNt?')
		return Conversions.str_to_int(response)
