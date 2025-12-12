from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class InfiniteCls:
	"""Infinite commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("infinite", core, parent)

	def set(self, inf_persist: bool, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:DISPlay:PERSistence:INFinite \n
		Snippet: driver.eye.display.persistence.infinite.set(inf_persist = False, eye = repcap.Eye.Default) \n
		If infinite persistence is ON, each new waveform point remains on the screen until this option is disabled, or the
		display is reset. \n
			:param inf_persist: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.bool_to_str(inf_persist)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:DISPlay:PERSistence:INFinite {param}')

	def get(self, eye=repcap.Eye.Default) -> bool:
		"""EYE<*>:DISPlay:PERSistence:INFinite \n
		Snippet: value: bool = driver.eye.display.persistence.infinite.get(eye = repcap.Eye.Default) \n
		If infinite persistence is ON, each new waveform point remains on the screen until this option is disabled, or the
		display is reset. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: inf_persist: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:DISPlay:PERSistence:INFinite?')
		return Conversions.str_to_bool(response)
