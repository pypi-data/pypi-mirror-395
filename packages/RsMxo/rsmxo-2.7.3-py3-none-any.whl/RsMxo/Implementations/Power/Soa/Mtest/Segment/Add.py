from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AddCls:
	"""Add commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("add", core, parent)

	def set(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default, segment=repcap.Segment.Default) -> None:
		"""POWer<*>:SOA:MTESt<*>:SEGMent<*>:ADD \n
		Snippet: driver.power.soa.mtest.segment.add.set(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default, segment = repcap.Segment.Default) \n
		Adds a new segment to the SOA mask. Consider the order of the segments (1, 2, 3, 4) and use the next free segment index.
		If the specified segment index already exists, the given number is ignored and the new segment gets the next free index.
		The new segment has no points. Use method RsMxo.Power.Soa.Mtest.Segment.Point.Add.set to add the points. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
		"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		segment_cmd_val = self._cmd_group.get_repcap_cmd_value(segment, repcap.Segment)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:SEGMent{segment_cmd_val}:ADD')

	def set_and_wait(self, power=repcap.Power.Default, maskTest=repcap.MaskTest.Default, segment=repcap.Segment.Default, opc_timeout_ms: int = -1) -> None:
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		maskTest_cmd_val = self._cmd_group.get_repcap_cmd_value(maskTest, repcap.MaskTest)
		segment_cmd_val = self._cmd_group.get_repcap_cmd_value(segment, repcap.Segment)
		"""POWer<*>:SOA:MTESt<*>:SEGMent<*>:ADD \n
		Snippet: driver.power.soa.mtest.segment.add.set_and_wait(power = repcap.Power.Default, maskTest = repcap.MaskTest.Default, segment = repcap.Segment.Default) \n
		Adds a new segment to the SOA mask. Consider the order of the segments (1, 2, 3, 4) and use the next free segment index.
		If the specified segment index already exists, the given number is ignored and the new segment gets the next free index.
		The new segment has no points. Use method RsMxo.Power.Soa.Mtest.Segment.Point.Add.set to add the points. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param maskTest: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mtest')
			:param segment: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Segment')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'POWer{power_cmd_val}:SOA:MTESt{maskTest_cmd_val}:SEGMent{segment_cmd_val}:ADD', opc_timeout_ms)
