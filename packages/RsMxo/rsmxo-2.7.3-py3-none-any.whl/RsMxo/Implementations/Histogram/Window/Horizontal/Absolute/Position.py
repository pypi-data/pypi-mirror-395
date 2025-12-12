from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class PositionCls:
	"""Position commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("position", core, parent)

	def set(self, center: float, histogram=repcap.Histogram.Default) -> None:
		"""HISTogram<*>:WINDow:HORizontal:ABSolute:POSition \n
		Snippet: driver.histogram.window.horizontal.absolute.position.set(center = 1.0, histogram = repcap.Histogram.Default) \n
		Set the horizontal window limits as absolute values. Enter the unit of the horizontal axis together with the value. \n
			:param center: No help available
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		param = Conversions.decimal_value_to_str(center)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'HISTogram{histogram_cmd_val}:WINDow:HORizontal:ABSolute:POSition {param}')

	def get(self, histogram=repcap.Histogram.Default) -> float:
		"""HISTogram<*>:WINDow:HORizontal:ABSolute:POSition \n
		Snippet: value: float = driver.histogram.window.horizontal.absolute.position.get(histogram = repcap.Histogram.Default) \n
		Set the horizontal window limits as absolute values. Enter the unit of the horizontal axis together with the value. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: center: No help available"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'HISTogram{histogram_cmd_val}:WINDow:HORizontal:ABSolute:POSition?')
		return Conversions.str_to_float(response)
