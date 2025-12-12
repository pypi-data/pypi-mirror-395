from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AddCls:
	"""Add commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("add", core, parent)

	def set(self, histogram=repcap.Histogram.Default) -> None:
		"""HISTogram<*>:ADD \n
		Snippet: driver.histogram.add.set(histogram = repcap.Histogram.Default) \n
		Creates a new histogram with the specified index. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
		"""
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		self._core.io.write(f'HISTogram{histogram_cmd_val}:ADD')

	def set_and_wait(self, histogram=repcap.Histogram.Default, opc_timeout_ms: int = -1) -> None:
		histogram_cmd_val = self._cmd_group.get_repcap_cmd_value(histogram, repcap.Histogram)
		"""HISTogram<*>:ADD \n
		Snippet: driver.histogram.add.set_and_wait(histogram = repcap.Histogram.Default) \n
		Creates a new histogram with the specified index. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param histogram: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Histogram')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'HISTogram{histogram_cmd_val}:ADD', opc_timeout_ms)
