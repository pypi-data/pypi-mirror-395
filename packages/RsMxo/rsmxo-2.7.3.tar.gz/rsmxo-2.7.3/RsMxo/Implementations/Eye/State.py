from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StateCls:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, state: bool, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:STATe \n
		Snippet: driver.eye.state.set(state = False, eye = repcap.Eye.Default) \n
		Activates or deactivates the eye diagram. \n
			:param state: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.bool_to_str(state)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:STATe {param}')

	def get(self, eye=repcap.Eye.Default) -> bool:
		"""EYE<*>:STATe \n
		Snippet: value: bool = driver.eye.state.get(eye = repcap.Eye.Default) \n
		Activates or deactivates the eye diagram. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: state: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
