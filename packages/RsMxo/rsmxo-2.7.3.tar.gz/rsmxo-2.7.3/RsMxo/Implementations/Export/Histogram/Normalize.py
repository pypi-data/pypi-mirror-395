from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NormalizeCls:
	"""Normalize commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("normalize", core, parent)

	def set(self, normalization: bool, histogram=repcap.Histogram.Default) -> None:
		"""EXPort:HISTogram<*>:NORMalize \n
		Snippet: driver.export.histogram.normalize.set(normalization = False, histogram = repcap.Histogram.Default) \n
		If normalization is off, the number of samples in a given bin is exported as integer values. With normalization, the
		ratio of samples in a given bin to the sum of all samples is exported as float value. The sum of all normalized values is
		1. The command affects all histogram exports. \n
			:param normalization: No help available
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		param = Conversions.bool_to_str(normalization)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'EXPort:HISTogram{histogram_cmd_val}:NORMalize {param}')

	def get(self, histogram=repcap.Histogram.Default) -> bool:
		"""EXPort:HISTogram<*>:NORMalize \n
		Snippet: value: bool = driver.export.histogram.normalize.get(histogram = repcap.Histogram.Default) \n
		If normalization is off, the number of samples in a given bin is exported as integer values. With normalization, the
		ratio of samples in a given bin to the sum of all samples is exported as float value. The sum of all normalized values is
		1. The command affects all histogram exports. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: normalization: No help available"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'EXPort:HISTogram{histogram_cmd_val}:NORMalize?')
		return Conversions.str_to_bool(response)
