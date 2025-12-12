from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RemoveCls:
	"""Remove commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("remove", core, parent)

	def set(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default, segment=repcap.Segment.Default) -> None:
		"""POWer<*>:SOA:MTESt<*>:SEGMent<*>:REMove \n
		Snippet: driver.power.soa.mtest.segment.remove.set(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default, segment = repcap.Segment.Default) \n
		Deletes the specified mask segment. When a segment is deleted, the remaining segments are reordered. For example, there
		are 3 segments (1, 2, 3) . When you delete segment 2, then segment 3 gets the index 2. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		segment_cmd_val = self._cmd_group.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:SEGMent{segment_cmd_val}:REMove')

	def set_and_wait(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default, segment=repcap.Segment.Default, opc_timeout_ms: int = -1) -> None:
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		segment_cmd_val = self._cmd_group.get_repcap_cmd_value(segment, repcap.Segment)
		"""POWer<*>:SOA:MTESt<*>:SEGMent<*>:REMove \n
		Snippet: driver.power.soa.mtest.segment.remove.set_and_wait(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default, segment = repcap.Segment.Default) \n
		Deletes the specified mask segment. When a segment is deleted, the remaining segments are reordered. For example, there
		are 3 segments (1, 2, 3) . When you delete segment 2, then segment 3 gets the index 2. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:SEGMent{segment_cmd_val}:REMove', opc_timeout_ms)
