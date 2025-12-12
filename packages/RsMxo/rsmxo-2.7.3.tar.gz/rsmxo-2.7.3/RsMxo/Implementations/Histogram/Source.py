from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SourceCls:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, source: enums.SignalSource, histogram=repcap.Histogram.Default) -> None:
		"""HISTogram<*>:SOURce \n
		Snippet: driver.histogram.source.set(source = enums.SignalSource.C1, histogram = repcap.Histogram.Default) \n
		Defines the source of the histogram. \n
			:param source: No help available
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		param = Conversions.enum_scalar_to_str(source, enums.SignalSource)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'HISTogram{histogram_cmd_val}:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, histogram=repcap.Histogram.Default) -> enums.SignalSource:
		"""HISTogram<*>:SOURce \n
		Snippet: value: enums.SignalSource = driver.histogram.source.get(histogram = repcap.Histogram.Default) \n
		Defines the source of the histogram. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: source: No help available"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'HISTogram{histogram_cmd_val}:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSource)
