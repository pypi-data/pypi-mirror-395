from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ApplyCls:
	"""Apply commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("apply", core, parent)

	def set(self, power=repcap.Power.Default) -> None:
		"""POWer<*>:SOA:LIMit:APPLy \n
		Snippet: driver.power.soa.limit.apply.set(power = repcap.Power.Default) \n
		Generates a mask using the given maximum values. The result is mask segment in the first quadrant of the XY-diagram. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		self._core.io.write(f'POWer{power_cmd_val}:SOA:LIMit:APPLy')

	def set_and_wait(self, power=repcap.Power.Default, opc_timeout_ms: int = -1) -> None:
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		"""POWer<*>:SOA:LIMit:APPLy \n
		Snippet: driver.power.soa.limit.apply.set_and_wait(power = repcap.Power.Default) \n
		Generates a mask using the given maximum values. The result is mask segment in the first quadrant of the XY-diagram. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsMxo.utilities.opc_timeout_set() to set the timeout value. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'POWer{power_cmd_val}:SOA:LIMit:APPLy', opc_timeout_ms)
