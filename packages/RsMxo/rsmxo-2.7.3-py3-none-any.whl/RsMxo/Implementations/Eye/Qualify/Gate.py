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

	def set(self, gate: float, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:QUALify:GATE \n
		Snippet: driver.eye.qualify.gate.set(gate = 1.0, eye = repcap.Eye.Default) \n
		Selects the timing reference, which defines the reference signal and the method that are used to obtain the timing
		information required to slice the data source waveform. Enable and configure a gate before you assign it (method RsMxo.
		Gate.Enable.set =ON) . The query returns 0, if no gate is assigned. \n
			:param gate: Number of the gate to be used
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(gate)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:QUALify:GATE {param}')

	def get(self, eye=repcap.Eye.Default) -> float:
		"""EYE<*>:QUALify:GATE \n
		Snippet: value: float = driver.eye.qualify.gate.get(eye = repcap.Eye.Default) \n
		Selects the timing reference, which defines the reference signal and the method that are used to obtain the timing
		information required to slice the data source waveform. Enable and configure a gate before you assign it (method RsMxo.
		Gate.Enable.set =ON) . The query returns 0, if no gate is assigned. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: gate: Number of the gate to be used"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:QUALify:GATE?')
		return Conversions.str_to_float(response)
