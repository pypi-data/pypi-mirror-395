from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MslicesCls:
	"""Mslices commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mslices", core, parent)

	def set(self, max_slice_count: int, eye=repcap.Eye.Default) -> None:
		"""EYE<*>:MSLices \n
		Snippet: driver.eye.mslices.set(max_slice_count = 1, eye = repcap.Eye.Default) \n
		Sets the number of waveform slices for a single acquisition. \n
			:param max_slice_count: No help available
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
		"""
		param = Conversions.decimal_value_to_str(max_slice_count)
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		self._core.io.write(f'EYE{eye_cmd_val}:MSLices {param}')

	def get(self, eye=repcap.Eye.Default) -> int:
		"""EYE<*>:MSLices \n
		Snippet: value: int = driver.eye.mslices.get(eye = repcap.Eye.Default) \n
		Sets the number of waveform slices for a single acquisition. \n
			:param eye: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Eye')
			:return: max_slice_count: No help available"""
		eye_cmd_val = self._cmd_group.get_repcap_cmd_value(eye, repcap.Eye)
		response = self._core.io.query_str(f'EYE{eye_cmd_val}:MSLices?')
		return Conversions.str_to_int(response)
