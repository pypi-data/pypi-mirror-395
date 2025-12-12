from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SaveCls:
	"""Save commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("save", core, parent)

	def set(self, histogram=repcap.Histogram.Default) -> None:
		"""EXPort:HISTogram<*>:SAVE \n
		Snippet: driver.export.histogram.save.set(histogram = repcap.Histogram.Default) \n
		Saves the specified histogram to file. The target file is set using method RsMxo.Export.Histogram.Name.set. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'EXPort:HISTogram{histogram_cmd_val}:SAVE')

	def set_and_wait(self, histogram=repcap.Histogram.Default, opc_timeout_ms: int = -1) -> None:
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		"""EXPort:HISTogram<*>:SAVE \n
		Snippet: driver.export.histogram.save.set_and_wait(histogram = repcap.Histogram.Default) \n
		Saves the specified histogram to file. The target file is set using method RsMxo.Export.Histogram.Name.set. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'EXPort:HISTogram{histogram_cmd_val}:SAVE', opc_timeout_ms)

	def get(self, histogram=repcap.Histogram.Default) -> bool:
		"""EXPort:HISTogram<*>:SAVE \n
		Snippet: value: bool = driver.export.histogram.save.get(histogram = repcap.Histogram.Default) \n
		Saves the specified histogram to file. The target file is set using method RsMxo.Export.Histogram.Name.set. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:return: success: No help available"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		response = self._core.io.query_str(f'EXPort:HISTogram{histogram_cmd_val}:SAVE?')
		return Conversions.str_to_bool(response)
