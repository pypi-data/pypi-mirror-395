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

	def set(self, relative_center: float, histogram=repcap.Histogram.Default) -> None:
		"""HISTogram<*>:WINDow:VERTical:RELative:POSition \n
		Snippet: driver.histogram.window.vertical.relative.position.set(relative_center = 1.0, histogram = repcap.Histogram.Default) \n
		Set the vertical window limits as relative values in % of the diagram height. \n
			:param relative_center: No help available
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		param = Conversions.decimal_value_to_str(relative_center)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'HISTogram{histogram_cmd_val}:WINDow:VERTical:RELative:POSition {param}')

	def get(self, histogram=repcap.Histogram.Default) -> float:
		"""HISTogram<*>:WINDow:VERTical:RELative:POSition \n
		Snippet: value: float = driver.histogram.window.vertical.relative.position.get(histogram = repcap.Histogram.Default) \n
		Set the vertical window limits as relative values in % of the diagram height. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: relative_center: No help available"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'HISTogram{histogram_cmd_val}:WINDow:VERTical:RELative:POSition?')
		return Conversions.str_to_float(response)
