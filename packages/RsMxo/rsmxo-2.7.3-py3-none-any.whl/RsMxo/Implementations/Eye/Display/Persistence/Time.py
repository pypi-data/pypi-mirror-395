from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TimeCls:
	"""Time commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	def set(self, time: float, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:DISPlay:PERSistence:TIME \n
		Snippet: driver.eye.display.persistence.time.set(time = 1.0, eye = repcap.Eye.Default) \n
		Sets the time how long the eye points remain on the display. \n
			:param time: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(time)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:DISPlay:PERSistence:TIME {param}')

	def get(self, eye=repcap.Eye.Default) -> float:
		"""EYE<*>:DISPlay:PERSistence:TIME \n
		Snippet: value: float = driver.eye.display.persistence.time.get(eye = repcap.Eye.Default) \n
		Sets the time how long the eye points remain on the display. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: time: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:DISPlay:PERSistence:TIME?')
		return Conversions.str_to_float(response)
