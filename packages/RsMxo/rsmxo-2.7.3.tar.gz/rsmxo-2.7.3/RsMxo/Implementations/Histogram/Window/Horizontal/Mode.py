from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModeCls:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, mode: enums.AbsRel, histogram=repcap.Histogram.Default) -> None:
		"""HISTogram<*>:WINDow:HORizontal:MODE \n
		Snippet: driver.histogram.window.horizontal.mode.set(mode = enums.AbsRel.ABS, histogram = repcap.Histogram.Default) \n
		The commands define whether the window limits are entered as absolute or relative values, in horizontal and vertical
		direction. \n
			:param mode: No help available
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AbsRel)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'HISTogram{histogram_cmd_val}:WINDow:HORizontal:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, histogram=repcap.Histogram.Default) -> enums.AbsRel:
		"""HISTogram<*>:WINDow:HORizontal:MODE \n
		Snippet: value: enums.AbsRel = driver.histogram.window.horizontal.mode.get(histogram = repcap.Histogram.Default) \n
		The commands define whether the window limits are entered as absolute or relative values, in horizontal and vertical
		direction. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: mode: No help available"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'HISTogram{histogram_cmd_val}:WINDow:HORizontal:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AbsRel)
