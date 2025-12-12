from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.HistMode, histogram=repcap.Histogram.Default) -> None:
		"""HISTogram<*>:MODE \n
		Snippet: driver.histogram.mode.set(mode = enums.HistMode.HORizontal, histogram = repcap.Histogram.Default) \n
		Defines the type of histogram. \n
			:param mode:
				- VERTical: A vertical histogram has horizontal bars that show the occurence of amplitude, or vertical values.
				- HORizontal: A horizontal histogram has vertical bars that show the occurrence of a sample at a given time on the x-axis.
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')"""
		param = Conversions.enum_scalar_to_str(mode, enums.HistMode)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'HISTogram{histogram_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, histogram=repcap.Histogram.Default) -> enums.HistMode:
		"""HISTogram<*>:MODE \n
		Snippet: value: enums.HistMode = driver.histogram.mode.get(histogram = repcap.Histogram.Default) \n
		Defines the type of histogram. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: mode:
				- VERTical: A vertical histogram has horizontal bars that show the occurence of amplitude, or vertical values.
				- HORizontal: A horizontal histogram has vertical bars that show the occurrence of a sample at a given time on the x-axis."""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'HISTogram{histogram_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.HistMode)
