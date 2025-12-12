from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ScaleCls:
	"""Scale commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scale", core, parent)

	def set(self, vertical_scale: float, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:VERTical:SCALe \n
		Snippet: driver.eye.vertical.scale.set(vertical_scale = 1.0, eye = repcap.Eye.Default) \n
		Defines the vertical scale in Volts per division if method RsMxo.Eye.Vertical.Couple.set is OFF. If coupling is ON, the
		query returns the coupled value. \n
			:param vertical_scale: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(vertical_scale)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:VERTical:SCALe {param}')

	def get(self, eye=repcap.Eye.Default) -> float:
		"""EYE<*>:VERTical:SCALe \n
		Snippet: value: float = driver.eye.vertical.scale.get(eye = repcap.Eye.Default) \n
		Defines the vertical scale in Volts per division if method RsMxo.Eye.Vertical.Couple.set is OFF. If coupling is ON, the
		query returns the coupled value. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: vertical_scale: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:VERTical:SCALe?')
		return Conversions.str_to_float(response)
