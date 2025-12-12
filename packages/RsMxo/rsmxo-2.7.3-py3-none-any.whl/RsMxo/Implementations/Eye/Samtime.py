from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SamtimeCls:
	"""Samtime commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("samtime", core, parent)

	def set(self, sampling_time: float, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:SAMTime \n
		Snippet: driver.eye.samtime.set(sampling_time = 1.0, eye = repcap.Eye.Default) \n
		Sets a sampling time for the clock signal, an offset for the clock edge in relation to the bit start. \n
			:param sampling_time: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(sampling_time)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:SAMTime {param}')

	def get(self, eye=repcap.Eye.Default) -> float:
		"""EYE<*>:SAMTime \n
		Snippet: value: float = driver.eye.samtime.get(eye = repcap.Eye.Default) \n
		Sets a sampling time for the clock signal, an offset for the clock edge in relation to the bit start. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: sampling_time: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:SAMTime?')
		return Conversions.str_to_float(response)
