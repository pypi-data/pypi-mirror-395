from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GateCls:
	"""Gate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gate", core, parent)

	def set(self, gate: float, timingReference=repcap.TimingReference.Default) -> None:
		"""TREFerence<*>:GATE \n
		Snippet: driver.treference.gate.set(gate = 1.0, timingReference = repcap.TimingReference.Default) \n
		Sets the gate for the timing reference. Enable and configure a gate before you assign it (method RsMxo.Gate.Enable.
		set =ON) . The query returns 0, if no gate is assigned. \n
			:param gate: Number of the gate to be used
			:param timingReference: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Treference')
		"""
		param = Conversions.decimal_value_to_str(gate)
		timingReference_cmd_val = self._cmd_group.get_repcap_cmd_value(timingReference, repcap.TimingReference)
		self._core.io.write(f'TREFerence{timingReference_cmd_val}:GATE {param}')

	def get(self, timingReference=repcap.TimingReference.Default) -> float:
		"""TREFerence<*>:GATE \n
		Snippet: value: float = driver.treference.gate.get(timingReference = repcap.TimingReference.Default) \n
		Sets the gate for the timing reference. Enable and configure a gate before you assign it (method RsMxo.Gate.Enable.
		set =ON) . The query returns 0, if no gate is assigned. \n
			:param timingReference: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Treference')
			:return: gate: Number of the gate to be used"""
		timingReference_cmd_val = self._cmd_group.get_repcap_cmd_value(timingReference, repcap.TimingReference)
		response = self._core.io.query_str(f'TREFerence{timingReference_cmd_val}:GATE?')
		return Conversions.str_to_float(response)
