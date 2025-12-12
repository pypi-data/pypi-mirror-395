from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OpenCls:
	"""Open commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("open", core, parent)

	def set(self, maskTest=repcap.MaskTest.Default) -> None:
		"""MTESt<*>:IMEXport:OPEN \n
		Snippet: driver.mtest.imExport.open.set(maskTest = repcap.MaskTest.Default) \n
		Opens and loads the mask selected by method RsMxo.Mtest.ImExport.Name.set. \n
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
		"""
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		self._core.io.write(f'MTESt{maskTest_cmd_val}:IMEXport:OPEN')

	def set_and_wait(self, maskTest=repcap.MaskTest.Default, opc_timeout_ms: int = -1) -> None:
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		"""MTESt<*>:IMEXport:OPEN \n
		Snippet: driver.mtest.imExport.open.set_and_wait(maskTest = repcap.MaskTest.Default) \n
		Opens and loads the mask selected by method RsMxo.Mtest.ImExport.Name.set. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'MTESt{maskTest_cmd_val}:IMEXport:OPEN', opc_timeout_ms)

	def get(self, maskTest=repcap.MaskTest.Default) -> bool:
		"""MTESt<*>:IMEXport:OPEN \n
		Snippet: value: bool = driver.mtest.imExport.open.get(maskTest = repcap.MaskTest.Default) \n
		Opens and loads the mask selected by method RsMxo.Mtest.ImExport.Name.set. \n
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:return: success: No help available"""
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		response = self._core.io.query_str(f'MTESt{maskTest_cmd_val}:IMEXport:OPEN?')
		return Conversions.str_to_bool(response)
