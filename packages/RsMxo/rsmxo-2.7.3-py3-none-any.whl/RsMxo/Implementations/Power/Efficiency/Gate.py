from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GateCls:
	"""Gate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gate", core, parent)

	def set(self, gate: int, power=repcap.Power.Default) -> None:
		"""POWer<*>:EFFiciency:GATE \n
		Snippet: driver.power.efficiency.gate.set(gate = 1, power = repcap.Power.Default) \n
		Sets the gate for the specified efficiency analysis. Configure the gate before you can assign it. Make sure that the
		suffix matches the power effciency measurement. \n
			:param gate: 0 to 8, index of the assigned gate. The value 0 indicates that no gate is assigned.
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
		"""
		param = Conversions.decimal_value_to_str(gate)
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		self._core.io.write(f'POWer{power_cmd_val}:EFFiciency:GATE {param}')

	def get(self, power=repcap.Power.Default) -> int:
		"""POWer<*>:EFFiciency:GATE \n
		Snippet: value: int = driver.power.efficiency.gate.get(power = repcap.Power.Default) \n
		Sets the gate for the specified efficiency analysis. Configure the gate before you can assign it. Make sure that the
		suffix matches the power effciency measurement. \n
			:param power: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Power')
			:return: gate: 0 to 8, index of the assigned gate. The value 0 indicates that no gate is assigned."""
		power_cmd_val = self._cmd_group.get_repcap_cmd_value(power, repcap.Power)
		response = self._core.io.query_str(f'POWer{power_cmd_val}:EFFiciency:GATE?')
		return Conversions.str_to_int(response)
