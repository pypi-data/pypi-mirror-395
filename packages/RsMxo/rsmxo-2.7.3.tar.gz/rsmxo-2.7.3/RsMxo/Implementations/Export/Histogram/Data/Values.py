from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ValuesCls:
	"""Values commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("values", core, parent)

	def get(self, histogram=repcap.Histogram.Default) -> bytes:
		"""EXPort:HISTogram<*>:DATA[:VALues] \n
		Snippet: value: bytes = driver.export.histogram.data.values.get(histogram = repcap.Histogram.Default) \n
		Returns the data of the specified histogram for transmission from the instrument to the controlling computer. The data
		can be used in MATLAB, for example. To set the export format, use method RsMxo.FormatPy.Data.set. For histogram data,
		only ASCii and REAL,32 and REAL,64 are supported. The normalization setting is considered: method RsMxo.Export.Histogram.
		Normalize.set. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: data: Comma-separated list of values according to the format setting."""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_bin_block_ERROR(f'EXPort:HISTogram{histogram_cmd_val}:DATA:VALues?')
		return response
