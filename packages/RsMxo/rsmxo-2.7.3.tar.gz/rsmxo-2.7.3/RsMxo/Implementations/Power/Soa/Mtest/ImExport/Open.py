from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OpenCls:
	"""Open commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("open", core, parent)

	def set(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default) -> None:
		"""POWer<*>:SOA:MTESt<*>:IMEXport:OPEN \n
		Snippet: driver.power.soa.mtest.imExport.open.set(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default) \n
		Opens and loads the mask selected by method RsMxo.Power.Soa.Mtest.ImExport.Name.set. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
		"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:IMEXport:OPEN')

	def set_and_wait(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default, opc_timeout_ms: int = -1) -> None:
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		"""POWer<*>:SOA:MTESt<*>:IMEXport:OPEN \n
		Snippet: driver.power.soa.mtest.imExport.open.set_and_wait(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default) \n
		Opens and loads the mask selected by method RsMxo.Power.Soa.Mtest.ImExport.Name.set. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:IMEXport:OPEN', opc_timeout_ms)

	def get(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default) -> bool:
		"""POWer<*>:SOA:MTESt<*>:IMEXport:OPEN \n
		Snippet: value: bool = driver.power.soa.mtest.imExport.open.get(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default) \n
		Opens and loads the mask selected by method RsMxo.Power.Soa.Mtest.ImExport.Name.set. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:return: success: No help available"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:IMEXport:OPEN?')
		return Conversions.str_to_bool(response)
