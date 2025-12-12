from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class NameCls:
	"""Name commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("name", core, parent)

	def set(self, save_as_path: str, histogram=repcap.Histogram.Default) -> None:
		"""EXPort:HISTogram<*>:NAME \n
		Snippet: driver.export.histogram.name.set(save_as_path = 'abc', histogram = repcap.Histogram.Default) \n
		Sets the path, the filename and the file format of the export file for histogram. The command affects all histogram
		exports. \n
			:param save_as_path: String with path and file name with extension .csv.
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		param = Conversions.value_to_quoted_str(save_as_path)
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'EXPort:HISTogram{histogram_cmd_val}:NAME {param}')

	def get(self, histogram=repcap.Histogram.Default) -> str:
		"""EXPort:HISTogram<*>:NAME \n
		Snippet: value: str = driver.export.histogram.name.get(histogram = repcap.Histogram.Default) \n
		Sets the path, the filename and the file format of the export file for histogram. The command affects all histogram
		exports. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: save_as_path: String with path and file name with extension .csv."""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'EXPort:HISTogram{histogram_cmd_val}:NAME?')
		return trim_str_response(response)
